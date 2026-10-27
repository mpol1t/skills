# Implementation Issue format: implementation specification

Status: user-confirmed specification implemented following separate authorization to add the skill, review it, update docs, and publish a draft PR within the user's fork. The original specification received two rounds of independent challenge.

Evidence: [research report](issue-format-agentic-research.md).

## Problem and intended result

Implementation Issue producers currently use different templates and authority conventions. `to-tickets` can carry unresolved agreements while declaring work ready by construction; triage stores its authoritative brief in a comment. Consumers do not consistently identify that authority or retrieve blockers stored only as native relationships. Existing path prohibitions also conflict with the agreed use of grounded navigation hints.

Introduce one shared format and interpretation owner so a fresh implementer can determine the slice's outcome, obligations, context, and prerequisites without reconstructing a conversation. Keep existing workflow effects and gates in their current owners. The research supports relevant information and explicit uncertainty, not a proven universally optimal heading scheme.

## Scope and ownership

Add the promoted, model-invoked `issue-brief` skill at `skills/engineering/issue-brief/`. Its two uses are composing an implementation brief from supplied context and interpreting an existing implementation Issue. These are prose instructions, not an executable API, parser, schema, or intermediate artifact.

The skill owns the default headings, information semantics, proportionality, authority interpretation, and material-gap checks. It does not decompose work, publish, set labels, dispatch workers, implement, schedule, or decide acceptance. It may inspect available context through existing read-only tools; callers retain tracker transport and workflow decisions. The invocation description must cover implementation Issue authoring and intake, not general public reports, parent-spec authoring, decision tickets, or PR bodies.

All four callers load it explicitly through the harness loader, with the existing installed-catalog fallback. Keep supporting material inside its package, accessed from the installed entry point. Report a missing dependency; do not silently claim it was applied or substitute human-facing docs. Do not invoke user-only skills as dependencies. A caller can apply already-loaded guidance without repeatedly loading it for each worker or minor step.

## Shared information contract

Use this default order for newly authored implementation briefs:

| Heading | Required meaning |
| --- | --- |
| Outcome | Why the work is needed and the intended result. Explicit for every new brief. |
| Acceptance criteria | Observable conditions for this slice to be accepted. Explicit for every new brief; numbered bullets or checkboxes are presentation choices. |
| Constraints and scope | Applicable binding decisions, invariants, compatibility, exclusions, and any permitted intermediate limitations. Include when relevant. |
| Verification | Agreed or consequential checking approach, prerequisites, and any prior observations clearly labeled as such. Include where the method matters or is not obvious. |
| Context and dependencies | Essential references, parent/source identity, useful navigation hints, and prerequisites not already represented by native relationships. Include when relevant. |

Retain titles, identity, category, and tracker metadata where the owning workflow needs them; these are not additional universal body sections. Respect explicit user instructions and repository templates by mapping the same information into equivalent sections. Do not impose duplicate headings or a rewrite on a complete existing Issue. Requirements remain discoverable even when representation differs.

Conditional guidance must stay compact:

- Bugs: describe trigger, observed versus expected behavior, and available reproduction evidence or relevant environment. Do not invent a cause, reproduction, or result.
- Features: state capability, meaningful examples, and material limits.
- Refactors: state the structural goal and preserved behavior; do not invent a change in user-visible behavior.
- Multi-slice work: identify what this slice guarantees, any intentionally deferred guarantee, and the later Issue or agreed integration step responsible for it. Specify intermediate limitations when applicable.

Distinguish binding requirements from suggestions in ordinary prose. Paths and symbols are optional verified navigation hints unless their identity is itself an explicit contract. Recheck stale hints through repository exploration; an obsolete hint alone need not block work if the relevant code is found. Avoid line-number recipes and inventories of discoverable files. Preserve agreed concise contract sketches, examples, laws, seams, and justified example-only verification choices rather than replacing them with generic requests to add tests.

Criteria express success; planned checks describe how to assess it; observed evidence records what happened. A criterion need not fail before implementation when it expresses preservation or an invariant. Checking a box is not integration evidence. Do not copy runtime assignments, worktrees, commits, review rounds, or check logs into a second Issue execution ledger.

## Authority, inheritance, and intake

At existing intake, callers retrieve the referenced Issue and relevant discussion, identify the designated authoritative brief, read essential references, and retrieve native dependency relationships where supported. Absence of a body-level blocker list does not mean independence. In local files or trackers without native blocking, use explicit blocker references. Parentage alone does not establish an execution dependency. Briefly explain a non-obvious prerequisite where its rationale affects sequencing or safe parallel work. Native edges remove the need to duplicate the blocker list, not the need to preserve consequential rationale; carry that rationale into the existing handoff.

Use a clearly designated triage brief as the contract for that Issue; the original body and superseded discussion provide context. Otherwise use the Issue body or explicitly supplied agreed requirements. Do not assume an arbitrary later comment supersedes a designated brief. If competing briefs lack a clear designation, or applicable instructions materially conflict, surface the ambiguity rather than silently merging requirements. Explicit user direction can resolve it. Historical context clearly superseded by a designated brief is not itself an unresolved conflict.

Each new Issue states its own outcome, scope, and acceptance criteria, carrying the specific inherited constraints necessary for its slice. Link broad rationale and shared contracts without copying the parent specification. Consumers read applicable parent decisions, preserve their applicability, and do not import future slices' deliverables into the current review scope.

A question is material when its answer would change outcome, scope, compatibility, or acceptance criteria. Surface it before work depending on the answer. Resolve ordinary repository facts by inspection and leave ordinary implementation choices to the implementer. Inaccessible essential context and unavailable dependency information are reported as gaps; do not silently convert unknown into absent. A relevant nonessential hint may be omitted with no new approval requirement.

Preserve authoritative source identity and applicable requirements in existing worker and review handoffs. Use available Issue/comment identifiers, local paths, or the supplied agreed text; require no new snapshot store or versioning service. A material change discovered during existing work triggers reconciliation before affected work continues, not background polling or automatic edits to tracked requirements.

Specification readiness, dependency satisfaction, and authorization remain different. A fully specified Issue can still be blocked. A ready label, closed prerequisite, or completed checklist does not independently authorize work or replace integration gates. The shared skill identifies gaps; the calling workflow owns resulting action.

## Changes by owner

| Files | Required change and preserved behavior |
| --- | --- |
| `skills/engineering/issue-brief/SKILL.md`, `agents/openai.yaml` | Add the model-invoked owner above. Omit user-only invocation restrictions; include discoverable UI metadata. Keep instructions focused and examples proportional. |
| `skills/engineering/to-tickets/SKILL.md` | Load the shared owner when drafting slices; replace duplicated semantic template rules with delegation plus local/tracker wrappers. Keep approved sizing, vertical slicing, dependency derivation, user quiz, publication transport, native edges, and no-parent-mutation rule. Replace unconditional readiness and path bans. Material unresolved work remains a draft by default; explicit unfinished publication carries its true status. Never label unfinished work ready merely because it passed through this producer. |
| `skills/engineering/triage/SKILL.md`, `AGENT-BRIEF.md` | Use the shared owner for implementation Issue briefs while retaining the authoritative comment wrapper, existing AI disclaimer, category, triage state machine, and existing maintainer interaction. Avoid competing Issue templates or path prohibitions. Keep PR-remediation guidance and examples separate, including remaining work against an existing diff. Preserve quick maintainer state overrides; a label-only override is not proof of semantic completeness for consumers. Normal readiness recommendations must account for material gaps. |
| `skills/engineering/implement/SKILL.md` | At existing Issue intake, load and apply interpretation guidance, retrieve authority/context/relationships, and carry scope into the existing code-review call. Preserve the same-session conversation and direct-spec entry paths without requiring an artificial Issue or new document. Keep TDD, checkpoint, committed-candidate verification, repair, and completion behavior. Missing product decisions cannot be invented by verification guidance. |
| `skills/engineering/implement-spec/SKILL.md` | Apply the owner to Issue intake and existing worker briefs. Preserve authoritative sources, native edges, applicable contracts, verification prerequisites, and deferred obligations. Keep user-owned sizing, local enforcement of discovered safety dependencies, tracked-graph change authority, worktrees, selective communication, ledger recovery, serialized integration, exact-SHA checks, independent review, manual acceptance, and dependency-release gates. Do not require workers to invoke user-only `implement`. |

The `code-review` skill already gives explicitly supplied requirements precedence. Callers must supply the selected authoritative brief and applicable slice scope using that interface. No new review format, review axis, standalone review discovery workflow, or direct `issue-brief` dependency in `code-review` is required by this change. Standalone review behavior remains outside scope.

Keep `to-spec`, public intake, `wayfinder`, and tracker setup operations unchanged. This format does not initiate bulk migration of existing Issues. No Agent Disclosure section is required: PR provenance policy is separate. The unimplemented PR-description specification is a sibling proposal, not a runtime dependency or authorization to implement it.

## Documentation and packaging

- Add `docs/engineering/issue-brief.md`; resync docs for `to-tickets`, `triage`, `implement`, and `implement-spec` following `.agents/writing-docs.md`. Replace claims that production alone guarantees readiness and any advice that every acceptance criterion must initially fail. Explain conditional sections, equivalent legacy formats, and the distinction between readiness and dependency release.
- Update `ask-matt` and its docs to locate the shared owner underneath authoring and intake without adding a human-required chain step. Preserve distinct parent specs and decision work. Replace unconditional claims that all generated Issues are already ready, without adding mandatory triage to the authoring flow.
- Add linked Model-invoked entries to the engineering bucket README and top-level README. Update existing summaries only where behavior descriptions become stale. Add exactly the new promoted skill path to `.claude-plugin/plugin.json`'s skills array. Do not change marketplace, install commands, existing invocation policies, or unrelated membership.
- Include `agents/openai.yaml` for the new skill and check its model-invoked policy matches frontmatter. Run `scripts/link-skills.sh` after adding it. Run `claude plugin validate . --strict` after the manifest change; report unavailable tooling or failure honestly.
- Use repository-relative docs links and no em dashes. Keep general tracked-work vocabulary as Issue; no glossary cleanup or new ADR is required for this bounded change.

## Acceptance and review scenarios

These scenarios guide independent review of the instructions and examples. They do not require a new executable test harness.

| Scenario | Expected behavior |
| --- | --- |
| Tiny bug with clear reproduction | Explicit outcome and criteria; add only useful evidence. No mandatory empty sections or speculative cause. |
| Feature with a settled parent contract | Child carries applicable constraints and its own completion conditions; references broad rationale. Worker and reviewer use the same scope. |
| Behavior-preserving refactor | Structural goal and preservation criteria are clear; no fabricated user-visible before/after change or requirement that every criterion initially fail. |
| Material compatibility question | Return draft with the question; do not label ready or silently decide. Explicit planning publication remains unfinished. |
| Fully specified but blocked slice | Can be semantically ready while execution remains blocked. Preserve native edges even if the body omits them. |
| Native relationship fetch fails | Report unknown prerequisites; no assumption of independence and no dependent dispatch based on incomplete information. |
| Non-obvious native blocker | Preserve the consequential dependency rationale without duplicating the native blocker list; the worker and orchestrator can understand the prerequisite. |
| Parent-child relationship without blocking edge | Do not infer a prerequisite merely from hierarchy. |
| Migration with deferred final guarantee | Current slice's permitted limitations and later integration owner are explicit; reviewers do not demand deferred behavior early. Existing final gates still apply. |
| Body asks for A; designated triage brief supersedes it with B | Use B, retaining A only as historical context. Carry the brief's identity through worker and review handoffs. |
| Two competing designated briefs or conflicting applicable parent contract | Surface material ambiguity for resolution; do not combine incompatible requirements. |
| Complete legacy Issue or repository template | Interpret equivalent content without rewriting, exact-heading rejection, or duplicate sections. |
| Stale optional path hint | Explore and find current location; do not mistake it for a binding edit instruction. Missing essential external contract remains a material gap. |
| Planned check and prior failed reproduction | Preserve their different meanings. Neither is evidence that the eventual candidate passed. |
| Quick triage label override without brief | Preserve maintainer override; later consumers still inspect requirements and identify material gaps. |
| PR remediation through triage | Preserve the existing-diff task, not a fresh implementation Issue assignment. |
| Conversation-only or direct-spec implementation | Existing entry path still works; create no artificial tracked Issue or mandatory wrapper. |
| Missing shared skill dependency | Identify it explicitly; do not claim the shared checks ran or use the human docs as runtime replacement. |

Review in two bounded rounds: first independent assessments of consumer compatibility, producer/invocation integration, and simplicity/requirements fidelity; then targeted review of corrections and any unresolved objections. Record supported findings and dispositions. Structural validation should cover links, invocation metadata, promoted membership, documentation obligations, and removal of conflicting old instructions. Do not broaden into benchmarks, a schema validator, or mandatory new automated tests. This specification's review is not evidence that future skill implementation has passed these checks.

## Delivery boundary

Implement the shared owner and caller changes as one coherent behavior change with corresponding documentation and packaging. The original drafting request authorized no tracker publication, branch push, PR creation, or skill implementation. The subsequent implementation request authorizes committing and pushing this change and opening a draft PR inside `mpol1t/skills`, without an upstream PR or merge. Preserve unrelated work, including the separate unimplemented PR-description drafts.


## Agreed requirements

1. Scope covers implementation Issues and triage's implementation briefs. Public intake, parent specifications, and decision questions retain distinct formats.
2. A fresh agent must be able to identify the intended outcome, boundaries, applicable decisions, and completion conditions without reconstructing the prior conversation. Consistent headings support this goal but are insufficient alone.
3. Use a compact default format with detail proportional to the work. Add reproduction evidence, compatibility constraints, intermediate-state guarantees, and other details when relevant; avoid mandatory filler.
4. Preserve user control over Issue sizing and existing publication, implementation, and orchestration workflows. Resolve readiness inconsistencies explicitly without introducing automatic decomposition, dispatch, or new approval stages.
5. A question prevents implementation readiness when different answers materially change the outcome, scope, compatibility, or acceptance criteria. Record it explicitly. Ordinary implementation choices remain the implementer's responsibility.
6. Identify one authoritative brief per implementation handoff, preserving Issue bodies and designated triage comments as existing surfaces. Surface material conflicts with applicable parent decisions or other instructions instead of silently choosing or combining requirements.
7. Each Issue states its own outcome, boundaries, and acceptance criteria, and carries the specific inherited constraints needed for its slice. Link broader rationale and shared contracts without copying the entire parent spec. Resolve inaccessible essential references before implementation.
8. Acceptance criteria describe success; verification guidance describes how to check it where the method matters or is not obvious. Distinguish prior observations from planned checks and later results. Do not require a detailed test plan for every Issue.
9. Optimize the format for ingestion by `implement` and `implement-spec`, including fresh-worker understanding and orchestration. Consumer compatibility is a primary requirement, not merely presentation consistency.
10. Newly generated Issues use consistent Markdown headings. Consumers accept equivalent information in existing Issues and repository templates without demanding rewrites or exact heading names.
11. Distinguish binding decisions from optional implementation suggestions. Preserve requirements through ingestion and worker handoffs while allowing suggested approaches to change after exploration.
12. Permit verified paths, symbols, and examples as optional navigation hints. Recheck them against current repository state. A path or name is binding only when explicitly required. Avoid line-number instructions and exhaustive file inventories.
13. Distinguish prerequisites from parentage. Identify actual prerequisites using native tracker relationships where available and explicit references otherwise; explain non-obvious dependencies briefly. Preserve existing integration and verification gates.
14. When a slice defers a guarantee to later integration, state its own completion conditions and where the deferred guarantee will be established. Include relevant permitted intermediate limitations without repeating the delivery plan.
15. Keep runtime details in existing handoffs and the orchestration ledger. The Issue states work and completion conditions; it is not a second execution log. Checked acceptance boxes do not establish successful integration.
16. Default headings are Outcome, Acceptance criteria, Constraints and scope, Verification, and Context and dependencies. Outcome and acceptance criteria are explicit. Other sections appear only when useful; do not duplicate native tracker relationships.
17. During existing intake, `implement` and `implement-spec` check essential information for completeness and consistency. Explore ordinary repository facts; surface material ambiguity or conflicts before dependent work. Add no approval stage or exact-heading rejection.
18. Return a draft identifying material unresolved requirements by default. Explicit requests to publish unfinished planning work retain its unfinished status and do not authorize implementation.
19. Introduce a small model-invoked skill owning the shared Issue format and interpretation rules. `to-tickets`, `triage`, `implement`, and `implement-spec` use it during existing steps. Existing owners retain sizing, publication, labels, implementation, and scheduling.
20. Consumers retrieve the designated authoritative brief, essential references, and native dependency relationships rather than relying only on the body. Preserve their information and authoritative source in existing worker and review handoffs. Report inaccessible essential information rather than assuming absent constraints or blockers.

## Consumer audit

An independent read-only audit of `implement` and `implement-spec` found no mandatory parser or heading schema. Both consume applicable contracts and verification decisions. Orchestrated workers receive the parent spec and slice requirements; review must not count future slices' behavior as missing from the current slice. Dependency release follows integration and applicable verification, not implementation completion or tracker closure. Runtime evidence belongs in the existing orchestration ledger. These existing behaviors constrain the format; they are not newly approved workflow changes.

## Ownership review

Two independent reviewers compared a dedicated model-invoked owner, ownership in `codebase-design`, and deliberate duplication in existing workflows. They used independent contexts; model diversity was not established. A dedicated owner provides one runtime contract but adds a skill and its packaging obligations. Duplication is the smallest initial change but requires coordinated maintenance. `codebase-design` would broaden beyond its existing purpose and conditional invocation would miss some work. User-only producers cannot serve as callable shared owners under the current invocation policy.

Concrete risks identified: matching headings do not resolve authority between bodies and designated triage comments; consumers can miss blockers stored only in native relationships; new guidance can conflict with existing path prohibitions; triage's PR-remediation instructions must remain distinct. Previously agreed draft/readiness rules resolve the publication question raised in the reviews. The user selected a dedicated model-invoked owner, accepting its packaging cost to keep the shared contract consistent. Explicit consumer retrieval and propagation address the authority and native-relationship risks. The implementation specification must replace conflicting operative instructions rather than merely append new guidance.

The shared-owner architecture is settled. No glossary changes are needed.

## Specification challenge record

Three independent reviewers used fresh contexts to assess consumer compatibility, producer/invocation integration, and simplicity/requirements fidelity. Model diversity was not established. The review used the twenty confirmed requirements and current repository instructions, not a vote on preferred designs.

| Finding or challenge | Disposition |
| --- | --- |
| S1: native edges could suppress the reason for a non-obvious prerequisite | Added explicit preservation of consequential dependency rationale in intake and handoffs, plus a review scenario. |
| Producer preservation checks | Made triage's existing AI disclaimer and removal of unconditional router readiness claims explicit. These preserve existing obligations and agreed readiness behavior. |
| Quick readiness override with unresolved compatibility | Targeted consumer challenge found the material-gap rules still apply; the override affects labels, not semantic completeness. |
| Closed prerequisite without required integration/manual evidence | Targeted consumer challenge confirmed required evidence remains necessary where the applicable contract requires it, without adding a ledger or universal new gates to standalone implement. |
| Tiny-Issue proportionality | Already covered by conditional sections and the small-bug scenario; no additional mandatory fields added. |

The first round found no blocking defects. The targeted second round confirmed the corrections and counterexamples introduce no remaining material findings. Consumer, producer, and simplicity reviews are complete. This is a review of the specification, not validation of implemented skills. No executable tests, manifest changes, or installation actions were performed during specification drafting.

## Implementation verification

The shared skill and four callers were reviewed independently against this specification and repository invocation rules. Initial findings identified a missing installed-catalog fallback in triage and readiness-check ordering; both were corrected. A separate synthetic intake exercise preserved designated-brief authority, deferred scope, streaming constraints, stale-hint recovery, and unknown native blockers. This is bounded scenario evidence, not a production performance benchmark.

The new skill passes the skill-creator validator. Strict plugin validation was run using the available Claude Code CLI via npx: it reports the same pre-existing root CLAUDE.md warning and missing-icon advisory on both the implementation tree and baseline d95e69c. These warnings are disclosed rather than treated as a passing strict check. No executable test suite was added.

Final complete-change review found no actionable issues across the twenty requirements, workflow gates, documentation, router, promoted membership, links, and local symlinks. Structural validation passed. Independent reviewers used separate contexts; model diversity was not established.
