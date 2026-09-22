# Example — Investment Decision

This is an illustrative reasoning audit, not investment advice or a recommendation to buy or sell.

## Input

> I want to increase my position because the asset is down 30% and my long-term thesis is unchanged.

## Example Output

```text
DECISION DEBUGGER REPORT

Decision State: FRAGILE
Assessment Confidence: MODERATE

Primary Vulnerability:
The decision treats a price decline as evidence that the opportunity improved, but the causal or valuation link is not established by the price move alone.

Decision-Changing Finding:
If new evidence invalidates a material thesis assumption, increasing exposure may no longer satisfy the stated thesis.

MATERIAL FINDINGS

[DECISION-CHANGING] #001
Severity: HIGH
Type: REASONING
Problem: “Price fell, therefore the opportunity improved” is not established by price decline alone.
Evidence: Price movement is an observed fact; opportunity improvement requires additional premises.
Reasoning: The price movement is being used as a proxy for thesis validity without a demonstrated link.
Recommended Action: Separate price, valuation, thesis evidence, and invalidation conditions.

EVIDENCE AUDIT
Check whether supporting evidence is independent, current, relevant to the thesis, and contradicted by any material disconfirming evidence.

FAILURE MODE ANALYSIS
FM-001 — Decision-Critical Premise Failure
Trigger: A material thesis assumption deteriorates.
Upstream Link: ASSUMPTION — the thesis remains supported by current evidence.
Vulnerable Dependency: Position sizing depends on thesis validity.
Failure Mechanism: Exposure remains elevated while the thesis is weakening.
Failure State: Capital concentration no longer matches the current evidence base.
Direct Effect: Loss sensitivity increases while flexibility decreases.
Cascade: Weaker thesis → higher relative exposure → reduced optionality → slower willingness to reassess.
Common-Mode Driver: The thesis evidence and the “buy the dip” rationale may rely on the same upstream market narrative.
Failure Interaction: FM-001 can be MASKED by short-term price recovery even while the underlying thesis deteriorates.
Detection: LEADING — disconfirming evidence or a thesis-invalidating indicator appears before a major price move, if observable.
Detection Window: UNKNOWN unless a concrete invalidation indicator is established.
Prevention: Define thesis-invalidating evidence before adding exposure; stage commitments.
Containment: Cap concentration or pause further additions when invalidation evidence appears.
Recovery / Exit: Reduce exposure or exit when the user-defined thesis condition is materially invalidated.
Residual Vulnerability: Market behavior can remain noisy even when the thesis is weakening.
Decision Boundary: Condition: verified evidence materially invalidates a critical thesis premise → Interpretation: the original position thesis no longer holds → Implication: reassess sizing or maintain no-action until evidence improves.
ALTERNATIVES
- maintain position
- reduce position
- staged increase
- wait for specified evidence
- no action

FINAL DECISION DEBUG
What is sound: The user has identified a thesis and a proposed action.
What is fragile: The inference from price decline to improved opportunity.
What is unresolved: Whether the thesis remains supported by current evidence.
What would change the decision: Verified evidence that materially changes a thesis assumption or valuation premise.
What should be monitored: Thesis-validity indicators, disconfirming evidence, concentration, and invalidation conditions.
```
