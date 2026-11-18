"""Exercise the runner on an unrelated canary before exposing any fixture."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from run import build_trial, PROTOCOL, verify

source, package, auth, evidence = map(lambda arg: Path(arg).resolve(), sys.argv[1:])
job = Path(tempfile.mkdtemp(prefix="evaluation-canary-", dir=Path.home() / ".local/share"))
repo = job / "repo"
repo.mkdir()
subprocess.run(["git", "init", "-q", repo], check=True)
launcher, env, installed = build_trial(job, repo, package, auth, PROTOCOL["skill_revision"], source)
protected = [
    source / "docs/specs/engineering-test-evidence.md",
    Path.home() / ".agents/skills/tdd/SKILL.md",
    Path.home() / ".claude/skills/tdd/SKILL.md",
]
verify(launcher, env, repo, job, installed, protected, evidence / "sandbox.txt")
(repo / "canary.py").write_text(f"""
from pathlib import Path
import errno
import socket
import subprocess

assert Path({str(installed / "tdd/SKILL.md")!r}).is_file()
for path in {list(map(str, protected + [job / 'config/auth.json']))!r}:
    assert not Path(path).is_file(), path
try:
    socket.socket()
except OSError as error:
    assert error.errno in (errno.EPERM, errno.EACCES), error
else:
    raise AssertionError("Socket creation unexpectedly permitted")
public = "https://github.com/"
assert subprocess.run(["curl", "--max-time", "3", public], capture_output=True).returncode
print("offline and private canary unavailable")
""")
with (evidence / "prompt-inspection.json").open("w") as output:
    subprocess.run(launcher + ["debug", "prompt-input", "Runner probe"], env=env,
                   cwd=repo, stdout=output, timeout=20, check=True)
with (evidence / "probe.jsonl").open("w") as output, (evidence / "probe.stderr").open("w") as error:
    try:
        subprocess.run(
            launcher + ["exec", "--json", "-C", str(repo), "-"], env=env, cwd=repo,
            input="Run python3 canary.py yourself, then spawn a fresh child to run the same command. Wait for the child and report both results.",
            text=True, stdout=output, stderr=error, timeout=150, check=True,
        )
    finally:
        (job / "config/auth.json").unlink(missing_ok=True)
        for index, file in enumerate(sorted((job / "config/sessions").rglob("*.jsonl")), 1):
            (evidence / f"session-{index}.jsonl").write_bytes(file.read_bytes())
