# Startup Sequence

Purpose: define how a runtime boots the organization.

Owner: `org-bootstrap` (runtime role)

Steps:
1. Read `AGENTS.md` and confirm write scope.
2. Load `agent_org/charter/*` and `policies/*`.
3. Check for missing artifacts and create them if required.
4. Load or initialize state layer using `state/sqlite_schema.sql`.
5. Register the observer-approved run in SQLite and set `runtime.current_run` before active execution starts.
6. If `state.projection_refresh_mode` is `watcher`, start active execution through `python3 agent_org/bootstrap/runtime_session.py --run-id <RUN-ID> -- <command>` so `state/watch_projections.py` is started before SQLite writes, uses adaptive polling while idle, is supervised during execution, and stops with a final projection sync at shutdown.
7. If the watcher mode is not active, run the command directly and use `python3 agent_org/state/sync_projections.py --run-id <RUN-ID>` after write-heavy execution.
8. Enter waiting mode for external signals when no observer-approved run is active.

Update rules:
- Updates require `learning-agent` review.
