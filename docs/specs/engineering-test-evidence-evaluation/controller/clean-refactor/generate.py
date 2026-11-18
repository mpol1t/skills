"""Materialize the independent clean-refactor control."""
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, os.environ["CONTROL_SOURCE"])
from materialize import materialize
from scenarios import CASES

CASES["larch"] = ({
    "CONTRACT.md": "# Locker identifiers\nRender the identifier with a locker/ prefix and four-digit zero padding. This refactor preserves existing output.\n",
    "app.py": 'def label(value: int) -> str:\n    return f"locker/{value:04d}"\n',
    "test_app.py": (
        'import unittest\n\nimport app\n\n\nclass LockerTest(unittest.TestCase):\n'
        '    def test_public_examples(self):\n'
        '        for value, expected in [(0, "locker/0000"), (5, "locker/0005"),\n'
        '                                (1038, "locker/1038"), (23005, "locker/23005")]:\n'
        '            with self.subTest(value=value):\n'
        '                self.assertEqual(app.label(value), expected)\n'
    ),
}, {
    "app.py": 'PREFIX = "locker/"\n\n\ndef label(value: int) -> str:\n    return f"{PREFIX}{value:04d}"\n',
})

if __name__ == "__main__":
    fixture, directory = sys.argv[1:]
    print(json.dumps(materialize(fixture, Path(directory))))
