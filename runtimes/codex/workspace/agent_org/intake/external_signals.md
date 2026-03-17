# External Signals

Purpose: record incoming requests and context.

Owner: `business-sponsor-interface`

Signal log:
- `2026-03-17` | `RUN-001` | Bootstrap GT-001 in Codex runtime sandbox.
- `2026-03-17` | `RUN-002` | Continue Codex runtime after scaffold creation; activate live SQLite state and reconcile operational trace.
- `2026-03-17` | `RUN-003` | Observer-approved continuation: implement SQLite-to-markdown projection sync so control-plane views no longer require manual reconciliation.
- `2026-03-17` | `RUN-005` | Observer-approved continuation: add watcher-driven projection refresh so SQLite-backed markdown views stay current without a manual sync command.
- `2026-03-17` | `RUN-007` | Observer-approved continuation: reduce idle projection-watcher polling overhead with adaptive refresh triggers while keeping runtime-session supervision.

Update rules:
- Append-only log.
- Each entry must map to a work item in `intake/demand_queue.md`.

Links:
- `intake/demand_queue.md`
