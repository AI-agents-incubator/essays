# Product Brief: PB-007 RUN-007 Projection Watcher Adaptive Refresh

Work item ID: `WI-007`
Owner: `product-lead`
Status: complete

Goal:
Reduce idle projection-watcher overhead without breaking the supervised runtime-session path introduced in `RUN-006`.

Out of scope:
- Replacing the local watcher with OS-specific file notifications or a long-lived daemon.
- Reworking completed `RUN-001` to `RUN-006` artifacts beyond what is needed to close `IM-006`.
- Expanding the observer protocol beyond the `OBS-CODEX-006` directive.

Success criteria:
- `state/watch_projections.py` stops recomputing the full SQLite source signature on every idle loop.
- Idle watcher checks back off to a larger interval while active changes still reset to a short interval.
- `bootstrap/runtime_session.py` continues to supervise watcher startup, shutdown, and final sync while exposing the new timing controls.
- `IM-006` is closed and `CP-006` is marked implemented.

Dependencies:
- `control/OBSERVER_DIRECTIVE.md`
- `workspace/agent_org/state/runtime_state.sqlite`
- `evaluation/RUN-006_projection_watcher_runtime_session_evaluation.md`

Risks and assumptions:
- Assume SQLite `PRAGMA data_version` is a sufficient stdlib-only signal for cheap commit detection inside this sandbox.
- Assume a bounded adaptive backoff is preferable to adding platform-specific notification dependencies.

Required handoffs:
- `product-lead -> engineering-manager`
