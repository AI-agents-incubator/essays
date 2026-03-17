# RUN-002: Claude Code Launch Brief for GT-002

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `execution launch brief`
> Основание:
> - [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
> - [../../../agent_org_tz_claudecode.md](../../../agent_org_tz_claudecode.md)
> - [../../../core/benchmarks/GT-002-wave-synchronized-orchestration.md](../../../core/benchmarks/GT-002-wave-synchronized-orchestration.md)
> - [../../../core/expected_results/GT-002-expected_result.md](../../../core/expected_results/GT-002-expected_result.md)
>

## Цель прогона

Выполнить `GT-002` для `Claude Code` внутри `runtimes/claudecode/` как часть общей wave, где проверяется:
- shared stage barriers;
- честный переход в `waiting_peers`, если второй runtime ещё не готов;
- корректный final `hold`;
- согласованность human monitor, observer directive и runtime ack.

## Порядок чтения перед запуском

Перед началом реализации агент должен прочитать материалы в таком порядке:

1. [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
2. [../../../agent_org_tz_claudecode.md](../../../agent_org_tz_claudecode.md)
3. [../../../core/benchmarks/GT-002-wave-synchronized-orchestration.md](../../../core/benchmarks/GT-002-wave-synchronized-orchestration.md)
4. [../../../core/expected_results/GT-002-expected_result.md](../../../core/expected_results/GT-002-expected_result.md)
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

В рамках `RUN-002 / GT-002` `Claude Code` должен:

1. пройти свою часть общей wave без выхода за пределы sandbox;
2. корректно обработать observer directives через локальный `control/`;
3. явно отражать wave-stage состояние, а не только локальный completed status;
4. не объявлять локальное завершение всей wave, если peer-runtime ещё активен;
5. оставить trace coordination quality в evaluation и learning artifacts;
6. участвовать в final hold reconciliation без запуска новых engineering runs.

## Что считается хорошим результатом

Хороший результат — это локальный runtime trace, по которому видно:
- какой stage wave проходил `Claude Code`;
- где был барьер ожидания peers;
- как был подтверждён final hold;
- почему monitor может честно вывести итоговое состояние.

## Что считать недопустимым

Недопустимо:
- локально считать wave завершённой без peer-runtime;
- оставлять несхлопнутый final `hold`;
- не обновить `control/` артефакты;
- прятать protocol mismatch за narrative;
- писать вне своей runtime-сandbox.

## Формат результата прогона

После завершения `RUN-002` должны быть обновлены:

- `runtimes/claudecode/control/`
- `runtimes/claudecode/workspace/`
- `runtimes/claudecode/runs/`
- `runtimes/claudecode/evaluation/`

И отдельно должен существовать run summary с:
- описанием локального участия в общей wave;
- перечислением обновлённых coordination artifacts;
- указанием, был ли этап `waiting_peers`;
- указанием, где лежит локальная evaluation trace;
- указанием, где лежит evidence final hold reconciliation.
