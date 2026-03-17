# Local Storage Strategy

This runtime uses SQLite-first storage for operational state.

Why:
- local sandbox compatibility
- reproducible GT-001 runs
- minimal infrastructure overhead

Migration path:
- see `supabase_migration_path.md`
