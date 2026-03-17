# Claude Code Sandbox Entry Point

This workspace is not a normal software project. It is a runtime sandbox for building a local implementation of an agent organization.

Read in this exact order before doing any work:

1. `../../../agent_org_tz_core.md`
2. `../../../agent_org_tz_claudecode.md`
3. `../../../core/benchmarks/GT-001-bootstrap-runtime-sandbox.md`
4. `../../../core/expected_results/GT-001-expected_result.md`
5. `../../../core/state/storage_strategy.md`
6. `../../../core/state/state_entities.md`
7. `../../../core/state/sqlite_schema_template.sql`
8. `../runs/CURRENT_MISSION.md`

Write scope:
- You may write only inside `runtimes/claudecode/workspace/`, `runtimes/claudecode/runs/`, and `runtimes/claudecode/evaluation/`.
- Do not modify `core/`, `comparison/`, or `runtimes/codex/`.

Primary goal:
- Build a first minimal but operational `agent_org/` inside this workspace.
- Create the Claude Code-specific runtime files required by the runtime addendum.
- Create a SQLite-first state layer suitable for long-lived operation.
- Leave benchmark trace, evaluation trace, and learning trace.

Operational rules:
- Treat the markdown artifacts as the explainable control plane.
- Treat the local SQLite-first state layer as operational memory.
- Do not replace structure with essays.
- Do not expand scope beyond GT-001 unless required for structural completeness.

When finished, leave:
- a clear bootstrap path;
- a run summary;
- local evaluation artifacts;
- at least one learning-oriented next-step record.

Bootstrap entrypoints:
- `agent_org/bootstrap/startup_sequence.md`
- `agent_org/bootstrap/first_run_protocol.md`

Historical reference:
- `../runs/RUN-001_GT-001_launch_brief.md`
