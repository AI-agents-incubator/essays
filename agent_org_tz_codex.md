# Agent Organization Infrastructure: Codex Runtime Addendum

> Версия файла: `v2.0`
> Дата версии: `2026-03-16`
> Тип документа: `runtime-specific addendum`
> Основание:
> - [agent_org_tz_core.md](./agent_org_tz_core.md)
> - [codex_managment.md](./codex_managment.md)
> - [codex_process_1.md](./codex_process_1.md)
>

## Аннотация

Этот документ не дублирует общее ТЗ.

Он является **runtime-addendum** к [agent_org_tz_core.md](./agent_org_tz_core.md) и отвечает только на один вопрос:

**как именно `Codex` должен реализовывать общее ядро инфраструктуры внутри своей изолированной execution-sandbox.**

## 1. Нормативный статус

Главным документом является [agent_org_tz_core.md](./agent_org_tz_core.md).

Этот addendum:
- не меняет инвариантные требования;
- не переписывает состав целевых артефактов;
- не меняет canonical golden task;
- не меняет comparison criteria.

Он описывает только Codex-specific способ исполнения.

## 2. Scope записи

`Codex` имеет право писать только в пределах:

- `runtimes/codex/workspace/`
- `runtimes/codex/runs/`
- `runtimes/codex/evaluation/`

`Codex` не должен:
- изменять `runtimes/claudecode/`;
- менять `comparison/` до отдельного сравнения;
- переписывать `core/`, если это не специально эскалированное изменение source of truth.

## 3. Целевой результат для Codex

Внутри `runtimes/codex/workspace/` должна быть создана полная целевая организационная инфраструктура:

```text
runtimes/codex/workspace/agent_org/
```

А вокруг неё должны появиться Codex-specific runtime-файлы.

## 4. Обязательные Codex runtime-артефакты

В `runtimes/codex/workspace/` должны быть созданы:

1. `AGENTS.md`
2. `.codex/config.toml`
3. `.codex/agents/`
4. `.agents/skills/`

При необходимости могут быть добавлены дополнительные runtime-файлы, но только если они:
- реально помогают orchestration;
- не размывают структуру;
- не дублируют бессмысленно другие артефакты.

## 5. Требования к `AGENTS.md`

`AGENTS.md` должен:
- объяснять, что workspace содержит организационную инфраструктуру, а не обычный software project;
- направлять `Codex` к bootstrap-файлам;
- фиксировать минимальный write scope;
- запрещать хаотическое расширение структуры;
- указывать на runtime-specific зоны: `runs/`, `evaluation/`, `workspace/agent_org/`.

## 6. Требования к `.codex/config.toml`

Конфиг должен:
- задавать controlled autonomy;
- не включать unnecessarily dangerous defaults;
- поддерживать работу в пределах workspace;
- задавать безопасные approvals;
- не ломать benchmark и evaluation trace.

Приоритет должен быть у:
- воспроизводимости;
- изоляции;
- auditability.

## 7. Требования к `.codex/agents/`

Нужно создать минимум такие custom agents:
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

## 8. Требования к `.agents/skills/`

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

## 9. Требования к Codex execution trace

В `runtimes/codex/runs/` каждый прогон должен оставлять:
- идентификатор прогона;
- краткую цель;
- использованную версию core ТЗ;
- использованную версию addendum;
- список созданных или обновлённых артефактов;
- краткий итог.

## 10. Требования к Codex evaluation trace

В `runtimes/codex/evaluation/` должны накапливаться:
- benchmark results;
- local process audit;
- local findings;
- local change proposals для Codex-реализации.

## 11. Что считается успешной реализацией для Codex

Codex-реализация успешна, если:
- внутри своей песочницы создана полная целевая структура;
- runtime-файлы оформлены как рабочая среда для этой структуры;
- bootstrap читается ясно;
- roles, artifacts, benchmark и learning-контур связаны между собой;
- есть независимый trace прогонов и локальной оценки.

## 12. Формат финального отчёта Codex

После выполнения `Codex` должен вернуть:

1. список изменённых файлов в `runtimes/codex/`;
2. краткое объяснение runtime-решений;
3. список допущений;
4. список local limitations;
5. где лежит bootstrap;
6. где лежит canonical golden task;
7. где лежат результаты локальной оценки.
