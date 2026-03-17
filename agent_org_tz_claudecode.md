# Agent Organization Infrastructure: Claude Code Runtime Addendum

> Версия файла: `v2.1`
> Дата версии: `2026-03-16`
> Тип документа: `runtime-specific addendum`
> Основание:
> - [agent_org_tz_core.md](./agent_org_tz_core.md)
> - [cc_managment.md](./cc_managment.md)
> - [claudecode_process_1.md](./claudecode_process_1.md)
> - [claudecode-precess_2.md](./claudecode-precess_2.md)
>

## Аннотация

Этот документ не дублирует общее ТЗ.

Он является **runtime-addendum** к [agent_org_tz_core.md](./agent_org_tz_core.md) и отвечает только на один вопрос:

**как именно `Claude Code` должен реализовывать общее ядро инфраструктуры внутри своей изолированной execution-sandbox.**

## 1. Нормативный статус

Главным документом является [agent_org_tz_core.md](./agent_org_tz_core.md).

Этот addendum:
- не меняет инвариантные требования;
- не переписывает состав целевых артефактов;
- не меняет canonical golden task;
- не меняет comparison criteria.

Он описывает только Claude Code-specific способ исполнения.

## 2. Scope записи

`Claude Code` имеет право писать только в пределах:

- `runtimes/claudecode/workspace/`
- `runtimes/claudecode/runs/`
- `runtimes/claudecode/evaluation/`

`Claude Code` не должен:
- изменять `runtimes/codex/`;
- менять `comparison/` до отдельного сравнения;
- переписывать `core/`, если это не специально эскалированное изменение source of truth.

## 3. Целевой результат для Claude Code

Внутри `runtimes/claudecode/workspace/` должна быть создана полная целевая организационная инфраструктура:

```text
runtimes/claudecode/workspace/agent_org/
```

А вокруг неё должны появиться Claude Code-specific runtime-файлы.

## 4. Обязательные Claude Code runtime-артефакты

В `runtimes/claudecode/workspace/` должны быть созданы:

1. `CLAUDE.md`
2. `.claude/settings.json`
3. `.claude/agents/`
4. `.claude/skills/`
5. `.claude/rules/`
6. `.claude/hooks/` при необходимости

При необходимости могут быть добавлены дополнительные runtime-файлы, но только если они:
- реально помогают orchestration;
- не размывают структуру;
- не дублируют бессмысленно другие артефакты.

Также `Claude Code` должен создать и поддерживать локальный state layer для долгоживущей работы:
- `agent_org/state/README.md`
- `agent_org/state/state_registry.md`
- `agent_org/state/storage_strategy.md`
- `agent_org/state/sqlite_schema.sql`
- `agent_org/state/supabase_migration_path.md`

## 5. Требования к `CLAUDE.md`

`CLAUDE.md` должен:
- объяснять, что workspace содержит организационную инфраструктуру, а не обычный software project;
- направлять `Claude Code` к bootstrap-файлам;
- фиксировать минимальный write scope;
- запрещать хаотическое расширение структуры;
- указывать на runtime-specific зоны: `runs/`, `evaluation/`, `workspace/agent_org/`.

## 6. Требования к `.claude/settings.json`

Конфиг должен:
- задавать controlled autonomy;
- не включать unnecessarily dangerous defaults;
- поддерживать работу в пределах workspace;
- задавать безопасные permissions;
- не ломать benchmark и evaluation trace.

Конфиг не должен мешать локальному SQLite-first state layer внутри sandbox.

Приоритет должен быть у:
- воспроизводимости;
- изоляции;
- auditability.

## 7. Требования к `.claude/agents/`

Нужно создать минимум такие subagents:
- `org-bootstrap`
- `product-lead`
- `engineering-manager`
- `integration-reviewer`
- `benchmark-auditor`
- `learning-coordinator`

Для каждого должны быть заданы:
- role summary;
- scope boundaries;
- required inputs;
- expected outputs;
- escalation rules;
- prohibition on uncontrolled structure drift.

## 8. Требования к `.claude/skills/`

Нужно создать минимум такие skills:
- `org-intake`
- `brief-to-spec`
- `task-graph-sync`
- `golden-task-audit`
- `change-proposal-review`

Каждый skill должен описывать:
- purpose;
- when to use;
- required inputs;
- expected outputs;
- какие именно артефакты он обновляет.

## 9. Требования к `.claude/rules/` и `.claude/hooks/`

Если используются `rules` и `hooks`, они должны:
- усиливать governance;
- не дублировать бессмысленно содержимое `CLAUDE.md`;
- удерживать границы опасных действий;
- помогать benchmark и learning-контуру оставаться контролируемыми.

## 10. Требования к Claude Code execution trace

В `runtimes/claudecode/runs/` каждый прогон должен оставлять:
- идентификатор прогона;
- краткую цель;
- использованную версию core ТЗ;
- использованную версию addendum;
- список созданных или обновлённых артефактов;
- краткий итог.

## 11. Требования к Claude Code evaluation trace

В `runtimes/claudecode/evaluation/` должны накапливаться:
- benchmark results;
- local process audit;
- local findings;
- local change proposals для Claude Code-реализации.

## 12. Что считается успешной реализацией для Claude Code

Claude Code-реализация успешна, если:
- внутри своей песочницы создана полная целевая структура;
- runtime-файлы оформлены как рабочая среда для этой структуры;
- bootstrap читается ясно;
- roles, artifacts, benchmark и learning-контур связаны между собой;
- state layer присутствует и готов к долговременной работе;
- есть независимый trace прогонов и локальной оценки.

## 13. Формат финального отчёта Claude Code

После выполнения `Claude Code` должен вернуть:

1. список изменённых файлов в `runtimes/claudecode/`;
2. краткое объяснение runtime-решений;
3. список допущений;
4. список local limitations;
5. где лежит bootstrap;
6. где лежит canonical golden task;
7. где лежат результаты локальной оценки.
