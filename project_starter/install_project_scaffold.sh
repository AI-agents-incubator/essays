#!/bin/zsh
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /absolute/path/to/project"
  exit 1
fi

TARGET_DIR="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/template_project"

if [ ! -d "$TEMPLATE_DIR" ]; then
  echo "Template directory not found: $TEMPLATE_DIR"
  exit 1
fi

mkdir -p "$TARGET_DIR"

if [ -e "$TARGET_DIR/START_HERE.md" ] || [ -d "$TARGET_DIR/agent_org" ] || [ -d "$TARGET_DIR/project_input" ]; then
  echo "Target already appears initialized: $TARGET_DIR"
  echo "Refusing to overwrite existing scaffold."
  exit 1
fi

cp -R "$TEMPLATE_DIR"/. "$TARGET_DIR"/

echo "Agent organization scaffold installed into:"
echo "  $TARGET_DIR"
echo
echo "Next steps:"
echo "  1. Fill in $TARGET_DIR/project_input/PROJECT_REQUEST.md"
echo "  2. Optionally refine $TARGET_DIR/project_input/PROJECT_CONSTRAINTS.md"
echo "  3. Start the runtime from $TARGET_DIR/START_HERE.md"
