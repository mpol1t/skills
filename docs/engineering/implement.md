## What it does

`implement` builds work that has already been decided. You point it at a ticket, a spec, or the plan you just agreed in the conversation, and it writes the code, drives [tdd](tdd.md) at the seams, typechecks as it goes, commits a reviewable checkpoint to the current branch, and runs [code-review](code-review.md) against that exact commit. Supported findings return to implementation, followed by focused re-review of the repairs.

It carries settled decisions into implementation rather than redesigning the work. Missing requirements or contradictory contracts remain explicit questions instead of becoming invented behavior. The skill's job is to turn agreed work into verified, reviewed commits. That is what separates it from typing "build this" at a fresh agent, which often redesigns the work while it builds it.

## When to reach for it

You invoke this by typing `/implement` yourself, and the agent won't reach for it on its own. It ships with `disable-model-invocation: true`, so no other skill can call it either. Wherever [ask-matt](ask-matt.md) or [to-tickets](to-tickets.md) says "then `/implement` per ticket", that is an instruction to you, not something the agent will do unprompted.

Where the work currently lives decides whether this is the right skill:

| The work is… | Reach for |
| --- | --- |
| A ticket on the tracker | `/implement #42`, one ticket per session, clearing context between tickets |
| A spec, not yet split up, and the build spans sessions | [to-tickets](to-tickets.md) first, then `/implement` per ticket |
| A spec, and the build is small | `/implement` directly against the spec |
| Only in the conversation you just had, and it's still small | `/implement` right there, in the same window |
| Not written down anywhere yet | [grill-with-docs](grill-with-docs.md), or [grill-me](../productivity/grill-me.md) if there's no codebase |
| One concrete behaviour you want test-first, with no spec | [tdd](tdd.md) directly |
| Already built, and you want it checked | [code-review](code-review.md) directly |

The same-session case is supported directly: an agreed conversation can supply the work without an intermediate spec file.

## Prerequisites

`implement` commits to the branch you are on. It does not create one, and it does not ask. Check you are on the branch you want the work on before you start.

If the tickets came from [to-tickets](to-tickets.md), [setup-matt-pocock-skills](setup-matt-pocock-skills.md) configured the tracker they live on. `code-review` reads the same configuration to find the originating spec at close-out.

Changed domain behavior uses [codebase-design](codebase-design.md) for functional contracts, alongside `tdd` for verification. Include those dependencies when installing selected skills.

## What one run does

A run has five steps, in order:

1. Read the work and its applicable contracts, following parent-spec references where needed, and recover agreed seams.
2. Drive [tdd](tdd.md) at those seams, establishing the smallest useful types and signatures for one behavior before its red-green slice.
3. Typecheck often, run single test files as it goes.
4. Run the full test suite once, at the end.
5. Commit a checkpoint, run [code-review](code-review.md), and resolve supported findings with repair commits, affected checks, and focused re-review.

One run covers one ticket. The tickets [to-tickets](to-tickets.md) produces are tracer-bullet vertical slices sized to fit a single fresh context window, so the intended rhythm is: clear context, implement one ticket, commit, clear again. Each ticket is self-contained, so you can discard the previous ticket's context.

## Pre-agreed seams

The skill's central idea is the **seam**, the public boundary you observe behaviour at without reaching inside. Tests live at seams. When the seam is agreed before any code exists, the tests last, and you can rewrite the implementation underneath without changing them.

The agreement travels with the contract and verification decisions in the spec or ticket. `implement` follows parent-spec references when needed and uses `tdd` to resolve missing agreements. It reuses existing agreements rather than asking again. Stable pure-domain interfaces and integration interfaces may both be needed when they cover different risks.

Verification stays proportionate: examples for concrete cases, properties for useful laws, and integration checks for effects. A justified example-only decision survives implementation. Before review, the agent accounts for contract obligations and assumptions, including temporary holes or unsafe assertions introduced during development.

## Common questions

**Will type-driven development or property testing make a small change elaborate?**

They should not. Type design is limited to the current behavior slice, and the agent chooses tests for useful evidence. A trivial function can use focused example-based unit tests or adequate existing coverage without generators or a new harness.

**It finished, but my ticket is still open and the acceptance criteria are still unchecked.**

Tracker closure is separate from completing the code. `implement` now resolves supported review findings and verifies the repairs, but it does not automatically close the work item or tick its acceptance boxes. Reconcile the criteria and close the ticket using your tracker's workflow. On a dependency chain, record which prerequisites have been integrated and verified so readiness remains visible even when the tracker keeps issues open until a PR merges.

**Can I point it at all my tickets at once, or run several in parallel?**

Not with `/implement`: one invocation, one ticket. For a whole spec in one run, use [implement-spec](implement-spec.md), which gives each ticket on the ready frontier to a subagent in its own worktree, then merges the results onto one integration branch. Running several `/implement` sessions side by side in one checkout is worse than unsupported. One field report describes a `git commit --amend` in one session landing on another session's commit, a stash vanishing from `refs/stash`, and commits landing on the wrong branch, all in a single afternoon across three issues. The sessions share one working directory, one index, and one HEAD. Users work around this with git worktrees, but `refs/stash` is shared across worktrees too, so worktrees alone do not fix the stash case.

**Can it open a pull request instead of committing?**

Not built in. It commits straight to the current branch. Several people find this too eager, because the code lands before they can verify it works. There is no configuration flag and no PR mode. People override it in the invocation ("commit to a branch and open a PR") or by editing their local copy of the skill. When the agent does write the PR, [pr](pr.md) shapes its body.

**`code-review` says it cannot see my changes.**

`code-review` reads committed changes and excludes staged and working-tree changes. `implement` now creates a checkpoint first and supplies the starting commit and candidate commit, so the reviewer sees the implementation. Repair commits receive focused re-review before the run reports completion.

The Standards and Spec reviewers assess the code in separate contexts. A reviewer needs the ticket, relevant decisions, and repository rules, rather than the implementer's narrative about why the solution is correct.

**One ticket burned 150k tokens. Am I using it wrong?**

Probably not. The ticket is more likely too big. A run does codebase exploration, a red-green loop per seam, a full suite, and a review, so a non-trivial ticket exceeding 100k tokens is normal rather than a sign something broke. The fix is upstream. Right-size the tickets in [to-tickets](to-tickets.md) so each fits one fresh window. If a single ticket keeps going over, split it rather than raising the effort level.

**`/implement #2` in a fresh session worked on something completely unrelated.**

The agent resolved `#2` against another numbered list in context, such as a todo file or checklist, rather than the configured tracker. `implement` now fetches a passed reference from the issue tracker and states its title before starting, and asks when the reference is ambiguous. Check that title matches the ticket you meant; passing the issue URL or `owner/repo#2` removes the ambiguity entirely.

## It's working if

- The session opens by reading the ticket or spec and restating what it will build, rather than asking you what to build.
- You can see an actual `tdd` Skill tool call in the trace, not just tests appearing in the diff.
- Each behavior starts from a small contract, and the checks match that contract without speculative types or automatic generated testing.
- Typechecks and single test files run repeatedly during the run, and the full suite runs once near the end.
- The review names the candidate commit, and repair commits receive affected checks and focused re-review.
- Unresolved blockers are reported with a checkpoint instead of disappearing behind a completion claim.
- The diff is one ticket's worth of change: a vertical slice through every layer, not several tickets swept together.

## Where it fits

`implement` is the build step of the main chain:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review → retro
```

Its neighbours are [to-tickets](to-tickets.md), which produces the tickets it consumes and declares the blocking edges that decide their order; [tdd](tdd.md), which it drives internally at each seam; and [code-review](code-review.md), which it runs against checkpoint commits and uses to verify repairs. It sits downstream of the planning skills and trusts them. It does not re-validate the shape of what it was handed, so a badly-structured map or a horizontally-layered ticket gets built as written.

That trust is why [wayfinder](wayfinder.md) merges onto the chain at [to-spec](to-spec.md) rather than looping its map straight into `implement`. Go straight to `implement` from a map only when the effort turned out small.

[ask-matt](ask-matt.md) is the router over the whole set when you are not sure which flow you are in.
