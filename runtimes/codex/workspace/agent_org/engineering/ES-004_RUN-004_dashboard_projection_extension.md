# Engineering Spec: ES-004 RUN-004 Dashboard Projection Extension

Work item ID: `WI-004`
Owner: `engineering-manager`
Status: complete

Scope summary:
Extend the SQLite-first projection path so evaluation and evolution dashboard markdown is generated from live state, while keeping markdown as the readable control plane.

Non-goals:
- Introducing background automation beyond the manual `sync_projections.py` command.
- Reworking completed `RUN-001` to `RUN-003` artifacts beyond what is needed for projection coverage and state continuity.
- Modifying `core/`, `comparison/`, or the Claude Code sandbox.

Required artifacts:
- `state/sqlite_schema.sql`
- `state/sync_projections.py`
- `evaluation/benchmark_results.md`
- `evaluation/process_audits.md`
- `evaluation/metric_dashboard.md`
- `evolution/improvement_backlog.md`
- `evolution/change_proposals.md`
- `evolution/approved_changes.md`
- `execution/work_orders/WO-004_RUN-004_dashboard_projection_extension.md`
- `runs/RUN-004_dashboard_projection_extension_summary.md`
- `evaluation/RUN-004_dashboard_projection_extension_evaluation.md`

State layer requirements:
- Extend the local schema with the minimum entities needed to represent improvement backlog items and approved changes.
- Register `RUN-004`, `WI-004`, roles, handoffs, artifacts, benchmark updates, and learning updates in SQLite before projecting markdown.
- Record the expanded projection target inventory in `state_variables`.

Task breakdown:
1. Extend the local SQLite schema for evaluation/evolution projection coverage.
2. Register `RUN-004` operational state and backfill any missing evolution metadata needed for generation.
3. Extend `state/sync_projections.py` to render evaluation and evolution dashboards from live SQLite data.
4. Regenerate the expanded projection set and verify it with `--check`.
5. Publish `RUN-004` summary, evaluation trace, and the next learning-oriented recommendation.

Acceptance criteria:
- `python3 workspace/agent_org/state/sync_projections.py --check` passes.
- Evaluation and evolution dashboard markdown is derived from SQLite-backed records rather than manual rollups.
- `IM-003` is marked complete and the new projection inventory is explicit in the run trace.
- `RUNTIME_STATUS.md` and `RUNTIME_ACK.md` both end in a completed state for `OBS-CODEX-003`.

Handoffs:
- `engineering-manager -> implementation-agent`
