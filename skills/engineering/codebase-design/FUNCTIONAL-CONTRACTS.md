# Functional contracts

Use this reference when designing domain types, implementing behavior, or reviewing purity, partiality, effects, and invariants. Adapt examples and mechanisms to the project's language; these defaults prescribe no library.

## Specify one behavior at a time

For significant changed behavior in the current slice, identify admitted inputs, outputs, expected rejection cases, state transitions, effects, and the laws that matter. Sketch domain types and function signatures before implementation, then use compiler feedback where available. Separate guarantees enforced by types from runtime validation and behavioral evidence. Implement and verify this slice before extending the model for later work. Keep the explanation and machinery proportionate; a simple operation can need only a signature and a concrete example.

Represent alternatives and valid states explicitly. Validate untrusted values at entry, construct domain values through checked operations, and preserve their invariants through transitions. A type annotation, assertion, cast, or branded primitive alone does not validate external data. Account for the language's enforcement limits. A validated value does not prove an external fact remains true when an effect executes; recheck or enforce that fact at the relevant operation. Prefer the simplest representation that excludes a meaningful invalid state; additional types must earn their cost.

## Purity and functional reasoning

Prefer a pure domain core with explicit inputs and returned values. A pure computation's result depends on those inputs, and evaluating it has no observable side effects. Check ambient time, randomness, configuration, hidden state, and aliases as well as I/O. Dependency injection makes dependencies visible; calling an injected effect still performs an effect.

Default to immutable data. Encapsulated local mutation is acceptable when it improves clarity or measured performance, provided mutable aliases do not escape, caller-owned values remain unchanged, and the operation preserves its observable contract. Record the justification when choosing this exception. Immutable syntax alone is not evidence of purity.

Reason compositionally: state each operation's preconditions, postconditions, and applicable laws, then check that an upstream output satisfies the downstream input contract. Use substitution of equal values to examine a pure expression. Reordering, retrying, caching, or parallelizing computations requires the relevant laws and effect constraints; do not infer those freedoms from function syntax.

## Totality and failure

Default domain operations to total functions: each admitted input terminates with a defined result. Express expected rejection as an explicit outcome, or narrow inputs through validated constructors. Cover empty collections, missing values, illegal transitions, arithmetic limits, and malformed inputs where relevant. Exhaustive alternatives help account for cases; they do not prove termination or validate inputs.

At raw-input interfaces, represent expected validation failure in the returned outcome. A broad input type plus a comment describing valid values does not establish an enforced narrower domain. Throwing for expected malformed input is a partiality exception requiring an explicit rationale and caller handling; do not describe that interface as total. Separate checked types are optional when a simple returned rejection expresses the contract.

For recursion and loops, identify the decreasing measure or finite bound where needed. Record remaining partial operations and termination assumptions, with their reason and caller handling. Known divergence in the admitted domain is partiality; an unsupported assertion of termination does not remove it. State guarantees within the runtime's resource assumptions; compiler success and passing tests do not establish universal totality. Intentional long-running processes have lifecycle and cancellation contracts rather than a terminating domain-function contract.

Separate expected domain rejection, operational failure, and programming defects. Keep these distinctions in outcomes and handling without forcing every failure into one generic error. An illegal transition returns the specified rejection or an explicitly agreed no-op; silently ignoring it is not a default.

## Effects

Keep effect execution at explicit seams. Supply time, randomness, and external observations as data when that makes the domain computation independent of their acquisition. Describe intended work as data when it clarifies decisions; define the executor's ordering, failure, state consistency, retry, duplicate execution, and cancellation behavior separately where relevant. Explicitly describing an effect does not make repeating it safe. Use project-native mechanisms without inventing an effect framework.

`tdd` owns the compiler and behavioral feedback loop and choice of examples, properties, and integration checks. When actively selecting or writing tests and `tdd` is not already active, call the Skill tool with "tdd". Reading this design reference alone does not invoke it.
