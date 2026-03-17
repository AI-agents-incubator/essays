# Product Brief: PB-002 — State Activation & Continuation Readiness

> run: RUN-002
> benchmark: GT-001 continuation
> status: approved

## Goal

Transition the Claude Code sandbox from first-scaffold (RUN-001) to operational continuation by activating the live state layer, implementing CP-001, and producing a complete RUN-002 trace.

## Scope

1. Activate SQLite DB: create `runtime_state.sqlite` and seed with RUN-001 history + RUN-002 start.
2. Implement CP-001: add explicit state initialization checklist to `bootstrap/startup_sequence.md`.
3. Produce full RUN-002 pipeline artifacts (PB, ES, WO, handoffs).
4. Update evaluation layer to reflect continuation status.
5. Record an improvement decision for RUN-003.

## Out of scope

- Changes to `core/`, `comparison/`, or `runtimes/codex/`.
- New benchmarks beyond GT-001.
- Schema changes to `sqlite_schema.sql`.

## Success criteria

- `runtime_state.sqlite` exists and contains RUN-001 and RUN-002 rows.
- `startup_sequence.md` includes state init checklist.
- All RUN-002 trace files created and linked.
- `RUNTIME_STATUS.md` shows `completed`.
