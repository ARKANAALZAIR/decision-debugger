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

FAILURE MODE
Trigger: A material thesis assumption deteriorates.
→ Weak Point: The position-sizing decision relies on the thesis remaining valid.
→ Failure: Exposure increases while the thesis is weakening.
→ Immediate Impact: Capital concentration increases.
→ Secondary Impact: Portfolio flexibility decreases.
→ Cascade: Higher exposure → greater sensitivity to thesis failure → reduced optionality.

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
