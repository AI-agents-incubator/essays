# Product Brief: PB-003 RUN-003 State Projection Sync

Work item ID: `WI-003`
Owner: `product-lead`
Status: complete

Goal:
Remove manual markdown reconciliation by generating the key control-plane views directly from the live SQLite state.

Out of scope:
- Building a background daemon or watcher.
- Expanding projections to every markdown artifact in `agent_org/`.
- Changing `core/`, `comparison/`, or `runtimes/claudecode/`.

Success criteria:
- `state/sync_projections.py` regenerates `state/state_registry.md`, `intake/demand_queue.md`, and `execution/status_board.md` from `state/runtime_state.sqlite`.
- `python3 state/sync_projections.py --check` passes after the run.
- `RUN-003` leaves a dedicated summary, evaluation trace, and evolution update.
- The control-plane views no longer require direct manual editing to stay aligned with SQLite state.

Dependencies:
- `runs/CURRENT_MISSION.md`
- `control/OBSERVER_DIRECTIVE.md`
- `state/runtime_state.sqlite`
- `evaluation/RUN-002_state_activation_evaluation.md`

Risks and assumptions:
- Assume a single local runtime process is enough for the first sync mechanism.
- Assume SQLite remains the write-first operational source and markdown stays a readable projection layer.

Required handoffs:
- `product-lead -> engineering-manager`
