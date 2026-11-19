"""Replay the separately frozen clean-refactor control."""
import os
from pathlib import Path
import shutil
import tempfile

import run

source = run.ROOT
inputs = source / "controller/clean-refactor"

if __name__ == "__main__":
    os.environ["CONTROL_SOURCE"] = str(source)
    with tempfile.TemporaryDirectory(prefix="refactor-controller-") as directory:
        run.ROOT = Path(directory)
        control = run.ROOT / "controller"
        control.mkdir()
        for name in ("trials.json", "rubric.md", "fixture-revisions.json"):
            shutil.copyfile(inputs / name, control / name)
        shutil.copyfile(inputs / "generate.py", run.ROOT / "materialize.py")
        run.main()
