# Dependency Map

Purpose: record dependencies between artifacts.

Owner: `engineering-manager`

Dependencies:
- Product brief -> Engineering spec -> Task graph -> Work order.
- Work order -> Status board -> Integration log.
- Integration log -> Benchmark results -> Improvement backlog.
- State registry links to all artifacts.

Update rules:
- Updated by `engineering-manager`.
- Changes must be reflected in `execution/handoff_log.md`.
