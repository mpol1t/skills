---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration or property-based tests.
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle: consult them before and during the loop, not after.

When exploring the codebase, read `GLOSSARY.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

Choose tests for the evidence they add. Unit versus integration describes scope; examples versus properties describes test style. These are independent choices: a public pure function may have example-based unit tests, property-based unit tests, or both. Use focused examples for concrete scenarios and simple functions. Consider properties for meaningful laws across varied inputs, and integration tests for effects and collaboration. Existing adequate coverage can make another test unnecessary; state that judgment. Trivial behavior needs neither generators nor a new harness merely to satisfy the loop.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines. When selecting, writing, or debugging properties, generators, or state-machine tests, read [properties.md](properties.md) before proceeding.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, identify seams already agreed in the conversation or spec. Reuse that agreement; propose and confirm only new or changed seams. No test is written at an unconfirmed seam. You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Give each proposed seam a one-line note on what it catches and what it misses. Select stable pure-domain interfaces and integration interfaces where they cover distinct risks; the highest seam is not automatically the only useful one. Preserve useful domain coverage when adding integration tests.

When shaping an interface or its domain types, purity, totality, or effect contract, call the Skill tool with "codebase-design". It owns these contracts and the shared module and seam vocabulary; consult it as a reference, not a session to run. Reuse guidance already loaded and return to this loop instead of recursively invoking references.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Uninformative oracle**: deriving an assertion from the actual result without an independent constraint passes by construction. Copying the implementation into the expected-value calculation risks sharing its mistakes. Justify expectations through worked examples, domain laws, or a simpler independent reference model.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Types within the slice.** Establish the smallest useful domain types and function signature before the body. Use compiler feedback for the type contract and examples or properties for behavior. Preserve obligations from the spec, including justified example-only choices. Avoid speculative type hierarchies and casts or fallback values that merely silence a contract failure.
- **Red before green.** Observe the chosen example or property fail for the intended missing behavior before implementing it. A compile-time rejection check can verify a type contract; successful typechecking alone does not establish behavioral correctness. Add only enough code for the current slice.
- **One slice at a time.** One behavior at an agreed seam, one example or property, one minimal implementation per cycle. A property can exercise many generated inputs within that slice.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.
