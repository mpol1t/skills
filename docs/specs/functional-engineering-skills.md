# Functional engineering skills specification

Status: Implemented on the local `functional-engineering-skills` branch following the user's explicit `implement-spec` authorization. See the [validation record](functional-engineering-validation.md). The operating rules, skill responsibilities, and evaluation scenarios below define this implementation; language and library choices remain project-specific.

## Problem Statement

This fork should guide agents toward the user's functional programming workflow: purity, total domain functions, type-driven development, explicit invariants, and functional reasoning. The current engineering flow has useful foundations, including returned results, injected dependencies, tests through interfaces, and pure logic prototypes, but those foundations do not yet form a consistent discipline.

Some existing instructions pull in a different direction. Test planning favors the highest possible seam; deepening guidance can discard smaller tests without checking the evidence they provide; review heuristics prescribe object-oriented remedies; and implementation requests typechecking without first designing domain types and function contracts. Property testing appears in debugging but lacks a complete workflow for choosing laws, generating meaningful inputs, and retaining reproducible failures.

Adding generic instructions to prefer functional programming would leave these conflicts active. The goal is observable improvements in agent decisions across design, specification, implementation, testing, and review, with proportionate effort for simple work.

## Solution

Make the agreed functional engineering principles consistent across the existing skills. Give shared guidance clear ownership, carry relevant contracts through handoffs, and replace conflicting defaults. Evaluate the results using individual skill scenarios and complete workflow handoffs.

Agents should explain significant choices through the domain contract and the evidence needed to trust it. They should select familiar, project-appropriate mechanisms and avoid unnecessary type machinery, abstractions, or testing infrastructure. The core guidance remains language-neutral.

## User Stories

1. As a developer, I want pure domain behavior separated from effects, so that I can reason about calculations and transitions from explicit inputs.
2. As a developer, I want hidden dependencies identified, so that time, randomness, configuration, and shared state do not silently change an operation's meaning.
3. As a developer, I want total domain functions by default, so that every admitted input has a defined outcome.
4. As a developer, I want justified partiality and termination assumptions stated, so that the remaining obligations are visible.
5. As a developer, I want types and signatures designed within each behavior slice, so that the compiler helps guide implementation without an upfront type-design phase.
6. As a developer, I want invalid states excluded where practical, so that callers have fewer obligations to remember.
7. As a developer, I want static guarantees distinguished from runtime validation and assumptions, so that typechecking is not mistaken for complete correctness.
8. As a developer, I want expected failures represented explicitly, so that callers can handle domain outcomes deliberately.
9. As a developer, I want immutable data by default and justified private mutation, so that reasoning remains simple without excluding useful implementations.
10. As a developer, I want relevant laws and invariants identified, so that tests exercise the meaning of an operation.
11. As a developer, I want rational test selection, so that examples, properties, and integration checks are chosen for useful evidence.
12. As a developer, I want trivial behavior to receive proportionate verification, so that a simple function does not trigger an elaborate test harness.
13. As a developer, I want property failures minimized and reproducible, so that they become understandable regressions.
14. As a developer, I want tests at stable pure-domain interfaces alongside integration coverage, so that each important failure mode has an appropriate observation point.
15. As a developer, I want architectural changes to preserve distinct contract coverage, so that consolidating modules does not erase useful laws or tests.
16. As a developer, I want reviews to recognize sound functional designs, so that pure transformations and exhaustive matches are not rejected for lacking objects or polymorphism.
17. As a developer, I want specs and implementation Issues to preserve contracts and agreed seams, so that a fresh agent can continue without reconstructing the conversation.
18. As a maintainer, I want shared guidance to have clear ownership and reliable references, so that independent skills follow consistent rules.
19. As a maintainer, I want human docs and routing to match changed behavior, so that I can find and understand the right skill.
20. As the owner of this fork, I want specialist review and explicit implementation authorization, so that refining a specification does not silently change the skill set.

## Implementation Decisions

### Confirmed requirements

The following decisions were explicitly accepted during the design discussion.

1. **Language-neutral core.** Use project-native language features and conventions. Choose language-specific examples and libraries only when project context warrants them.
2. **Purity and functional reasoning.** Favor pure domain logic, explicit effects and errors, and operations whose behavior can be understood from their inputs and contracts.
3. **Total domain functions by default.** Every admitted input terminates with a defined outcome within stated execution assumptions. Expected failure is explicit; justified partiality and termination assumptions are documented. This is an engineering policy, not a claim that ordinary typechecking proves termination.
4. **Incremental type-driven development.** Design the smallest useful domain types and function signatures for one behavior slice, then use compiler feedback and behavioral tests together. Avoid designing the entire type hierarchy before behavioral feedback.
5. **Immutable defaults with encapsulated mutation.** Private mutation is permitted when justified by clarity or measured performance and when it cannot escape, alter caller-owned data, or change the observable contract.
6. **Contracts at appropriate seams.** Preserve properties of stable pure-domain interfaces alongside integration coverage for effects and orchestration. The highest seam is not automatically the only useful one.
7. **Rational testing.** Consider properties for nontrivial domain logic when they add meaningful evidence. Choose example-based unit tests, properties, integration checks, or a combination according to behavior and risk. Trivial behavior does not require generated testing or a new harness.
8. **Specialist collaboration.** Use independent functional-design, type-driven-development, and property-testing perspectives to challenge omissions and conflicting rules.
9. **Separate specification from implementation.** Agreement on principles or a draft authorizes further specification work. Skill edits require an explicit implementation instruction.

### Operating rules

These rules elaborate the confirmed requirements and were included in the specification the user authorized for implementation.

**Functional contracts.** For a significant changed operation, identify its admitted input domain, outputs and expected failures, relevant invariants or transitions, and observable effects. State enough to reason about composition without reconstructing hidden history. An upstream output must satisfy the downstream input contract. Reordering, caching, retrying, or parallelizing computations requires the relevant laws and effect constraints. Keep the explanation proportionate to the operation.

**Purity and totality are separate.** Audit hidden time, randomness, ambient configuration, and mutation through shared references. Dependency injection alone does not make a computation pure. Examine partial operations such as unchecked access, parsing, unwraps, arithmetic limits, and recursion where relevant. Returning a result value does not by itself rule out exceptions or divergence. Use an enforced narrower input domain or an explicit rejection result when appropriate. At raw-input interfaces, expected validation failure belongs in the returned outcome; throwing requires a stated partiality rationale and caller handling. A broad input type plus a valid-input comment is not an enforced narrower domain. For recursive or iterative operations, examine progress or bounds; known divergence within the admitted domain is partiality, not an assumption that can be waved away. The distinction between coverage of inputs and termination also appears explicitly in the [Idris totality documentation](https://idris2.readthedocs.io/en/latest/tutorial/theorems.html#totality-checking).

**Type guarantees have a scope.** Use alternatives, structured domain values, validated construction, and exhaustive handling when they prevent concrete mistakes. Trace untrusted entry routes such as deserialization and persisted data. Distinguish compiler enforcement, runtime enforcement, tests, reasoning, and assumptions. A locally validated value does not prove an external fact remains true at the point of an effect. Account for the chosen language's limitations; for example, [TypeScript documents deliberate soundness compromises](https://www.typescriptlang.org/docs/handbook/type-compatibility.html#a-note-on-soundness).

**Effects have an execution contract.** Keep expected domain rejection distinguishable from integration failures and programming defects. Describe intended work as data when that improves reasoning, without requiring an effects library. Check ordering, failure handling, and state consistency where the effect is executed. Account for retries, duplicate execution, and cancellation when the operation requires them; describing an effect explicitly does not make repeating it safe.

**Testing has two independent choices.** Unit versus integration describes scope; examples versus properties describes how cases and assertions are expressed. A unit test can use either examples or generated inputs. Prefer the smallest strategy that can catch plausible mistakes. Retain examples for readable scenarios and regressions even when properties are useful. Existing adequate coverage can make an additional test unnecessary.

**Properties need meaningful evidence.** State the law, domain, preconditions, and independent justification before selecting generators. Construct valid domain inputs where practical and test invalid raw inputs at validation interfaces. Check useful distributions, boundary cases, discarded cases, and shrinking that preserves the property's preconditions. Select laws that match the domain's equality and numeric semantics. Confirm that plausible incorrect implementations would violate the assertions. Finite successful runs supply evidence, not a proof of correctness or totality.

**Failures must be reproducible.** Capture useful minimized inputs or action sequences and the replay information required by the chosen tool. Keep significant counterexamples as readable regression cases. Bound routine input sizes, sequence lengths, and execution time; broaden exploration when warranted. A fixed seed is not a substitute for meaningful input coverage.

**Stateful behavior needs appropriate models.** Where sequences matter, consider an independent model, legal command preconditions, and invariants after transitions. Cover illegal commands through an explicit rejection contract. Sequential properties do not establish concurrent correctness; shared state and effects need their own relevant evidence.

**Architecture protects reasoning.** Evaluate abstractions by the domain obligations they encapsulate, effects they isolate, and composition they enable. Small pure functions can be useful modules. One production adapter can justify isolating an effect. Remove smaller tests only when their contract disappears or their useful coverage is demonstrably replaced. Method count alone does not determine test effort.

**Review remains contextual.** Diagnose duplicated domain decisions and inconsistent variant handling without automatically moving behavior onto objects or replacing matches with polymorphism. Respect documented project constraints. Distinguish a broken contract from a design preference. Do not demand property tests solely because a function is pure.

### Skill responsibilities

Prefer existing skill owners over a new catch-all skill. Each rule should have one authoritative home; consumers should reach it through the repository's skill invocation conventions.

| Skill or group | Responsibility |
| --- | --- |
| `codebase-design` | Own functional contracts, purity, totality, type-driven design, composition, and effect isolation alongside deep-module guidance. |
| `domain-modeling` | Discover impossible combinations, permitted transitions, invariants, and facts that can become stale. Keep the glossary about domain meanings. |
| `tdd` | Own incremental verification, rational test selection, property technique, and the relationship between compiler feedback and behavioral evidence. |
| `to-spec` and `to-tickets` | Preserve applicable contracts, assumptions, verification decisions, and agreed seams across handoffs. |
| `implement` and `implement-spec` | Consume those obligations per behavior slice and report the relevant checks and remaining assumptions. Recheck affected combined behavior after integration. |
| `code-review` | Review changed functional contracts and revise conflicting object-oriented heuristics while preserving project precedence. |
| `diagnosing-bugs` | Use deliberate properties, reproducible exploration, minimization, and regression cases when the failure calls for them. |
| `improve-codebase-architecture` | Evaluate useful compositions and effect isolation; preserve distinct domain coverage during deepening. |
| `prototype` | Separate pure transition logic from its stateful driver and treat manual exploration as design evidence requiring production verification. |
| `ask-matt` and human docs | Explain the updated responsibilities, testing choices, and routes consistently. |

Supporting references must be reachable when their owning skills are installed. New dependencies must be explicit and must not rely on a full repository checkout being present accidentally. Changes should preserve existing invocation modes unless a separate reason is approved.

## Testing Decisions

### Confirmed validation seams

The user approved validation at both individual skill outputs and the full design-to-review handoff. The behavior under test is the agent's observable decisions and artifacts, rather than the exact prose of an instruction.

- **Individual skill seam:** invoke the relevant skill on a small scenario and inspect its design, test selection, or review findings.
- **Workflow handoff seam:** carry a design through a spec and implementation Issue into a fresh implementation context and review. Inspect whether contracts, assumptions, and agreed seams survive.

Existing repository practice provides useful starting points: interface-level examples in `tdd`, pure reducers in logic prototypes, deterministic repros and minimization in debugging, and separate Standards and Spec review perspectives. The scenario matrix below defines the evaluation plan; execution results are recorded separately.

### Evaluation scenarios

| Scenario | Observable acceptance criterion |
| --- | --- |
| Trivial deterministic transformation | Chooses a focused example-based unit test or explains adequate existing coverage; does not introduce generators or a harness without a useful reason. |
| Domain calculation with meaningful laws | Identifies a justified law and its preconditions, selects useful examples and/or properties, and covers relevant domain boundaries. |
| Nontrivial behavior implemented incrementally | Sketches the smallest useful domain types and signatures before the body, uses compiler feedback and behavioral evidence for that slice, and avoids speculative unrelated types or casts and fallback values added merely to silence contract failures. |
| Empty input to an operation that requires a value | Enforces a restricted domain or specifies an explicit outcome instead of hiding an unchecked access. |
| Recursive or iterative domain operation | Examines a decreasing measure or bound, or states and justifies remaining partiality; does not treat an unsupported termination assertion as a guarantee. |
| Hidden clock, randomness, or shared mutation | Identifies the dependency or effect and avoids calling the computation pure merely because dependencies are injected. |
| Local mutable builder with immutable results | Allows a justified private implementation while checking that aliases and caller-owned data are not observably mutated. |
| Untrusted input entering a typed domain | Validates at the entry interface and distinguishes constructor guarantees from later behavioral invariants. |
| Weak property such as sort idempotence alone | Notices that an always-empty implementation could pass and adds independently justified obligations where the sort contract requires them. |
| Generated failure | Replays a useful minimized repro against the defective implementation and observes the same contract violation, retaining sufficient replay information without claiming global minimality. |
| Legal and illegal state transitions | Preserves invariants for legal transitions and implements the specified rejection behavior for illegal ones. |
| Pure domain logic plus persistence or external effects | Selects domain and integration coverage for distinct risks rather than enforcing one highest seam; covers a relevant operational failure such as duplicate execution when the scenario admits it. |
| Composition with an ordering dependency | Checks that intermediate values meet downstream contracts and rejects an unjustified reorder, cache, or parallel execution that changes observable behavior. |
| Pure functions and exhaustive matches under review | Evaluates correctness and maintainability without demanding methods or polymorphism solely from their shape. |
| Architecture consolidation | Preserves valuable domain laws and removes only tests whose obligations disappeared or are demonstrably covered elsewhere. |
| Fresh-context handoff | The implementer recovers applicable contracts and agreed seams from artifacts; review checks the same obligations. Both a justified example-only choice and a property-testing choice survive without mechanically adding generated tests. |
| Proposed action after design agreement | Produces or refines the specification and waits for explicit implementation authorization before changing skills. |

For each evaluation, record the task, relevant skill version, material project conventions, observed output, and why it passes or fails. Compare representative cases against current behavior where useful. Rerun cases affected by revisions; avoid equating one favorable run with reliable behavior across models or projects. Specialist review should challenge both missed obligations and unnecessary complexity.

### Repository consistency checks for eventual implementation

- Changed promoted skills have synchronized human docs, and the router describes their actual roles.
- References resolve, and shared guidance is reachable through valid skill dependencies.
- Invocation metadata remains consistent between harnesses.
- Promoted-set README and plugin entries remain consistent if membership changes.
- Strict plugin validation runs if either manifest changes.
- Modified prose follows repository conventions, including the prohibition on em dashes.

These structural checks complement behavioral evaluation; they do not establish that an agent follows the guidance.

## Out of Scope

- Inferring implementation authorization merely from agreement during drafting or review; the current implementation has been explicitly requested.
- Selecting a mandatory language, FP library, effect system, or property-testing framework.
- Requiring formal proofs, dependent types, or universal termination guarantees from ordinary application tooling.
- Requiring property tests for every function or replacing useful example-based unit and integration tests.
- Rewriting unrelated productivity skills, changing the promoted skill set, or redesigning the plugin installation system.
- Automatically refactoring consumer projects, creating implementation Issues, or marking work ready for autonomous execution.
- Broad fixes to unrelated commit, review, tracker, or deployment workflows.

## Further Notes

### Implementation scope

The user authorized implementation of this specification after the engineering principles and two validation seams were confirmed. Deliver the skill responsibilities above as one coordinated change, checking missing requirements, contradictions, and disproportionate obligations during review. Language and library choices remain project-specific.

### Publication and implementation status

This specification is local. The repository defines triage labels but has no configured issue tracker. Publication through `to-spec` requires tracker setup or an explicit destination. It has not been published or labeled ready for agent execution. The user's subsequent `implement-spec` instruction separately authorized implementation on a local integration branch.

### Specialist review

Independent specialist agents previously examined functional design, type-driven development, and property testing against the repository. They agreed that conflicting defaults must be corrected along with new guidance. The specification and implementation incorporate their recommendations; no claim of external human review or formal verification is made.

The first draft review clarified termination, added direct evaluation of incremental type design and composition, and strengthened replay and handoff checks. These were specification revisions only. The subsequent implementation and behavioral evaluations are recorded in the [validation report](functional-engineering-validation.md), including a totality ambiguity found during evaluation and the fresh rerun after clarification.
