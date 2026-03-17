# Decision Log

| id | decision | rationale |
| --- | --- | --- |
| D-001 | SQLite-first state layer | matches core storage strategy and enables local sandbox testing |
| D-002 | Keep artifacts minimal but complete | GT-001 requires full structure without essays |
| D-003 | Seed live DB with RUN-001 history on first activation | preserves continuity; state layer is operational memory, not just schema |
| D-004 | Implement hook layer as Python script (not bash) | stdlib-only, no external deps; consistent with existing framework-core rationale; easy to extend |
| D-005 | Consistency invariant checks both DB and markdown simultaneously | dual-layer architecture requires dual-layer validation to catch drift |
