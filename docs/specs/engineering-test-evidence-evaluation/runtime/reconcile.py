"""Validate trial accounting and emit protocol-level observations."""
import argparse
from collections import Counter
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "controller/trials.json"
FIXTURES = ROOT / "controller/fixture-revisions.json"


def read_json(path):
    return json.loads(path.read_text())


def records(path):
    if path.is_file():
        for line in path.read_text().splitlines():
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def counts(attempt):
    events = list(records(attempt / "events.jsonl"))
    commands = sum(
        event["type"] == "item.completed"
        and event.get("item", {}).get("type") == "command_execution" for event in events
    )
    child_sessions = 0
    shell_calls = 0
    for path in sorted(attempt.glob("session-*.jsonl.gz")):
        child_sessions += 1
        with gzip.open(path, mode="rt") as file:
            for line in file:
                payload = json.loads(line)["payload"]
                if payload.get("type") == "custom_tool_call" and payload.get("name") == "exec":
                    shell_calls += payload.get("input", "").count("tools.exec_command(")
    return {
        "top_level_completed_commands": commands,
        "recorded_sessions_including_root": child_sessions,
        "shell_call_expressions_in_session_traces": shell_calls,
    }


def reconcile(evidence, scores_file):
    plan = read_json(PLAN)["trials"]
    fixtures = read_json(FIXTURES)
    scores = read_json(scores_file)
    ids = [entry["id"] for entry in plan]
    assert len(ids) == len(set(ids)), "Duplicate planned trial"
    assert len(scores) == len({entry["id"] for entry in scores}), "Duplicate score"
    by_id = {entry["id"]: entry for entry in scores}
    assert set(ids) == set(by_id), "Missing or unexpected scores"
    assert set(ids) == {path.name for path in evidence.iterdir() if path.is_dir()}, "Missing or unexpected trial logs"
    first_status = Counter()
    score_count = Counter()
    all_status = Counter()
    all_rows = []
    for trial in plan:
        trial_id = trial["id"]
        paths = sorted((evidence / trial_id).glob("attempt-*"))
        assert 1 <= len(paths) <= 2, f"Unexpected attempt count for {trial_id}"
        attempts = []
        for index, path in enumerate(paths, 1):
            assert path.name == f"attempt-{index}", path
            outcome = read_json(path / "outcome.json")
            assert outcome["trial"] == trial_id and outcome["attempt"] == index, path
            assert outcome["skill"] == trial["skill"], path
            if outcome["status"] != "setup-failed-before-dispatch":
                assert outcome["fixture"] == fixtures[trial["fixture"]], path
                assert "Pass:" in (path / "isolation.txt").read_text(), path
                prompt = (path / "prompt.txt").read_text()
                assert prompt.endswith(trial["prompt"] + "\n"), path
            row = {**outcome, **counts(path)}
            all_status[row["status"]] += 1
            attempts.append(row)
        if len(attempts) == 2:
            assert attempts[0]["status"] == "runtime-failed-before-interaction", trial_id
        score = by_id[trial_id]["score"]
        assert score in {"met", "missed", "unobserved"}, trial_id
        first_status[attempts[0]["status"]] += 1
        score_count[score] += 1
        all_rows.append({"id": trial_id, "score": score, "attempts": attempts})
    return {
        "planned": len(ids),
        "first_status": first_status,
        "all_status": all_status,
        "first_scores": score_count,
        "results": all_rows,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("scores", type=Path)
    args = parser.parse_args()
    print(json.dumps(reconcile(args.evidence, args.scores), indent=2))
