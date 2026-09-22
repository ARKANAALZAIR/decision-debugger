#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="project"

case "${1:-}" in
  --project|"") MODE="project" ;;
  --personal) MODE="personal" ;;
  *) echo "Usage: $0 [--project|--personal]" >&2; exit 2 ;;
esac

if [[ "$MODE" == "project" ]]; then
  DEST="$PWD/.claude/skills/decision-debugger"
else
  DEST="$HOME/.claude/skills/decision-debugger"
fi

mkdir -p "$DEST"
cp "$ROOT_DIR/SKILL.md" "$DEST/SKILL.md"
echo "Installed Decision Debugger skill to: $DEST/SKILL.md"
