# Engineering Spec: ES-006 RUN-006 Projection Watcher Runtime Session

Work item ID: `WI-006`
Owner: `engineering-manager`
Status: complete

Scope summary:
Add a bootstrap-level runtime session wrapper that supervises projection watcher lifecycle around active execution, while keeping the watcher and projection renderer as the existing state-layer components.

Non-goals:
- Replacing the poll-based watcher with a daemon or OS-level service.
- Reworking completed `RUN-001` to `RUN-005` artifacts beyond what is needed to close `IM-005`.
- Changing `core/`, `comparison/`, or `runtimes/claudecode/`.

Required artifacts:
- `bootstrap/runtime_session.py`
- `bootstrap/startup_sequence.md`
- `state/watch_projections.py`
- `state/sync_projections.py`
- `state/README.md`
- `state/storage_strategy.md`
- `execution/work_orders/WO-006_RUN-006_projection_watcher_runtime_session.md`
- `runs/RUN-006_projection_watcher_runtime_session_summary.md`
- `evaluation/RUN-006_projection_watcher_runtime_session_evaluation.md`

State layer requirements:
- Register `RUN-006`, `WI-006`, seven roles, six handoffs, the new runtime-session artifact, `BR-006`, `F-005`, and `AC-005` in SQLite.
- Update runtime state variables so `runtime.current_run = RUN-006` and watcher lifecycle metadata is visible in projections.
- Close `IM-005`, implement `CP-005`, and leave one next-step improvement recommendation for `RUN-007`.

Task breakdown:
1. Add `bootstrap/runtime_session.py` to launch the watcher before active execution and shut it down after the command completes.
2. Extend `state/watch_projections.py` to record watcher lifecycle metadata and stop cleanly on runtime-session shutdown.
3. Surface watcher lifecycle status in the generated projections and update the bootstrap/state docs to use the supervised session path.
4. Register `RUN-006` operational records and learning updates in SQLite.
5. Verify the supervised runtime session refreshes projections during a bounded SQLite write and confirm `python3 workspace/agent_org/state/sync_projections.py --check`.
6. Publish the `RUN-006` summary, local evaluation trace, and runtime protocol updates.

Acceptance criteria:
- `python3 workspace/agent_org/bootstrap/runtime_session.py --run-id RUN-006 -- zsh -lc "sqlite3 workspace/agent_org/state/runtime_state.sqlite ..."` runs successfully and leaves the projection set in sync.
- `python3 workspace/agent_org/state/sync_projections.py --check` passes after the bounded runtime-session verification.
- `IM-005` is marked complete, `CP-005` is marked implemented, and the generated state/evaluation dashboards show watcher lifecycle metadata from the supervised path.
- `RUNTIME_STATUS.md` and `RUNTIME_ACK.md` both end in a completed state for `OBS-CODEX-005`.

Handoffs:
- `engineering-manager -> implementation-agent`
