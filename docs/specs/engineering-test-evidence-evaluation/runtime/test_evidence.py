"""Model-free checks for collector and reconciliation failure modes."""
import gzip
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import export_evidence
import reconcile
import run


START = [{"type": "thread.started"}, {"type": "turn.started"}]
COMPLETED = {"type": "turn.completed", "usage": {"output_tokens": 3}}


def jsonl(rows):
    return "".join(json.dumps(row) + "\n" for row in rows).encode()


class EvidenceTest(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def test_status_requires_consistent_dispatch_exit_terminal_and_timeout(self):
        path = self.root / "events.jsonl"
        running = {"launch": ["codex"], "timeout_seconds": 1, "elapsed_seconds": 1.1}
        completed = {**running, "status": "completed", "exit_code": 0, "usage": COMPLETED["usage"]}
        started_item = {"type": "item.started"}
        for events, outcome, valid in [
            ([*START, COMPLETED], completed, True),
            ([*START, COMPLETED], {**completed, "status": "bogus", "exit_code": 99}, False),
            ([*START, COMPLETED], {**completed, "status": "bogus"}, False),
            ([*START, COMPLETED], {**completed, "status": "interrupted-after-interaction"}, False),
            ([*START, COMPLETED, COMPLETED], completed, False),
            ([*START, started_item], completed, False),
            (START, {**running, "status": "runtime-failed-before-interaction", "exit_code": 2}, True),
            ([*START, started_item], {**running, "status": "interrupted-after-interaction", "exit_code": 2}, True),
            ([*START, started_item], {**running, "status": "runtime-failed-before-interaction", "exit_code": 2}, False),
            (START, {**running, "status": "interrupted-after-interaction", "exit_code": 2}, False),
            (START, {**running, "status": "runtime-failed-before-interaction", "exit_code": 0}, False),
            (START, {**running, "status": "budget-exhausted", "timed_out": True}, True),
            (START, {**running, "status": "budget-exhausted", "timed_out": True, "exit_code": 2}, False),
            (START, {**running, "status": "budget-exhausted", "timed_out": True, "elapsed_seconds": 0.5}, False),
            ([*START, COMPLETED], {**running, "status": "budget-exhausted", "timed_out": True}, False),
            ([], {"status": "setup-failed-before-dispatch", "error": "could not launch"}, True),
            ([], {**running, "status": "setup-failed-before-dispatch", "error": "could not launch"}, False),
            (START, {"status": "setup-failed-before-dispatch", "error": "could not launch"}, False),
        ]:
            with self.subTest(events=events, outcome=outcome):
                path.write_bytes(jsonl(events))
                if valid:
                    self.assertEqual(reconcile.trial_events(self.root, outcome), events)
                else:
                    with self.assertRaises((AssertionError, ValueError)):
                        reconcile.trial_events(self.root, outcome)

    def test_reconciliation_fails_closed_with_assertions_disabled(self):
        result = subprocess.run(
            [sys.executable, "-B", "-O", reconcile.__file__, str(self.root), str(self.root / "scores.json")],
            capture_output=True, text=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Reconciliation requires Python assertions enabled", result.stderr)

    def test_timeout_preserves_split_utf8_and_session_trace(self):
        self.root.joinpath("results").mkdir()
        script = self.root / "fake_cli.py"
        events = [*START, {"type": "item.started"}]
        tail = b'{"type":"item.completed","text":"\xe2\x82'
        script.write_text(
            "import os, sys, time\n"
            "from pathlib import Path\n"
            "sessions = Path(os.environ['CODEX_HOME']) / 'sessions'\n"
            "sessions.mkdir(parents=True)\n"
            "sessions.joinpath('child.jsonl').write_text('{}\\n')\n"
            f"sys.stdout.buffer.write({jsonl(events) + tail!r})\n"
            "sys.stdout.buffer.flush()\n"
            "time.sleep(10)\n"
        )
        fixture = {"base": "a", "candidate": "a"}
        args = SimpleNamespace(
            results=self.root / "results", fixtures={"sample": {**fixture, "working_tree_sha256": "hash"}},
            source=None, auth=None, package=None, revision=None, protected=[], writable_fixture_git=False,
        )

        def build(job, repo, *_args, **_kwargs):
            repo.mkdir()
            return [sys.executable, str(script)], {"CODEX_HOME": str(job / "config")}, job

        def save(*_args):
            raise OSError("test collector unavailable")

        with (patch.object(run, "build_trial", side_effect=build),
              patch.object(run, "capture", return_value=json.dumps(fixture)),
              patch.object(run, "git", return_value="a"),
              patch.object(run, "working_tree_hash", return_value="hash"),
              patch.object(run, "verify"),
              patch.object(run, "save_tree", side_effect=save),
              patch.dict(run.PROTOCOL["timeouts_seconds"], default=1)):
            run.run_trial({"id": "sample", "fixture": "sample", "skill": "skill", "prompt": "Check"}, args, self.root)
        evidence = args.results / "sample/attempt-1"
        outcome = json.loads((evidence / "outcome.json").read_text())
        self.assertEqual("budget-exhausted", outcome["status"])
        self.assertEqual(len(tail), outcome["truncated_event_tail"]["byte_count"])
        self.assertEqual(jsonl(events) + tail, (evidence / "events.jsonl").read_bytes())
        self.assertEqual("{}\n", (evidence / "session-1.jsonl").read_text())
        self.assertEqual(events, reconcile.trial_events(evidence, outcome))

    def test_export_rejects_interior_errors_and_records_only_interrupted_tail(self):
        attempt = self.root / "raw/sample/attempt-1"
        attempt.mkdir(parents=True)
        outcome = attempt / "outcome.json"
        outcome.write_text(json.dumps({"status": "budget-exhausted"}))
        session = attempt / "session-1.jsonl"
        good = jsonl([{"type": "event_msg", "payload": {"type": "task_complete"}}])
        bad_tail = b'{"interrupted":"\xe2\x82'
        destination = self.root / "exported"
        session.write_bytes(good + bad_tail + b"\n" + good)
        with self.assertRaisesRegex(ValueError, "invalid JSONL record"):
            export_evidence.export(self.root / "raw", destination)
        self.assertFalse(destination.exists())

        session.write_bytes(good + bad_tail)
        outcome.write_text(json.dumps({"status": "completed"}))
        with self.assertRaisesRegex(ValueError, "invalid JSONL record"):
            export_evidence.export(self.root / "raw", destination)
        self.assertFalse(destination.exists())

        outcome.write_text(json.dumps({"status": "budget-exhausted"}))
        export_evidence.export(self.root / "raw", destination)
        exported = destination / "sample/attempt-1"
        tail = json.loads((exported / "truncated_sessions.json").read_text())["session-1.jsonl"]
        self.assertEqual((2, len(bad_tail)), (tail["source_line"], tail["byte_count"]))
        with gzip.open(exported / "session-1.jsonl.gz", "rt") as stream:
            self.assertEqual([1], [json.loads(line)["source_line"] for line in stream])
        self.assertEqual(good + bad_tail, session.read_bytes())

    def test_timeout_with_no_complete_session_actions_remains_reconcilable(self):
        attempt = self.root / "raw/sample/attempt-1"
        attempt.mkdir(parents=True)
        outcome = {
            "status": "budget-exhausted", "timed_out": True, "launch": ["codex"],
            "timeout_seconds": 1, "elapsed_seconds": 1.1, "collection_error": "not available",
        }
        (attempt / "outcome.json").write_text(json.dumps(outcome))
        (attempt / "stderr.txt").touch()
        session = attempt / "session-1.jsonl"
        metadata = jsonl([{"type": "session_meta", "payload": {}}])
        for name, suffix, actions_started in (
            ("metadata-only", b"", False),
            ("partial-action", b'{"type":"event_msg"', False),
            ("missing-action-evidence", b"", True),
        ):
            with self.subTest(case=name):
                events = [*START, {"type": "item.started"}] if actions_started else START
                (attempt / "events.jsonl").write_bytes(jsonl(events))
                session.write_bytes(metadata + suffix)
                destination = self.root / name
                export_evidence.export(self.root / "raw", destination)
                exported = destination / "sample/attempt-1"

                self.assertFalse((exported / "session-1.jsonl.gz").exists())
                tail_path = exported / "truncated_sessions.json"
                if suffix:
                    tail = json.loads(tail_path.read_text())
                    self.assertEqual(2, tail["session-1.jsonl"]["source_line"])
                else:
                    self.assertFalse(tail_path.exists())
                if actions_started:
                    with self.assertRaisesRegex(AssertionError, "Missing interaction evidence"):
                        reconcile.counts(exported, outcome)
                else:
                    self.assertEqual(0, reconcile.counts(exported, outcome)["recorded_sessions_including_root"])
                self.assertEqual(metadata + suffix, session.read_bytes())

    def test_interrupted_interaction_requires_more_than_telemetry(self):
        attempt = self.root / "raw/sample/attempt-1"
        attempt.mkdir(parents=True)
        outcome = {
            "status": "budget-exhausted", "timed_out": True, "launch": ["codex"],
            "timeout_seconds": 1, "elapsed_seconds": 1.1, "collection_error": "not available",
        }
        (attempt / "outcome.json").write_text(json.dumps(outcome))
        (attempt / "stderr.txt").touch()
        command = {"type": "command_execution", "command": "git status", "status": "in_progress"}
        (attempt / "events.jsonl").write_bytes(jsonl([*START, {"type": "item.started", "item": command}]))
        telemetry = {"type": "event_msg", "payload": {"type": "token_count", "info": {"total_tokens": 42}}}
        action = {"type": "response_item", "payload": {
            "type": "custom_tool_call", "name": "exec", "input": "tools.exec_command({cmd: 'git status'})",
        }}
        torn = b'{"type":"response_item","payload":'
        session = attempt / "session-1.jsonl"
        for name, actions in (("telemetry-only", []), ("with-action", [action])):
            with self.subTest(case=name):
                raw = jsonl([telemetry, *actions]) + torn
                session.write_bytes(raw)
                destination = self.root / name
                export_evidence.export(self.root / "raw", destination)
                exported = destination / "sample/attempt-1"
                with gzip.open(exported / "session-1.jsonl.gz", "rt") as stream:
                    self.assertEqual(
                        [row["payload"] for row in [telemetry, *actions]],
                        [json.loads(line)["payload"] for line in stream],
                    )
                tail = json.loads((exported / "truncated_sessions.json").read_text())
                self.assertEqual(len(actions) + 2, tail["session-1.jsonl"]["source_line"])
                self.assertEqual(raw, session.read_bytes())
                if actions:
                    self.assertEqual(1, reconcile.counts(exported, outcome)["recorded_sessions_including_root"])
                else:
                    with self.assertRaisesRegex(AssertionError, "Missing interaction evidence"):
                        reconcile.counts(exported, outcome)

    def test_collector_preserves_porcelain_columns_and_newline(self):
        repo = self.root / "repo"
        subprocess.run(["git", "init", "-q", "--template=", str(repo)], check=True)
        for name in ("a.txt", "b.txt"):
            (repo / name).write_text("before\n")
        subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(repo), "-c", "user.name=Example", "-c",
                        "user.email=example@example.invalid", "commit", "-qm", "initial"], check=True)
        first = run.git(repo, "rev-parse", "HEAD")
        for name in ("a.txt", "b.txt"):
            (repo / name).write_text("after\n")
        subprocess.run(["git", "-C", str(repo), "add", "b.txt"], check=True)
        shim = self.root / "sandbox_shim.py"
        shim.write_text("import os, sys\nargs = sys.argv[sys.argv.index('/usr/bin/git'):]\nos.execv(args[0], args)\n")
        tree = self.root / "tree.json"
        run.save_tree(repo, first, tree, [sys.executable, str(shim)], {})
        self.assertEqual(" M a.txt\nM  b.txt\n", json.loads(tree.read_text())[0]["output"])


if __name__ == "__main__":
    unittest.main()
