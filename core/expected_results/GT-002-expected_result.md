# GT-002 Expected Result

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `expected result signature`
> Основание:
> - [expected_result_template.md](./expected_result_template.md)
> - [../benchmarks/GT-002-wave-synchronized-orchestration.md](../benchmarks/GT-002-wave-synchronized-orchestration.md)
>

## Result Identity

- benchmark: `GT-002`
- expected result version: `v1.0`

## Итоговые свойства результата

После успешного прогона система должна демонстрировать не просто два локальных завершённых runtime, а **одну общую wave с честно согласованным состоянием**.

## Обязательные результатные сигнатуры

### 1. Shared wave coordination

Должно быть возможно восстановить:
- идентификатор общей wave;
- текущую и финальную стадию wave;
- момент, когда один runtime ждал второй;
- момент, когда closeout стал допустим для всей системы;
- момент финального схлопывания протокола.

Минимально ожидаются:
- один wave-level coordination artifact;
- один barrier-state artifact;
- одна observer decision trace по фазам wave.

### 2. Raw protocol consistency

В финальном состоянии у обоих runtime обязано выполняться:
- `observer_directive.action = hold`
- `observer_directive.directive_status = completed`
- `runtime_ack.directive_id = observer_directive.directive_id`
- `runtime_ack.ack_status` принадлежит множеству:
  - `seen`
  - `accepted`
  - `completed`

То есть финальный hold обязан быть не только выписан, но и подтверждён.

### 3. Human-facing monitor consistency

Human monitor обязан:
- показывать `protocol_inconsistent`, если raw protocol не схлопнулся;
- показывать `waiting_peers`, если один runtime локально завершён, а второй ещё нет;
- показывать `terminal_complete` только если wave реально завершена;
- объяснять, почему сейчас именно такой статус;
- быть восстанавливаемым из файлов, а не из памяти интерактивной сессии.

Минимально ожидаются:
- один human heartbeat artifact;
- один явный human-readable status explanation;
- evidence, что monitor derived from raw artifacts, а не от narrative.

### 4. Runtime-local closeout discipline

Оба runtime обязаны оставить после себя:
- локальный `RUNTIME_STATUS.md`;
- matching `RUNTIME_ACK.md`;
- completion or closeout artifact;
- trace того, что runtime не стартовал новый run самовольно после финального hold.

### 5. Learning signal

После `GT-002` должна появиться как минимум одна learning-запись о качестве координации:
- где именно был coordination risk;
- что было улучшено;
- что переносится в core;
- что остаётся runtime-specific.

## Expected Process Signature

Правильный процесс должен оставить evidence следующих фаз:

1. `wave_open`
2. `parallel_runtime_progress`
3. `peer_wait_or_barrier_hold`
4. `closeout_enablement`
5. `final_hold_reconciliation`
6. `wave_complete`

## Failure Signature

Признаками failure считаются:
- human monitor показывает финальное завершение до raw reconciliation;
- один runtime локально завершён, но система не умеет показать `waiting_peers`;
- final hold не подтверждён matching ack;
- невозможно восстановить wave-level переходы;
- monitoring truth зависит от чата, а не от файловых артефактов;
- нет отдельного coordination signal сверх локальных runtime status.
