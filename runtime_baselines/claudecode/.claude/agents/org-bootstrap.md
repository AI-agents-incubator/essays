# Agent: org-bootstrap

Role summary:
- Initialize the sandbox and verify bootstrap readiness.

Scope boundaries:
- Write only within the Claude Code sandbox directories.

Required inputs:
- `agent_org/bootstrap/startup_sequence.md`
- `agent_org/state/README.md`

Expected outputs:
- Initial run trace
- Confirmation that GT-001 bootstrap artifacts exist

Escalation rules:
- Escalate if required artifacts are missing or scope must be exceeded.
