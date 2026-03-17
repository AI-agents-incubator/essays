# Product Brief: PB-003 — Hook Layer & Continuous State Sync

> run: RUN-003
> benchmark: GT-001 continuation
> directive: OBS-CLAUDE-002
> status: approved

## Goal

Implement CP-002: a hook-driven mechanism that continuously synchronizes the SQLite operational state with the markdown governance layer, preventing drift between the two representation layers.

## Scope

1. Create `agent_org/state/hooks/run_hooks_spec.md` — hook protocol specification.
2. Create `agent_org/state/sync_projections.py` — stdlib-only Python sync script with commands: `run_start`, `run_end`, `check_consistency`, `show_state`.
3. Define and validate consistency invariant: `state_variables.latest_run (DB) == current_run (RUNTIME_STATUS.md)`.
4. Process DQ-002 signal from demand_queue.
5. Produce full RUN-003 pipeline trace and run artifacts.
6. Wire sync reference into startup_sequence.md (CP-003 for RUN-004).

## Out of scope

- Changes to `core/`, `comparison/`, `runtimes/codex/`.
- External dependencies in sync script.
- Automated daemon / file watcher (future RUN).

## Success criteria

- `sync_projections.py` runs without errors.
- `check_consistency` returns `OK`.
- `run_start` and `run_end` hooks update DB correctly.
- Full RUN-003 trace recorded.
- `RUNTIME_STATUS.md` shows `completed`.
