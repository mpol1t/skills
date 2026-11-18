#!/usr/bin/env python3
"""Materialize one deterministic Git fixture in a new directory."""

import argparse
import json
import os
from pathlib import Path
import subprocess

from scenarios import CASES

BASE_FILES = {
    ".gitignore": "__pycache__/\n.run-state/\n",
    "README.md": "# Example project\n\nRun ./check. See CONTRACT.md for caller-facing requirements.\n",
    "check": '#!/bin/sh\nset -eu\ncd "$(dirname "$0")"\nexec python3 -m unittest discover -v "$@"\n',
}

GIT_ENV = {
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_AUTHOR_NAME": "Fixture Author",
    "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
    "GIT_COMMITTER_NAME": "Fixture Author",
    "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
    "GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z",
    "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z",
}


def git(directory, *arguments):
    return subprocess.check_output(
        ["git", "-C", str(directory), *arguments],
        env={**os.environ, **GIT_ENV},
        text=True,
    ).strip()


def install(directory, files):
    for relative, content in files.items():
        path = directory / relative
        if content is None:
            path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        if content.startswith("#!"):
            path.chmod(0o755)


def checkpoint(directory, message):
    git(directory, "add", "-A")
    git(directory, "-c", "commit.gpgsign=false", "commit", "-qm", message)
    return git(directory, "rev-parse", "HEAD")


def materialize(case_id, directory):
    base_files, change = CASES[case_id]
    directory.mkdir(parents=True)
    git(directory, "init", "-q", "--initial-branch=main", "--template=")
    git(directory, "config", "user.name", "Project Agent")
    git(directory, "config", "user.email", "agent@example.invalid")
    install(directory, BASE_FILES | base_files)
    base = checkpoint(directory, "Initial project")
    git(directory, "tag", "review-base", base)
    candidate = base
    if change:
        install(directory, change)
        candidate = checkpoint(directory, "Proposed change")
    git(directory, "tag", "starting-point", candidate)
    if case_id == "pearl":
        reports = {
            "current/p1.json": [1, 2, 3],
            "current/p2.json": [2, 3, 4],
            "archive/p3.json": [5, 6, 7],
        }
        install(directory, {
            f"artifacts/{path}": json.dumps({"checkout": candidate, "hits": hits}) + "\n"
            for path, hits in reports.items()
        })
    return {"base": base, "candidate": candidate}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("id", choices=sorted(CASES))
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(materialize(args.id, args.directory), sort_keys=True))
