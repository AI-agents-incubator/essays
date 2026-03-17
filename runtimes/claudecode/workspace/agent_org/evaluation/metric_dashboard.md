# Metric Dashboard

| metric | value | notes |
| --- | --- | --- |
| required_artifacts_present | yes | GT-001 baseline + RUN-002 artifacts |
| handoff_trace_complete | yes | H-001 to H-012 recorded |
| state_layer_ready | yes | SQLite DB live (schema + seeded data) |
| sqlite_db_live | yes | runtime_state.sqlite created RUN-002 |
| cp001_implemented | yes | startup_sequence.md updated |
| cp002_implemented | yes | hook layer live; sync_projections.py created RUN-003 |
| hook_spec_present | yes | state/hooks/run_hooks_spec.md |
| sync_script_present | yes | state/sync_projections.py |
| consistency_invariant_defined | yes | latest_run in DB == current_run in RUNTIME_STATUS.md |
| next_run_ready | yes | CP-003 TBD; RUN-004 pending observer directive |
