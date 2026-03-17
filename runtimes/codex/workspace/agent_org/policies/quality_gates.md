# Quality Gates

Purpose: define minimal checks before a cycle is considered complete.

Owner: `benchmark-and-audit-agent`

Gate 1: Artifact completeness
- All required GT-001 files exist.
- Templates include purpose, owner, required fields, update rules, links.

Gate 2: Process trace
- One product brief, engineering spec, task graph, work order, handoff log, integration log.

Gate 3: State layer readiness
- SQLite schema present and referenced.
- State registry lists run, roles, work item, artifacts.

Gate 4: Evaluation and learning
- Benchmark result recorded.
- Process audit recorded.
- At least one learning entry in `evolution/improvement_backlog.md`.

Update rules:
- Proposed by `benchmark-and-audit-agent`, approved by `engineering-manager`.
