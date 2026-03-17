# Task Graph

Purpose: map the ordered tasks for active work items.

Owner: `engineering-manager`

Tracked graphs:

`WI-001` | status: complete
1. Create required `agent_org/` directories and templates.
2. Draft product brief and engineering spec.
3. Populate execution artifacts and logs.
4. Create state layer files and registry.
5. Create runtime-specific Codex agents and skills.
6. Record benchmark results and process audit.
7. Add learning entry in improvement backlog.

`WI-002` | status: complete
1. Audit the `RUN-001` sandbox state and identify drift between control-plane artifacts.
2. Instantiate `state/runtime_state.sqlite` from `state/sqlite_schema.sql`.
3. Backfill `RUN-001` and record `RUN-002` operational entities in SQLite.
4. Synchronize `intake/`, `execution/`, `state/`, `evaluation/`, and `evolution/` artifacts with the live state layer.
5. Publish `RUN-002` summary and local evaluation trace with a recommended `RUN-003`.

`WI-003` | status: complete
1. Register `RUN-003` continuation state in SQLite and treat the database as the write-first source of truth.
2. Implement `state/sync_projections.py` to regenerate `state_registry.md`, `demand_queue.md`, and `status_board.md`.
3. Run the projection sync and verify the generated markdown matches the live database.
4. Record `RUN-003` benchmark, evaluation, and evolution updates around the new sync path.
5. Leave the runtime in a completed observer-ready state with a recommended `RUN-004`.

`WI-004` | status: complete
1. Extend the local SQLite schema so improvement backlog items and approved changes can be projected from state.
2. Register `RUN-004` operational records and backfill evolution metadata needed for generation.
3. Extend `state/sync_projections.py` to regenerate evaluation and evolution dashboards from live SQLite data.
4. Verify the expanded projection set with `python3 workspace/agent_org/state/sync_projections.py --check`.
5. Close `IM-003`, publish the `RUN-004` summary/evaluation trace, and leave a recommended `RUN-005`.

`WI-005` | status: complete
1. Refactor `state/sync_projections.py` so projection writes update projection freshness metadata.
2. Add `state/watch_projections.py` to watch SQLite source-state changes and trigger projection refreshes.
3. Register `RUN-005` automation state, watcher metadata, and learning updates in SQLite.
4. Verify watcher-driven refresh without a manual sync command, then confirm `python3 workspace/agent_org/state/sync_projections.py --check`.
5. Close `IM-004`, publish the `RUN-005` summary/evaluation trace, and leave a recommended `RUN-006`.

`WI-006` | status: complete
1. Add `bootstrap/runtime_session.py` so active run commands start and stop the watcher through the bootstrap path instead of manual shell supervision.
2. Extend `state/watch_projections.py` to record watcher lifecycle metadata and shut down cleanly when the runtime session ends.
3. Surface watcher lifecycle state in the SQLite-backed projections and update bootstrap/state documentation to use the supervised session path.
4. Register `RUN-006` operational records and close `IM-005` / implement `CP-005` in SQLite.
5. Verify the supervised runtime session refreshes projections during a bounded SQLite write and confirm `python3 workspace/agent_org/state/sync_projections.py --check`.
6. Publish the `RUN-006` summary/evaluation trace and leave a recommended `RUN-007`.

`WI-007` | status: complete
1. Change `state/watch_projections.py` so idle loops rely on SQLite `PRAGMA data_version` and adaptive backoff before recomputing the full source signature.
2. Extend `bootstrap/runtime_session.py` to pass adaptive watcher timing controls without changing the supervised runtime-session contract.
3. Update the directly affected bootstrap/state docs and decision trace.
4. Register `RUN-007` operational records and close `IM-006` / implement `CP-006` in SQLite.
5. Verify the adaptive watcher refreshes projections during a bounded runtime session and confirm `python3 workspace/agent_org/state/sync_projections.py --check`.
6. Publish the `RUN-007` summary/evaluation trace and return the runtime to an observer-ready completed state.

Update rules:
- Updated by `engineering-manager`.
- Must align with `execution/work_orders/`.
