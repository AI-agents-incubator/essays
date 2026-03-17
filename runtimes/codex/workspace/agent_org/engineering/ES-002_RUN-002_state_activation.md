# Engineering Spec: ES-002 RUN-002 State Activation

Work item ID: `WI-002`
Owner: `engineering-manager`
Status: complete

Scope summary:
Evolve the existing Codex sandbox from scaffold to operational continuation by instantiating the live SQLite state store, backfilling run history, and aligning the markdown control plane with current state.

Non-goals:
- Rebuilding the entire `agent_org/` structure from scratch.
- Changing `core/`, `comparison/`, or the Claude Code runtime sandbox.

Required artifacts:
- `state/runtime_state.sqlite`
- `state/state_registry.md`
- `execution/work_orders/WO-002_RUN-002_state_activation.md`
- `runs/RUN-002_state_activation_summary.md`
- `evaluation/RUN-002_state_activation_evaluation.md`

State layer requirements:
- Instantiate the database from `state/sqlite_schema.sql`.
- Backfill `RUN-001` bootstrap history and register `RUN-002` continuation records.
- Keep markdown artifacts as the explainable control plane over the operational database.

Task breakdown:
1. Audit existing sandbox artifacts and identify structural drift after `RUN-001`.
2. Instantiate `state/runtime_state.sqlite` from the local SQLite schema.
3. Register `RUN-001` and `RUN-002` runs, roles, work items, handoffs, and representative artifacts.
4. Synchronize `intake/`, `execution/`, `state/`, `evaluation/`, and `evolution/` docs with the operational state.
5. Publish `RUN-002` summary, evaluation trace, and at least one next-run improvement decision.

Acceptance criteria:
- Live SQLite state exists and can be queried locally.
- `state_registry.md` matches the seeded database content.
- `WI-001`/`WI-002` statuses are aligned across intake, execution, and state artifacts.
- `RUNTIME_STATUS.md` ends in a completed state with artifact references.

Handoffs:
- `engineering-manager -> implementation-agent`
