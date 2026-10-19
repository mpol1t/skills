# Planning handoff report

Produced:

- `spec.md`
- `.scratch/inventory/issues/01-format.md`
- `.scratch/inventory/issues/02-reserve.md`
- `REPORT.md`

Applied the source `codebase-design`, `to-spec`, and `to-tickets` skills and the design skill's `FUNCTIONAL-CONTRACTS.md` reference. The explicit fixture-local tracker and planning-only scope control delivery. No prior repository spec was read, no network publication was performed, and no implementation was written.

Carried forward the approved two-ticket breakdown with no blockers and no repeated approval request. Kept formatting checks deliberately example-only. Preserved separate pure-reservation properties and persistence integration evidence because they establish different guarantees. Included runtime admission rules, native TypeScript limitations, explicit rejection/conflict outcomes, and expected-version CAS at the effect seam. Kept unspecified parsing syntax and existing operational-failure conventions explicit rather than inventing guarantees. No redesign, framework, or shared-contract prerequisite was added.

## Produced specification

# Inventory library specification

## Problem Statement

Callers need predictable quantity text and reservations that preserve valid inventory counts. A reservation must not report success if another writer changes persisted stock before the save.

## Solution

Provide independent formatting and reservation behavior in TypeScript. Keep reservation arithmetic pure and coordinate persistence through the agreed injected store interface, using its existing compare-and-swap (CAS) capability.

## User Stories

1. As a library caller, I want a quantity formatted as a number followed by ` units`, so that display text is consistent.
2. As a library caller, I want `1 units`, so that the specified format has no singular exception.
3. As a library caller, I want zero and the upper bound of 100 supported, so that every admitted quantity can be displayed.
4. As an input consumer, I want untrusted raw quantities validated before domain operations, so that invalid counts never enter the domain.
5. As a reservation caller, I want a successful reservation to subtract the requested quantity, so that remaining stock is accurate.
6. As a reservation caller, I want to reserve all remaining stock, so that zero stock is a valid result.
7. As a reservation caller, I want insufficient stock explicitly rejected, so that I can distinguish rejection from success.
8. As a reservation caller, I want my input preserved, so that computing a reservation cannot alter caller-owned data.
9. As a persistence caller, I want current stock and version loaded through an injected store, so that observations and writes have an explicit seam.
10. As a persistence caller, I want the save conditioned on the observed version, so that a stale observation cannot overwrite a concurrent change.
11. As a persistence caller, I want a CAS conflict returned explicitly, so that a failed save never looks successful.
12. As a persistence caller, I want insufficient stock to avoid a save, so that rejected reservations do not write inventory.

## Implementation Decisions

- Preserve the approved two independent slices: formatting, and reservation including persistence orchestration. Neither blocks the other. No shared-contract prerequisite slice is needed.
- Use TypeScript's native types and the simplest adequate design. Do not introduce frameworks. Define the relevant types and interfaces within each behavior before implementing it.
- `formatQuantity(q)` admits finite integers from 0 through 100 inclusive and returns the decimal quantity followed by the literal ` units`, including for 1. It is a pure, defined operation over that admitted domain.
- `reserve(stock, quantity)` admits stock as a finite integer from 0 through 100 and quantity as a finite integer from 1 through 100. It returns an explicit success containing remaining stock when quantity is at most stock, or an explicit insufficient-stock rejection otherwise.
- Successful remaining stock equals stock minus quantity and lies in 0 through 100. Every admitted input pair has a defined outcome. The pure operation performs no I/O, reads no ambient mutable state, and preserves inputs on either outcome.
- Validate untrusted raw quantities before constructing or passing domain values. Finite, integral, and range checks are runtime obligations; TypeScript number annotations or casts alone cannot enforce them. Raw parsing syntax is not specified by this plan; use existing project conventions and retain the stated numeric admission rules rather than inventing coercions.
- Use explicit native outcome alternatives to distinguish pure success and insufficient stock, and persistence success, insufficient stock, and conflict. Exact existing interface names and representations may be retained. Compile-time outcome checking does not prove numeric invariants.
- The persistence module owns effects: load current stock and version through the injected store, compute `reserve`, and, only for pure success, conditionally save remaining stock with the loaded version as expected version. Report success only after CAS confirms the write. A failed version match returns conflict explicitly.
- The injected store is the existing effect-isolation seam and already supports CAS. Its observation of stock must satisfy the domain contract; validate untrusted stored quantities on entry. CAS enforces consistency at the write because validation of a prior observation cannot establish that it remains current.
- Preserve existing store operational-failure handling; this plan specifies CAS conflict, not a new transport-error contract. Operational errors must never be converted into success. No automatic retry policy is agreed.

## Testing Decisions

- Test caller-visible behavior through the agreed interfaces, without assertions on private helpers or implementation shape.
- Formatting uses example-only unit checks at public `formatQuantity`; representative examples include 0, 1, and 100. This deliberately sufficient choice needs no generated-property machinery.
- Pure reservation uses properties over admitted stock and quantity: when quantity is at most stock, success contains stock minus quantity and is nonnegative; every evaluation preserves inputs. Retain focused rejection examples such as zero stock with quantity 1 and stock 2 with quantity 3, plus exact depletion as a success example.
- Validation evidence must show nonfinite numbers, fractions, and out-of-range values cannot enter the domain, with quantity zero rejected for reservations but accepted for stock and formatting. Use the project's existing validation test conventions; raw string grammar is not newly specified.
- At the persistence module's public service interface, integrate an injected store adapter to verify successful save, insufficient stock with no save, and CAS conflict. Success must exercise use of the loaded expected version. Conflict must demonstrate that a changed version prevents a stale save and yields conflict rather than success.
- Pure tests establish arithmetic and input-preservation evidence. Persistence integration checks establish effect ordering and write consistency. These seams provide distinct evidence and both remain necessary.
- TypeScript checking covers declared input and result shape and outcome handling where exhaustiveness is expressed. Runtime validation covers numeric admission. Properties and examples provide behavioral evidence. The store's existing atomic CAS semantics and normal runtime resources are assumptions; passing tests does not prove universal termination or store correctness.
- No codebase-specific testing prior art was supplied or inspected for this fixture. The implementer should reuse the existing runner and conventions, with no new frameworks.

## Out of Scope

Implementation during this planning invocation; network publication; additional tickets; redesigning approved interfaces; singular grammar; quantities outside the specified ranges; new effect frameworks; retry policy; new operational-error taxonomy; claims of distributed exactly-once execution.

## Further Notes

The local fixture is the configured tracker. The breakdown and seams are already approved and need no further interview. Each ticket includes its own contract so a fresh implementer can begin either independently. No prior repository spec was used.

## Produced Issue 01-format.md

# 01: Format admitted inventory quantities

**What to build:** Library callers can use public `formatQuantity(q)` to obtain the decimal quantity followed by the literal ` units`, including `1 units`.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

**Contract and verification:** Admitted quantities are finite integers from 0 through 100 inclusive. Formatting is pure and defined for every admitted value. Untrusted raw quantities must pass runtime finite, integer, and range validation before entering the domain; a TypeScript annotation or cast is insufficient. Reuse native TypeScript types and existing validation conventions, with the simplest adequate design and no new frameworks. Example-only unit checks at public `formatQuantity` are deliberately sufficient; no property suite is required. Raw parsing syntax is not specified; do not invent coercions. Define types for this behavior before implementation; no shared type ticket or reservation dependency is needed.

- [ ] Public formatting returns `0 units`, `1 units`, and `100 units` for the corresponding admitted inputs.
- [ ] The implementation preserves the contract across the admitted range without side effects.
- [ ] Untrusted input cannot enter the domain as nonfinite, fractional, negative, or greater than 100; reuse and verify existing validation where available.
- [ ] Run example-only formatting checks through the public interface and the existing TypeScript checks.

## Produced Issue 02-reserve.md

# 02: Reserve inventory with conditional persistence

**What to build:** Callers can compute a reservation without effects and persist it through a service that detects concurrent stock changes explicitly.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

**Contract and verification:** Use the pre-agreed pure domain and injected-store seams, native TypeScript types, and simplest adequate design without new frameworks. Define the relevant types before implementing this behavior. `reserve(stock, quantity)` admits finite integer stock from 0 through 100 inclusive and finite integer quantity from 1 through 100 inclusive. For quantity at most stock, return explicit success with remaining stock equal to stock minus quantity. Otherwise return explicit insufficient-stock rejection. Every admitted input pair has a defined outcome; all inputs remain unchanged. The pure module has no I/O or ambient mutable dependencies. Runtime validation must establish numeric admission for untrusted raw quantities, including untrusted store observations; number annotations and casts do not establish this. Raw parsing syntax remains unspecified and should follow existing conventions.

The service owns load and save effects. Load current stock and version from the injected store, call the pure reservation operation, and save only on pure success using the loaded version as expected version in the existing CAS operation. Return success only after that conditional save succeeds. Return explicit conflict when versions do not match, never false success; an insufficient-stock result performs no save. The store already supports atomic CAS, which is an assumed store guarantee. Preserve existing operational-failure handling and do not convert failures into success; new transport-error outcomes and automatic retries are not agreed.

Property tests at public `reserve` cover successful arithmetic, nonnegative remaining stock, and input preservation across admitted inputs. Focused examples cover insufficient-stock rejections. Integration checks at the public service interface with an injected store adapter separately cover successful save, insufficient stock without save, and CAS conflict. Types cover declared shapes and distinguish alternatives; runtime checks establish numeric admission; tests provide behavioral evidence. Neither dependency injection nor types prove purity or write consistency. Reuse existing runner and conventions.

- [ ] Pure success subtracts exactly quantity, including exact depletion to zero, and keeps remaining stock in 0 through 100.
- [ ] Pure insufficient-stock rejection is explicit for cases including stock 0 with quantity 1 and stock 2 with quantity 3.
- [ ] Properties cover arithmetic, nonnegativity, and unchanged inputs, with inputs generated only from the admitted domain.
- [ ] Runtime validation excludes nonfinite, fractional, and out-of-range values before domain entry; stock zero is legal, reservation quantity zero is not.
- [ ] A service integration check loads stock and version and verifies the conditional save of the computed remaining stock using that version, followed by success.
- [ ] A service integration check verifies insufficient stock returns rejection without a save.
- [ ] A service integration check changes the version before save and verifies CAS prevents the stale write and the service returns conflict rather than success.
- [ ] Run relevant behavioral and TypeScript checks without depending on the formatting ticket or introducing a separate shared-contract slice.
