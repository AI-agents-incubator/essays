# Change Proposals

Purpose: capture proposed structural changes.

Owner: `learning-agent`

Projection status:
- source_of_truth: `state/runtime_state.sqlite`
- projection_script: `state/sync_projections.py`
- projected_at: `2026-03-17 13:27:52 PDT`

Proposals:
- `CP-001` | target: `state/state_registry.md` | type: `automation` | expected effect: Reduce manual state registry updates. | status: `implemented` | backlog: `IM-001`
- `CP-002` | target: `execution/status_board.md,intake/demand_queue.md` | type: `synchronization` | expected effect: Derive queue and status-board views from SQLite state to eliminate drift. | status: `implemented` | backlog: `IM-002`
- `CP-003` | target: `evaluation/benchmark_results.md,evaluation/process_audits.md,evaluation/metric_dashboard.md,evolution/improvement_backlog.md,evolution/change_proposals.md,evolution/approved_changes.md` | type: `extension` | expected effect: Extend SQLite-backed projections to benchmark, scorecard, and learning dashboards. | status: `implemented` | backlog: `IM-003`
- `CP-004` | target: `state/sync_projections.py,state/watch_projections.py` | type: `automation` | expected effect: Trigger projection refresh automatically after SQLite source-state changes without requiring a manual sync command. | status: `implemented` | backlog: `IM-004`
- `CP-005` | target: `bootstrap/startup_sequence.md,state/watch_projections.py` | type: `automation` | expected effect: Start and supervise the projection watcher automatically when the runtime enters active execution. | status: `implemented` | backlog: `IM-005`
- `CP-006` | target: `state/watch_projections.py,bootstrap/runtime_session.py` | type: `optimization` | expected effect: Reduce idle polling cost while keeping watcher supervision in the bootstrap/runtime session path. | status: `implemented` | backlog: `IM-006`

Update rules:
- Change proposals must be written to SQLite first.
- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.
