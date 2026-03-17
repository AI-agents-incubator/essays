#!/usr/bin/env python3
"""Run a command inside a runtime session with supervised projection refresh."""

from __future__ import annotations

import argparse
import os
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Start the projection watcher for a runtime session, run a command, then stop and sync cleanly.",
    )
    parser.add_argument(
        "--run-id",
        required=True,
        help="run id recorded with watcher metadata and the final projection sync",
    )
    parser.add_argument(
        "--watcher-ready-timeout",
        type=float,
        default=5.0,
        help="seconds to wait for the watcher to report readiness",
    )
    parser.add_argument(
        "--watcher-stop-timeout",
        type=float,
        default=5.0,
        help="seconds to wait for the watcher or child command to stop cleanly",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        help="override the watcher minimum polling interval for this session",
    )
    parser.add_argument(
        "--max-poll-interval",
        type=float,
        help="override the watcher maximum polling interval for this session",
    )
    parser.add_argument(
        "--poll-backoff-factor",
        type=float,
        help="override the watcher idle backoff multiplier for this session",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="command to run after '--' once the watcher is active",
    )
    args = parser.parse_args()

    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        parser.error("provide a command to run after '--'")
    if args.watcher_ready_timeout <= 0:
        parser.error("--watcher-ready-timeout must be greater than zero")
    if args.watcher_stop_timeout <= 0:
        parser.error("--watcher-stop-timeout must be greater than zero")
    if args.poll_interval is not None and args.poll_interval <= 0:
        parser.error("--poll-interval must be greater than zero")
    if args.max_poll_interval is not None and args.max_poll_interval <= 0:
        parser.error("--max-poll-interval must be greater than zero")
    if args.poll_backoff_factor is not None and args.poll_backoff_factor < 1:
        parser.error("--poll-backoff-factor must be greater than or equal to one")
    if (
        args.poll_interval is not None
        and args.max_poll_interval is not None
        and args.max_poll_interval < args.poll_interval
    ):
        parser.error("--max-poll-interval must be greater than or equal to --poll-interval")

    return args


def state_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "state"


def state_db_path() -> Path:
    return state_dir() / "runtime_state.sqlite"


def state_var(scope: str, key: str, default: str) -> str:
    conn = sqlite3.connect(state_db_path())
    try:
        row = conn.execute(
            """
            SELECT value
            FROM state_variables
            WHERE scope = ? AND key = ?
            """,
            (scope, key),
        ).fetchone()
    finally:
        conn.close()
    return row[0] if row else default


def stop_process(process: subprocess.Popen[bytes], timeout: float) -> int:
    if process.poll() is not None:
        return process.returncode or 0

    process.terminate()
    try:
        return process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        return process.wait()


def wait_for_ready_file(
    ready_file: Path,
    watcher: subprocess.Popen[bytes],
    timeout: float,
) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if ready_file.exists():
            return
        if watcher.poll() is not None:
            raise RuntimeError(
                f"projection watcher exited before startup completed with code {watcher.returncode}"
            )
        time.sleep(0.05)
    raise RuntimeError("timed out waiting for the projection watcher to become ready")


def run_command_with_watcher(
    args: argparse.Namespace,
    watcher: subprocess.Popen[bytes],
) -> int:
    command = subprocess.Popen(args.command)
    try:
        while True:
            command_returncode = command.poll()
            watcher_returncode = watcher.poll()

            if watcher_returncode is not None and command_returncode is None:
                stop_process(command, args.watcher_stop_timeout)
                raise RuntimeError(
                    f"projection watcher exited unexpectedly with code {watcher_returncode}"
                )

            if command_returncode is not None:
                return command_returncode

            time.sleep(0.1)
    finally:
        if command.poll() is None:
            stop_process(command, args.watcher_stop_timeout)


def final_sync(run_id: str) -> int:
    sync_script = state_dir() / "sync_projections.py"
    result = subprocess.run(
        [sys.executable, "-B", str(sync_script), "--run-id", run_id],
        check=False,
    )
    return result.returncode


def state_var_float(scope: str, key: str, default: str) -> float:
    return float(state_var(scope, key, default))


def watcher_poll_config(args: argparse.Namespace) -> tuple[float, float, float]:
    poll_interval = args.poll_interval
    if poll_interval is None:
        poll_interval = state_var_float(
            "state", "projection_watcher_poll_interval_seconds", "0.5"
        )

    max_poll_interval = args.max_poll_interval
    if max_poll_interval is None:
        max_poll_interval = state_var_float(
            "state", "projection_watcher_max_poll_interval_seconds", "2.0"
        )

    poll_backoff_factor = args.poll_backoff_factor
    if poll_backoff_factor is None:
        poll_backoff_factor = state_var_float(
            "state", "projection_watcher_poll_backoff_factor", "2.0"
        )

    if max_poll_interval < poll_interval:
        raise ValueError(
            "projection watcher max poll interval is lower than the minimum poll interval"
        )

    return poll_interval, max_poll_interval, poll_backoff_factor


def main() -> int:
    args = parse_args()
    refresh_mode = state_var("state", "projection_refresh_mode", "manual")

    if refresh_mode != "watcher":
        result = subprocess.run(args.command, check=False)
        return result.returncode

    try:
        poll_interval, max_poll_interval, poll_backoff_factor = watcher_poll_config(
            args
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    ready_file = Path(tempfile.gettempdir()) / (
        f"codex_runtime_session_{os.getpid()}_{int(time.time() * 1000)}.ready"
    )
    watcher_script = state_dir() / "watch_projections.py"
    watcher_command = [
        sys.executable,
        "-B",
        str(watcher_script),
        "--run-id",
        args.run_id,
        "--poll-interval",
        str(poll_interval),
        "--max-poll-interval",
        str(max_poll_interval),
        "--poll-backoff-factor",
        str(poll_backoff_factor),
        "--launch-mode",
        "bootstrap/runtime_session.py",
        "--ready-file",
        str(ready_file),
    ]

    print(
        f"runtime session: starting projection watcher for {args.run_id} "
        f"with adaptive polling {poll_interval:.2f}s..{max_poll_interval:.2f}s "
        f"(x{poll_backoff_factor:.2f} idle backoff)"
    )
    watcher = subprocess.Popen(watcher_command)
    command_returncode = 1
    try:
        wait_for_ready_file(ready_file, watcher, args.watcher_ready_timeout)
        print("runtime session: projection watcher ready")
        command_returncode = run_command_with_watcher(args, watcher)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        command_returncode = 1
    finally:
        watcher_returncode = stop_process(watcher, args.watcher_stop_timeout)
        if ready_file.exists():
            ready_file.unlink()
        print(
            f"runtime session: projection watcher stopped with code {watcher_returncode}"
        )

    sync_returncode = final_sync(args.run_id)
    if sync_returncode != 0:
        return sync_returncode
    return command_returncode


if __name__ == "__main__":
    sys.exit(main())
