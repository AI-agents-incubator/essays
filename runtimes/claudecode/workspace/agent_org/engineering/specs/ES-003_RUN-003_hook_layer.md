# Engineering Spec: ES-003 — Hook Layer & Continuous State Sync

> run: RUN-003
> product_brief: PB-003
> status: approved

## Work items

### WI-003-A: Hook spec
- Create `agent_org/state/hooks/run_hooks_spec.md`.
- Document: consistency invariant, run_start / run_end / check_consistency / show_state commands.
- Document startup_sequence.md integration steps.

### WI-003-B: sync_projections.py
- Python 3, stdlib only (sqlite3, argparse, json, re, pathlib, datetime).
- `run_start`: INSERT/UPDATE organization_runs + work_items + state_variables.latest_run.
- `run_end`: UPDATE organization_runs (status, finished_at, summary_path) + work_items + state_variables.last_completed_run.
- `check_consistency`: compare DB state_variables.latest_run vs RUNTIME_STATUS.md current_run field.
- `show_state`: JSON dump of organization_runs, state_variables, work_items.
- Paths: DB relative to script; RUNTIME_STATUS.md at ../../../runs/RUNTIME_STATUS.md.

### WI-003-C: Validate hooks
- Run `run_start --run-id RUN-003 --benchmark "GT-001 continuation"`.
- Run `check_consistency` → must return `OK`.
- Confirm DB has RUN-003 row with status=in_progress.

### WI-003-D: Create sync_log.md
- `agent_org/state/sync_log.md` — execution log for hook invocations.

### WI-003-E: Update .claude/hooks/README.md
- Document hook commands with invocation examples.

### WI-003-F: Update startup_sequence.md
- Add Step 9: run `check_consistency` before each new run.

### WI-003-G: Pipeline artifacts and evaluation
- PB-003, ES-003, WO-003.
- Handoffs H-013 to H-018.
- Update evaluation, evolution, knowledge artifacts.

### WI-003-H: Run end
- Run `run_end` hook to finalize DB.
- Create run summary and evaluation trace.
- Update RUNTIME_STATUS.md → completed.
- Update RUNTIME_ACK.md.

## Constraints

- Additive only on existing artifacts.
- No modifications outside `runtimes/claudecode/`.
