# Research: implement-spec orchestration

Research date: 2026-10-27. This note supports the proposed orchestration spec. The sources describe different agent systems and workloads, so their findings do not establish a speedup for this skill.

## Coordination and parallel work

Anthropic's [multi-agent research system report](https://www.anthropic.com/research/multi-agent-research-system), published in June 2025, reports gains on its internal research evaluation for parallel, breadth-first exploration, but notes high token costs and cautions that coding often offers fewer independent tasks and difficult real-time coordination. This is a vendor report about a research system, not an evaluation of this repository's implementation pipeline. It supports choosing parallel work from actual dependency and contract independence rather than treating high agent utilization as an objective by itself.

The [CooperBench paper](https://cooperbench.com/static/pdfs/main.pdf), January 2026, studies more than 600 two-agent coding tasks across 12 libraries. Its authors report lower average success for paired agents than when agents handled both features individually, and identify vague or mistimed communication, broken commitments, and incorrect expectations. Its benchmark setup is not the same as isolated worktrees with a serialized integration writer. It nevertheless suggests that selective, specific coordination and integration checks are necessary even where features appear independent.

The [MAST study](https://papers.nips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html), NeurIPS 2025, introduces a dataset of more than 1,600 annotated traces across seven multi-agent frameworks, with failure categories covering system design, inter-agent misalignment, and verification. The taxonomy identifies risks, not the effectiveness of a specific scheduling intervention. The proposed skill should preserve review, verification, and failure handoffs while improving scheduling.

## Scheduling and communication

The [critical-path scheduling study](https://journal.jci.co.id/jitie/article/view/598), 2026, simulates policies on 100 coding-task dependency graphs using word counts as work units. Critical-path scheduling produced small mean improvements over FIFO in that simulation, while the evaluated communication-control policy increased mean makespan despite reducing communication work. The simulation does not measure actual agent execution, correctness, or tool latency. Treat critical-path awareness as a heuristic and communication minimization as a tradeoff, not a guarantee that fewer messages or wait calls means faster delivery.

The [CodeCRDT preprint](https://arxiv.org/abs/2510.18893), October 2025, reports both speedups and slowdowns across six code-generation tasks using a shared-state coordination approach. Its shared-state mechanism differs from this skill's worktree isolation and single integration writer. The varying results reinforce the need to test overlap against representative workflows instead of assuming parallelism is always faster.

## Context and recovery

Anthropic's [context engineering report](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents), September 2025, describes compaction, structured notes, and subagents as approaches for managing long-running context. It is practitioner guidance, not proof that a ledger will survive every compaction or accurately reflect live state. For this skill, a durable scheduling snapshot and reconciliation against available agent, Git, and check state are reasonable design inferences. A ledger records last-known state; it is not a substitute for checking whether an agent or operation is still running.

## Evaluation implications

Measure elapsed time to a verified result and preserve review and correctness outcomes. Record useful bottleneck observations and, when comparing runs, account for work size, dependency structure, capacity, failures, rework, and resource use. Wait-call count alone does not identify idle time or prove an improvement. These are recommendations inferred from the studies' tradeoffs, not measured outcomes for `implement-spec`.
