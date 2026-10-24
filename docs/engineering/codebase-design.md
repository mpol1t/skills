## What it does

`codebase-design` supplies a shared vocabulary for **deep modules** and functional contracts. It is a reference applied to the current design question, so invoking it alone does not authorize a new architecture project.

For consequential plans, specs, or ticket graphs, it also supplies independent adversarial review. The invoking agent selects expertise, available models, and context deliberately, then resolves supported objections rather than collecting votes.

A small interface is useful when it reduces what callers must understand. The reference also makes inputs, valid states, outcomes, and effects explicit so callers can reason about composition. It uses language-neutral defaults and project-native mechanisms.

## When to reach for it

Type `/codebase-design`, or the agent reaches for it automatically when a design task fits.

| Your question | Where to start |
| --- | --- |
| How should a module expose its domain types, behavior, or effects? | `codebase-design` |
| Which part of the codebase needs redesigning? | [improve-codebase-architecture](improve-codebase-architecture.md) |
| What does a domain term mean, and which states are possible? | [domain-modeling](domain-modeling.md) |
| Which examples, properties, and integration checks provide useful evidence? | [tdd](tdd.md) |

## Depth and functional contracts

A **module** has an **interface**, everything a caller must know to use it, and an **implementation**. **Depth** means useful behavior for the amount of interface a caller must learn. A **seam** is where that interface lives; an **adapter** satisfies it. **Leverage** is the benefit to callers, and **locality** keeps changes and verification concentrated.

The deletion test asks whether removing a module eliminates complexity or pushes it back into callers. Small pure functions can earn their place through clear domain contracts and useful composition. Method count and implementation size do not determine their value.

Functional contracts make the admitted input domain, outputs, expected failures, invariants, and effects visible for the behavior being changed. Types and signatures develop one behavior slice at a time. Static enforcement, runtime validation, and remaining assumptions stay distinct. Total domain functions are the default: admitted inputs terminate with a defined outcome within stated execution assumptions.

Pure domain calculations use explicit observations. Effects have execution contracts, including ordering and retry behavior where relevant. Deepening preserves useful domain laws alongside integration evidence; fewer modules do not justify discarding distinct tests.

## Independent challenge

The orchestrator gives specialists different questions and lets them assess independently before sharing their conclusions. It preserves the requirements and evidence in each brief while withholding its preferred answer where possible. A focused challenge round tests disputed assumptions and counterexamples. Further rounds earn their cost through new evidence.

Consensus is optional. Material objections need evidence or an explicit tradeoff; unresolved human choices return to you. The technique is selective, so a straightforward design does not require a cohort.

## Common questions

**Does the agent need this repository to use an installed skill?**

No. Runtime instructions come from installed skill entry points and their bundled supporting files. Dependencies are located through the harness loader or skill catalog; fresh agents receive resolved installed paths. These docs links are for navigation in the fork, not runtime dependencies.


**Does independent review require different models?**

The orchestrator chooses among the models the environment exposes. Diversity can be useful, but it does not guarantee independent mistakes. Distinct questions, independent first passes, and source checks matter too. With one available model, fresh agents can still assess independently, with that diversity limitation stated. When delegation is unavailable, the agent reports the limitation and performs local checks without claiming an independent review.

**Does functional programming rule out local mutation?**

Immutable data is the default. Private mutation is acceptable when it improves clarity or measured performance and cannot escape, alter caller-owned data, or change the observable contract. The agent should explain that choice. Immutable syntax alone does not establish purity.

**Does an explicit result type make a function total?**

No. It makes expected outcomes visible, but unchecked operations or divergence can remain. The agent examines partial operations and termination arguments where relevant, and states justified remaining assumptions. Ordinary compiler success is not a termination proof.

**Can a raw-input validator throw and still count as total?**

Expected malformed inputs should produce a returned rejection. A broad input type and a comment listing valid values do not establish an enforced narrower domain. Throwing for that expected failure needs an explicit partiality rationale and caller handling; the interface should not be called total. A simple rejection variant can be sufficient without separate checked types or a framework.

**Must a seam have two adapters?**

No. Variation is one reason for a seam; effect isolation or protection of a domain invariant can justify one production adapter. The purpose must be concrete, so the rule does not license speculative abstraction.

**Will it prescribe a TypeScript package layout or an effects library?**

No. The reference addresses the contract and what callers can observe. Use the project's module controls and language features to enforce the design. Additional type machinery or an effects library must solve a concrete problem.

**Where did `design-an-interface` go?**

Its interface-design guidance lives here. When exploring alternatives is useful, the supporting design-it-twice technique compares different interfaces on depth, locality, composition, and effect visibility. It is not a reason to restart a settled design.

## It's working if

- You can explain a proposed module's purpose and what complexity it removes from callers.
- The design states valid inputs, failure cases, and effects, not just a short signature.
- A composition checks that each intermediate result meets the next operation's contract.
- The agent distinguishes what the compiler enforces from runtime checks and assumptions.
- Useful domain laws survive a refactor alongside checks of effects and orchestration.
- A challenged decision records the supporting evidence and any substantive dissent, rather than reporting agreement alone.
- A simple operation stays simple instead of acquiring speculative types or abstractions.

## Where it fits

`codebase-design` is a **reach-for-it-anytime standalone** reference underneath the engineering flow. [domain-modeling](domain-modeling.md) supplies the domain meanings; [tdd](tdd.md) supplies the verification loop. Skills consuming these references require the corresponding installed skills. [ask-matt](ask-matt.md) maps the whole set.
