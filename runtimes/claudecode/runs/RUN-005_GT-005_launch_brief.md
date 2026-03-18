# RUN-005: Claude Code Launch Brief for GT-005

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `execution launch brief`
> Основание:
> - [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
> - [../../../agent_org_tz_claudecode.md](../../../agent_org_tz_claudecode.md)
> - [../../../core/benchmarks/GT-005-graceful-failure-escalation.md](../../../core/benchmarks/GT-005-graceful-failure-escalation.md)
> - [../../../core/expected_results/GT-005-expected_result.md](../../../core/expected_results/GT-005-expected_result.md)
>

## Цель прогона

Выполнить `GT-005` для `Claude Code` внутри `runtimes/claudecode/` так, чтобы при stress-сценарии система использовала bounded retry, а затем честно эскалировала, если локального repair path недостаточно.

## Порядок чтения перед запуском

Перед началом реализации агент должен прочитать материалы в таком порядке:

1. [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
2. [../../../agent_org_tz_claudecode.md](../../../agent_org_tz_claudecode.md)
3. [../../../core/benchmarks/GT-005-graceful-failure-escalation.md](../../../core/benchmarks/GT-005-graceful-failure-escalation.md)
4. [../../../core/expected_results/GT-005-expected_result.md](../../../core/expected_results/GT-005-expected_result.md)
5. [../workspace/README.md](../workspace/README.md)
6. [../control/README.md](../control/README.md)
7. [../evaluation/README.md](../evaluation/README.md)

## Write Scope

Во время этого прогона разрешено писать только в:

- `runtimes/claudecode/workspace/`
- `runtimes/claudecode/control/`
- `runtimes/claudecode/runs/`
- `runtimes/claudecode/evaluation/`

Нельзя изменять:

- `core/`
- `comparison/`
- `runtimes/codex/`
- центральный `control_plane/`

## Что именно нужно сделать

В рамках `RUN-005 / GT-005` `Claude Code` должен:

1. участвовать в bounded retry path, если возникает stress-сценарий;
2. не превращать repeated retry в бесконечный redispatch;
3. оставить trace того, почему escalation стала необходимой;
4. честно оформить terminal failure-bearing outcome, если локального repair path недостаточно;
5. не стирать peer-runtime success, если он уже был;
6. обновить evaluation и learning artifacts так, чтобы было видно:
   - сколько было попыток;
   - когда repair path стал недостаточен;
   - как оформлен escalation path.

## Что считается хорошим результатом

Хороший результат — это не обязательно локальный success.

Хороший результат — это bounded retry plus honest escalation, после которого system-level truth остаётся понятной и не теряет peer progress.

## Что считать недопустимым

Недопустимо:

- бесконечно relaunch/retry без terminal решения;
- скрывать escalation за narrative об "активной работе";
- терять successful artifacts другой ветки;
- писать вне своей runtime-sandbox.

## Формат результата прогона

После завершения `RUN-005` должны быть обновлены:

- `runtimes/claudecode/control/`
- `runtimes/claudecode/workspace/`
- `runtimes/claudecode/runs/`
- `runtimes/claudecode/evaluation/`

И отдельно должен существовать run summary с:

- описанием bounded retry path;
- описанием escalation decision;
- указанием terminal outcome;
- указанием, где лежит evidence peer-progress preservation.
