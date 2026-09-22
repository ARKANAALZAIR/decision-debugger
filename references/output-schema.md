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
failure_criticality: "DECISION-CRITICAL"
trigger_precondition: ""
upstream_links:
  - type: ASSUMPTION
    reference: ""
    status: "SUPPORTED | INFERRED | UNKNOWN"
vulnerable_dependency: ""
failure_mechanism: ""
failure_state: ""
direct_effect: ""
cascade: []
common_mode_driver: null
interactions:
  - with_failure_mode: "FM-002"
    relation: "AMPLIFICATION"
    mechanism: ""
    decision_effect: ""
feedback_loop:
  present: false
  nodes: []
  direction: []
  type: "REINFORCING | BALANCING | UNKNOWN"
  activation_signal: ""
  intervention_point: ""
terminal_consequence: ""
detection:
  signal: ""
  signal_type: "LEADING | LAGGING | UNKNOWN"
  window: "UNKNOWN"
prevention: []
containment: []
recovery_exit: []
residual_vulnerability: ""
decision_changing: "YES | NO | UNKNOWN"
detectability: "EARLY | MID-COURSE | LATE | UNKNOWN"
recoverability: "HIGH | MODERATE | LOW | UNKNOWN"
optionality_impact: "PRESERVED | REDUCED | LOST | UNKNOWN"
decision_boundary: null
evidence_provenance: []
```

Rules:
- `common_mode_driver` is used when more than one branch shares a material upstream failure driver.
- `interactions` should contain only decision-relevant relationships; do not create a combinatorial graph of every imaginable dependency.
- `feedback_loop.present` may be `true` only when a supportable mechanism closes the loop.
- `decision_boundary` should use `condition → interpretation → implication` when a material trigger can govern action or reassessment.
- `failure_criticality` is a qualitative materiality label, not a risk score.
- `detection.window`, `decision_changing`, `detectability`, `recoverability`, `optionality_impact`, and unsupported interaction details must not be fabricated. Use `UNKNOWN`.

The machine-readable failure-mode list must describe the same material failure paths, interactions, common-mode drivers, and feedback loops shown in the human-readable report.

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
