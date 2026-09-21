# Output Schema

The human-readable report and machine-readable representation must describe the same decision audit.

## Executive state

```yaml
state: CONDITIONAL
assessment_confidence: MODERATE
primary_vulnerability: ""
decision_changing_finding: null
```

Allowed state values:
- `INSUFFICIENT EVIDENCE`
- `CONTESTED`
- `FRAGILE`
- `CONDITIONAL`
- `ROBUST`

`NO MATERIAL DIFFERENCE` is **not** an executive state. It is an alternative-analysis relationship used when relevant options are materially equivalent under the stated criteria.

## Finding

```yaml
id: ""
severity: HIGH
type: ASSUMPTION
location: ""
problem: ""
evidence: ""
reasoning: ""
impact: ""
recommended_action: ""
decision_changing: YES
provenance: USER-PROVIDED
verification: UNVERIFIED
```

## Canonical object

```json
{
  "decision": {
    "statement": "",
    "objective": [],
    "constraints": [],
    "options": [],
    "owner": null,
    "decision_rights": null,
    "stakeholders": [],
    "time_horizon": null,
    "reversibility": null,
    "stakes": null,
    "mode": "STANDARD"
  },
  "executive_state": {
    "state": "CONDITIONAL",
    "assessment_confidence": "MODERATE",
    "primary_vulnerability": "",
    "decision_changing_finding": null
  },
  "findings": [],
  "evidence_audit": [],
  "assumptions": [],
  "dependencies": [],
  "failure_modes": [],
  "scenarios": [],
  "alternatives": [],
  "feasibility": {},
  "stakeholder_agency": {},
  "second_order_effects": [],
  "reversibility": {},
  "decision_boundaries": [],
  "reassessment_triggers": [],
  "next_best_information": [],
  "ledger": {}
}
```

Assessment confidence is confidence in the audit assessment, not a probability that the decision succeeds.

Machine-readable output must not introduce information that is absent from the human-readable audit.
