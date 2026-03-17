# Escalation Policy

Purpose: define when the organization escalates to a human sponsor.

Owner: `business-sponsor-interface`

Escalation triggers:
- Write scope conflict or ambiguity.
- Missing artifacts required by core GT-001.
- Conflicting role instructions that block progress.
- Security or compliance risk.
- Benchmark failure without a clear remediation.

Escalation path:
1. Role owner logs issue in `execution/handoff_log.md`.
2. `engineering-manager` attempts resolution.
3. If blocked, escalate to `business-sponsor-interface`.

Required escalation record:
- timestamp
- blocking reason
- attempted mitigation
- decision requested

Update rules:
- Only `business-sponsor-interface` can change triggers.
- Changes must be logged in `knowledge/decision_log.md`.
