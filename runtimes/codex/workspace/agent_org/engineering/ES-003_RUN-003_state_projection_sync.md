# Engineering Spec: ES-003 RUN-003 State Projection Sync

Work item ID: `WI-003`
Owner: `engineering-manager`
Status: complete

Scope summary:
Implement a small SQLite-to-markdown projection path so the runtime can regenerate the key control-plane views from the live state store instead of reconciling them by hand.

Non-goals:
- Replacing markdown artifacts with a database-only workflow.
- Adding background processes or external services.
- Reworking completed `RUN-001` or `RUN-002` artifacts outside what is needed for the new sync path.

Required artifacts:
- `state/sync_projections.py`
- `state/state_registry.md`
- `intake/demand_queue.md`
- `execution/status_board.md`
- `execution/work_orders/WO-003_RUN-003_state_projection_sync.md`
- `runs/RUN-003_state_projection_sync_summary.md`
- `evaluation/RUN-003_state_projection_sync_evaluation.md`

State layer requirements:
- Register `RUN-003` and `WI-003` in SQLite before projecting markdown.
- Record the projection script and generated artifacts in `artifact_registry`.
- Keep SQLite as the operational source of truth and markdown as the explainable projection layer.

Task breakdown:
1. Register `RUN-003`, `WI-003`, roles, handoffs, and state variables in SQLite.
2. Implement `state/sync_projections.py` to render registry, queue, and status-board views from live SQLite data.
3. Regenerate the target markdown files and verify them with `--check`.
4. Record the benchmark, evaluation, and evolution updates for the sync mechanism.
5. Close the run with updated runtime status and runtime ack.

Acceptance criteria:
- `python3 workspace/agent_org/state/sync_projections.py --check` passes.
- The generated markdown files match the SQLite contents for runs, work items, handoffs, artifacts, and state variables.
- `RUN-003` leaves a distinct implementation trace rather than another manual reconciliation pass.
- `RUNTIME_STATUS.md` and `RUNTIME_ACK.md` both end in a completed state for `OBS-CODEX-002`.

Handoffs:
- `engineering-manager -> implementation-agent`
