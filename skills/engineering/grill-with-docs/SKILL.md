---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
disable-model-invocation: true
---

Load model-invoked dependencies through the harness's skill loader. If no loader is exposed, resolve their installed `SKILL.md` paths from the available skill catalog and read those entry points, preserving invocation policy. Report unavailable dependencies instead of guessing an installation directory or using this repository's human-facing docs as instructions.


Call the Skill tool twice, for "grilling" and "domain-modeling".

During consequential design decisions where independent challenge could change the outcome, call the Skill tool with "codebase-design" and use its adversarial-review guidance. Keep the interview with the user: specialist findings inform the next question frontier, and agents never answer the user's choices for them. Carry resolved objections and substantive dissent into the appropriate decision record without turning the glossary into a plan.
