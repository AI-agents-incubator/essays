# Metric Dashboard

Purpose: track operational metrics and scorecard signals over time.

Owner: `benchmark-and-audit-agent`

Projection status:
- source_of_truth: `state/runtime_state.sqlite`
- projection_script: `state/sync_projections.py`
- projected_at: `2026-03-17 13:27:52 PDT`

Metrics:
- current_run: `RUN-007`
- completed_runs: `7` / `7`
- benchmark_pass_rate: `100% (7/7)`
- projection_sync_active: `yes`
- projection_refresh_mode: `watcher`
- projection_watcher_status: `stopped`
- projection_watcher_launch_mode: `bootstrap/runtime_session.py`
- projected_control_plane_views: `9`
- projected_evaluation_views: `3`
- projected_evolution_views: `3`
- open_improvements: `0`
- proposed_change_proposals: `0`
- implemented_changes: `6`

Update rules:
- Scorecard metrics must be derived from SQLite state and state variables.
- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.
