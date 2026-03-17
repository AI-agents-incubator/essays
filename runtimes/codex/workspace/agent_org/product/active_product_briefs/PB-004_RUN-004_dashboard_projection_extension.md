# Product Brief: PB-004 RUN-004 Dashboard Projection Extension

Work item ID: `WI-004`
Owner: `product-lead`
Status: complete

Goal:
Extend the SQLite-backed projection path into the evaluation and evolution dashboards so benchmark, scorecard, and learning summaries are regenerated from live state instead of manual markdown duplication.

Out of scope:
- Building a watcher or daemon that runs projections automatically.
- Replacing markdown artifacts with a database-only workflow.
- Changing `core/`, `comparison/`, or `runtimes/claudecode/`.

Success criteria:
- `state/sync_projections.py` regenerates `evaluation/benchmark_results.md`, `evaluation/process_audits.md`, `evaluation/metric_dashboard.md`, `evolution/improvement_backlog.md`, `evolution/change_proposals.md`, and `evolution/approved_changes.md` from `state/runtime_state.sqlite`.
- The state layer records the improvement backlog and approved change history needed to generate those dashboards.
- `IM-003` is closed with an explicit SQLite-backed projection inventory.
- `python3 state/sync_projections.py --check` passes after the run.

Dependencies:
- `control/OBSERVER_DIRECTIVE.md`
- `state/runtime_state.sqlite`
- `evaluation/RUN-003_state_projection_sync_evaluation.md`

Risks and assumptions:
- Assume a local command-driven projection step is still acceptable for `RUN-004`.
- Assume the local runtime schema can be extended inside the sandbox without changing `core/`.

Required handoffs:
- `product-lead -> engineering-manager`
