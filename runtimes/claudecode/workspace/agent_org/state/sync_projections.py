#!/usr/bin/env python3
"""
sync_projections.py — Hook-driven state sync for Claude Code agent_org sandbox.

Syncs state between:
  - SQLite DB (runtime_state.sqlite)      — operational memory
  - Markdown governance layer             — explainable control plane

Commands:
  run_start     --run-id ID --benchmark BENCH
  run_end       --run-id ID --status STATUS --summary-path PATH
  check_consistency
  show_state
"""

import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR / "runtime_state.sqlite"
RUNTIME_STATUS_PATH = (SCRIPT_DIR / "../../../runs/RUNTIME_STATUS.md").resolve()


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def get_db() -> sqlite3.Connection:
    if not DB_PATH.exists():
        print(f"ERROR: DB not found at {DB_PATH}", file=sys.stderr)
        print("Run: sqlite3 runtime_state.sqlite < sqlite_schema.sql", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def read_runtime_status_field(field: str):
    if not RUNTIME_STATUS_PATH.exists():
        return None
    text = RUNTIME_STATUS_PATH.read_text()
    pattern = rf"^- {re.escape(field)}:\s*`?([^`\n]+)`?\s*$"
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else None


def cmd_run_start(run_id: str, benchmark: str) -> None:
    conn = get_db()
    ts = now_iso()
    work_item_id = f"WI-{run_id.replace('RUN-', '')}"

    conn.execute(
        "INSERT INTO organization_runs (id, runtime, benchmark_id, status, started_at) "
        "VALUES (?, 'claude-code', ?, 'in_progress', ?) "
        "ON CONFLICT(id) DO UPDATE SET status='in_progress', started_at=excluded.started_at",
        (run_id, benchmark, ts),
    )
    conn.execute(
        "INSERT INTO work_items (id, run_id, source_signal, current_stage, priority, status, updated_at) "
        "VALUES (?, ?, ?, 'in_progress', 'high', 'in_progress', ?) "
        "ON CONFLICT(id) DO UPDATE SET status='in_progress', updated_at=excluded.updated_at",
        (work_item_id, run_id, benchmark, ts),
    )
    conn.execute(
        "INSERT INTO state_variables (scope, key, value, runtime, run_id, updated_at) "
        "VALUES ('global', 'latest_run', ?, 'claude-code', ?, ?) "
        "ON CONFLICT(scope, key) DO UPDATE SET value=excluded.value, run_id=excluded.run_id, updated_at=excluded.updated_at",
        (run_id, run_id, ts),
    )
    conn.commit()
    conn.close()
    print(f"run_start: {run_id} registered in DB at {ts}")


def cmd_run_end(run_id: str, status: str, summary_path: str) -> None:
    conn = get_db()
    ts = now_iso()
    work_item_id = f"WI-{run_id.replace('RUN-', '')}"

    conn.execute(
        "UPDATE organization_runs SET status=?, finished_at=?, summary_path=? WHERE id=?",
        (status, ts, summary_path, run_id),
    )
    conn.execute(
        "UPDATE work_items SET status='done', current_stage='done', updated_at=? WHERE id=?",
        (ts, work_item_id),
    )
    conn.execute(
        "INSERT INTO state_variables (scope, key, value, runtime, run_id, updated_at) "
        "VALUES ('global', 'last_completed_run', ?, 'claude-code', ?, ?) "
        "ON CONFLICT(scope, key) DO UPDATE SET value=excluded.value, run_id=excluded.run_id, updated_at=excluded.updated_at",
        (run_id, run_id, ts),
    )
    conn.commit()
    conn.close()
    print(f"run_end: {run_id} marked {status} in DB at {ts}")


def cmd_check_consistency() -> None:
    conn = get_db()
    row = conn.execute(
        "SELECT value FROM state_variables WHERE scope='global' AND key='latest_run'"
    ).fetchone()
    conn.close()
    db_run = row["value"] if row else None
    md_run = read_runtime_status_field("current_run")

    if db_run == md_run:
        print(f"OK: DB and RUNTIME_STATUS agree — current_run = {db_run}")
    else:
        print(f"SYNC_DRIFT: DB latest_run={db_run!r}, RUNTIME_STATUS current_run={md_run!r}")
        sys.exit(2)


def cmd_show_state() -> None:
    conn = get_db()
    runs = [dict(r) for r in conn.execute("SELECT * FROM organization_runs ORDER BY started_at")]
    variables = [dict(r) for r in conn.execute("SELECT * FROM state_variables ORDER BY scope, key")]
    work_items = [dict(r) for r in conn.execute("SELECT id, run_id, status FROM work_items ORDER BY run_id")]
    conn.close()
    print(json.dumps({"organization_runs": runs, "state_variables": variables, "work_items": work_items}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="agent_org state sync")
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("run_start")
    p_start.add_argument("--run-id", required=True)
    p_start.add_argument("--benchmark", required=True)

    p_end = sub.add_parser("run_end")
    p_end.add_argument("--run-id", required=True)
    p_end.add_argument("--status", required=True)
    p_end.add_argument("--summary-path", required=True)

    sub.add_parser("check_consistency")
    sub.add_parser("show_state")

    args = parser.parse_args()
    if args.command == "run_start":
        cmd_run_start(args.run_id, args.benchmark)
    elif args.command == "run_end":
        cmd_run_end(args.run_id, args.status, args.summary_path)
    elif args.command == "check_consistency":
        cmd_check_consistency()
    elif args.command == "show_state":
        cmd_show_state()


if __name__ == "__main__":
    main()
