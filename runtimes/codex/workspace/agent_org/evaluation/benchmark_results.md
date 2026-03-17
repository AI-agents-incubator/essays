# Benchmark Results

Purpose: record benchmark outcomes.

Owner: `benchmark-and-audit-agent`

Projection status:
- source_of_truth: `state/runtime_state.sqlite`
- projection_script: `state/sync_projections.py`
- projected_at: `2026-03-17 13:27:52 PDT`

Results:
- `GT-001` | run: `RUN-001` | status: `pass` | date: `2026-03-17` | notes: Bootstrap artifact set, state layer files, and traces present.
- `GT-001` | run: `RUN-002` | status: `pass` | date: `2026-03-17` | notes: Live SQLite store instantiated, status drift corrected, and continuation trace recorded.
- `GT-001` | run: `RUN-003` | status: `pass` | date: `2026-03-17` | notes: SQLite-backed projections now regenerate the registry, demand queue, and status board without manual markdown reconciliation.
- `GT-001` | run: `RUN-004` | status: `pass` | date: `2026-03-17` | notes: SQLite-backed projections now cover evaluation and evolution dashboards, so benchmark and learning rollups regenerate from state.
- `GT-001` | run: `RUN-005` | status: `pass` | date: `2026-03-17` | notes: Watcher-driven refresh now updates the SQLite-backed markdown projections after source-state changes without a manual sync command.
- `GT-001` | run: `RUN-006` | status: `pass` | date: `2026-03-17` | notes: Bootstrap runtime session now supervises watcher startup and shutdown, and the projection set remains synced without manual watcher management.
- `GT-001` | run: `RUN-007` | status: `pass` | date: `2026-03-17` | notes: Adaptive watcher now uses SQLite data-version checks plus idle backoff, so idle runtime sessions avoid fixed-interval full source scans while the supervised runtime-session path stays intact.

Update rules:
- Benchmark outcomes must be written to SQLite first.
- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.
