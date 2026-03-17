# Product Brief: PB-005 RUN-005 Projection Watcher Refresh

Work item ID: `WI-005`
Owner: `product-lead`
Status: complete

Goal:
Remove the manual projection-refresh step by adding a local watcher that refreshes SQLite-backed markdown views after SQLite state changes.

Out of scope:
- Replacing polling with OS-specific file notification dependencies.
- Supervising the watcher outside this sandbox or across multiple runtimes.
- Changing `core/`, `comparison/`, or `runtimes/claudecode/`.

Success criteria:
- `state/watch_projections.py` detects SQLite source-state changes and reruns the markdown projection path without a manual sync command.
- `state/sync_projections.py` remains the single projection renderer and records projection freshness metadata on write.
- `IM-004` is closed and `CP-004` is marked implemented.
- `python3 state/sync_projections.py --check` passes after watcher-driven refresh.

Dependencies:
- `control/OBSERVER_DIRECTIVE.md`
- `state/runtime_state.sqlite`
- `evaluation/RUN-004_dashboard_projection_extension_evaluation.md`

Risks and assumptions:
- Assume a poll-based watcher is acceptable for the first watcher-driven refresh inside the sandbox.
- Assume watcher lifecycle can remain locally started for `RUN-005` even if future bootstrap automation is still needed.

Required handoffs:
- `product-lead -> engineering-manager`
