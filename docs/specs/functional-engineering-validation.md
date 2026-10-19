# Functional engineering validation

Specification: [Functional engineering skills](functional-engineering-skills.md).
Baseline: `5beb35b040e3de97e54fa9e386d7e42d15c295c2`.
Integration branch: `functional-engineering-skills`.

## Method and limits

Fresh-context specialist agents loaded the edited skills from repository source and applied them to bounded tasks. They did not read this project's acceptance matrix. The implementation handoff received only the fixture specification and Issues, and a separate reviewer inspected the resulting work. Scenarios used the agreed interfaces without another seam interview.

This checks source-guided behavior in a small set of synthetic tasks. It does not establish automatic skill discovery, installed-plugin behavior, reliability across models, or correctness of real external stores. TypeScript and fast-check were fixture tools, not new requirements for consumer projects. They were installed outside the repository; no production dependency or manifest was changed.

The first integrated instruction review used `d18a776`. A guarded dependency-call correction followed in `4cd1ef5`. A behavioral totality ambiguity was corrected in `4565d33`; the affected handoff was rerun against that version with the original planning artifacts.

## Behavioral evidence

| Specification scenario | Observation | Evidence kind |
| --- | --- | --- |
| Trivial transformation | Formatter used worked examples and compiler checks, with no generators. | Executed fixture |
| Meaningful domain laws | Sorting checks covered element multiplicities, ordering, and input preservation. | Executed fixture |
| Incremental type design | Handoff implementation saved signatures before bodies and recorded compiler feedback and meaningful red-green checks. | Executed fixture |
| Empty input | Design advice offered an explicit absence result or a checked nonempty domain, without a fabricated fallback. | Design response |
| Recursion and termination | Cyclic traversal was identified as partial unless bounded or handled through an explicit cycle policy. | Design response |
| Hidden effects | Injected clock calls, randomness, and shared mutation were identified as effects. | Design response |
| Encapsulated mutation | Local mutable construction was accepted with alias and ownership checks; sorting mutated only its fresh copy. | Design response and executed fixture |
| Raw input validation | Initial handoff threw expected validation errors from broad raw-input interfaces; this exposed a policy ambiguity and prompted a clarification and focused rerun. | Finding corrected; fresh rerun passed |
| Weak property | Idempotence passed for an always-empty sort. Stronger checks exposed data loss. | Executed fixture |
| Generated replay | The sort failure shrank to `[0]`; seed `20261019`, replay path `1:1:0:0:1`, and the same multiplicity failure were observed before fixing it. | Executed fixture |
| State transitions | Advice rejected silent illegal transitions unless specified as no-ops. Reservation checks exercised depletion and rejection. | Design response and executed fixture |
| Effects and persistence | Handoff used an injected store with a competing version update, preventing a stale CAS save and false success. | Executed fixture |
| Composition | Advice checked reservation-before-charge preconditions and rejected unjustified reordering, caching, and retries. | Design response |
| Functional review | The reviewer rejected demands for State methods, polymorphism, and mandatory property tests for simple pure functions. | Review response |
| Architecture consolidation | Advice retained distinct domain-law evidence rather than deleting it because one E2E scenario passed. | Design response |
| Fresh-context handoff | Example-only formatting and reservation properties plus integration checks survived the artifact handoff. | Planning artifacts and executed fixture |
| Authorization boundary | The planning agent wrote only a spec and two local Issues, then stopped. Implementation occurred in a separately authorized run. | Observed artifact boundary |

### Executed testing fixture

[Testing evidence](functional-engineering-evidence/testing.md) preserves exact commands, outputs, replay information, and source snapshots. Node `v18.20.4`, TypeScript `7.0.2`, and fast-check `4.10.2` were used.

The defective sorter passed 100 idempotence checks. The useful property failed after two generated cases and shrank four times. Replay against the defective implementation failed with the same contract violation. After the fix, regression examples, the original replay, and 200 generated cases passed. The unchanged defective implementation remains a negative control in the recorded source. Sample inspection included empty, singleton, duplicate, and negative-valued inputs.

### Handoff and policy correction

[Planning evidence](functional-engineering-evidence/handoff-plan.md) contains the produced specification and two independent Issues. [Initial execution evidence](functional-engineering-evidence/handoff-initial.md) preserves source snapshots and logs. Its compiler check and 11 tests passed, including 1,000 generated reservation cases, and an independent review found no violation of the fixture's narrower artifact requirements.

Further type-design review found that the broad raw-input signatures omitted expected validation rejection from their result types. The reference's phrase "explicit outcome" had allowed an exception-based interpretation without justified partiality. The clarification requires returned rejection at raw-input interfaces, or an explicitly justified partiality exception with caller handling. It does not require brands or a new framework. The initial passing test suite is retained as evidence that green tests alone did not settle this policy question.

[Final handoff evidence](functional-engineering-evidence/handoff-final.md) records the fresh rerun against the clarified guidance. Checked constructors return explicit invalid outcomes before admitting domain values. Formatting retains example-only coverage; reservation retains properties plus persistence integration checks. Strict TypeScript checking and all 11 tests passed, including 1,000 generated reservation cases. An independent reviewer rebuilt the fixture and reported zero Standards and zero Spec findings.

Corrupt stored stock rejects the service promise as a documented store-contract failure, with caller rejection handling, rather than an expected domain rejection. The reviewer distinguished this operational exception from raw user-input validation. Store atomicity remains an assumption modeled by the fixture, not a verified production guarantee.

### Design and review responses

[Design evidence](functional-engineering-evidence/design.md) records the eight supplied scenarios and resulting advice. [Review evidence](functional-engineering-evidence/review.md) records the three challenged review comments and their rejection. These are instruction-application checks, not executions of the described external systems.

## Standards

One P2 finding: the functional reference used "consult that installed skill" for an operative `tdd` dependency, contrary to the explicit Skill-tool invocation convention. It was corrected to a guarded explicit invocation, preserving the already-active condition. Focused inspection confirmed the correction. No other supported Standards findings were reported.

## Spec

No actionable instruction-level findings were reported against the integrated specification. The independent reviewer found the required functional contracts, proportional testing, handoff information, and named dependencies represented. The later behavioral totality ambiguity and its correction are recorded above rather than hidden by that initial review result.

Review summary: one Standards finding, resolved; zero initial Spec findings. Behavioral review additionally identified one totality ambiguity, clarified and checked in a fresh rerun with independent review.

## Repository checks

The initial integrated checks passed for required human-doc sections and their order, local reference targets, absolute links in human docs, prohibited punctuation, invocation metadata pairing, and README/plugin membership for all 27 promoted skills. `npm run check-plugin-version` confirmed version `1.3.1` remains synchronized. Whitespace checks passed. Manifests are unchanged, so strict manifest validation is not triggered.

Final checks also covered the index descriptions, policy clarification, and recorded evidence. No claims about behavioral reliability follow from these structural checks alone.
