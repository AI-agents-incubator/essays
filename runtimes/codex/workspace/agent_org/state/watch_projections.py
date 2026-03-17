#!/usr/bin/env python3
"""Watch SQLite source state and refresh markdown projections when it changes."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import sqlite3
import sys
import time
from pathlib import Path

import sync_projections


class StopWatching(Exception):
    """Raised when the watcher is asked to shut down cleanly."""


SOURCE_QUERIES = {
    "organization_runs": """
        SELECT id, runtime, benchmark_id, status, started_at, finished_at, summary_path
        FROM organization_runs
        ORDER BY started_at, id
    """,
    "roles": """
        SELECT id, run_id, role_type, scope, status, owner_context, updated_at
        FROM roles
        ORDER BY run_id, id
    """,
    "work_items": """
        SELECT id, run_id, source_signal, current_stage, product_brief_path,
               engineering_spec_path, priority, status, updated_at
        FROM work_items
        ORDER BY id
    """,
    "handoff_events": """
        SELECT id, run_id, work_item_id, from_role, to_role, status, artifact_path, created_at
        FROM handoff_events
        ORDER BY id
    """,
    "artifact_registry": """
        SELECT id, run_id, work_item_id, artifact_type, path, version, updated_at
        FROM artifact_registry
        ORDER BY id
    """,
    "benchmark_runs": """
        SELECT id, run_id, benchmark_id, expected_result_version, status, notes, created_at
        FROM benchmark_runs
        ORDER BY id
    """,
    "audit_findings": """
        SELECT id, benchmark_run_id, severity, category, description, recommendation, created_at
        FROM audit_findings
        ORDER BY id
    """,
    "improvement_backlog": """
        SELECT id, title, source_reference, status, updated_at
        FROM improvement_backlog
        ORDER BY id
    """,
    "change_proposals": """
        SELECT id, source_finding_id, backlog_item_id, target_artifact, proposal_type,
               expected_effect, status, validating_benchmark_id, updated_at
        FROM change_proposals
        ORDER BY id
    """,
    "approved_changes": """
        SELECT id, run_id, source_reference, change_summary, status, updated_at
        FROM approved_changes
        ORDER BY id
    """,
    "state_variables": """
        SELECT scope, key, value, run_id, updated_at
        FROM state_variables
        ORDER BY scope, key
    """,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Watch SQLite source state and refresh markdown projections."
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=0.5,
        help="minimum seconds between SQLite source-state checks",
    )
    parser.add_argument(
        "--max-poll-interval",
        type=float,
        default=2.0,
        help="maximum seconds between SQLite source-state checks while idle",
    )
    parser.add_argument(
        "--poll-backoff-factor",
        type=float,
        default=2.0,
        help="multiplier used to back off toward --max-poll-interval while idle",
    )
    parser.add_argument(
        "--max-refreshes",
        type=int,
        help="stop after this many refreshes",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        help="stop watching after this many seconds",
    )
    parser.add_argument(
        "--skip-initial-sync",
        action="store_true",
        help="start from the current source signature without an initial sync",
    )
    parser.add_argument(
        "--run-id",
        help="override the run id recorded with projection metadata updates",
    )
    parser.add_argument(
        "--launch-mode",
        default="manual",
        help="metadata label for how the watcher was started",
    )
    parser.add_argument(
        "--ready-file",
        help="touch this file after the watcher is ready to observe source-state changes",
    )
    args = parser.parse_args()

    if args.poll_interval <= 0:
        parser.error("--poll-interval must be greater than zero")
    if args.max_poll_interval <= 0:
        parser.error("--max-poll-interval must be greater than zero")
    if args.max_poll_interval < args.poll_interval:
        parser.error("--max-poll-interval must be greater than or equal to --poll-interval")
    if args.poll_backoff_factor < 1:
        parser.error("--poll-backoff-factor must be greater than or equal to one")
    if args.max_refreshes is not None and args.max_refreshes <= 0:
        parser.error("--max-refreshes must be greater than zero")
    if args.timeout_seconds is not None and args.timeout_seconds <= 0:
        parser.error("--timeout-seconds must be greater than zero")

    return args


def install_signal_handlers() -> None:
    def handle_stop(_signum: int, _frame: object) -> None:
        raise StopWatching()

    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)


def update_watcher_state(
    state_dir: Path,
    *,
    run_id: str | None,
    status: str,
    launch_mode: str,
    pid: int | None = None,
    exit_code: int | None = None,
) -> None:
    applied_at = sync_projections.current_timestamp()
    conn = sync_projections.open_connection(state_dir / "runtime_state.sqlite")
    try:
        sync_projections.upsert_state_variable(
            conn,
            "state",
            "projection_watcher_status",
            status,
            run_id,
            applied_at,
        )
        sync_projections.upsert_state_variable(
            conn,
            "state",
            "projection_watcher_launch_mode",
            launch_mode,
            run_id,
            applied_at,
        )
        if pid is not None:
            sync_projections.upsert_state_variable(
                conn,
                "state",
                "projection_watcher_pid",
                str(pid),
                run_id,
                applied_at,
            )
            sync_projections.upsert_state_variable(
                conn,
                "state",
                "projection_watcher_started_at",
                applied_at,
                run_id,
                applied_at,
            )
        else:
            sync_projections.upsert_state_variable(
                conn,
                "state",
                "projection_watcher_pid",
                "none",
                run_id,
                applied_at,
            )
            sync_projections.upsert_state_variable(
                conn,
                "state",
                "projection_watcher_stopped_at",
                applied_at,
                run_id,
                applied_at,
            )
        if exit_code is not None:
            sync_projections.upsert_state_variable(
                conn,
                "state",
                "projection_watcher_last_exit_code",
                str(exit_code),
                run_id,
                applied_at,
            )
        conn.commit()
    finally:
        conn.close()


def write_ready_file(ready_file: str | None) -> None:
    if not ready_file:
        return
    ready_path = Path(ready_file)
    ready_path.parent.mkdir(parents=True, exist_ok=True)
    ready_path.write_text("ready\n", encoding="utf-8")


def remove_ready_file(ready_file: str | None) -> None:
    if not ready_file:
        return
    ready_path = Path(ready_file)
    if ready_path.exists():
        ready_path.unlink()


def open_watch_connection(db_path: Path) -> sqlite3.Connection:
    conn = sync_projections.open_connection(db_path)
    conn.execute("PRAGMA busy_timeout = 100")
    return conn


def sqlite_data_version(conn: sqlite3.Connection) -> int:
    row = conn.execute("PRAGMA data_version").fetchone()
    assert row is not None
    return int(row[0])


def source_signature(conn: sqlite3.Connection) -> str:
    payload = {}
    for name, query in SOURCE_QUERIES.items():
        rows = [dict(row) for row in conn.execute(query)]
        if name == "state_variables":
            rows = [
                row
                for row in rows
                if (row["scope"], row["key"])
                not in sync_projections.NON_TRIGGERING_STATE_VARIABLE_KEYS
            ]
        payload[name] = rows

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def run_refresh(state_dir: Path, run_id: str | None) -> int:
    _, updated_count = sync_projections.sync_projection_targets(
        state_dir,
        check=False,
        update_state_metadata=True,
        run_id=run_id,
    )
    return updated_count


def next_poll_interval(current_interval: float, args: argparse.Namespace) -> float:
    return min(current_interval * args.poll_backoff_factor, args.max_poll_interval)


def main() -> int:
    args = parse_args()
    state_dir = Path(__file__).resolve().parent
    db_path = state_dir / "runtime_state.sqlite"
    started_at = time.monotonic()
    refreshes = 0
    exit_code = 1
    watcher_started = False
    watch_conn: sqlite3.Connection | None = None
    install_signal_handlers()

    try:
        watch_conn = open_watch_connection(db_path)
        baseline_signature = source_signature(watch_conn)
        last_data_version = sqlite_data_version(watch_conn)
        update_watcher_state(
            state_dir,
            run_id=args.run_id,
            status="running",
            launch_mode=args.launch_mode,
            pid=os.getpid(),
        )
        watcher_started = True

        if args.skip_initial_sync:
            print(
                f"watching SQLite source state from signature {baseline_signature[:12]} "
                f"with adaptive polling {args.poll_interval:.2f}s..{args.max_poll_interval:.2f}s"
            )
            last_signature = baseline_signature
        else:
            updated_count = run_refresh(state_dir, args.run_id)
            refreshes += 1
            last_signature = source_signature(watch_conn)
            last_data_version = sqlite_data_version(watch_conn)
            print(
                f"initial refresh {refreshes}: updated {updated_count} projection files "
                f"for source signature {last_signature[:12]}"
            )

        write_ready_file(args.ready_file)
        current_interval = args.poll_interval

        while True:
            if args.max_refreshes is not None and refreshes >= args.max_refreshes:
                exit_code = 0
                break
            if (
                args.timeout_seconds is not None
                and time.monotonic() - started_at >= args.timeout_seconds
            ):
                if args.max_refreshes is not None and refreshes < args.max_refreshes:
                    print(
                        "timed out before the requested number of refreshes completed",
                        file=sys.stderr,
                    )
                    exit_code = 1
                    break
                exit_code = 0
                break

            time.sleep(current_interval)

            try:
                current_data_version = sqlite_data_version(watch_conn)
            except sqlite3.OperationalError:
                current_interval = next_poll_interval(current_interval, args)
                continue

            if current_data_version == last_data_version:
                current_interval = next_poll_interval(current_interval, args)
                continue

            try:
                current_signature = source_signature(watch_conn)
            except sqlite3.OperationalError:
                current_interval = next_poll_interval(current_interval, args)
                continue
            last_data_version = current_data_version

            if current_signature == last_signature:
                current_interval = next_poll_interval(current_interval, args)
                continue

            updated_count = run_refresh(state_dir, args.run_id)
            refreshes += 1
            last_signature = source_signature(watch_conn)
            last_data_version = sqlite_data_version(watch_conn)
            current_interval = args.poll_interval
            print(
                f"refresh {refreshes}: updated {updated_count} projection files "
                f"for source signature {last_signature[:12]}"
            )
    except StopWatching:
        print("watcher received shutdown signal")
        exit_code = 0
    except sqlite3.OperationalError as exc:
        print(f"unable to read SQLite source state: {exc}", file=sys.stderr)
        exit_code = 1
    finally:
        remove_ready_file(args.ready_file)
        if watch_conn is not None:
            watch_conn.close()
        if watcher_started:
            update_watcher_state(
                state_dir,
                run_id=args.run_id,
                status="stopped" if exit_code == 0 else "failed",
                launch_mode=args.launch_mode,
                exit_code=exit_code,
            )

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
