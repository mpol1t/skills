---
name: issue-brief
description: Compose or interpret implementation Issue briefs for authoring and intake. Use when drafting implementation Issues or checking their authoritative requirements, context, and prerequisites before implementation. Public intake, parent-spec authoring, decision questions, and PR bodies have separate formats.
---

# Issue Brief

Make an implementation Issue usable by a fresh worker without reconstructing the conversation. Apply this guidance when composing a brief or interpreting an existing one. The calling workflow owns sizing, publication, labels, implementation, scheduling, and acceptance; this skill supplies the information contract, not those actions.

## Establish the contract

Read the supplied requirements and essential references. At Issue intake, retrieve relevant discussion and native blocking relationships through the configured tracker. Use explicit blocker references for local files or trackers without native blocking. Parentage is context, not a blocking edge. Missing body-level blockers do not establish independence; report inaccessible essential context or unknown prerequisites rather than treating them as absent.

Use a clearly designated triage brief as the Issue's authoritative contract; its superseded body and discussion remain historical context. Otherwise use the Issue body or explicitly supplied agreed requirements. An arbitrary later comment does not automatically supersede a designated brief. Surface competing briefs without a clear designation and material conflicts with applicable parent decisions or other instructions; explicit user direction can resolve them. Clearly superseded history is not a conflict to reopen.

Read applicable parent contracts and carry the specific constraints needed by this slice. Keep its outcome, scope, and acceptance criteria explicit; link broader rationale without copying the parent spec. Future slices' deliverables are not omissions in this slice. For deferred guarantees, identify the later Issue or agreed integration step responsible and any permitted intermediate limitations.

## Compose a brief

Use these headings in order by default. Map the information into equivalent sections when explicit user instructions or a repository template use another layout. Outcome and acceptance criteria are explicit; omit other sections when they add nothing.

| Heading | Content |
| --- | --- |
| Outcome | Problem or purpose and intended result. |
| Acceptance criteria | Observable conditions for accepting this slice. Checkboxes or bullets are both suitable. |
| Constraints and scope | Binding decisions, preservation requirements, compatibility, exclusions, and relevant intermediate limitations. |
| Verification | Agreed or consequential checking approach and prerequisites; clearly labeled prior observations when available. |
| Context and dependencies | Essential references, parent/source identity, useful navigation hints, and prerequisites not already represented by native relationships. |

Keep workflow-specific title, identity, category, and status wrappers with their owner. Native relationships remove duplicate blocker lists, not consequential rationale: briefly explain non-obvious prerequisites when the reason affects sequencing or safe parallel work, and preserve that reason in handoffs.

Tailor detail to the work:

- **Bug:** trigger, observed and expected behavior, available reproduction evidence, and relevant conditions. Identify missing evidence instead of inventing it.
- **Feature:** intended capability, meaningful examples, and material limits.
- **Refactor:** structural goal and required behavior preservation, without inventing a change in user-visible behavior.

Distinguish binding requirements from optional implementation suggestions. Verified paths, symbols, and examples can guide navigation; recheck them against the current repository. A name or path is binding only when its identity is an explicit requirement. Prefer behavioral contracts over line-number recipes and exhaustive file inventories. Retain concise agreed type/state/schema sketches and prototype provenance where they convey a decision.

Acceptance criteria state what must hold; verification guidance states how to check it. Preserve agreed examples, properties, seams, invariants, expected failures, effect ownership, and justified example-only choices where applicable. Add guidance when the method matters or is not obvious, rather than prescribing a detailed test plan for every Issue. Preservation criteria may already hold before implementation. Label prior reproduction observations separately from planned checks; neither establishes that a future candidate passed.

## Interpret and hand off

Accept equivalent information in legacy Issues and repository templates without rewriting them or requiring exact headings. Check essential information for consistency and completeness during existing intake. Resolve ordinary repository facts through exploration and leave ordinary implementation choices to the implementer. An obsolete optional hint need not block work if the relevant code is found.

A question is material when its answer changes outcome, scope, compatibility, or acceptance criteria. Identify such questions before dependent work proceeds. During authoring, return a draft with the open questions by default; an explicit request to publish unfinished planning work retains its unfinished status and does not authorize implementation. A ready label does not settle missing requirements.

Specification readiness, dependency satisfaction, and authorization are distinct. A fully specified Issue can still be blocked. Tracker closure and checked acceptance boxes do not replace applicable integration checks or required manual evidence. Keep existing workflow gates and runtime evidence in their current owners; do not add a second execution ledger.

Carry the authoritative source identity, applicable constraints, prerequisite information and rationale, verification choices, and deferred obligations into existing worker and review handoffs. Use available Issue/comment identifiers, local paths, or supplied agreed text; no new snapshot store is needed. Reconcile material changes discovered during existing work before affected work continues, without background polling or automatically editing tracked requirements. Reuse already-loaded guidance where applicable.
