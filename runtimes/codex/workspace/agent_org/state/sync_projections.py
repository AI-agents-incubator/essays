#!/usr/bin/env python3
"""Generate markdown control-plane projections from the live SQLite state."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


TABLES = [
    "organization_runs",
    "roles",
    "work_items",
    "handoff_events",
    "artifact_registry",
    "benchmark_runs",
    "audit_findings",
    "improvement_backlog",
    "change_proposals",
    "approved_changes",
    "state_variables",
]

STAGE_OWNERS = {
    "intake": "business-sponsor-interface",
    "product": "product-lead",
    "engineering": "engineering-manager",
    "implementation": "implementation-agent",
    "review": "review-and-integration-agent",
    "benchmark": "benchmark-and-audit-agent",
    "learning": "learning-agent",
    "archived": "learning-agent",
}

NON_TRIGGERING_STATE_VARIABLE_KEYS = {
    ("state", "last_projection_at"),
    ("state", "registry_status"),
    ("state", "projection_watcher_launch_mode"),
    ("state", "projection_watcher_last_exit_code"),
    ("state", "projection_watcher_pid"),
    ("state", "projection_watcher_started_at"),
    ("state", "projection_watcher_status"),
    ("state", "projection_watcher_stopped_at"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Project selected markdown control-plane files from SQLite."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if generated content differs from files on disk",
    )
    parser.add_argument(
        "--run-id",
        help="override the run id recorded with projection metadata updates",
    )
    parser.add_argument(
        "--no-update-state-metadata",
        action="store_true",
        help="write projections without updating freshness metadata in SQLite",
    )
    return parser.parse_args()


def current_timestamp() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def open_connection(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all(
    conn: sqlite3.Connection, query: str, params: tuple[object, ...] = ()
) -> list[sqlite3.Row]:
    return conn.execute(query, params).fetchall()


def fetch_one(
    conn: sqlite3.Connection, query: str, params: tuple[object, ...] = ()
) -> sqlite3.Row | None:
    return conn.execute(query, params).fetchone()


def state_var_map(conn: sqlite3.Connection) -> dict[tuple[str, str], sqlite3.Row]:
    rows = fetch_all(
        conn,
        """
        SELECT scope, key, value, run_id, updated_at
        FROM state_variables
        ORDER BY scope, key
        """,
    )
    return {(row["scope"], row["key"]): row for row in rows}


def state_var_value(
    variables: dict[tuple[str, str], sqlite3.Row],
    scope: str,
    key: str,
    default: str = "not recorded",
) -> str:
    row = variables.get((scope, key))
    return row["value"] if row else default


def upsert_state_variable(
    conn: sqlite3.Connection,
    scope: str,
    key: str,
    value: str,
    run_id: str | None,
    updated_at: str,
) -> None:
    conn.execute(
        """
        INSERT INTO state_variables (scope, key, value, runtime, run_id, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(scope, key) DO UPDATE SET
            value = excluded.value,
            runtime = excluded.runtime,
            run_id = excluded.run_id,
            updated_at = excluded.updated_at
        """,
        (scope, key, value, "codex", run_id, updated_at),
    )


def current_run_id(conn: sqlite3.Connection) -> str | None:
    row = fetch_one(
        conn,
        """
        SELECT value
        FROM state_variables
        WHERE scope = 'runtime' AND key = 'current_run'
        """,
    )
    return row["value"] if row else None


def update_projection_metadata(
    conn: sqlite3.Connection,
    run_id: str | None = None,
    projected_at: str | None = None,
) -> str:
    applied_at = projected_at or current_timestamp()
    applied_run_id = run_id or current_run_id(conn)
    upsert_state_variable(
        conn,
        "state",
        "last_projection_at",
        applied_at,
        applied_run_id,
        applied_at,
    )
    upsert_state_variable(
        conn,
        "state",
        "registry_status",
        "in_sync",
        applied_run_id,
        applied_at,
    )
    conn.commit()
    return applied_at


def projection_targets_list(
    variables: dict[tuple[str, str], sqlite3.Row],
) -> list[str]:
    raw = state_var_value(variables, "state", "projection_targets", "")
    return [item.strip() for item in raw.split(",") if item.strip()]


def projection_count(targets: list[str], prefix: str | None = None) -> int:
    if prefix is None:
        return len(targets)
    return sum(1 for item in targets if item.startswith(prefix))


def normalized_date(timestamp: str) -> str:
    return timestamp.split(" ")[0] if timestamp else "n/a"


def role_summary(conn: sqlite3.Connection) -> list[str]:
    runs = fetch_all(
        conn,
        """
        SELECT run_id, COUNT(*) AS role_count
        FROM roles
        GROUP BY run_id
        ORDER BY run_id
        """,
    )
    rows: list[str] = []
    for run in runs:
        statuses = fetch_all(
            conn,
            """
            SELECT status
            FROM roles
            WHERE run_id = ?
            ORDER BY role_type
            """,
            (run["run_id"],),
        )
        distinct_statuses = sorted({row["status"] for row in statuses})
        summary = ", ".join(distinct_statuses)
        rows.append(
            f"- `{run['run_id']}` | `{run['role_count']}` roles recorded | status: `{summary}`"
        )
    return rows


def handoff_summary(conn: sqlite3.Connection) -> list[str]:
    runs = fetch_all(
        conn,
        """
        SELECT run_id, MIN(id) AS first_id, MAX(id) AS last_id, COUNT(*) AS handoff_count
        FROM handoff_events
        GROUP BY run_id
        ORDER BY run_id
        """,
    )
    return [
        f"- `{row['run_id']}` | `{row['first_id']}` .. `{row['last_id']}` | count: `{row['handoff_count']}` | log: `execution/handoff_log.md`"
        for row in runs
    ]


def row_count_lines(conn: sqlite3.Connection) -> list[str]:
    lines: list[str] = []
    for table in TABLES:
        count = fetch_one(conn, f"SELECT COUNT(*) AS count FROM {table}")
        lines.append(f"- `{table}`: `{count['count']}`")
    return lines


def render_state_registry(conn: sqlite3.Connection) -> str:
    variables = state_var_map(conn)
    runs = fetch_all(
        conn,
        """
        SELECT id, benchmark_id, status, summary_path
        FROM organization_runs
        ORDER BY started_at
        """,
    )
    work_items = fetch_all(
        conn,
        """
        SELECT id, run_id, current_stage, status, product_brief_path, engineering_spec_path
        FROM work_items
        ORDER BY id
        """,
    )
    artifacts = fetch_all(
        conn,
        """
        SELECT path
        FROM artifact_registry
        ORDER BY updated_at, id
        """,
    )
    sync_note = state_var_value(variables, "state", "last_projection_at")
    current_run_value = state_var_value(variables, "runtime", "current_run", "unknown")
    refresh_mode = state_var_value(variables, "state", "projection_refresh_mode", "manual")
    watcher_status = state_var_value(
        variables, "state", "projection_watcher_status", "not recorded"
    )
    watcher_launch_mode = state_var_value(
        variables, "state", "projection_watcher_launch_mode", "not recorded"
    )

    lines = [
        "# State Registry",
        "",
        "Purpose: map operational entities to artifacts and live run context.",
        "",
        "Owner: `engineering-manager`",
        "",
        "Projection status:",
        "- source_of_truth: `state/runtime_state.sqlite`",
        "- projection_script: `state/sync_projections.py`",
        f"- projected_at: `{sync_note}`",
        f"- refresh_mode: `{refresh_mode}`",
        f"- watcher_status: `{watcher_status}`",
        f"- watcher_launch_mode: `{watcher_launch_mode}`",
        f"- current_run: `{current_run_value}`",
        "",
        "State layer:",
        "- mode: `SQLite-first`",
        "- schema: `state/sqlite_schema.sql`",
        "- live_db: `state/runtime_state.sqlite`",
        "- live_db_status: present and queryable",
        "- activation_run: `RUN-002`",
        "",
        "Run ledger:",
    ]
    lines.extend(
        [
            f"- `{row['id']}` | benchmark: `{row['benchmark_id']}` | status: `{row['status']}` | summary: `{row['summary_path'] or 'pending'}`"
            for row in runs
        ]
    )
    lines.extend(["", "Roles:"])
    lines.extend(role_summary(conn))
    lines.extend(["", "Work items:"])
    lines.extend(
        [
            f"- `{row['id']}` | run: `{row['run_id']}` | stage: `{row['current_stage']}` | status: `{row['status']}` | product brief: `{row['product_brief_path'] or 'n/a'}` | engineering spec: `{row['engineering_spec_path'] or 'n/a'}`"
            for row in work_items
        ]
    )
    lines.extend(["", "Handoffs:"])
    lines.extend(handoff_summary(conn))
    lines.extend(["", "Representative artifacts registered in SQLite:"])
    lines.extend([f"- `{row['path']}`" for row in artifacts])
    lines.extend(["", "SQLite row counts:"])
    lines.extend(row_count_lines(conn))
    lines.extend(["", "State variables:"])
    lines.extend(
        [
            f"- `{row['scope']}.{row['key']} = {row['value']}`"
            for row in variables.values()
        ]
    )
    lines.extend(
        [
            "",
            "Update rules:",
            "- Write operational changes to SQLite first.",
            "- Regenerate this file with `python3 state/sync_projections.py`.",
            "- Treat SQLite as the operational source and this registry as its readable projection.",
            "",
        ]
    )
    return "\n".join(lines)


def render_demand_queue(conn: sqlite3.Connection) -> str:
    work_items = fetch_all(
        conn,
        """
        SELECT id, run_id, source_signal, priority, status
        FROM work_items
        ORDER BY id
        """,
    )
    variables = state_var_map(conn)
    sync_note = state_var_value(variables, "state", "last_projection_at")

    lines = [
        "# Demand Queue",
        "",
        "Purpose: track active and queued work items.",
        "",
        "Owner: `product-lead`",
        "",
        "Projection status:",
        "- source_of_truth: `state/runtime_state.sqlite`",
        "- projection_script: `state/sync_projections.py`",
        f"- projected_at: `{sync_note}`",
        "",
        "Queue:",
    ]
    lines.extend(
        [
            f"- `{row['id']}` | run: `{row['run_id']}` | status: `{row['status']}` | signal: {row['source_signal']} | priority: `{row['priority'] or 'n/a'}`"
            for row in work_items
        ]
    )
    lines.extend(
        [
            "",
            "Update rules:",
            "- New items and status transitions must be written to SQLite first.",
            "- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.",
            "",
            "Links:",
            "- `execution/status_board.md`",
            "- `state/state_registry.md`",
            "",
        ]
    )
    return "\n".join(lines)


def render_status_board(conn: sqlite3.Connection) -> str:
    work_items = fetch_all(
        conn,
        """
        SELECT id, current_stage, status
        FROM work_items
        ORDER BY id
        """,
    )
    variables = state_var_map(conn)
    sync_note = state_var_value(variables, "state", "last_projection_at")

    lines = [
        "# Status Board",
        "",
        "Purpose: track current execution status of work items.",
        "",
        "Owner: `implementation-agent`",
        "",
        "Projection status:",
        "- source_of_truth: `state/runtime_state.sqlite`",
        "- projection_script: `state/sync_projections.py`",
        f"- projected_at: `{sync_note}`",
        "",
        "Tracked items:",
    ]
    for row in work_items:
        owner = STAGE_OWNERS.get(row["current_stage"], "engineering-manager")
        lines.append(
            f"- `{row['id']}` | status: `{row['status']}` | stage: `{row['current_stage']}` | owner: `{owner}`"
        )
    lines.extend(
        [
            "",
            "Update rules:",
            "- Stage and status changes must be written to SQLite first.",
            "- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.",
            "",
            "Links:",
            "- `execution/work_orders/`",
            "",
        ]
    )
    return "\n".join(lines)


def render_benchmark_results(conn: sqlite3.Connection) -> str:
    rows = fetch_all(
        conn,
        """
        SELECT benchmark_id, run_id, status, notes, created_at
        FROM benchmark_runs
        ORDER BY created_at, id
        """,
    )
    variables = state_var_map(conn)
    sync_note = state_var_value(variables, "state", "last_projection_at")

    lines = [
        "# Benchmark Results",
        "",
        "Purpose: record benchmark outcomes.",
        "",
        "Owner: `benchmark-and-audit-agent`",
        "",
        "Projection status:",
        "- source_of_truth: `state/runtime_state.sqlite`",
        "- projection_script: `state/sync_projections.py`",
        f"- projected_at: `{sync_note}`",
        "",
        "Results:",
    ]
    lines.extend(
        [
            f"- `{row['benchmark_id']}` | run: `{row['run_id']}` | status: `{row['status']}` | date: `{normalized_date(row['created_at'])}` | notes: {row['notes']}"
            for row in rows
        ]
    )
    lines.extend(
        [
            "",
            "Update rules:",
            "- Benchmark outcomes must be written to SQLite first.",
            "- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.",
            "",
        ]
    )
    return "\n".join(lines)


def render_process_audits(conn: sqlite3.Connection) -> str:
    benchmark_rows = fetch_all(
        conn,
        """
        SELECT id, run_id, notes
        FROM benchmark_runs
        ORDER BY created_at, id
        """,
    )
    finding_rows = fetch_all(
        conn,
        """
        SELECT benchmark_run_id, severity, category, description, recommendation
        FROM audit_findings
        ORDER BY created_at, id
        """,
    )
    findings_by_run: dict[str, list[sqlite3.Row]] = defaultdict(list)
    for row in finding_rows:
        findings_by_run[row["benchmark_run_id"]].append(row)

    variables = state_var_map(conn)
    sync_note = state_var_value(variables, "state", "last_projection_at")

    lines = [
        "# Process Audits",
        "",
        "Purpose: capture audit findings for each run.",
        "",
        "Owner: `benchmark-and-audit-agent`",
        "",
        "Projection status:",
        "- source_of_truth: `state/runtime_state.sqlite`",
        "- projection_script: `state/sync_projections.py`",
        f"- projected_at: `{sync_note}`",
        "",
        "Audits:",
    ]
    for benchmark in benchmark_rows:
        findings = findings_by_run.get(benchmark["id"], [])
        if not findings:
            lines.append(
                f"- `{benchmark['run_id']}` | severity: `none` | category: `baseline` | summary: No explicit audit finding recorded; {benchmark['notes']}"
            )
            continue
        for finding in findings:
            recommendation = finding["recommendation"] or "none"
            lines.append(
                f"- `{benchmark['run_id']}` | severity: `{finding['severity']}` | category: `{finding['category']}` | summary: {finding['description']} | recommendation: {recommendation}"
            )
    lines.extend(
        [
            "",
            "Update rules:",
            "- Audit findings must be written to SQLite first.",
            "- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.",
            "",
        ]
    )
    return "\n".join(lines)


def render_metric_dashboard(conn: sqlite3.Connection) -> str:
    variables = state_var_map(conn)
    targets = projection_targets_list(variables)
    runs_total = fetch_one(conn, "SELECT COUNT(*) AS count FROM organization_runs")
    completed_runs = fetch_one(
        conn,
        "SELECT COUNT(*) AS count FROM organization_runs WHERE status = 'completed'",
    )
    benchmark_total = fetch_one(conn, "SELECT COUNT(*) AS count FROM benchmark_runs")
    benchmark_pass = fetch_one(
        conn,
        "SELECT COUNT(*) AS count FROM benchmark_runs WHERE status = 'pass'",
    )
    open_improvements = fetch_one(
        conn,
        """
        SELECT COUNT(*) AS count
        FROM improvement_backlog
        WHERE status NOT IN ('complete', 'implemented', 'closed')
        """,
    )
    proposed_changes = fetch_one(
        conn,
        "SELECT COUNT(*) AS count FROM change_proposals WHERE status = 'proposed'",
    )
    implemented_changes = fetch_one(
        conn,
        "SELECT COUNT(*) AS count FROM approved_changes WHERE status = 'implemented'",
    )

    benchmark_ratio = "0% (0/0)"
    if benchmark_total["count"]:
        ratio = int((benchmark_pass["count"] / benchmark_total["count"]) * 100)
        benchmark_ratio = (
            f"{ratio}% ({benchmark_pass['count']}/{benchmark_total['count']})"
        )

    registry_status = state_var_value(variables, "state", "registry_status")
    sync_note = state_var_value(variables, "state", "last_projection_at")
    current_run = state_var_value(variables, "runtime", "current_run", "unknown")
    refresh_mode = state_var_value(
        variables, "state", "projection_refresh_mode", "manual"
    )
    watcher_status = state_var_value(
        variables, "state", "projection_watcher_status", "not recorded"
    )
    watcher_launch_mode = state_var_value(
        variables, "state", "projection_watcher_launch_mode", "not recorded"
    )

    lines = [
        "# Metric Dashboard",
        "",
        "Purpose: track operational metrics and scorecard signals over time.",
        "",
        "Owner: `benchmark-and-audit-agent`",
        "",
        "Projection status:",
        "- source_of_truth: `state/runtime_state.sqlite`",
        "- projection_script: `state/sync_projections.py`",
        f"- projected_at: `{sync_note}`",
        "",
        "Metrics:",
        f"- current_run: `{current_run}`",
        f"- completed_runs: `{completed_runs['count']}` / `{runs_total['count']}`",
        f"- benchmark_pass_rate: `{benchmark_ratio}`",
        f"- projection_sync_active: `{'yes' if registry_status == 'in_sync' else 'no'}`",
        f"- projection_refresh_mode: `{refresh_mode}`",
        f"- projection_watcher_status: `{watcher_status}`",
        f"- projection_watcher_launch_mode: `{watcher_launch_mode}`",
        f"- projected_control_plane_views: `{projection_count(targets)}`",
        f"- projected_evaluation_views: `{projection_count(targets, 'evaluation/')}`",
        f"- projected_evolution_views: `{projection_count(targets, 'evolution/')}`",
        f"- open_improvements: `{open_improvements['count']}`",
        f"- proposed_change_proposals: `{proposed_changes['count']}`",
        f"- implemented_changes: `{implemented_changes['count']}`",
    ]
    lines.extend(
        [
            "",
            "Update rules:",
            "- Scorecard metrics must be derived from SQLite state and state variables.",
            "- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.",
            "",
        ]
    )
    return "\n".join(lines)


def render_improvement_backlog(conn: sqlite3.Connection) -> str:
    backlog_rows = fetch_all(
        conn,
        """
        SELECT id, title, source_reference, status
        FROM improvement_backlog
        ORDER BY id
        """,
    )
    proposal_rows = fetch_all(
        conn,
        """
        SELECT backlog_item_id, id
        FROM change_proposals
        WHERE backlog_item_id IS NOT NULL
        ORDER BY id
        """,
    )
    proposals_by_backlog: dict[str, list[str]] = defaultdict(list)
    for row in proposal_rows:
        proposals_by_backlog[row["backlog_item_id"]].append(row["id"])

    variables = state_var_map(conn)
    sync_note = state_var_value(variables, "state", "last_projection_at")

    lines = [
        "# Improvement Backlog",
        "",
        "Purpose: track learning-driven improvements.",
        "",
        "Owner: `learning-agent`",
        "",
        "Projection status:",
        "- source_of_truth: `state/runtime_state.sqlite`",
        "- projection_script: `state/sync_projections.py`",
        f"- projected_at: `{sync_note}`",
        "",
        "Backlog:",
    ]
    for row in backlog_rows:
        linked = ", ".join(f"`{item}`" for item in proposals_by_backlog.get(row["id"], []))
        proposal_note = linked if linked else "`n/a`"
        lines.append(
            f"- `{row['id']}` | {row['title']} | source: {row['source_reference']} | status: `{row['status']}` | proposals: {proposal_note}"
        )
    lines.extend(
        [
            "",
            "Update rules:",
            "- Learning backlog changes must be written to SQLite first.",
            "- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.",
            "",
        ]
    )
    return "\n".join(lines)


def render_change_proposals(conn: sqlite3.Connection) -> str:
    rows = fetch_all(
        conn,
        """
        SELECT id, target_artifact, proposal_type, expected_effect, status, backlog_item_id
        FROM change_proposals
        ORDER BY id
        """,
    )
    variables = state_var_map(conn)
    sync_note = state_var_value(variables, "state", "last_projection_at")

    lines = [
        "# Change Proposals",
        "",
        "Purpose: capture proposed structural changes.",
        "",
        "Owner: `learning-agent`",
        "",
        "Projection status:",
        "- source_of_truth: `state/runtime_state.sqlite`",
        "- projection_script: `state/sync_projections.py`",
        f"- projected_at: `{sync_note}`",
        "",
        "Proposals:",
    ]
    for row in rows:
        backlog = row["backlog_item_id"] or "n/a"
        lines.append(
            f"- `{row['id']}` | target: `{row['target_artifact']}` | type: `{row['proposal_type']}` | expected effect: {row['expected_effect']} | status: `{row['status']}` | backlog: `{backlog}`"
        )
    lines.extend(
        [
            "",
            "Update rules:",
            "- Change proposals must be written to SQLite first.",
            "- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.",
            "",
        ]
    )
    return "\n".join(lines)


def render_approved_changes(conn: sqlite3.Connection) -> str:
    rows = fetch_all(
        conn,
        """
        SELECT id, run_id, source_reference, change_summary, status
        FROM approved_changes
        ORDER BY id
        """,
    )
    variables = state_var_map(conn)
    sync_note = state_var_value(variables, "state", "last_projection_at")

    lines = [
        "# Approved Changes",
        "",
        "Purpose: record approved and implemented changes.",
        "",
        "Owner: `business-sponsor-interface`",
        "",
        "Projection status:",
        "- source_of_truth: `state/runtime_state.sqlite`",
        "- projection_script: `state/sync_projections.py`",
        f"- projected_at: `{sync_note}`",
        "",
        "Approved:",
    ]
    for row in rows:
        source = row["source_reference"] or "n/a"
        lines.append(
            f"- `{row['id']}` | run: `{row['run_id']}` | source: `{source}` | change: {row['change_summary']} | status: `{row['status']}`"
        )
    lines.extend(
        [
            "",
            "Update rules:",
            "- Approved change records must be written to SQLite first.",
            "- Regenerate this file with `python3 state/sync_projections.py` instead of editing it by hand.",
            "",
        ]
    )
    return "\n".join(lines)


def projection_targets_from_connection(
    state_dir: Path, conn: sqlite3.Connection
) -> dict[Path, str]:
    agent_org_dir = state_dir.parent
    return {
        state_dir / "state_registry.md": render_state_registry(conn),
        agent_org_dir / "intake" / "demand_queue.md": render_demand_queue(conn),
        agent_org_dir / "execution" / "status_board.md": render_status_board(conn),
        agent_org_dir / "evaluation" / "benchmark_results.md": render_benchmark_results(conn),
        agent_org_dir / "evaluation" / "process_audits.md": render_process_audits(conn),
        agent_org_dir / "evaluation" / "metric_dashboard.md": render_metric_dashboard(conn),
        agent_org_dir / "evolution" / "improvement_backlog.md": render_improvement_backlog(conn),
        agent_org_dir / "evolution" / "change_proposals.md": render_change_proposals(conn),
        agent_org_dir / "evolution" / "approved_changes.md": render_approved_changes(conn),
    }


def projection_targets(state_dir: Path) -> dict[Path, str]:
    db_path = state_dir / "runtime_state.sqlite"
    conn = open_connection(db_path)
    try:
        return projection_targets_from_connection(state_dir, conn)
    finally:
        conn.close()


def sync_projection_targets(
    state_dir: Path,
    *,
    check: bool = False,
    update_state_metadata: bool = True,
    run_id: str | None = None,
) -> tuple[list[Path], int]:
    db_path = state_dir / "runtime_state.sqlite"
    conn = open_connection(db_path)
    try:
        if update_state_metadata:
            update_projection_metadata(conn, run_id=run_id)
        targets = projection_targets_from_connection(state_dir, conn)
    finally:
        conn.close()

    stale: list[Path] = []
    updated_count = 0
    for path, content in targets.items():
        existing = path.read_text(encoding="utf-8") if path.exists() else None
        if existing != content:
            updated_count += 1
            if check:
                stale.append(path)
            else:
                path.write_text(content, encoding="utf-8")

    return stale, updated_count


def main() -> int:
    args = parse_args()
    state_dir = Path(__file__).resolve().parent
    update_state_metadata = not args.check and not args.no_update_state_metadata
    stale, updated_count = sync_projection_targets(
        state_dir,
        check=args.check,
        update_state_metadata=update_state_metadata,
        run_id=args.run_id,
    )

    if args.check:
        if stale:
            for path in stale:
                print(f"stale projection: {path}", file=sys.stderr)
            return 1
        print("projection files are in sync")
    else:
        print(f"updated {updated_count} projection files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
