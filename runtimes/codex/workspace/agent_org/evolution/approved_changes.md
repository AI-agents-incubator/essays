# Approved Changes

Purpose: record approved and implemented changes.

Owner: `business-sponsor-interface`

Projection status:
- source_of_truth: `state/runtime_state.sqlite`
- projection_script: `state/sync_projections.py`
- projected_at: `2026-03-17 13:27:52 PDT`

Approved:
- `AC-001` | run: `RUN-002` | source: `observer-approved` | change: instantiate state/runtime_state.sqlite and backfill operational records for RUN-001 and RUN-002 | status: `implemented`
- `AC-002` | run: `RUN-003` | source: `CP-001,CP-002` | change: generate state_registry.md, demand_queue.md, and status_board.md from SQLite via state/sync_projections.py | status: `implemented`
- `AC-003` | run: `RUN-004` | source: `OBS-CODEX-003,CP-003` | change: generate evaluation and evolution dashboard projections from SQLite and close IM-003 | status: `implemented`
- `AC-004` | run: `RUN-005` | source: `OBS-CODEX-004,CP-004` | change: add metadata-aware projection sync and a poll-based watcher so SQLite-backed markdown views refresh automatically after source-state changes | status: `implemented`
- `AC-005` | run: `RUN-006` | source: `OBS-CODEX-005,CP-005` | change: add bootstrap/runtime_session.py and watcher lifecycle metadata so watcher-mode execution is supervised through startup and shutdown | status: `implemented`
- `AC-006` | run: `RUN-007` | source: `OBS-CODEX-006,CP-006` | change: use SQLite data-version checks plus adaptive watcher backoff so idle runtime sessions reduce projection polling cost without leaving the supervised runtime-session path | status: `implemented`

Update rules:
- Approved change records must be written to SQLite first.
- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.
