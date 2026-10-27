---
name: to-tickets
description: Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker).
disable-model-invocation: true
---

Load model-invoked dependencies through the harness's skill loader. If no loader is exposed, resolve their installed `SKILL.md` paths from the available skill catalog and read those entry points, preserving invocation policy. Report unavailable dependencies instead of guessing an installation directory or using this repository's human-facing docs as instructions.


# To Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

The issue tracker and triage label vocabulary should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Call the Skill tool with "issue-brief" to compose the implementation briefs. Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first
- Carry applicable domain contracts, assumptions, and agreed test seams into each slice. Include legal inputs/transitions, invariants, expected failures, and verification choices where relevant. Read referenced decisions before carrying them forward; a fresh implementer must not need the prior conversation. Mark missing agreements as unresolved rather than inventing them.
- Keep type design within the behavior it supports. A separate shared-contract slice is justified only when it genuinely blocks other behavior slices.

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers is eligible for implementation once its requirements are settled and implementation is authorized. Derive edges from acceptance criteria as well as data and types: a shared mechanism, foundation, or interface another ticket introduces is a prerequisite. A prerequisite releases its dependants after review, integration, and the agreed verification, not merely after implementation. For intentionally non-green intermediate migration slices, state the permitted intermediate failures and the final verification gate explicitly.

For each proposed parallel group, check that its shared dependencies will be integrated before the group starts and its contracts permit independent work. Different files or domain labels do not establish independence. Order shared foundations and unsettled contracts first; keep naturally independent slices parallel. Check for missing blockers and cycles.

For consequential breakdowns, call the Skill tool with "codebase-design" and use its adversarial-review guidance before the user quiz. Give independent reviewers the source requirements and draft graph to challenge missing behavior, hidden blockers, shared-contract conflicts, and unnecessary slicing. Resolve supported objections and preserve unresolved choices for the user; the cohort does not approve the breakdown on their behalf.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown.

### 5. Publish the tickets to the configured tracker

Before publication, apply the material-gap check from "issue-brief". Return drafts with unresolved material questions by default. If the user explicitly requests unfinished planning publication, retain an unfinished status rather than labeling it ready-for-agent. Approval of a breakdown does not settle missing requirements or authorize implementation.

Publish the approved, sufficiently specified tickets. **How** depends on the tracker `/setup-matt-pocock-skills` configured; the tickets are the same either way, only the shape of the blocking edges changes:

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file's "Blocked by" lists the numbers/titles it depends on. Use the shared brief inside the local wrapper below: one ticket per file, never a single combined file.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the shared brief as the body. Use the platform's native blocking relationship where it has one; otherwise set each ticket's "Blocked by" to the blocking issues. If the source was an existing issue, make each ticket its sub-issue (tracker doc's operation). Apply the `ready-for-agent` triage label to sufficiently specified tickets unless instructed otherwise; dependency satisfaction remains separate.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

Do NOT close or modify any parent issue.

## Publication wrappers

The shared brief comes from "issue-brief"; keep its format and interpretation rules there.

- **Local:** title each file `# <NN>: <Issue title>`, identify its parent/source when applicable, and record its actual status. List explicit blockers by number/title, or None, in Context and dependencies. Then use the shared brief's sections without duplicating that metadata.
- **Tracker:** use the Issue title and shared brief body. Preserve source-parent linkage through the tracker's sub-issue operation. Use explicit parent/source references when needed for retrieval; native blockers replace a duplicate blocker list. Retain consequential dependency rationale.

Concise agreed contract sketches remain part of the brief where useful; keep prototype provenance and decision-rich content rather than a working demo.
