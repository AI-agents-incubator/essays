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
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
EXEC_DIR = Path(__file__).resolve().parent
STATE_FILE = EXEC_DIR / "runtime_process_state.json"
EVENT_LOG = EXEC_DIR / "observer_event_log.md"
PID_FILE = EXEC_DIR / "orchestrator.pid"
HEARTBEAT_FILE = EXEC_DIR / "HUMAN_PROGRESS.md"
LOG_DIR = EXEC_DIR / "logs"
LAST_MESSAGES_DIR = EXEC_DIR / "last_messages"
STALE_RETRY_COOLDOWN = timedelta(seconds=15)
STALL_SIGNAL_TIMEOUT = timedelta(seconds=120)
PROTOCOL_STALE_TIMEOUT = timedelta(seconds=300)
DISPATCH_ACK_TIMEOUT = timedelta(seconds=60)
DIRECTIVE_ID_RE = re.compile(r"^(.*?)(\d+)$")


FIELD_RE = re.compile(r"^- ([A-Za-z0-9_]+):\s*(.*)$")


RUNTIMES: dict[str, dict[str, Any]] = {
    "codex": {
        "runtime_dir": ROOT / "runtimes" / "codex",
        "workspace_dir": ROOT / "runtimes" / "codex" / "workspace",
        "status_file": ROOT / "runtimes" / "codex" / "runs" / "RUNTIME_STATUS.md",
        "observer_directive_file": ROOT / "control_plane" / "codex" / "OBSERVER_DIRECTIVE.md",
        "observer_ack_file": ROOT / "control_plane" / "codex" / "RUNTIME_ACK.md",
        "control_dir": ROOT / "runtimes" / "codex" / "control",
        "directive_file": ROOT / "runtimes" / "codex" / "control" / "OBSERVER_DIRECTIVE.md",
        "ack_file": ROOT / "runtimes" / "codex" / "control" / "RUNTIME_ACK.md",
        "protocol_file": ROOT / "runtimes" / "codex" / "control" / "observer_runtime_protocol.md",
        "improvement_backlog_file": ROOT / "runtimes" / "codex" / "workspace" / "agent_org" / "evolution" / "improvement_backlog.md",
        "launch_command": [
            "codex",
            "exec",
            "--dangerously-bypass-approvals-and-sandbox",
            "--ephemeral",
            "--json",
        ],
        "prompt": (
            "Read workspace/AGENTS.md, runs/CURRENT_MISSION.md, runs/RUNTIME_STATUS.md, "
            "control/observer_runtime_protocol.md, control/OBSERVER_DIRECTIVE.md, "
            "control/RUNTIME_ACK.md. "
            "Act strictly according to the current observer directive. "
            "Update RUNTIME_ACK before doing further work. "
            "If the directive action is hold, acknowledge it and stop. "
            "Do not start a new run unless the observer directive explicitly requires it."
        ),
    },
    "claudecode": {
        "runtime_dir": ROOT / "runtimes" / "claudecode",
        "workspace_dir": ROOT / "runtimes" / "claudecode" / "workspace",
        "status_file": ROOT / "runtimes" / "claudecode" / "runs" / "RUNTIME_STATUS.md",
        "observer_directive_file": ROOT / "control_plane" / "claudecode" / "OBSERVER_DIRECTIVE.md",
        "observer_ack_file": ROOT / "control_plane" / "claudecode" / "RUNTIME_ACK.md",
        "control_dir": ROOT / "runtimes" / "claudecode" / "control",
        "directive_file": ROOT / "runtimes" / "claudecode" / "control" / "OBSERVER_DIRECTIVE.md",
        "ack_file": ROOT / "runtimes" / "claudecode" / "control" / "RUNTIME_ACK.md",
        "protocol_file": ROOT / "runtimes" / "claudecode" / "control" / "observer_runtime_protocol.md",
        "improvement_backlog_file": ROOT / "runtimes" / "claudecode" / "workspace" / "agent_org" / "evolution" / "improvement_backlog.md",
        "settings_file": ROOT / "runtimes" / "claudecode" / "workspace" / ".claude" / "settings.json",
        "launch_command": [
            "claude",
            "--print",
            "--permission-mode",
            "bypassPermissions",
            "--dangerously-skip-permissions",
            "--no-session-persistence",
        ],
        "prompt": (
            "Read workspace/CLAUDE.md, runs/CURRENT_MISSION.md, runs/RUNTIME_STATUS.md, "
            "control/observer_runtime_protocol.md, control/OBSERVER_DIRECTIVE.md, "
            "control/RUNTIME_ACK.md. "
            "Act strictly according to the current observer directive. "
            "Update RUNTIME_ACK before doing further work. "
            "If the directive action is hold, acknowledge it and stop. "
            "Do not start a new run unless the observer directive explicitly requires it."
        ),
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_iso_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


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


def read_recent_events(limit: int = 6) -> list[str]:
    if not EVENT_LOG.exists():
        return []
    lines = [line.rstrip() for line in EVENT_LOG.read_text().splitlines() if line.startswith("- ")]
    return lines[-limit:]


def sync_text_file(source: Path, target: Path) -> None:
    if not source.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    content = source.read_text()
    if target.exists() and target.read_text() == content:
        return
    target.write_text(content)


def seed_text_file_if_missing(source: Path, target: Path) -> None:
    if target.exists():
        return
    sync_text_file(source, target)


def slug_for_runtime(runtime_key: str) -> str:
    return "CLAUDE" if runtime_key == "claudecode" else runtime_key.upper()


def next_directive_id(runtime_key: str, current_id: str) -> str:
    match = DIRECTIVE_ID_RE.match(current_id or "")
    if match:
        prefix, digits = match.groups()
        return f"{prefix}{int(digits) + 1:0{len(digits)}d}"
    return f"OBS-{slug_for_runtime(runtime_key)}-001"


def infer_next_run_id(current_run: str, hinted_next_run: str) -> str:
    if hinted_next_run.startswith("RUN-"):
        return hinted_next_run.split()[0]
    match = re.match(r"^RUN-(\d+)$", current_run or "")
    if match:
        return f"RUN-{int(match.group(1)) + 1:03d}"
    return "RUN-NEXT"


def parse_open_backlog_item(runtime_key: str) -> dict[str, str] | None:
    backlog_file: Path = RUNTIMES[runtime_key]["improvement_backlog_file"]
    if not backlog_file.exists():
        return None

    lines = backlog_file.read_text().splitlines()
    if runtime_key == "codex":
        pattern = re.compile(
            r"^- `([^`]+)` \| ([^|]+)\| .*status: `open`(?: \| proposals: `([^`]+)`)?"
        )
        for raw_line in lines:
            match = pattern.match(raw_line.strip())
            if not match:
                continue
            item_id, description, proposal = match.groups()
            result = {
                "id": item_id.strip(),
                "description": description.strip(),
            }
            if proposal:
                result["proposal"] = proposal.strip()
            return result
        return None

    for raw_line in lines:
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        if "---" in line or "id | description" in line:
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 4:
            continue
        item_id, description, priority, status = parts[:4]
        if status != "open":
            continue
        return {
            "id": item_id,
            "description": description,
            "priority": priority,
        }
    return None


def observer_decision_snapshot(runtime_key: str, runtime_state: dict[str, Any], status_fields: dict[str, str]) -> dict[str, str]:
    open_item = parse_open_backlog_item(runtime_key)
    if open_item:
        return {
            "observer_phase": "next_run_available",
            "open_item": f"{open_item['id']}: {open_item['description']}",
        }
    if status_fields.get("status") == "completed":
        return {
            "observer_phase": "autonomous_cycle_complete",
            "open_item": "none",
        }
    return {
        "observer_phase": runtime_state.get("observer_phase", "in_flight"),
        "open_item": "unknown",
    }


def runtime_control_view(runtime_key: str) -> dict[str, Any]:
    cfg = RUNTIMES[runtime_key]
    status_fields = parse_markdown_fields(cfg["status_file"])
    directive_fields = parse_markdown_fields(cfg["observer_directive_file"])
    ack_fields = parse_markdown_fields(cfg["observer_ack_file"])
    open_item = parse_open_backlog_item(runtime_key)
    return {
        "status": status_fields,
        "directive": directive_fields,
        "ack": ack_fields,
        "open_item": open_item,
    }


def runtime_ready_for_closeout(runtime_key: str) -> bool:
    view = runtime_control_view(runtime_key)
    status_fields = view["status"]
    if status_fields.get("status") != "completed":
        return False
    if status_fields.get("needs_human") != "no":
        return False
    if status_fields.get("blocking_issue") not in {"none", ""}:
        return False
    if view["open_item"] is not None:
        return False
    return True


def all_runtimes_ready_for_closeout() -> bool:
    return all(runtime_ready_for_closeout(runtime_key) for runtime_key in RUNTIMES)


def runtime_closeout_complete(runtime_key: str) -> bool:
    view = runtime_control_view(runtime_key)
    directive_fields = view["directive"]
    ack_fields = view["ack"]
    status_fields = view["status"]
    return (
        status_fields.get("status") == "completed"
        and directive_fields.get("action") == "hold"
        and directive_fields.get("directive_status") == "completed"
        and ack_fields.get("directive_id") == directive_fields.get("directive_id")
        and ack_fields.get("ack_status") in {"seen", "accepted", "completed"}
    )


def all_runtimes_closeout_complete() -> bool:
    return all(runtime_closeout_complete(runtime_key) for runtime_key in RUNTIMES)


def write_observer_directive(
    runtime_key: str,
    directive_id: str,
    based_on_run: str,
    directive_status: str,
    action: str,
    objective: str,
    required_outputs: str,
    next_expected_step: str,
    comment: str,
) -> None:
    runtime_label = "Claude Code" if runtime_key == "claudecode" else "Codex"
    content = "\n".join(
        [
            f"# Observer Directive: {runtime_label}",
            "",
            "> Версия файла: `v1.2`",
            f"> Дата версии: `{datetime.now().date().isoformat()}`",
            "> Тип документа: `observer -> runtime`",
            "",
            f"- runtime: `{runtime_label}`",
            f"- directive_id: `{directive_id}`",
            f"- based_on_run: `{based_on_run}`",
            f"- directive_status: `{directive_status}`",
            f"- action: `{action}`",
            f"- objective: `{objective}`",
            f"- required_outputs: `{required_outputs}`",
            f"- created_at: `{datetime.now().date().isoformat()}`",
            "- written_by: `observer-auto`",
            "- human_review_required: `no`",
            f"- next_expected_step: `{next_expected_step}`",
            "",
            "## Комментарий",
            "",
            comment,
            "",
        ]
    )
    path: Path = RUNTIMES[runtime_key]["observer_directive_file"]
    path.write_text(content)


def maybe_advance_observer(runtime_key: str, state: dict[str, Any], verbose: bool = False) -> None:
    cfg = RUNTIMES[runtime_key]
    runtime_state = state.setdefault(runtime_key, {})
    running_pid = runtime_state.get("running_pid")
    if running_pid and not pid_alive(running_pid):
        runtime_state["running"] = False
        runtime_state["running_pid"] = None
        runtime_state["finished_at"] = now_utc()

    status_fields = parse_markdown_fields(cfg["status_file"])
    directive_fields = parse_markdown_fields(cfg["observer_directive_file"])
    ack_fields = parse_markdown_fields(cfg["observer_ack_file"])

    if pid_alive(runtime_state.get("running_pid")):
        if (
            status_fields.get("status") == "completed"
            and ack_fields.get("ack_status") == "completed"
            and ack_fields.get("directive_id") == directive_fields.get("directive_id")
        ):
            terminate_process_group(runtime_state["running_pid"])
            runtime_state["running"] = False
            runtime_state["running_pid"] = None
            runtime_state["finished_at"] = now_utc()
            append_event(
                f"{runtime_key}: terminated lingering runtime process after completed status/ack to unblock observer advancement"
            )
            if verbose:
                print(f"[{runtime_key}] terminated lingering completed runtime")
        else:
            runtime_state["observer_phase"] = "runtime_busy"
            return

    decision = observer_decision_snapshot(runtime_key, runtime_state, status_fields)
    runtime_state["observer_phase"] = decision["observer_phase"]
    runtime_state["open_backlog_item"] = decision["open_item"]

    if status_fields.get("status") != "completed":
        return
    if status_fields.get("needs_human") != "no":
        return
    if status_fields.get("blocking_issue") not in {"none", ""}:
        return
    current_run = status_fields.get("current_run", "")
    current_directive_based_on = directive_fields.get("based_on_run", "")
    current_directive_id = directive_fields.get("directive_id", "")
    current_action = directive_fields.get("action", "")
    current_directive_status = directive_fields.get("directive_status", "")
    current_ack_id = ack_fields.get("directive_id", "")
    current_ack_status = ack_fields.get("ack_status", "")
    ack_matches_current_directive = current_ack_id == current_directive_id
    ack_confirms_hold = ack_matches_current_directive and current_ack_status in {"seen", "accepted", "completed"}

    if current_action == "hold":
        pass
    elif current_ack_status != "completed":
        return

    # The current completed run has already been observed and rebased.
    if current_directive_based_on == current_run and current_action == "continue_with_next_run":
        return
    if (
        current_directive_based_on == current_run
        and current_action == "hold"
        and current_directive_status == "active"
    ):
        if ack_confirms_hold:
            write_observer_directive(
                runtime_key=runtime_key,
                directive_id=current_directive_id,
                based_on_run=current_run,
                directive_status="completed",
                action="hold",
                objective=directive_fields.get("objective", "Автономный цикл завершён."),
                required_outputs=directive_fields.get("required_outputs", "Новых run не требуется."),
                next_expected_step=directive_fields.get(
                    "next_expected_step",
                    "Никаких новых run автоматически не запускать.",
                ),
                comment="Runtime подтвердил финальный hold. Observer фиксирует полное завершение автономного цикла.",
            )
            runtime_state["observer_phase"] = "autonomous_cycle_complete"
            runtime_state["open_backlog_item"] = "none"
            append_event(
                f"{runtime_key}: observer-auto finalized hold `{current_directive_id}` after matching runtime ack"
            )
        else:
            runtime_state["observer_phase"] = "awaiting_final_hold_ack"
            runtime_state["open_backlog_item"] = "awaiting matching runtime ack for final hold"
        return
    if (
        current_directive_based_on == current_run
        and current_action == "hold"
        and current_directive_status == "completed"
    ):
        if not ack_confirms_hold:
            write_observer_directive(
                runtime_key=runtime_key,
                directive_id=current_directive_id,
                based_on_run=current_run,
                directive_status="active",
                action="hold",
                objective="Автономный цикл для текущего benchmark wave завершён: требуется явное подтверждение финального hold от runtime.",
                required_outputs="Runtime должен перечитать финальную hold-директиву и подтвердить её через matching RUNTIME_ACK.",
                next_expected_step="Runtime должен обновить RUNTIME_ACK на текущий directive_id и остановиться без запуска новых run.",
                comment="Предыдущий финальный hold был выписан без matching runtime ack. Observer переоткрывает эту же hold-директиву, чтобы довести протокол до консистентного состояния.",
            )
            runtime_state["observer_phase"] = "awaiting_final_hold_ack"
            runtime_state["open_backlog_item"] = "awaiting matching runtime ack for final hold"
            append_event(
                f"{runtime_key}: observer-auto reopened final hold `{current_directive_id}` because runtime ack was still `{current_ack_id}`"
            )
            return
        runtime_state["observer_phase"] = "autonomous_cycle_complete"
        runtime_state["open_backlog_item"] = "none"
        return

    open_item = parse_open_backlog_item(runtime_key)
    next_id = next_directive_id(runtime_key, current_directive_id)

    if open_item:
        next_run_id = infer_next_run_id(current_run, status_fields.get("next_run", ""))
        proposal_suffix = f" Предлагаемое изменение: {open_item['proposal']}." if open_item.get("proposal") else ""
        objective = (
            f"Запустить {next_run_id} как реализацию {open_item['id']}: "
            f"{open_item['description']}.{proposal_suffix}"
        )
        required_outputs = (
            f"Новый run summary, новая evaluation trace, обновлённые runtime-артефакты в рамках "
            f"{open_item['id']}, и явная фиксация результата {next_run_id}."
        )
        next_expected_step = (
            f"Runtime должен принять директиву, перевести статус в in_progress и выполнить "
            f"{next_run_id} как следующий observer-approved run без паузы."
        )
        comment = (
            f"{current_run} завершён без блокеров. Следующий шаг однозначно определён через open backlog item "
            f"{open_item['id']}, поэтому observer-auto немедленно выпускает следующую директиву."
        )
        write_observer_directive(
            runtime_key=runtime_key,
            directive_id=next_id,
            based_on_run=current_run,
            directive_status="active",
            action="continue_with_next_run",
            objective=objective,
            required_outputs=required_outputs,
            next_expected_step=next_expected_step,
            comment=comment,
        )
        runtime_state["observer_phase"] = "next_run_scheduled"
        runtime_state["open_backlog_item"] = f"{open_item['id']}: {open_item['description']}"
        append_event(
            f"{runtime_key}: observer-auto issued `{next_id}` for `{current_run}` -> "
            f"`{infer_next_run_id(current_run, status_fields.get('next_run', ''))}` based on backlog item `{open_item['id']}`"
        )
        return

    if not all_runtimes_ready_for_closeout():
        if not (
            current_action == "hold"
            and current_directive_status == "active"
            and current_directive_based_on == current_run
        ):
            objective = (
                "Локальный backlog для этого runtime уже исчерпан, но другие runtime текущей benchmark wave "
                "ещё не достигли общего closeout barrier."
            )
            required_outputs = (
                "Новых engineering run не запускать. Сохранить completed state и ждать, пока peer-runtime "
                "дойдёт до общего closeout barrier."
            )
            next_expected_step = (
                "Runtime должен подтвердить hold и остаться в режиме ожидания peers. "
                "prepare_comparison будет выдан только после достижения общего barrier всеми runtime."
            )
            comment = (
                f"{current_run} локально завершён и open backlog item больше нет, "
                "но wave-synchronized closeout ещё недоступен, потому что peer-runtime не завершил инженерную фазу."
            )
            write_observer_directive(
                runtime_key=runtime_key,
                directive_id=next_id,
                based_on_run=current_run,
                directive_status="active",
                action="hold",
                objective=objective,
                required_outputs=required_outputs,
                next_expected_step=next_expected_step,
                comment=comment,
            )
            append_event(
                f"{runtime_key}: observer-auto issued peer-barrier hold `{next_id}` after `{current_run}`"
            )
        runtime_state["observer_phase"] = "waiting_for_peers"
        runtime_state["open_backlog_item"] = "waiting for peer runtimes to reach closeout barrier"
        return

    if current_action != "prepare_comparison":
        objective = (
            "Подготовить terminal comparison/completion package по завершённому автономному циклу, "
            "чтобы зафиксировать итоги benchmark wave без ручного observer шага."
        )
        required_outputs = (
            "Completion/comparison package в локальной песочнице, обновлённый runtime ack со статусом completed, "
            "и явная фиксация отсутствия дальнейших open improvement items для этой волны."
        )
        next_expected_step = (
            "Runtime должен принять директиву, подготовить comparison/closure package без запуска нового engineering run, "
            "а затем перевести RUNTIME_ACK в completed."
        )
        comment = (
            f"{current_run} завершён без блокеров и improvement backlog уже пуст. "
            "Observer-auto сначала выпускает терминальную задачу закрытия волны, а не зависает и не перескакивает молча в final hold."
        )
        write_observer_directive(
            runtime_key=runtime_key,
            directive_id=next_id,
            based_on_run=current_run,
            directive_status="active",
            action="prepare_comparison",
            objective=objective,
            required_outputs=required_outputs,
            next_expected_step=next_expected_step,
            comment=comment,
        )
        runtime_state["observer_phase"] = "completion_package_scheduled"
        runtime_state["open_backlog_item"] = "terminal comparison/completion package"
        append_event(
            f"{runtime_key}: observer-auto issued terminal comparison directive `{next_id}` after `{current_run}`"
        )
        return

    if ack_fields.get("ack_status") != "completed":
        runtime_state["observer_phase"] = "completion_package_in_flight"
        runtime_state["open_backlog_item"] = "terminal comparison/completion package"
        return

    if not all_runtimes_ready_for_closeout():
        runtime_state["observer_phase"] = "waiting_for_peers"
        runtime_state["open_backlog_item"] = "waiting for peer runtimes to finish closeout"
        return

    if not all_runtimes_closeout_complete():
        if not (
            current_action == "hold"
            and current_directive_status == "active"
            and current_directive_based_on == current_run
        ):
            objective = (
                "Этот runtime уже подготовил terminal comparison package, но общий wave closeout "
                "ещё не завершён всеми runtime."
            )
            required_outputs = (
                "Новых run не запускать. Оставаться в completed closeout state и ждать peer-runtime."
            )
            next_expected_step = (
                "Runtime должен подтвердить hold и ждать, пока peer-runtime завершит свой terminal closeout. "
                "Финальный completed hold будет выписан после общего barrier."
            )
            comment = (
                f"{current_run} уже закрыл local closeout package, но wave-complete barrier ещё не достигнут всеми runtime."
            )
            write_observer_directive(
                runtime_key=runtime_key,
                directive_id=next_id,
                based_on_run=current_run,
                directive_status="active",
                action="hold",
                objective=objective,
                required_outputs=required_outputs,
                next_expected_step=next_expected_step,
                comment=comment,
            )
            append_event(
                f"{runtime_key}: observer-auto issued post-closeout peer wait `{next_id}` after `{current_run}`"
            )
        runtime_state["observer_phase"] = "waiting_for_peers"
        runtime_state["open_backlog_item"] = "waiting for peer runtimes to finish closeout"
        return

    objective = "Автономный цикл для текущего benchmark wave завершён: открытых improvement items больше нет."
    required_outputs = "Новых run не требуется. Runtime считается structurally complete for the current autonomous period."
    next_expected_step = "Никаких новых run автоматически не запускать. Зафиксировать завершение автономного цикла и ожидать следующей benchmark wave или comparison-phase."
    comment = (
        f"{current_run} завершён без блокеров, comparison/closure package уже подготовлен, а improvement backlog пуст. "
        "Observer-auto фиксирует завершение автономного цикла без участия человека."
    )
    write_observer_directive(
        runtime_key=runtime_key,
        directive_id=next_id,
        based_on_run=current_run,
        directive_status="active",
        action="hold",
        objective=objective,
        required_outputs=required_outputs,
        next_expected_step=next_expected_step,
        comment=(
            f"{comment} Runtime ещё должен явно подтвердить финальный hold, "
            "только после этого observer зафиксирует полное завершение автономного цикла."
        ),
    )
    runtime_state["observer_phase"] = "awaiting_final_hold_ack"
    runtime_state["open_backlog_item"] = "awaiting matching runtime ack for final hold"
    append_event(
        f"{runtime_key}: observer-auto issued final hold `{next_id}` after `{current_run}` and is waiting for runtime confirmation"
    )


def project_control_plane(runtime_key: str) -> None:
    cfg = RUNTIMES[runtime_key]
    sync_text_file(ROOT / "control_plane" / "observer_runtime_protocol.md", cfg["protocol_file"])
    sync_text_file(cfg["observer_directive_file"], cfg["directive_file"])
    seed_text_file_if_missing(cfg["observer_ack_file"], cfg["ack_file"])


def mirror_runtime_outputs(runtime_key: str) -> None:
    cfg = RUNTIMES[runtime_key]
    sync_text_file(cfg["ack_file"], cfg["observer_ack_file"])


def pid_alive(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    try:
        state = (
            subprocess.check_output(
                ["ps", "-p", str(pid), "-o", "state="],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            .strip()
        )
    except subprocess.SubprocessError:
        return False
    if not state:
        return False
    if state.startswith("Z"):
        return False
    return True


def file_age_seconds(path: Path) -> str:
    if not path.exists():
        return "unknown"
    return str(int(time.time() - path.stat().st_mtime))


def file_size_bytes(path: Path) -> str:
    if not path.exists():
        return "unknown"
    return str(path.stat().st_size)


def file_age_delta(path: Path | None) -> timedelta | None:
    if path is None or not path.exists():
        return None
    return timedelta(seconds=time.time() - path.stat().st_mtime)


def terminate_process_group(pid: int) -> None:
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    except OSError:
        return

    deadline = time.time() + 5
    while time.time() < deadline:
        if not pid_alive(pid):
            return
        time.sleep(0.2)

    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        return
    except OSError:
        return


def stall_reason(
    runtime_key: str,
    runtime_state: dict[str, Any],
    status_fields: dict[str, str],
    directive_fields: dict[str, str],
    ack_fields: dict[str, str],
) -> str | None:
    running_pid = runtime_state.get("running_pid")
    if not pid_alive(running_pid):
        return None

    if directive_fields.get("directive_status") != "active":
        return None

    action = directive_fields.get("action", "")
    if action == "hold":
        return None

    cfg = RUNTIMES[runtime_key]
    log_path_value = runtime_state.get("log_file")
    log_path = ROOT / log_path_value if log_path_value else None
    log_age = file_age_delta(log_path)
    status_age = file_age_delta(cfg["status_file"])
    ack_age = file_age_delta(cfg["ack_file"])

    if log_age is None or status_age is None or ack_age is None:
        return None

    ack_status = ack_fields.get("ack_status", "")
    runtime_status = status_fields.get("status", "")
    ack_id = ack_fields.get("directive_id", "")
    directive_id = directive_fields.get("directive_id", "")

    if log_age < STALL_SIGNAL_TIMEOUT:
        if ack_id != directive_id and ack_age >= DISPATCH_ACK_TIMEOUT:
            return (
                f"stalled dispatch: directive `{directive_id}` not acknowledged for "
                f"{int(ack_age.total_seconds())}s while worker stayed alive"
            )
        return None

    if ack_status == "accepted" and runtime_status == "in_progress" and status_age >= STALL_SIGNAL_TIMEOUT:
        return (
            f"stalled active runtime: no log growth for {int(log_age.total_seconds())}s, "
            f"status unchanged for {int(status_age.total_seconds())}s, "
            f"ack unchanged for {int(ack_age.total_seconds())}s"
        )

    if ack_status == "accepted" and action in {"prepare_comparison", "repair_current_state"} and ack_age >= STALL_SIGNAL_TIMEOUT:
        return (
            f"stalled control action `{action}`: no log growth for {int(log_age.total_seconds())}s, "
            f"ack unchanged for {int(ack_age.total_seconds())}s"
        )

    return None


def human_status(snapshot: dict[str, Any]) -> tuple[str, str]:
    observer_phase = snapshot["observer_phase"]
    directive_action = snapshot["directive_action"]
    directive_status = snapshot["directive_status"]
    runtime_status = snapshot["runtime_status"]
    worker_alive = snapshot["worker_alive"]
    needs_human = snapshot["needs_human"]
    blocking_issue = snapshot["blocking_issue"]
    status_signal_age = snapshot["status_signal_age_delta"]
    ack_signal_age = snapshot["ack_signal_age_delta"]
    ack_id = snapshot["ack_id"]
    directive_id = snapshot["directive_id"]
    ack_status = snapshot["ack_status"]

    if needs_human == "yes" or blocking_issue not in {"none", "", "unknown"}:
        return "needs_attention", "human or blocker intervention required"

    if directive_status == "completed" and directive_action == "hold":
        if ack_id != directive_id or ack_status not in {"seen", "accepted", "completed"}:
            return (
                "protocol_inconsistent",
                "final hold directive is not confirmed by the matching runtime ack, so the wave cannot be trusted as fully closed",
            )

    if worker_alive and directive_action in {"continue_with_next_run", "prepare_comparison", "repair_current_state"} and ack_id != directive_id:
        return "dispatching", "new directive has been issued and the runtime is starting the next step"

    if worker_alive and (
        (status_signal_age is not None and status_signal_age >= PROTOCOL_STALE_TIMEOUT)
        or (ack_signal_age is not None and ack_signal_age >= PROTOCOL_STALE_TIMEOUT)
    ):
        return (
            "protocol_stale",
            "worker is still producing output, but runtime status/ack signals are too old to trust as healthy",
        )

    if observer_phase == "autonomous_cycle_complete":
        return "terminal_complete", "no further work expected in the current autonomous wave"

    if observer_phase == "waiting_for_peers":
        return "waiting_peers", "local scope is finished; waiting for peer runtimes to reach the same wave barrier"

    if worker_alive and observer_phase == "runtime_busy":
        return "active", "work is actively progressing"

    if directive_action == "hold" and directive_status == "active":
        return "waiting", "paused for the next observer directive"

    if runtime_status == "in_progress" and not worker_alive:
        return "recovery_pending", "runtime marked in_progress but no live worker is attached"

    return runtime_status, "state derived directly from runtime artifacts"


def protocol_consistency(snapshot: dict[str, Any]) -> tuple[str, str]:
    directive_id = snapshot["directive_id"]
    ack_id = snapshot["ack_id"]
    directive_action = snapshot["directive_action"]
    directive_status = snapshot["directive_status"]
    ack_status = snapshot["ack_status"]

    if ack_id != directive_id:
        return "mismatch", "runtime ack points to a different directive than the current observer directive"

    if directive_action == "hold" and directive_status == "completed":
        if ack_status in {"seen", "accepted", "completed"}:
            return "ok", "final hold reconciled: observer directive and runtime ack are aligned"
        return "weak", "final hold is completed on observer side, but runtime ack status is weaker than expected"

    if directive_status == "active" and ack_status in {"seen", "accepted", "completed"}:
        return "ok", "active directive is acknowledged by the runtime"

    return "ok", "observer directive and runtime ack refer to the same directive"


def runtime_snapshot(runtime_key: str, runtime_state: dict[str, Any]) -> dict[str, Any]:
    cfg = RUNTIMES[runtime_key]
    status_fields = parse_markdown_fields(cfg["status_file"])
    directive_fields = parse_markdown_fields(cfg["directive_file"])
    ack_fields = parse_markdown_fields(cfg["ack_file"])
    running_pid = runtime_state.get("running_pid")
    log_path_value = runtime_state.get("log_file", "unknown")
    log_path = ROOT / log_path_value if log_path_value != "unknown" else None
    if log_path and not log_path.exists():
        log_path = None

    status_age_delta = file_age_delta(cfg["status_file"])
    ack_age_delta = file_age_delta(cfg["ack_file"])
    log_age_delta = file_age_delta(log_path) if log_path else None

    snapshot = {
        "runtime_key": runtime_key,
        "runtime_label": status_fields.get("runtime", runtime_key),
        "current_run": status_fields.get("current_run", "unknown"),
        "runtime_status": status_fields.get("status", "unknown"),
        "updated_at": status_fields.get("updated_at", "unknown"),
        "needs_human": status_fields.get("needs_human", "unknown"),
        "blocking_issue": status_fields.get("blocking_issue", "unknown"),
        "directive_id": directive_fields.get("directive_id", "unknown"),
        "directive_action": directive_fields.get("action", "unknown"),
        "directive_status": directive_fields.get("directive_status", "unknown"),
        "ack_id": ack_fields.get("directive_id", "unknown"),
        "ack_status": ack_fields.get("ack_status", "unknown"),
        "ack_next_action": ack_fields.get("next_action", "unknown"),
        "worker_pid": running_pid if pid_alive(running_pid) else None,
        "worker_alive": pid_alive(running_pid),
        "log_file": log_path_value,
        "log_signal_age_seconds": file_age_seconds(log_path) if log_path else "unknown",
        "log_size_bytes": file_size_bytes(log_path) if log_path else "unknown",
        "status_signal_age_seconds": file_age_seconds(cfg["status_file"]),
        "ack_signal_age_seconds": file_age_seconds(cfg["ack_file"]),
        "status_signal_age_delta": status_age_delta,
        "ack_signal_age_delta": ack_age_delta,
        "log_signal_age_delta": log_age_delta,
        "observer_phase": runtime_state.get("observer_phase", "unknown"),
        "open_backlog_item": runtime_state.get("open_backlog_item", "unknown"),
    }
    display_status, progress_expectation = human_status(snapshot)
    protocol_state, protocol_explanation = protocol_consistency(snapshot)
    snapshot["display_status"] = display_status
    snapshot["progress_expectation"] = progress_expectation
    snapshot["protocol_consistency"] = protocol_state
    snapshot["protocol_explanation"] = protocol_explanation
    return snapshot


def write_human_heartbeat(state: dict[str, Any]) -> None:
    snapshots = {
        runtime_key: runtime_snapshot(runtime_key, state.get(runtime_key, {}))
        for runtime_key in sorted(RUNTIMES)
    }
    non_terminal_runtimes = [
        snapshot["runtime_label"]
        for snapshot in snapshots.values()
        if snapshot["display_status"] != "terminal_complete"
    ]

    for snapshot in snapshots.values():
        if snapshot["display_status"] == "terminal_complete" and non_terminal_runtimes:
            snapshot["display_status"] = "waiting_peers"
            snapshot["progress_expectation"] = (
                f"this runtime finished its local scope, but the wave is not globally complete because "
                f"{', '.join(non_terminal_runtimes)} "
                f"{'is' if len(non_terminal_runtimes) == 1 else 'are'} still unresolved"
            )

    active_runtimes = [
        snapshot["runtime_label"]
        for snapshot in snapshots.values()
        if snapshot["display_status"] == "active"
    ]
    terminal_runtimes = [
        snapshot["runtime_label"]
        for snapshot in snapshots.values()
        if snapshot["display_status"] in {"terminal_complete", "waiting_peers"}
    ]
    waiting_peer_runtimes = [
        snapshot["runtime_label"]
        for snapshot in snapshots.values()
        if snapshot["display_status"] == "waiting_peers"
    ]
    attention_runtimes = [
        snapshot["runtime_label"]
        for snapshot in snapshots.values()
        if snapshot["display_status"] == "needs_attention"
    ]
    inconsistent_runtimes = [
        snapshot["runtime_label"]
        for snapshot in snapshots.values()
        if snapshot["display_status"] == "protocol_inconsistent" or snapshot["protocol_consistency"] == "mismatch"
    ]
    weak_protocol_runtimes = [
        snapshot["runtime_label"]
        for snapshot in snapshots.values()
        if snapshot["protocol_consistency"] == "weak"
    ]

    if attention_runtimes:
        system_display_status = "needs_attention"
        system_progress_expectation = (
            f"system requires intervention because {', '.join(attention_runtimes)} "
            f"{'has' if len(attention_runtimes) == 1 else 'have'} an unresolved blocker"
        )
    elif inconsistent_runtimes:
        system_display_status = "degraded"
        system_progress_expectation = (
            f"system is degraded: final protocol signals do not match for "
            f"{', '.join(inconsistent_runtimes)}"
        )
    elif weak_protocol_runtimes:
        system_display_status = "degraded"
        system_progress_expectation = (
            f"system is degraded: protocol confirmation is weaker than expected for "
            f"{', '.join(weak_protocol_runtimes)}"
        )
    elif any(snapshot["display_status"] == "protocol_stale" for snapshot in snapshots.values()):
        stale_runtimes = [
            snapshot["runtime_label"]
            for snapshot in snapshots.values()
            if snapshot["display_status"] == "protocol_stale"
        ]
        system_display_status = "degraded"
        system_progress_expectation = (
            f"system is degraded: {', '.join(stale_runtimes)} "
            f"{'has' if len(stale_runtimes) == 1 else 'have'} stale control signals"
        )
    elif any(snapshot["display_status"] == "dispatching" for snapshot in snapshots.values()):
        dispatching_runtimes = [
            snapshot["runtime_label"]
            for snapshot in snapshots.values()
            if snapshot["display_status"] == "dispatching"
        ]
        system_display_status = "active"
        system_progress_expectation = (
            f"wave is still running; runtime{'s' if len(dispatching_runtimes) != 1 else ''} "
            f"starting next step: {', '.join(dispatching_runtimes)}"
        )
    elif waiting_peer_runtimes:
        system_display_status = "waiting_peers"
        system_progress_expectation = (
            f"some runtimes finished their local scope and are waiting at a shared barrier: "
            f"{', '.join(waiting_peer_runtimes)}"
        )
    elif active_runtimes:
        system_display_status = "active"
        system_progress_expectation = (
            f"wave is still running; active runtime{'s' if len(active_runtimes) != 1 else ''}: "
            f"{', '.join(active_runtimes)}"
        )
    else:
        system_display_status = "terminal_complete"
        system_progress_expectation = "all runtimes finished the current autonomous wave"

    lines = [
        "# Human Progress",
        "",
        "> Версия файла: `v1.0`",
        f"> Дата версии: `{datetime.now().date().isoformat()}`",
        "> Тип документа: `human heartbeat`",
        "",
        f"- heartbeat_at: `{now_utc()}`",
        f"- orchestrator_pid: `{os.getpid()}`",
        f"- system_display_status: `{system_display_status}`",
        f"- system_progress_expectation: `{system_progress_expectation}`",
        f"- active_runtimes: `{', '.join(active_runtimes) if active_runtimes else 'none'}`",
        f"- terminal_runtimes: `{', '.join(terminal_runtimes) if terminal_runtimes else 'none'}`",
        f"- attention_runtimes: `{', '.join(attention_runtimes) if attention_runtimes else 'none'}`",
        "",
        "Этот файл обновляется самим execution plane на каждом цикле и является главным человеко-читаемым окном состояния.",
        "",
    ]

    for runtime_key in sorted(RUNTIMES):
        snapshot = snapshots[runtime_key]
        worker_state = "alive" if snapshot["worker_alive"] else "not_running"
        lines.extend(
            [
                f"## {snapshot['runtime_label']}",
                "",
                f"- current_run: `{snapshot['current_run']}`",
                f"- display_status: `{snapshot['display_status']}`",
                f"- progress_expectation: `{snapshot['progress_expectation']}`",
                f"- runtime_status: `{snapshot['runtime_status']}`",
                f"- runtime_updated_at: `{snapshot['updated_at']}`",
                f"- observer_directive: `{snapshot['directive_id']} / {snapshot['directive_action']} / {snapshot['directive_status']}`",
                f"- runtime_ack: `{snapshot['ack_id']} / {snapshot['ack_status']}`",
                f"- protocol_consistency: `{snapshot['protocol_consistency']}`",
                f"- protocol_explanation: `{snapshot['protocol_explanation']}`",
                f"- next_action: `{snapshot['ack_next_action']}`",
                f"- worker_process: `{worker_state}`",
                f"- worker_pid: `{snapshot['worker_pid'] or 'none'}`",
                f"- status_signal_age_seconds: `{snapshot['status_signal_age_seconds']}`",
                f"- ack_signal_age_seconds: `{snapshot['ack_signal_age_seconds']}`",
                f"- log_signal_age_seconds: `{snapshot['log_signal_age_seconds']}`",
                f"- log_size_bytes: `{snapshot['log_size_bytes']}`",
                f"- observer_phase: `{snapshot['observer_phase']}`",
                f"- open_backlog_item: `{snapshot['open_backlog_item']}`",
                f"- needs_human: `{snapshot['needs_human']}`",
                f"- blocking_issue: `{snapshot['blocking_issue']}`",
                f"- log_file: `{snapshot['log_file']}`",
                "",
            ]
        )

    recent_events = read_recent_events()
    lines.extend(["## Recent Events", ""])
    if recent_events:
        lines.extend(recent_events)
    else:
        lines.append("- `no events yet`")
    lines.append("")
    HEARTBEAT_FILE.write_text("\n".join(lines))


def build_command(runtime_key: str) -> tuple[list[str], Path, Path, str | None]:
    cfg = RUNTIMES[runtime_key]
    runtime_dir: Path = cfg["runtime_dir"]
    last_message_file = LAST_MESSAGES_DIR / f"{runtime_key}_last_message.txt"

    if runtime_key == "codex":
        command = cfg["launch_command"] + [
            "-C",
            str(runtime_dir),
            "-o",
            str(last_message_file),
            cfg["prompt"],
        ]
        stdin_prompt = None
    else:
        command = cfg["launch_command"] + [
            "--settings",
            str(cfg["settings_file"]),
            "--add-dir",
            str(runtime_dir),
        ]
        stdin_prompt = cfg["prompt"]

    return command, runtime_dir, last_message_file, stdin_prompt


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
    based_on_run = directive_fields.get("based_on_run", "")
    ack_id = ack_fields.get("directive_id", "")
    ack_status = ack_fields.get("ack_status", "not_seen")
    current_run = status_fields.get("current_run", "")
    runtime_status = status_fields.get("status", "")
    last_finished_at = parse_iso_timestamp(runtime_state.get("finished_at"))
    now = datetime.now(timezone.utc)

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

    if action in {"prepare_comparison", "repair_current_state", "stop", "human_review_required"}:
        if ack_id == directive_id and ack_status == "completed":
            return False, f"{action} directive already completed"
        if ack_id == directive_id and ack_status == "accepted":
            if not last_finished_at or (now - last_finished_at) >= STALE_RETRY_COOLDOWN:
                return True, f"stale {action} without live process; redispatch"
            return False, f"{action} cooling down"
        return True, f"dispatch action={action}"

    # If the current directive has already been accepted and the runtime is now working
    # or already completed the corresponding step, avoid duplicate launches.
    if ack_id == directive_id and ack_status in {"accepted", "completed"}:
        if runtime_status == "in_progress":
            if not last_finished_at or (now - last_finished_at) >= STALE_RETRY_COOLDOWN:
                return True, "stale in_progress without live process; redispatch"
            return False, "stale in_progress cooling down"
        if based_on_run and current_run and current_run != based_on_run:
            return False, "runtime already moved beyond the source run"

    return True, f"dispatch action={action}"


def launch_runtime(runtime_key: str, runtime_state: dict[str, Any]) -> dict[str, Any]:
    command, cwd, _, stdin_prompt = build_command(runtime_key)
    log_path = LOG_DIR / f"{runtime_key}_{int(time.time())}.log"
    with log_path.open("wb") as log_handle:
        process = subprocess.Popen(
            command,
            cwd=str(cwd),
            stdin=subprocess.PIPE if stdin_prompt is not None else None,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            text=True,
        )
        if stdin_prompt is not None and process.stdin is not None:
            process.stdin.write(stdin_prompt)
            process.stdin.close()

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
    project_control_plane(runtime_key)
    status_fields = parse_markdown_fields(cfg["status_file"])
    directive_fields = parse_markdown_fields(cfg["directive_file"])
    ack_fields = parse_markdown_fields(cfg["ack_file"])
    mirror_runtime_outputs(runtime_key)

    runtime_state = state.setdefault(runtime_key, {})
    running_pid = runtime_state.get("running_pid")
    if running_pid and not pid_alive(running_pid):
        runtime_state["running"] = False
        runtime_state["running_pid"] = None
        runtime_state["finished_at"] = now_utc()

    stall = stall_reason(runtime_key, runtime_state, status_fields, directive_fields, ack_fields)
    if stall:
        terminate_process_group(running_pid)
        runtime_state["running"] = False
        runtime_state["running_pid"] = None
        runtime_state["finished_at"] = now_utc()
        append_event(f"{runtime_key}: watchdog terminated stalled runtime ({stall})")
        if verbose:
            print(f"[{runtime_key}] watchdog terminated stalled runtime")
        status_fields = parse_markdown_fields(cfg["status_file"])
        directive_fields = parse_markdown_fields(cfg["directive_file"])
        ack_fields = parse_markdown_fields(cfg["ack_file"])

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
        maybe_advance_observer(runtime_key, state, verbose=verbose)
    for runtime_key in sorted(RUNTIMES):
        reconcile_runtime(runtime_key, state, verbose=verbose)
    save_state(state)
    write_human_heartbeat(state)


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
