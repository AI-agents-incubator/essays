# RUN-006: Codex Launch Brief for GT-006

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `execution launch brief`
> Основание:
> - [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
> - [../../../agent_org_tz_codex.md](../../../agent_org_tz_codex.md)
> - [../../../core/benchmarks/GT-006-retry-budget-exhaustion-closeout.md](../../../core/benchmarks/GT-006-retry-budget-exhaustion-closeout.md)
> - [../../../core/expected_results/GT-006-expected_result.md](../../../core/expected_results/GT-006-expected_result.md)
>

## Цель прогона

Выполнить `GT-006` для `Codex` внутри `runtimes/codex/` так, чтобы после исчерпания retry budget система честно остановила automatic redispatch и оформила terminal closeout через `human_review_required` или `wave_failed`.

## Порядок чтения перед запуском

Перед началом реализации агент должен прочитать материалы в таком порядке:

1. [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
2. [../../../agent_org_tz_codex.md](../../../agent_org_tz_codex.md)
3. [../../../core/benchmarks/GT-006-retry-budget-exhaustion-closeout.md](../../../core/benchmarks/GT-006-retry-budget-exhaustion-closeout.md)
4. [../../../core/expected_results/GT-006-expected_result.md](../../../core/expected_results/GT-006-expected_result.md)
5. [../workspace/README.md](../workspace/README.md)
6. [../control/README.md](../control/README.md)
7. [../evaluation/README.md](../evaluation/README.md)

## Write Scope

Во время этого прогона разрешено писать только в:

- `runtimes/codex/workspace/`
- `runtimes/codex/control/`
- `runtimes/codex/runs/`
- `runtimes/codex/evaluation/`

Нельзя изменять:

- `core/`
- `comparison/`
- `runtimes/claudecode/`
- центральный `control_plane/`

## Что именно нужно сделать

В рамках `RUN-006 / GT-006` `Codex` должен:

1. пройти bounded retry path до exhaustion;
2. не продолжать automatic redispatch после exhaustion;
3. оставить evidence состояния `retry_budget_exhausted`;
4. участвовать в terminal closeout через `human_review_required` или `wave_failed`;
5. не стирать peer-runtime success, если он уже есть;
6. обновить evaluation и learning artifacts так, чтобы было видно:
   - как учитывался retry budget;
   - на какой попытке budget исчерпался;
   - почему дальше продолжать автоматически уже нельзя.

## Что считается хорошим результатом

Хороший результат — это не обязательно локальный success.

Хороший результат — это строгий exhaustion closeout, который прекращает бесполезный automatic redispatch и оставляет comparison-ready evidence.

## Что считать недопустимым

Недопустимо:

- новый automatic retry после exhaustion;
- ambiguous state между active и failed;
- потеря peer-success;
- отсутствие явного exhaustion trace;
- запись вне своей runtime-sandbox.

## Формат результата прогона

После завершения `RUN-006` должны быть обновлены:

- `runtimes/codex/control/`
- `runtimes/codex/workspace/`
- `runtimes/codex/runs/`
- `runtimes/codex/evaluation/`

И отдельно должен существовать run summary с:

- описанием retry budget;
- указанием exhaustion point;
- описанием terminal closeout;
- указанием, где лежит evidence peer-progress preservation.
