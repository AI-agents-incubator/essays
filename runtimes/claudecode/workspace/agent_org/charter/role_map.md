# Role Map

Core roles required by GT-001:
- business-sponsor-interface: provides the initial demand signal.
- product-lead: converts demand into a product brief.
- engineering-manager: converts product brief into engineering spec and task graph.
- implementation-agent: executes work orders.
- review-and-integration-agent: verifies outputs and logs integration.
- benchmark-and-audit-agent: runs GT-001 audit and logs benchmark results.
- learning-agent: records gaps and improvement proposals.

Claude Code runtime mapping:
- org-bootstrap -> business-sponsor-interface (intake + bootstrap orchestration)
- product-lead -> product-lead
- engineering-manager -> engineering-manager
- implementation-agent -> engineering-manager (delegated in work orders)
- integration-reviewer -> review-and-integration-agent
- benchmark-auditor -> benchmark-and-audit-agent
- learning-coordinator -> learning-agent

Primary artifact ownership:
- Product brief: product-lead
- Engineering spec + task graph: engineering-manager
- Work orders + status board: implementation-agent (delegated)
- Integration log: integration-reviewer
- Benchmark results + process audit: benchmark-auditor
- Improvement backlog: learning-coordinator
