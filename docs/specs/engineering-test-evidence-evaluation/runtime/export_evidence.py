"""Export outcomes and observed actions without account or harness metadata."""
import argparse
import gzip
import json
from pathlib import Path
import shutil

ACTIONS = {
    "agent_message", "function_call", "function_call_output", "custom_tool_call",
    "custom_tool_call_output", "task_complete", "token_count", "error",
    "web_search_call", "mcp_tool_call",
}


def session_records(path):
    for line in path.read_text().splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = record.get("type")
        payload = record.get("payload", {})
        if payload.get("type") in ACTIONS and kind in {"response_item", "event_msg"}:
            payload.pop("internal_chat_message_metadata_passthrough", None)
            yield record


def export(results, destination):
    destination.mkdir()
    for trial in sorted(results.iterdir()):
        if not trial.is_dir():
            continue
        for attempt in sorted(trial.glob("attempt-*")):
            out = destination / trial.name / attempt.name
            out.mkdir(parents=True)
            for name in ("outcome.json", "prompt.txt", "isolation.txt", "stderr.txt", "events.jsonl", "tree.json"):
                source = attempt / name
                if source.is_file():
                    shutil.copyfile(source, out / name)
            for session in sorted(attempt.glob("session-*.jsonl")):
                lines = "".join(json.dumps(event) + "\n" for event in session_records(session))
                (out / f"{session.name}.gz").write_bytes(gzip.compress(lines.encode(), mtime=0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    export(args.results, args.destination)
