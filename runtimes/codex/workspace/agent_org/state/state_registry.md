# State Registry

Purpose: map operational entities to artifacts and run context.

Owner: `engineering-manager`

Run:
- id: `RUN-001`
- runtime: `codex`
- benchmark: `GT-001`
- summary: `runtimes/codex/runs/RUN-001_GT-001_summary.md`

Roles:
- `business-sponsor-interface` | status: complete
- `product-lead` | status: complete
- `engineering-manager` | status: complete
- `implementation-agent` | status: complete
- `review-and-integration-agent` | status: complete
- `benchmark-and-audit-agent` | status: complete
- `learning-agent` | status: complete

Work items:
- `WI-001` | stage: evaluation | status: complete | product brief: `product/active_product_briefs/PB-001_GT-001.md`

Artifacts (representative):
- product brief: `product/active_product_briefs/PB-001_GT-001.md`
- engineering spec: `engineering/ES-001_GT-001.md`
- task graph: `engineering/task_graph.md`
- work order: `execution/work_orders/WO-001_GT-001.md`
- handoff log: `execution/handoff_log.md`
- benchmark results: `evaluation/benchmark_results.md`

Update rules:
- Sync after each run and benchmark.
