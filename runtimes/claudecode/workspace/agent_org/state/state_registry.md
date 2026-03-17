# State Registry

run id: RUN-003
runtime: Claude Code
benchmark: GT-001 continuation

## RUN-001 entities (historical)

- organization_runs: RUN-001 completed
- roles: org-bootstrap, product-lead, engineering-manager, integration-reviewer, benchmark-auditor, learning-coordinator
- work_items: WI-001 (GT-001 bootstrap) — done
- handoff_events: H-001 through H-006
- artifact_registry: required artifacts under `agent_org/`
- benchmark_runs: BR-001 (GT-001) — passed
- audit_findings: none
- change_proposals: CP-001 — done (implemented in RUN-002)
- state_variables: latest_run=RUN-001 (superseded)

## RUN-002 entities (historical)

- organization_runs: RUN-002 completed
- work_items: WI-002 (state activation & continuation) — done
- handoff_events: H-007 through H-012
- artifact_registry:
  - PB-002_RUN-002_state_activation.md
  - ES-002_RUN-002_state_activation.md
  - WO-002_RUN-002_state_activation.md
  - runtime_state.sqlite (live, seeded)
  - startup_sequence.md (CP-001 applied)
- change_proposals: CP-002 — done (implemented in RUN-003)
- approved_changes: AC-001 (CP-001 implemented)
- state_variables: latest_run=RUN-002 (superseded)

## RUN-003 entities (current)

- organization_runs: RUN-003 completed
- work_items: WI-003 (hook layer & state sync) — done
- handoff_events: H-013 through H-018
- artifact_registry:
  - PB-003_RUN-003_hook_layer.md
  - ES-003_RUN-003_hook_layer.md
  - WO-003_RUN-003_hook_layer.md
  - state/hooks/run_hooks_spec.md (new)
  - state/sync_projections.py (new)
- change_proposals: CP-003 (open, for RUN-004)
- approved_changes: AC-002 (CP-002 implemented)
- state_variables: latest_run=RUN-003, latest_completed_run=RUN-003

## Live DB

- file: `agent_org/state/runtime_state.sqlite`
- schema: `agent_org/state/sqlite_schema.sql`
- status: active
- tables seeded: organization_runs (3), roles (6), work_items (3), handoff_events (18), benchmark_runs, change_proposals (2), state_variables (4)

## Hook Layer

- spec: `agent_org/state/hooks/run_hooks_spec.md`
- script: `agent_org/state/sync_projections.py`
- consistency_invariant: state_variables.latest_run == RUNTIME_STATUS.current_run
- sync_log: `agent_org/state/sync_log.md` (created on first hook execution)
