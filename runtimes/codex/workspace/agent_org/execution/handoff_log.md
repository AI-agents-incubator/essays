# Handoff Log

Purpose: record role-to-role transitions.

Owner: `review-and-integration-agent`

Handoffs:
- `H-001` | from: business-sponsor-interface | to: product-lead | artifact: `product/active_product_briefs/PB-001_GT-001.md`
- `H-002` | from: product-lead | to: engineering-manager | artifact: `engineering/ES-001_GT-001.md`
- `H-003` | from: engineering-manager | to: implementation-agent | artifact: `execution/work_orders/WO-001_GT-001.md`
- `H-004` | from: implementation-agent | to: review-and-integration-agent | artifact: `execution/integration_log.md`
- `H-005` | from: review-and-integration-agent | to: benchmark-and-audit-agent | artifact: `evaluation/benchmark_results.md`
- `H-006` | from: benchmark-and-audit-agent | to: learning-agent | artifact: `evolution/improvement_backlog.md`

Update rules:
- Append-only.
- Each handoff must reference a concrete artifact.
