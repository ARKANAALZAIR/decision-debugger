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

## Failure mode object

Each material failure mode in the human-readable report should map to an object with this shape:

```yaml
id: "FM-001"
option_branch: ""
family: "PREMISE FAILURE"
trigger_precondition: ""
vulnerable_dependency: ""
failure_mechanism: ""
failure_state: ""
direct_effect: ""
cascade: []
terminal_consequence: ""
detection_signal: ""
detection_window: "UNKNOWN"
prevention: []
containment: []
recovery_exit: []
residual_vulnerability: ""
decision_changing: "UNKNOWN"
detectability: "UNKNOWN"
recoverability: "UNKNOWN"
optionality_impact: "UNKNOWN"
evidence_provenance: []
```

`detection_window`, `decision_changing`, `detectability`, `recoverability`, and `optionality_impact` must not be fabricated. `UNKNOWN` is preferred to pseudo-precision.

The machine-readable failure-mode list must describe the same material failure paths shown in the human-readable report.

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
