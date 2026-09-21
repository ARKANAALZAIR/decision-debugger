# Installation Notes

## Standalone Agent Skill

Use the repository's root `SKILL.md` as the standalone skill entrypoint in environments that accept custom Agent Skills.

## Claude Code Plugin

This repository also contains the standard Claude Code plugin layout:

```text
.claude-plugin/plugin.json
skills/decision-debugger/SKILL.md
commands/decision-debug.md
```

The plugin skill is an exact content mirror of the root `SKILL.md` and is checked by the repository validator.

## Local validation

```bash
python scripts/validate.py
python scripts/run_spec_eval.py
```

The second command is a deterministic specification harness. It does not invoke Claude.
