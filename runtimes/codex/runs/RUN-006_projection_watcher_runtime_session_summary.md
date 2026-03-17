# RUN-006 Summary: Projection Watcher Runtime Session

Run ID: `RUN-006`
Benchmark: `GT-001`
Runtime: `codex`
Core TZ: `agent_org_tz_core.md v1.1`
Addendum: `agent_org_tz_codex.md v2.1`
Date: `2026-03-17`

Goal:
Implement the observer-approved `RUN-006` scope for `IM-005` by integrating projection watcher lifecycle into the bootstrap/runtime startup path.

Key audit findings:
- `RUN-005` automated projection refresh but still relied on manually starting and stopping the watcher process.
- `OBS-CODEX-005` explicitly approved `RUN-006` to close that lifecycle gap without widening the runtime beyond watcher supervision.

Actions completed:
- Added `workspace/agent_org/bootstrap/runtime_session.py` as the supervised runtime-session wrapper for watcher-mode execution.
- Extended `workspace/agent_org/state/watch_projections.py` to record lifecycle metadata, ignore self-trigger watcher state variables when hashing source state, and shut down cleanly on runtime-session signals.
- Extended `workspace/agent_org/state/sync_projections.py` so generated projections surface watcher status and watcher launch mode from SQLite state.
- Updated local bootstrap/state docs so watcher-mode execution routes through `bootstrap/runtime_session.py` instead of a separately managed watcher shell.
- Verified the supervised path with `python3 -B workspace/agent_org/bootstrap/runtime_session.py --run-id RUN-006 -- python3 -c '...'`, which produced an initial projection sync, one watcher-driven refresh while the bounded SQLite update was active, a second refresh after cleanup, and a clean watcher shutdown.
- Registered `RUN-006`, `WI-006`, seven roles, six handoffs, new artifacts, `BR-006`, `F-005`, `AC-005`, and updated watcher/runtime state variables in `state/runtime_state.sqlite`.
- Closed `IM-005`, implemented `CP-005`, and recorded `IM-006` / `CP-006` as the next learning-oriented recommendation.

Representative artifacts updated:
- `workspace/agent_org/bootstrap/runtime_session.py`
- `workspace/agent_org/state/watch_projections.py`
- `workspace/agent_org/state/sync_projections.py`
- `workspace/agent_org/bootstrap/startup_sequence.md`
- `workspace/agent_org/state/README.md`
- `workspace/agent_org/state/storage_strategy.md`
- `runs/RUN-006_projection_watcher_runtime_session_summary.md`
- `evaluation/RUN-006_projection_watcher_runtime_session_evaluation.md`

Outcome:
- Watcher lifecycle now enters and exits through the documented bootstrap/runtime session path instead of relying on a separately supervised manual process.
- SQLite-backed projections now expose watcher lifecycle metadata so the control plane shows whether the watcher was started manually or through the supervised session.
- The live state layer now contains `6` runs, `42` role records, `6` work items, `36` handoffs, `48` registered artifacts, `6` benchmark runs, and `5` implemented changes.
- The next recommended run is `RUN-007` to reduce the remaining idle-polling cost of the watcher lifecycle.
