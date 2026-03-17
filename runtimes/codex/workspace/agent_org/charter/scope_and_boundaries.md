# Scope and Boundaries

Purpose: define what this organization does and does not do.

Owner: `product-lead`

In scope:
- Maintain an artifact-based operating system for agent work.
- Execute the full cycle from intake to learning.
- Track operational state in a local SQLite-first layer.

Out of scope:
- Editing `core/` or `comparison/` source of truth.
- Writing outside `runtimes/codex/`.
- Shipping software artifacts beyond the organizational infrastructure.

Boundary rules:
- All outputs must map to `agent_org/` artifacts or runtime traces.
- Any new structure requires an entry in `evolution/change_proposals.md`.

Update rules:
- Proposed by `product-lead`, approved by `business-sponsor-interface`.
- Log changes in `knowledge/decision_log.md`.

Links:
- `policies/quality_gates.md`
- `policies/artifact_change_policy.md`
