#!/usr/bin/env bash
# Log task dispatch for observability
# Receives tool input via stdin as JSON

set -euo pipefail

LOG_DIR="${CLAUDE_PROJECT_ROOT:-.}/.claude/plugins/technical-director/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/dispatch-$(date +%Y%m%d).log"

# Read stdin (tool input JSON)
INPUT=$(cat)

# Extract task details
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
DESCRIPTION=$(echo "$INPUT" | jq -r '.tool_input.description // "unknown"' 2>/dev/null || echo "unknown")
PROMPT=$(echo "$INPUT" | jq -r '.tool_input.prompt // ""' 2>/dev/null | head -c 200)

# Log dispatch
cat >> "$LOG_FILE" << EOF
---
timestamp: $TIMESTAMP
event: dispatch
description: $DESCRIPTION
prompt_preview: "${PROMPT}..."
---
EOF

# Allow the tool to proceed
echo '{}'
exit 0