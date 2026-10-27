## What it does

`implement-spec` builds a spec and its tickets on one **integration branch**. The orchestrating agent gives each ticket to a fresh implementer subagent in a separate worktree and branch, coordinates independent review and repairs, and verifies the integrated result.

The tickets form a **task graph**. Each ticket follows a sequential pipeline, while independent tickets can run alongside one another when their prerequisites are satisfied. A dependant becomes ready only after its prerequisites have been reviewed, integrated, and verified.

## When to reach for it

You invoke this by typing `/implement-spec`, and the agent won't reach for it on its own.

| Your situation | Reach for |
| --- | --- |
| A spec split into tickets whose dependencies should drive the build | `/implement-spec` |
| One ticket you want to drive in your own context window | [implement](implement.md) |
| A spec that is not split into tickets yet | [to-tickets](to-tickets.md) first |
| A small piece of agreed work with no useful task graph | [implement](implement.md) directly |

## Prerequisites

- **An issue tracker**, configured by [setup-matt-pocock-skills](setup-matt-pocock-skills.md), and tickets with explicit blocking edges.
- **The design, testing, and review skills.** Workers use [codebase-design](codebase-design.md), [tdd](tdd.md), and [code-review](code-review.md). Include these dependencies in selective installations.
- **A harness that supports delegated agents and isolated worktrees.** The graph can be a chain; concurrency is useful only where independent work is ready.
- **A working verification environment in each worktree.** Required fixtures, local services, and manual acceptance prerequisites must be accounted for. A skipped required check is unresolved verification.

## The dependency pipeline

Within a ticket, implementation comes before review, repairs before re-review, and integration before releasing dependants. The implementer commits a checkpoint before review so the reviewer can inspect an exact base and candidate commit. A fresh review agent coordinates the independent assessment. Supported findings return to the same implementer, preserving useful working knowledge. Focused re-review checks the repairs and affected behavior.

Across tickets, the orchestrator works the **frontier** of ready work. Separate worktrees isolate active implementers. Shared contracts, schemas, or resources can still require ordering even when the tickets touch different files. Integration into the shared branch is serialized, and affected checks establish whether the combined result works.

An expand-contract migration can explicitly defer a guarantee to its final integrate-and-verify ticket. Each intermediate slice still meets its own declared obligations, and final acceptance waits for the deferred guarantees.

The orchestrator keeps issue states, active ownership, pending checks, and accepted and provisional integration commits in one durable ledger. After compaction or interruption, it checks that snapshot against available agent, Git, and verification evidence before dispatching or integrating. Unknown worker state remains unresolved, so a lost session does not silently create a second writer. Tracker closure and implementation readiness are separate: a prerequisite can be integrated and verified while its issue remains open until the final PR merges.

## Keeping the frontier moving

The orchestrator considers the whole pipeline when capacity becomes available. Reviewing a completed candidate can unblock more work than starting another implementation. Useful preparation can happen while workers run: a provisional dependent brief or an outline for review may shorten the next handoff. Preparation stays small and yields to actionable results. Workers send early messages about consequential blockers or contract conflicts; a conflict pauses affected work while the orchestrator contains it and checks the actual changes.

| Current state | What can advance |
| --- | --- |
| Integration checks are pending | Safe independent work from the last accepted commit; further integration and dependent implementation wait |
| No useful action is ready, but active work can advance | Wait for a result using the harness's available mechanisms |
| Neither ready nor active work can advance | Report the blocker and preserve the checkpoint |

Issue sizing and changes to tracked dependencies remain your decisions. Newly discovered safety dependencies constrain work immediately while any tracker change awaits agreement. The aim is less avoidable delay; this guidance has not established a measured speedup.

## Common questions

**Does the agent need this repository to use an installed skill?**

No. Runtime instructions come from installed skill entry points and their bundled supporting files. Dependencies are located through the harness loader or skill catalog; fresh agents receive resolved installed paths. These docs links are for navigation in the fork, not runtime dependencies.

**How is this different from running `/implement` on each ticket myself?**

With `implement`, you dispatch each ticket and keep track of its dependants. `implement-spec` owns that coordination, including ticket review, repair verification, and final whole-spec review. It uses its own worker instructions rather than invoking the user-only `implement` skill.

**Why is the orchestrator waiting while agents run?**

Waiting is appropriate when nothing worthwhile can advance. A completed candidate, an actionable conflict, or cheap preparation that would remove a later delay should prompt coordination first. Counting wait calls alone cannot tell you whether the run is wasting time, and the orchestrator does not invent work to keep every slot busy.

**What changes after context compaction?**

The orchestrator reconciles its saved ledger with the work that is actually observable, including ownership, candidate commits, check results, prior review dispositions, and the remaining repair budget. Missing evidence stays unknown. If ownership cannot be recovered safely, it preserves the work and reports a blocker instead of guessing that a worker finished.

**Does every ready ticket run in parallel?**

No. Parallelism follows from independence in the graph and the available execution capacity. Shared interfaces, migration order, and verification resources may require serialization. Multiple agents never implement concurrently in one worktree.

**Will reviewing a ticket flag the rest of the spec as missing?**

Ticket review checks that ticket's acceptance criteria and applicable parent contracts. Future tickets remain outside that review's implementation scope. A final whole-spec review checks coverage and interactions after all tickets have integrated.

**What stops review and repair from running for hours?**

The orchestrator keeps findings and their dispositions, then requests focused re-review of fixes and their consequences. Optional preferences do not automatically become blockers. Repeated disagreement or repairs that make no progress produce a checkpoint with unresolved findings for arbitration, rather than another unrestricted broad review or a claim of completion.

**Blocked tickets never start, even after their blocker has merged.**

Some trackers count a blocker as open until the final PR merges. The orchestrator computes readiness from its own reviewed, integrated, and verified ticket states during the run, rather than waiting for the tracker's open-issue count to change.

**Two implementers chose different names for the same shared resource.**

Worktrees cannot establish agreement about a shared contract. The orchestrator must settle shared names and interfaces before dispatching dependent work, or order the tickets so the later implementer reads the accepted change. Parallelism does not justify inventing another seam around unseen work.

**A ticket's key test was skipped in its worktree. Is that green?**

No. Gitignored fixtures and local services do not automatically follow a worktree. Make the required verification environment available through the repository's supported setup, or report the missing prerequisite. Preserve worktree isolation and record checks that could not run.

**Does it need GitHub or have to open a pull request?**

No. The configured tracker determines close-out. A PR is created when that workflow requires it or you request one. Otherwise the result is the integration branch and the tracker's corresponding completion state. A draft PR becoming ready is a handoff, not a claim that its linked issues have already closed.

## It's working if

- Ready, independent tickets can progress together, while shared contracts and dependencies determine ordering.
- Each ticket has an identifiable checkpoint, independent review, and verified repair commits.
- A dependant starts only after its prerequisites are integrated and affected checks pass.
- Ticket reviews stay within ticket scope, and final review checks the combined spec.
- Review-ready candidates get attention while independent implementation continues; preparation does not hold up actionable results.
- Interrupted or blocked work preserves ownership, accepted commits, findings, and budget state, with uncertain evidence reported explicitly.
- The report distinguishes completed code, unresolved verification, and tracker or PR state.

## Where it fits

`implement-spec` is the orchestrated build step after [to-tickets](to-tickets.md), which supplies its dependency graph. Use [implement](implement.md) when you prefer to drive one ticket yourself. [Code-review](code-review.md) provides the independent Standards and Spec assessments within the pipeline and at whole-spec close-out.

[Ask-matt](ask-matt.md) maps these choices to the rest of the flow.
