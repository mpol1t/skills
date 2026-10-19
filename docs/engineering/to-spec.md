## What it does

`to-spec` turns the conversation you have just had into a **[spec](https://www.aihero.dev/ai-coding-dictionary/spec)**. A draft request stays local for iteration; otherwise it publishes to your configured issue tracker as a single issue. Producing or agreeing a spec does not start implementation.

It does not interview you. When you reach for it, the deciding is already done. So it synthesises what is known (from the thread, the codebase, your `GLOSSARY.md` and ADRs) and does not start a new round of questions. The spec records decisions you already made. It is not a place to make new ones.

## When to reach for it

You invoke this by typing `/to-spec`; the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) won't reach for it on its own.

Reach for it when the build is too big for one agent [session](https://www.aihero.dev/ai-coding-dictionary/session) and must be split across several. That is the whole trigger:

| Where you are | What to run |
| --- | --- |
| You haven't decided anything yet | [grill-with-docs](https://aihero.dev/skills-grill-with-docs) first |
| Decided, and the work fits one [context window](https://www.aihero.dev/ai-coding-dictionary/context-window) | [implement](https://aihero.dev/skills-implement): skip the spec |
| Decided, and the work spans several sessions | `/to-spec`, then [to-tickets](https://aihero.dev/skills-to-tickets) |
| A [wayfinder](https://aihero.dev/skills-wayfinder) map has cleared | `/to-spec #<map_issue>` |

## Prerequisites

For publication, [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) must configure a tracker and the triage-label vocabulary for this repo. The tracker can be a hosted service or local markdown files. Changed domain contracts also use [codebase-design](https://aihero.dev/skills-codebase-design); include it when installing selected skills.

## The spec is a decision record

The spec exists because context windows end. You settled many things while [grilling](https://www.aihero.dev/ai-coding-dictionary/grilling): the shape of the solution, the choices you argued through, and what you deliberately refused. All of that is in one conversation that you are about to clear. The spec keeps it.

So the spec does not validate or decide anything. It records what you decided, in your project's own vocabulary, so a fresh session can pick up the work without you explaining it again. If the spec states something you never said, that is a defect.

## Seams before prose

Before it writes anything, `to-spec` identifies the **seams** where the feature will be tested. It reuses agreements already made and checks new or changed seams with you. Existing interfaces are preferred, with the smallest useful set covering distinct risks: stable domain interfaces for calculations and laws, integration interfaces for effects and orchestration.

The spec preserves admitted inputs, legal transitions, expected failures, invariants, and effect ownership. It distinguishes what types enforce from runtime validation, tests, and assumptions. Testing decisions explain why examples, properties, integration checks, or existing coverage fit the behavior. Trivial behavior stays simple.

Other skills use those agreed seams later. [tdd](https://aihero.dev/skills-tdd) works only at seams you agreed in advance. [code-review](https://aihero.dev/skills-code-review) reviews the diff against the spec, so a seam nobody agreed to shows up as a review finding. Both connections go through this document. That is why you should take the seam conversation seriously here, and not leave it for implementation.

## Common questions

**Does agreeing the spec authorize implementation?**

No. The skill returns the requested artifact and stops. Asking to draft or iterate also keeps it from publishing or applying a ready label. Explicitly invoke an implementation step when you want the build to begin.

**Does every domain function need property-based tests?**

No. The spec records the useful evidence for each contract. A focused example-based unit test can be sufficient; generated cases earn their place when a meaningful law adds coverage.

**Where did `/to-prd` go?**
It is this skill, renamed in v1.1. "Spec" is now the one term used throughout, and the old `to-prd` slug no longer works, so reinstall under the new name. The old vocabulary is replaced by the pair *spec* and *tickets*. The spec is the destination and the decisions that fix it. The [tickets](https://www.aihero.dev/ai-coding-dictionary/ticket) are the steps that get there. If you change direction, delete the unfinished tickets and keep the spec.

**Why does the spec get the `ready-for-agent` label? I don't want an agent implementing off it.**
The label means "no further triage needed": the document is complete enough for an agent to work from. It marks an input, not a work order. But [AFK](https://www.aihero.dev/ai-coding-dictionary/afk) agents that poll for `ready-for-agent` cannot see that difference. They will try to build the whole spec in one run instead of picking up the ticket slices. This is the most-reported problem with the skill. Until it changes, exclude the parent spec explicitly in your AFK agent's prompt, or remove the label after `/to-tickets` has run.

**Why not go straight from grilling to `/to-tickets` and skip the spec?**
Often you should. The spec is worth its step only on multi-session work. Its value is that the tickets are disposable and the spec is not. Each ticket is sized for one fresh context window and then gets deleted or closed, while the spec stays as the one place that records the reasoning behind them. On a single-session change, that gives you nothing, and you pay for an extra synthesis step where the [model](https://www.aihero.dev/ai-coding-dictionary/model) can drift. Go from grilling to `/implement`.

**I just finished a wayfinder map. What do I feed it?**
Give it the main map issue, `/to-spec #<map_issue>`, not the individual decision tickets. [wayfinder](https://aihero.dev/skills-wayfinder) produces decisions spread across a map, not deliverables. `to-spec` collapses them into one document you can build from. If you loop the map straight into `/implement`, you lose that step.

**Is the spec for me to review, or is it just for the agent?**
Mostly for the agent, and it reads that way: complete, dense, and full of references. Read the seams and the out-of-scope section. In those two places, a wrong decision is cheapest to catch now and most expensive to find later. People do complain about reading the whole thing, and there is no summary mode. But if the spec surprises you, the grilling was too shallow; the spec is not too long.

**Do I keep the spec frozen once tickets start, or let the agent rewrite it?**
Nothing keeps it in sync. In practice it is a snapshot of what you knew at that moment, and it goes out of date the first time implementation teaches you something. Treat it as disposable after the work ships. Your `GLOSSARY.md` and ADRs are the files meant to last. If you learn something during implementation that should last, put it there, not in an edited spec.

**My work is a refactor or a module boundary, not a feature. Does the template fit?**
Less well, and this is a known limitation. The template relies heavily on user stories, which do not fit architectural work. You end up writing stories nobody asked for around decisions that are really about interfaces and invariants. Use the implementation-decisions and testing-decisions sections instead. Record the lasting architectural decisions as ADRs through [grill-with-docs](https://aihero.dev/skills-grill-with-docs), not in the spec.

**Will it check the tracker for related work, or cite the ADRs it's respecting?**
No to both. It reads and follows the ADRs for the area it touches, but it does not link them. It also does not search the tracker for overlapping issues before it writes, so a spec can duplicate work that someone already filed, and nothing warns you. If the area is busy, search the tracker yourself first.

**`/to-tickets` couldn't read my spec: it kept truncating.**
A tracker issue may not return a very large spec in full, and there is no local copy to use instead. To fix this, do not [clear](https://www.aihero.dev/ai-coding-dictionary/clearing) or [compact](https://www.aihero.dev/ai-coding-dictionary/compaction) between `/to-spec` and `/to-tickets`. Run them in the same window, and `/to-tickets` never has to fetch the spec again.

## It's working if

- It starts writing instead of asking you a new round of questions.
- It reuses agreed seams and explains the distinct risk covered by each new one.
- Its contracts and test choices are clear enough for a fresh implementer, including justified example-only choices.
- It uses your project's nouns, not generic product-management boilerplate.
- You remember making every decision in it. It invented nothing to fill a section.
- The out-of-scope section lists real things. The things you refused are usually the most useful lines on the page.

## Where it fits

`to-spec` is a step in the main build chain, but only on the multi-session branch of it:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review → retro
```

Upstream, [grill-with-docs](https://aihero.dev/skills-grill-with-docs) makes the decisions that this skill only records, and a finished [wayfinder](https://aihero.dev/skills-wayfinder) map joins the chain here. Downstream, [to-tickets](https://aihero.dev/skills-to-tickets) cuts the spec into tracer-bullet tickets for [implement](https://aihero.dev/skills-implement) to build. When you're unsure which skill or flow fits, [ask-matt](https://aihero.dev/skills-ask-matt) routes you.
