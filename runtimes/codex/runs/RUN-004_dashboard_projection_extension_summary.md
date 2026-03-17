# RUN-004 Summary: Dashboard Projection Extension

Run ID: `RUN-004`
Benchmark: `GT-001`
Runtime: `codex`
Core TZ: `agent_org_tz_core.md v1.1`
Addendum: `agent_org_tz_codex.md v2.1`
Date: `2026-03-17`

Goal:
Implement the observer-approved `RUN-004` scope for `IM-003` by extending SQLite-backed projections into the evaluation and evolution dashboards.

Key audit findings:
- `RUN-003` left benchmark, scorecard, and learning rollups as manual markdown summaries even though the operational state already lived in SQLite.
- `OBS-CODEX-003` explicitly approved `RUN-004` to close that gap without starting any broader engineering run.

Actions completed:
- Extended the local SQLite schema with `improvement_backlog` and `approved_changes`, plus backlog linkage for `change_proposals`.
- Registered `RUN-004`, `WI-004`, seven roles, six handoffs, new artifacts, `BR-004`, `F-003`, backlog items, proposals, approved changes, and updated state variables in `state/runtime_state.sqlite`.
- Extended `workspace/agent_org/state/sync_projections.py` from `3` to `9` markdown projections.
- Regenerated `evaluation/benchmark_results.md`, `evaluation/process_audits.md`, `evaluation/metric_dashboard.md`, `evolution/improvement_backlog.md`, `evolution/change_proposals.md`, and `evolution/approved_changes.md` from SQLite.
- Closed `IM-003`, implemented `CP-003`, and recorded `IM-004` / `CP-004` as the next learning-oriented recommendation.

Markdown projections now generated from SQLite state:
- `state/state_registry.md`
- `intake/demand_queue.md`
- `execution/status_board.md`
- `evaluation/benchmark_results.md`
- `evaluation/process_audits.md`
- `evaluation/metric_dashboard.md`
- `evolution/improvement_backlog.md`
- `evolution/change_proposals.md`
- `evolution/approved_changes.md`

Representative artifacts updated:
- `workspace/agent_org/state/sqlite_schema.sql`
- `workspace/agent_org/state/sync_projections.py`
- `workspace/agent_org/evaluation/metric_dashboard.md`
- `workspace/agent_org/evolution/improvement_backlog.md`
- `runs/RUN-004_dashboard_projection_extension_summary.md`
- `evaluation/RUN-004_dashboard_projection_extension_evaluation.md`

Outcome:
- SQLite is now the write-first source for the runtime's state, intake, execution, evaluation, and evolution dashboards.
- The live state layer now contains `4` runs, `28` role records, `4` work items, `24` handoffs, `32` registered artifacts, `4` backlog items, and `3` approved changes.
- `IM-003` is closed, and the next recommended run is `RUN-005` to explore watcher-driven projection refresh.
