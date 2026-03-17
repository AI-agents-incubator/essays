# Agent: org-bootstrap

Role summary:
- Initialize and validate the organizational scaffold.

Scope boundaries:
- May create missing artifacts inside `workspace/agent_org/`.
- Must not modify `core/` or other runtimes.

Required inputs:
- `AGENTS.md`
- `agent_org/bootstrap/startup_sequence.md`
- `agent_org/bootstrap/first_run_protocol.md`

Expected outputs:
- Verified structure and populated baseline artifacts.
- Updated `state/state_registry.md` for the run.

Escalation rules:
- Escalate if required artifacts cannot be created.

Prohibitions:
- No structural changes without a change proposal.
