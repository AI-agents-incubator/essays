# Project Scaffold Manifest

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `starter manifest`

## Что создаёт starter scaffold

После установки в новом проекте появляется такая структура:

```text
project_input/
  PROJECT_REQUEST.md
  PROJECT_CONSTRAINTS.md
agent_org/
  bootstrap/
    ORG_BOOTSTRAP.md
    STARTUP_SEQUENCE.md
  charter/
    mission.md
    autonomy_model.md
    role_map.md
  policies/
    escalation_policy.md
    quality_gates.md
    artifact_change_policy.md
  intake/
    intake_protocol.md
    intake_log.md
  product/
    active_product_brief.md
  engineering/
    active_engineering_spec.md
    task_graph.md
  execution/
    status_board.md
    work_orders/
  evaluation/
    current_wave.md
  evolution/
    improvement_backlog.md
  knowledge/
    decision_log.md
START_HERE.md
```

## Зачем нужен каждый блок

### `project_input/`

Это человеческий вход в систему.

Здесь пользователь описывает:

- что хочет сделать;
- какие ограничения есть;
- что уже известно;
- что пока неясно.

### `agent_org/bootstrap/`

Это вход для runtime.

Здесь зафиксированы:

- порядок чтения;
- первый цикл действий;
- правило перехода от project request к product and engineering framing.

### `agent_org/charter/`

Здесь лежат постоянные рамки организации:

- миссия;
- модель автономности;
- карта ролей.

### `agent_org/policies/`

Здесь лежат постоянные правила:

- когда эскалировать;
- какие проверки обязательны;
- как менять артефакты.

### `agent_org/intake/`

Здесь входящий запрос превращается в рабочий intake.

### `agent_org/product/`

Здесь появляется продуктовая формулировка задачи.

### `agent_org/engineering/`

Здесь появляется инженерная постановка и task graph.

### `agent_org/execution/`

Здесь фиксируется ход исполнения.

### `agent_org/evaluation/`

Здесь фиксируется текущая wave и её итог.

### `agent_org/evolution/`

Здесь копятся улучшения и lessons learned.

### `agent_org/knowledge/`

Здесь копятся решения и проектная память.

## Главный смысл manifest

Этот scaffold не пытается сразу создать production-уровневую организацию.

Его задача проще:

- дать проекту готовую организационную оболочку;
- убрать необходимость каждый раз заново изобретать стартовую структуру;
- сделать handoff от человека к агентной организации воспроизводимым.
