# Supabase Migration Path

Purpose: outline migration from local SQLite to a managed Postgres backend.

Owner: `engineering-manager`

Migration steps:
1. Export SQLite schema and data.
2. Map tables to Supabase/Postgres.
3. Validate constraints and indexes.
4. Update runtime configuration to point at Supabase.
5. Keep artifact layer unchanged.

Readiness criteria:
- Stable schema used across multiple runs.
- Need for multi-agent or long-lived persistence.
