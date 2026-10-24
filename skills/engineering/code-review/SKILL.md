---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
---

Two-axis review of a committed candidate against a fixed point supplied by the user or calling workflow:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

The issue tracker should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## Process

### 1. Pin the fixed point

Resolve the supplied fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.) and candidate (default `HEAD`) to immutable commit SHAs. If no fixed point was supplied, ask for it. Record both SHAs and the requested review scope before dispatching reviewers.

Capture `git diff <base-sha>...<candidate-sha>` once (three-dot, so the comparison is against the merge-base), plus `git log <base-sha>..<candidate-sha> --oneline`. Both reviewers use those exact endpoints, even if branches move during review.

Validate both commits and a non-empty diff before dispatch. An invalid ref or empty diff is not a passing review. Uncommitted changes are outside this review: identify them and request a checkpoint of the intended changes when they are part of the requested work. Keep unrelated user changes out of that checkpoint.

For a repair or reconciliation re-review, also receive the previous reviewed candidate SHA, prior findings and dispositions, and the original ticket/spec. Capture `git diff <previous-candidate-sha> <candidate-sha>` as a direct comparison of the complete trees, even when rebasing has changed their ancestry. Supply this command alongside the original review baseline. Inspect the complete change and affected behavior, checking resolved findings, removed behavior, and newly introduced defects; account for already accepted integrations separately. Preserve earlier review coverage; expand to the full candidate when the change makes that coverage unreliable.

### 2. Identify the spec source

Use the explicitly supplied ticket/spec and review scope first. For a ticket review, parent contracts apply but future tickets' behavior is not missing functionality in this slice. Otherwise look for the originating spec in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.), fetched via the workflow in the tracker doc.
2. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
3. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Search the repo for every file that documents how code should be written. When `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists, it must be on the list.

When the diff changes domain types, functions, state transitions, or their tests, call the Skill tool with "codebase-design" for functional and type-contract guidance. That skill must be available for this branch, including when skills are installed individually. Carry the applicable guidance and its source into the Standards brief. Review admitted inputs, totality assumptions, expected errors, invariant enforcement, composition, and observable effects against the changed contract. Judge encapsulated mutation by its observable contract and justification. Match verification to risk and behaviour; purity alone does not require property tests.

Repository standards override this guidance. In their absence, label functional-design recommendations as judgement calls and cite the contract and hunk concerned. Distinguish compiler enforcement, runtime checks, testing evidence, and assumptions; passing checks are not proof of every domain guarantee.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: an adapted set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: logic depends on another module's private representation. → colocate the operation with that knowledge or expose a cohesive function interface. Pure transformations over explicit domain data are not a smell merely because the data lives elsewhere.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same domain decision is duplicated across the change. → centralize that decision when it must evolve together. Exhaustive matches implementing distinct operations over a sum type can remain separate; choose polymorphism only when it improves the contract.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: navigation exposes representation the caller should not depend on. → hide that knowledge behind a function or module interface. A composition pipeline is not a smell solely because it chains operations.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Spawn both sub-agents in parallel

Issue both sub-agent calls together, in the foreground, and aggregate the reports they return.

Use fresh contexts for independent first assessments. Select expertise and available model capability for each axis; another model can add perspective but does not replace source-grounded review. Supply the artifacts below without the implementer's conversation or the other axis's conclusions. For re-review, include prior findings and the repair scope from step 1.

**Standards sub-agent prompt** should include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full (the sub-agent has no other access to it).
- The applicable functional and type-contract guidance from step 3, with its source and repository-override rule, when that branch applies.
- The brief: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk; and (c) when functional guidance is supplied, concerns supported by the changed contract and hunk, citing that guidance. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline smells and functional-design recommendations are judgement calls unless a documented rule establishes the requirement. Documented repo standards override both. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** should include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Identify findings with stable IDs, location, supporting obligation or labelled judgement call, impact, and evidence. Keep those IDs when checking repairs. Distinguish defects and requirement violations from optional recommendations; an evidence-backed "no actionable findings" is valid. State missing verification or spec coverage explicitly.

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings, because the two axes are deliberately separate (see _Why two axes_).

Record the reviewed base and candidate SHAs and any limited or repair-only scope. End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes: that's the reranking the separation exists to prevent. The calling workflow adjudicates findings and owns acceptance; this report covers only the recorded snapshot and scope.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
