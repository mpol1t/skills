---
name: to-spec
description: "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed."
disable-model-invocation: true
---

Load model-invoked dependencies through the harness's skill loader. If no loader is exposed, resolve their installed `SKILL.md` paths from the available skill catalog and read those entry points, preserving invocation policy. Report unavailable dependencies instead of guessing an installation directory or using this repository's human-facing docs as instructions.


This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

Stay within the requested artifact stage. A request to draft or iterate produces a draft, without publishing or applying a ready label. Agreement on a design or spec does not authorize implementation; finish by handing back the spec.

The issue tracker and triage label vocabulary should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. For changed domain behavior, call the Skill tool with "codebase-design" to express the agreed functional contracts and type decisions. If that dependency is unavailable, identify it rather than silently claiming its guidance was applied. Record settled decisions and flag unresolved obligations instead of inventing guarantees.

Sketch the smallest useful set of seams covering the feature's contracts and failure modes. Prefer existing interfaces. Stable pure-domain interfaces can carry laws and example-based unit tests; integration seams cover effects and orchestration. Keep seams that provide distinct evidence. Choose tests by behavior and risk, keeping trivial behavior simple.

Check new or changed seams with the user; carry forward existing agreements without asking again.

3. Write the spec using the template below. For consequential specs with uncertain contracts or substantial failure risks, call the Skill tool with "codebase-design" and use its adversarial-review guidance to challenge the draft against the agreed conversation and source decisions. Ask independent reviewers to find omitted guarantees, contradictions, unsupported assumptions, and verification gaps. Correct synthesis errors; record unresolved choices rather than reopening the interview or inventing agreement. A material unresolved obligation prevents an agent-ready publication; return the draft and identify what remains unsettled.

4. Return or publish the spec. For a draft request or a material unresolved obligation, return the draft for iteration. Otherwise publish it to the configured project issue tracker and apply the `ready-for-agent` triage label, with no additional triage. Neither branch starts implementation.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions
- Admitted inputs, legal states and transitions, expected failures, and effect ownership for changed domain behavior
- Relevant invariants, how types or runtime validation enforce them, and remaining assumptions or justified partiality

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: inline a concise type, state-machine, reducer, or schema sketch when it records an agreed contract more precisely than prose. Note prototype provenance where applicable. Keep only the decision-rich parts, not a working demo.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)
- Agreed seams and the distinct failure modes each covers
- Relevant laws and preconditions, with the rationale for examples, properties, integration checks, or existing adequate coverage; omit generated testing where it adds no useful evidence
- Which guarantees are compiler-enforced, runtime-enforced, tested, or assumed

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
