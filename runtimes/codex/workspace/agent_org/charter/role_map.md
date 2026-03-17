# Role Map

Purpose: define the minimal role set and their handoffs.

Owner: `engineering-manager`

Roles (invariant):
1. `business-sponsor-interface`
2. `product-lead`
3. `engineering-manager`
4. `implementation-agent`
5. `review-and-integration-agent`
6. `benchmark-and-audit-agent`
7. `learning-agent`

Primary handoffs:
- `business-sponsor-interface -> product-lead`
- `product-lead -> engineering-manager`
- `engineering-manager -> implementation-agent`
- `implementation-agent -> review-and-integration-agent`
- `review-and-integration-agent -> benchmark-and-audit-agent`
- `benchmark-and-audit-agent -> learning-agent`

Role linkage:
- Each role owns one or more artifacts in `product/`, `engineering/`, `execution/`, `evaluation/`, `evolution/`.
- Roles are tracked in `state/state_registry.md` and the SQLite state layer.

Update rules:
- Changes require a change proposal and approval.
- Update `execution/handoff_log.md` if handoff rules change.

Links:
- `execution/handoff_log.md`
- `state/state_registry.md`
