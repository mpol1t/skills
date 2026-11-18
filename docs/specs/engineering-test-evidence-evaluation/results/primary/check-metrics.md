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
separately when both are exercised, as in Teal. A fixture runner that exits
before assertions still counts once the documented command runs and returns
its own failure, as in Drift.

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
of the same result contribute one scope. Commands run at the base, probes
bypassing the documented entry point, deliberate test-first red steps,
intermediate implementation states, and wrapper setup failures do not
contribute. Jade's March invocation recorded an authorized quarantine and
its bare invocation exited with usage help. The April invocation exercised
the required test and contributes one check.

Evidence references are relative to each trial's `attempt-1`. For a
compressed child session, the comma-separated numbers are the saved
`source_line` values of the tool call and its result. For a grouped tool
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
