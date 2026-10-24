---
name: implement-spec
description: "Implement a spec's ticket graph through isolated workers, independent review, and verified integration."
disable-model-invocation: true
---

Load model-invoked dependencies through the harness's skill loader. If no loader is exposed, resolve their installed `SKILL.md` paths from the available skill catalog and read those entry points, preserving invocation policy. Report unavailable dependencies instead of guessing an installation directory or using this repository's human-facing docs as instructions.


Implement the provided spec and its tickets on a single **integration branch**. The invoking agent is the **orchestrator**: it owns scheduling, review dispositions, and integration. Each ticket moves through a pipeline:

**Implement → checkpoint → review → repair and re-review as needed → integrate → verify.**

Stages within a ticket have strict dependencies. Tickets whose prerequisites are satisfied can progress concurrently when their contracts permit independent work. Every active implementer owns a separate worktree and branch; integration into the shared branch is serialized through one writer. Parallelism comes from the task graph, not multiple implementers editing one worktree.

The issue tracker should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## 1. Establish the graph and checkpoints

Read the spec, tickets, blocking edges, and applicable repository instructions. Check for missing prerequisites and cycles. Include shared schemas, interfaces, generated artifacts, and behavioral contracts when deciding whether ready tickets are independent; different files alone are insufficient. Order overlapping work and record newly discovered dependencies.

Create or resume the integration branch, recording its initial review base and last accepted SHA. Keep a small durable ledger accessible to future workers: ticket status, dependencies, worktree/branch, base and candidate SHAs, checks, review findings and dispositions, and accepted integration SHA. Report its location when handing off or stopping.

Set an effort budget for review and repair proportionate to the task before dispatching workers. Extend it only when new evidence justifies the cost within existing authorization.

Distinguish **implemented**, **reviewed**, and **integrated and verified**. Only the last satisfies an implementation dependency. Use the ledger to track this even when the tracker keeps tickets open until a PR merges. A required manual acceptance step remains a dependency until its evidence is available. If unfinished work has no ready ticket, wait for active workers; if none can advance, report the blockers instead of claiming completion.

Carry each ticket's verification contract, including any explicitly deferred guarantees in an expand-contract migration. Intermediate slices must satisfy their declared obligations; the final integrate-and-verify ticket owns guarantees explicitly deferred to it.

## 2. Dispatch ready work

Choose expertise, available model capability, and context deliberately. Use fresh implementers per ticket; retain each implementer's context for repairs. Give fresh reviewers the authoritative artifacts and evidence rather than the implementer's conversational rationale. Model diversity can add perspective when available; independent briefs and evidence remain necessary.

Dispatch only independent ready tickets, within available capacity. If exploration would unblock several workers, an exploration subagent can save shared notes outside the repo and return context pointers. Keep primary-source pointers available so workers can check the notes.

Each implementer receives a precise brief containing:

- The assigned ticket, parent spec, acceptance criteria, contracts, repository rules, and relevant decisions or research pointers.
- Its exclusive worktree and branch, based on the accepted integration SHA, plus any local prerequisites needed to run checks. Preserve existing work when resuming; reconcile a stale base without discarding changes.
- The resolved absolute installed `SKILL.md` paths for required model-invoked dependencies, accessible from the worker's workspace, alongside their registered names. Workers load those entry points using the loader or catalog fallback above; supporting files resolve relative to their containing file.
- Instructions to call the Skill tool with `codebase-design` for changed domain contracts, then separately with `tdd` to build one behavior at a time from its smallest useful types and signatures. Report unavailable dependencies.
- The ticket's agreed verification choices: examples, properties, integration checks, applicable invariants, and justified assumptions. Check worktree fixtures and tooling explicitly; skipped or unavailable checks are not passing evidence.
- The required handback: committed candidate SHA, review base SHA, verification results from that committed tree, assumptions, and blockers. Use an isolated checkout if excluded working changes could influence checks; bind evidence and local prerequisites to the candidate SHA. The orchestrator owns the independent review and integration stages.

This worker contract is part of this skill. `implement` remains a human-invoked entry point; delegation does not invoke it or duplicate its review stage.

## 3. Review each candidate and resolve findings

For each committed candidate, dispatch a fresh review agent with instructions to call the Skill tool with `code-review`. Supply the resolved installed `code-review` entry-point path and its required dependency paths as well as the exact base and candidate SHAs, ticket as the immediate spec, parent contracts, standards, and verification evidence. Parent requirements inform the slice without treating later tickets' behavior as missing from this ticket. The review skill supplies the independent Standards and Spec axes.

Return actionable findings to the same implementer. Keep finding IDs and dispositions: fixed, rejected with evidence, or awaiting a decision. Requirement violations and defects block acceptance; optional recommendations require judgement rather than automatic implementation. Preserve the separate review axes when making dispositions.

Have the implementer commit repairs and rerun affected checks on the committed tree. Request focused re-review with the original base, previous reviewed candidate, new candidate SHA, and prior findings. Review the complete repair diff and affected behavior, including regressions the fix could introduce. Retain prior findings and expand review for substantial design changes. An unchanged candidate needs no duplicate review.

Continue while evidence resolves substantive objections, within the effort budget for the task. Repeated disagreement, oscillating fixes, or no progress calls for investigation or escalation of unresolved product or contract choices. Preserve checkpoints and report remaining blockers; exhausting the budget does not accept the ticket. Missing required review or checks leaves the ticket unaccepted.

## 4. Integrate and advance the frontier

Integrate one reviewed ticket at a time through the integration branch's sole writer. If its base is behind the accepted tip, have its implementer reconcile against that tip in its own worktree, rerun affected checks, and obtain review of changes introduced by reconciliation before integration. Record the resulting candidate SHA and review coverage.

After integration, recheck affected shared contracts and combined behavior at the resulting integration SHA. Individually passing slices do not establish their combined invariants. Mark the ticket accepted in the ledger and release dependants only when its applicable integration checks pass. If integration fails, record the failed SHA and last accepted SHA, stop further integrations and dependency release, and repair and re-review the failure before advancing.

Recompute the ready frontier after each acceptance. Fresh implementers may start newly ready tickets while other independent tickets remain in implementation or review. Serialize work that shares mutable contracts or integration resources.

If the configured tracker closes work through PRs, or the user requested one, open a draft PR after the first accepted integration, marked as closing the spec and tickets. Tracker closure and implementation readiness remain separate states.

## 5. Verify the whole spec and hand off

Once all ticket obligations, including deferred integration guarantees, are met, run the required whole-spec checks and dispatch a fresh agent to call the Skill tool with `code-review` over the integration branch's recorded initial base and exact current SHA, using the entire spec. Supply the same installed entry-point and dependency paths as for ticket review. This review checks cross-ticket behavior and scope.

Return supported findings to the responsible implementer where available. Run final repairs through the same isolated worker, checkpoint, focused re-review, serialized integration, and verification stages. Apply the same evidence and progress criteria as ticket review. Record the final accepted SHA only after blocking findings are resolved and required checks pass on that tree.

If a draft PR exists, mark it ready for review. Otherwise resolve tickets the way the configured tracker closes work, and report the integration branch. Report verification, review dispositions, remaining assumptions, and ledger location. Clean up completed worker worktrees after preserving their accepted commits; retain interrupted or unresolved work for resumption.
