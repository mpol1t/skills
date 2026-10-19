# Inventory fixture implementation

Implemented both approved tickets independently. Final strict TypeScript check succeeds; all 11 Node tests pass, including 1,000 fast-check cases.

## Inputs and skills

Requirements read only from `spec.md`, `.scratch/inventory/issues/01-format.md`, and `.scratch/inventory/issues/02-reserve.md`. Did not read planner REPORT.md, parent specification, or other evaluation reports. Invoked current source `tdd` and `codebase-design` by reading their SKILL.md files, plus tdd tests.md, mocking.md, properties.md, and codebase-design FUNCTIONAL-CONTRACTS.md. No repo edits, commits, network publication, or framework installs.

The fixture contained planning artifacts, with no existing source, runner, validation convention, or concrete store interface declaration to preserve. Used built-in Node test/assert and the supplied fast-check installation. Store method names are a minimal realization of the already approved load/version/CAS interface. Invalid raw inputs throw RangeError with no coercion. Operational failures propagate unchanged; no retry or new operational-error outcome was added.

## Final files

- [Formatting](#artifact-1)
- [Pure reservation](#artifact-2)
- [Persistence](#artifact-3)
- [Formatting examples](#artifact-4)
- [Reservation examples and property](#artifact-5)
- [Injected-store integration checks](#artifact-6)
- [Compiler configuration](#artifact-7)
- [Final compiler log](#artifact-8)
- [Final test log](#artifact-9)

`formatQuantity(unknown): string` validates and formats. `reserve(unknown, unknown): Reservation` validates then computes explicit success or insufficient-stock outcomes. Both operate synchronously without I/O, mutable ambient dependencies, or caller-owned mutation. Numeric primitive inputs need no brand or object hierarchy; runtime admission protects the operations. No casts are used. The checks reject nonnumeric inputs as well as invalid numeric ranges, fractions, and nonfinite numbers.

`reservePersisted(store, unknown): Promise<PersistedReservation>` loads an observation, validates it through reserve, avoids saving on rejection, awaits CAS with the observed version, and reports success only after confirmation. The store observation deliberately uses unknown stock because persisted data is untrusted. Result fields are readonly. TypeScript checks declared shapes and discriminant narrowing; no claim of an exhaustive switch check or compile-time numeric admission is made.

## Type-first and red/green evidence

Before each behavior body, saved its public types/signatures with a throwing placeholder, then invoked the real compiler:

- [Formatting signature](#artifact-10)
- [Reservation types and signature](#artifact-11)
- [Persistence types and signature](#artifact-12)

Compiler command, from this directory, on every compilation:

```sh
node /tmp/functional-skills.ECtJb0/evaluation/node_modules/typescript/bin/tsc -p tsconfig.json
```

Initial compiler feedback was TS5011: explicit rootDir required. It is retained in `evidence/01-types.log`. The initial test attempt could not find the output module (`02-format-red.log`); this is a setup failure, not behavioral evidence. Set rootDir to src; compilation then passed (`03-types.log`) before behavioral implementation. Subsequent type-first checks passed (`08-types.log`, `15-types.log`).

Actual behavioral sequence and exact test commands:

1. `node --test tests/format.test.cjs`: admitted examples 0, 1, 100 failed on placeholder (`04-format-red.log`). Added literal units formatting, compiled, reran: green (`05-format-green.log`).
2. Same command: new raw validation examples failed with missing RangeError (`06-validation-red.log`). Added finite/integer/range/type checks, compiled, reran: green (`07-validation-green.log`). Formatting remains example-only.
3. `node --test tests/reserve.test.cjs`: generated admitted inputs failed on placeholder (`09-property-red.log`). fast-check seed 20261019, path `0:0`, counterexample `[0,1]`, one shrink. Replayed unchanged defective implementation with `REPLAY=0:0 node --test tests/reserve.test.cjs` (`10-property-replay.log`), again failed. Retained `[0,1]` alongside `[2,3]` and exact depletion `[100,100]` as readable examples; same test command failed (`11-examples-red.log`). Implemented outcomes and arithmetic, compiled; `node --test tests/*.test.cjs` passed (`12-reserve-green.log`).
4. `node --test tests/reserve.test.cjs`: new raw admission tests failed with missing RangeError (`13-raw-red.log`). Added complete validation; compiled and ran `node --test tests/*.test.cjs`: green (`14-raw-green.log`).
5. `node --test tests/persistence.test.cjs`: injected-store successful persistence failed on placeholder (`16-persistence-red.log`). Added load, computation, insufficient return, awaited CAS; compiled and ran `node --test tests/*.test.cjs`: green (`17-persistence-green.log`).
6. `node --test tests/persistence.test.cjs`: new concurrent-write test observed false success instead of conflict (`18-conflict-red.log`). Checked CAS boolean; compiled and ran `node --test tests/*.test.cjs`: green (`19-conflict-green.log`).
7. Added verification cases for behavior already supplied by these slices: insufficient stock without writes, untrusted observations/raw requests without writes, unchanged operational errors, and waiting for CAS confirmation. These were green on first run, not claimed as new red/green cycles. Final compiler command above and `node --test tests/*.test.cjs` passed (`20-final-types.log`, `21-final-tests.log`).

Logs were captured using shell redirection `> evidence/<named-log> 2>&1`; red runs intentionally return failure. Final commands are directly runnable with the supplied parent dependencies. No runner installation is needed.

## Evidence selection and limits

Formatting is intentionally simple example-only coverage. Public reserve properties generate stock 0..100 and requested quantity 1..100 constructively, with no discarded cases. The conservation law `remaining + quantity === stock`, bounds, explicit rejected branch, and focused depletion examples constrain plausible wrong results. Frozen input tuples remain unchanged; because domain values are primitives, there is no mutable domain alias to protect. The fixed seed and 1,000-run budget provide reproducible sampled evidence, not proof over all pairs.

Store integration uses an in-memory adapter at the approved injected seam, with observations read through load. A nonzero version 42 verifies that the loaded version is used. The race adapter performs a real conditional competing write before the stale CAS, leaving stock 9/version 8 and returning conflict. Writes are observed only at this expressly agreed persistence seam to verify the no-save promise. No internal helper is mocked.

Types do not establish numeric invariants, runtime validation does not establish that a loaded observation stays current, and injection alone does not establish purity. Atomic CAS in a production adapter remains an assumption. Normal runtime resources and eventual settlement of store promises remain assumptions. No distributed exactly-once or universal termination claim is made. The finite pure computations have no loops or recursion; the persistence module performs at most one load and one save attempt.

Tool versions observed: TypeScript 7.0.2 (`node /tmp/functional-skills.ECtJb0/evaluation/node_modules/typescript/bin/tsc --version`), fast-check 4.10.2 (`node -p "require('fast-check/package.json').version"`), Node v18.20.4 (reported by test runner).

## Artifact 1

Original file: `src/format.ts`.

```text
/** Raw numeric inputs only. Admits finite integers in [0, 100]. */
export function formatQuantity(quantity: unknown): string {
  if (typeof quantity !== 'number' || !Number.isFinite(quantity) || !Number.isInteger(quantity) || quantity < 0 || quantity > 100) {
    throw new RangeError('Expected integer quantity from 0 to 100');
  }
  return `${quantity} units`;
}
```

## Artifact 2

Original file: `src/reserve.ts`.

```text
export type Reservation =
  | { readonly kind: 'success'; readonly remaining: number }
  | { readonly kind: 'insufficient-stock' };

/** Numeric stock in [0, 100], quantity in [1, 100]; validates raw entry. */
export function reserve(stock: unknown, quantity: unknown): Reservation {
  if (typeof stock !== 'number' || !Number.isFinite(stock) || !Number.isInteger(stock) || stock < 0 || stock > 100) throw new RangeError('Expected stock from 0 to 100');
  if (typeof quantity !== 'number' || !Number.isFinite(quantity) || !Number.isInteger(quantity) || quantity < 1 || quantity > 100) throw new RangeError('Expected quantity from 1 to 100');
  return quantity <= stock
    ? { kind: 'success', remaining: stock - quantity }
    : { kind: 'insufficient-stock' };
}
```

## Artifact 3

Original file: `src/persistence.ts`.

```text
import { reserve, type Reservation } from './reserve';
export interface InventoryStore {
  load(): Promise<{ readonly stock: unknown; readonly version: number }>;
  compareAndSwap(expectedVersion: number, remaining: number): Promise<boolean>;
}
export type PersistedReservation = Reservation | { readonly kind: 'conflict' };
/** Errors propagate; one attempt, no retries. CAS must be atomic in the adapter. */
export async function reservePersisted(store: InventoryStore, quantity: unknown): Promise<PersistedReservation> {
  const observed = await store.load();
  const result = reserve(observed.stock, quantity);
  if (result.kind === 'insufficient-stock') return result;
  const saved = await store.compareAndSwap(observed.version, result.remaining);
  if (!saved) return { kind: 'conflict' };
  return result;
}
```

## Artifact 4

Original file: `tests/format.test.cjs`.

```text
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { formatQuantity } = require('../dist/format');
test('formats admitted quantities with literal units', () => {
  for (const [input, expected] of [[0, '0 units'], [1, '1 units'], [100, '100 units']]) {
    assert.equal(formatQuantity(input), expected);
  }
});
test('rejects raw invalid format quantities without coercion', () => {
  for (const value of [NaN, Infinity, -Infinity, 0.5, -1, 101, '1', null, undefined, {}, true]) {
    assert.throws(() => formatQuantity(value), RangeError);
  }
});
```

## Artifact 5

Original file: `tests/reserve.test.cjs`.

```text
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fc = require('fast-check');
const { reserve } = require('../dist/reserve');
test('admitted reservations conserve stock and preserve inputs', () => {
  fc.assert(fc.property(fc.integer({ min: 0, max: 100 }), fc.integer({ min: 1, max: 100 }), (stock, quantity) => {
    const inputs = Object.freeze([stock, quantity]);
    const result = reserve(...inputs);
    assert.deepEqual(inputs, [stock, quantity]);
    if (quantity <= stock) {
      assert.equal(result.kind, 'success');
      assert.equal(result.remaining + quantity, stock);
      assert.ok(result.remaining >= 0 && result.remaining <= 100);
    } else {
      assert.deepEqual(result, { kind: 'insufficient-stock' });
    }
  }), { seed: 20261019, numRuns: 1000, ...(process.env.REPLAY ? { path: process.env.REPLAY } : {}) });
});
test('zero stock and insufficient stock reject; exact depletion succeeds', () => {
  assert.deepEqual(reserve(0, 1), { kind: 'insufficient-stock' });
  assert.deepEqual(reserve(2, 3), { kind: 'insufficient-stock' });
  assert.deepEqual(reserve(100, 100), { kind: 'success', remaining: 0 });
});
test('raw reservation inputs reject invalid numeric domains', () => {
  for (const value of [NaN, Infinity, -Infinity, 0.5, -1, 101, '1', null, undefined, {}, true]) {
    assert.throws(() => reserve(value, 1), RangeError);
    assert.throws(() => reserve(100, value), RangeError);
  }
  assert.throws(() => reserve(100, 0), RangeError);
  assert.deepEqual(reserve(0, 1), { kind: 'insufficient-stock' });
});
```

## Artifact 6

Original file: `tests/persistence.test.cjs`.

```text
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { reservePersisted } = require('../dist/persistence');
class MemoryStore {
  constructor(stock, version = 7) { this.stock = stock; this.version = version; this.writes = 0; }
  async load() { return { stock: this.stock, version: this.version }; }
  async compareAndSwap(expectedVersion, remaining) {
    this.writes++;
    if (expectedVersion !== this.version) return false;
    this.stock = remaining;
    this.version++;
    return true;
  }
}
test('persists remaining stock using the loaded version', async () => {
  const store = new MemoryStore(10, 42);
  assert.deepEqual(await reservePersisted(store, 3), { kind: 'success', remaining: 7 });
  assert.deepEqual(await store.load(), { stock: 7, version: 43 });
  assert.equal(store.writes, 1);
});
test('concurrent version change prevents stale write and reports conflict', async () => {
  class RacingStore extends MemoryStore {
    async compareAndSwap(expectedVersion, remaining) {
      await super.compareAndSwap(this.version, 9);
      return super.compareAndSwap(expectedVersion, remaining);
    }
  }
  const store = new RacingStore(10);
  assert.deepEqual(await reservePersisted(store, 3), { kind: 'conflict' });
  assert.deepEqual(await store.load(), { stock: 9, version: 8 });
  assert.equal(store.writes, 2);
});
test('insufficient stock performs no conditional save', async () => {
  const store = new MemoryStore(2);
  assert.deepEqual(await reservePersisted(store, 3), { kind: 'insufficient-stock' });
  assert.equal(store.writes, 0);
  assert.deepEqual(await store.load(), { stock: 2, version: 7 });
});
test('untrusted observations and reservation quantities cannot be saved', async () => {
  for (const raw of [NaN, Infinity, -Infinity, 0.5, -1, 101, '1', null, undefined, {}, true]) {
    const corrupt = new MemoryStore(raw);
    await assert.rejects(reservePersisted(corrupt, 1), RangeError);
    assert.equal(corrupt.writes, 0);
    const valid = new MemoryStore(100);
    await assert.rejects(reservePersisted(valid, raw), RangeError);
    assert.equal(valid.writes, 0);
  }
  const store = new MemoryStore(100);
  await assert.rejects(reservePersisted(store, 0), RangeError);
  assert.equal(store.writes, 0);
});
test('operational failures propagate unchanged', async () => {
  const error = new Error('storage unavailable');
  await assert.rejects(reservePersisted({
    load: async () => { throw error; },
    compareAndSwap: async () => { assert.fail('must not save'); }
  }, 1), e => e === error);
  await assert.rejects(reservePersisted({
    load: async () => ({ stock: 10, version: 7 }),
    compareAndSwap: async () => { throw error; }
  }, 1), e => e === error);
});
test('does not report success until CAS confirms', async () => {
  let confirm;
  const pendingCAS = new Promise(resolve => { confirm = resolve; });
  let settled = false;
  const result = reservePersisted({
    load: async () => ({ stock: 10, version: 7 }),
    compareAndSwap: () => pendingCAS
  }, 1).then(value => { settled = true; return value; });
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(settled, false);
  confirm(true);
  assert.deepEqual(await result, { kind: 'success', remaining: 9 });
});
```

## Artifact 7

Original file: `tsconfig.json`.

```text
{"compilerOptions": {"target": "ES2022", "module": "CommonJS", "strict": true, "outDir": "dist", "declaration": true, "rootDir": "src"}, "include": ["src/**/*.ts"]}
```

## Artifact 8

Original file: `evidence/20-final-types.log`.

```text

```

## Artifact 9

Original file: `evidence/21-final-tests.log`.

```text
TAP version 13
# Subtest: formats admitted quantities with literal units
ok 1 - formats admitted quantities with literal units
  ---
  duration_ms: 1.626862
  ...
# Subtest: rejects raw invalid format quantities without coercion
ok 2 - rejects raw invalid format quantities without coercion
  ---
  duration_ms: 0.593604
  ...
# Subtest: persists remaining stock using the loaded version
ok 3 - persists remaining stock using the loaded version
  ---
  duration_ms: 3.644268
  ...
# Subtest: concurrent version change prevents stale write and reports conflict
ok 4 - concurrent version change prevents stale write and reports conflict
  ---
  duration_ms: 0.567895
  ...
# Subtest: insufficient stock performs no conditional save
ok 5 - insufficient stock performs no conditional save
  ---
  duration_ms: 0.241703
  ...
# Subtest: untrusted observations and reservation quantities cannot be saved
ok 6 - untrusted observations and reservation quantities cannot be saved
  ---
  duration_ms: 1.87633
  ...
# Subtest: operational failures propagate unchanged
ok 7 - operational failures propagate unchanged
  ---
  duration_ms: 1.02886
  ...
# Subtest: does not report success until CAS confirms
ok 8 - does not report success until CAS confirms
  ---
  duration_ms: 11.726884
  ...
# Subtest: admitted reservations conserve stock and preserve inputs
ok 9 - admitted reservations conserve stock and preserve inputs
  ---
  duration_ms: 32.071076
  ...
# Subtest: zero stock and insufficient stock reject; exact depletion succeeds
ok 10 - zero stock and insufficient stock reject; exact depletion succeeds
  ---
  duration_ms: 0.244128
  ...
# Subtest: raw reservation inputs reject invalid numeric domains
ok 11 - raw reservation inputs reject invalid numeric domains
  ---
  duration_ms: 2.118465
  ...
1..11
# tests 11
# suites 0
# pass 11
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 287.183759
```

## Artifact 10

Original file: `evidence/01-format-signature.ts.txt`.

```text
/** Raw numeric inputs only. Admits finite integers in [0, 100]. */
export function formatQuantity(quantity: unknown): string {
  throw new Error('not implemented');
}
```

## Artifact 11

Original file: `evidence/08-reserve-signatures.ts.txt`.

```text
export type Reservation =
  | { readonly kind: 'success'; readonly remaining: number }
  | { readonly kind: 'insufficient-stock' };

/** Numeric stock in [0, 100], quantity in [1, 100]; validates raw entry. */
export function reserve(stock: unknown, quantity: unknown): Reservation {
  throw new Error('not implemented');
}
```

## Artifact 12

Original file: `evidence/15-persistence-signatures.ts.txt`.

```text
import { reserve, type Reservation } from './reserve';
export interface InventoryStore {
  load(): Promise<{ readonly stock: unknown; readonly version: number }>;
  compareAndSwap(expectedVersion: number, remaining: number): Promise<boolean>;
}
export type PersistedReservation = Reservation | { readonly kind: 'conflict' };
/** Errors propagate; one attempt, no retries. CAS must be atomic in the adapter. */
export async function reservePersisted(store: InventoryStore, quantity: unknown): Promise<PersistedReservation> {
  throw new Error('not implemented');
}
```

## Independent fixture review

# Handoff fixture review

Scope: `spec.md`, `.scratch/inventory/issues/01-format.md`, `.scratch/inventory/issues/02-reserve.md`, `src/*.ts`, `tests/*.cjs`, `tsconfig.json`, and `evidence/*` in this fixture. Review criteria: the Standards and Spec axes from `skills/engineering/code-review/SKILL.md`, with `skills/engineering/codebase-design/SKILL.md` and `FUNCTIONAL-CONTRACTS.md` as functional-design references. This is a bounded artifact review, not a commit-diff review. Implementer, planner, and other evaluator reports were not read.

## Standards

No findings.

The implementation uses native discriminated outcomes and a small injected store interface. The pure operations validate raw values before performing arithmetic or formatting, without coercion, ambient observations, I/O, or mutation of caller values. Finite integer and range guards establish the numeric invariants at runtime. `unknown` inputs explicitly permit validation at entry; TypeScript does not establish their numeric validity. Invalid raw inputs throw `RangeError`, while admitted-domain insufficient stock and persistence conflict have distinct returned alternatives. Store operational failures propagate. These distinctions are visible in implementation and tests; the functions are total over the specified admitted numeric domains under normal runtime resources, not universally nonthrowing functions over `unknown`.

The signature snapshots in `evidence/01-format-signature.ts.txt`, `08-reserve-signatures.ts.txt`, and `15-persistence-signatures.ts.txt` show types and interfaces with unimplemented bodies. Subsequent logs support a type-first, incremental workflow. The initial formatting failure is a build/output-path problem, followed by an actual behavioral failure against the placeholder implementation. The final source has no loops or recursion requiring a termination argument. Persistence termination remains conditional on store promises settling.

Verification is proportionate: formatting has examples, reservation has generated properties plus rejection and depletion examples, and persistence has separate service-level adapter checks. There is no unsupported demand for property tests merely because formatting is pure. Encapsulated mutation in the test store models persisted state; it does not undermine the pure arithmetic contract. No actionable smell-baseline concern was found.

## Spec

No findings.

The two tickets remain independently implementable: formatting has no reservation dependency, and reservation/persistence has no formatting dependency. Both contain their own numeric and verification contracts. Formatting returns the specified literal suffix, including `1 units`. Reservation validates stock in 0 through 100 and requested quantity in 1 through 100, returns exact subtraction for success, and explicitly rejects insufficient stock. The guards handle nonfinite values, fractions, and range violations, including raw stored stock.

`reservePersisted` loads once, computes the pure result, skips saving on insufficient stock, and passes the loaded version and remaining stock to CAS. It awaits CAS, returns conflict on false, propagates operational errors, and adds no retries or transport-error taxonomy.

The success adapter test uses initial version 42 and verifies remaining stock and version advancement. The racing adapter performs a competing CAS, changing stock from 10 to 9 and version from 7 to 8, before trying the stale expected version. Assertions require conflict and preservation of that competing state. `18-conflict-red.log` records false success being detected; `19-conflict-green.log` records the corrected result. This is actual modeled CAS conflict evidence rather than an unconditional false stub. Other public-service checks cover insufficient stock without save, invalid observations without save, error propagation, and delayed confirmation.

## Evidence limits

The recorded final run reports 11 passing tests. Compiler logs after the initial configuration failure are empty; without captured exit statuses, their contents alone do not independently attest successful compiler execution. Signature snapshots and numbered logs support, but do not independently prove, historical execution order. No new commands compiling or running tests were executed for this read-only review.

The property suite samples 1,000 pairs with a fixed seed; it is not exhaustive proof. Numeric primitives cannot be mutated through argument passing, so the preservation assertion contributes limited evidence beyond source inspection. TypeScript checks declared shapes, not numeric ranges, purity, or adapter correctness; JavaScript test files are outside the TypeScript include set. The service tests exercise an in-memory adapter, not production storage or distributed concurrency. Atomic CAS semantics, a trustworthy version protocol, settling store operations, and normal runtime resources remain assumptions. No original store implementation was supplied here to independently verify compatibility or historical operational-failure conventions.

Summary: Standards 0 findings; Spec 0 findings. No actionable issue found within the reviewed scope.

## Subsequent policy finding

This initial run passed its artifact checks but exposed an ambiguity in the broader totality policy. Raw-input functions accepted `unknown` and threw expected validation errors without a declared rejection outcome or justified partiality. The reference and human docs were clarified in commit `4565d33`, and a fresh-context rerun uses the unchanged planning artifacts. This initial report is retained as evidence of the issue, not as a final pass for raw-input totality.
