# Final handoff evidence

Skill source revision: `4565d33`. Fresh implementation received the original planning artifacts, not earlier evaluation results. The following report and snapshots are preserved from the fixture, with trailing whitespace normalized.

# Inventory implementation report

Both tickets are implemented. Final strict TypeScript checking passed; all 11 Node tests passed, including a 1,000-run fast-check property.

## Inputs and scope

Requirements were read only from `spec.md` and `.scratch/inventory/issues/01-format.md` and `02-reserve.md`. I explicitly read the current source `tdd/SKILL.md`, `codebase-design/SKILL.md`, and their `tests.md`, `mocking.md`, `properties.md`, and `FUNCTIONAL-CONTRACTS.md` references under `/home/user/projects/skills/skills/engineering`. No planner report, other evaluation directory, or parent specification was read. All writes were confined to this fixture.

The fixture contained specifications but no implementation, runner, glossary, validation convention, or concrete store interface. I used Node's existing built-in test runner and assert, installed TypeScript and fast-check 4.10.2. No installation, network action, publication, or commit occurred. `rg` was unavailable, so local file discovery used `find . -maxdepth 3 -type f`.

## Types before bodies and compiler feedback

Per-behavior type/signature snapshots were captured before implementing their bodies:

- [Formatting declarations](#artifact-1): branded admitted quantity, explicit raw-validation result, public formatter.
- [Reservation declarations](#artifact-10): independent stock/request brands, validation alternatives, success/insufficient-stock alternatives, pure operation.
- [Persistence declarations](#artifact-19): injected load/CAS interface and success/insufficient-stock/conflict alternatives.

These snapshots use throwing placeholders, not claimed working implementations. Strict compiler runs preceded the corresponding behavior implementations. The first compiler run exposed TS5011: an explicit `rootDir` was required. [Original compiler output](#artifact-5) is retained. Setting `rootDir` to `src` fixed it. Successful declaration-stage checks are in `01-types-fixed.log`, `03-types.log`, and `05-types.log`; successful final checking is in `final-types.log`. Empty compiler logs indicate exit zero.

Brands restrict ordinary TypeScript callers, while runtime constructors check type, finiteness, integrality, and range before branding. The remaining-stock brand is justified by validated arithmetic and the insufficient-stock branch. Deliberate casts and untyped JavaScript can bypass TypeScript contracts; callers must validate raw inputs. Types alone do not enforce numeric admission.

## Incremental behavioral evidence

Tests target public interfaces at the already approved seams; no further interview was needed.

| Cycle | Observed red | Implementation and observed green |
| --- | --- | --- |
| Formatting examples | `01-red.log`: formatter throws for admitted zero | Literal quantity plus ` units`; `01-green.log` passes 0, 1, 100 |
| Formatting raw validation | `02-red.log`: temporary unchecked constructor admits NaN | Runtime numeric checks; `02-green.log` passes |
| Reservation raw validation | `03-red.log`: constructor placeholder throws | Independent stock/request admission checks; `03-green.log` passes |
| Pure reservation property | `04-red.log`: missing operation, shrunk to `[0,1]`; replay retained in `04-replay-red.log` | Intermediate rejection-only implementation handles rejection but intentionally remains incomplete for success |
| Pure arithmetic | `04-arithmetic-red.log`: rejection-only operation rejects `[1,1]`; replay retained in `04-arithmetic-replay-red.log` | Conditional rejection and subtraction; `04-green.log` passes property and focused regressions |
| Persistence success | `05-red.log`: orchestration placeholder throws | Load, validate, compute, conditional save; `05-green.log` passes |
| CAS conflict | `06-red.log`: real adapter prevents stale write but orchestration falsely reports success | Inspect CAS confirmation; return explicit conflict on false; `06-green.log` passes |

Each behavioral failure occurred after successful compilation, except the earlier separately recorded compiler configuration correction. The arithmetic property was replayed against the unchanged defective implementation before fixing it. fast-check used seed `20261019`; the missing-operation failure replay used path `0:0`, and the rejection-only failure replay used path `0`, with `endOnFailure: true`. Logs retain shrink details. Focused retained examples cover `[0,1]`, `[2,3]`, `[1,1]`, and `[100,100]`.

The property constructs admitted integer inputs directly, without filtering or discarded cases. For successful outcomes it checks conservation (`remaining + requested == original stock`) and the nonnegative bounded range; for insufficient inputs it checks explicit rejection. This is the independently specified stock-conservation law, not a result-derived oracle. Every evaluation checks unchanged inputs. Inputs are scalar numbers, so preservation is simple; a frozen caller-owned container documents the promise without pretending to test mutable domain objects. The test covers both outcome partitions; fixed rejection/depletion examples make edge coverage explicit.

Formatting deliberately has examples only, with no property machinery. Raw numeric validation uses examples covering NaN, both infinities, fractions, negatives, values above 100, and nonnumeric input without coercion. Zero is accepted for formatting and stock but rejected for requested reservation quantity.

Persistence uses an injected in-memory adapter with actual version comparison and writes. Success exercises loaded version 42 and observes stock 7/version 43 through the store interface. Rejection performs zero saves. A racing adapter writes stock 9/version 43 between observation and CAS; stale save is rejected and stock remains 9. Additional public-interface checks cover invalid observed stock, unchanged propagation of load/save failures, and a deferred CAS proving success awaits confirmation. The insufficient-stock and supplementary checks were already green when added because the typed success implementation and earlier guards necessarily handled them; they are regression evidence, not falsely reported new red cycles.

## Exact verification commands

All commands ran with working directory `/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun`.

```sh
node ../node_modules/typescript/bin/tsc --noEmit > evidence/01-types.log 2>&1
node ../node_modules/typescript/bin/tsc --noEmit > evidence/01-types-fixed.log 2>&1
node ../node_modules/typescript/bin/tsc && node --test test/format.cjs > evidence/01-red.log 2>&1
node ../node_modules/typescript/bin/tsc && node --test test/format.cjs > evidence/01-green.log 2>&1
node --test test/format.cjs > evidence/02-red.log 2>&1
node ../node_modules/typescript/bin/tsc && node --test test/format.cjs > evidence/02-green.log 2>&1
node ../node_modules/typescript/bin/tsc --noEmit > evidence/03-types.log 2>&1
node ../node_modules/typescript/bin/tsc && node --test test/reserve.cjs > evidence/03-red.log 2>&1
node ../node_modules/typescript/bin/tsc && node --test test/reserve.cjs > evidence/03-green.log 2>&1
node --test test/reserve.cjs > evidence/04-red.log 2>&1
node --test test/reserve.cjs > evidence/04-replay-red.log 2>&1
node ../node_modules/typescript/bin/tsc && node --test test/reserve.cjs > evidence/04-arithmetic-red.log 2>&1
node --test test/reserve.cjs > evidence/04-arithmetic-replay-red.log 2>&1
node ../node_modules/typescript/bin/tsc && node --test test/reserve.cjs > evidence/04-green.log 2>&1
node ../node_modules/typescript/bin/tsc --noEmit > evidence/05-types.log 2>&1
node ../node_modules/typescript/bin/tsc && node --test test/persistence.cjs > evidence/05-red.log 2>&1
node ../node_modules/typescript/bin/tsc && node --test test/persistence.cjs > evidence/05-green.log 2>&1
node --test test/persistence.cjs > evidence/06-red.log 2>&1
node ../node_modules/typescript/bin/tsc && node --test test/persistence.cjs > evidence/06-green.log 2>&1
node ../node_modules/typescript/bin/tsc --noEmit > evidence/final-types.log 2>&1
node ../node_modules/typescript/bin/tsc && node --test test/*.cjs > evidence/final-tests.log 2>&1
```

The initial compile-and-test attempt stopped at TS5011 before running tests. The listed `01-red.log` command was rerun after fixing the configuration. Replay runs temporarily added the above path/endOnFailure options to the property, then restored the broader 1,000-run configuration.

## Final files and limits

- [Formatter and validator](#artifact-26)
- [Pure reservation and validators](#artifact-28)
- [Persistence module and store contract](#artifact-27)
- [Formatting examples](#artifact-29)
- [Reservation properties and examples](#artifact-31)
- [Persistence integration checks](#artifact-30)
- [Compiler configuration](#artifact-32)
- [Final test output](#artifact-24)

The pure modules read no ambient mutable state, perform no I/O, and use finite straight-line computation over admitted values. Sampling and compiler success are evidence, not universal proofs. Atomic CAS and ordinary runtime resources remain assumptions. The adapter models the specified CAS guarantee; tests do not establish any production store's atomicity.

Raw-validation interfaces return explicit invalid outcomes. Invalid persisted observations reject the promise with `TypeError`: this is a store-contract violation, deliberately not a new expected reservation outcome. Callers handle rejected promises for operational failures and broken store contracts. Load/save exceptions propagate unchanged. No existing operational-error handling was present to preserve beyond that normal promise convention. No retry is introduced. Store version is an opaque-to-the-module numeric token supplied by the injected interface. No raw string grammar or coercion was invented.

## Independent review

# Independent final review

Scope: finalized `spec.md`, `.scratch/inventory/issues/01-format.md`, `.scratch/inventory/issues/02-reserve.md`, `src/*.ts`, `test/*.cjs`, and `tsconfig.json`. Applied the repository's `code-review` and `codebase-design` skills, including `FUNCTIONAL-CONTRACTS.md`, as a bounded reference review. No author history, implementation reports, evaluation reports, or other fixture implementations were consulted.

## Standards

No supported findings. Functional-design guidance is a judgement baseline here, not an additional fixture specification. Checked constructors perform runtime type, finite, integral, and range validation before introducing branded values. Raw user validation returns explicit invalid outcomes; brands alone are not treated as validation. Pure reservation uses only numeric inputs and preserves its checked range through subtraction. The injected store is an explicit effect seam, and the service awaits conditional write confirmation before returning success.

`src/persistence.ts:9` rejects corrupt stored stock with `TypeError`, so the service promise has an exceptional failure path outside its resolved result union. This differs from expected raw user validation, whose public constructors return invalid outcomes. The supplied specification requires validating storage observations, preserving operational failure behavior, and avoiding a new operational-error taxonomy. It does not require corrupt storage to be a reservation rejection. The implementation validates before domain entry and prevents a save; its test explicitly observes the rejection. This is not sufficient evidence for a defect or a requirement to add an invalid-storage result alternative. Callers must handle promise rejection for this service, as for store operational failures; the service is not a total raw-input operation.

## Spec

No supported findings. Formatting covers the literal suffix and required endpoints. Reservation checks distinct stock and request admission ranges, returns explicit insufficient-stock outcomes, and implements subtraction including depletion. The seeded property suite exercises successful arithmetic, range preservation, and rejection across admitted generated inputs; focused examples cover depletion and insufficient stock.

Persistence loads stock and version, validates stock, skips CAS on insufficient stock, and supplies the observed version and computed remainder to CAS. Tests demonstrate successful persistence, a changed version preventing a stale overwrite, operational errors propagating, and delayed CAS confirmation preventing early success. There is no automatic retry.

## Evidence limits

Fresh `node ../node_modules/typescript/bin/tsc --strict` succeeded. The rebuilt output passed `node --test test/*.cjs`: 11 tests, including 1,000 seeded reservation property trials. Compiler success establishes declared shapes, not numeric admission or universal totality. Property trials are behavioral evidence, not exhaustive coverage of all admitted pairs. Primitive numeric arguments make input preservation simple; freezing the containing test object does not establish a broader aliasing guarantee.

The in-memory store checks the orchestration contract and models atomic CAS; it does not prove any production store's atomicity, durability, or distributed execution guarantees. Checked brands can be bypassed by unsafe casts or JavaScript callers; the checked-domain functions assume callers use the constructors. No predecessor implementation or operational-error convention was supplied for comparison, so preservation of historical failure behavior cannot be independently established. No signature-first or red/green chronology claims were evaluated.

Findings: Standards 0; Spec 0. No worst issue on either axis.

## Artifact 1

`evidence/01-format-signatures.ts.txt`

````text
declare const formatBrand: unique symbol;
export type FormatQuantity = number & { readonly [formatBrand]: true };
export type FormatValidation = { readonly kind: 'valid'; readonly value: FormatQuantity } | { readonly kind: 'invalid' };
export function validateFormatQuantity(raw: unknown): FormatValidation { throw new Error('not implemented'); }
export function formatQuantity(q: FormatQuantity): string { throw new Error('not implemented'); }

````

## Artifact 2

`evidence/01-green.log`

````text
TAP version 13
# Subtest: formats admitted zero, one and upper bound with literal units
ok 1 - formats admitted zero, one and upper bound with literal units
  ---
  duration_ms: 1.659464
  ...
1..1
# tests 1
# suites 0
# pass 1
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 223.844805

````

## Artifact 3

`evidence/01-red.log`

````text
TAP version 13
# Subtest: formats admitted zero, one and upper bound with literal units
not ok 1 - formats admitted zero, one and upper bound with literal units
  ---
  duration_ms: 1.531814
  location: '/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/format.cjs:4:1'
  failureType: 'testCodeFailure'
  error: 'not implemented'
  code: 'ERR_TEST_FAILURE'
  stack: |-
    formatQuantity (/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/dist/format.js:6:36)
    TestContext.<anonymous> (/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/format.cjs:8:18)
    Test.runInAsyncScope (node:async_hooks:203:9)
    Test.run (node:internal/test_runner/test:631:25)
    Test.start (node:internal/test_runner/test:542:17)
    startSubtest (node:internal/test_runner/harness:214:17)
  ...
1..1
# tests 1
# suites 0
# pass 0
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 202.115603

````

## Artifact 4

`evidence/01-types-fixed.log`

````text

````

## Artifact 5

`evidence/01-types.log`

````text

````

## Artifact 6

`evidence/02-green.log`

````text
TAP version 13
# Subtest: formats admitted zero, one and upper bound with literal units
ok 1 - formats admitted zero, one and upper bound with literal units
  ---
  duration_ms: 1.611254
  ...
# Subtest: formatting validates numeric admission without coercion
ok 2 - formatting validates numeric admission without coercion
  ---
  duration_ms: 1.11904
  ...
1..2
# tests 2
# suites 0
# pass 2
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 184.036291

````

## Artifact 7

`evidence/02-red.log`

````text
TAP version 13
# Subtest: formats admitted zero, one and upper bound with literal units
ok 1 - formats admitted zero, one and upper bound with literal units
  ---
  duration_ms: 1.45489
  ...
# Subtest: formatting validates numeric admission without coercion
not ok 2 - formatting validates numeric admission without coercion
  ---
  duration_ms: 4.137453
  location: '/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/format.cjs:11:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected

      {
    +   kind: 'valid',
    +   value: NaN
    -   kind: 'invalid'
      }
  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
    kind: 'invalid'
  actual:
    kind: 'valid'
    value: NaN
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/format.cjs:13:12)
    Test.runInAsyncScope (node:async_hooks:203:9)
    Test.run (node:internal/test_runner/test:631:25)
    Test.processPendingSubtests (node:internal/test_runner/test:374:18)
    Test.postRun (node:internal/test_runner/test:715:19)
    Test.run (node:internal/test_runner/test:673:12)
    async startSubtest (node:internal/test_runner/harness:214:3)
  ...
1..2
# tests 2
# suites 0
# pass 1
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 232.329765

````

## Artifact 8

`evidence/03-green.log`

````text
TAP version 13
# Subtest: stock and requested quantity validate finite integer ranges without coercion
ok 1 - stock and requested quantity validate finite integer ranges without coercion
  ---
  duration_ms: 2.870997
  ...
1..1
# tests 1
# suites 0
# pass 1
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 183.319987

````

## Artifact 9

`evidence/03-red.log`

````text
TAP version 13
# Subtest: stock and requested quantity validate finite integer ranges without coercion
not ok 1 - stock and requested quantity validate finite integer ranges without coercion
  ---
  duration_ms: 1.495246
  location: '/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/reserve.cjs:6:1'
  failureType: 'testCodeFailure'
  error: 'not implemented'
  code: 'ERR_TEST_FAILURE'
  stack: |-
    validateStock (/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/dist/reserve.js:6:37)
    TestContext.<anonymous> (/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/reserve.cjs:8:114)
    Test.runInAsyncScope (node:async_hooks:203:9)
    Test.run (node:internal/test_runner/test:631:25)
    Test.start (node:internal/test_runner/test:542:17)
    startSubtest (node:internal/test_runner/harness:214:17)
  ...
1..1
# tests 1
# suites 0
# pass 0
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 185.782357

````

## Artifact 10

`evidence/03-reserve-signatures.ts.txt`

````text
declare const stockBrand: unique symbol;
declare const quantityBrand: unique symbol;
export type Stock = number & { readonly [stockBrand]: true };
export type ReservationQuantity = number & { readonly [quantityBrand]: true };
export type Validation<T> = { readonly kind: 'valid'; readonly value: T } | { readonly kind: 'invalid' };
export type Reservation = { readonly kind: 'success'; readonly remaining: Stock } | { readonly kind: 'insufficient-stock' };
export function validateStock(raw: unknown): Validation<Stock> { throw new Error('not implemented'); }
export function validateReservationQuantity(raw: unknown): Validation<ReservationQuantity> { throw new Error('not implemented'); }
export function reserve(stock: Stock, quantity: ReservationQuantity): Reservation { throw new Error('not implemented'); }

````

## Artifact 11

`evidence/03-types.log`

````text

````

## Artifact 12

`evidence/04-arithmetic-red.log`

````text
TAP version 13
# Subtest: stock and requested quantity validate finite integer ranges without coercion
ok 1 - stock and requested quantity validate finite integer ranges without coercion
  ---
  duration_ms: 2.320624
  ...
# Subtest: reservation conserves stock, stays in range and preserves every admitted input pair
not ok 2 - reservation conserves stock, stays in range and preserves every admitted input pair
  ---
  duration_ms: 5.71874
  location: '/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/reserve.cjs:14:1'
  failureType: 'testCodeFailure'
  error: |-
    Property failed after 1 tests
    { seed: 20261019, path: "0", endOnFailure: true }
    Counterexample: [1,1]
    Shrunk 0 time(s)

    Hint: Enable verbose mode in order to have the list of all failing values encountered during the run
  code: 'ERR_TEST_FAILURE'
  stack: |-
    buildError (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2484:16)
    throwIfFailed (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2491:8)
    reportRunDetails (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2507:14)
    Module.assert (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2677:7)
    TestContext.<anonymous> (/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/reserve.cjs:15:6)
    Test.runInAsyncScope (node:async_hooks:203:9)
    Test.run (node:internal/test_runner/test:631:25)
    Test.processPendingSubtests (node:internal/test_runner/test:374:18)
    Test.postRun (node:internal/test_runner/test:715:19)
    Test.run (node:internal/test_runner/test:673:12)
  ...
1..2
# tests 2
# suites 0
# pass 1
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 174.71417

````

## Artifact 13

`evidence/04-arithmetic-replay-red.log`

````text
TAP version 13
# Subtest: stock and requested quantity validate finite integer ranges without coercion
ok 1 - stock and requested quantity validate finite integer ranges without coercion
  ---
  duration_ms: 2.424088
  ...
# Subtest: reservation conserves stock, stays in range and preserves every admitted input pair
not ok 2 - reservation conserves stock, stays in range and preserves every admitted input pair
  ---
  duration_ms: 5.550023
  location: '/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/reserve.cjs:14:1'
  failureType: 'testCodeFailure'
  error: |-
    Property failed after 1 tests
    { seed: 20261019, path: "0", endOnFailure: true }
    Counterexample: [1,1]
    Shrunk 0 time(s)

    Hint: Enable verbose mode in order to have the list of all failing values encountered during the run
  code: 'ERR_TEST_FAILURE'
  stack: |-
    buildError (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2484:16)
    throwIfFailed (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2491:8)
    reportRunDetails (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2507:14)
    Module.assert (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2677:7)
    TestContext.<anonymous> (/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/reserve.cjs:15:6)
    Test.runInAsyncScope (node:async_hooks:203:9)
    Test.run (node:internal/test_runner/test:631:25)
    Test.processPendingSubtests (node:internal/test_runner/test:374:18)
    Test.postRun (node:internal/test_runner/test:715:19)
    Test.run (node:internal/test_runner/test:673:12)
  ...
1..2
# tests 2
# suites 0
# pass 1
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 180.270565

````

## Artifact 14

`evidence/04-green.log`

````text
TAP version 13
# Subtest: stock and requested quantity validate finite integer ranges without coercion
ok 1 - stock and requested quantity validate finite integer ranges without coercion
  ---
  duration_ms: 2.436091
  ...
# Subtest: reservation conserves stock, stays in range and preserves every admitted input pair
ok 2 - reservation conserves stock, stays in range and preserves every admitted input pair
  ---
  duration_ms: 14.790041
  ...
# Subtest: focused rejection and depletion regressions
ok 3 - focused rejection and depletion regressions
  ---
  duration_ms: 0.250049
  ...
1..3
# tests 3
# suites 0
# pass 3
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 210.379469

````

## Artifact 15

`evidence/04-property-test.cjs.txt`

````text
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fc = require('fast-check');
const { validateStock, validateReservationQuantity, reserve } = require('../dist/reserve');
function admitted(check, raw) { const result = check(raw); assert.equal(result.kind, 'valid'); return result.value; }
test('stock and requested quantity validate finite integer ranges without coercion', () => {
  for (const check of [validateStock, validateReservationQuantity]) {
    for (const raw of [NaN, Infinity, -Infinity, 0.5, -1, 101, '1', null, undefined, {}, true]) assert.deepEqual(check(raw), { kind: 'invalid' });
    for (const raw of [1, 100]) assert.equal(admitted(check, raw), raw);
  }
  assert.equal(admitted(validateStock, 0), 0);
  assert.deepEqual(validateReservationQuantity(0), { kind: 'invalid' });
});
test('reservation conserves stock, stays in range and preserves every admitted input pair', () => {
  fc.assert(fc.property(fc.integer({ min: 0, max: 100 }), fc.integer({ min: 1, max: 100 }), (s, q) => {
    const inputs = Object.freeze({ stock: admitted(validateStock, s), quantity: admitted(validateReservationQuantity, q) });
    const before = { ...inputs };
    const result = reserve(inputs.stock, inputs.quantity);
    assert.deepEqual(inputs, before);
    if (q <= s) {
      assert.equal(result.kind, 'success');
      assert.equal(result.remaining + q, s);
      assert.ok(result.remaining >= 0 && result.remaining <= 100);
    } else assert.deepEqual(result, { kind: 'insufficient-stock' });
  }), { seed: 20261019, numRuns: 1000 });
});

````

## Artifact 16

`evidence/04-red.log`

````text
TAP version 13
# Subtest: stock and requested quantity validate finite integer ranges without coercion
ok 1 - stock and requested quantity validate finite integer ranges without coercion
  ---
  duration_ms: 2.863884
  ...
# Subtest: reservation conserves stock, stays in range and preserves every admitted input pair
not ok 2 - reservation conserves stock, stays in range and preserves every admitted input pair
  ---
  duration_ms: 4.001779
  location: '/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/reserve.cjs:14:1'
  failureType: 'testCodeFailure'
  error: |-
    Property failed after 1 tests
    { seed: 20261019, path: "0:0", endOnFailure: true }
    Counterexample: [0,1]
    Shrunk 1 time(s)

    Hint: Enable verbose mode in order to have the list of all failing values encountered during the run
  code: 'ERR_TEST_FAILURE'
  stack: |-
    buildError (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2484:16)
    throwIfFailed (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2491:8)
    reportRunDetails (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2507:14)
    Module.assert (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2677:7)
    TestContext.<anonymous> (/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/reserve.cjs:15:6)
    Test.runInAsyncScope (node:async_hooks:203:9)
    Test.run (node:internal/test_runner/test:631:25)
    Test.processPendingSubtests (node:internal/test_runner/test:374:18)
    Test.postRun (node:internal/test_runner/test:715:19)
    Test.run (node:internal/test_runner/test:673:12)
  ...
1..2
# tests 2
# suites 0
# pass 1
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 192.907877

````

## Artifact 17

`evidence/04-replay-red.log`

````text
TAP version 13
# Subtest: stock and requested quantity validate finite integer ranges without coercion
ok 1 - stock and requested quantity validate finite integer ranges without coercion
  ---
  duration_ms: 2.870366
  ...
# Subtest: reservation conserves stock, stays in range and preserves every admitted input pair
not ok 2 - reservation conserves stock, stays in range and preserves every admitted input pair
  ---
  duration_ms: 5.158008
  location: '/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/reserve.cjs:14:1'
  failureType: 'testCodeFailure'
  error: |-
    Property failed after 1 tests
    { seed: 20261019, path: "0:0", endOnFailure: true }
    Counterexample: [0,1]
    Shrunk 0 time(s)

    Hint: Enable verbose mode in order to have the list of all failing values encountered during the run
  code: 'ERR_TEST_FAILURE'
  stack: |-
    buildError (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2484:16)
    throwIfFailed (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2491:8)
    reportRunDetails (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2507:14)
    Module.assert (/tmp/functional-skills.ECtJb0/evaluation/node_modules/fast-check/lib/cjs/fast-check.js:2677:7)
    TestContext.<anonymous> (/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/reserve.cjs:15:6)
    Test.runInAsyncScope (node:async_hooks:203:9)
    Test.run (node:internal/test_runner/test:631:25)
    Test.processPendingSubtests (node:internal/test_runner/test:374:18)
    Test.postRun (node:internal/test_runner/test:715:19)
    Test.run (node:internal/test_runner/test:673:12)
  ...
1..2
# tests 2
# suites 0
# pass 1
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 194.117076

````

## Artifact 18

`evidence/05-green.log`

````text
TAP version 13
# Subtest: successful persistence uses observed version and completes save before success
ok 1 - successful persistence uses observed version and completes save before success
  ---
  duration_ms: 2.299395
  ...
1..1
# tests 1
# suites 0
# pass 1
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 156.555017

````

## Artifact 19

`evidence/05-persistence-signatures.ts.txt`

````text
import { Reservation, ReservationQuantity, Stock, reserve, validateStock } from './reserve';
export interface InventoryStore {
  load(): Promise<{ readonly stock: unknown; readonly version: number }>;
  compareAndSwap(expectedVersion: number, remaining: Stock): Promise<boolean>;
}
export type PersistedReservation = Reservation | { readonly kind: 'conflict' };
export async function reservePersisted(store: InventoryStore, quantity: ReservationQuantity): Promise<PersistedReservation> { throw new Error('not implemented'); }

````

## Artifact 20

`evidence/05-red.log`

````text
TAP version 13
# Subtest: successful persistence uses observed version and completes save before success
not ok 1 - successful persistence uses observed version and completes save before success
  ---
  duration_ms: 4.624056
  location: '/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/persistence.cjs:17:1'
  failureType: 'testCodeFailure'
  error: 'not implemented'
  code: 'ERR_TEST_FAILURE'
  stack: |-
    reservePersisted (/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/dist/persistence.js:4:58)
    TestContext.<anonymous> (/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/persistence.cjs:19:26)
    Test.runInAsyncScope (node:async_hooks:203:9)
    Test.run (node:internal/test_runner/test:631:25)
    Test.start (node:internal/test_runner/test:542:17)
    startSubtest (node:internal/test_runner/harness:214:17)
  ...
1..1
# tests 1
# suites 0
# pass 0
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 172.323544

````

## Artifact 21

`evidence/05-types.log`

````text

````

## Artifact 22

`evidence/06-green.log`

````text
TAP version 13
# Subtest: successful persistence uses observed version and completes save before success
ok 1 - successful persistence uses observed version and completes save before success
  ---
  duration_ms: 2.307479
  ...
# Subtest: insufficient stock avoids writes
ok 2 - insufficient stock avoids writes
  ---
  duration_ms: 0.223269
  ...
# Subtest: concurrent change prevents a stale save and returns explicit conflict
ok 3 - concurrent change prevents a stale save and returns explicit conflict
  ---
  duration_ms: 0.333736
  ...
1..3
# tests 3
# suites 0
# pass 3
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 147.609522

````

## Artifact 23

`evidence/06-red.log`

````text
TAP version 13
# Subtest: successful persistence uses observed version and completes save before success
ok 1 - successful persistence uses observed version and completes save before success
  ---
  duration_ms: 2.54251
  ...
# Subtest: insufficient stock avoids writes
ok 2 - insufficient stock avoids writes
  ---
  duration_ms: 0.204133
  ...
# Subtest: concurrent change prevents a stale save and returns explicit conflict
not ok 3 - concurrent change prevents a stale save and returns explicit conflict
  ---
  duration_ms: 2.778794
  location: '/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/persistence.cjs:28:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected

      {
    +   kind: 'success',
    +   remaining: 7
    -   kind: 'conflict'
      }
  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
    kind: 'conflict'
  actual:
    kind: 'success'
    remaining: 7
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (/tmp/functional-skills.ECtJb0/evaluation/handoff-rerun/test/persistence.cjs:36:10)
    async Test.run (node:internal/test_runner/test:632:9)
    async Test.processPendingSubtests (node:internal/test_runner/test:374:7)
  ...
1..3
# tests 3
# suites 0
# pass 2
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 175.418872

````

## Artifact 24

`evidence/final-tests.log`

````text
TAP version 13
# Subtest: formats admitted zero, one and upper bound with literal units
ok 1 - formats admitted zero, one and upper bound with literal units
  ---
  duration_ms: 2.114157
  ...
# Subtest: formatting validates numeric admission without coercion
ok 2 - formatting validates numeric admission without coercion
  ---
  duration_ms: 1.562572
  ...
# Subtest: successful persistence uses observed version and completes save before success
ok 3 - successful persistence uses observed version and completes save before success
  ---
  duration_ms: 4.731989
  ...
# Subtest: insufficient stock avoids writes
ok 4 - insufficient stock avoids writes
  ---
  duration_ms: 0.266179
  ...
# Subtest: concurrent change prevents a stale save and returns explicit conflict
ok 5 - concurrent change prevents a stale save and returns explicit conflict
  ---
  duration_ms: 1.294289
  ...
# Subtest: invalid stored observations never reach a save
ok 6 - invalid stored observations never reach a save
  ---
  duration_ms: 1.124099
  ...
# Subtest: load and save operational failures propagate unchanged
ok 7 - load and save operational failures propagate unchanged
  ---
  duration_ms: 0.656491
  ...
# Subtest: persistence success waits for CAS confirmation
ok 8 - persistence success waits for CAS confirmation
  ---
  duration_ms: 0.673363
  ...
# Subtest: stock and requested quantity validate finite integer ranges without coercion
ok 9 - stock and requested quantity validate finite integer ranges without coercion
  ---
  duration_ms: 2.64917
  ...
# Subtest: reservation conserves stock, stays in range and preserves every admitted input pair
ok 10 - reservation conserves stock, stays in range and preserves every admitted input pair
  ---
  duration_ms: 16.286259
  ...
# Subtest: focused rejection and depletion regressions
ok 11 - focused rejection and depletion regressions
  ---
  duration_ms: 0.252795
  ...
1..11
# tests 11
# suites 0
# pass 11
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 198.830429

````

## Artifact 25

`evidence/final-types.log`

````text

````

## Artifact 26

`src/format.ts`

````text
declare const formatBrand: unique symbol;
export type FormatQuantity = number & { readonly [formatBrand]: true };
export type FormatValidation = { readonly kind: 'valid'; readonly value: FormatQuantity } | { readonly kind: 'invalid' };
export function validateFormatQuantity(raw: unknown): FormatValidation { if (typeof raw !== 'number' || !Number.isFinite(raw) || !Number.isInteger(raw) || raw < 0 || raw > 100) return { kind: 'invalid' };
  return { kind: 'valid', value: raw as FormatQuantity }; }
export function formatQuantity(q: FormatQuantity): string { return `${q} units`; }

````

## Artifact 27

`src/persistence.ts`

````text
import { Reservation, ReservationQuantity, Stock, reserve, validateStock } from './reserve';
export interface InventoryStore {
  load(): Promise<{ readonly stock: unknown; readonly version: number }>;
  compareAndSwap(expectedVersion: number, remaining: Stock): Promise<boolean>;
}
export type PersistedReservation = Reservation | { readonly kind: 'conflict' };
export async function reservePersisted(store: InventoryStore, quantity: ReservationQuantity): Promise<PersistedReservation> { const observed = await store.load();
  const stock = validateStock(observed.stock);
  if (stock.kind === 'invalid') throw new TypeError('Store returned invalid stock');
  const result = reserve(stock.value, quantity);
  if (result.kind === 'insufficient-stock') return result;
  if (!await store.compareAndSwap(observed.version, result.remaining)) return { kind: 'conflict' };
  return result; }

````

## Artifact 28

`src/reserve.ts`

````text
declare const stockBrand: unique symbol;
declare const quantityBrand: unique symbol;
export type Stock = number & { readonly [stockBrand]: true };
export type ReservationQuantity = number & { readonly [quantityBrand]: true };
export type Validation<T> = { readonly kind: 'valid'; readonly value: T } | { readonly kind: 'invalid' };
export type Reservation = { readonly kind: 'success'; readonly remaining: Stock } | { readonly kind: 'insufficient-stock' };
export function validateStock(raw: unknown): Validation<Stock> { if (typeof raw !== 'number' || !Number.isFinite(raw) || !Number.isInteger(raw) || raw < 0 || raw > 100) return { kind: 'invalid' };
  return { kind: 'valid', value: raw as Stock }; }
export function validateReservationQuantity(raw: unknown): Validation<ReservationQuantity> { if (typeof raw !== 'number' || !Number.isFinite(raw) || !Number.isInteger(raw) || raw < 1 || raw > 100) return { kind: 'invalid' };
  return { kind: 'valid', value: raw as ReservationQuantity }; }
export function reserve(stock: Stock, quantity: ReservationQuantity): Reservation { if (quantity > stock) return { kind: 'insufficient-stock' };
  return { kind: 'success', remaining: (stock - quantity) as Stock }; }

````

## Artifact 29

`test/format.cjs`

````text
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { validateFormatQuantity, formatQuantity } = require('../dist/format');
test('formats admitted zero, one and upper bound with literal units', () => {
  for (const [q, expected] of [[0, '0 units'], [1, '1 units'], [100, '100 units']]) {
    const checked = validateFormatQuantity(q);
    assert.equal(checked.kind, 'valid');
    assert.equal(formatQuantity(checked.value), expected);
  }
});
test('formatting validates numeric admission without coercion', () => {
  for (const raw of [NaN, Infinity, -Infinity, 0.5, -1, 101, '1', null, undefined, {}, true]) {
    assert.deepEqual(validateFormatQuantity(raw), { kind: 'invalid' });
  }
});

````

## Artifact 30

`test/persistence.cjs`

````text
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { reservePersisted } = require('../dist/persistence');
const { validateReservationQuantity } = require('../dist/reserve');
const quantity = n => { const r = validateReservationQuantity(n); assert.equal(r.kind, 'valid'); return r.value; };
class MemoryStore {
  constructor(stock, version = 42) { this.stock = stock; this.version = version; this.saves = 0; }
  async load() { return { stock: this.stock, version: this.version }; }
  async compareAndSwap(expected, remaining) {
    this.saves++;
    if (expected !== this.version) return false;
    this.stock = remaining;
    this.version++;
    return true;
  }
}
test('successful persistence uses observed version and completes save before success', async () => {
  const store = new MemoryStore(10, 42);
  assert.deepEqual(await reservePersisted(store, quantity(3)), { kind: 'success', remaining: 7 });
  assert.deepEqual(await store.load(), { stock: 7, version: 43 });
});
test('insufficient stock avoids writes', async () => {
  const store = new MemoryStore(2);
  assert.deepEqual(await reservePersisted(store, quantity(3)), { kind: 'insufficient-stock' });
  assert.equal(store.saves, 0);
  assert.deepEqual(await store.load(), { stock: 2, version: 42 });
});
test('concurrent change prevents a stale save and returns explicit conflict', async () => {
  class RacingStore extends MemoryStore {
    async compareAndSwap(expected, remaining) {
      await super.compareAndSwap(this.version, 9);
      return super.compareAndSwap(expected, remaining);
    }
  }
  const store = new RacingStore(10);
  assert.deepEqual(await reservePersisted(store, quantity(3)), { kind: 'conflict' });
  assert.deepEqual(await store.load(), { stock: 9, version: 43 });
});
test('invalid stored observations never reach a save', async () => {
  for (const raw of [NaN, Infinity, -Infinity, 0.5, -1, 101, '1', null, undefined]) {
    const store = new MemoryStore(raw);
    await assert.rejects(reservePersisted(store, quantity(1)), { name: 'TypeError', message: 'Store returned invalid stock' });
    assert.equal(store.saves, 0);
  }
  assert.deepEqual(await reservePersisted(new MemoryStore(0), quantity(1)), { kind: 'insufficient-stock' });
});
test('load and save operational failures propagate unchanged', async () => {
  const failure = new Error('unavailable');
  const loadFailure = new MemoryStore(10);
  loadFailure.load = async () => { throw failure; };
  await assert.rejects(reservePersisted(loadFailure, quantity(1)), e => e === failure);
  assert.equal(loadFailure.saves, 0);
  const saveFailure = new MemoryStore(10);
  saveFailure.compareAndSwap = async () => { await Promise.resolve(); throw failure; };
  await assert.rejects(reservePersisted(saveFailure, quantity(1)), e => e === failure);
});
test('persistence success waits for CAS confirmation', async () => {
  const store = new MemoryStore(10);
  let release;
  const gate = new Promise(resolve => { release = resolve; });
  const cas = store.compareAndSwap.bind(store);
  let entered;
  const started = new Promise(resolve => { entered = resolve; });
  store.compareAndSwap = async (...args) => { entered(); await gate; return cas(...args); };
  let settled = false;
  const pending = reservePersisted(store, quantity(3)).then(result => { settled = true; return result; });
  await started;
  await Promise.resolve();
  assert.equal(settled, false);
  release();
  assert.deepEqual(await pending, { kind: 'success', remaining: 7 });
});

````

## Artifact 31

`test/reserve.cjs`

````text
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fc = require('fast-check');
const { validateStock, validateReservationQuantity, reserve } = require('../dist/reserve');
function admitted(check, raw) { const result = check(raw); assert.equal(result.kind, 'valid'); return result.value; }
test('stock and requested quantity validate finite integer ranges without coercion', () => {
  for (const check of [validateStock, validateReservationQuantity]) {
    for (const raw of [NaN, Infinity, -Infinity, 0.5, -1, 101, '1', null, undefined, {}, true]) assert.deepEqual(check(raw), { kind: 'invalid' });
    for (const raw of [1, 100]) assert.equal(admitted(check, raw), raw);
  }
  assert.equal(admitted(validateStock, 0), 0);
  assert.deepEqual(validateReservationQuantity(0), { kind: 'invalid' });
});
test('reservation conserves stock, stays in range and preserves every admitted input pair', () => {
  fc.assert(fc.property(fc.integer({ min: 0, max: 100 }), fc.integer({ min: 1, max: 100 }), (s, q) => {
    const inputs = Object.freeze({ stock: admitted(validateStock, s), quantity: admitted(validateReservationQuantity, q) });
    const before = { ...inputs };
    const result = reserve(inputs.stock, inputs.quantity);
    assert.deepEqual(inputs, before);
    if (q <= s) {
      assert.equal(result.kind, 'success');
      assert.equal(result.remaining + q, s);
      assert.ok(result.remaining >= 0 && result.remaining <= 100);
    } else assert.deepEqual(result, { kind: 'insufficient-stock' });
  }), { seed: 20261019, numRuns: 1000 });
});
test('focused rejection and depletion regressions', () => {
  for (const [s, q] of [[0, 1], [2, 3]]) assert.deepEqual(reserve(admitted(validateStock, s), admitted(validateReservationQuantity, q)), { kind: 'insufficient-stock' });
  for (const n of [1, 100]) assert.deepEqual(reserve(admitted(validateStock, n), admitted(validateReservationQuantity, n)), { kind: 'success', remaining: 0 });
});

````

## Artifact 32

`tsconfig.json`

````text
{"compilerOptions":{"target":"ES2022","module":"CommonJS","strict":true,"rootDir":"src","outDir":"dist"},"include":["src/**/*.ts"]}

````
