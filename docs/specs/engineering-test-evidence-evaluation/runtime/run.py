"""Run frozen fixture trials with a fresh, restricted Codex CLI process."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import time

from trial_events import classify, records

HERE = Path(__file__).resolve().parent
PROTOCOL = json.loads((HERE / "runtime.json").read_text())
ROOT = HERE.parent
CODEX_BINARY = Path("node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/bin/codex")
SKILLS = PROTOCOL["skills"]
sys.path.insert(0, str(ROOT))
from controller.freeze_fixtures import working_tree_hash


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def capture(args, **kwargs):
    return subprocess.check_output(args, text=True, **kwargs)


def git(repo, *args):
    return capture(["/usr/bin/git", "-C", str(repo), *args]).strip()


def build_trial(job, repo, package, auth, revision, source, *, writable_fixture_git=False):
    home = job / "home"
    installed = home / ".agents/skills"
    installed.mkdir(parents=True)
    config = job / "config"
    config.mkdir()
    local_tmp = job / "tmp"
    local_tmp.mkdir()
    shutil.copyfile(auth, config / "auth.json")
    (config / "auth.json").chmod(0o600)

    paths = [f"skills/engineering/{name}" for name in SKILLS]
    archive = subprocess.check_output(
        ["/usr/bin/git", "-C", str(source), "archive", revision, *paths]
    )
    with tarfile.open(fileobj=io.BytesIO(archive)) as files:
        for member in files:
            parts = Path(member.name).parts
            if len(parts) <= 2:
                continue
            local = installed.joinpath(*parts[2:])
            if member.isdir():
                local.mkdir(exist_ok=True, parents=True)
            elif member.isfile():
                local.write_bytes(files.extractfile(member).read())
                local.chmod(0o555 if member.mode & 0o111 else 0o444)
            else:
                raise ValueError(f"Unexpected archive member: {member.name}")
    for directory in sorted(installed.rglob("*"), reverse=True):
        if directory.is_dir():
            directory.chmod(0o555)

    allowed_reads = (installed, config / "tmp/arg0-linux", (package / CODEX_BINARY).parent)
    rules = "\n".join(f"{json.dumps(str(path))} = \"read\"" for path in allowed_reads)
    if writable_fixture_git:
        rules += f'\n{json.dumps(str(repo / ".git"))} = "write"'
    options = f"""
default_permissions = "trial"
approval_policy = "never"
web_search = "disabled"
model = "{PROTOCOL['model']}"
model_reasoning_effort = "{PROTOCOL['reasoning_effort']}"
[features]
apps = false
shell_snapshot = false
multi_agent_v2 = true
[history]
persistence = "none"
[permissions.trial.filesystem]
":minimal" = "read"
"/usr" = "read"
"/etc" = "read"
{json.dumps(str(repo))} = "write"
{json.dumps(str(local_tmp))} = "write"
{rules}
[permissions.trial.network]
enabled = false
"""
    (config / "config.toml").write_text(options)
    env = {
        "HOME": str(home), "USER": "user", "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
        "TZ": "UTC", "TMPDIR": str(local_tmp), "CODEX_HOME": str(config), "GIT_AUTHOR_NAME": "Fixture Contributor",
        "GIT_AUTHOR_EMAIL": "contributor@example.invalid",
        "GIT_COMMITTER_NAME": "Fixture Contributor", "GIT_COMMITTER_EMAIL": "contributor@example.invalid",
    }
    return ["/usr/bin/node", str(package / "bin/codex.js")], env, installed


def verify(launcher, env, repo, job, installed, protected, destination):
    canary = job / "config/private-canary"
    canary.touch()
    (repo / "restricted-link").symlink_to(canary)
    program = """
import errno, os, pathlib, socket, subprocess, sys
allowed, *blocked = map(pathlib.Path, sys.argv[1:])
assert allowed.is_file() and allowed.read_text().startswith("---")
for path in blocked:
    try:
        path.open().close()
    except OSError as error:
        assert error.errno in (errno.ENOENT, errno.EACCES, errno.EPERM), (path, error)
    else:
        raise AssertionError(f"Readable: {path}")
try:
    handle = socket.socket()
    handle.settimeout(2)
    handle.connect(("1.1.1.1", 443))
except OSError as error:
    assert error.errno in (errno.EACCES, errno.EPERM, errno.ENETUNREACH), error
else:
    raise AssertionError("Socket connected")
result = subprocess.run(["curl", "--fail", "--max-time", "4", "-sS",
                        "https://github.com/mpol1t/skills/issues/4"], capture_output=True)
assert result.returncode != 0
print("Pass: pinned skill readable; private files, symlink, socket and tracker unavailable.")
"""
    link = repo / "restricted-link"
    command = launcher + [
        "sandbox", "-C", str(repo), "-P", "trial", "/usr/bin/python3", "-c", program,
        str(installed / "tdd/SKILL.md"), str(canary), str(job / "config/auth.json"),
        str(link), *map(str, protected),
    ]
    try:
        with destination.open("wb") as output:
            subprocess.run(command, cwd=repo, env=env, check=True, timeout=15,
                           stdout=output, stderr=subprocess.STDOUT)
    finally:
        link.unlink()


def save_tree(repo, starting, path, launcher, env):
    def collect(*command):
        sandboxed_git = launcher + [
            "sandbox", "-C", str(repo), "-P", "trial",
            "/usr/bin/git", "-C", str(repo), *command,
        ]
        return capture(sandboxed_git, cwd=repo, env=env, timeout=20)

    outputs = []
    commands = [
        ["status", "--porcelain=v1", "--untracked-files=all"],
        ["worktree", "list", "--porcelain"], ["log", "--all", "--oneline", "--decorate"],
        ["diff", "--binary", starting],
    ]
    refs = collect("for-each-ref", "--format=%(refname)", "refs/heads").splitlines()
    commands += [["diff", "--binary", starting, ref] for ref in refs]
    for command in commands:
        outputs.append({"command": ["git", *command], "output": collect(*command)})
    write_json(path, outputs)


def run_trial(trial, args, runtime_root):
    trial_id = trial["id"]
    destination = args.results / trial_id
    destination.mkdir()
    for attempt in range(1, PROTOCOL["maximum_attempts"] + 1):
        result = destination / f"attempt-{attempt}"
        result.mkdir()
        job = Path(tempfile.mkdtemp(prefix=f"{trial_id}-", dir=runtime_root))
        repo = job / "repo"
        record = {"trial": trial_id, "attempt": attempt, "skill": trial["skill"]}
        began = time.monotonic()
        try:
            fixture = capture([
                sys.executable, str(ROOT / "materialize.py"), trial["fixture"], str(repo)
            ])
            record["fixture"] = json.loads(fixture)
            record["fixture"]["working_tree_sha256"] = working_tree_hash(repo)
            if record["fixture"] != args.fixtures[trial["fixture"]]:
                raise ValueError("Fixture does not match the frozen revision")
            starting = git(repo, "rev-parse", "HEAD")
            record["starting_head"] = starting
            launcher, env, installed = build_trial(
                job, repo, args.package, args.auth, args.revision, args.source,
                writable_fixture_git=args.writable_fixture_git,
            )
            verify(launcher, env, repo, job, installed, args.protected, result / "isolation.txt")
            skill_path = installed / trial["skill"] / "SKILL.md"
            prompt = f"Use ${trial['skill']} ({skill_path}).\n\n{trial['prompt']}"
            (result / "prompt.txt").write_text(prompt + "\n")
            command = launcher + ["exec", "--json", "-C", str(repo), "-"]
            budget = PROTOCOL["timeouts_seconds"].get(
                trial["skill"], PROTOCOL["timeouts_seconds"]["default"]
            )
            started = time.monotonic()
            try:
                with (result / "events.jsonl").open("wb") as output, (result / "stderr.txt").open("wb") as error:
                    with subprocess.Popen(
                        command, cwd=repo, env=env, stdin=subprocess.PIPE,
                        stdout=output, stderr=error, start_new_session=True,
                    ) as process:
                        record.update(launch=command, timeout_seconds=budget)
                        try:
                            process.communicate(prompt.encode(), timeout=budget)
                            record["exit_code"] = process.returncode
                        except subprocess.TimeoutExpired:
                            record["timed_out"] = True
                            os.killpg(process.pid, signal.SIGKILL)
                            process.wait()
            finally:
                if "launch" in record:
                    record["elapsed_seconds"] = round(time.monotonic() - started, 3)
                    sessions = job / "config/sessions"
                    for index, logfile in enumerate(sorted(sessions.rglob("*.jsonl")), start=1):
                        shutil.copyfile(logfile, result / f"session-{index}.jsonl")

            tail = {}
            interrupted = record.get("timed_out") or record.get("exit_code") != 0
            events = [event for _, event in records(
                result / "events.jsonl", truncated=tail if interrupted else None,
            )]
            if tail:
                record["truncated_event_tail"] = tail
            record["status"] = classify(
                events, exit_code=record.get("exit_code"), timed_out=record.get("timed_out", False),
            )
            if record["status"] == "completed":
                record["usage"] = events[-1].get("usage")
            try:
                save_tree(repo, starting, result / "tree.json", launcher, env)
            except (subprocess.SubprocessError, OSError) as error:
                record["collection_error"] = str(error)
        except Exception as error:
            fallback = "invalid-evidence-after-dispatch" if "launch" in record else "setup-failed-before-dispatch"
            record.setdefault("status", fallback)
            record["error"] = str(error)
        finally:
            try:
                (job / "config/auth.json").unlink(missing_ok=True)
                for subdirectory in (job / "home/.agents/skills").rglob("*"):
                    if subdirectory.is_dir():
                        subdirectory.chmod(0o755)
                shutil.rmtree(job)
            except OSError as error:
                record["cleanup_error"] = str(error)
            finally:
                record["total_seconds"] = round(time.monotonic() - began, 3)
                write_json(result / "outcome.json", record)
        print(f"{trial_id} {attempt} {record['status']}", flush=True)
        if record["status"] != "runtime-failed-before-interaction":
            break


def main(*, trial_ids=None, writable_fixture_git=False):
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--auth", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--revision", default=PROTOCOL["skill_revision"])
    parser.add_argument("--protected", type=Path, action="append", default=[])
    args = parser.parse_args()
    args.writable_fixture_git = writable_fixture_git
    args.results = args.results.resolve()
    args.package = args.package.resolve()
    args.auth = args.auth.resolve()
    args.source = args.source.resolve()
    if sha256((args.package / CODEX_BINARY).read_bytes()).hexdigest() != PROTOCOL["codex_sha256"]:
        parser.error("Codex runtime hash differs from the frozen protocol")
    args.protected += [
        ROOT / "controller/trials.json", ROOT / "controller/rubric.md",
        args.auth, args.source / "docs/specs/engineering-test-evidence.md",
        Path.home() / ".agents/skills/tdd/SKILL.md", Path.home() / ".claude/skills/tdd/SKILL.md",
    ]
    args.fixtures = json.loads((ROOT / "controller/fixture-revisions.json").read_text())
    plan = json.loads((ROOT / "controller/trials.json").read_text())["trials"]
    assert len(plan) == len({item["id"] for item in plan})
    assert all(re.fullmatch("[a-z0-9-]+", item["id"]) for item in plan)
    if trial_ids is not None:
        selected = set(trial_ids)
        plan = [item for item in plan if item["id"] in selected]
        if len(plan) != len(trial_ids):
            parser.error("Expected unique known trial IDs")
    args.results.mkdir()
    with tempfile.TemporaryDirectory(prefix="evaluation-", dir=Path.home() / ".local/share") as root:
        with ThreadPoolExecutor(max_workers=PROTOCOL["max_parallel_trials"]) as pool:
            list(pool.map(lambda item: run_trial(item, args, Path(root)), plan))


if __name__ == "__main__":
    main()
