# Local State Storage Strategy

Purpose: define the SQLite-first storage approach for this sandbox.

Owner: `engineering-manager`

Strategy:
- Use a local SQLite database `runtime_state.sqlite` for operational state.
- Keep schema in `sqlite_schema.sql`.
- Treat markdown artifacts as the control plane.
- Do not store policy text inside the database.

Operational status:
- Live database activation completed in `RUN-002`.
- `RUN-001` bootstrap state is backfilled into the live store to preserve continuity.

Operational rules:
- Each run must insert a record in `organization_runs`.
- Roles and handoffs must be traceable to artifacts.
- State variables are for transient operational values.
- `state_registry.md`, `intake/demand_queue.md`, `execution/status_board.md`, `evaluation/benchmark_results.md`, `evaluation/process_audits.md`, `evaluation/metric_dashboard.md`, `evolution/improvement_backlog.md`, `evolution/change_proposals.md`, and `evolution/approved_changes.md` are generated projections from SQLite via `state/sync_projections.py`, not separate sources of truth.
- If `state.projection_refresh_mode` is `watcher`, run active execution through `python3 agent_org/bootstrap/runtime_session.py --run-id <RUN-ID> -- <command>` so watcher startup, adaptive idle backoff, supervision, shutdown, and final sync stay in the bootstrap path.
- Projection drift must be checked with `python3 state/sync_projections.py --check` and corrected by rerunning the generator or restarting the watcher.

Migration:
- Follow `supabase_migration_path.md` when moving to Postgres/Supabase.
