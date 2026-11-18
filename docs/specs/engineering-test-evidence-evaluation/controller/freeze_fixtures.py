#!/usr/bin/env python3
"""Record or verify deterministic fixture commits and working-tree bytes."""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from materialize import materialize
from scenarios import CASES


def working_tree_hash(directory):
    digest = hashlib.sha256()
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory)
        if relative.parts[0] == ".git" or not path.is_file():
            continue
        entry = [relative.as_posix(), path.stat().st_mode & 0o111, path.read_bytes().hex()]
        digest.update(json.dumps(entry, separators=(",", ":")).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def collect():
    plan = json.loads((ROOT / "trials.json").read_text())["trials"]
    ids = [entry["fixture"] for entry in plan]
    if len(ids) != len(set(ids)) or set(ids) != set(CASES):
        raise SystemExit("Trial allocation does not cover each fixture once.")
    revisions = {}
    with tempfile.TemporaryDirectory() as temp:
        for case in ids:
            directory = Path(temp) / case
            revisions[case] = materialize(case, directory)
            revisions[case]["working_tree_sha256"] = working_tree_hash(directory)
    return json.dumps(revisions, indent=2, sort_keys=True) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = collect()
    if args.verify:
        if (ROOT / "fixture-revisions.json").read_text() != result:
            raise SystemExit("Frozen fixture revisions do not match.")
        print(f"Verified {len(CASES)} frozen fixture revisions.")
    else:
        print(result, end="")
