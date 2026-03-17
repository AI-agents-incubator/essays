# Supabase Migration Path

Steps:
1. Export SQLite schema into Postgres-compatible DDL.
2. Provision Supabase project and apply schema.
3. Update runtime configuration to point to Supabase.
4. Add data migration job for existing state records.
5. Keep markdown artifacts as the control plane.
