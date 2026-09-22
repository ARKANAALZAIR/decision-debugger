from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals/cases.jsonl"
SKILL = ROOT / "SKILL.md"

MARKERS = {
    "framing_gap": ["Decision Framing", "material", "clarifying"],
    "no_invented_objective": ["Do not invent", "objective"],
    "evidence_limitation": ["Evidence limitation", "generalize"],
    "no_generalization": ["generalization", "evidence"],
    "source_dependence": ["Evidence dependence", "independent"],
    "causal_check": ["Causal Identification Check", "causal"],
    "no_causal_upgrade": ["correlation", "causation"],
    "information_set_lock": ["information set", "Post-Decision Review"],
    "separate_outcome": ["outcome", "original reasoning"],
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
    "mandatory_gate": ["Mandatory execution gate", "NOT MATERIAL / NOT APPLICABLE"],
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
}

def contains_all(text: str, terms):
    low = text.lower()
    return all(t.lower() in low for t in terms)


def main():
    validator = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py")], capture_output=True, text=True)
    if validator.returncode != 0:
        print(validator.stdout)
        print(validator.stderr)
        return validator.returncode

    skill = SKILL.read_text(encoding="utf-8")
    cases = []
    for line in CASES.read_text(encoding="utf-8").splitlines():
        if line.strip():
            cases.append(json.loads(line))

    rows = []
    for case in cases:
        missing = []
        for exp in case["expect"]:
            terms = MARKERS.get(exp, [])
            if not contains_all(skill, terms):
                missing.append(exp)
        rows.append({"id": case["id"], "status": "PASS" if not missing else "PARTIAL", "missing": missing})

    passed = sum(r["status"] == "PASS" for r in rows)
    print(f"Specification cases: {len(rows)}")
    print(f"PASS: {passed}")
    print(f"PARTIAL: {len(rows) - passed}")
    print("Runtime Claude execution: NOT RUN")
    print(json.dumps(rows, indent=2))
    return 0 if passed == len(rows) else 1

if __name__ == "__main__":
    raise SystemExit(main())
