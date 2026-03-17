# State Registry

Purpose: map operational entities to artifacts and live run context.

Owner: `engineering-manager`

Projection status:
- source_of_truth: `state/runtime_state.sqlite`
- projection_script: `state/sync_projections.py`
- projected_at: `2026-03-17 13:27:52 PDT`
- refresh_mode: `watcher`
- watcher_status: `stopped`
- watcher_launch_mode: `bootstrap/runtime_session.py`
- current_run: `RUN-007`

State layer:
- mode: `SQLite-first`
- schema: `state/sqlite_schema.sql`
- live_db: `state/runtime_state.sqlite`
- live_db_status: present and queryable
- activation_run: `RUN-002`

Run ledger:
- `RUN-001` | benchmark: `GT-001` | status: `completed` | summary: `runs/RUN-001_GT-001_summary.md`
- `RUN-002` | benchmark: `GT-001` | status: `completed` | summary: `runs/RUN-002_state_activation_summary.md`
- `RUN-003` | benchmark: `GT-001` | status: `completed` | summary: `runs/RUN-003_state_projection_sync_summary.md`
- `RUN-004` | benchmark: `GT-001` | status: `completed` | summary: `runs/RUN-004_dashboard_projection_extension_summary.md`
- `RUN-005` | benchmark: `GT-001` | status: `completed` | summary: `runs/RUN-005_projection_watcher_refresh_summary.md`
- `RUN-006` | benchmark: `GT-001` | status: `completed` | summary: `runs/RUN-006_projection_watcher_runtime_session_summary.md`
- `RUN-007` | benchmark: `GT-001` | status: `completed` | summary: `runs/RUN-007_projection_watcher_adaptive_refresh_summary.md`

Roles:
- `RUN-001` | `7` roles recorded | status: `complete`
- `RUN-002` | `7` roles recorded | status: `complete`
- `RUN-003` | `7` roles recorded | status: `complete`
- `RUN-004` | `7` roles recorded | status: `complete`
- `RUN-005` | `7` roles recorded | status: `complete`
- `RUN-006` | `7` roles recorded | status: `complete`
- `RUN-007` | `7` roles recorded | status: `complete`

Work items:
- `WI-001` | run: `RUN-001` | stage: `archived` | status: `complete` | product brief: `product/active_product_briefs/PB-001_GT-001.md` | engineering spec: `engineering/ES-001_GT-001.md`
- `WI-002` | run: `RUN-002` | stage: `learning` | status: `complete` | product brief: `product/active_product_briefs/PB-002_RUN-002_state_activation.md` | engineering spec: `engineering/ES-002_RUN-002_state_activation.md`
- `WI-003` | run: `RUN-003` | stage: `learning` | status: `complete` | product brief: `product/active_product_briefs/PB-003_RUN-003_state_projection_sync.md` | engineering spec: `engineering/ES-003_RUN-003_state_projection_sync.md`
- `WI-004` | run: `RUN-004` | stage: `learning` | status: `complete` | product brief: `product/active_product_briefs/PB-004_RUN-004_dashboard_projection_extension.md` | engineering spec: `engineering/ES-004_RUN-004_dashboard_projection_extension.md`
- `WI-005` | run: `RUN-005` | stage: `learning` | status: `complete` | product brief: `product/active_product_briefs/PB-005_RUN-005_projection_watcher_refresh.md` | engineering spec: `engineering/ES-005_RUN-005_projection_watcher_refresh.md`
- `WI-006` | run: `RUN-006` | stage: `learning` | status: `complete` | product brief: `product/active_product_briefs/PB-006_RUN-006_projection_watcher_runtime_session.md` | engineering spec: `engineering/ES-006_RUN-006_projection_watcher_runtime_session.md`
- `WI-007` | run: `RUN-007` | stage: `learning` | status: `complete` | product brief: `product/active_product_briefs/PB-007_RUN-007_projection_watcher_adaptive_refresh.md` | engineering spec: `engineering/ES-007_RUN-007_projection_watcher_adaptive_refresh.md`

Handoffs:
- `RUN-001` | `H-001` .. `H-006` | count: `6` | log: `execution/handoff_log.md`
- `RUN-002` | `H-007` .. `H-012` | count: `6` | log: `execution/handoff_log.md`
- `RUN-003` | `H-013` .. `H-018` | count: `6` | log: `execution/handoff_log.md`
- `RUN-004` | `H-019` .. `H-024` | count: `6` | log: `execution/handoff_log.md`
- `RUN-005` | `H-025` .. `H-030` | count: `6` | log: `execution/handoff_log.md`
- `RUN-006` | `H-031` .. `H-036` | count: `6` | log: `execution/handoff_log.md`
- `RUN-007` | `H-037` .. `H-042` | count: `6` | log: `execution/handoff_log.md`

Representative artifacts registered in SQLite:
- `product/active_product_briefs/PB-001_GT-001.md`
- `engineering/ES-001_GT-001.md`
- `execution/work_orders/WO-001_GT-001.md`
- `evaluation/benchmark_results.md`
- `state/state_registry.md`
- `state/runtime_state.sqlite`
- `product/active_product_briefs/PB-002_RUN-002_state_activation.md`
- `engineering/ES-002_RUN-002_state_activation.md`
- `execution/work_orders/WO-002_RUN-002_state_activation.md`
- `runs/RUN-002_state_activation_summary.md`
- `evaluation/RUN-002_state_activation_evaluation.md`
- `product/active_product_briefs/PB-003_RUN-003_state_projection_sync.md`
- `engineering/ES-003_RUN-003_state_projection_sync.md`
- `execution/work_orders/WO-003_RUN-003_state_projection_sync.md`
- `state/sync_projections.py`
- `state/state_registry.md`
- `intake/demand_queue.md`
- `execution/status_board.md`
- `runs/RUN-003_state_projection_sync_summary.md`
- `evaluation/RUN-003_state_projection_sync_evaluation.md`
- `product/active_product_briefs/PB-004_RUN-004_dashboard_projection_extension.md`
- `engineering/ES-004_RUN-004_dashboard_projection_extension.md`
- `execution/work_orders/WO-004_RUN-004_dashboard_projection_extension.md`
- `state/sync_projections.py`
- `evaluation/benchmark_results.md`
- `evaluation/process_audits.md`
- `evaluation/metric_dashboard.md`
- `evolution/improvement_backlog.md`
- `evolution/change_proposals.md`
- `evolution/approved_changes.md`
- `runs/RUN-004_dashboard_projection_extension_summary.md`
- `evaluation/RUN-004_dashboard_projection_extension_evaluation.md`
- `product/active_product_briefs/PB-005_RUN-005_projection_watcher_refresh.md`
- `engineering/ES-005_RUN-005_projection_watcher_refresh.md`
- `execution/work_orders/WO-005_RUN-005_projection_watcher_refresh.md`
- `state/sync_projections.py`
- `state/watch_projections.py`
- `runs/RUN-005_projection_watcher_refresh_summary.md`
- `evaluation/RUN-005_projection_watcher_refresh_evaluation.md`
- `product/active_product_briefs/PB-006_RUN-006_projection_watcher_runtime_session.md`
- `engineering/ES-006_RUN-006_projection_watcher_runtime_session.md`
- `execution/work_orders/WO-006_RUN-006_projection_watcher_runtime_session.md`
- `bootstrap/runtime_session.py`
- `state/watch_projections.py`
- `state/sync_projections.py`
- `bootstrap/startup_sequence.md`
- `runs/RUN-006_projection_watcher_runtime_session_summary.md`
- `evaluation/RUN-006_projection_watcher_runtime_session_evaluation.md`
- `product/active_product_briefs/PB-007_RUN-007_projection_watcher_adaptive_refresh.md`
- `engineering/ES-007_RUN-007_projection_watcher_adaptive_refresh.md`
- `execution/work_orders/WO-007_RUN-007_projection_watcher_adaptive_refresh.md`
- `bootstrap/runtime_session.py`
- `state/watch_projections.py`
- `state/README.md`
- `state/storage_strategy.md`
- `bootstrap/startup_sequence.md`
- `runs/RUN-007_projection_watcher_adaptive_refresh_summary.md`
- `evaluation/RUN-007_projection_watcher_adaptive_refresh_evaluation.md`
- `evaluation/GT-001_autonomous_cycle_completion_package.md`

SQLite row counts:
- `organization_runs`: `7`
- `roles`: `49`
- `work_items`: `7`
- `handoff_events`: `42`
- `artifact_registry`: `59`
- `benchmark_runs`: `7`
- `audit_findings`: `6`
- `improvement_backlog`: `6`
- `change_proposals`: `6`
- `approved_changes`: `6`
- `state_variables`: `22`

State variables:
- `planning.closeout_status = comparison_package_prepared`
- `planning.completion_package_path = evaluation/GT-001_autonomous_cycle_completion_package.md`
- `planning.next_recommended_run = none`
- `planning.open_improvement_items = 0`
- `runtime.current_run = RUN-007`
- `runtime.last_completed_run = RUN-007`
- `state.last_projection_at = 2026-03-17 13:27:52 PDT`
- `state.live_db_path = agent_org/state/runtime_state.sqlite`
- `state.projection_refresh_mode = watcher`
- `state.projection_script = agent_org/state/sync_projections.py`
- `state.projection_targets = state/state_registry.md,intake/demand_queue.md,execution/status_board.md,evaluation/benchmark_results.md,evaluation/process_audits.md,evaluation/metric_dashboard.md,evolution/improvement_backlog.md,evolution/change_proposals.md,evolution/approved_changes.md`
- `state.projection_watcher_last_exit_code = 0`
- `state.projection_watcher_launch_mode = bootstrap/runtime_session.py`
- `state.projection_watcher_max_poll_interval_seconds = 2.0`
- `state.projection_watcher_pid = none`
- `state.projection_watcher_poll_backoff_factor = 2.0`
- `state.projection_watcher_poll_interval_seconds = 0.5`
- `state.projection_watcher_script = agent_org/state/watch_projections.py`
- `state.projection_watcher_started_at = 2026-03-17 13:17:22 PDT`
- `state.projection_watcher_status = stopped`
- `state.projection_watcher_stopped_at = 2026-03-17 13:17:24 PDT`
- `state.registry_status = in_sync`

Update rules:
- Write operational changes to SQLite first.
- Regenerate this file with `python3 state/sync_projections.py`.
- Treat SQLite as the operational source and this registry as its readable projection.
