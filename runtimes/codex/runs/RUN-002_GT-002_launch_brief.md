# RUN-002: Codex Launch Brief for GT-002

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `execution launch brief`
> Основание:
> - [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
> - [../../../agent_org_tz_codex.md](../../../agent_org_tz_codex.md)
> - [../../../core/benchmarks/GT-002-wave-synchronized-orchestration.md](../../../core/benchmarks/GT-002-wave-synchronized-orchestration.md)
> - [../../../core/expected_results/GT-002-expected_result.md](../../../core/expected_results/GT-002-expected_result.md)
>

## Цель прогона

Выполнить `GT-002` для `Codex` внутри `runtimes/codex/` как часть общей wave, где проверяется не только локальный runtime-прогресс, но и:
- shared stage barriers;
- честное состояние `waiting_peers`;
- финальный `hold` с matching `ACK`;
- согласованность human-facing monitor с raw protocol.

## Порядок чтения перед запуском

Перед началом реализации агент должен прочитать материалы в таком порядке:

1. [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
2. [../../../agent_org_tz_codex.md](../../../agent_org_tz_codex.md)
3. [../../../core/benchmarks/GT-002-wave-synchronized-orchestration.md](../../../core/benchmarks/GT-002-wave-synchronized-orchestration.md)
4. [../../../core/expected_results/GT-002-expected_result.md](../../../core/expected_results/GT-002-expected_result.md)
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

В рамках `RUN-002 / GT-002` `Codex` должен:

1. пройти свою часть общей wave без нарушения sandbox;
2. корректно читать и подтверждать observer directives через локальный `control/`;
3. оставлять честный переход между состояниями:
   - `in_progress`
   - `waiting_peers`, если peer-runtime ещё не закончил свой этап
   - `completed`
4. не инициировать финальный closeout раньше общего wave barrier;
5. оставить trace того, как локальный runtime участвовал в общей stage-синхронизации;
6. обновить evaluation и learning artifacts так, чтобы было видно:
   - что сработало;
   - где был coordination risk;
   - что стоит улучшать в observer/execution layer.

## Что считается хорошим результатом

Хороший результат — это не просто ещё один локальный completed run.

Хороший результат — это локальный вклад в общую wave, после которого можно восстановить:
- на каком барьере находился `Codex`;
- почему система ждала или не ждала peer-runtime;
- почему final hold считается консистентным;
- почему human monitor показывает именно тот статус, который показывает.

## Что считать недопустимым

Недопустимо:
- локально закрыть wave без учёта peer-runtime;
- скрыть raw protocol mismatch narrative-объяснением;
- не обновить `control/` артефакты;
- стартовать следующий run без observer-approved directive;
- писать вне своей runtime-сandbox.

## Формат результата прогона

После завершения `RUN-002` должны быть обновлены:

- `runtimes/codex/control/`
- `runtimes/codex/workspace/`
- `runtimes/codex/runs/`
- `runtimes/codex/evaluation/`

И отдельно должен существовать run summary с:
- описанием локального участия в общей wave;
- перечислением обновлённых coordination artifacts;
- указанием, был ли этап `waiting_peers`;
- указанием, где лежит локальная evaluation trace;
- указанием, где лежит evidence final hold reconciliation.
