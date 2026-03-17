#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
HEARTBEAT_FILE="$ROOT_DIR/HUMAN_PROGRESS.md"

while true; do
  clear
  echo "Agent Organization Live Monitor"
  echo "screen_refresh: $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "source_update_interval: 5s"
  echo
  if [[ -f "$HEARTBEAT_FILE" ]]; then
    awk '
      /^- heartbeat_at:/ { print $0; next }
      /^- system_display_status:/ { print $0; next }
      /^- system_progress_expectation:/ { print $0; next }
      /^- active_runtimes:/ { print $0; next }
      /^- terminal_runtimes:/ { print $0; next }
      /^- attention_runtimes:/ { print $0; print ""; next }
      /^## Claude Code$/ { section="claude"; print $0; next }
      /^## Codex$/ { section="codex"; print $0; next }
      /^## Recent Events$/ { section="events"; print ""; print $0; next }
      section == "claude" && /^- (current_run|display_status|progress_expectation|runtime_status|runtime_updated_at|observer_directive|runtime_ack|protocol_consistency|protocol_explanation|next_action|worker_process|worker_pid|status_signal_age_seconds|ack_signal_age_seconds|log_signal_age_seconds|log_size_bytes|observer_phase|open_backlog_item|needs_human|blocking_issue|log_file):/ { print }
      section == "codex" && /^- (current_run|display_status|progress_expectation|runtime_status|runtime_updated_at|observer_directive|runtime_ack|protocol_consistency|protocol_explanation|next_action|worker_process|worker_pid|status_signal_age_seconds|ack_signal_age_seconds|log_signal_age_seconds|log_size_bytes|observer_phase|open_backlog_item|needs_human|blocking_issue|log_file):/ { print }
      section == "events" && /^- / { events[++n] = $0 }
      END {
        if (n > 0) {
          start = n - 3
          if (start < 1) start = 1
          for (i = start; i <= n; i++) print events[i]
        }
      }
    ' "$HEARTBEAT_FILE"
  else
    echo "No heartbeat file yet: $HEARTBEAT_FILE"
  fi
  sleep 5
done
