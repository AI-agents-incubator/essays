# Autonomy Model

Purpose: define how autonomy is granted and controlled.

Owner: `engineering-manager`

Autonomy levels:
- Level 0: read-only audit.
- Level 1: create/modify artifacts within scope.
- Level 2: spawn roles and execute full cycle within scope.
- Level 3: propose structural changes (requires approval).

Default for GT-001:
- Level 2 for implementation and integration roles.
- Level 1 for learning and audit roles.
- Level 3 reserved for `business-sponsor-interface`.

Guardrails:
- No writes outside `runtimes/codex/`.
- No changes to `core/` or `comparison/`.
- All structural changes require `evolution/change_proposals.md`.

Update rules:
- Proposed by `engineering-manager`, approved by `business-sponsor-interface`.

Links:
- `policies/escalation_policy.md`
- `policies/quality_gates.md`
