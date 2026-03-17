# RUN-005 Summary: Projection Watcher Refresh

Run ID: `RUN-005`
Benchmark: `GT-001`
Runtime: `codex`
Core TZ: `agent_org_tz_core.md v1.1`
Addendum: `agent_org_tz_codex.md v2.1`
Date: `2026-03-17`

Goal:
Implement the observer-approved `RUN-005` scope for `IM-004` by removing the manual projection-refresh step from the SQLite-backed markdown views.

Key audit findings:
- `RUN-004` left the markdown projections state-backed but still command-driven.
- `OBS-CODEX-004` explicitly approved `RUN-005` to close that automation gap without broadening the runtime beyond watcher-driven refresh.

Actions completed:
- Refactored `workspace/agent_org/state/sync_projections.py` so projection writes update freshness metadata and can be reused by a watcher.
- Added `workspace/agent_org/state/watch_projections.py` as a poll-based watcher over SQLite source-state signatures.
- Updated local bootstrap/state docs so the watcher is the expected refresh mode when `state.projection_refresh_mode = watcher`.
- Registered `RUN-005`, `WI-005`, seven roles, six handoffs, new artifacts, `BR-005`, `F-004`, `AC-004`, and updated state variables in `state/runtime_state.sqlite`.
- Verified watcher-driven refresh with bounded runs of `python3 -B workspace/agent_org/state/watch_projections.py --skip-initial-sync --max-refreshes 1 --timeout-seconds 60 --run-id RUN-005`, which refreshed `9` projection files after the finalization update and again after summary/evaluation artifact registration.
- Verified `python3 -B workspace/agent_org/state/sync_projections.py --check` passes after the watcher-driven refreshes.
- Closed `IM-004`, implemented `CP-004`, and recorded `IM-005` / `CP-005` as the next learning-oriented recommendation.

Representative artifacts updated:
- `workspace/agent_org/state/sync_projections.py`
- `workspace/agent_org/state/watch_projections.py`
- `workspace/agent_org/state/README.md`
- `workspace/agent_org/bootstrap/startup_sequence.md`
- `workspace/agent_org/evaluation/metric_dashboard.md`
- `runs/RUN-005_projection_watcher_refresh_summary.md`
- `evaluation/RUN-005_projection_watcher_refresh_evaluation.md`

Outcome:
- SQLite-backed markdown views now refresh through a local watcher instead of requiring a manual sync command after each SQLite change.
- The live state layer now contains `5` runs, `35` role records, `5` work items, `30` handoffs, `39` registered artifacts, `5` backlog items, and `4` approved changes.
- `IM-004` is closed, and the next recommended run is `RUN-006` to integrate watcher lifecycle management into bootstrap/runtime startup.
