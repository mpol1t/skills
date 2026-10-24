## What it does

`code-review` reviews committed changes between a fixed point you name and a pinned candidate commit along two axes. Both endpoints resolve to immutable commit IDs before reviewers start. **Standards** asks whether the code follows how this repo writes code. **Spec** asks whether the code does what the originating issue or [spec](https://www.aihero.dev/ai-coding-dictionary/spec) asked for. Each axis runs in its own [sub-agent](https://www.aihero.dev/ai-coding-dictionary/subagent) so neither sees the other's reasoning.

The skill never merges or re-ranks the two axes. The report ends with a worst issue *per axis* and declines to name a single winner across them. A change can pass one axis and fail the other. Code that follows every convention but implements the wrong thing passes Standards and fails Spec. Code that does exactly what the [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) asked but breaks the repo's conventions does the reverse. A blended verdict lets the passing axis hide the failing one.

## When to reach for it

Type `/code-review`, or the agent reaches for it automatically when you ask to review a branch, a PR, work in progress, or anything "since X".

| Your situation | Reach for |
| --- | --- |
| A diff exists and you want to know if it is built right *and* is the right thing | `code-review` |
| You want bugs hunted in the diff: null paths, races, off-by-one | Claude Code's own built-in review, not this one (see the name clash below) |
| Nothing is written yet and you want it written test-first | [tdd](https://aihero.dev/skills-tdd) |
| A ticket needs building, review included | [implement](https://aihero.dev/skills-implement), which calls this skill itself |
| A whole ticket graph needs building and review | [implement-spec](https://aihero.dev/skills-implement-spec) |
| The whole codebase has drifted, not one diff | [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) |
| Something is broken and you do not know why | [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) |

Supply the fixed point and, when reviewing an earlier checkpoint, its candidate commit. The current committed tip is the default candidate. Before reviewers start, the skill resolves both endpoints and checks the diff. Review results belong to those commits; later edits need their own verification.

## Prerequisites

The Standards axis needs no existing standards file. Reviewing changed domain contracts also requires [codebase-design](https://aihero.dev/skills-codebase-design) to be available, including with a selective installation. It reads whatever the repo documents (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, and the like) and falls back on a built-in baseline when the repo documents nothing.

The Spec axis needs a spec or ticket to exist and be findable. An explicitly supplied source and scope define the review; otherwise it looks for the originating source:

1. Issue references in the commit messages, fetched through the configured tracker.
2. A matching spec file under `docs/`, `specs/`, or `.scratch/`.
3. Asking you.

Issue lookup depends on the tracker doc, which [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) writes. Without it the axis still works if you hand it a path. With no spec at all, the skill skips the Spec sub-agent and the report says "no spec available" rather than inventing requirements.

## The two axes

| | Standards | Spec |
| --- | --- | --- |
| Question | Is it built right? | Is it the right thing? |
| Reads | The repo's documented standards, the smell baseline, and applicable functional-contract guidance | The originating issue or spec |
| Reports | Documented breaches (can be hard), smells and functional-design recommendations (judgement calls) | Missing or partial requirements, scope creep, requirements implemented wrongly |
| Every finding cites | The standards rule, named smell, or functional-contract guidance, plus the affected hunk | The line of the spec |

This design exists to avoid a generic review skill that does not know your standards. Such a skill flags what is deliberate in your codebase and misses the invariants your codebase depends on. So the repo's own documentation is the [primary source](https://www.aihero.dev/ai-coding-dictionary/primary-source) on the Standards axis, and **the repo always overrides**.

The **smell baseline** sits under the repo's standards. It adapts twelve code smells from chapter 3 of Fowler's _Refactoring_: Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest. Each is a labelled heuristic ("possible Feature Envy"), never a hard violation. Each states what the smell is and how to fix it, so a finding comes with a fix attached rather than only a complaint. Pure transformations, exhaustive matches for distinct operations, and composition pipelines can be sound designs. The adapted remedies target representation coupling and duplicated decisions. Both axes skip anything your linter already enforces.

Changes to domain types, functions, transitions, or their tests also bring in `codebase-design`. The Standards reviewer checks admitted inputs, totality assumptions, expected errors, invariant enforcement, composition, and observable effects. Repository rules still take precedence. Functional-design recommendations remain judgement calls unless a documented standard establishes the requirement.

## Common questions

**Will it push functional code toward classes or demand property tests for every function?**

No. A pure function over domain data, an exhaustive match, or a composition pipeline can be the appropriate design. The reviewer checks evidence against the changed contract: examples, unit tests, properties, and integration tests each serve different needs. A trivial function does not need generated tests merely to satisfy a preference. Encapsulated mutation is assessed by its observable contract and justification.

**Does passing typechecking establish totality or prove an invariant?**

Only claim what the actual checks establish. The reviewer looks for admitted inputs, termination assumptions, construction and validation rules, and evidence for the remaining obligations. Passing generated cases supports a property within the tested scope; it does not prove the property for every input.


**It collides with Claude Code's own `/code-review`. What do I do?**

This is the most reported problem with the skill, and it is not fixed. Claude Code ships its own `/code-review`, which does something different: it hunts bugs in the diff, where this one checks spec compliance and repo standards. When you install this library, one of them wins, and which one depends on how you installed:

- **Plugin marketplace.** Every skill gets a `mattpocock-skills:` prefix, and the built-in becomes hard to reach at the unqualified name.
- **Plain skills install.** The local file wins, and this skill shadows the built-in.

One answer is to remove Claude Code's built-in skills entirely. That saves a lot of [context](https://www.aihero.dev/ai-coding-dictionary/context), and the collision stops mattering. The shadowing itself is arguably a Claude Code [harness](https://www.aihero.dev/ai-coding-dictionary/harness) bug (a skill author should be free to name a skill anything), so the other answer is to rename the local copy. `npx skills update` undoes an edit to the frontmatter or a renamed directory. The durable workaround users report is to fork the skill to a new name and drop `code-review` from the managed set. Keep a note of the commit you forked from so you can re-sync by hand.

**Its sub-agents keep invoking `/code-review` again and spawn more agents.**

This is a known open bug. Several people have reproduced it, in more than one harness. The Standards and Spec prompts do not forbid delegation, so a sub-agent can find the skill again and fan out again. One report reached more than 50 agents. The fix people have applied on forks is one line appended to both sub-agent briefs: "Do not invoke `/code-review` or spawn additional agents: perform this review directly." Some prefer to handle it at the harness level so every skill inherits the guard. Neither is in the shipped skill yet. If you run this unattended, watch the agent count.

**Should I run it in the same [session](https://www.aihero.dev/ai-coding-dictionary/session) that wrote the code?**

Prefer fresh reviewer contexts. Give reviewers the committed diff, requirements, relevant decisions, repository standards, and verification evidence. They should assess the work before seeing the implementer's explanation or another reviewer's conclusions. The caller can retain working context while the Standards and Spec reviewers assess independently.

**After every ticket, or once at the end?**

They answer different questions. Per-ticket review checks the ticket's acceptance criteria and applicable parent contracts, without treating future tickets as missing work. Final integration review checks the whole spec and cross-ticket effects. `implement-spec` uses both boundaries.

**Can I trust the findings?**

Not without checking. Sub-agent output is a hypothesis, not evidence. One team reported a dozen breaking changes that prose-based reviews had missed. The skill combines the two reports as they are, or lightly cleaned. It does not re-verify each claim against the files, so a finding can cite the wrong location or overstate an impact. Read the citation on each finding before you act on it. The skill requires every finding to carry a citation (a standards rule, a smell plus its hunk, or a spec line), and that is what makes the findings checkable.

**Why does it find new problems every single time I run it?**

A fresh broad pass can keep surfacing different preferences. Separate supported blockers from judgement calls and preserve each finding's ID and disposition. For repairs, use focused re-review: verify the original findings, inspect the complete repair diff, and check affected behavior. Significant scope changes can justify a broader review; repeated disagreement without new evidence should lead to arbitration rather than an endless search for unanimous approval.

**Does it review my uncommitted work?**

No. It reviews committed changes between pinned endpoints. The three-dot form measures from the merge-base and excludes staged and working-tree changes. `implement` now commits a checkpoint before requesting review. Commit repairs as well, then verify the new candidate with focused re-review.

Repair and reconciliation review also compares the previous and new candidate trees directly. This includes removed behavior after a rebase, when a three-dot comparison alone would show only changes since their merge-base. Verification evidence belongs to the committed candidate, with any required local fixtures identified.

## It's working if

- The report identifies the base and candidate commits, and bad references fail before reviewers start.
- The report arrives as two separate blocks under `## Standards` and `## Spec`, not one merged list.
- Every Standards finding names a repository rule, a baseline smell, or applicable functional-contract guidance, with the affected hunk identified; every Spec finding quotes a line of the spec.
- Functional-design findings explain the contract at risk and respect documented repository choices.
- The closing summary gives a worst issue per axis and declines to pick an overall winner.
- With no spec available, the Spec block says so instead of listing requirements it inferred from the code.

## Where it fits

`code-review` is the review step near the tail of the build chain: `grill-with-docs → to-spec → to-tickets → implement → code-review → retro`. It also stands alone on any branch or PR you point it at.

- [implement](https://aihero.dev/skills-implement) is the closest neighbour. It drives the build and calls this skill on committed checkpoints and verifies repairs. [implement-spec](https://aihero.dev/skills-implement-spec) coordinates ticket reviews and a final whole-spec assessment.
- [retro](https://aihero.dev/skills-retro) comes after it and tunes it. When a session shows the review missing a class of mistake, `retro` proposes the check or the `CODING_STANDARDS.md` rule the Standards axis then reads.
- [pr](https://aihero.dev/skills-pr) writes the pull request body once the reviewed work goes up.
- [to-spec](https://aihero.dev/skills-to-spec) and [to-tickets](https://aihero.dev/skills-to-tickets) produce the document the Spec axis checks against, so a vague spec makes that axis vague.
- [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) is the whole-codebase counterpart, because this skill only looks at one diff.

[ask-matt](https://aihero.dev/skills-ask-matt) routes across the whole set when you are unsure which skill the situation wants.
