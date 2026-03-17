-- SQLite-first schema for GT-001 runtime sandbox testing
-- Minimal operational traceability schema

CREATE TABLE IF NOT EXISTS organization_runs (
  id TEXT PRIMARY KEY,
  runtime TEXT NOT NULL,
  benchmark_id TEXT NOT NULL,
  status TEXT NOT NULL,
  started_at TEXT NOT NULL,
  finished_at TEXT,
  summary_path TEXT
);

CREATE TABLE IF NOT EXISTS roles (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  role_type TEXT NOT NULL,
  scope TEXT,
  status TEXT NOT NULL,
  owner_context TEXT,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (run_id) REFERENCES organization_runs(id)
);

CREATE TABLE IF NOT EXISTS work_items (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  source_signal TEXT NOT NULL,
  current_stage TEXT NOT NULL,
  product_brief_path TEXT,
  engineering_spec_path TEXT,
  priority TEXT,
  status TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (run_id) REFERENCES organization_runs(id)
);

CREATE TABLE IF NOT EXISTS handoff_events (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  work_item_id TEXT NOT NULL,
  from_role TEXT NOT NULL,
  to_role TEXT NOT NULL,
  status TEXT NOT NULL,
  artifact_path TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (run_id) REFERENCES organization_runs(id),
  FOREIGN KEY (work_item_id) REFERENCES work_items(id)
);

CREATE TABLE IF NOT EXISTS artifact_registry (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  work_item_id TEXT,
  artifact_type TEXT NOT NULL,
  path TEXT NOT NULL,
  version TEXT,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (run_id) REFERENCES organization_runs(id),
  FOREIGN KEY (work_item_id) REFERENCES work_items(id)
);

CREATE TABLE IF NOT EXISTS benchmark_runs (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  benchmark_id TEXT NOT NULL,
  expected_result_version TEXT NOT NULL,
  status TEXT NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (run_id) REFERENCES organization_runs(id)
);

CREATE TABLE IF NOT EXISTS audit_findings (
  id TEXT PRIMARY KEY,
  benchmark_run_id TEXT NOT NULL,
  severity TEXT NOT NULL,
  category TEXT NOT NULL,
  description TEXT NOT NULL,
  recommendation TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (benchmark_run_id) REFERENCES benchmark_runs(id)
);

CREATE TABLE IF NOT EXISTS change_proposals (
  id TEXT PRIMARY KEY,
  source_finding_id TEXT,
  target_artifact TEXT NOT NULL,
  proposal_type TEXT NOT NULL,
  expected_effect TEXT,
  status TEXT NOT NULL,
  validating_benchmark_id TEXT,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS state_variables (
  scope TEXT NOT NULL,
  key TEXT NOT NULL,
  value TEXT NOT NULL,
  runtime TEXT,
  run_id TEXT,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (scope, key)
);
