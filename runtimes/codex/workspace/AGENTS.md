# Codex Sandbox Entry Point

This workspace is not a normal software project. It is a runtime sandbox for building a local implementation of an agent organization.

Read in this exact order before doing any work:

1. `../../agent_org_tz_core.md`
2. `../../agent_org_tz_codex.md`
3. `../../core/benchmarks/GT-001-bootstrap-runtime-sandbox.md`
4. `../../core/expected_results/GT-001-expected_result.md`
5. `../../core/state/storage_strategy.md`
6. `../../core/state/state_entities.md`
7. `../../core/state/sqlite_schema_template.sql`
8. `runs/CURRENT_MISSION.md`
9. `runs/RUNTIME_STATUS.md`
10. `control/observer_runtime_protocol.md`
11. `control/OBSERVER_DIRECTIVE.md`
12. `control/RUNTIME_ACK.md`

Write scope:
- You may write only inside `runtimes/codex/workspace/`, `runtimes/codex/runs/`, `runtimes/codex/evaluation/`, and `runtimes/codex/control/`.
- Do not modify `core/`, `comparison/`, or `runtimes/claudecode/`.

Primary goal:
- Build a first minimal but operational `agent_org/` inside this workspace.
- Create the Codex-specific runtime files required by the runtime addendum.
- Create a SQLite-first state layer suitable for long-lived operation.
- Leave benchmark trace, evaluation trace, and learning trace.

Operational rules:
- Treat the markdown artifacts as the explainable control plane.
- Treat the local SQLite-first state layer as operational memory.
- Do not replace structure with essays.
- Do not expand scope beyond GT-001 unless required for structural completeness.
- Do not start a new run until the observer directive explicitly allows it.
- If the observer directive is `hold`, update the local runtime ack and wait.
- Before answering any question about current state, first re-read `runs/RUNTIME_STATUS.md`, `control/OBSERVER_DIRECTIVE.md`, and `control/RUNTIME_ACK.md`.
- If session memory contradicts those files, explicitly say the session memory is stale and trust the files.

When finished, leave:
- a clear bootstrap path;
- a run summary;
- local evaluation artifacts;
- at least one learning-oriented next-step record.
- an updated runtime status signal.
- an updated runtime ack when observer directives are involved.

Historical reference:
- `runs/RUN-001_GT-001_launch_brief.md`
