## What it does

`tdd` builds a feature or fixes a bug test-first: one failing test, then just enough code to pass it, then the next behaviour. It carries the standards that make that loop produce tests worth keeping: what a good test is, where tests go, what mocks are for, and the three anti-patterns that make a suite worthless.

It writes no test at a seam you have not agreed to first. It reuses seams already agreed in the conversation or spec and asks you to confirm only new or changed ones, explaining what each catches and misses. Testing effort is finite, and this step spends it on the critical paths instead of on every edge case. `tdd` is also a **reference**, not a driver. It contains the rules of the loop, and something else (you, or [implement](https://aihero.dev/skills-implement)) runs the [session](https://www.aihero.dev/ai-coding-dictionary/session) that applies them.

## When to reach for it

Type `/tdd`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically when a task fits: building a feature or fixing a bug test-first, when you request integration or property-based tests, or when you say "red-green-refactor".

Reach for it when there is a concrete behaviour to build, with an input and an observable output, and you want tests that survive a refactor.

| Your situation | Where to go |
| --- | --- |
| A behaviour with defined inputs and outputs (business logic, a request/response contract, a transformation, validation) | `tdd` |
| The behaviour isn't pinned down yet | [to-spec](https://aihero.dev/skills-to-spec), which also agrees the test seams before any code is written |
| The question is really the shape of the interface, not the tests | [codebase-design](https://aihero.dev/skills-codebase-design) |
| You have a [spec](https://www.aihero.dev/ai-coding-dictionary/spec) or [tickets](https://www.aihero.dev/ai-coding-dictionary/ticket) and want the whole build run for you | [implement](https://aihero.dev/skills-implement), which drives `tdd` per ticket |
| Config, wiring, glue, type annotations, straight CRUD delegation | Choose a focused test only if it adds independent behavioral evidence |

Choose tests for the behavior and risk:

| Evidence needed | Useful choice |
| --- | --- |
| A concrete scenario or simple function | A focused example-based test |
| A meaningful law across varied inputs | A property, with suitable generators and independent assertions |
| Effects or collaboration | Integration coverage at the relevant interface |
| Behavior already covered adequately | Explain that evidence instead of adding a redundant test |

Unit versus integration describes scope; example versus property describes style. A property-based test can be a unit test, and a simple example-based unit test can be the best choice.

## Prerequisites

[codebase-design](https://aihero.dev/skills-codebase-design) needs to be installed. `tdd` used to carry its own deep-module and interface-design notes; v1.0 deleted them in favour of the shared skill, and `tdd` now uses its interface-design vocabulary. Nothing else; the skill is [stateless](https://www.aihero.dev/ai-coding-dictionary/stateless) and writes no files of its own.

## The loop, and the seam it runs at

The skill rests on three terms.

**Red-green.** Establish the smallest useful types and signature for the current behavior, then write an example or property and watch it fail for that missing behavior before implementing it. Typechecking verifies type contracts; behavior needs its own evidence. Do not write code for the test after next. There is no refactor phase. The skill dropped it in June 2026 because agents almost never performed it, and because review and implementation work better as separate sessions. Refactoring belongs to [code-review](https://aihero.dev/skills-code-review).

**Vertical slice.** Develop types, one example or property, and the minimal implementation for one behavior at an agreed seam, then repeat. A property can exercise many inputs within that slice. The first cycle is a **tracer bullet** that proves a single path end to end. The opposite is horizontal slicing: all the tests first, then all the code. Tests written in bulk verify *imagined* behaviour. They check the shape of things rather than what a user does, and they commit you to a test structure before you understand the implementation.

**Pre-agreed seam.** A seam is the public boundary you observe behaviour at without reaching inside. The rule has no exceptions. No test goes at an unconfirmed seam. In the full chain the seams are agreed earlier, during [to-spec](https://aihero.dev/skills-to-spec): "`/tdd` is told to only work at pre-agreed test seams, `/code-review` checks that only agreed-upon test seams were used." Invoked on its own, `tdd` asks you about new seams. Existing agreement carries forward.

The three anti-patterns it is written to prevent:

| Anti-pattern | The tell |
| --- | --- |
| Implementation-coupled | The test breaks when you rename an internal function, though behaviour did not change. Mocked internal collaborators, asserted call counts, database queries used to verify instead of the interface. |
| Uninformative oracle | The assertion derives from the result without an independent constraint, or copies an algorithm and risks sharing its mistakes. Expectations need an independent example, law, or simpler model. |
| Horizontal slicing | A batch of tests landed before any implementation. |

Mocks are for system boundaries only: external APIs, time, randomness, sometimes the filesystem or the database. Never mock your own modules.

## Common questions

**Does using properties mean replacing example-based unit tests?**

No. Use a property when a meaningful law across many inputs adds useful evidence. Keep clear examples for small functions, concrete scenarios, and important regressions. Generated failures need replayable counterexamples that preserve the original contract violation. A passing run supplies sampled evidence, not a proof of totality or purity.

**Why doesn't it refactor? The description says "red-green-refactor".**

Because the refactor step was removed and the description was not. The removal was deliberate. Agents almost never did the step, and keeping implementation and review in separate sessions works better. Whether the result still counts as TDD by the book matters less than whether the loop produces better code. The mismatch between the trigger phrase and the body is filed as [issue #589](https://github.com/mattpocock/skills/issues/589) and is still open, so "red-green-refactor" continues to work as a phrase that fires the skill. What you get is red-green, with refactoring in [code-review](https://aihero.dev/skills-code-review).

**It asked me to choose a test seam and I had no idea which to pick.**

Seam selection has caused confusion ([issue #607](https://github.com/mattpocock/skills/issues/607)). This version explains what each proposed seam catches and misses. Public domain interfaces can carry fast examples and properties; integration interfaces cover effects and collaboration. Useful domain coverage stays when integration coverage is added.

**It wrote the implementation before the test, even though the skill says red first.**

It happens. One user pushed the [model](https://www.aihero.dev/ai-coding-dictionary/model) on it and got an unusually honest answer: "I knew the skill said 'one test at a time, watch it fail for the right reason'. I read it. I just defaulted to my normal habit." The skill accepts this. No instruction makes an agent comply 100% of the time, and stricter wording restricts the agent's creativity for little gain. The loop is worth running even when the agent does not follow it strictly, because the results are still better overall. If strict adherence matters for a particular slice, watch the run rather than trusting the skill to enforce it.

**Should it write browser or end-to-end tests first?**

Usually not, and the skill will not stop it. A user reported the agent writing a Playwright test first, then spending a long loop re-running it and concluding the *test* was broken for a feature that did not exist yet. Browser tests are slow enough that the red-green feedback loop stops paying for itself. State in your repo's `CLAUDE.md` that browser tests come after the behaviour works.

**Does `/tdd` replace `/implement`, or the course's `/do-work`?**

No. `/tdd` documents the methodology; `/implement` is a simple work→feedback→commit loop and is the direct stand-in for `/do-work`. The course's single `/do-work` step is now split across `/implement`, `/tdd` and `/code-review`. If you are asking which one to run against a ticket, the answer is almost always `/implement`.

**Where did the deep-modules and interface-design guidance go?**

Into [codebase-design](https://aihero.dev/skills-codebase-design) in v1.0, generalised so several skills share one vocabulary. `refactoring.md` left at the same time; refactoring is now [code-review](https://aihero.dev/skills-code-review)'s job, and that skill carries the Fowler smell baseline.

**Does it know about my other tickets?**

No. Run against one ticket, it can propose work that belongs to a sibling ticket, because it has no view of the rest of the issue graph ([issue #129](https://github.com/mattpocock/skills/issues/129)). This is not `tdd`'s job. Passing the spec alongside the ticket helps; right-sizing the tickets in the first place helps more.

## It's working if

- It reuses agreed seams and explains the trade-offs before asking you to confirm a new one.
- One test appears, goes red, gets just enough code to pass, and only then does the next test appear, not a batch of tests followed by a batch of code.
- Test names read as capabilities ("user can checkout with valid cart"), not as internals ("checkout calls paymentService.process").
- Examples, laws, and reference models have expectations you can trace to the contract.
- Generated failures include a small counterexample and a replay that demonstrates the same failure.
- A simple function gets a focused example or a reason its existing coverage is sufficient.
- Renaming an internal function breaks nothing in the suite.
- Mocks appear only at external boundaries (the payment API, the clock) and never around your own modules.

## Where it fits

`tdd` runs inside the build step of the main chain; it is not a step of its own:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review → retro
```

[to-spec](https://aihero.dev/skills-to-spec) agrees the test seams up front, [implement](https://aihero.dev/skills-implement) drives `tdd` per ticket, and [code-review](https://aihero.dev/skills-code-review) checks afterwards that only the agreed seams were used, and owns the refactoring `tdd` no longer does. Its other neighbour is [codebase-design](https://aihero.dev/skills-codebase-design), the shared source of the seam and deep-module vocabulary that `tdd` uses. You can also reach for it on its own, whenever there is a concrete behaviour to build and no full spec in play. When you are unsure which skill fits your situation, [ask-matt](https://aihero.dev/skills-ask-matt) routes you.
