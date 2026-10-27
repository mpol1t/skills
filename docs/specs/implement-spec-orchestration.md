# Implement-spec orchestration specification

Status: Implementation authorized by the user through `implement-spec`. Local delivery only; issue publication has not been requested.

## Problem Statement

During long implementation runs, the orchestrator can spend time waiting for agents while useful coordination and preparation remain available. The problem can become more visible after context compaction, when the orchestrator must reconstruct the state of multiple workers and their dependencies. The number of wait calls alone does not establish a delay: waiting is appropriate when nothing useful can advance.

The current skill permits independent issues to progress concurrently and requires a durable ledger, but does not explicitly guide scheduling around pending results, proactive preparation, or recovery of active scheduling state. The goal is to reduce avoidable delay while preserving review, verification, isolation, and dependency guarantees, and keeping agent communication proportionate.

## Solution

Make scheduling a continuous, lightweight responsibility of the orchestrator. It identifies actions that can reduce future delays, responds to useful worker signals, and waits for events when no worthwhile action is available and active work can still advance. When neither ready nor active work can advance the run, it reports blockers. The ledger supports recovery across compaction and interruption, but is reconciled against current evidence before decisions with effects. The orchestrator adapts its use of limited capacity to the work at hand.

## User Stories

1. As a user, I want useful coordination to continue while workers run, so that avoidable orchestration delays do not extend the run.
2. As a user, I want the orchestrator to wait when nothing useful can advance, so that it does not create busywork or waste calls.
3. As a user, I want actions that unblock downstream work considered promptly, so that the critical path receives attention.
4. As a user, I want independent work to proceed during integration checks, so that verification does not unnecessarily idle the pipeline.
5. As a user, I want reviews prepared ahead of completion where useful, so that candidates can be reviewed promptly.
6. As a user, I want dependent work prepared provisionally, so that an accepted prerequisite can release it without unnecessary delay.
7. As a user, I want workers to surface actionable conflicts or blockers early, so that the schedule can adapt before the final handback.
8. As a user, I want communication limited to consequential information, so that status chatter does not become another bottleneck.
9. As a user, I want capacity allocated to the current bottleneck, so that implementation does not crowd out review or leave useful slots idle without reason.
10. As a user, I want scheduling state recoverable after compaction, so that long runs do not lose track of active work.
11. As a user, I want recovery to verify stale or uncertain state, so that it does not duplicate workers or integrate unchecked changes.
12. As a user, I want existing review and verification gates preserved, so that faster coordination does not weaken the result.
13. As a user, I want control over issue sizing and tracked graph changes, so that the orchestrator does not silently reshape the agreed work.
14. As a user, I want meaningful bottlenecks reported at handoff, so that I can judge whether the workflow needs further improvement.

## Implementation Decisions

### Relationship to the existing skill

This is an additive amendment to the existing `implement-spec` skill, reviewed against repository commit `f1f413422770844a83fb7feb51071a58b0a66d07`. It clarifies scheduling, actionable communication, and recovery; it does not replace the worker contract or delivery pipeline. All existing requirements remain in force unless an amendment explicitly identifies a change. If implementation exposes a conflict not resolved here, surface it rather than silently dropping an existing requirement.

### Confirmed requirements

- Optimize orchestration for less avoidable waiting and better coordination across the whole pipeline. Do not optimize the number of wait calls as a proxy for success.
- The user owns issue sizing. Within an issue's existing scope, the orchestrator may adjust supporting delegation, such as read-only exploration or brief preparation, while preserving a fresh implementer per issue, its exclusive worktree and branch, and the same implementer's context for repairs and stale-base reconciliation. Final repairs return to the responsible implementer where available, as in the original skill. This does not authorize multiple implementers to share that worktree or replace required independent review. Ask before splitting or otherwise changing tracked issues or their dependency graph; do not change acceptance criteria without agreement. Routine tracker actions already authorized by the workflow remain permitted. Immediately record and enforce newly discovered safety dependencies locally; only the corresponding tracker change awaits agreement.
- Preserve existing worker isolation, review and repair, sole-writer integration, exact-SHA evidence, verification, and the rule that only integrated and verified work releases implementation dependencies.
- Allow independent scheduling and preparation while integration checks are pending. A pending integration is provisional, not accepted. No further integration or dependent release may occur until required checks pass; workers start from the last accepted integration SHA. On failure, preserve the failure and accepted checkpoints and follow the existing repair and review process. Independent work may continue if safe.
- When likely to remove a later delay at modest cost, prepare review briefs using the available authoritative artifacts before candidates arrive, but dispatch review only with the committed candidate SHA, base, and relevant evidence. Refresh prepared material if the contracts or evidence change. Preserve reviewer independence.
- When useful at modest cost, prepare dependent briefs and inspect requirements before prerequisites are accepted. No mandatory preparation artifact is required. Mark assumptions provisional and refresh them against accepted results. Do not start implementation that requires the unaccepted prerequisite.
- Workers send early signals when they can change another agent's work, scheduling, a contract, or a decision. Include the relevant issue and impact. Routine progress messages are unnecessary; final handbacks remain required.
- Reconsider scheduling at dispatch, actionable results or messages, integration acceptance, and recovery. Favor actions that remove likely bottlenecks, while accounting for their cost and urgency. Preparation is bounded and interruptible; it must not starve ready results, review, integration, or inexpensive dispatch. No fixed ordering or reserved slot is required.
- Keep a durable, concise scheduling snapshot within the existing ledger: active work and owners or handles, pending results and checks, accepted and provisional SHAs, dependencies, ready work, and next useful actions. Retain prior finding dispositions and review/repair budget state across recovery so compaction cannot reset a stalled loop. Update it at material transitions and ensure it is current before waiting or handing off, proportionate to the run. Do not duplicate state into a separate ledger or rewrite unchanged entries on each wait. Reconcile duplicate, delayed, or superseded messages with authoritative ownership, issue state, and candidate SHA before taking action.
- On compaction or resumption, reconcile the ledger with available agent or session state, worktrees, branches, commits, and check evidence before dispatch or integration. Treat unobservable state as unknown, not finished. Avoid duplicate writers, preserving committed and uncommitted work; recover from reliable artifacts or surface the uncertainty if ownership cannot be established.
- When no useful action is ready but active work can still advance, wait for an actionable event using the harness's supported mechanism. If unfinished work has neither a ready action nor an active operation that can advance it, report the blockers instead of waiting indefinitely or claiming completion. If wait-any or event delivery is unavailable, use the available completion or polling mechanism without inventing guarantees about its behavior. No fixed polling interval is prescribed.
- Report meaningful bottlenecks and avoidable delays at handoff when observed. A detailed event log, mandatory metrics, and performance claims are not required.

### Operating boundaries

Capacity decisions are adaptive, not a prediction that a critical path can always be known. Do not reserve a review slot by default. A review or integration may be prioritized over another implementation when evidence suggests it will unblock work sooner, subject to available harness controls. Do not preempt or cancel active work merely to satisfy a scheduling heuristic. Account for nested review agents and failed dispatches; never skip a required review because capacity is limited. If no compliant schedule is possible, report the capacity blocker.

The orchestrator owns scheduling, enforces agreed shared contracts, and retains authority over evidence-based review dispositions, including rejecting findings with evidence and judging optional recommendations. It escalates unresolved product or contract choices to the user rather than deciding them on the user's behalf. A worker that discovers a potentially conflicting shared-contract change pauses its affected work, preserves its state, and communicates the conflict promptly. The orchestrator records the constraint and contains affected work, including work already in progress, then reconciles actual commits and contracts before deciding how to proceed. Independent work may continue. Review any resulting changes as required. Agent communication does not substitute for review or verification.

Run checks asynchronously where the harness supports it and doing so is safe; bind evidence to the exact checked tree and avoid concurrent use of mutable integration resources. Bound preparation to avoid delaying actionable results, while acknowledging that some harness operations cannot be interrupted.

Recovery cannot guarantee that an inaccessible worker has stopped or that a result has not been lost. Do not advance a gate on uncertain evidence. Preserve work and report a blocker when safe ownership or required evidence cannot be established.

## Testing Decisions

For this delivery, the user explicitly requested multiple review rounds instead of implementing actual tests. Use independent Standards and Spec reviews, a final whole-spec review, and structural checks. The scenarios below remain review prompts and future evaluation guidance; do not claim they were executed or that runtime performance was measured.

Evaluate observable scheduling decisions and artifacts using realistic scenarios, not exact instruction wording or wait-call counts. Compare with current behavior where feasible. Record the skill version, harness capabilities, scenario, decisions, evidence, and outcomes; do not claim general latency improvements from isolated examples. Use the smallest useful scenario or harness that can observe the decisions and safety gates. Execute representative scenarios with a scripted harness or documented manual runs, recording event order, relevant immutable evidence, observed actions, and results. Label scenarios that have only been inspected rather than executed as review scenarios, not passing tests. If a later evaluation claims a latency improvement, compare suitable workloads and harness conditions and record elapsed time to a verified result alongside success, rework, and resource use; do not generalize from a single run.

| Scenario | Expected behavior |
| --- | --- |
| Review-ready candidate arrives while independent implementation runs and review capacity is available | Dispatch review without first waiting for that independent implementation to finish. |
| Active worker and actionable independent preparation | Do worthwhile bounded work before waiting, without delaying an already actionable result. |
| No ready action, active work can still advance | Wait using available harness capabilities without repeated busywork or claiming completion. |
| Unfinished work, no ready action and no active operation can advance it | Report blockers rather than waiting indefinitely or claiming completion. |
| Integration checks pending | Continue safe independent coordination from the accepted SHA; do not integrate again or release dependants. |
| Integration check fails | Keep the accepted checkpoint, block integration and dependent release, and repair and re-review before advancement; independent work continues only when safe. |
| Candidate completes after a prepared review brief | Refresh the brief with the exact committed SHA and evidence, then dispatch independent review. |
| Prerequisite changes during review | Refresh provisional dependent preparation; do not start dependent implementation before acceptance. |
| Worker reports a contract conflict | Pause affected work and contain the conflict, including work already started; reconcile changes and review as needed, without requiring routine status messages. |
| Limited capacity with a review ready | Consider the effect of implementation dispatch on review delay; account for nested reviewer needs and failed dispatches, and report a blocker if no compliant schedule is possible. |
| Duplicate or stale worker message | Reconcile the event with current ownership and candidate SHA; do not accept stale evidence or duplicate an action. |
| Newly discovered safety dependency | Record and enforce it immediately, and ask before changing the tracked graph. |
| Compaction during active work, followed by a duplicate delayed result | Reconcile the scheduling snapshot with available actual state, resume without duplicate ownership, and do not accept stale evidence. |
| Agent or check state unavailable after recovery | Mark the state unknown, preserve checkpoints, and do not treat missing evidence as success or start a potentially conflicting writer. |
| Tracked issue appears too large | Leave issue sizing to the user; adapt internal delegation only within its scope and ask before tracked graph changes. |
| Harness lacks event or wait-any support | Use available mechanisms and make no unsupported wake-up guarantees. |

Review the updated skill and its human-facing docs together. Check that the router still accurately describes the flow when the changed behavior affects it. Behavioral scenarios supplement repository consistency checks; neither constitutes a controlled production performance evaluation.

### Original-requirement regression checklist

During eventual implementation, compare the complete original skill with the edited skill and record a disposition for each requirement: preserved, clarified by a named amendment, or unresolved. An unresolved conflict prevents claiming the implementation complete. This is a review of the skill edit, not a new checklist imposed on every consumer run.

At minimum, cover these requirement groups, including their details in the original skill:

- Invocation policy, installed dependency resolution, and tracker setup.
- Graph validation, contract independence, dependency discovery, and serialization of overlapping work.
- Initial review base, last accepted SHA, existing ledger evidence, and checkpoint preservation.
- Proportionate review and repair budgets, escalation on stalled progress, and no acceptance through budget exhaustion.
- Manual acceptance dependencies, implemented/reviewed/accepted distinctions, and deferred verification guarantees.
- Fresh implementers, retained repair context, exclusive worktrees and branches, and accepted-base dispatch.
- Complete worker briefs, `codebase-design` and `tdd` use, fixtures and tooling checks, committed candidate handback, and evidence isolation.
- Fresh independent `code-review`, separate Standards and Spec axes, finding dispositions, focused repair review, and no duplicate review of unchanged candidates.
- Reconciliation of stale candidates, affected checks, review coverage, sole-writer integration, combined invariants, and failed/accepted checkpoints.
- Draft PR timing and closure semantics, final whole-spec checks and fresh review, final repair pipeline, ready-for-review transition, handoff, and worktree cleanup or retention.

## Out of Scope

- Automatic issue sizing, decomposition, acceptance-criteria changes, or tracker graph changes without user agreement.
- Speculative implementation of work whose prerequisite is not integrated and verified.
- Relaxing review, verification, isolation, or integration guarantees.
- A new orchestration service, mandatory telemetry system, fixed polling interval, or guaranteed speedup.
- Changes to harness capabilities, cancellation policy, model selection, or unrelated skills unless independently justified.
- Publishing issues or expanding this authorized delivery beyond the skill and its associated documentation.

## Further Notes

The observed symptom is increased waiting, especially in longer runs after context compaction. The root cause has not been established from a run trace; the proposed recovery and scheduling guidance should be evaluated as a hypothesis. Research evidence and its limitations are captured separately in the accompanying research note. The draft received independent reviews of safety and scheduling, spec testability and repository conventions, and alignment with the research. Their findings strengthened conflict containment, stale-event handling, capacity constraints, recovery, and evaluation. No reviewer established a measured latency benefit. The underlying cause of the observed waits remains unresolved until representative traces are examined; the user has now authorized implementation with review-based validation.

### Compatibility review

A second cohort reviewed compatibility with the original skill, concurrency and recovery, and scope and evaluation. The independent assessments converged on preserving implementer ownership, narrowing contract authority, and extending one ledger. Their additional findings corrected indefinite waiting on terminal blockers, preserved review dispositions and budget state through recovery, and made preparation conditional rather than mandatory. The compatibility checklist supplements observable scheduling scenarios; it does not establish runtime behavior or a speedup.
