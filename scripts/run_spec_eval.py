import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals/cases.jsonl"
SKILL = ROOT / "SKILL.md"

MARKERS = {
    "auto_execution": ["run **STANDARD** automatically", "complex prompt"],
    "module_status_taxonomy": ["ERROR FOUND", "ERROR NOT FOUND", "NOT ASSESSABLE", "NOT APPLICABLE", "COMPLETED"],
    "finding_ownership": ["Primary Module:", "Related Modules:", "one finding ID"],
    "integrity_check": ["Core module coverage: PASS / FAIL", "Human / machine finding parity"],
    "fma_barrier_coverage": ["Barrier analysis: prevent → contain → recover", "weakest"],
    "proportionality": ["For simple everyday decisions", "low-stakes decisions"],
    "framing_gap": ["Decision Framing", "material", "clarifying"],
    "no_invented_objective": ["Do not invent", "objective"],
    "evidence_limitation": ["Evidence limitation", "generalize"],
    "no_generalization": ["generalization", "evidence"],
    "source_dependence": ["Evidence dependence", "independent"],
    "causal_check": ["Causal Identification Check", "causal"],
    "no_causal_upgrade": ["correlation", "causation"],
    "information_set_lock": ["information set", "Post-Decision Review"],
    "separate_outcome": ["outcome", "original reasoning"],
    "calibration_record": ["Decision Outcome Calibration Record", "decision_id", "USER-SUPPLIED ASSUMPTION", "USER-ESTIMATE"],
    "outcome_review": ["IN_RANGE", "OUT_OF_RANGE", "HELD", "FAILED", "UNRESOLVED"],
    "decision_outcome_quality": ["decision-process quality", "outcome quality", "hindsight alone"],
    "calibration_metric_limits": ["eligible sample", "universal minimum sample", "NOT ASSESSABLE"],
    "missing_original_forecasts": ["NOT ASSESSABLE", "Never invent a forecast"],
    "partial_record": ["copyable blank or partially completed record", "continue any analysis supported"],
    "assumption_reassessment": ["assumption invalidation", "reassessment triggers"],
    "no_information_leakage": ["Later information must not alter the locked decision-time record", "separate, append-only review"],
    "authority_gap": ["decision rights", "authority"],
    "no_inferred_rule": ["Do not infer", "decision rule"],
    "agency_check": ["coercion", "agency"],
    "no_unsupported_legal_conclusion": ["unsupported legal conclusion", "legal"],
    "shared_dependency": ["shared", "dependency"],
    "aggregate_risk": ["portfolio", "concentration"],
    "alternative_completeness": ["Alternative Analysis", "option completeness"],
    "inaction_delay_pilot": ["do nothing", "delay", "pilot"],
    "high_stakes_routing": ["High-Stakes Routing", "professional"],
    "external_verification": ["external verification", "primary"],
    "user_claim": ["USER-CLAIM", "USER-PROVIDED"],
    "no_probability_fabrication": ["probability fabrication", "invent a probability"],
    "no_forced_winner": ["materially equivalent", "winner"],
    "lineage_freshness_scope_method": ["lineage", "freshness", "scope", "method"],
    "optionality": ["pilot", "staging", "option value"],
    "reversibility": ["Reversibility / Optionality", "lock-in"],
    "policy_mode": ["Recurring Policy Mode", "policy"],
    "monitoring": ["monitoring", "reassessment"],
    "exceptions": ["exception", "trigger"],
    "untrusted_content_isolation": ["Untrusted Content Isolation", "embedded", "instructions"],
    "second_order": ["Second-Order Effects", "feedback"],
    "value_owned": ["Value-dominant decisions", "user-owned"],
    "no_value_as_fact": ["values", "factual premises"],
    "user_probability": ["USER-ESTIMATE", "Do not silently recalibrate"],
    "firsthand_scope": ["firsthand", "generalizable"],
    "ledger_minimization": ["minimum necessary retention", "secrets"],
    "reference_class": ["base rates", "reference classes"],
    "citation_integrity": ["citation", "support"],
    "no_material_difference": ["NO MATERIAL DIFFERENCE", "materially equivalent"],
    "second_order_schema": ["second_order_effects", "machine-readable"],
    "mandatory_gate": ["Mandatory execution gate", "role-appropriate status"],
    "sensitivity": ["HIGH SENSITIVITY", "affected decision component"],
    "red_team_output": ["Red-team output minimum", "WHAT WOULD DEFEAT THE ATTACK"],
    "voi_priority": ["HIGH", "verification / acquisition cost", "delay cost"],
    "robustness": ["ROBUSTNESS CONDITIONS", "FRAGILITY CONDITIONS", "MOST SENSITIVE DRIVER"],
    "boundary_format": ["Condition: [observable fact or verified change]", "Interpretation:", "Implication:"],
    "uncertainty_structure": ["Uncertainty Structure", "UNKNOWN", "CONTESTED"],
    "fma_full_chain": ["Failure-engine architecture", "FAILURE MECHANISM", "TERMINAL CONSEQUENCE", "CONTAINMENT", "RECOVERY / EXIT"],
    "fma_recovery": ["PREVENT", "CONTAIN", "RECOVER"],
    "fma_symmetry": ["Failure-mode symmetry test", "How can the alternative fail?"],
    "inaction_failure": ["How can waiting / doing nothing fail?", "inaction", "delay"],
    "fma_families": ["PREMISE FAILURE", "EXECUTION FAILURE", "TIMING / SEQUENCING FAILURE", "MEASUREMENT / FEEDBACK FAILURE"],
    "fma_warning_trigger": ["Early-warning and kill-switch discipline", "WARNING SIGNAL"],
    "fma_decision_boundary": ["FAILURE SIGNAL", "CONDITION", "INTERPRETATION", "IMPLICATION"],
    "fma_no_pseudo_precision": ["Do not invent probabilities", "Do not assign a numeric risk score"],
    "fma_unknowns": ["Use `UNKNOWN` rather than inventing a detection window", "recovery path"],
    "fma_upstream_link": ["Assumption-to-failure linkage", "ASSUMPTION", "DEPENDENCY", "EVIDENCE GAP"],
    "fma_common_mode": ["Common-mode failure analysis", "shared"],
    "fma_shared_driver": ["COMMON FAILURE DRIVER", "multiple branches"],
    "fma_interactions": ["Failure interaction and feedback-loop analysis", "AMPLIFICATION", "MASKING"],
    "fma_dedup": ["Failure-path deduplication", "coverage without combinatorial explosion"],
    "fma_feedback": ["FEEDBACK", "reinforcing or balancing"],
    "fma_intervention_point": ["intervention point", "activation signal"],
    "fma_criticality": ["FAILURE CRITICALITY", "DECISION-CRITICAL", "MONITOR-ONLY"],
    "fma_no_numeric": ["Do not convert these labels into numeric scores", "Do not assign numeric risk scores"],
    "fma_signal_type": ["SIGNAL TYPE", "LEADING", "LAGGING"],
    "fma_barriers": ["Barrier analysis", "PREVENTION BARRIER", "CONTAINMENT BARRIER", "RECOVERY / EXIT BARRIER"],
    "canonical_trigger": ["Jalankan Decision Debugger", "canonical trigger", "STANDARD", "complex prompt"],
    "module_matrix": ["Module Execution Matrix", "19 core modules"],
}

def contains_all(text: str, terms):
    low = text.lower()
    return all(t.lower() in low for t in terms)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run Decision Debugger offline checks or evaluate real runtime captures.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--offline-only", action="store_true", help="run structural checks and evaluator unit tests without claiming runtime behavior")
    mode.add_argument("--captures", type=Path, help="evaluate actual target-runtime captures for CAL-01 through CAL-10")
    args = parser.parse_args(argv)

    try:
        validator = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/validate.py")], capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        print("VALIDATOR FAILED: timeout after 20 seconds")
        return 1
    if validator.returncode != 0:
        print(validator.stdout)
        print(validator.stderr)
        return validator.returncode

    skill = SKILL.read_text(encoding="utf-8")
    cases = []
    for line in CASES.read_text(encoding="utf-8").splitlines():
        if line.strip():
            cases.append(json.loads(line))

    unknown = sorted({expectation for case in cases for expectation in case["expect"] if expectation not in MARKERS})
    if unknown:
        print("Unknown expectation markers:", ", ".join(unknown))
        return 2

    rows = []
    for case in cases:
        missing = []
        for exp in case["expect"]:
            terms = MARKERS.get(exp, [])
            if not contains_all(skill, terms):
                missing.append(exp)
        rows.append({"id": case["id"], "status": "PASS" if not missing else "PARTIAL", "missing": missing})

    passed = sum(r["status"] == "PASS" for r in rows)
    print("Structural marker cases: {}/{}".format(passed, len(rows)))
    if passed != len(rows):
        print(json.dumps([row for row in rows if row["status"] != "PASS"], indent=2))
        return 1

    try:
        unit_tests = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/test_calibration_eval.py")], capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        print("CAPTURE EVALUATOR UNIT TESTS FAILED: timeout after 30 seconds")
        return 1
    print(unit_tests.stdout, end="")
    if unit_tests.stderr:
        print(unit_tests.stderr, file=sys.stderr, end="")
    if unit_tests.returncode != 0:
        print("CAPTURE EVALUATOR UNIT TESTS FAILED (exit {})".format(unit_tests.returncode))
        return unit_tests.returncode

    if args.offline_only:
        print("OFFLINE CHECKS PASSED: structural markers and evaluator unit tests")
        print("TARGET RUNTIME: NOT RUN (offline-only mode)")
        return 0
    if args.captures is None:
        print("TARGET RUNTIME EVALUATION BLOCKED: no actual-runtime captures supplied")
        print("Use --captures DIR for captured-output evaluation, or --offline-only for local checks.")
        return 2

    try:
        captured = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts/calibration_eval.py"), "--captures", str(args.captures)],
            capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        print("CAPTURE EVALUATION FAILED: timeout after 30 seconds")
        return 1
    print(captured.stdout, end="")
    if captured.stderr:
        print(captured.stderr, file=sys.stderr, end="")
    return captured.returncode

if __name__ == "__main__":
    raise SystemExit(main())
