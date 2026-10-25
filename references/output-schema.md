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
barrier_coverage: "COMPLETE | PARTIAL | UNSUPPORTED | UNKNOWN"
weakest_barrier: ""
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
  "ledger": {
    "decision_time_record": null,
    "outcome_review": null,
    "cross_decision_learning": null
  },
  "module_execution": [],
  "audit_integrity": {}
}
```

## Module execution object

```yaml
module_execution:
  - module: "Decision Framing"
    class: "DIAGNOSTIC"
    status: "ERROR FOUND"
    primary_finding_ids: ["F-001"]
    evidence_coverage: "..."
```

Diagnostic statuses:
- `ERROR FOUND`
- `ERROR NOT FOUND`
- `NOT ASSESSABLE`
- `NOT APPLICABLE`

Synthesis / control statuses:
- `COMPLETED`
- `NOT ASSESSABLE`
- `NOT APPLICABLE`

A finding has exactly one `primary_module` and may have zero or more `related_modules`. `ERROR FOUND` requires at least one primary finding. `ERROR NOT FOUND` requires zero primary findings. Related findings do not make a detector `ERROR FOUND`.

## Audit integrity object

```yaml
audit_integrity:
  core_module_coverage: "PASS"
  status_finding_ownership: "PASS"
  primary_related_deduplication: "PASS"
  not_assessable_gaps: "PASS"
  not_applicable_reasons: "PASS"
  human_machine_parity: "PASS"
  executive_state_precedence: "PASS"
  overall: "PASS"
```

Never emit `overall: PASS` when any component is `FAIL`.

Assessment confidence is confidence in the audit assessment, not a probability that the decision succeeds.

Machine-readable output must not introduce information that is absent from the human-readable audit.

## Decision Outcome Calibration Record

The ledger remains user-controlled and optional for routine decisions. When uncertainty or observable outcomes make a record useful, use one `decision_time_record` and add an `outcome_review` later. Keep the original record locked; put later information only in the review. A stable, user-controlled `decision_id` is assigned once and reused unchanged.

```yaml
ledger:
  decision_time_record:
    decision_id: "DD-YYYYMMDD-neutral-label"
    record_date: "YYYY-MM-DD"
    record_status: PRE-DECISION # or USER-RECONSTRUCTED AFTER DECISION
    decision_question: ""
    chosen_option: null
    objective: ""
    material_assumptions:
      - statement: ""
        provenance: USER-SUPPLIED ASSUMPTION
    evidence_available_at_record_time:
      - claim_or_observation: ""
        source: ""
        available_date: ""
        provenance: USER-PROVIDED
        verification: UNVERIFIED
    expected_outcomes:
      - prediction: ""
        measure: null
        forecast_range: null
        horizon: null
        probability: null # when present: {value: 0.7, provenance: USER-ESTIMATE}
    time_horizon: null
    leading_indicators:
      - indicator: ""
        observable_measure: ""
    reassessment_thresholds:
      - condition: ""
        source: USER-PROVIDED # or EVIDENCE-SUPPORTED / QUALITATIVE
    unresolved_uncertainties: []
  outcome_review:
    review_date: "YYYY-MM-DD"
    observed_outcomes:
      - result: ""
        observed_date: ""
        source: ""
        evidence: ""
    later_information:
      - information: ""
        learned_date: ""
        source: ""
    assumption_reviews:
      - assumption: ""
        result: HELD # FAILED | UNRESOLVED
        evidence: ""
    forecast_comparisons:
      - prediction: ""
        observed_result: ""
        result: IN_RANGE # OUT_OF_RANGE | NOT ASSESSABLE
        evidence: ""
    reassessment_trigger_reviews:
      - trigger: ""
        result: NOT ASSESSABLE # TRIGGERED | NOT TRIGGERED
        evidence: ""
    decision_process_quality: ""
    decision_process_quality_class: SOUND # WEAK | MIXED | NOT ASSESSABLE
    decision_process_quality_basis: LOCKED_DECISION_TIME_RECORD
    outcome_quality: ""
    outcome_quality_class: BAD # GOOD | MIXED | NOT ASSESSABLE
    evidence_supported_lessons: []
  cross_decision_learning: null
```

`evidence_available_at_record_time` includes only material information available when the record was made. User-provided assumptions and probabilities retain explicit provenance labels; omit a probability when none is supplied or defensible. Do not convert a qualitative forecast to a numeric one. A retrospective reconstruction is labeled `USER-RECONSTRUCTED AFTER DECISION` and cannot stand in for a contemporaneous forecast.

For each forecast, compare the recorded prediction with an observed result and source. If the original record, forecast, or outcome is absent, mark the affected comparison `NOT ASSESSABLE`; do not invent either side. Assess reasoning quality from the locked record and outcome quality separately from later observations. `later_information` never changes the original record.

Cross-decision learning is included only for records supplied in the current workflow. Link qualitative patterns to decision IDs and state counts, comparability, and limitations. Include a quantitative metric only when the forecast type, observed results, and eligible sample suit that metric. Range-coverage counts can fit comparable measurable forecasts; a Brier score can fit resolved binary probability forecasts, but is an outcome score and does not by itself establish calibration. Report the eligible sample and limitations without claiming a universal minimum sample or statistical confidence. Otherwise mark the metric `NOT ASSESSABLE` or report qualitative learning.

`decision_process_quality_class` and `outcome_quality_class` are descriptive review fields, not canonical module statuses. The process class is based only on the locked decision-time record; its basis field makes that boundary explicit. Use `NOT ASSESSABLE` when the relevant evidence is absent.

When cross-decision learning is available, use this shape so every pattern and metric remains traceable:

```yaml
cross_decision_learning:
  decision_ids: []
  comparability_and_limitations: ""
  patterns:
    - pattern: ""
      supporting_decision_ids: []
      observed_count: 0
      limitations: ""
  metrics:
    - name: ""
      value: null
      eligible_sample_count: 0
      eligible_decision_ids: []
      method: ""
      status: NOT ASSESSABLE # or COMPUTED
      limitations: ""
```
