# Startup Sequence

Purpose: define how a runtime boots the organization.

Owner: `org-bootstrap` (runtime role)

Steps:
1. Read `AGENTS.md` and confirm write scope.
2. Load `agent_org/charter/*` and `policies/*`.
3. Check for missing artifacts and create them if required.
4. Load or initialize state layer using `state/sqlite_schema.sql`.
5. Register the run in `state/state_registry.md`.
6. Enter waiting mode for external signals.

Update rules:
- Updates require `learning-agent` review.
