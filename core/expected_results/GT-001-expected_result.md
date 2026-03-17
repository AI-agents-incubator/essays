# GT-001 Expected Result

> Версия файла: `v1.0`
> Дата версии: `2026-03-16`
> Тип документа: `expected result signature`
> Основание:
> - [expected_result_template.md](./expected_result_template.md)
> - [../benchmarks/GT-001-bootstrap-runtime-sandbox.md](../benchmarks/GT-001-bootstrap-runtime-sandbox.md)
>

## Result Identity

- benchmark: `GT-001`
- expected result version: `v1.0`

## Итоговые артефакты

После успешного прогона обязаны существовать:

### В runtime workspace

- `agent_org/charter/mission.md`
- `agent_org/charter/scope_and_boundaries.md`
- `agent_org/charter/role_map.md`
- `agent_org/charter/autonomy_model.md`
- `agent_org/policies/escalation_policy.md`
- `agent_org/policies/risk_policy.md`
- `agent_org/policies/quality_gates.md`
- `agent_org/policies/artifact_change_policy.md`
- `agent_org/intake/external_signals.md`
- `agent_org/intake/demand_queue.md`
- `agent_org/intake/triage_rules.md`
- `agent_org/product/product_brief_template.md`
- `agent_org/engineering/engineering_spec_template.md`
- `agent_org/engineering/task_graph.md`
- `agent_org/engineering/contract_registry.md`
- `agent_org/engineering/dependency_map.md`
- `agent_org/execution/status_board.md`
- `agent_org/execution/handoff_log.md`
- `agent_org/execution/integration_log.md`
- `agent_org/knowledge/decision_log.md`
- `agent_org/knowledge/domain_glossary.md`
- `agent_org/knowledge/pattern_library.md`
- `agent_org/knowledge/failure_library.md`
- `agent_org/evaluation/golden_tasks.md`
- `agent_org/evaluation/benchmark_results.md`
- `agent_org/evaluation/process_audits.md`
- `agent_org/evaluation/metric_dashboard.md`
- `agent_org/state/README.md`
- `agent_org/state/state_registry.md`
- `agent_org/state/storage_strategy.md`
- `agent_org/state/sqlite_schema.sql`
- `agent_org/state/supabase_migration_path.md`
- `agent_org/evolution/improvement_backlog.md`
- `agent_org/evolution/change_proposals.md`
- `agent_org/evolution/approved_changes.md`
- `agent_org/bootstrap/startup_sequence.md`
- `agent_org/bootstrap/first_run_protocol.md`

### Runtime-specific артефакты

Ожидается, что будут существовать runtime-файлы, соответствующие addendum:

- для `Codex`:
  - `AGENTS.md`
  - `.codex/config.toml`
  - `.codex/agents/`
  - `.agents/skills/`

- для `Claude Code`:
  - `CLAUDE.md`
  - `.claude/settings.json`
  - `.claude/agents/`
  - `.claude/skills/`
  - при необходимости `.claude/rules/` и `.claude/hooks/`

### Trace-артефакты

Ожидается наличие:
- как минимум одного run trace;
- как минимум одного benchmark result;
- как минимум одного process audit;
- как минимум одной learning-записи о дефиците или улучшении.

## Ключевые свойства результата

### 1. Полнота

Структура не должна обрываться на нескольких README. Она должна представлять собой минимально рабочую инфраструктуру, по которой можно делать следующий запуск.

### 2. Связность

Артефакты должны быть связаны между собой:
- product должен вести в engineering;
- engineering должен вести в execution;
- execution должен вести в evaluation;
- evaluation должен вести в evolution.

### 3. Изоляция

Результат должен быть создан только внутри своей runtime-песочницы.

### 4. Состоятельность state layer

State layer должен:
- быть физически создан;
- быть связан с artifact layer;
- быть пригодным для фиксации run state;
- быть рассчитанным на SQLite-first режим.

### 5. Пригодность к следующему запуску

После завершения GT-001 следующий агент должен иметь возможность:
- прочитать bootstrap;
- понять текущее состояние структуры;
- запустить следующий цикл без ручного восстановления контекста.

## Expected Process Signature

Правильный процесс должен оставить следы следующих фаз:

1. intake;
2. product interpretation;
3. engineering decomposition;
4. execution planning;
5. integration;
6. benchmark/audit;
7. learning feedback.

Минимально ожидаемые process markers:
- один product brief;
- одна engineering spec;
- один task graph;
- один work order;
- один handoff trace;
- один integration trace;
- один state bootstrap trace;
- один benchmark result;
- одна learning запись.

## Failure Signature

Признаками failure считаются:
- runtime заполнил только структуру папок без рабочего содержания;
- отсутствуют execution и evaluation артефакты;
- отсутствуют state-артефакты;
- отсутствует learning trace;
- обязательные handoff не отражены вообще никак;
- нет runtime-specific адаптера;
- структура не готова к следующему автономному запуску.
