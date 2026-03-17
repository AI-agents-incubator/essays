# Demand Queue

Purpose: track active and queued work items.

Owner: `product-lead`

Projection status:
- source_of_truth: `state/runtime_state.sqlite`
- projection_script: `state/sync_projections.py`
- projected_at: `2026-03-17 13:27:52 PDT`

Queue:
- `WI-001` | run: `RUN-001` | status: `complete` | signal: GT-001 bootstrap | priority: `high`
- `WI-002` | run: `RUN-002` | status: `complete` | signal: RUN-002 continuation and state activation | priority: `high`
- `WI-003` | run: `RUN-003` | status: `complete` | signal: Observer-approved RUN-003 SQLite-to-markdown projection sync | priority: `high`
- `WI-004` | run: `RUN-004` | status: `complete` | signal: Observer-approved RUN-004 evaluation/evolution dashboard projection extension | priority: `high`
- `WI-005` | run: `RUN-005` | status: `complete` | signal: Observer-approved RUN-005 watcher-driven projection refresh | priority: `high`
- `WI-006` | run: `RUN-006` | status: `complete` | signal: Observer-approved RUN-006 projection watcher runtime-session supervision | priority: `high`
- `WI-007` | run: `RUN-007` | status: `complete` | signal: Observer-approved RUN-007 adaptive projection watcher refresh | priority: `high`

Update rules:
- New items and status transitions must be written to SQLite first.
- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.

Links:
- `execution/status_board.md`
- `state/state_registry.md`
