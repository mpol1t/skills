# Engineering test evidence evaluation inputs

The fixture materializer creates exactly one self-contained project with its
own Git history and no remotes. From this directory, run
`python3 -B materialize.py <fixture-id> <new-directory>`. Use the printed base
and candidate SHAs and the tags `review-base` and `starting-point`.

The controller directory contains the schedule, scoring key and the fixture
revision manifest. Materialize on the controller side, then expose only
that single project and its individual skill invocation and neutral prompt
to the evaluated session. Run the following checks outside evaluated sessions.

- `python3 -B controller/freeze_fixtures.py --verify` regenerates all fixture
  revisions and compares the starting file-byte and executable-mode digests,
  including the generated shard receipts for the matching candidate.
- `python3 -B controller/check_fixtures.py` verifies command outcomes and
  runs independent probes at both revisions for seeded defects.

The fixtures use Git, a POSIX shell and Python 3's standard library. Coverage
gate artifacts model versioned CI exports. Local coverage exercises a
standard-library trace-based fixture instrument, with branch outcome logic
limited to the declared return alternatives for the admission and reservation
projects. Runner loss and readiness receipts are deterministic simulations.
These inputs test the workflow's evidence handling in controlled projects.

[The baseline report](baseline.md) records the first attempts and distinct
recovery runs. [Runner and replay instructions](runtime/README.md) describe
how to recover the pinned skill snapshot and run the three frozen sets.
