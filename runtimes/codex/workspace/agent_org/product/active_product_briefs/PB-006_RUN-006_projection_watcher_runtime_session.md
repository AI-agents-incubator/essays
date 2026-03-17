# Product Brief: PB-006 RUN-006 Projection Watcher Runtime Session

Work item ID: `WI-006`
Owner: `product-lead`
Status: complete

Goal:
Integrate projection watcher startup and shutdown into the documented runtime startup path so active execution does not depend on a separately managed watcher process.

Out of scope:
- Replacing the poll-based watcher with OS-specific file notifications.
- Introducing a persistent external daemon outside this sandbox.
- Broadening the observer protocol beyond the `RUN-006` objective.

Success criteria:
- `bootstrap/runtime_session.py` starts `state/watch_projections.py` automatically when `state.projection_refresh_mode = watcher`.
- The runtime session stops the watcher cleanly after the command finishes and runs a final `state/sync_projections.py` pass.
- Watcher lifecycle metadata is recorded in SQLite and visible in the generated dashboard/state projections.
- `IM-005` is closed and `CP-005` is marked implemented.

Dependencies:
- `control/OBSERVER_DIRECTIVE.md`
- `state/runtime_state.sqlite`
- `evaluation/RUN-005_projection_watcher_refresh_evaluation.md`

Risks and assumptions:
- Assume a session-scoped supervisor is sufficient for the GT-001 sandbox even without a long-lived daemon.
- Assume stdlib-only process supervision is preferable to adding new runtime dependencies.

Required handoffs:
- `product-lead -> engineering-manager`
