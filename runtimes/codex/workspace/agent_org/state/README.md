# State Layer README

Purpose: describe how the state layer supports long-lived operation.

Owner: `engineering-manager`

Scope:
- SQLite-first operational state inside this sandbox.
- Artifact layer remains the explainable control plane.

Files:
- `state_registry.md`: human-readable index of active state entities.
- `storage_strategy.md`: local storage rules and migration expectations.
- `sqlite_schema.sql`: SQLite schema used for the operational database.
- `supabase_migration_path.md`: future migration outline.

Update rules:
- Updates must align with `core/state/*` expectations.
