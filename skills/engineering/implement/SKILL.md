---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec, tickets, or agreed conversation.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Read applicable contracts and verification decisions, including referenced parent-spec decisions when the ticket is incomplete. Carry forward agreed seams; resolve missing agreements through "tdd" rather than silently skipping verification.

For changed domain behavior, call the Skill tool with "codebase-design" for functional contracts and type-driven design. If this dependency is unavailable, identify it rather than claiming its guidance was applied. Preserve the contract's invariants, expected failures, and effect ownership within each behavior slice.

Call the Skill tool with "tdd" for incremental verification and rational test selection at pre-agreed seams. Begin each behavior slice with its smallest useful types and signatures, then use compiler feedback and behavioral checks. Preserve justified example-only choices; trivial behavior needs neither generated tests nor a new harness.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Before review, account for the slice's contract obligations and justified assumptions. Resolve temporary holes and unsafe assertions used during development; do not silence contract failures with casts, swallowed errors, or invented fallback values merely to make checks pass.

Once done, call the Skill tool with "code-review" to review the work.

Commit your work to the current branch.
