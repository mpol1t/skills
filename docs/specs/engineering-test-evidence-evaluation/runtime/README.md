# Evaluation runner

Run the controller outside all evaluated workspaces. Use Python 3.11, Git 2.39.5,
Node and Codex CLI 0.170.0 on Linux with the named permission profile operational.
The runtime JSON pins the Codex binary hash, skill revision, model and effort,
concurrency, time limits and maximum attempts. The model name identifies the
served configuration. An immutable underlying model weights revision was unavailable.

Each trial uses a fresh Git repository, profile, home and model session. The
runner installs only pinned copies of the named skills and their support files.
It enables local shell and native subagents, disables apps and web search, and uses
an approval policy of never. Shell reads are limited to system paths, skill copies
and the sandbox helper. The fixture workspace and a private temporary directory
are writable. There are no Git remotes or external tracker credentials. The
model client authenticates to the provider outside the tool sandbox. Its
credential file and thread history are outside the tool read allowlist.

Before replay, verify the isolation with an authenticated client and disposable
fixture using the qualification script. Check the tool inventory and both
root and child command logs. Supply the protected scoring key, issue exports,
parent spec and previous results as additional `--protected` paths where
available. Keep all outside the fixture and out of prompts. The runtime
checks a direct file read, a symlink to private material, a raw socket and
an HTTPS request before each dispatch. Logs go outside the replay workspace.

From the evaluation directory, verify and fetch the bundle into the same
repository passed as the runner's `--source`.

```sh
git -C /path/to/skills bundle verify "$PWD/runtime/skill-input.bundle"
git -C /path/to/skills fetch "$PWD/runtime/skill-input.bundle" issue-4-baseline-skill-input
python3 runtime/qualification.py /path/to/skills /path/to/codex-package /path/to/auth.json /path/to/new-qualification-directory
python3 runtime/run.py /path/to/new-results \
  --source /path/to/skills --package /path/to/codex-package \
  --auth /path/to/auth.json --protected /path/to/protected-key
```

Create the qualification directory first. The results directory must be new.
The authorization file is an existing Codex login file and stays private.
The package path contains `bin/codex.js`. The runner checks the binary hash
before starting. The bundle is incremental against the published repository
base. Only the named skill directories are extracted into the fixture home.

A started interaction is preserved on timeout, interruption or tool
failure. A runtime failure before any recorded agent interaction permits
one fresh replacement with the same inputs. A failed sandbox or fixture
setup leaves the trial undispatched and records the setup outcome. A fixture
command's simulated or real failure is part of the trial observations.
The scoring key uses first-attempt evidence. Replacement attempts are
reported separately, and a tool error is preserved even if replay succeeds.

## Separate recovery protocols

The primary 26-trial protocol lives at `01b4dcfb2fe437f95d0cb02abdcef49e9fdead87`.
Its primary attempt remains the unit of comparison. Two later runs address
specific evaluation faults. Compare their results separately and use the
same recovery settings during any later candidate comparison.

- `runtime/git_recovery.py` accepts the same arguments as `runtime/run.py`.
  It runs only the four IDs in `runtime/git_recovery.json` with Git metadata
  writable in each disposable fixture. Frozen at
  `64db6b18c47816410d073718493b93db122195f0`.
- `runtime/clean_refactor.py` accepts the same arguments as `runtime/run.py`.
  It runs the new clean control using
  `controller/clean-refactor/` and the primary permissions. Frozen at
  `8575fa55df7b021435f2a3d65f11f05802b7c601`.

Pass previous results using additional `--protected` file probes. Paths
remain outside the read allowlist independently of the probes.

## Interrupted replay evidence

The controller preserves the original CLI event bytes, including an
unterminated record split inside a UTF-8 character. An interrupted attempt
may report that final record's source line, byte count and SHA-256 digest.
The minimized session export likewise records partial session tails in
`truncated_sessions.json`. The private raw session files retain the bytes.
An invalid interior record fails the export, and an invalid final record
fails export for a completed attempt. The reconciler checks each status
against dispatch, exit, terminal and timeout evidence. A dispatched run
with inconsistent evidence is preserved for diagnosis and fails
reconciliation.

Run the model-free regression checks from this directory with
`python3 -B -m unittest -v test_evidence`.

Git collection preserves the status columns and line endings in new
captures. The original Hazel tree export lost the first status column.
The contemporaneous `item_10` output shows an unstaged modification for
both files. The retained tree export and original command output document
the discrepancy. [Tree export](../results/primary/hazel/attempt-1/tree.json)
[Command events](../results/primary/hazel/attempt-1/events.jsonl)
