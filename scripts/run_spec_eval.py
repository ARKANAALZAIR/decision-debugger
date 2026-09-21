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
    "second_order_schema": ["second_order_effects", "machine-readable"]
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
