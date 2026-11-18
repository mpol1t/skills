# Engineering test evidence baseline

[GitHub Issue #4](https://github.com/mpol1t/skills/issues/4) and the agreed
local engineering test evidence specification define the evaluation. This
run used the current skill contents at
`75f0fb80d731f53716d74904d0eb31d4a3833777`, including three local skill
edits captured from repository base
`042e535543c8596230f9fb8fe29378db8f5bd6e1`.
[Runtime and replay instructions](runtime/README.md) recover the snapshot
and describe the fresh Linux session configuration.

The first attempts use the protocol at
`01b4dcfb2fe437f95d0cb02abdcef49e9fdead87`. It names one independent
session per trial, with two deliberately identical starting projects for
the explicit and ordinary implementation prompts. The
[trial plan](controller/trials.json),
[fixture revisions](controller/fixture-revisions.json), and
[controller-only rubric and key](controller/rubric.md) were frozen before
dispatch. The sole orchestration fixture uses its own Markdown issue
tracker. [Isolation qualification](qualification/summary.md) covers the
parent and child processes, and each attempt preserves its own preflight.

## Trial accounting

| Set | Planned | First outcomes | Replacement attempts | Met | Missed | Unobserved |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Primary | 26 | 26 | 0 | 20 | 5 | 1 |
| Writable fixture Git recovery | 4 | 4 | 0 | 3 | 1 | 0 |
| Clean-refactor control recovery | 1 | 1 | 0 | 1 | 0 | 0 |

Primary runtime outcomes were 1 budget-exhausted, 25 completed. Git recovery outcomes
were 1 budget-exhausted, 3 completed. Completion means the model session returned a
disposition or report. Workflow outcomes are scored separately.

- Seeded defects missed: **0/6 observed**, with 0 unobserved.
  The denominator is the six seeded cases in the frozen rubric.
- Correct candidates wrongly blocked: **0/2 eligible primary controls**,
  with 1 of the three planned controls unobserved for this measure.
  Willow raised a genuine label-format regression for an admitted Python
  subtype, so the reported block cannot establish a false positive. The
  separate larch trial approved a valid refactor and requested zero redundant
  tests. Willow and larch both recorded zero redundant test requests or additions.
- Intermittent failures correctly localized: **2/2 observed**, with
  0 unobserved. Drift separately classified a runner failure correctly.
  It retained the same-revision green replacement and withheld credit for it.
- Initially failing required fixture checks: **6/29 observed
  first checks**. Of initially failing required checks that were rerun,
  **4/6 later passed**. Base controls, deliberate TDD red steps,
  and unsuccessful attempts to start a check are separate from these counts.
- New tests and requests: **11 added methods** in the 26 primary traces, with
  no redundant additions. The traces contain **six** additional proposed
  cases, of which **one** was redundant. Final recommendations were observable
  for 25 of 26 primary trials. The timed-out trial's worker trace still
  records four added tests. The Git recovery records nine additions and zero
  redundant requests. The clean-refactor recovery adds and requests zero.
  Each score has an attempt-level inventory and pointers to its evidence.
- Recorded primary model time: **2749.8 seconds across 26
  sessions**. The median for the 17 standalone review sessions
  was **88.9 seconds**. The primary CLI logs record
  **340 completed root shell calls**. Session traces contain
  **874 shell command call expressions** across root and child
  logs. These are activity counts, and elapsed figures overlap under concurrent
  execution.

## Evidence and per-trial outcomes

Each attempt contains the launched prompt, outcome and effort metadata,
isolation check, command and output events, and fixture Git status and diffs.
The compressed session traces retain child actions and original source-line
numbers, with unrelated account and harness metadata omitted. Repository
paths in tool output refer to disposable checkouts. Commit and command
evidence from trials that used a private temporary clone is in the traces.
The per-trial score JSON carries more evidence references and counting detail.
For compressed traces, use the saved `source_line` to resolve original JSONL
line references.

[Primary accounting](results/primary/accounting.json) ·
[Primary scores](results/primary/scores.json) ·
[Git recovery accounting](results/git-recovery/accounting.json) ·
[Clean recovery accounting](results/clean-refactor/accounting.json)

### Primary trials

- **quartz · met**. Ran app.decision at 36, 37 and 38 on both commits; only 37 changed from accept to reject. ./check passed with both branch outcomes hit. Blocked the inclusive-boundary regression and named the missing assertion for load 37. [First attempt](results/primary/quartz/attempt-1/outcome.json)
- **saffron · met**. Ran public read_catalog on both revisions. BOM fixture returned Yarrow at base and raised JSONDecodeError at candidate, while plain UTF-8 still worked. ./check passed the pure conversion test. Blocked the compatibility break and proposed testing both documented formats at the public importer. [First attempt](results/primary/saffron/attempt-1/outcome.json)
- **elm · met**. Compared public state after a failed audit at both SHAs. Both returned False, but only candidate changed stock from 3 to 2. ./check passed with both branch outcomes hit. Requested changes because the passing failure test checks only the returned value and misses rollback. [First attempt](results/primary/elm/attempt-1/outcome.json)
- **ochre · met**. At d02a07b, archived clean candidate ./check failed (1), immediate same-checkout rerun passed (0), and clearing the order marker reproduced the failure. Individual unittest cases passed; deliberate regional-then-default order failed at base, reverse order passed. Identified test_regional leaving cy-GB in shared app.settings and test_default failing afterward. Also flagged dropped discovery arguments, which the command output demonstrated. [First attempt](results/primary/ochre/attempt-1/outcome.json)
- **drift · missed**. First probe setup failed because the installed Python did not support TarFile.extractall(filter=...). A second snapshot command used tar and recovered. At cbdb267, archived clean candidate ./check exited 75 with zero assertions, then the unchanged checkout passed the full suite on immediate rerun. An independent clean candidate reproduced exit 75. Identified the wrapper-generated startup failure, but left the required check unresolved without crediting complete same-revision replacement evidence under the rubric. [First attempt](results/primary/drift/attempt-1/outcome.json)
- **birch · met**. Ran archived candidate ./check: first read captures/a and failed with pending != ready, next two read captures/b and passed; clearing marker restored failure. Explicit receipt replay produced both results. Left readiness unresolved after green retry. Captures omit live start timing and telemetry, so the upstream pending observation remained unexplained. [First attempt](results/primary/birch/attempt-1/outcome.json)
- **jade · met**. Ran both dated ./check commands; March was quarantined under R87, April actually ran the passing test. Also reproduced usage exit 2 for bare ./check. Separated the scoped March waiver from exercised April acceptance evidence and stated expiry. Reported a separate, supported Standards finding for the bare command documented by README. [First attempt](results/primary/jade/attempt-1/outcome.json)
- **reed · met**. ./check passed the single-delivery case. Exercised two public receive calls with one receipt set at both revisions. Reported candidate produced two effects versus base one, despite both returning two acknowledgments. Named production guard as the repair and a distinct regression example. [First attempt](results/primary/reed/attempt-1/outcome.json)
- **lilac · met**. Loaded the base implementation and checked label(4) is bin:004. The same independent protocol assertion raised at starting-point because it returned bin:4. ./check passed against the changed golden. Blocked removal of documented three-digit padding and explained how replacing the oracle concealed the defect. [First attempt](results/primary/lilac/attempt-1/outcome.json)
- **crane · met**. Read owner decision 18 from review-base; its independent expected output for ID 4 is bin[0004]. ./check and git diff --check passed. Approved the authorized format and golden change. The concern about unspecified identifier range was explicitly non-blocking. [First attempt](results/primary/crane/attempt-1/outcome.json)
- **willow · missed**. Ran a public input probe: an int subclass whose __format__ returns a str subclass with __radd__ produced bin:004 at base but changed at candidate. Ordinary integers matched. This disproves the clean-control premise for the declared int input. ./check passed its four ordinary-integer examples. Blocked a reproduced behavior change; under the frozen rubric it did not accept the expected clean refactor. The observed block has evidence and is excluded from the false-block metric. [First attempt](results/primary/willow/attempt-1/outcome.json)
- **walnut · met**. Read the Labels workflow and pre-commit hook; the hook runs ./check. Ran .github/checks/labels; package-lines was 8/10, above 70%. Ran .githooks/pre-commit and observed the unit test pass. Reported both results, package scope and script sources. The setup draft awaited approval, which did not obscure the criterion's verification discovery. [First attempt](results/primary/walnut/attempt-1/outcome.json)
- **acorn · met**. Read dependency-free Public shelf label issue in the local Markdown tracker. Discovered .githooks/pre-commit, .github/workflows/labels.yml, and its package check without prior verification setup. Worked around read-only initial .git by committing in a writable local clone. Ran the Labels package CI rule; 8/10 (80%) exceeded its 70% minimum. Re-ran the package gate after two independently reviewed repairs for Python's integer conversion limits. Reported four passing tests and the package report check at reviewed commit 38e219b62e9a4c5572b4a500df9d805cdd1dc00e in the writable clone. [First attempt](results/primary/acorn/attempt-1/outcome.json)
- **plum · met**. attempt-1/events.jsonl item_8–12 and item_17: .githooks/pre-commit passed (one project test). Candidate .github/checks/labels failed at 2/4 changed branch outcomes (50%, required 75%). The same check passed at the review base (4/4). Final disposition requests changes for the failed CI gate and separately credits the hook. [First attempt](results/primary/plum/attempt-1/outcome.json)
- **teal · met**. attempt-1/events.jsonl item_8, item_9 and item_15: CI threshold 80% passed at 17/20 (85%). Re-executing the native checker at the governing contract floor of 90% exited 1. Final disposition blocks release and identifies the enforcement gap. Both review child work logs independently repeat the checks. [First attempt](results/primary/teal/attempt-1/outcome.json)
- **agate · met**. attempt-1/events.jsonl item_8–11 and item_14: .github/checks/labels passed at 29/50 (58%) against the 55% floor; the base was 28/50 and also passed. Final approves the candidate and treats 80% as aspirational under CONTRACT.md. [First attempt](results/primary/agate/attempt-1/outcome.json)
- **rose · missed**. attempt-1/events.jsonl item_11–12 and item_15: recovered an extraction error and ran coverage at the base's default 1/2 and candidate's default 1/1. It correctly withheld a directional conclusion and noted app.py at 1/1 in both, but never reran the candidate with maintenance.py restored under the base include scope. Child traces also only considered default scopes. [First attempt](results/primary/rose/attempt-1/outcome.json)
- **pearl · met**. attempt-1/events.jsonl item_11 and item_13–15: native combiner first failed because p3 was absent. The agent recovered matching p3 from archive, copied all three into a disposable candidate checkout and ran the unmodified revision-checking combiner. Union count 7/8 cleared 75%; it separately noted the original collector still lacked p3. [First attempt](results/primary/pearl/attempt-1/outcome.json)
- **clover · met**. attempt-1/events.jsonl item_9–12 and item_15: diff removed two executable lines, leaving zero added or modified surviving lines. Direct public read_catalog calls returned Yarrow for the BOM input at base and raised JSONDecodeError at candidate. The plain input worked at both revisions and ./check passed because it covers only convert. Final disposition blocks the regression. [First attempt](results/primary/clover/attempt-1/outcome.json)
- **moss · missed**. attempt-1/events.jsonl item_8–10 and item_14 and session-1/3 commands: correctly found maintenance.py listed by project.toml, missing from candidate scope and present in base scope (1/1 versus 1/2). Asked for restoration; no command attempted to remeasure candidate with both configured files. [First attempt](results/primary/moss/attempt-1/outcome.json)
- **maple · met**. attempt-1/events.jsonl item_9–13 and item_16: default candidate coverage passed at 1/1 only after maintenance.py was excluded; base scope failed at 1/2. Final rejects the reduced denominator because the 100% requirement covers both files and no owner approval exists. [First attempt](results/primary/maple/attempt-1/outcome.json)
- **jasper · met**. attempt-1/events.jsonl item_12–13 and item_19: ./check and python3 tools/coverage.py passed at both revisions. The final reports 1/2 lines, says branch outcomes are unmeasured and identifies no required branch gate. Standards optionally suggested duplicating label(12) from the executable coverage probe in the unit suite. [First attempt](results/primary/jasper/attempt-1/outcome.json)
- **topaz · met**. attempt-1/events.jsonl item_11–14 and item_19: ./check passed, line coverage was 4/5 overall, and the agent kept the required 80% changed-branch gate unverified despite examples exercising both lines. It separately found an incidental signed-input compatibility change (label(-1) returned bin:00-1 versus bin:-01 at base). [First attempt](results/primary/topaz/attempt-1/outcome.json)
- **hazel · met**. attempt-1/events.jsonl item_3, item_5, item_8, item_10 and item_11: loaded TDD, confirmed the existing suite passed, added the new shelf-label example, observed it go red before editing app.py, and then passed both tests and additional direct calls. The added test covers a new public function. [First attempt](results/primary/hazel/attempt-1/outcome.json)
- **aspen · missed**. attempt-1/events.jsonl item_3–4 and item_9–11 explicitly invoke and follow TDD for an ordinary implementation request. The work nevertheless produced a reviewed committed result in a writable private clone after the original .git was read-only. At item_22–26 the agent reproduced the review's very-large-ID failure, extended the oracle, and repaired it. The final item_31 reports four passing tests on 33cbd9d1433fcce94aee70077bf878032fc119ec, preserving the former label format. [First attempt](results/primary/aspen/attempt-1/outcome.json)
- **fern · unobserved**. attempt-1/outcome.json records 540 s budget exhaustion. events.jsonl item_2–11 shows fixture-only tracker intake and isolated integration and worker repositories. Item_17–19 records checkpoint 5f041bed481a58070217b5de430de315abc2de8c, three passing tests, and independent review. Item_26–48 records three repairs and focused reviews. The original formatting failed for 4,301-digit IDs; the Decimal repair still failed without _decimal; the second repair required defensive normalization for int subclasses. At expiry checkpoint e0183769ab9228c345c77c09e57a5a19752639a2 had five passing worker checks and focused re-review in progress. Integration remained at the base, so integrated verification and whole-spec review were unobserved. [First attempt](results/primary/fern/attempt-1/outcome.json)

### Git checkpoint recovery

The primary profile's default Git metadata protection prompted some agents
to create disposable clones to reach checkpoint and review. The separate
recovery grants writes only to the disposable fixture's Git directory.
The same four prompts and fixture revisions were frozen for that run. Its
scores remain separate.

- **acorn · met**. Read the isolated issue, contract, pre-commit hook, Labels CI workflow and its check script in the fresh implementation checkout. At first commit 2b695223, ran the full suite and package gate; report was 8/10, above 70%. Independent review reproduced the digit-limit failure for a nonnegative ID. Reran required checks from archive of repair commit 57d446a1 and retained same-scope report and low digit-limit run. Final report kept all evidence tied to reviewed commit 57d446a1, with both review axes clear. [First attempt](results/git-recovery/acorn/attempt-1/outcome.json)
- **hazel · met**. Explicit user TDD request activated the TDD skill. Public example for ID 4 failed because shelf_label did not yet exist. First implementation made ID 4 pass. Second public example at ID 10 failed under the initial padding behavior. Adjusted implementation and passed all three tests. Final response traces both red-green cycles. [First attempt](results/git-recovery/hazel/attempt-1/outcome.json)
- **aspen · missed**. Ordinary implementation expressly activated the tdd skill. Ran test-first failure for the missing public function. Ran the passing test after implementation. Added and demonstrated a separate red for a large-ID edge found by review. Committed a portability fix at cc42a7f and passed all three tests. Reported successful repair and independent review, while the undesired TDD activation remained directly observed. [First attempt](results/git-recovery/aspen/attempt-1/outcome.json)
- **fern · met**. Created integration branch and exclusive ticket worktree after local one-Issue intake. Recorded isolated worker checkpoint with three passing tests and dispatched independent review. Independent review reproduced Python's digit conversion limit and authority re-review later found a pure-Python fallback defect. Recorded portable repair checkpoint aaff897892e588247f49869f6076707a68e51720 after both repair cycles. Serialized fast-forward after approval to aaff897892e588247f49869f6076707a68e51720. Verified integrated revision with ./check, the low digit-limit variant, and git diff --check. After whole-spec review, committed only local issue closure at facdc9caffc60d77a4df406cbf11e772389f7c0c, and reverified both suite variants on that commit. The runtime ended at the 540-second budget before a final answer; recorded actions establish the rubric's full handoff criterion. [First attempt](results/git-recovery/fern/attempt-1/outcome.json)

### Clean-refactor control recovery

- **larch · met**. attempt-1/events.jsonl item_10 ran the existing public examples. Item_11 checked 11 representative integers against both pinned revisions without adding a test. Item_14 approved the diff, with one optional design concern and no requests for redundant tests. [First attempt](results/clean-refactor/larch/attempt-1/outcome.json)

## Replay and export repairs

The historical runner collected Git status and diffs outside the trial
sandbox. This mattered once the Git recovery allowed agent writes to
fixture Git metadata. The archived command audit found no changes to
Git helper settings. The historical collector had no independent process
audit. The repaired replay now collects Git evidence inside the trial's
permission profile. The published trace export omits account quota and
harness metadata, copied credentials are removed on qualification failure,
and reconciliation rejects missing or malformed completed-event evidence.
The frozen inputs and recorded trial actions remain available for comparison.

## Limits

These small synthetic projects observe instruction behavior in one served
model configuration, one session per trial or recovery condition. The Codex
binary hash and named model configuration are recoverable. The hosted
model weights revision and sampling seed were unavailable. Fixture gate
reports and selected runner failures are controlled simulations. The
evaluation measures observed review and workflow evidence, and production
flake rates would need separate downstream data.
