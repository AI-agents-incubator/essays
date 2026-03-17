# Startup Sequence

1. Read `agent_org/charter/mission.md` and `charter/scope_and_boundaries.md`.
2. Read `policies/` for escalation and quality gates.
3. Review `intake/` for active demand signals.
4. Confirm product brief exists in `product/active_product_briefs/`.
5. Confirm engineering spec and task graph exist.
6. Verify state layer readiness in `state/`.
7. Check execution status in `execution/status_board.md`.
8. Review evaluation artifacts and open improvement items.

## State Initialization Checklist (CP-001)

Before starting any run, verify the following:

- [ ] `state/runtime_state.sqlite` file exists (not just schema).
- [ ] DB contains a row in `organization_runs` for the current run with `status = in_progress`.
- [ ] `state_variables` row `latest_run` reflects the current run id.
- [ ] `state_registry.md` lists entities created in the current run.
- [ ] If DB is absent: create it via `sqlite3 state/runtime_state.sqlite < state/sqlite_schema.sql` and seed prior run data before proceeding.

## Consistency Check (CP-002)

Step 9 — run before proceeding with any new run:

```bash
python3 agent_org/state/sync_projections.py check_consistency
```

- If `OK` → proceed.
- If `SYNC_DRIFT` → run `run_start` hook first, then re-check.

Full hook reference: `state/hooks/run_hooks_spec.md`

## Mandatory Bootstrap Sync Hook (CP-003)

Step 10 — **mandatory** at the start of every new run, after RUNTIME_STATUS is set to `in_progress`.

This step makes state sync proactive rather than reactive. It must be executed regardless of the consistency check result.

```bash
python3 agent_org/state/sync_projections.py run_start \
  --run-id <current-run-id> \
  --benchmark "<benchmark-or-objective-label>"
```

Replace `<current-run-id>` with the actual run id (e.g. `RUN-004`) and `<benchmark-or-objective-label>` with the run's primary objective label.

**Effects:**
- Registers the run in `organization_runs` with `status=in_progress`
- Creates a `work_items` entry for the run's primary work item
- Sets `state_variables.latest_run` to the current run id

**Failure policy:**
- If the script exits with an error (e.g. DB not found), fix the DB before proceeding.
- Do not skip this step. A run without a DB entry is an invisible run.

## Mandatory Run-End Sync Hook (CP-003)

Step 11 — **mandatory** at the end of every run, before RUNTIME_STATUS is set to `completed`.

```bash
python3 agent_org/state/sync_projections.py run_end \
  --run-id <current-run-id> \
  --status completed \
  --summary-path "runtimes/claudecode/runs/<run-id>_<label>_summary.md"
```

**Effects:**
- Marks the run as `completed` in `organization_runs`
- Sets `finished_at` and `summary_path`
- Updates `work_items` to `done`
- Sets `state_variables.last_completed_run`

These two hooks (run_start / run_end) form the mandatory sync lifecycle for every run in this sandbox.
