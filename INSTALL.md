# Installation Notes

## Standalone Agent Skill

Use the repository root `SKILL.md` as the standalone skill entrypoint in environments that accept custom Agent Skills. The package contains exactly one `SKILL.md`, which keeps the Claude.ai upload package unambiguous.

## Claude Code

Project skill:

```bash
mkdir -p .claude/skills/decision-debugger
cp /path/to/decision-debugger/SKILL.md .claude/skills/decision-debugger/SKILL.md
```

Personal skill:

```bash
mkdir -p ~/.claude/skills/decision-debugger
cp /path/to/decision-debugger/SKILL.md ~/.claude/skills/decision-debugger/SKILL.md
```

Or run:

```bash
scripts/install_claude_code.sh --project
```

Use `--personal` for the personal skill path.

## Local validation

```bash
python scripts/validate.py
python scripts/run_spec_eval.py
```

The second command is a deterministic specification harness. It does not invoke Claude.
