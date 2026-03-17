# Engineering Spec: ES-007 RUN-007 Projection Watcher Adaptive Refresh

Work item ID: `WI-007`
Owner: `engineering-manager`
Status: complete

Scope summary:
Reduce watcher polling overhead by making idle checks cheaper and adaptive, while preserving the existing bootstrap-supervised watcher lifecycle and SQLite-first control plane.

Non-goals:
- Replacing the watcher with a daemon, socket service, or OS-specific file-notification stack.
- Changing `core/`, `comparison/`, or `runtimes/claudecode/`.
- Broadening `RUN-007` into a general runtime-orchestration rewrite.

Required artifacts:
- `state/watch_projections.py`
- `bootstrap/runtime_session.py`
- `state/README.md`
- `state/storage_strategy.md`
- `bootstrap/startup_sequence.md`
- `execution/work_orders/WO-007_RUN-007_projection_watcher_adaptive_refresh.md`
- `runs/RUN-007_projection_watcher_adaptive_refresh_summary.md`
- `evaluation/RUN-007_projection_watcher_adaptive_refresh_evaluation.md`

State layer requirements:
- Register `RUN-007`, `WI-007`, seven roles, six handoffs, `BR-007`, `F-006`, and `AC-006` in SQLite.
- Update runtime state variables so `runtime.current_run = RUN-007`, `runtime.last_completed_run = RUN-007`, and watcher timing configuration is visible in projections.
- Close `IM-006`, implement `CP-006`, and record the next recommended step for the observer loop.

Task breakdown:
1. Change `state/watch_projections.py` so idle loops use SQLite `PRAGMA data_version` plus adaptive backoff before recomputing the full source signature.
2. Extend `bootstrap/runtime_session.py` to read and pass adaptive watcher timing controls without changing the supervised session contract.
3. Update the directly affected bootstrap/state docs and decision trace.
4. Verify the adaptive watcher in a bounded runtime session and confirm `python3 workspace/agent_org/state/sync_projections.py --check`.
5. Register `RUN-007` operational records, learning closure, summary, evaluation, and runtime protocol completion.

Acceptance criteria:
- `python3 workspace/agent_org/bootstrap/runtime_session.py --run-id RUN-007 -- zsh -lc "python3 - <<'PY' ... PY"` runs successfully and refreshes projections after a bounded SQLite write while the watcher remains supervised.
- `python3 workspace/agent_org/state/sync_projections.py --check` passes after the `RUN-007` updates.
- `IM-006` is marked complete, `CP-006` is marked implemented, and the generated state projections show the adaptive watcher timing variables.
- `RUNTIME_STATUS.md` and `RUNTIME_ACK.md` both end in a completed state for `OBS-CODEX-006`.

Handoffs:
- `engineering-manager -> implementation-agent`
