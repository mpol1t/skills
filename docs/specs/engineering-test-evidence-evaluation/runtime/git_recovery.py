"""Run the frozen checkpoint-capable supplement via the primary runner."""
import json

import run

RECOVERY = json.loads((run.HERE / "git_recovery.json").read_text())
load_json = run.json.loads
build_trial = run.build_trial


def recovered_plan(data, *args, **kwargs):
    result = load_json(data, *args, **kwargs)
    if isinstance(result, dict) and isinstance(result.get("trials"), list):
        result["trials"] = [row for row in result["trials"] if row["id"] in RECOVERY["trials"]]
        assert len(result["trials"]) == len(RECOVERY["trials"])
    return result


def allow_fixture_git(job, repo, *args):
    launcher, env, installed = build_trial(job, repo, *args)
    config = job / "config/config.toml"
    rules = config.read_text()
    marker = "[permissions.trial.network]"
    rule = f"{json.dumps(str(repo / '.git'))} = \"write\"\n"
    assert rules.count(marker) == 1
    config.write_text(rules.replace(marker, rule + marker))
    return launcher, env, installed


if __name__ == "__main__":
    run.json.loads = recovered_plan
    run.build_trial = allow_fixture_git
    run.main()
