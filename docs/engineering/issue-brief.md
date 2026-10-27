## What it does

`issue-brief` makes an implementation Issue understandable to a fresh worker: what outcome it owns, what must hold for acceptance, which constraints apply, and what it depends on. It supplies the shared information contract for composing and interpreting briefs; the calling workflow keeps responsibility for sizing, publication, labels, implementation, scheduling, and acceptance.

It works with existing Issue bodies and designated triage comments. A complete older Issue can keep its layout. Useful information and clear authority matter more than exact heading names.

## When to reach for it

Type `/issue-brief`, or the agent reaches for it automatically when a task fits. [to-tickets](to-tickets.md) and [triage](triage.md) use it during implementation Issue authoring; [implement](implement.md) and [implement-spec](implement-spec.md) use it during Issue intake.

| Your situation | Where it fits |
| --- | --- |
| Drafting an implementation Issue from agreed context | Compose a brief with explicit outcome and acceptance criteria |
| Starting from an existing implementation Issue | Identify the authoritative requirements, essential context, and prerequisites |
| Writing a parent specification | Use [to-spec](to-spec.md) |
| Handling a raw incoming report | Use [triage](triage.md), which owns that workflow |
| Writing a decision question or PR body | Keep that artifact's own format; this is implementation guidance |

## A brief, not an execution log

The default starts with **Outcome** and **Acceptance criteria**. **Constraints and scope**, **Verification**, and **Context and dependencies** follow where useful. A small bug needs its trigger and observed versus expected behavior, without empty sections or an invented cause. A refactor can state a structural goal and behavior to preserve without inventing a user-visible change.

Acceptance criteria describe success. Verification explains how to assess it when the method matters. Prior observations record what happened already; they do not establish that a later candidate passed. Preservation criteria can hold before implementation. Agreed contracts, examples, and justified example-only checking choices survive the handoff.

Verified paths and symbols are optional navigation hints unless their identity is explicitly required. A stale hint can be resolved through repository exploration. Each slice carries the inherited constraints it needs and names any later Issue or integration step responsible for a deferred guarantee. Runtime assignments, commits, and check logs stay in the existing handoffs and orchestration ledger.

## Authority and prerequisites

A clearly designated triage brief is the contract; the original report and superseded discussion remain context. Otherwise the Issue body or explicitly supplied agreed requirements provide authority. An arbitrary later comment does not silently replace the contract. Competing briefs and material conflicts require resolution before affected work continues.

Native blocking relationships supply prerequisites where supported. Local files and trackers without native blocking use explicit references. Parentage alone does not create a dependency, and an empty body-level blocker list does not prove independence. Non-obvious dependency rationale travels with the handoff even when native edges make a duplicate list unnecessary.

A question is material when its answer changes outcome, scope, compatibility, or acceptance. Such questions leave authored work in draft by default. Explicit publication of unfinished planning work retains that status. Missing essential references or unavailable dependency information stay visible as gaps; ordinary repository facts are explored and implementation choices remain with the implementer.

## Common questions

**Is this another command I must run between planning and implementation?**

No. It is model-invoked shared guidance loaded by the existing authoring and intake skills. You can use it directly to compose or interpret a brief, but the human workflow gains no required step. That is why the README lists it under Model-invoked while its workflow callers remain User-invoked.

**Does a ready Issue mean an agent can start immediately?**

No. Specification readiness, dependency satisfaction, and authorization are separate. A complete brief can still be blocked. A ready label, closed prerequisite, or checked acceptance box does not replace applicable integration checks or required manual evidence.

## It's working if

- A fresh worker can state this slice's outcome and acceptance conditions without reconstructing the planning conversation.
- The worker and reviewer use the same authoritative brief and applicable parent constraints.
- Small Issues stay compact, while material unanswered questions remain visible.
- Older complete Issues are consumed without a formatting rewrite.
- Prerequisites stored outside the body still appear in the handoff, and future slices' deliverables stay outside the current review scope.

## Where it fits

`issue-brief` is a shared model-invoked layer underneath authoring and intake. [to-tickets](to-tickets.md) uses it to preserve agreed requirements in each slice; [implement](implement.md) uses it to recover those requirements before building. It neither replaces parent specs nor introduces mandatory triage. [ask-matt](ask-matt.md) maps the surrounding flows.
