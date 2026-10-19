# Property-based testing

Use properties when a meaningful law over varied inputs adds evidence beyond a few examples. Keep the simplest effective test for the contract. Follow the test-selection and seam rules in [SKILL.md](SKILL.md); generated inputs do not change the scope of a test.

## Specify the claim

State the input domain, preconditions, and independently justified relationship before choosing generators. Candidate properties include preservation of domain invariants, round trips, idempotence, metamorphic relationships, and agreement with a simpler reference model. Use only laws that hold for the actual domain, including its equality and numeric semantics.

Check that plausible incorrect implementations would fail. Sorting idempotence alone permits a function that always returns an empty list; preservation of elements and ordering supply missing constraints. Two mutually incorrect encoder/decoder functions can satisfy a round trip, so add independently known examples where compatibility matters. A reference model should be simpler or independently derived, rather than a copy of the production algorithm.

## Generate and shrink meaningful cases

- Construct valid domain values directly when practical. Cover meaningful partitions and boundaries, including empty or singleton values where admitted. Inspect representative inputs and the frequency of important cases.
- Generate invalid raw inputs separately at validation interfaces and check their rejection contract. Test a restricted domain function with values its contract admits; casting invalid values into a branded type bypasses that contract.
- Preserve the property's preconditions during shrinking. Check discarded cases and vacuous implications: a green result that rarely exercises the claim provides little evidence. Prefer constructive generation when filtering wastes the budget.
- For stateful behavior, consider command sequences with a simpler independent model, legal-command preconditions, and assertions after transitions. Cover invalid-command rejection when it belongs to the interface. Reset state between runs. Sequential properties do not establish concurrent correctness; use relevant scheduling or integration evidence when interleavings are the failure mode.

## Run, replay, and retain

Use the repository's testing framework and bound the run count, input size, sequence length, and execution time to keep feedback useful. Broader exploration can have a separate budget. A fixed seed repeats the same exploration; it is not a substitute for meaningful coverage. Log replay information for varying-seed runs.

Observe a new property fail for the intended missing behavior. On failure, retain the minimized input or action sequence, seed and other tool-specific replay details, tool version, and invocation. Replay against the defective implementation and observe the same contract violation before changing it. Shrinking must retain the input feature that triggers that failure, not merely any failure. Report a useful minimized repro without claiming global minimality.

Keep significant counterexamples as readable regression examples so generator or library changes do not erase them. After a fix, rerun both the regression example and the relevant broader property.

Passing generated tests is sampled evidence, not proof of correctness, purity, or termination. Test the observable contract defined using `codebase-design`: for an encapsulated mutable implementation, check relevant input preservation and aliasing promises rather than asserting an internal implementation strategy. Integration tests supply distinct evidence for effects, serialization, and collaboration.
