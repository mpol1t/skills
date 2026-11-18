"""Export outcomes and observed actions without account or harness metadata."""
import argparse
import gzip
import json
from pathlib import Path
import shutil
import tempfile

from trial_events import records

ACTIONS = {
    "agent_message", "function_call", "function_call_output", "custom_tool_call",
    "custom_tool_call_output", "task_complete", "token_count", "error",
    "web_search_call", "mcp_tool_call",
}


def session_records(path, *, truncated=None):
    for line_number, record in records(path, truncated=truncated):
        kind = record.get("type")
        payload = record.get("payload", {})
        if payload.get("type") in ACTIONS and kind in {"response_item", "event_msg"}:
            payload.pop("internal_chat_message_metadata_passthrough", None)
            payload.pop("rate_limits", None)
            yield {
                "timestamp": record.get("timestamp"),
                "type": kind,
                "source_line": line_number,
                "payload": payload,
            }


def export(results, destination):
    if destination.exists():
        raise FileExistsError(destination)
    with tempfile.TemporaryDirectory(prefix=".trace-export-", dir=destination.parent) as staging:
        pending = Path(staging) / "results"
        pending.mkdir()
        for trial in sorted(results.iterdir()):
            if not trial.is_dir():
                continue
            for attempt in sorted(trial.glob("attempt-*")):
                export_attempt(attempt, pending / trial.name / attempt.name)
        pending.rename(destination)


def export_attempt(attempt, out):
    outcome = json.loads((attempt / "outcome.json").read_text())
    interrupted = outcome["status"] in {
        "budget-exhausted", "interrupted-after-interaction", "runtime-failed-before-interaction",
    }
    out.mkdir(parents=True)
    for name in ("outcome.json", "prompt.txt", "isolation.txt", "stderr.txt", "events.jsonl", "tree.json"):
        source = attempt / name
        if source.is_file():
            shutil.copyfile(source, out / name)

    truncated_sessions = {}
    for session in sorted(attempt.glob("session-*.jsonl")):
        tail = {}
        lines = "".join(
            json.dumps(event) + "\n"
            for event in session_records(session, truncated=tail if interrupted else None)
        )
        if lines or not interrupted:
            (out / f"{session.name}.gz").write_bytes(gzip.compress(lines.encode(), mtime=0))
        if tail:
            truncated_sessions[session.name] = tail
    if truncated_sessions:
        (out / "truncated_sessions.json").write_text(json.dumps(truncated_sessions, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    export(args.results, args.destination)
