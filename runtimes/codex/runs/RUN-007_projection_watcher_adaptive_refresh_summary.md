# RUN-007 Summary: Projection Watcher Adaptive Refresh

Run ID: `RUN-007`
Benchmark: `GT-001`
Runtime: `codex`
Core TZ: `agent_org_tz_core.md v1.1`
Addendum: `agent_org_tz_codex.md v2.1`
Date: `2026-03-17`

Goal:
Implement the observer-approved `RUN-007` scope for `IM-006` by reducing idle projection-watcher overhead without leaving the supervised runtime-session path.

Key audit findings:
- `RUN-006` left the watcher on a fixed `0.5s` idle polling loop even after lifecycle supervision moved into `bootstrap/runtime_session.py`.
- `OBS-CODEX-006` explicitly approved `RUN-007` to close that overhead gap through `CP-006` instead of starting a wider runtime rewrite.

Actions completed:
- Updated `workspace/agent_org/state/watch_projections.py` so the watcher uses SQLite `PRAGMA data_version` as a cheap change gate and backs off from `0.5s` polling toward a `2.0s` idle ceiling.
- Extended `workspace/agent_org/bootstrap/runtime_session.py` to read and pass adaptive watcher timing controls while preserving the same supervised startup, shutdown, and final-sync contract.
- Updated the directly affected bootstrap/state docs and the local decision trace to reflect adaptive watcher behavior and the data-version check.
- Added the `RUN-007` product brief, engineering spec, work order, task-graph entry, contracts, signal trace, and handoff trace.
- Verified the adaptive path with `python3 -B workspace/agent_org/bootstrap/runtime_session.py --run-id RUN-007 --poll-interval 0.2 --max-poll-interval 0.8 --poll-backoff-factor 2 -- ...`, which produced an initial refresh plus two watcher-driven refreshes around bounded SQLite probe writes.
- Verified `python3 -B workspace/agent_org/state/sync_projections.py --check` passes after the adaptive watcher change and the SQLite finalization update.
- Registered `RUN-007`, `WI-007`, seven roles, six handoffs, ten new/updated artifacts, `BR-007`, `F-006`, `AC-006`, and the new watcher timing state variables in `state/runtime_state.sqlite`.
- Closed `IM-006`, implemented `CP-006`, and left `prepare_comparison` as the next recommended observer step instead of starting `RUN-008`.

Representative artifacts updated:
- `workspace/agent_org/state/watch_projections.py`
- `workspace/agent_org/bootstrap/runtime_session.py`
- `workspace/agent_org/state/README.md`
- `workspace/agent_org/state/storage_strategy.md`
- `workspace/agent_org/bootstrap/startup_sequence.md`
- `workspace/agent_org/product/active_product_briefs/PB-007_RUN-007_projection_watcher_adaptive_refresh.md`
- `workspace/agent_org/engineering/ES-007_RUN-007_projection_watcher_adaptive_refresh.md`
- `workspace/agent_org/execution/work_orders/WO-007_RUN-007_projection_watcher_adaptive_refresh.md`
- `runs/RUN-007_projection_watcher_adaptive_refresh_summary.md`
- `evaluation/RUN-007_projection_watcher_adaptive_refresh_evaluation.md`

Outcome:
- Idle watcher loops now avoid repeated full source-state hashing until SQLite reports a committed change, and active changes reset the watcher to a short poll interval.
- The live state layer now contains `7` runs, `49` role records, `7` work items, `42` handoffs, `58` registered artifacts, `7` benchmark runs, and `6` implemented changes.
- All tracked improvement items through `IM-006` are complete; the next observer-facing step is `prepare_comparison`.
