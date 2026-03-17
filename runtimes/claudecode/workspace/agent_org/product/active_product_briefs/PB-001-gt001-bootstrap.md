# Product Brief PB-001

brief id: PB-001
problem statement: Claude Code sandbox needs a minimal, operational agent organization scaffold.
goal: implement GT-001 requirements inside the sandbox with traceable artifacts.
scope: create required folders, core artifacts, runtime files, state layer, and traces.
constraints: write only inside `runtimes/claudecode/{workspace,runs,evaluation}`.
success criteria:
- all required artifacts exist and are linked across stages
- state layer is SQLite-first and ready for persistence
- run summary and evaluation trace are recorded
required artifacts:
- product brief, engineering spec, task graph, work order, handoff log, integration log
handoff target: engineering-manager
