# Behavioral fixture evaluation

Read repository tdd/SKILL.md, tests.md, mocking.md, properties.md; diagnosing-bugs/SKILL.md; codebase-design/SKILL.md and FUNCTIONAL-CONTRACTS.md. No rubric or project spec read. No fixture glossary or ADR exists. The two public seams were already agreed. No external effects or integration collaborators require integration tests or mocks.

formatCount: nonnegative integer number inputs, string output with literal suffix ` items`, including singular 1. Focused worked examples suffice; no generators needed. TypeScript number does not validate integer/nonnegative input, which is a caller precondition. Decimal means no exponential notation, including large representable integers. Invalid inputs are outside this task. Compilation establishes signature compatibility only.

sortNumbers: bounded integer arrays, output nondecreasing, multiplicities preserved, caller input unchanged. Independent frequency counts, adjacent ordering, and before/after snapshot are useful properties; idempotence alone admits constant empty output. Bounded fast-check generation adds evidence across negatives, duplicates, and mixed lengths. No proof of universal correctness is claimed.

Every command below ran from this directory. Source snapshots preserve intermediate behavior. Node v18.20.4; TypeScript 7.0.2; fast-check 4.10.2. Run counts 100 for baseline and 200 for contract, integer range [-100,100], maximum length 30, seed 20261019.

Command: `node ../node_modules/typescript/bin/tsc format.ts --strict --target es2020 --module commonjs --outDir dist && node format.test.cjs`

```text
/tmp/functional-skills.ECtJb0/evaluation/testing/dist/format.js:5
    throw new Error('not implemented');
    ^

Error: not implemented
    at formatCount (/tmp/functional-skills.ECtJb0/evaluation/testing/dist/format.js:5:11)
    at Object.<anonymous> (/tmp/functional-skills.ECtJb0/evaluation/testing/format.test.cjs:3:14)
    at Module._compile (node:internal/modules/cjs/loader:1364:14)
    at Module._extensions..js (node:internal/modules/cjs/loader:1422:10)
    at Module.load (node:internal/modules/cjs/loader:1203:32)
    at Module._load (node:internal/modules/cjs/loader:1019:12)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:128:12)
    at node:internal/main/run_main_module:28:49

Node.js v18.20.4

Exit: 1
```

Command: `node ../node_modules/typescript/bin/tsc format.ts --strict --target es2020 --module commonjs --outDir dist && node format.test.cjs`

```text
formatCount singular suffix passes

Exit: 0
```

Command: `node ../node_modules/typescript/bin/tsc format.ts --strict --target es2020 --module commonjs --outDir dist && node format.test.cjs`

```text
formatCount singular suffix passes
node:assert:125
  throw new AssertionError(obj);
  ^

AssertionError [ERR_ASSERTION]: Expected values to be strictly equal:
+ actual - expected

+ '1e+21 items'
- '1000000000000000000000 items'
    at Object.<anonymous> (/tmp/functional-skills.ECtJb0/evaluation/testing/format.test.cjs:7:8)
    at Module._compile (node:internal/modules/cjs/loader:1364:14)
    at Module._extensions..js (node:internal/modules/cjs/loader:1422:10)
    at Module.load (node:internal/modules/cjs/loader:1203:32)
    at Module._load (node:internal/modules/cjs/loader:1019:12)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:128:12)
    at node:internal/main/run_main_module:28:49 {
  generatedMessage: true,
  code: 'ERR_ASSERTION',
  actual: '1e+21 items',
  expected: '1000000000000000000000 items',
  operator: 'strictEqual'
}

Node.js v18.20.4

Exit: 1
```

Command: `node ../node_modules/typescript/bin/tsc format.ts --strict --target es2020 --module commonjs --outDir dist && node format.test.cjs`

```text
formatCount singular suffix passes
formatCount decimal and boundary examples pass

Exit: 0
```

Command: `node ../node_modules/typescript/bin/tsc sort.ts sort.defective.ts --strict --target es2020 --module commonjs --outDir dist && node sort.test.cjs baseline`

```text
Idempotence passes, even for defective implementation

Exit: 0
```

Command: `node sort.test.cjs contract`

```text
{
  "failed": true,
  "seed": 20261019,
  "counterexamplePath": "1:1:0:0:1",
  "counterexample": [
    [
      0
    ]
  ],
  "numRuns": 2,
  "numShrinks": 4,
  "failures": [
    [
      [
        29,
        97,
        87,
        -86,
        6,
        -58,
        -60
      ]
    ],
    [
      [
        -86,
        6,
        -58,
        -60
      ]
    ],
    [
      [
        -58,
        -60
      ]
    ],
    [
      [
        -60
      ]
    ],
    [
      [
        0
      ]
    ]
  ],
  "error": "elements and multiplicities must survive"
}

Exit: 1
```

Command: `node sort.test.cjs replay --defective`

```text
{
  "failed": true,
  "seed": 20261019,
  "counterexamplePath": "1:1:0:0:1",
  "counterexample": [
    [
      0
    ]
  ],
  "numRuns": 1,
  "numShrinks": 0,
  "failures": [
    [
      [
        0
      ]
    ]
  ],
  "error": "elements and multiplicities must survive"
}

Exit: 1
```

Diagnosis checkpoint before probing: (1) unconditional empty-result placeholder predicts every nonempty array loses its values; (2) filtering predicts loss depends on values, so [1] may survive while [0] fails; (3) input mutation predicts the caller's array changes. These ranked hypotheses were communicated before the probe. No interview was needed. The minimized [0] retains the essential nonempty feature; deleting its only element gives [], which passes. This is a useful minimal repro, not a claim that shrinking proves global minimality.

Command: `cat sort.ts && node -e 'const {sortNumbers}=require("./dist/sort.js");for(const xs of [[0],[1],[]]) console.log(JSON.stringify({before:xs.slice(),out:sortNumbers(xs),after:xs}));'`

```text
export function sortNumbers(xs: readonly number[]): number[] {
  return [];
}
{"before":[0],"out":[],"after":[0]}
{"before":[1],"out":[],"after":[1]}
{"before":[],"out":[],"after":[]}

Exit: 0
```

Command: `node sort.test.cjs regression`

```text
node:assert:125
  throw new AssertionError(obj);
  ^

AssertionError [ERR_ASSERTION]: elements and multiplicities must survive
    at contract (/tmp/functional-skills.ECtJb0/evaluation/testing/sort.test.cjs:16:10)
    at Object.<anonymous> (/tmp/functional-skills.ECtJb0/evaluation/testing/sort.test.cjs:24:3)
    at Module._compile (node:internal/modules/cjs/loader:1364:14)
    at Module._extensions..js (node:internal/modules/cjs/loader:1422:10)
    at Module.load (node:internal/modules/cjs/loader:1203:32)
    at Module._load (node:internal/modules/cjs/loader:1019:12)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:128:12)
    at node:internal/main/run_main_module:28:49 {
  generatedMessage: false,
  code: 'ERR_ASSERTION',
  actual: Map(0) {},
  expected: Map(1) { 0 => 1 },
  operator: 'deepStrictEqual'
}

Node.js v18.20.4

Exit: 1
```

Command: `node ../node_modules/typescript/bin/tsc format.ts sort.ts sort.defective.ts --strict --target es2020 --module commonjs --outDir dist && node format.test.cjs && node sort.test.cjs regression && node sort.test.cjs contract && node sort.test.cjs replay`

```text
formatCount singular suffix passes
formatCount decimal and boundary examples pass
Regression and explicit boundary examples pass
{
  "failed": false,
  "seed": 20261019,
  "counterexamplePath": null,
  "counterexample": null,
  "numRuns": 200,
  "numShrinks": 0,
  "failures": []
}
{
  "failed": false,
  "seed": 20261019,
  "counterexamplePath": null,
  "counterexample": null,
  "numRuns": 6,
  "numShrinks": 0,
  "failures": []
}

Exit: 0
```

Command: `node sort.test.cjs replay --defective`

```text
{
  "failed": true,
  "seed": 20261019,
  "counterexamplePath": "1:1:0:0:1",
  "counterexample": [
    [
      0
    ]
  ],
  "numRuns": 1,
  "numShrinks": 0,
  "failures": [
    [
      [
        0
      ]
    ]
  ],
  "error": "elements and multiplicities must survive"
}

Exit: 1
```

Root cause: the unconditional return [] discards all input. Idempotence compares two empty results and is satisfied by this wrong implementation. Direct probing showed all nonempty inputs disappear while caller arrays remain intact, ruling out mutation and value-selective filtering for this fixture.

Fix: numerically sort a copy. Local mutation of the fresh copy is justified by the native sort operation; no caller-owned alias is mutated. A readonly input annotation adds compile-time protection in the body, while before/after checks provide runtime evidence. The numeric comparator avoids lexical ordering mistakes. Finite arrays and bounded finite integers ensure the comparator is defined; termination relies on the runtime sort implementation and ordinary resource availability. No external state or effects are involved.

The original seeded exploration was rerun after fixing and passes, as do the exact replay and readable regression. Defective replay still fails with the same multiplicity violation. Generated checks provide sampled evidence over the stated domain. No debug logs were added to production files. Defective and intermediate sources are intentionally retained as evaluation artifacts, not production code.

Formatting used two vertical cycles: first the literal suffix for 1, then decimal representation including 1e21. The intermediate String implementation exposed exponential notation; BigInt conversion formats the represented integer exactly. The contract cannot restore precision already lost before a number is supplied. No rejection behavior for invalid-domain values was invented.

An initial attempt to invoke `python runlog.py ...` failed because `python` is absent (`/bin/bash: python: command not found`, exit 127). All captured test invocations use python3. runlog.py captures exact executed test commands, combined stdout/stderr, and exit codes; its own exit code is deliberately zero so expected red phases can be recorded.

## format.initial.ts

```
export function formatCount(n: number): string {
  throw new Error('not implemented');
}

```

## format.intermediate.ts

```
export function formatCount(n: number): string {
  return String(n) + ' items';
}

```

## format.ts

```
export function formatCount(n: number): string {
  return BigInt(n).toString() + ' items';
}

```

## format.test.cjs

```
const assert = require('node:assert/strict');
const {formatCount} = require('./dist/format.js');
assert.equal(formatCount(1), '1 items');
console.log('formatCount singular suffix passes');
assert.equal(formatCount(0), '0 items');
assert.equal(formatCount(42), '42 items');
assert.equal(formatCount(1e21), '1000000000000000000000 items');
console.log('formatCount decimal and boundary examples pass');

```

## sort.defective.ts

```
export function sortNumbers(xs: readonly number[]): number[] {
  return [];
}

```

## sort.ts

```
export function sortNumbers(xs: readonly number[]): number[] {
  return [...xs].sort((a, b) => a - b);
}

```

## sort.test.cjs

```
const assert = require('node:assert/strict');
const fs = require('node:fs');
const fc = require('fast-check');
const mode = process.argv[2] || 'contract';
const defective = process.argv.includes('--defective');
const {sortNumbers} = require(defective ? './dist/sort.defective.js' : './dist/sort.js');
const arb = fc.array(fc.integer({min:-100,max:100}), {maxLength:30});
const freq = xs => {
  const counts = new Map();
  for (const x of xs) counts.set(x,(counts.get(x)||0)+1);
  return counts;
};
function contract(xs) {
  const before = xs.slice();
  const ys = sortNumbers(xs);
  assert.deepEqual(freq(ys), freq(before), 'elements and multiplicities must survive');
  for(let i=1;i<ys.length;i++) assert.ok(ys[i-1]<=ys[i], 'output nondecreasing');
  assert.deepEqual(xs,before,'input unchanged');
}
if(mode === 'baseline') {
  fc.assert(fc.property(arb, xs => assert.deepEqual(sortNumbers(sortNumbers(xs)),sortNumbers(xs))), {seed:20261019,numRuns:100});
  console.log('Idempotence passes, even for defective implementation');
} else if(mode === 'regression') {
  contract([0]);
  contract([]);
  contract([10,2,2,-1]);
  console.log('Regression and explicit boundary examples pass');
} else {
  let opts = {seed:20261019,numRuns:200,verbose:2};
  if(mode === 'replay') {
    const saved = JSON.parse(fs.readFileSync('failure.json','utf8'));
    opts = {...opts, seed:saved.seed, path:saved.counterexamplePath};
  }
  const result = fc.check(fc.property(arb,contract),opts);
  const detail = {failed:result.failed,seed:result.seed,counterexamplePath:result.counterexamplePath,counterexample:result.counterexample,numRuns:result.numRuns,numShrinks:result.numShrinks,failures:result.failures,error:result.errorInstance?.message};
  console.log(JSON.stringify(detail,null,2));
  if(result.failed && mode !== 'replay') fs.writeFileSync('failure.json',JSON.stringify(detail,null,2));
  process.exitCode = result.failed ? 1 : 0;
}

```

## failure.json

```
{
  "failed": true,
  "seed": 20261019,
  "counterexamplePath": "1:1:0:0:1",
  "counterexample": [
    [
      0
    ]
  ],
  "numRuns": 2,
  "numShrinks": 4,
  "failures": [
    [
      [
        29,
        97,
        87,
        -86,
        6,
        -58,
        -60
      ]
    ],
    [
      [
        -86,
        6,
        -58,
        -60
      ]
    ],
    [
      [
        -58,
        -60
      ]
    ],
    [
      [
        -60
      ]
    ],
    [
      [
        0
      ]
    ]
  ],
  "error": "elements and multiplicities must survive"
}
```

Command: `node -e 'const fc=require("fast-check");const xs=fc.sample(fc.array(fc.integer({min:-100,max:100}),{maxLength:30}),{seed:20261019,numRuns:200}); console.log(JSON.stringify({sample:xs.slice(0,4),empty:xs.filter(x=>!x.length).length,singleton:xs.filter(x=>x.length===1).length,duplicates:xs.filter(x=>new Set(x).size<x.length).length,negative:xs.filter(x=>x.some(n=>n<0)).length,total:xs.length},null,2));'`

```text
{
  "sample": [
    [],
    [
      29,
      97,
      87,
      -86,
      6,
      -58,
      -60
    ],
    [
      -37,
      14
    ],
    [
      3,
      23,
      -2,
      -13,
      -1,
      -16
    ]
  ],
  "empty": 19,
  "singleton": 23,
  "duplicates": 17,
  "negative": 161,
  "total": 200
}

Exit: 0
```
