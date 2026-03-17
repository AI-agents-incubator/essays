# Hooks

Hook layer configured in RUN-003 (CP-002).

## State Sync Hooks

Script: `agent_org/state/sync_projections.py`
Spec: `agent_org/state/hooks/run_hooks_spec.md`

### Run start
```bash
python3 agent_org/state/sync_projections.py run_start \
  --run-id RUN-XXX --benchmark "GT-001 continuation"
```

### Run end
```bash
python3 agent_org/state/sync_projections.py run_end \
  --run-id RUN-XXX --status completed \
  --summary-path "runtimes/claudecode/runs/RUN-XXX_summary.md"
```

### Consistency check
```bash
python3 agent_org/state/sync_projections.py check_consistency
```

### Show state
```bash
python3 agent_org/state/sync_projections.py show_state
```
