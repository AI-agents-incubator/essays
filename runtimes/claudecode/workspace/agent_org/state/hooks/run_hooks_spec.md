# Hook Layer Spec: Run-Start / Run-End State Sync

> implemented_in_run: RUN-003
> change_proposal: CP-002
> script: `agent_org/state/sync_projections.py`

## Purpose

Maintain consistency between two layers:

| layer | role |
|---|---|
| `runtime_state.sqlite` | operational memory — machine-queryable |
| markdown governance layer | explainable control plane — human-readable |

Without sync, the two layers can drift. This hook layer prevents drift.

## Consistency Invariant

```
state_variables.latest_run (DB) == current_run (RUNTIME_STATUS.md)
```

If these diverge, `check_consistency` reports `SYNC_DRIFT`.

## Hooks

### run_start

**When:** at the beginning of each new run, after RUNTIME_STATUS is set to `in_progress`.

**Command:**
```bash
python3 agent_org/state/sync_projections.py run_start \
  --run-id RUN-003 \
  --benchmark "GT-001 continuation"
```

**Effect on DB:**
- INSERT or UPDATE `organization_runs` row with `status=in_progress`, `started_at=now`
- INSERT `work_items` row for the run's primary work item
- UPDATE `state_variables.latest_run` to current run id

### run_end

**When:** after all run work is done, before RUNTIME_STATUS is set to `completed`.

**Command:**
```bash
python3 agent_org/state/sync_projections.py run_end \
  --run-id RUN-003 \
  --status completed \
  --summary-path "runtimes/claudecode/runs/RUN-003_hook_layer_summary.md"
```

**Effect on DB:**
- UPDATE `organization_runs`: `status=completed`, `finished_at=now`, `summary_path=...`
- UPDATE `work_items` for this run: `status=done`
- INSERT `state_variables.last_completed_run`

### check_consistency

**When:** any time — diagnostic.

**Command:**
```bash
python3 agent_org/state/sync_projections.py check_consistency
```

**Effect:**
- Reads `state_variables.latest_run` from DB
- Reads `current_run` from RUNTIME_STATUS.md
- Prints `OK` or `SYNC_DRIFT: DB=X, STATUS=Y`

### show_state

**When:** any time — diagnostic.

**Command:**
```bash
python3 agent_org/state/sync_projections.py show_state
```

**Effect:** prints current organization_runs + state_variables + work_items as JSON.

## Integration with startup_sequence.md

Step 6 of startup_sequence.md references this spec. Before proceeding with any run:

1. Run `check_consistency`.
2. If `SYNC_DRIFT` detected → run `run_start` to re-sync.
3. If DB row for current run absent → run `run_start` first.
