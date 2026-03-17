# State Layer README

Purpose: describe how the state layer supports long-lived operation.

Owner: `engineering-manager`

Scope:
- SQLite-first operational state inside this sandbox, activated as a live store in `RUN-002`.
- Artifact layer remains the explainable control plane.

Files:
- `runtime_state.sqlite`: live SQLite operational store for runs, roles, work items, and handoffs.
- `state_registry.md`: human-readable index of active state entities.
- `sync_projections.py`: regenerates markdown projections from SQLite state across state, intake, execution, evaluation, and evolution views, and records projection freshness metadata on write.
- `watch_projections.py`: adaptive watcher that uses SQLite change detection to refresh projections automatically after triggering source-state commits.
- `../bootstrap/runtime_session.py`: supervised runtime-session wrapper that starts and stops the watcher around active execution and passes watcher timing controls.
- `storage_strategy.md`: local storage rules and migration expectations.
- `sqlite_schema.sql`: SQLite schema used for the operational database.
- `supabase_migration_path.md`: future migration outline.

Update rules:
- Instantiate `runtime_state.sqlite` from `sqlite_schema.sql` when the live store is absent.
- Run active watcher-mode commands through `python3 agent_org/bootstrap/runtime_session.py --run-id <RUN-ID> -- <command>` so watcher startup, adaptive polling, shutdown, and final sync are supervised.
- Use `python3 state/watch_projections.py` directly only for bounded diagnostics or manual watcher testing.
- Use `python3 state/sync_projections.py` for an explicit one-shot refresh when the watcher is not active.
- Use `python3 state/sync_projections.py --check` to verify that the markdown projections are not stale.
- The watcher keeps a short minimum poll interval for active changes, backs off toward a larger idle interval, and uses SQLite `PRAGMA data_version` before recomputing full source signatures.
- Updates must align with `core/state/*` expectations.
