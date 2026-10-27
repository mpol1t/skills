# Implementation issues in agentic development: research

Research date: 2026-10-27. Status: research record, not an accepted format or implementation contract. This repeats the independent evidence and challenge process used for the [PR-description research](pr-description-agentic-research.md). The earlier PR decisions, including Agent Disclosure, do not automatically apply to issues.

## Findings

The strongest evidence supports making the intended outcome, consequential context and completion conditions recoverable. Coding-agent experiments show that withholding relevant information can reduce task success and that clarification can recover some losses. Human bug-report studies and current vendor guidance identify useful diagnostic information. None of this establishes a universally optimal issue template, mandatory heading order, word count or set of fields.

An issue is interpreted alongside repository state, instructions, tools and accessible discussions. Completeness cannot reasonably mean copying everything an agent could discover. Conversely, code search cannot recover an undocumented product decision. Useful specificity concerns what changes a correct implementation or its verification, not the amount of prose supplied.

Three distinctions matter before discussing format. Intake records a report or request that may still need investigation. Implementation work has a sufficiently understood outcome to act on. Decision or investigation work produces understanding, options or a decision rather than an assumed code change. These are analytical distinctions, not a proposed taxonomy or mandatory workflow.

Acceptance conditions and planned checks are prospective. Observed reproduction results may already exist before implementation, but future validation results do not. A written command or unchecked criterion is not proof that work ran or passed. The issue should not silently become a retrospective PR report.

Sizing remains the user's decision. Bounded work is a recurring recommendation, but the evidence does not establish a universal threshold or authorize automatic decomposition, new scheduling rules or a dependency-management protocol.

## Academic evidence

Dates identify publication or revision, not when historical tasks occurred. Much agent research reuses SWE-bench tasks; multiple papers are not necessarily independent observations of current production agents. Peer review does not make observational findings causal.

| Primary source and status | Relevant finding | Limits |
| --- | --- | --- |
| [Ambig-SWE](https://arxiv.org/html/2502.13069v3), first submitted February 18, 2025; v3 February 21, 2026; ICLR 2026 | Manipulates descriptions of 500 historical Verified issues and compares full information, synthetic reductions and clarification. Interaction recovers substantial lost performance. | Simulated users receive full issues, extra hints and files to modify. Clarification therefore supplies more than the removed prose. Synthetic omission and historical tasks limit transfer to real users. |
| [Asking What Matters](https://arxiv.org/html/2604.14624v1), April 16, 2026 preprint | Uses 1,500 omission variants of the same 500 issues; evaluates 700 for information impact. With a fixed backbone, success falls from 43.8% to 23.7% between full and reduced descriptions. Selective clarification improves question efficiency. | Error information ranks highest in SHAP attribution, but intervals overlap and the authors call the ordering indicative. Attribution is not a causal field ranking. Answerability uses a simulated judge. |
| [What Makes a Good Bug Report?](https://thomas-zimmermann.com/publications/files/bettenburg-tr-2008.pdf), technical report revision March 12, 2008; associated FSE 2008 paper | Survey of 466 respondents and developer ratings of 289 reports identify reproduction steps, stack traces and test cases as useful but often difficult for reporters to provide. | Historical human bug-report evidence. Perceptions and observational ratings do not prove mandatory fields improve resolution or apply equally to features. |
| [Inside Bug Report Templates](https://researchportalplus.anu.edu.au/en/publications/inside-bug-report-templates-an-empirical-study-on-bug-report-temp/), Internetware, July 24, 2024; [DOI](https://doi.org/10.1145/3671016.3671401) | Studies 3,194 projects, 5,987 template commit messages and developer/reporter surveys. Template adoption associates with fewer comments and a higher likelihood of being addressed. | Primary abstract inspected; full paper unavailable in this round. Adoption is nonrandom. Fewer comments and addressed reports do not establish correctness or agent performance. |
| [Evaluating AGENTS.md](https://arxiv.org/html/2602.11988v1), February 12, 2026 preprint | Controlled context-file conditions across four agent/model configurations. Generated context often reduces success and increases cost; human-written files improve three of four agents on AGENTbench. | Repository instructions differ from task descriptions. One completion per task, agent and condition, historical tasks and incomplete quality measures constrain generalization. It does not show all context hurts. |
| [Do Agent Rules Shape or Distort?](https://arxiv.org/html/2604.11088v1), April 13, 2026 preprint | On selectively retained tasks, rule conditions improve observed success; random rules match curated rules, and no degradation appears up to 50 rules. | One agent/model, 58 selected tasks and 35 for ablations. Individual comparisons are not significant; conditions share a baseline. This challenges universal minimalism without proving a general rule benefit. |
| [Specification-Oracle Gaps](https://arxiv.org/html/2610.30635v1), October 22, 2026 preprint | Audits SWE-Milestone and finds tests demanding unstated, non-inferable names or paths in 25 of 98 milestones. Targeted perturbation demonstrates a concrete compilation failure mechanism. | Only five days old at research time. Narrow naming/path/literal audit, not every behavioral ambiguity. Supports fair contracts, not prescribing one implementation. Leaderboard ordering remains robust after exclusions. |
| [Evaluating Software Development Agents](https://arxiv.org/abs/2410.12468), December 27, 2024 revision; SANER 2025 | Observes 4,892 patches from ten agents on 500 Verified tasks. Simpler codebases correlate with greater success; authors suggest decomposition. | Does not compare equivalent work as one issue versus several. Complexity and task difficulty co-vary. No evidence for a maximum file count, duration or issue size. |

The studies support recovering important information more strongly than they support any representation. An evaluation that gives one format richer facts would confound information enrichment with formatting.

Benchmark cleanliness and everyday collaboration also differ. [SWE-Bench+](https://arxiv.org/abs/2410.06992), October 2024, identifies solution leakage and weak tests in a selected set of successful benchmark patches. Sharing an existing patch can be legitimate collaboration while invalidating a test of independent problem-solving. Historical overlap creates contamination risk, not proof of memorization in any particular run.

## Current product guidance

The following are first-party living documentation, accessed October 27, 2026. Unless specified, a stable publication date was not displayed. They document recommendations and product behavior, not controlled comparisons of issue formats.

| Source | Documented guidance or behavior | Interpretation boundary |
| --- | --- | --- |
| [GitHub Copilot task best practices](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results) | Recommends clear problems, acceptance criteria and file directions. Explicitly says semantic search can discover code without exact paths. Treats an assigned issue as a prompt and recommends initially bounded work. | Supports useful task information, not compulsory paths or headings. Current terminology is cloud agent; the former coding-agent URL redirects. |
| [GitLab Developer Flow](https://docs.gitlab.com/user/project/merge_requests/developer/) | Recommends relevant files/discussions, criteria, paths when known, existing-pattern examples and visual context. Repository instructions and execution setup support tests. Workplans can override descriptions. | Workplan-on-assignment and status triggers are listed as introduced in 19.6; do not generalize to earlier deployments. Environment readiness is separate from prose quality. |
| [Linear coding sessions](https://linear.app/docs/coding-sessions) | Recommends contained changes with clear outcomes and constraints. Starts from issue context. Direct implementation requests initiate coding; investigation, research and planning requests are treated as scoping. | This authorization distinction is product-specific. It does not establish a universal readiness schema. |
| [Linear delegation](https://linear.app/docs/assigning-issues) | Passes issue information and configurable prompts to coding tools. Standing instructions can request planning first. | Supports separating reusable procedure from task-specific content; does not guarantee retrieval of every linked source. |
| [VS Code best practices](https://code.visualstudio.com/docs/agents/best-practices) | Recommends observable results, relevant errors/files/constraints, existing test commands and expected outputs. Planning can resolve unclear approaches. Search is automatic; symbols and paths can disambiguate. | General prompting guidance, not a tracker template or evidence that every task needs every detail. |
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices) | Favors information unavailable or costly to rediscover, while recommending useful file pointers, symptoms, fixed states and consequential preferences. Requests executable checks and actual output or screenshots as evidence. | Challenges both indiscriminate context accumulation and banning pointers. Prompt instructions do not enforce outcomes merely by stating them. |
| [Claude Code common workflows](https://code.claude.com/docs/en/common-workflows) | Bug recipes request reproduction commands/steps and intermittent conditions. Refactoring recipes preserve behavior and compatibility and run tests. | Adaptable examples, not mandatory fields. Bug-specific guidance should not become a universal feature specification. |

The cross-vendor overlap concerns meaning: intent, relevant context, boundaries and checkable outcomes. It does not establish interchangeable agent context contracts or a machine-readable Markdown protocol.

## Task distinctions and prospective evidence

The following are synthesis, not prescribed sections. They identify different information needs without deciding how the eventual skill should present them.

| Work | Information that can change the implementation | What completion could mean |
| --- | --- | --- |
| Bug fix | Trigger, observed failure, expected behavior, reproduction evidence and relevant conditions | The failing scenario behaves correctly and relevant existing behavior remains intact. |
| Feature | Intended capability, examples, boundaries, constraints and applicable design or existing patterns | The capability works for agreed scenarios, including material limits. |
| Refactor | Motivation, desired structural improvement, invariants and compatibility requirements | The structure improves while required behavior remains unchanged. |
| Investigation or decision | Question, uncertainty, available evidence and decision criteria | Findings or a decision are delivered; coding is not presumed. |

A before/after explanation can clarify all three implementation types, but should not force a refactor to invent changed user behavior or a feature to claim a prior defect. A reporter may not know the cause or reproduction. The older bug-report study suggests that obtaining useful evidence can be difficult; assistance and explicit uncertainty are alternatives to demanding invented answers.

Acceptance criteria describe conditions a valid result must satisfy. A verification plan describes how those conditions might be checked. Existing observations describe what was actually seen, with their circumstances. Later implementation evidence describes what ran and what happened. These concepts can coexist without duplicating every requirement or creating a permanent results ledger inside the issue.

The specification-oracle study makes one constraint particularly concrete: a check must not silently demand an arbitrary contract that neither the issue nor repository makes inferable. The remedy may be documenting a required public name, or changing an overly implementation-coupled test. It is not necessarily more implementation detail.

Pointers need judgment. Known paths, symbols, screenshots and discussions can reduce ambiguity; repository discovery can replace unnecessary inventories. No located evidence establishes that paths are always stale or always useful. Likewise, dependencies matter when an unavailable prerequisite changes what can be done, but these sources do not prescribe a universal blocker field or sequencing protocol.

## Repository practice and local ownership

A purposeful first-party sample shows different artifact roles, not prevalence or comparative effectiveness. Links pin inspected content, not publication dates. [VS Code feature intake](https://github.com/microsoft/vscode/blob/d4dd44c1926b91e01a98ead72f10be7c460a06ae/.github/ISSUE_TEMPLATE/feature_request.md) asks for a desired feature. [Rust bug intake](https://github.com/rust-lang/rust/blob/16d1ffac17ad8b739e32483ac2e65fe7e1804977/.github/ISSUE_TEMPLATE/bug_report.md) requests reproduction and environment; its [tracking hub](https://github.com/rust-lang/rust/blob/16d1ffac17ad8b739e32483ac2e65fe7e1804977/.github/ISSUE_TEMPLATE/tracking_issue.md) records unresolved questions and history. [Ruff](https://github.com/astral-sh/ruff/blob/abee0da3f2ccf12f322ac50817b621d32753f860/.github/ISSUE_TEMPLATE/1_bug_report.yaml) requests compact reproduction evidence inside one required summary. [Spec Kit implementation tasks](https://github.com/github/spec-kit/blob/ee94598c3c87ae231027b22fb2be2b5a13e8820f/templates/tasks-template.md) reference separate specifications/contracts and require paths. Intake simplicity does not establish implementation readiness; Spec Kit is not a universal Issue standard.

Local observations concern working files inspected at baseline `d95e69cb1882ac59fc2ce54f8dc5f847f2e4faad`, not an asserted clean checkout:

- [to-tickets](../../skills/engineering/to-tickets/SKILL.md) owns implementation bodies, criteria, applicable contracts and verification. It records unresolved agreements yet assigns ready-for-agent by construction. [to-spec](../../skills/engineering/to-spec/SKILL.md) instead blocks ready publication for material unresolved obligations. The missing distinction is consequential uncertainty versus an acceptable assumption, not a requirement to eliminate every uncertainty.
- [triage's brief](../../skills/engineering/triage/AGENT-BRIEF.md) makes a comment authoritative over original body/discussion, including PR-remediation work. Other producers emit bodies. Common headings would not resolve conflicting bodies, brief revisions or parent changes. Preserve this separate surface until explicitly redesigned.
- [implement](../../skills/engineering/implement/SKILL.md) consumes ticket/parent contracts; [code-review](../../skills/engineering/code-review/SKILL.md) compares supplied specification with the candidate. [implement-spec](../../skills/engineering/implement-spec/SKILL.md) releases dependants only after integration and verification. Specification readiness, dependency release and authorization are distinct; a ready label is not all three.
- [wayfinder](../../skills/engineering/wayfinder/SKILL.md) owns decision questions and resolution comments, not implementation readiness. Tracker setup owns transport. Parentage and execution dependencies are different relationships.
- Under [invocation policy](../../.agents/invocation.md), these human-only producers cannot be invoked as shared dependencies. Shared ownership needs a design choice that respects loading rules. A new cross-folder link alone is insufficient.

Local producers generally avoid paths, whereas vendor guidance permits grounded hints and Spec Kit requires them. This is a policy choice to discuss, not proof the repository must change. Bug/feature/refactor distinctions above are conditional information needs, not new triage roles; mixed work exists. Glossary cleanup and scheduling changes remain outside this research.

## Challenge, open questions and method

Cross-source challenge rejected several shortcuts: information availability is not heading effectiveness; observational adoption is not causation; vendor recommendations are not experimental findings; smaller-task correlations do not prove splitting equivalent work helps. Context studies differ in selection and models, so neither maximal detail nor universal minimalism follows. A check can be unfairly coupled to hidden implementation choices; a passing check can also miss important behavior.

The later interview still needs to decide:

- Is the target implementation bodies only, or also authoritative triage comments and parent specifications?
- Is the desired improvement semantic completeness, presentation, readiness, or some combination?
- What source wins conflicts, and what may a child inherit without copying?
- Which uncertainties prevent readiness, and which assumptions are acceptable?
- What path policy and conditional information help actual local tasks?
- Where can shared guidance live without violating invocation rules?
- What representative tasks and outcomes would compare alternatives fairly while preserving user-owned sizing?

A compact contract, a layered handoff and a semantic checklist without fixed headings remain possible comparators. None is selected. Agent Disclosure requires a separate decision; provenance policy from PR work is not inherited automatically. No migration of existing issues is authorized.

Three independent contexts investigated academic evidence, vendor guidance and local/library practice, followed by cross-source challenge and an academic evidence check of the synthesis. This bounded review is not systematic, representative or an execution benchmark. Primary-source depth varies as marked. No local Issue outcome corpus was measured. Correct behavior, reviewability, user effort, cost and completion time are different evaluation targets. The research informs discussion without authorizing implementation.
