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

FAILURE MODE
Trigger: Validation takes materially longer than planned.
→ Weak Point: Runway planning depends on the six-month assumption.
→ Failure: Revenue remains below the required level.
→ Immediate Impact: Cash runway declines faster than planned.
→ Secondary Impact: Short-term cash pressure increases.
→ Cascade: Pressure → scope changes → execution focus falls → validation slows.
→ Early Warning: Burn or validation metrics diverge from plan.

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
