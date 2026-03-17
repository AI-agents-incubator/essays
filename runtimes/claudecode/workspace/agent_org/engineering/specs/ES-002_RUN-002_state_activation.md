# Engineering Spec: ES-002 — State Activation & Continuation

> run: RUN-002
> product_brief: PB-002
> status: approved

## Work items

### WI-002-A: Activate SQLite state layer
- Create `agent_org/state/runtime_state.sqlite` via `sqlite3` + existing schema.
- Seed: RUN-001 organization_run, roles (6), work_item WI-001, handoffs H-001 to H-006, benchmark BR-001, change_proposals CP-001, state_variables.
- Seed: RUN-002 organization_run (in_progress), work_item WI-002.
- Verify row counts for each table.

### WI-002-B: Implement CP-001
- Edit `agent_org/bootstrap/startup_sequence.md`: append explicit state initialization checklist.
- Update `evolution/change_proposals.md`: CP-001 → `done`.
- Update `evolution/improvement_backlog.md`: CP-001 → `done`.
- Update `evolution/approved_changes.md`: record AC-001.

### WI-002-C: Sync state_registry.md
- Add RUN-002 entries: new work item, new handoffs H-007 to H-012, updated state_variables.

### WI-002-D: Update evaluation layer
- `evaluation/benchmark_results.md`: add RUN-002 row.
- `evaluation/process_audits.md`: add PA-002.
- `evaluation/metric_dashboard.md`: update `sqlite_db_live` metric.
- `knowledge/decision_log.md`: add D-003 (live DB seeding decision).

### WI-002-E: Create run artifacts
- `runtimes/claudecode/runs/RUN-002_state_activation_summary.md`
- `runtimes/claudecode/evaluation/RUN-002_state_activation_evaluation.md`
- Add CP-002 to `improvement_backlog.md` for RUN-003.

### WI-002-F: Finalize
- Update `execution/handoff_log.md`, `execution/status_board.md`, `execution/integration_log.md`.
- Finalize SQLite: update WI-002 to done, close RUN-002.
- Update `RUNTIME_STATUS.md` to `completed`.

## Constraints

- Do not modify files outside `runtimes/claudecode/`.
- Additive only on all existing artifacts.
