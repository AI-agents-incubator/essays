# RUN-001: Codex Launch Brief for GT-001

> Версия файла: `v1.0`
> Дата версии: `2026-03-16`
> Тип документа: `execution launch brief`
> Основание:
> - [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
> - [../../../agent_org_tz_codex.md](../../../agent_org_tz_codex.md)
> - [../../../core/benchmarks/GT-001-bootstrap-runtime-sandbox.md](../../../core/benchmarks/GT-001-bootstrap-runtime-sandbox.md)
> - [../../../core/expected_results/GT-001-expected_result.md](../../../core/expected_results/GT-001-expected_result.md)
>

## Цель прогона

Выполнить `GT-001` для `Codex` внутри `runtimes/codex/` и развернуть первую минимально рабочую версию `agent_org/` внутри `runtimes/codex/workspace/`.

## Порядок чтения перед запуском

Перед началом реализации агент должен прочитать материалы в таком порядке:

1. [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
2. [../../../agent_org_tz_codex.md](../../../agent_org_tz_codex.md)
3. [../../../core/benchmarks/GT-001-bootstrap-runtime-sandbox.md](../../../core/benchmarks/GT-001-bootstrap-runtime-sandbox.md)
4. [../../../core/expected_results/GT-001-expected_result.md](../../../core/expected_results/GT-001-expected_result.md)
5. [../workspace/README.md](../workspace/README.md)
6. [../evaluation/README.md](../evaluation/README.md)

## Write Scope

Во время этого прогона разрешено писать только в:

- `runtimes/codex/workspace/`
- `runtimes/codex/runs/`
- `runtimes/codex/evaluation/`

Нельзя изменять:
- `core/`
- `comparison/`
- `runtimes/claudecode/`

## Что именно нужно создать

В рамках RUN-001 `Codex` должен:

1. создать внутри `workspace/` локальную реализацию `agent_org/`;
2. создать Codex-specific runtime-файлы;
3. создать минимум один product brief, одну engineering spec и один task graph;
4. создать минимум один work order и один handoff trace;
5. создать integration trace;
6. создать локальный benchmark result;
7. создать локальный process audit;
8. создать минимум одну learning-запись о слабом месте или следующем улучшении.

## Что считается хорошим результатом

Хороший результат — это не просто заполненная структура папок.

Хороший результат — это связный первый operational skeleton, который:
- готов к следующему запуску;
- не смешивает уровни;
- не нарушает write scope;
- оставляет trace принятия решений;
- оставляет trace локальной оценки.

## Что считать недопустимым

Недопустимо:
- писать вне своей sandbox;
- создавать только narrative-документ без рабочей структуры;
- пропускать benchmark и learning trace;
- игнорировать source of truth;
- произвольно менять core-логику под удобство runtime.

## Формат результата прогона

После завершения RUN-001 должны быть обновлены:

- `runtimes/codex/workspace/`
- `runtimes/codex/runs/`
- `runtimes/codex/evaluation/`

И отдельно должен существовать краткий run summary с:
- перечислением созданных файлов;
- кратким объяснением архитектурных решений;
- перечислением ограничений;
- указанием, где лежит bootstrap;
- указанием, где лежит benchmark trace.
