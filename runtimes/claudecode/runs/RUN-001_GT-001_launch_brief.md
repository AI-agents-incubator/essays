# RUN-001: Claude Code Launch Brief for GT-001

> Версия файла: `v1.0`
> Дата версии: `2026-03-16`
> Тип документа: `execution launch brief`
> Основание:
> - [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
> - [../../../agent_org_tz_claudecode.md](../../../agent_org_tz_claudecode.md)
> - [../../../core/benchmarks/GT-001-bootstrap-runtime-sandbox.md](../../../core/benchmarks/GT-001-bootstrap-runtime-sandbox.md)
> - [../../../core/expected_results/GT-001-expected_result.md](../../../core/expected_results/GT-001-expected_result.md)
> - [../../../core/state/storage_strategy.md](../../../core/state/storage_strategy.md)
>

## Цель прогона

Выполнить `GT-001` для `Claude Code` внутри `runtimes/claudecode/` и развернуть первую минимально рабочую версию `agent_org/` внутри `runtimes/claudecode/workspace/`.

## Порядок чтения перед запуском

Перед началом реализации агент должен прочитать материалы в таком порядке:

1. [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
2. [../../../agent_org_tz_claudecode.md](../../../agent_org_tz_claudecode.md)
3. [../../../core/benchmarks/GT-001-bootstrap-runtime-sandbox.md](../../../core/benchmarks/GT-001-bootstrap-runtime-sandbox.md)
4. [../../../core/expected_results/GT-001-expected_result.md](../../../core/expected_results/GT-001-expected_result.md)
5. [../../../core/state/storage_strategy.md](../../../core/state/storage_strategy.md)
6. [../workspace/README.md](../workspace/README.md)
7. [../evaluation/README.md](../evaluation/README.md)

## Write Scope

Во время этого прогона разрешено писать только в:

- `runtimes/claudecode/workspace/`
- `runtimes/claudecode/runs/`
- `runtimes/claudecode/evaluation/`

Нельзя изменять:
- `core/`
- `comparison/`
- `runtimes/codex/`

## Что именно нужно создать

В рамках RUN-001 `Claude Code` должен:

1. создать внутри `workspace/` локальную реализацию `agent_org/`;
2. создать Claude Code-specific runtime-файлы;
3. создать SQLite-first state layer;
4. создать минимум один product brief, одну engineering spec и один task graph;
5. создать минимум один work order и один handoff trace;
6. создать integration trace;
7. создать локальный benchmark result;
8. создать локальный process audit;
9. создать минимум одну learning-запись о слабом месте или следующем улучшении.

## Что считается хорошим результатом

Хороший результат — это не просто заполненная структура папок.

Хороший результат — это связный первый operational skeleton, который:
- готов к следующему запуску;
- не смешивает уровни;
- не нарушает write scope;
- имеет state layer для долгоживущей работы;
- оставляет trace принятия решений;
- оставляет trace локальной оценки.

## Что считать недопустимым

Недопустимо:
- писать вне своей sandbox;
- создавать только narrative-документ без рабочей структуры;
- пропускать benchmark, learning или state trace;
- игнорировать source of truth;
- произвольно менять core-логику под удобство runtime.

## Формат результата прогона

После завершения RUN-001 должны быть обновлены:

- `runtimes/claudecode/workspace/`
- `runtimes/claudecode/runs/`
- `runtimes/claudecode/evaluation/`

И отдельно должен существовать краткий run summary с:
- перечислением созданных файлов;
- кратким объяснением архитектурных решений;
- перечислением ограничений;
- указанием, где лежит bootstrap;
- указанием, где лежит benchmark trace.
