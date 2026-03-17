# Local State Storage Strategy

Purpose: define the SQLite-first storage approach for this sandbox.

Owner: `engineering-manager`

Strategy:
- Use a local SQLite database for operational state.
- Keep schema in `sqlite_schema.sql`.
- Treat markdown artifacts as the control plane.
- Do not store policy text inside the database.

Operational rules:
- Each run must insert a record in `organization_runs`.
- Roles and handoffs must be traceable to artifacts.
- State variables are for transient operational values.

Migration:
- Follow `supabase_migration_path.md` when moving to Postgres/Supabase.
