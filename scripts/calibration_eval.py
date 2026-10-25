#!/usr/bin/env python3
"""Evaluate explicitly captured Decision Debugger calibration outputs.

This tool never invokes or simulates a model. Capture metadata is supplied by
the evaluator and must be checked against the actual target-runtime run.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from output_schema_validator import validate_instance, validate_schema_document

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals/calibration-scenarios.jsonl"
OUTPUT_SCHEMA = ROOT / "evals/schema.json"
RUNTIME_PROMPT_SUFFIX = "\n\nFor this evaluation, include the complete canonical machine-readable JSON output in a fenced `json` block."


def load_cases(path: Path = DEFAULT_CASES) -> list[dict[str, Any]]:
    cases = []
    seen = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError("{}:{}: {}".format(path, line_number, exc))
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id or any(char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-" for char in case_id) or case_id in seen:
            raise ValueError("{}:{}: missing or duplicate case id".format(path, line_number))
        if not isinstance(case.get("prompt"), str) or not isinstance(case.get("assertions"), dict):
            raise ValueError("{}:{}: prompt and assertions are required".format(path, line_number))
        seen.add(case_id)
        cases.append(case)
    return cases


def runtime_prompt(case: dict[str, Any]) -> str:
    return case["prompt"] + RUNTIME_PROMPT_SUFFIX


def _extract_json_output(raw_output: str) -> tuple[dict[str, Any] | None, str | None]:
    trimmed = raw_output.strip()
    blocks = re.findall(r"(?is)```json\s*(.*?)\s*```", trimmed)
    if len(blocks) == 1:
        candidate = blocks[0]
    elif len(blocks) > 1:
        return None, "raw output contains multiple fenced JSON objects"
    elif trimmed.startswith("{"):
        candidate = trimmed
    else:
        return None, "raw output must contain one fenced JSON object"
    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError as exc:
        return None, "raw output JSON is invalid: {}".format(exc)
    if not isinstance(parsed, dict):
        return None, "raw output JSON must be an object"
    return parsed, None


def _is_nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _record_errors(record: Any) -> list[str]:
    errors = []
    if not isinstance(record, dict):
        return ["ledger.decision_time_record must be an object"]
    required = (
        "decision_id", "record_date", "decision_question", "objective",
        "material_assumptions", "evidence_available_at_record_time",
        "expected_outcomes", "time_horizon", "leading_indicators",
        "reassessment_thresholds", "unresolved_uncertainties",
    )
    for field in required:
        if field not in record:
            errors.append("decision_time_record missing {}".format(field))
    for field in ("decision_id", "decision_question", "objective"):
        if not _is_nonempty(record.get(field)):
            errors.append("decision_time_record.{} must be nonempty".format(field))
    record_date = record.get("record_date")
    if record_date is not None:
        try:
            datetime.strptime(record_date, "%Y-%m-%d")
        except (TypeError, ValueError):
            errors.append("record_date must be YYYY-MM-DD or null")
    array_fields = ("material_assumptions", "evidence_available_at_record_time", "expected_outcomes", "leading_indicators", "reassessment_thresholds", "unresolved_uncertainties")
    for field in array_fields:
        if field in record and not isinstance(record[field], list):
            errors.append("decision_time_record.{} must be an array".format(field))
    forecasts = record.get("expected_outcomes", [])
    for index, prediction in enumerate(forecasts if isinstance(forecasts, list) else []):
        if not isinstance(prediction, dict):
            errors.append("expected_outcomes[{}] must be an object".format(index))
            continue
        probability = prediction.get("probability")
        if isinstance(probability, (int, float)):
            errors.append("expected_outcomes[{}] has an unlabeled probability".format(index))
        elif probability is not None and (not isinstance(probability, dict) or probability.get("provenance") not in ("USER-ESTIMATE", "EVIDENCE-SUPPORTED")):
            errors.append("expected_outcomes[{}] probability needs supported provenance".format(index))
    return errors


def _review(capture: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    output = capture.get("output")
    if not isinstance(output, dict):
        return None, ["capture.output must be a structured object extracted from the captured response"]
    errors = _schema_errors(output)
    ledger = output.get("ledger")
    if not isinstance(ledger, dict):
        return None, errors + ["output.ledger must be an object"]
    errors.extend(_record_errors(ledger.get("decision_time_record")))
    review = ledger.get("outcome_review")
    if review is not None and not isinstance(review, dict):
        errors.append("outcome_review must be an object or null")
        review = None
    return {"ledger": ledger, "review": review}, errors


def _schema_errors(output: Any) -> list[str]:
    try:
        schema = json.loads(OUTPUT_SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return ["cannot load canonical output schema: {}".format(exc)]
    document_errors = validate_schema_document(schema)
    if document_errors:
        return ["canonical output schema uses unsupported rules: {}".format("; ".join(document_errors))]
    return validate_instance(output, schema)


def evaluate_case(case: dict[str, Any], capture: dict[str, Any]) -> list[str]:
    """Return behavioral contract failures for one actual captured output."""
    errors = []
    if capture.get("case_id") != case.get("id"):
        errors.append("capture case_id does not match scenario")
    metadata = capture.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("capture metadata is required")
    else:
        for field in ("runtime", "model_id", "captured_at"):
            if not _is_nonempty(metadata.get(field)):
                errors.append("capture metadata.{} is required".format(field))
    if not _is_nonempty(capture.get("raw_output")):
        errors.append("capture.raw_output must preserve the actual response text")
    elif capture.get("prompt") != runtime_prompt(case):
        errors.append("captured prompt does not match the exact evaluation prompt")
    if _is_nonempty(capture.get("raw_output")):
        extracted, extraction_error = _extract_json_output(capture["raw_output"])
        if extraction_error:
            errors.append(extraction_error)
        elif extracted != capture.get("output"):
            errors.append("structured output differs from the JSON present in raw_output")

    parsed, parse_errors = _review(capture)
    errors.extend(parse_errors)
    if parsed is None:
        return errors
    ledger, review = parsed["ledger"], parsed["review"]
    assertion = case.get("assertions", {})
    initial = ledger.get("decision_time_record")
    if not isinstance(initial, dict):
        return errors

    complete_record = assertion.get("complete_predecision_record")
    if complete_record:
        for field in ("record_status", "chosen_option"):
            if field not in initial:
                errors.append("decision_time_record missing {}".format(field))
        if initial.get("record_status") != "PRE-DECISION":
            errors.append("pre-decision case must retain PRE-DECISION status")
        if not initial.get("expected_outcomes"):
            errors.append("pre-decision case requires a supported expected outcome")
        if not initial.get("time_horizon"):
            errors.append("pre-decision case requires a time horizon")
        if isinstance(complete_record, dict):
            for field in ("decision_question", "objective", "time_horizon"):
                if initial.get(field) != complete_record.get(field):
                    errors.append("pre-decision {} does not match supplied context".format(field))
            expected_values = {
                "material_assumptions": complete_record.get("assumption"),
                "evidence_available_at_record_time": complete_record.get("evidence"),
                "expected_outcomes": complete_record.get("forecast"),
            }
            for field, expected_value in expected_values.items():
                if expected_value is not None and not any(expected_value in json.dumps(item, sort_keys=True) for item in initial.get(field, [])):
                    errors.append("pre-decision {} does not preserve supplied detail".format(field))

    if assertion.get("preserve_record_exactly"):
        supplied = case.get("input", {}).get("decision_time_record")
        if supplied is None:
            errors.append("scenario must supply its locked decision-time record")
        elif initial != supplied:
            errors.append("decision_time_record changed after later information was supplied")

    if assertion.get("later_information_separate"):
        if not isinstance(review, dict):
            errors.append("outcome_review is required")
        elif not isinstance(review.get("later_information"), list):
            errors.append("later information must be recorded in outcome_review.later_information")
        elif case.get("input", {}).get("later_information") is not None and case["input"]["later_information"] not in review["later_information"]:
            errors.append("supplied later information is missing from outcome_review")

    expected_process = assertion.get("decision_process_quality_class")
    expected_outcome = assertion.get("outcome_quality_class")
    if expected_process or expected_outcome or assertion.get("quality_basis"):
        if not isinstance(review, dict):
            errors.append("outcome_review is required for quality comparison")
        else:
            if review.get("decision_process_quality_class") != expected_process:
                errors.append("decision-process quality class does not match the decision-time evidence")
            if review.get("outcome_quality_class") != expected_outcome:
                errors.append("outcome quality class is not separately represented as expected")
            if review.get("decision_process_quality_basis") != assertion.get("quality_basis"):
                errors.append("decision-process quality must cite its permitted information basis")

    if "comparison" in assertion:
        if not isinstance(review, dict):
            errors.append("outcome_review is required for forecast comparison")
        else:
            comparisons = review.get("forecast_comparisons", [])
            matching = [item for item in comparisons if isinstance(item, dict) and item.get("prediction") == assertion.get("prediction")]
            if len(matching) != 1:
                errors.append("expected exactly one forecast comparison for the supplied prediction")
            else:
                item = matching[0]
                recorded = [entry for entry in initial.get("expected_outcomes", []) if isinstance(entry, dict) and entry.get("prediction") == assertion.get("prediction")]
                if len(recorded) != 1:
                    errors.append("forecast comparison must refer to exactly one original recorded prediction")
                elif recorded[0].get("forecast_range") != assertion.get("forecast_range"):
                    errors.append("comparison range differs from the locked original forecast")
                if item.get("result") != assertion["comparison"]:
                    errors.append("forecast comparison status is incorrect")
                observed = item.get("observed_numeric_value")
                low, high = assertion["forecast_range"]
                if not isinstance(observed, (int, float)) or observed != assertion["observed_value"]:
                    errors.append("observed value does not match the supplied outcome")
                elif item.get("result") != ("IN_RANGE" if low <= observed <= high else "OUT_OF_RANGE"):
                    errors.append("forecast status does not agree with the numeric range comparison")

    if "decision_ids" in assertion:
        cross = ledger.get("cross_decision_learning")
        if not isinstance(cross, dict):
            errors.append("cross_decision_learning is required")
        else:
            if cross.get("decision_ids") != assertion["decision_ids"]:
                errors.append("cross-decision IDs do not match the supplied records")
            patterns = [item for item in cross.get("patterns", []) if isinstance(item, dict) and item.get("pattern") == assertion.get("pattern")]
            if len(patterns) != 1:
                errors.append("expected exactly one traceable recurring pattern")
            else:
                pattern = patterns[0]
                if pattern.get("supporting_decision_ids") != assertion["supporting_decision_ids"] or pattern.get("observed_count") != assertion["observed_count"]:
                    errors.append("pattern must identify its supporting records and count")
            metric_statuses = [item.get("status") for item in cross.get("metrics", []) if isinstance(item, dict)]
            if assertion.get("metric_status") not in metric_statuses:
                errors.append("ineligible cross-decision metric must be NOT ASSESSABLE")

    if assertion.get("no_computed_metric"):
        cross = ledger.get("cross_decision_learning") or {}
        metrics = cross.get("metrics", []) if isinstance(cross, dict) else []
        if any(isinstance(item, dict) and item.get("status") == "COMPUTED" for item in metrics):
            errors.append("insufficient or incomparable data must not produce a computed metric")

    if assertion.get("forecast_status"):
        if not isinstance(review, dict):
            errors.append("outcome_review is required to report a missing forecast")
        else:
            comparisons = review.get("forecast_comparisons", [])
            if not any(isinstance(item, dict) and item.get("result") == assertion["forecast_status"] and item.get("prediction") in (None, "NOT PROVIDED") for item in comparisons):
                errors.append("missing original forecast must be marked NOT ASSESSABLE")

    if assertion.get("no_invented_forecast"):
        supplied_forecasts = case.get("input", {}).get("expected_outcomes", [])
        if supplied_forecasts:
            errors.append("missing-forecast scenario unexpectedly supplies a historical forecast")
        if isinstance(review, dict):
            for item in review.get("forecast_comparisons", []):
                if isinstance(item, dict) and item.get("result") != "NOT ASSESSABLE":
                    errors.append("reconstructed forecast was treated as assessable")

    if "assumption_id" in assertion:
        if not isinstance(review, dict):
            errors.append("outcome_review is required for assumption reassessment")
        else:
            assumptions = [item for item in review.get("assumption_reviews", []) if isinstance(item, dict) and item.get("assumption_id") == assertion["assumption_id"]]
            triggers = [item for item in review.get("reassessment_trigger_reviews", []) if isinstance(item, dict) and item.get("trigger_id") == assertion["trigger_id"]]
            if len(assumptions) != 1 or assumptions[0].get("result") != assertion["assumption_status"]:
                errors.append("invalidated assumption must be classified FAILED")
            if len(triggers) != 1 or triggers[0].get("result") != assertion["trigger_status"] or not _is_nonempty(triggers[0].get("evidence")):
                errors.append("crossed recorded threshold must trigger reassessment")

    return errors


def evaluate_capture_directory(cases: list[dict[str, Any]], directory: Path) -> tuple[list[str], list[str]]:
    """Return (blocked case IDs, failed case messages) without invoking a model."""
    blocked, failed = [], []
    for case in cases:
        path = directory / (case["id"] + ".json")
        if not path.is_file():
            blocked.append(case["id"])
            continue
        try:
            capture = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failed.append("{}: invalid capture: {}".format(case["id"], exc))
            continue
        case_errors = evaluate_case(case, capture)
        failed.extend("{}: {}".format(case["id"], error) for error in case_errors)
    return blocked, failed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--captures", required=True, type=Path, help="directory of actual-runtime <case-id>.json captures")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    args = parser.parse_args(argv)
    try:
        cases = load_cases(args.cases)
    except (OSError, ValueError) as exc:
        print("INVALID CASE SET: {}".format(exc))
        return 1
    blocked, failed = evaluate_capture_directory(cases, args.captures)
    if failed:
        print("CAPTURE EVALUATION FAILED")
        for item in failed:
            print("- " + item)
    if blocked:
        print("RUNTIME EVALUATION BLOCKED: missing actual-runtime captures for {} case(s): {}".format(len(blocked), ", ".join(blocked)))
    if failed:
        return 1
    if blocked:
        return 2
    print("CAPTURED OUTPUTS PASSED: {}/{} scenarios".format(len(cases), len(cases)))
    print("Runtime execution is not independently authenticated by this local evaluator.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
