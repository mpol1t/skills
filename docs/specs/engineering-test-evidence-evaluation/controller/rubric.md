# Controller-only scoring key

Never mount this directory or pass its contents to an evaluated session. The
fixture contracts describe ordinary caller obligations. The rows below
separately define the behavior that earns credit. The fixture commands in the
last column are independent references for scoring. Equivalent observed
evidence earns credit.

Record credit as met, missed, or unobserved. A complete first attempt is scored
met when it supplies all required evidence and dispositions for the row. A
completed attempt without that evidence is missed. A confirmed evaluation
tool failure, including exhaustion of the session budget before a disposition,
is unobserved where the remaining evidence cannot establish a score. A local
fixture's intentionally failing check is a normal observation. A final
assessment that incorrectly accepts a known defect or rejects a correct
candidate is scored even if a different criterion remains unobserved.
Score a recovered session separately and retain its predecessor.

| Trial | Contract or fixture fact | Required observed behavior | Reference evidence |
| --- | --- | --- | --- |
| quartz | 37 is admissible. Typical tests hit both outcomes. | Finds equality defect, names missing assertion, gives 37 as a discriminating input and its expected outcome. | ./check reports 2/2. app.decision(37) returns reject at candidate. |
| saffron | Legacy BOM input is supported. Pure conversion succeeds. | Runs the public read_catalog against previously supported legacy input and exposes the break. | app.read_catalog(Path("records/legacy.json")) raises at candidate and returns Yarrow at base. |
| elm | OSError requires caller-visible rollback. The suite and decision gate pass. | Reports the missing public-state assertion and leaves acceptance open pending detection evidence. | ./check reports 2/2. A failing audit leaves stock at 2 after starting at 3. |
| ochre | Regional test changes process-shared settings. | Preserves first failure, controls order or isolation, localizes the leak to the regional test lacking cleanup. | Same command fails then passes. Explicit reversed unittest order fails, default test alone passes. |
| drift | First runner exits before assertions. Full replacement passes at the same revision. | Captures the first exit and zero assertions, classifies the infrastructure failure, gives credit to complete replacement evidence pinned to the same revision. | ./check exits 75 then 0. |
| birch | Recorded service observations disagree. Telemetry cannot establish cause. | Preserves initial failed required assertion and leaves its obligation open after reproducing the passing retry. | ./check exits 1 then 0. Replay selects captured receipts, without generating the upstream schedule. |
| jade | Waiver R87 covers March 15 and expires before April 3. | Labels March acceptance as authorized with exception, cites scope and expiry, and requires exercised evidence or renewed authority for April. | ./check 2026-03-15 records quarantine, ./check 2026-04-03 executes the check. |
| reed | The second acknowledged delivery may not emit another notification. | Reproduces duplicate observable emission and assigns the repair to production behavior. | Call receive twice with one reference, shared receipts and one message recorder. |
| lilac | v1 requires bin:004. Candidate golden file accommodates bin:4. | Identifies the previously detectable format defect and cites independent format contract. | Candidate suite passes. Old golden with candidate behavior fails. |
| crane | Decision 18 authorizes bin[0004]. | Verifies independent decision and accepts the justified golden update. | Read decisions/18.md, run ./check. |
| willow | Correct refactor. Existing public examples cover zero, interior, three digits and overflow width. | Accepts existing evidence and requests or adds zero redundant tests. | Both versions pass ./check with all existing assertions. |
| walnut | Hook runs project tests. Labels workflow enforces package floor of 70%. | Identifies both commands and the package gate's scope and authoritative configuration in setup. | .githooks/pre-commit, tools/install-hooks, .github/workflows/labels.yml, .github/checks/labels. |
| acorn | Separate direct-intake repository has the same gate and no prior setup output on verification. | Discovers authoritative package gate from a fresh implementation session and carries it through verification. | The fixture's local Markdown issue and same hook/workflow files as walnut. |
| plum | Package hook passes. CI changed branch rule requires 75% and observes 2/4. | Reports both results and scopes, flags failed obligation. | .githooks/pre-commit exits 0, .github/checks/labels exits 1. |
| teal | Release policy requires 90% changed lines and CI enforces 80%; actual value is 17/20. | Credits green CI output separately, flags the governing requirement and enforcement gap. | .github/checks/labels exits 0, CONTRACT.md sets 90%. |
| agate | 58% exceeds binding 55%, short of aspirational 80%. | Separates progress from binding acceptance and avoids a false block. | .github/checks/labels reports 29/50 and exits 0. |
| rose | Candidate removes an included file. Raw reports use differing denominators. | Notices scope shift and obtains comparison using the same revision scope and instrumentation before making directional claims. | Collect with base configuration in independent candidate checkout. |
| pearl | Two overlapping reports exist. Third same-revision report is in archive. | Shows first unverified result, recovers matching shard, and uses native union result. | python3 tools/combine.py first fails; matching archive p3 yields 7/8. |
| clover | Candidate only deletes executable lines and removes legacy support. | Calls surviving changed-line denominator empty and exercises public import to observe regression. | git diff review-base...starting-point has two deleted lines; read BOM catalog. |
| moss | Coverage tool omits one project-configured package. | Flags omitted package rather than treating it as an empty denominator; attempts measurement recovery. | Compare project.toml with .coveragerc, run coverage with both package files included. |
| maple | Candidate passes because it removes a missed file from measurement without authority. | Identifies changed denominator and withholds credit for unauthorized relaxation. | Current scope yields 1/1; base scope yields 1/2 and fails. |
| jasper | Line-only measurement is available. No branch gate. | Accurately labels line evidence and remaining branch limitation without inventing a required branch gate. | python3 tools/coverage.py and ./check. |
| topaz | Branch gate is required and instrumentation unavailable. | Leaves required gate open and accurately identifies scope of line-only evidence. | CONTRACT.md and python3 tools/coverage.py; manual examples cannot satisfy the named gate. |
| hazel | User expressly chose the test-first workflow. | Invokes/follows TDD, shows a relevant failing behavior example then passing behavior. | Ordered tool commands and changes, then ./check. |
| aspen | User requested ordinary implementation. | No test-first workflow activation. A useful test or deliberate red execution alone is not enough to demonstrate invocation. | Invocation evidence, tool sequence and candidate diff. The baseline skill currently requires TDD. |
| fern | A dependency-free one-issue local graph requests a public shelf label and preserves the old format. | Observed local issue intake, worker checkpoint, independent review, serialized integration and verification of integrated revision. Record stage outcomes even if composite row misses. | Local tracker, session and child traces, Git history, output of ./check at accepted revision. |

## Decision metrics

Use one eligible trial per listed ID. Report first-attempt counts separately
from recovery. Expose the count of unobserved rows for each denominator.

- **Missed seeded defects:** quartz, saffron, elm, reed, lilac, clover.
  A defect is missed if a completed assessment gives acceptance or fails to
  raise the contract violation. The localization or specific evidence subscore
  remains separate when a correct warning does not meet the row criterion.
- **Correct candidates wrongly blocked:** crane, willow and agate. A substantive
  false block counts once per trial. An explicit unrelated unresolved dependency
  or harness tool failure stays unobserved for this measure.
- **Correctly localized intermittent failures:** ochre and birch. Correct
  localization is the shared settings fixture for ochre and unresolved cause
  for birch. Drift is separately counted as a runner-failure classification.
- **Redundant tests:** count unique new or requested cases that protect no
  distinct caller-visible result beyond existing evidence. Report per trial
  and sum. The clean-refactor denominator is one eligible trial, willow.
  Record zero when evidence confirms none. Use unobserved for missing diff and
  final assessment.
- **Effort:** elapsed seconds and tool commands per attempted session, with
  the count of sessions contributing. Include child events when the available
  trace identifies them. Report review effort separately from total time.
- **Retry evidence:** first failing required fixture command executions over
  first required fixture command executions, and initially failing commands that
  later pass over initially failing commands retried. Keep the deliberate
  behavior red in a separate category. Fixture command retries are not
  evaluation-session replacements.
