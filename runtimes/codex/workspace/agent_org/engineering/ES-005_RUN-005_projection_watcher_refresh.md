# Engineering Spec: ES-005 RUN-005 Projection Watcher Refresh

Work item ID: `WI-005`
Owner: `engineering-manager`
Status: complete

Scope summary:
Add a local watcher-driven refresh path so SQLite-backed markdown projections stay current after SQLite commits, while keeping `state/sync_projections.py` as the only renderer.

Non-goals:
- Replacing the current SQLite-first architecture or adding external services.
- Reworking completed `RUN-001` to `RUN-004` artifacts beyond what is needed to close `IM-004`.
- Introducing runtime-specific hook assumptions that are not already present in this sandbox.

Required artifacts:
- `state/sync_projections.py`
- `state/watch_projections.py`
- `state/README.md`
- `state/storage_strategy.md`
- `bootstrap/startup_sequence.md`
- `execution/work_orders/WO-005_RUN-005_projection_watcher_refresh.md`
- `runs/RUN-005_projection_watcher_refresh_summary.md`
- `evaluation/RUN-005_projection_watcher_refresh_evaluation.md`

State layer requirements:
- Register `RUN-005`, `WI-005`, seven roles, six handoffs, new artifacts, `BR-005`, `F-004`, and updated state variables in SQLite.
- Mark `state.projection_refresh_mode` as `watcher` and record the watcher script/poll interval in `state_variables`.
- Close `IM-004`, implement `CP-004`, and leave one next-step improvement recommendation for `RUN-006`.

Task breakdown:
1. Refactor `state/sync_projections.py` so projection writes can refresh projection metadata without separate manual bookkeeping.
2. Add `state/watch_projections.py` as a poll-based watcher over the SQLite source state.
3. Register `RUN-005` automation state in SQLite and regenerate projections through the watcher-driven path.
4. Verify watcher-driven refresh by running the watcher, applying SQLite updates, and confirming the markdown projections update without a manual sync command.
5. Publish the `RUN-005` summary, local evaluation trace, and next recommended improvement.

Acceptance criteria:
- `python3 workspace/agent_org/state/sync_projections.py --check` passes.
- `python3 workspace/agent_org/state/watch_projections.py --skip-initial-sync --max-refreshes 2 --timeout-seconds 15` can observe SQLite updates and refresh projections.
- `IM-004` is marked complete, `CP-004` is marked implemented, and the dashboards show `projection_refresh_mode: watcher`.
- `RUNTIME_STATUS.md` and `RUNTIME_ACK.md` both end in a completed state for `OBS-CODEX-004`.

Handoffs:
- `engineering-manager -> implementation-agent`
