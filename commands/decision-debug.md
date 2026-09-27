---
description: Run a Decision Debugger audit on the decision supplied by the user.
---

Use the `decision-debugger` skill.

Default to STANDARD mode unless the user specifies RAPID, DEEP, or POST-MORTEM.

Preserve the skill's non-prescriptive decision-ownership rules and its output contract.

Canonical trigger: when the user supplies a decision and says “Jalankan Decision Debugger.”, run STANDARD without requiring module names or a complex prompt. Equivalent natural-language requests such as “Debug this decision.” also run STANDARD. Apply the module-status and audit-integrity contract.
