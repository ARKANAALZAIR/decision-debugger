#!/usr/bin/env python3
"""Unit tests for the captured-output evaluator, not target-runtime tests."""

from __future__ import annotations

import copy
import json
import unittest

from calibration_eval import DEFAULT_CASES, evaluate_case, load_cases, runtime_prompt


def _record(case):
    supplied = case.get("input", {}).get("decision_time_record")
    if supplied is not None:
        return copy.deepcopy(supplied)
    if case["id"] == "CAL-01":
        return {
            "decision_id": "DD-CAL-01",
            "record_date": "2026-09-01",
            "record_status": "PRE-DECISION",
            "decision_question": "Whether to launch the pilot",
            "chosen_option": None,
            "objective": "Test demand without exceeding the approved budget",
            "material_assumptions": [{"statement": "The supplier can deliver in four weeks", "provenance": "USER-SUPPLIED ASSUMPTION"}],
            "evidence_available_at_record_time": [{"claim_or_observation": "Supplier quote received 2026-09-01", "source": "User-provided quote", "available_date": "2026-09-01", "provenance": "USER-PROVIDED", "verification": "UNVERIFIED"}],
            "expected_outcomes": [{"prediction": "At least 20 qualified signups within six weeks", "measure": "count", "forecast_range": "at least 20", "horizon": "Six weeks", "probability": None}],
            "time_horizon": "Six weeks",
            "leading_indicators": [{"indicator": "Weekly signups", "observable_measure": "count"}],
            "reassessment_thresholds": [{"condition": "Fewer than 10 qualified signups by week four", "source": "USER-PROVIDED"}],
            "unresolved_uncertainties": ["Actual conversion rate"],
        }
    expected_outcomes = []
    if case["id"] == "CAL-01":
        expected_outcomes = [{"prediction": "Qualified signups", "measure": "count", "forecast_range": "at least 20", "horizon": "six weeks", "probability": None}]
    elif case["id"] == "CAL-05":
        expected_outcomes = [{"prediction": "Renewal rate", "measure": "proportion", "forecast_range": [0.7, 0.9], "horizon": "one quarter", "probability": None}]
    elif case["id"] == "CAL-08":
        expected_outcomes = copy.deepcopy(case["input"]["expected_outcomes"])
    return {
        "decision_id": "DD-" + case["id"],
        "record_date": "2026-09-01",
        "record_status": "PRE-DECISION",
        "decision_question": "Whether to continue the pilot",
        "chosen_option": "Continue for one quarter",
        "objective": "Test the stated objective",
        "material_assumptions": [{"assumption_id": "assumption-1", "statement": "The plan is feasible", "provenance": "USER-SUPPLIED ASSUMPTION"}],
        "evidence_available_at_record_time": [{"claim_or_observation": "Current baseline supplied", "source": "User", "available_date": "2026-09-01", "provenance": "USER-PROVIDED", "verification": "UNVERIFIED"}],
        "expected_outcomes": expected_outcomes,
        "time_horizon": "one quarter",
        "leading_indicators": [{"indicator": "Weekly measure", "observable_measure": "count"}],
        "reassessment_thresholds": [{"condition": "Review if threshold is crossed", "source": "USER-PROVIDED"}],
        "unresolved_uncertainties": ["Market response"],
    }


def _capture(case):
    record = _record(case)
    review = {
        "later_information": [],
        "assumption_reviews": [],
        "forecast_comparisons": [],
        "reassessment_trigger_reviews": [],
        "decision_process_quality": "assessed from the original record",
        "decision_process_quality_class": "MIXED",
        "decision_process_quality_basis": "LOCKED_DECISION_TIME_RECORD",
        "outcome_quality": "assessed from observed evidence",
        "outcome_quality_class": "MIXED",
        "evidence_supported_lessons": [],
    }
    ledger = {"decision_time_record": record, "outcome_review": review, "cross_decision_learning": None}
    case_id = case["id"]
    if case_id in ("CAL-02", "CAL-10"):
        review["later_information"] = [copy.deepcopy(case["input"]["later_information"])] if case.get("input", {}).get("later_information") else [{"information": "Outcome evidence arrived later", "learned_date": "2026-10-20", "source": "User-supplied"}]
    if case_id in ("CAL-03", "CAL-04", "CAL-10"):
        expected = case["assertions"]
        review["decision_process_quality_class"] = expected.get("decision_process_quality_class", "MIXED")
        review["outcome_quality_class"] = expected.get("outcome_quality_class", "MIXED")
        review["decision_process_quality_basis"] = expected.get("quality_basis", "LOCKED_DECISION_TIME_RECORD")
    if case_id == "CAL-05":
        review["forecast_comparisons"] = [{"prediction": "Renewal rate", "observed_numeric_value": 0.82, "observed_result": "82%", "result": "IN_RANGE", "evidence": "Supplied renewal report"}]
    if case_id == "CAL-06":
        ledger["cross_decision_learning"] = {
            "decision_ids": ["DD-A", "DD-B", "DD-C"],
            "comparability_and_limitations": "Three supplied records; forecasts are not comparable.",
            "patterns": [{"pattern": "optimistic_timing", "supporting_decision_ids": ["DD-A", "DD-B"], "observed_count": 2, "limitations": "One record is not comparable."}],
            "metrics": [{"name": "range coverage", "value": None, "eligible_sample_count": 0, "eligible_decision_ids": [], "method": "Not suitable", "status": "NOT ASSESSABLE", "limitations": "Forecast types and outcomes are insufficient."}],
        }
    if case_id == "CAL-07":
        ledger["cross_decision_learning"] = {"decision_ids": ["DD-07A"], "patterns": [], "metrics": [{"name": "Brier score", "value": None, "eligible_sample_count": 0, "eligible_decision_ids": [], "method": "Not suitable", "status": "NOT ASSESSABLE", "limitations": "No comparable resolved forecasts."}]}
    if case_id == "CAL-08":
        review["forecast_comparisons"] = [{"prediction": "NOT PROVIDED", "observed_result": "Pilot ended after eight weeks", "result": "NOT ASSESSABLE", "evidence": "No contemporaneous forecast supplied."}]
    if case_id == "CAL-09":
        review["assumption_reviews"] = [{"assumption_id": "supplier_reliable", "result": "FAILED", "evidence": "Measured on-time delivery was 72%, below the recorded 95% condition."}]
        review["reassessment_trigger_reviews"] = [{"trigger_id": "supplier_threshold", "result": "TRIGGERED", "evidence": "Measured on-time delivery was 72%, below the recorded 95% threshold."}]
    capture = {
        "case_id": case_id,
        "prompt": runtime_prompt(case),
        "metadata": {"runtime": "unit-test-fixture", "model_id": "not-a-model-invocation", "captured_at": "2026-10-25T00:00:00Z"},
        "raw_output": "",
        "output": {
            "decision": {"statement": "Test decision", "objective": "Test objective"},
            "executive_state": {"state": "CONDITIONAL", "assessment_confidence": "MODERATE"},
            "findings": [],
            "ledger": ledger,
        },
    }
    capture["raw_output"] = "```json\n" + json.dumps(capture["output"], sort_keys=True) + "\n```"
    return capture


class CalibrationCaptureEvaluatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = {case["id"]: case for case in load_cases(DEFAULT_CASES)}

    def test_suite_contains_ten_distinct_scenarios(self):
        self.assertEqual(len(self.cases), 10)

    def test_each_unit_fixture_satisfies_its_declared_invariants(self):
        for case in self.cases.values():
            with self.subTest(case=case["id"]):
                self.assertEqual(evaluate_case(case, _capture(case)), [])

    def test_later_information_cannot_mutate_locked_record(self):
        case = self.cases["CAL-02"]
        capture = _capture(case)
        capture["output"]["ledger"]["decision_time_record"]["evidence_available_at_record_time"].append({"claim_or_observation": "learned later"})
        self.assertIn("decision_time_record changed after later information was supplied", evaluate_case(case, capture))

    def test_bad_outcome_does_not_overwrite_sound_process_quality(self):
        case = self.cases["CAL-03"]
        capture = _capture(case)
        capture["output"]["ledger"]["outcome_review"]["decision_process_quality_class"] = "WEAK"
        self.assertIn("decision-process quality class does not match the decision-time evidence", evaluate_case(case, capture))

    def test_forecast_status_must_match_original_range_and_observation(self):
        case = self.cases["CAL-05"]
        capture = _capture(case)
        capture["output"]["ledger"]["outcome_review"]["forecast_comparisons"][0]["result"] = "OUT_OF_RANGE"
        self.assertIn("forecast comparison status is incorrect", evaluate_case(case, capture))

    def test_incomparable_records_cannot_receive_computed_metric(self):
        case = self.cases["CAL-07"]
        capture = _capture(case)
        capture["output"]["ledger"]["cross_decision_learning"]["metrics"][0]["status"] = "COMPUTED"
        self.assertIn("insufficient or incomparable data must not produce a computed metric", evaluate_case(case, capture))

    def test_missing_prediction_is_not_assessable(self):
        case = self.cases["CAL-08"]
        capture = _capture(case)
        capture["output"]["ledger"]["outcome_review"]["forecast_comparisons"][0]["result"] = "IN_RANGE"
        self.assertIn("missing original forecast must be marked NOT ASSESSABLE", evaluate_case(case, capture))

    def test_invalidated_assumption_requires_trigger_evidence(self):
        case = self.cases["CAL-09"]
        capture = _capture(case)
        capture["output"]["ledger"]["outcome_review"]["reassessment_trigger_reviews"][0]["evidence"] = ""
        self.assertIn("crossed recorded threshold must trigger reassessment", evaluate_case(case, capture))

    def test_capture_requires_runtime_provenance_and_exact_prompt(self):
        case = self.cases["CAL-01"]
        capture = _capture(case)
        capture["metadata"].pop("model_id")
        capture["prompt"] = "different prompt"
        errors = evaluate_case(case, capture)
        self.assertIn("capture metadata.model_id is required", errors)
        self.assertIn("captured prompt does not match the exact evaluation prompt", errors)

    def test_raw_output_must_match_the_structured_output(self):
        case = self.cases["CAL-01"]
        capture = _capture(case)
        capture["output"]["decision"]["statement"] = "edited after capture"
        self.assertIn("structured output differs from the JSON present in raw_output", evaluate_case(case, capture))

    def test_nested_json_is_extracted_from_one_fenced_block(self):
        from calibration_eval import _extract_json_output

        value, error = _extract_json_output('```json\n{"outer":{"inner":1}}\n```')
        self.assertIsNone(error)
        self.assertEqual(value, {"outer": {"inner": 1}})

    def test_multiple_json_blocks_are_rejected(self):
        from calibration_eval import _extract_json_output

        value, error = _extract_json_output('```json\n{}\n```\n```json\n{}\n```')
        self.assertIsNone(value)
        self.assertEqual(error, "raw output contains multiple fenced JSON objects")

    def test_output_schema_rejects_missing_canonical_top_level_fields(self):
        case = self.cases["CAL-01"]
        capture = _capture(case)
        capture["output"].pop("findings")
        self.assertIn("$: missing required property findings", evaluate_case(case, capture))

    def test_unsupported_probability_cannot_pass_schema_or_provenance_checks(self):
        case = self.cases["CAL-01"]
        capture = _capture(case)
        capture["output"]["ledger"]["decision_time_record"]["expected_outcomes"][0]["probability"] = 0.7
        errors = evaluate_case(case, capture)
        self.assertTrue(any("oneOf" in error for error in errors))
        self.assertTrue(any("unlabeled probability" in error for error in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
