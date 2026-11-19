# Primary check counts

The [check inventory](check-metrics.csv) records the commands behind the corrected
aggregate for all 26 primary trials. The original scoring JSON and frozen
rubric remain available for audit. The trial scores and the first-attempt
tally of 20 met, five missed, and one unobserved are the original results.

## Counting unit

Count the first observed execution of each distinct documented fixture suite,
verification command, or applicable gate at the selected candidate state.
Count a hook and its underlying suite as one check when the hook only
invokes that suite. A command that reports both test and branch outcomes in one
invocation contributes one check. Distinct governing and CI thresholds count
separately when both are exercised, as in Teal.

An eligible invocation supplies any required scope selectors and reaches the
selected check or its own runner. A fixture runner can fail after accepting
that invocation and before starting assertions, as in Drift. The native gate
can likewise fail on a missing input it is responsible for validating, as in
Pearl. A usage response rejecting a missing or invalid selector occurs before
scope selection. A shell, sandbox, or snapshot setup failure can also prevent
the check from running. These observations stay in the trace and outside the
check counts. Eligibility depends on the reached scope, regardless of exit
code or assertion count.

Use the frozen candidate for review and diagnosis, and the starting state for
setup. For implementation, use the last verified candidate state. Acorn and
Aspen have reviewed clone commits, Hazel has a captured working-tree diff,
and Fern has a verified worker checkpoint. Fern's integrated candidate check
is unobserved and does not contribute an execution.

An execution uses the candidate's actual command and configured scope. A zero
exit describes that execution. Rose, Moss, and Maple each have a candidate
coverage execution with a narrower include set, and a separately unobserved
comparable or governing scope. Topaz has a tested suite and an unobserved
required branch gate. Its line-only report and Jasper's optional line report
are diagnostic evidence outside the execution count.

Count one retry denominator entry for each initially failing check that was
run again at the same candidate with the same check scope. Count the entry in
the numerator if a later eligible execution returned zero. Normal changes to
fixture runtime state and recovery of missing same-revision CI input can
occur between attempts. The inventory cites an eligible passing retry when
one exists, or a repeated failure when all observed retries fail. Independent
child confirmation on the same candidate is eligible. Repeated confirmations
of the same result contribute one scope. Commands run at the base, optional
diagnostics, probes bypassing the documented entry point, deliberate
test-first red steps, and intermediate implementation states do not
contribute. Jade's March invocation recorded an authorized quarantine.

Jade's generic fixture README says to run `./check`. The check script requires
a date to select a scope. The bare command was repeated and each attempt
returned usage with exit 2 before selecting a date or entering the runner.
April is the one observed check because it selected an active test scope.
The candidate script and repeated examples are in
`jade/attempt-1/session-3.jsonl.gz` at source lines 23, 28, 30, and 34.
See the first grouped April and bare results in
[jade's root event log](jade/attempt-1/events.jsonl).

## Execution order

The inventory audits the recorded calls and results in the root and child
sessions of all 26 primary trials. Within the selected candidate state,
choose the earliest eligible execution by recorded tool-call timestamp, and
use the corresponding result to verify that the check ran and returned the
recorded exit. For sequential invocations within one call, follow the
executed command and output order. Parallel invocations within one call
share its timestamp. The trace exposes the call interval and grouped
results for those invocations only.

If separate call intervals overlap, use the recorded dispatch order and
check the exits in both groups. The two initial Teal groups overlap and
agree on each exit. The later failing child confirmation, dispatched after
both groups returned, establishes the retry. In Rose, the child group
returned both candidate outcomes at 21:35:34.498 UTC. The later root archive
call dispatched at 21:35:38.338 UTC and confirmed both exits. The child
group supplies the first outcomes. These are trace timestamps rather than
individual process start or finish times.

Evidence references in the CSV are relative to each trial's `attempt-1`.
For a compressed root or child session, the comma-separated numbers are the
saved `source_line` values of the tool call and its result. The associated
UTC columns reproduce those records' timestamps. For an unobserved scope,
the reference points to evidence of the scope gap and has no execution
timestamps. For a grouped tool
call that ran multiple commands, `first_detail` and `retry_detail` identify
the relevant result within the event. The inventory stores exit codes from
the check itself, including when the surrounding shell or Python command
returned a different code.

## Recompute the aggregate

Run from this directory.

```sh
python3 -B - <<'PY'
import csv

with open("check-metrics.csv", newline="") as source:
    rows = list(csv.DictReader(source))
observed = [row for row in rows if row["observation"] == "observed"]
failed = [row for row in observed if int(row["first_exit"]) != 0]
retried = [row for row in failed if row["retry_exit"]]
passed = [row for row in retried if int(row["retry_exit"]) == 0]
print(f"Initially failing: {len(failed)}/{len(observed)}")
print(f"Passed on retry: {len(passed)}/{len(retried)}")
print(f"Unobserved scopes: {len(rows) - len(observed)}")
PY
```

The result is 6/36 initially failing, 4/6 passed on retry, and five
unobserved check scopes. These are check executions within primary trials.
The cohort had zero evaluation-session replacements.
