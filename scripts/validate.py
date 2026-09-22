from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "SKILL.md", "README.md", "PRD.md", "CHANGELOG.md", "CONTRIBUTING.md",
    "QUALITY-GATES.md", "LICENSE", "VERSION", "manifest.json",
    "commands/decision-debug.md", "references/decision-framework.md",
    "references/evidence-audit.md", "references/failure-mode-analysis.md",
    "references/causal-analysis.md", "references/stakeholder-and-agency.md",
    "references/output-schema.md", "references/rapid-mode.md",
    "references/high-stakes-routing.md", "references/privacy-and-ledger.md",
    "references/second-order-effects.md", "references/value-dominant-decisions.md",
    "templates/quick-debug.md", "templates/deep-debug.md", "templates/postmortem.md",
    "examples/career-decision.md", "examples/business-decision.md", "examples/investment-decision.md",
    "tests/test-cases.md", "evals/cases.jsonl", "evals/README.md", "scripts/run_spec_eval.py",
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
    "highest-value missing information", "ROBUSTNESS CONDITIONS", "FRAGILITY CONDITIONS",
    "Condition: [observable fact or verified change]", "UNKNOWN"
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
