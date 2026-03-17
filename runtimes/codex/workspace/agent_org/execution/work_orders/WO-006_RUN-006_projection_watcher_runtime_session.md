# Work Order: WO-006 RUN-006 Projection Watcher Runtime Session

Work item ID: `WI-006`
Owner: `implementation-agent`
Status: complete

Scope:
- Add `bootstrap/runtime_session.py` to supervise watcher startup, command execution, and shutdown.
- Extend watcher/projection scripts so watcher lifecycle state is recorded without creating self-trigger refresh loops.
- Update bootstrap/state docs to use the supervised runtime session path.
- Register `RUN-006` operational records, benchmark findings, and learning follow-up in SQLite.
- Publish the `RUN-006` run summary, local evaluation trace, and refreshed runtime protocol files.

Checklist:
- [x] Add `bootstrap/runtime_session.py` and update bootstrap docs to route watcher-mode execution through it.
- [x] Extend `state/watch_projections.py` and `state/sync_projections.py` for watcher lifecycle metadata and clean shutdown.
- [x] Register `RUN-006`, `WI-006`, roles, handoffs, artifacts, benchmark updates, and learning updates in SQLite.
- [x] Verify the supervised runtime session refreshes projections and confirm `python3 workspace/agent_org/state/sync_projections.py --check`.
- [x] Close `IM-005`, record the next recommended improvement, and complete the runtime protocol updates.

Update rules:
- Updated by `implementation-agent`.
- Completion requires review by `review-and-integration-agent`.
