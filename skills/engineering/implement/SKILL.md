---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Load model-invoked dependencies through the harness's skill loader. If no loader is exposed, resolve their installed `SKILL.md` paths from the available skill catalog and read those entry points, preserving invocation policy. Report unavailable dependencies instead of guessing an installation directory or using this repository's human-facing docs as instructions.


Implement the work described by the user in the spec, tickets, or agreed conversation.

If the user passes an Issue reference, call the Skill tool with "issue-brief" during intake. Retrieve its authoritative brief, relevant discussion, essential references, and native blocking relationships through the configured tracker; state its title. If the reference is ambiguous, ask. Apply the shared interpretation and material-gap checks before dependent work, including any applicable prerequisite evidence. Preserve authoritative source identity and slice scope for review. For direct specs or agreed conversation, keep the existing entry path without creating an artificial Issue or wrapper.

Record the starting commit as the review base before editing. Preserve pre-existing user changes; include only those belonging to the requested work in the implementation checkpoint.

Read applicable contracts and verification decisions, including referenced parent-spec decisions when the ticket is incomplete. Carry forward agreed seams; resolve missing agreements through "tdd" rather than silently skipping verification.

For changed domain behavior, call the Skill tool with "codebase-design" for functional contracts and type-driven design. If this dependency is unavailable, identify it rather than claiming its guidance was applied. Preserve the contract's invariants, expected failures, and effect ownership within each behavior slice.

Call the Skill tool with "tdd" for incremental verification and rational test selection at pre-agreed seams. Begin each behavior slice with its smallest useful types and signatures, then use compiler feedback and behavioral checks. Preserve justified example-only choices; trivial behavior needs neither generated tests nor a new harness.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Before review, account for the slice's contract obligations and justified assumptions. Resolve temporary holes and unsafe assertions used during development; do not silence contract failures with casts, swallowed errors, or invented fallback values merely to make checks pass.

Commit the implementation to the current branch before review, so the review includes the work. Record that candidate SHA and verify the committed tree itself, using an isolated checkout when excluded working changes could influence checks. Bind verification evidence to that SHA and report any required local fixtures. Then call the Skill tool with "code-review", supplying the base SHA, candidate SHA, and the authoritative brief or agreed requirements, source identity, applicable parent constraints, and slice scope. Review the committed candidate with fresh reviewers rather than passing along the implementation conversation.

Resolve supported findings: fix defects and requirement violations, or record an evidence-backed disposition for disputed findings and optional recommendations. Commit repairs, verify the new committed tree with affected checks, and call the Skill tool with "code-review" again with the original review base, previous reviewed SHA, new candidate SHA, and prior findings for the repair diff and affected behavior. Expand the review when a repair changes the design or scope. Continue while rounds resolve substantive findings; repeated disagreement or lack of progress calls for investigation or a user decision, with the current commits and unresolved findings preserved.

Finish when the accepted candidate meets the agreed requirements, applicable checks pass, and blocking findings are resolved. Report the accepted SHA, verification, and any remaining assumptions or non-blocking recommendations. Missing review or verification is an explicit limitation, not a passing result.
