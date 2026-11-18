"""Validate trial accounting and emit protocol-level observations."""
import argparse
from collections import Counter
import gzip
import json
import math
from pathlib import Path

from trial_events import INTERACTION_RECORD_TYPES, classify, records

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "controller/trials.json"
FIXTURES = ROOT / "controller/fixture-revisions.json"


def read_json(path):
    return json.loads(path.read_text())


def trial_events(attempt, outcome):
    status = outcome["status"]
    event_path = attempt / "events.jsonl"
    if status == "setup-failed-before-dispatch":
        assert outcome.get("error"), attempt
        process_fields = {"launch", "exit_code", "timed_out", "timeout_seconds",
                          "elapsed_seconds", "usage", "truncated_event_tail"}
        assert process_fields.isdisjoint(outcome), attempt
        assert not event_path.exists() or not event_path.read_bytes(), attempt
        assert not list(attempt.glob("session-*.jsonl.gz")), attempt
        assert not (attempt / "tree.json").exists(), attempt
        return []

    launch = outcome.get("launch")
    assert isinstance(launch, list) and launch and all(isinstance(arg, str) for arg in launch), attempt
    timeout = outcome["timeout_seconds"]
    elapsed = outcome["elapsed_seconds"]
    assert type(timeout) in {int, float} and math.isfinite(timeout) and timeout > 0, attempt
    assert type(elapsed) in {int, float} and math.isfinite(elapsed) and elapsed >= 0, attempt
    timed_out = outcome.get("timed_out", False)
    assert type(timed_out) is bool, attempt
    assert not timed_out or elapsed >= timeout, attempt

    tail = {}
    interrupted = timed_out or outcome.get("exit_code") != 0
    events = [event for _, event in records(event_path, truncated=tail if interrupted else None)]
    assert tail == outcome.get("truncated_event_tail", {}), attempt
    expected = classify(events, exit_code=outcome.get("exit_code"), timed_out=timed_out)
    assert status == expected, f"{attempt}: recorded {status}, evidence implies {expected}"
    if status == "completed":
        assert events[-1].get("usage") == outcome.get("usage"), attempt
    else:
        assert "usage" not in outcome, attempt
    return events


def counts(attempt, outcome):
    events = trial_events(attempt, outcome)
    status = outcome["status"]
    if status != "setup-failed-before-dispatch":
        assert (attempt / "stderr.txt").is_file(), attempt
        tree = attempt / "tree.json"
        if tree.is_file():
            commands = read_json(tree)
            assert isinstance(commands, list) and commands, tree
            assert all(isinstance(row["command"], list) and isinstance(row["output"], str)
                       for row in commands), tree
        else:
            assert outcome.get("collection_error"), tree
    commands = sum(
        event["type"] == "item.completed"
        and event.get("item", {}).get("type") == "command_execution" for event in events
    )
    child_sessions = 0
    shell_calls = 0
    has_interaction_evidence = False
    for path in sorted(attempt.glob("session-*.jsonl.gz")):
        child_sessions += 1
        previous_line = 0
        with gzip.open(path, mode="rt") as file:
            for line in file:
                entry = json.loads(line)
                source_line = entry["source_line"]
                assert isinstance(source_line, int) and source_line > previous_line, path
                assert entry["type"] in {"response_item", "event_msg"}, path
                previous_line = source_line
                payload = entry["payload"]
                if payload.get("type") in INTERACTION_RECORD_TYPES:
                    has_interaction_evidence = True
                if payload.get("type") == "custom_tool_call" and payload.get("name") == "exec":
                    shell_calls += payload.get("input", "").count("tools.exec_command(")
        assert previous_line, f"Empty session trace: {path}"
    contacted_agent = status == "completed" or any(
        event["type"].startswith("item.") for event in events
    )
    if contacted_agent:
        assert has_interaction_evidence, f"Missing interaction evidence: {attempt}"
    return {
        "top_level_completed_commands": commands,
        "recorded_sessions_including_root": child_sessions,
        "shell_call_expressions_in_session_traces": shell_calls,
    }


def reconcile(evidence, scores_file, group):
    if not __debug__:
        raise RuntimeError("Reconciliation requires Python assertions enabled")
    if group == "clean":
        clean = ROOT / "controller/clean-refactor"
        plan = read_json(clean / "trials.json")["trials"]
        fixtures = read_json(clean / "fixture-revisions.json")
    else:
        plan = read_json(PLAN)["trials"]
        fixtures = read_json(FIXTURES)
    if group == "git":
        expected = read_json(ROOT / "runtime/git_recovery.json")["trials"]
        plan = [trial for trial in plan if trial["id"] in expected]
        assert len(plan) == len(expected), "Missing Git recovery entries"
    timeouts = read_json(ROOT / "runtime/runtime.json")["timeouts_seconds"]
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
                assert outcome["starting_head"] == fixtures[trial["fixture"]]["candidate"], path
                assert outcome["timeout_seconds"] == timeouts.get(trial["skill"], timeouts["default"]), path
                assert "Pass:" in (path / "isolation.txt").read_text(), path
                prompt = (path / "prompt.txt").read_text()
                assert prompt.endswith(trial["prompt"] + "\n"), path
            row = {**outcome, **counts(path, outcome)}
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
    parser.add_argument("--group", choices=("primary", "git", "clean"), default="primary")
    args = parser.parse_args()
    print(json.dumps(reconcile(args.evidence, args.scores, args.group), indent=2))
