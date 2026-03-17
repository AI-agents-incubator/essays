#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
EXEC_DIR = Path(__file__).resolve().parent
STATE_FILE = EXEC_DIR / "runtime_process_state.json"
EVENT_LOG = EXEC_DIR / "observer_event_log.md"
PID_FILE = EXEC_DIR / "orchestrator.pid"
LOG_DIR = EXEC_DIR / "logs"
LAST_MESSAGES_DIR = EXEC_DIR / "last_messages"


FIELD_RE = re.compile(r"^- ([A-Za-z0-9_]+):\s*(.*)$")


RUNTIMES: dict[str, dict[str, Any]] = {
    "codex": {
        "workspace_dir": ROOT / "runtimes" / "codex" / "workspace",
        "status_file": ROOT / "runtimes" / "codex" / "runs" / "RUNTIME_STATUS.md",
        "directive_file": ROOT / "control_plane" / "codex" / "OBSERVER_DIRECTIVE.md",
        "ack_file": ROOT / "control_plane" / "codex" / "RUNTIME_ACK.md",
        "resume_command": [
            "codex",
            "exec",
            "resume",
            "--last",
            "--skip-git-repo-check",
            "--json",
        ],
        "prompt": (
            "Read AGENTS.md, ../runs/CURRENT_MISSION.md, ../runs/RUNTIME_STATUS.md, "
            "../../../control_plane/observer_runtime_protocol.md, "
            "../../../control_plane/codex/OBSERVER_DIRECTIVE.md, "
            "../../../control_plane/codex/RUNTIME_ACK.md. "
            "Act strictly according to the current observer directive. "
            "Update RUNTIME_ACK before doing further work. "
            "If the directive action is hold, acknowledge it and stop. "
            "Do not start a new run unless the observer directive explicitly requires it."
        ),
    },
    "claudecode": {
        "workspace_dir": ROOT / "runtimes" / "claudecode" / "workspace",
        "status_file": ROOT / "runtimes" / "claudecode" / "runs" / "RUNTIME_STATUS.md",
        "directive_file": ROOT / "control_plane" / "claudecode" / "OBSERVER_DIRECTIVE.md",
        "ack_file": ROOT / "control_plane" / "claudecode" / "RUNTIME_ACK.md",
        "settings_file": ROOT / "runtimes" / "claudecode" / "workspace" / ".claude" / "settings.json",
        "resume_command": [
            "claude",
            "--continue",
            "--print",
            "--permission-mode",
            "acceptEdits",
        ],
        "prompt": (
            "Read CLAUDE.md, ../runs/CURRENT_MISSION.md, ../runs/RUNTIME_STATUS.md, "
            "../../../control_plane/observer_runtime_protocol.md, "
            "../../../control_plane/claudecode/OBSERVER_DIRECTIVE.md, "
            "../../../control_plane/claudecode/RUNTIME_ACK.md. "
            "Act strictly according to the current observer directive. "
            "Update RUNTIME_ACK before doing further work. "
            "If the directive action is hold, acknowledge it and stop. "
            "Do not start a new run unless the observer directive explicitly requires it."
        ),
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ensure_dirs() -> None:
    LOG_DIR.mkdir(exist_ok=True)
    LAST_MESSAGES_DIR.mkdir(exist_ok=True)


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except json.JSONDecodeError:
        return {}


def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def parse_markdown_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    if not path.exists():
        return fields
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        match = FIELD_RE.match(line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip()
        if value.startswith("`") and value.endswith("`"):
            value = value[1:-1]
        fields[key] = value
    return fields


def append_event(message: str) -> None:
    timestamp = now_utc()
    if not EVENT_LOG.exists():
        EVENT_LOG.write_text("# Observer Event Log\n\n")
    with EVENT_LOG.open("a") as handle:
        handle.write(f"- `{timestamp}` {message}\n")


def pid_alive(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def build_command(runtime_key: str) -> tuple[list[str], Path, Path]:
    cfg = RUNTIMES[runtime_key]
    workspace_dir: Path = cfg["workspace_dir"]
    last_message_file = LAST_MESSAGES_DIR / f"{runtime_key}_last_message.txt"

    if runtime_key == "codex":
        command = cfg["resume_command"] + [
            "-o",
            str(last_message_file),
            cfg["prompt"],
        ]
    else:
        command = cfg["resume_command"] + [
            "--settings",
            str(cfg["settings_file"]),
            "--add-dir",
            str(ROOT / "runtimes" / "claudecode"),
            cfg["prompt"],
        ]

    return command, workspace_dir, last_message_file


def should_dispatch(
    runtime_key: str,
    status_fields: dict[str, str],
    directive_fields: dict[str, str],
    ack_fields: dict[str, str],
    runtime_state: dict[str, Any],
) -> tuple[bool, str]:
    action = directive_fields.get("action", "")
    directive_status = directive_fields.get("directive_status", "")
    directive_id = directive_fields.get("directive_id", "")
    ack_id = ack_fields.get("directive_id", "")
    ack_status = ack_fields.get("ack_status", "not_seen")

    running_pid = runtime_state.get("running_pid")
    if pid_alive(running_pid):
        return False, "runtime process already running"

    if directive_status != "active":
        return False, "directive is not active"

    # Hold only needs delivery until the runtime acknowledges it.
    if action == "hold":
        if ack_id == directive_id and ack_status in {"seen", "accepted", "completed"}:
            return False, "hold directive already acknowledged"
        return True, "deliver hold directive"

    # If the current directive has already been accepted and the runtime is now working
    # or already completed the corresponding step, avoid duplicate launches.
    if ack_id == directive_id and ack_status in {"accepted", "completed"}:
        if status_fields.get("status") in {"in_progress", "completed"}:
            return False, "directive already accepted or completed"

    last_dispatched = runtime_state.get("last_dispatched_directive_id")
    if last_dispatched == directive_id and ack_id == directive_id and ack_status in {"accepted", "seen"}:
        return False, "directive already dispatched and acknowledged"

    return True, f"dispatch action={action}"


def launch_runtime(runtime_key: str, runtime_state: dict[str, Any]) -> dict[str, Any]:
    command, cwd, _ = build_command(runtime_key)
    log_path = LOG_DIR / f"{runtime_key}_{int(time.time())}.log"
    with log_path.open("wb") as log_handle:
        process = subprocess.Popen(
            command,
            cwd=str(cwd),
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

    runtime_state.update(
        {
            "running_pid": process.pid,
            "running": True,
            "launched_at": now_utc(),
            "log_file": str(log_path.relative_to(ROOT)),
        }
    )
    return runtime_state


def reconcile_runtime(runtime_key: str, state: dict[str, Any], verbose: bool = False) -> None:
    cfg = RUNTIMES[runtime_key]
    status_fields = parse_markdown_fields(cfg["status_file"])
    directive_fields = parse_markdown_fields(cfg["directive_file"])
    ack_fields = parse_markdown_fields(cfg["ack_file"])

    runtime_state = state.setdefault(runtime_key, {})
    running_pid = runtime_state.get("running_pid")
    if running_pid and not pid_alive(running_pid):
        runtime_state["running"] = False
        runtime_state["running_pid"] = None
        runtime_state["finished_at"] = now_utc()

    dispatch, reason = should_dispatch(runtime_key, status_fields, directive_fields, ack_fields, runtime_state)
    if verbose:
        print(f"[{runtime_key}] {reason}")

    if not dispatch:
        return

    runtime_state["last_dispatched_directive_id"] = directive_fields.get("directive_id", "")
    runtime_state["last_dispatched_action"] = directive_fields.get("action", "")
    launch_runtime(runtime_key, runtime_state)
    append_event(
        f"{runtime_key}: launched runtime for directive "
        f"`{runtime_state['last_dispatched_directive_id']}` "
        f"with action `{runtime_state['last_dispatched_action']}`"
    )


def write_pid_file() -> None:
    PID_FILE.write_text(f"{os.getpid()}\n")


def remove_pid_file() -> None:
    if PID_FILE.exists():
        PID_FILE.unlink()


def run_once(verbose: bool = False) -> None:
    ensure_dirs()
    state = load_state()
    for runtime_key in sorted(RUNTIMES):
        reconcile_runtime(runtime_key, state, verbose=verbose)
    save_state(state)


def run_loop(interval: int, verbose: bool = False) -> None:
    ensure_dirs()
    write_pid_file()
    append_event("execution plane started")
    try:
        while True:
            run_once(verbose=verbose)
            time.sleep(interval)
    finally:
        append_event("execution plane stopped")
        remove_pid_file()


def main() -> int:
    parser = argparse.ArgumentParser(description="Control-plane execution orchestrator.")
    parser.add_argument("--loop", action="store_true", help="Run continuously instead of a single pass.")
    parser.add_argument("--interval", type=int, default=15, help="Polling interval in seconds for --loop.")
    parser.add_argument("--verbose", action="store_true", help="Print runtime decisions to stdout.")
    args = parser.parse_args()

    if args.loop:
        run_loop(interval=args.interval, verbose=args.verbose)
    else:
        run_once(verbose=args.verbose)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
