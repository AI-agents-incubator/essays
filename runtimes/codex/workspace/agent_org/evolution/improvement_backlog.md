# Improvement Backlog

Purpose: track learning-driven improvements.

Owner: `learning-agent`

Projection status:
- source_of_truth: `state/runtime_state.sqlite`
- projection_script: `state/sync_projections.py`
- projected_at: `2026-03-17 13:27:52 PDT`

Backlog:
- `IM-001` | Improve automation of state registry updates | source: GT-001 audit | status: `complete` | proposals: `CP-001`
- `IM-002` | Generate queue/status-board projections from SQLite state to prevent control-plane drift | source: RUN-002 audit | status: `complete` | proposals: `CP-002`
- `IM-003` | Extend SQLite-backed projections into evaluation and evolution dashboards | source: RUN-003 audit | status: `complete` | proposals: `CP-003`
- `IM-004` | Consider watcher-driven projection refresh for SQLite-backed markdown views | source: RUN-004 audit | status: `complete` | proposals: `CP-004`
- `IM-005` | Integrate projection watcher lifecycle into bootstrap and runtime startup | source: RUN-005 audit | status: `complete` | proposals: `CP-005`
- `IM-006` | Reduce projection watcher polling overhead with event-driven or adaptive refresh triggers | source: RUN-006 audit | status: `complete` | proposals: `CP-006`

Update rules:
- Learning backlog changes must be written to SQLite first.
- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.
