# Work Order: WO-007 RUN-007 Projection Watcher Adaptive Refresh

Work item ID: `WI-007`
Owner: `implementation-agent`
Status: complete

Scope:
- Make the projection watcher adaptive so idle periods stop doing full source-state scans at a fixed interval.
- Preserve the supervised `bootstrap/runtime_session.py` execution path and expose the new timing controls there.
- Update bootstrap/state docs and learning records for the new watcher behavior.
- Register `RUN-007` operational records, benchmark findings, and learning closure in SQLite.
- Publish the `RUN-007` run summary, local evaluation trace, and completed runtime protocol files.

Checklist:
- [x] Update `state/watch_projections.py` to use cheap SQLite change detection plus adaptive idle backoff.
- [x] Extend `bootstrap/runtime_session.py` to pass adaptive watcher timing controls.
- [x] Update the affected bootstrap/state docs and decision trace.
- [x] Verify the adaptive watcher path and confirm `python3 workspace/agent_org/state/sync_projections.py --check`.
- [x] Register `RUN-007`, `WI-007`, roles, handoffs, benchmark updates, approved changes, and observer-protocol completion state.

Update rules:
- Updated by `implementation-agent`.
- Completion requires review by `review-and-integration-agent`.
