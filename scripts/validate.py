from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "SKILL.md", "README.md", "PRD.md", "CHANGELOG.md", "CONTRIBUTING.md",
    "QUALITY-GATES.md", "LICENSE", "VERSION", "manifest.json", "RELEASE-MANIFEST.json", "PRODUCTION-READINESS.md",
    "commands/decision-debug.md", "references/decision-framework.md",
    "references/evidence-audit.md", "references/failure-mode-analysis.md",
    "references/causal-analysis.md", "references/stakeholder-and-agency.md",
    "references/output-schema.md", "references/rapid-mode.md",
    "references/high-stakes-routing.md", "references/privacy-and-ledger.md",
    "references/second-order-effects.md", "references/value-dominant-decisions.md",
    "references/module-execution-and-integrity.md",
    "templates/quick-debug.md", "templates/deep-debug.md", "templates/postmortem.md",
    "examples/career-decision.md", "examples/business-decision.md", "examples/investment-decision.md",
    "tests/test-cases.md", "evals/cases.jsonl", "evals/schema.json", "evals/calibration-scenarios.jsonl", "evals/README.md", "scripts/run_spec_eval.py",
    "scripts/calibration_eval.py", "scripts/output_schema_validator.py", "scripts/test_calibration_eval.py",
    "scripts/install_claude_code.sh"
]

TERMS = [
    "# 3. Intake", "# 4. Decision Framing", "# 5. Decision Decomposition",
    "# 6. Evidence Audit", "# 8. Assumption Registry", "# 9. Dependency / Sensitivity Mapping",
    "# 10. Failure Mode Analysis", "# 11. Red-Team Challenge", "# 12. Causal Identification Check",
    "# 19. Reversibility / Optionality", "# 20. Decision Robustness",
    "# 22. Decision Boundaries", "# 23. Reassessment Triggers",
    "INSUFFICIENT EVIDENCE", "CONTESTED", "FRAGILE", "CONDITIONAL", "ROBUST",
    "Untrusted Content Isolation", "Post-Decision Review", "Decision-Changing Test",
    "Second-Order Effects", "Value-dominant decisions", "NO MATERIAL DIFFERENCE",
    "USER-ESTIMATE", "minimum necessary retention",
    "Mandatory execution gate", "HIGH SENSITIVITY", "Red-team output minimum",
    "Automatic Execution & Proportionality", "Module Execution Matrix", "Primary Findings",
    "ERROR FOUND", "ERROR NOT FOUND", "NOT ASSESSABLE", "NOT APPLICABLE", "COMPLETED",
    "Primary Module", "Related Modules", "Audit Integrity Check", "status ↔ primary-finding ownership",
    "Human / machine finding parity", "simple everyday decisions", "low-stakes", "reversible",
    "Do not invent evidence", "BARRIER COVERAGE", "WEAKEST BARRIER", "COMPLETE", "PARTIAL", "UNSUPPORTED",
    "highest-value missing information", "ROBUSTNESS CONDITIONS", "FRAGILITY CONDITIONS",
    "Condition: [observable fact or verified change]", "UNKNOWN",
    "Decision Outcome Calibration Record", "decision_time_record", "outcome_review",
    "USER-SUPPLIED ASSUMPTION", "USER-ESTIMATE", "Later information must not alter the locked decision-time record",
    "Never invent a forecast or outcome", "universal minimum sample", "cross-decision patterns",
    "copyable blank or partially completed record", "decision_process_quality_class",
    "outcome_quality_class", "LOCKED_DECISION_TIME_RECORD"
]

def main() -> int:
    errors = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing: {rel}")

    skill_path = ROOT / "SKILL.md"
    if skill_path.exists():
        skill = skill_path.read_text(encoding="utf-8")
        if not skill.startswith("---\n"):
            errors.append("SKILL.md has no YAML frontmatter")
        fm = re.search(r"^---\n(.*?)\n---\n", skill, re.S)
        if not fm:
            errors.append("SKILL.md frontmatter block is malformed")
        else:
            block = fm.group(1)
            if not re.search(r"^name:\s*\S+", block, re.M):
                errors.append("SKILL.md frontmatter missing name")
            if not re.search(r"^description:\s*.+", block, re.M):
                errors.append("SKILL.md frontmatter missing description")
        for term in TERMS:
            if term not in skill:
                errors.append(f"SKILL.md missing: {term}")

    readiness_path = ROOT / "PRODUCTION-READINESS.md"
    if readiness_path.is_file():
        readiness = readiness_path.read_text(encoding="utf-8")
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        if version not in readiness:
            errors.append("PRODUCTION-READINESS.md version is stale")
        if "CODE/CONTRACT HARDENED — RUNTIME RELEASE BLOCKED" not in readiness:
            errors.append("PRODUCTION-READINESS.md must block runtime release until captures pass")

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    try:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        release_manifest = json.loads((ROOT / "RELEASE-MANIFEST.json").read_text(encoding="utf-8"))
        if manifest.get("version") != version or release_manifest.get("version") != version:
            errors.append("manifest versions must match VERSION")
        if manifest.get("runtime_validation_claim") is not False or release_manifest.get("runtime_validation_claim") is not False:
            errors.append("manifests must not claim target-runtime verification")
        if "--offline-only" not in manifest.get("spec_validation_command", ""):
            errors.append("manifest spec validation command must identify offline-only evaluation")
        if "--captures" not in manifest.get("runtime_capture_evaluation_command", ""):
            errors.append("manifest must identify the actual capture evaluation command")
        if release_manifest.get("runtime_readiness") != "BLOCKED_PENDING_ACTUAL_TARGET_CAPTURES":
            errors.append("release manifest must block readiness pending actual target captures")
        expected_skill_hash = hashlib.sha256((ROOT / "SKILL.md").read_bytes()).hexdigest()
        if release_manifest.get("skill_sha256") != expected_skill_hash:
            errors.append("release manifest skill hash is stale")
    except (OSError, json.JSONDecodeError, AttributeError) as exc:
        errors.append(f"release manifests are invalid: {exc}")

    scenario_path = ROOT / "evals/calibration-scenarios.jsonl"
    if scenario_path.is_file():
        scenarios = []
        try:
            scenarios = [json.loads(line) for line in scenario_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        except json.JSONDecodeError as exc:
            errors.append(f"calibration-scenarios.jsonl contains invalid JSON: {exc}")
        scenario_ids = [item.get("id") for item in scenarios if isinstance(item, dict)]
        required_domains = {
            "complete_predecision_record", "locked_record_preservation", "bad_outcome_sound_process",
            "good_outcome_weak_process", "forecast_comparison", "cross_decision_pattern",
            "insufficient_calibration_data", "missing_original_forecast",
            "invalidated_assumption_reassessment", "no_hindsight_leakage",
        }
        if len(scenarios) != 10 or len(scenario_ids) != len(set(scenario_ids)):
            errors.append("calibration scenario set must contain ten unique cases")
        if {item.get("domain") for item in scenarios if isinstance(item, dict)} != required_domains:
            errors.append("calibration scenario domains do not cover the required behaviors")
        for item in scenarios:
            if not isinstance(item.get("prompt"), str) or not isinstance(item.get("assertions"), dict):
                errors.append("each calibration scenario must define a prompt and output assertions")
                break

    schema_path = ROOT / "evals/schema.json"
    if schema_path.is_file():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            from output_schema_validator import validate_schema_document
            schema_errors = validate_schema_document(schema)
            if schema_errors:
                errors.append("evals/schema.json has unsupported rules: " + "; ".join(schema_errors))
            outcome_properties = schema["$defs"]["outcomeReview"]["properties"]
            record_properties = schema["$defs"]["decisionTimeRecord"]["properties"]
            if "decision_process_quality_class" not in outcome_properties or "outcome_quality_class" not in outcome_properties:
                errors.append("output schema missing separate process/outcome quality classes")
            if "decision_process_quality_basis" not in outcome_properties:
                errors.append("output schema missing decision-time basis for process quality")
            forecast_range = record_properties["expected_outcomes"]["items"]["properties"]["forecast_range"]
            allowed_range_types = set(forecast_range.get("type", []))
            if not {"string", "null", "array"}.issubset(allowed_range_types):
                errors.append("output schema forecast_range must accept qualitative and numeric-range forms")
            if forecast_range.get("items", {}).get("type") != "number" or forecast_range.get("minItems") != 2 or forecast_range.get("maxItems") != 2:
                errors.append("numeric forecast_range must be exactly two numbers")
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            errors.append(f"evals/schema.json calibration contract is invalid: {exc}")

    # If a legacy Claude Code plugin wrapper is present, ensure it mirrors the root skill.
    plugin_skill_path = ROOT / "skills/decision-debugger/SKILL.md"
    if plugin_skill_path.exists() and skill_path.exists():
        def sha(path: Path) -> str:
            return hashlib.sha256(path.read_bytes()).hexdigest()
        if sha(skill_path) != sha(plugin_skill_path):
            errors.append("root SKILL.md and plugin skill SKILL.md differ")

    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print("-", e)
        return 1

    print("VALIDATION PASSED")
    print(f"Required files checked: {len(REQUIRED)}")
    print("Standalone skill identity: OK")
    print("Frontmatter: OK")
    print("Required behavior markers: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
