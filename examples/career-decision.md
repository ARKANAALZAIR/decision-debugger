# Example — Career Decision

This is an illustrative output, not a recommendation.

## Input

> Should I leave my job to build a startup full-time? I have about 12 months of runway and expect revenue validation within six months.

## Example Output

```text
DECISION DEBUGGER REPORT

Decision State: CONDITIONAL
Assessment Confidence: MODERATE

Primary Vulnerability:
The six-month revenue-validation timeline is treated as a planning assumption without a clear evidence basis.

Decision-Changing Finding:
If validation takes materially longer than the available runway can support, the decision conditions change.

DECISION PROFILE
Decision: Leave current job to build startup full-time
Objective: Build the startup while preserving acceptable financial security
Constraints: Personal runway, business burn, validation timeline
Options: Full-time, part-time, delay, staged/pilot transition
Decision Owner: User

MATERIAL FINDINGS

[DECISION-CHANGING] #001
Severity: HIGH
Type: ASSUMPTION
Problem: The six-month validation milestone lacks a sufficiently verified evidence basis.
Impact: A delay can compress runway and change feasibility.
Recommended Action: Validate the timeline and model downside runway conditions.

FAILURE MODE ANALYSIS
FM-001 — Decision-Critical Resource / Constraint Failure
Trigger: Validation takes materially longer than planned.
Upstream Link: ASSUMPTION — six-month validation milestone.
Vulnerable Dependency: Personal runway supports the required learning period.
Failure Mechanism: Revenue remains below the level required to sustain planned burn.
Failure State: Available runway falls below the amount required to continue the full-time branch safely.
Direct Effect: Cash pressure increases.
Cascade: Pressure → scope changes → execution focus falls → validation slows.
Feedback Loop: REINFORCING — lower runway increases pressure; pressure reduces execution capacity; slower execution delays validation; delay further reduces runway.
Common-Mode Driver: Revenue timing also affects the staged transition because both branches depend on the same market validation.
Detection: LEADING — burn and validation progress diverge from plan.
Detection Window: Before the minimum acceptable runway buffer is crossed, if tracked consistently.
Prevention: Validate the milestone; preserve a minimum buffer; stage commitment.
Containment: Reduce burn or narrow scope when the operating condition changes materially.
Recovery / Exit: Preserve income option, pause the full-time branch, or return to staged execution.
Residual Vulnerability: The true validation curve remains uncertain.
Decision Boundary: Condition: runway or validation evidence crosses the minimum operating boundary → Interpretation: original transition assumption no longer holds → Implication: reassess the branch.
ALTERNATIVES
A. Full-time transition
B. Part-time build
C. Delay
D. Defined pilot / staged transition

DECISION BOUNDARIES
Reassess if runway, burn, validation timing, or a material assumption changes.

FINAL DECISION DEBUG
What is sound: The objective and core constraints are identifiable.
What is fragile: The validation timeline.
What is unresolved: Evidence supporting that timeline.
What would change the decision: Verified evidence materially changing runway or validation requirements.
What should be monitored: Burn, runway, validation progress, and assumption integrity.
```

This example intentionally does not tell the user to quit or stay.
