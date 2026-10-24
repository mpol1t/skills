## What it does

`implement-spec` builds a [spec](https://www.aihero.dev/ai-coding-dictionary/spec) and its [tickets](https://www.aihero.dev/ai-coding-dictionary/ticket) on one **integration branch**. The orchestrating [agent](https://www.aihero.dev/ai-coding-dictionary/agent) gives each ticket to a fresh implementer [subagent](https://www.aihero.dev/ai-coding-dictionary/subagent) in a separate worktree and branch, coordinates independent review and repairs, and verifies the integrated result.

The tickets form a **task graph**. Each ticket follows a sequential pipeline, while independent tickets can run alongside one another when their prerequisites are satisfied. A dependant becomes ready only after its prerequisites have been reviewed, integrated, and verified.

## When to reach for it

You invoke this by typing `/implement-spec`, and the agent won't reach for it on its own.

| Your situation | Reach for |
| --- | --- |
| A spec split into tickets whose dependencies should drive the build | `/implement-spec` |
| One ticket you want to drive in your own [context window](https://www.aihero.dev/ai-coding-dictionary/context-window) | [implement](https://aihero.dev/skills-implement) |
| A spec that is not split into tickets yet | [to-tickets](https://aihero.dev/skills-to-tickets) first |
| A small piece of agreed work with no useful task graph | [implement](https://aihero.dev/skills-implement) directly |

## Prerequisites

- **An issue tracker**, configured by [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills), and tickets with explicit blocking edges.
- **The design, testing, and review skills.** Workers use [codebase-design](https://aihero.dev/skills-codebase-design), [tdd](https://aihero.dev/skills-tdd), and [code-review](https://aihero.dev/skills-code-review). Include these dependencies in selective installations.
- **A [harness](https://www.aihero.dev/ai-coding-dictionary/harness) that supports delegated agents and isolated worktrees.** The graph can be a chain; concurrency is useful only where independent work is ready.
- **A working verification environment in each worktree.** Required fixtures, local services, and manual acceptance prerequisites must be accounted for. A skipped required check is unresolved verification.

## The dependency pipeline

Within a ticket, implementation comes before review, repairs before re-review, and integration before releasing dependants. The implementer commits a checkpoint before review so the reviewer can inspect an exact base and candidate commit. A fresh review agent coordinates the independent assessment. Supported findings return to the same implementer, preserving useful working knowledge. Focused re-review checks the repairs and affected behavior.

Across tickets, the orchestrator works the **frontier** of ready work. Separate worktrees isolate active implementers. Shared contracts, schemas, or resources can still require ordering even when the tickets touch different files. Integration into the shared branch is serialized, and affected checks establish whether the combined result works.

An expand-contract migration can explicitly defer a guarantee to its final integrate-and-verify ticket. Each intermediate slice still meets its own declared obligations, and final acceptance waits for the deferred guarantees.

The orchestrator keeps durable ticket states and accepted integration commits through [context pointers](https://www.aihero.dev/ai-coding-dictionary/context-pointer). Tracker closure and implementation readiness are separate: a prerequisite can be integrated and verified while its issue remains open until the final PR merges.

## Common questions

**How is this different from running `/implement` on each ticket myself?**

With `implement`, you dispatch each ticket and keep track of its dependants. `implement-spec` owns that coordination, including ticket review, repair verification, and final whole-spec review. It uses its own worker instructions rather than invoking the user-only `implement` skill.

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
- Interrupted or blocked work leaves enough state to resume without rediscovering accepted commits and findings.
- The report distinguishes completed code, unresolved verification, and tracker or PR state.

## Where it fits

`implement-spec` is the orchestrated build step after [to-tickets](https://aihero.dev/skills-to-tickets), which supplies its dependency graph. Use [implement](https://aihero.dev/skills-implement) when you prefer to drive one ticket yourself. [Code-review](https://aihero.dev/skills-code-review) provides the independent Standards and Spec assessments within the pipeline and at whole-spec close-out.

[Ask-matt](https://aihero.dev/skills-ask-matt) maps these choices to the rest of the flow.
