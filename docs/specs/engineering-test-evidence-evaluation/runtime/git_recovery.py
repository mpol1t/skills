"""Run the frozen checkpoint-capable supplement via the primary runner."""
import json

import run

RECOVERY = json.loads((run.HERE / "git_recovery.json").read_text())


if __name__ == "__main__":
    run.main(trial_ids=RECOVERY["trials"], writable_fixture_git=True)
