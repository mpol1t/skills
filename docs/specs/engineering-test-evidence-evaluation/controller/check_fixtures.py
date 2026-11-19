#!/usr/bin/env python3
"""Check fixture contracts and expected command outcomes without an agent."""

import json
from pathlib import Path
import subprocess
import tempfile

from freeze_fixtures import CASES, collect, materialize


CHECKS = {
    "quartz": [("./check", 0, "Branch outcomes: 2/2")],
    "elm": [("./check", 0, "Branch outcomes: 2/2")],
    "ochre": [("./check", 1, "cy-GB"), ("./check", 0, "OK")],
    "drift": [("./check", 75, "Assertions started: 0"), ("./check", 0, "OK")],
    "birch": [("./check", 1, "pending"), ("./check", 0, "OK")],
    "jade": [("./check 2026-03-15", 0, "quarantined"), ("./check 2026-04-03", 0, "test_region")],
    "plum": [(".githooks/pre-commit", 0, "OK"), (".github/checks/labels", 1, "2/4 (50%)")],
    "teal": [(".github/checks/labels", 0, "17/20 (85%)")],
    "agate": [(".github/checks/labels", 0, "29/50 (58%)")],
    "rose": [("python3 tools/coverage.py", 0, "Overall: 1/1")],
    "pearl": [
        ("python3 tools/combine.py", 1, "Missing coverage report for shard p3"),
        ("cp artifacts/archive/p3.json artifacts/current && python3 tools/combine.py", 0, "7/8"),
    ],
    "moss": [("python3 tools/coverage.py", 0, "Overall: 1/1")],
    "maple": [
        ("python3 tools/coverage.py", 0, "Overall: 1/1"),
        ("git show review-base:.coveragerc > .coveragerc && python3 tools/coverage.py", 1, "Overall: 1/2"),
    ],
    "jasper": [("python3 tools/coverage.py", 0, "Overall: 1/2")],
    "topaz": [("python3 tools/coverage.py", 0, "Overall: 4/5")],
}

DEFECT_PROBES = {
    "quartz": 'import app; assert app.decision(37) == "accept"',
    "saffron": 'from pathlib import Path; import app; assert app.read_catalog(Path("records/legacy.json")) == "Yarrow"',
    "elm": (
        'import app; state = {"paper": 3}; '
        'assert not app.reserve(state, lambda: (_ for _ in ()).throw(OSError())); '
        'assert state == {"paper": 3}'
    ),
    "reed": (
        'import app; seen = set(); output = []; '
        'assert app.receive("r9", seen, output.append) == app.receive("r9", seen, output.append) == "ack"; '
        'assert output == ["r9"]'
    ),
    "lilac": 'import app; assert app.label(4) == "bin:004"',
    "clover": 'from pathlib import Path; import app; assert app.read_catalog(Path("records/legacy.json")) == "Yarrow"',
}


def verify_fixtures():
    revisions = json.loads(collect())
    with tempfile.TemporaryDirectory() as temp:
        for case in CASES:
            directory = Path(temp) / case
            materialize(case, directory)
            for arguments in (["status", "--porcelain"], ["remote"]):
                output = subprocess.check_output(["git", *arguments], cwd=directory)
                if output:
                    raise ValueError(f"{case} has unexpected Git state: {output!r}")
            for command, expected_exit, expected_text in CHECKS.get(case, [("./check", 0, "OK")]):
                result = subprocess.run(command, cwd=directory, shell=True, text=True, capture_output=True)
                if result.returncode != expected_exit or expected_text not in result.stdout + result.stderr:
                    raise ValueError(f"{case}: {command}\n{result}")
            if case in DEFECT_PROBES:
                for revision, expect_success in ((revisions[case]["candidate"], False), (revisions[case]["base"], True)):
                    subprocess.run(["git", "checkout", "--quiet", revision], cwd=directory, check=True)
                    result = subprocess.run(
                        ["python3", "-B", "-c", DEFECT_PROBES[case]], cwd=directory, capture_output=True, text=True,
                    )
                    if (result.returncode == 0) != expect_success:
                        raise ValueError(f"{case}: defect probe at {revision}\n{result}")
    print(f"Verified command outcomes for {len(CASES)} fixtures and {len(DEFECT_PROBES)} defect probes at base and candidate.")


if __name__ == "__main__":
    verify_fixtures()
