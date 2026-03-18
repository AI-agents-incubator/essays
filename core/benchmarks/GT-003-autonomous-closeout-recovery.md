# GT-003: Autonomous Closeout Recovery Without Observer-Side Truth File Edits

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `canonical golden task`
> Основание:
> - [golden_task_template.md](./golden_task_template.md)
> - [../../agent_org_tz_core.md](../../agent_org_tz_core.md)
> - [GT-002-wave-synchronized-orchestration.md](./GT-002-wave-synchronized-orchestration.md)
> - [../../control_plane/observer_runtime_protocol.md](../../control_plane/observer_runtime_protocol.md)
> - [../../execution_plane/README.md](../../execution_plane/README.md)
>

## Идентификатор задачи

`GT-003`

## Название

`Autonomous Closeout Recovery Without Observer-Side Truth File Edits`

## Цель

Проверить, способна ли система самостоятельно восстановить корректный terminal closeout после protocol drift или stale closeout state, не прибегая к observer-side переписыванию runtime-local truth files.

Если `GT-002` проверял shared wave, stage barriers и честный monitor, то `GT-003` проверяет следующий переход:

**может ли runtime сам авторствовать recovery-артефакты и довести closeout до консистентного финала, а не быть "дочинен" наблюдателем прямой правкой truth files.**

## Контекст

Этот benchmark рождается из следующего class of failure:

- wave в целом уже близка к завершению;
- observer понимает, что closeout должен состояться;
- но `RUNTIME_STATUS.md`, `RUNTIME_ACK.md`, local state или derived monitor truth ещё не схлопнулись корректно;
- возникает соблазн у observer или человека "поправить файлы руками", чтобы быстро получить красивый terminal state.

`GT-003` специально запрещает такую подмену.

Он требует, чтобы repair path был:

- runtime-authored;
- traceable;
- bounded;
- пригодным для последующего comparison и learning.

## Вход

Входящий внешний сигнал:

> Восстанови корректный terminal closeout после stale или protocol-drift состояния так, чтобы итоговая консистентность была достигнута без observer-side правки runtime-local truth files.

Runtime и observer получают в качестве доступных данных:

- [../../agent_org_tz_core.md](../../agent_org_tz_core.md)
- [GT-002-wave-synchronized-orchestration.md](./GT-002-wave-synchronized-orchestration.md)
- [../expected_results/GT-003-expected_result.md](../expected_results/GT-003-expected_result.md)
- [../../control_plane/observer_runtime_protocol.md](../../control_plane/observer_runtime_protocol.md)
- [../../execution_plane/README.md](../../execution_plane/README.md)
- runtime-specific addendum:
  - [../../agent_org_tz_codex.md](../../agent_org_tz_codex.md)
  - [../../agent_org_tz_claudecode.md](../../agent_org_tz_claudecode.md)

## Ограничения

Система обязана:

- не считать observer-side ручную правку runtime-local truth files допустимым repair path;
- различать `diagnosis`, `repair directive`, `runtime-authored repair`, `revalidation`, `final closeout`;
- сохранять физическую изоляцию двух runtime-песочниц;
- оставлять repair evidence как publishable artifact, а не только narrative summary;
- показывать в human monitor, что идёт repair/closeout recovery, пока финальная консистентность не достигнута;
- не объявлять `terminal_complete`, пока не схлопнуты `directive`, `ack`, status и derived monitor truth.

## Что именно проверяется

### 1. Runtime-owned repair path

Должно быть видно, что repair выполняет сам runtime в своей sandbox, а не observer прямой правкой локальных truth files.

Минимально должна быть evidence цепочка:

1. observer обнаружил closeout inconsistency;
2. observer выписал repair-oriented directive;
3. runtime сам обновил локальные truth artifacts;
4. после этого произошла revalidation и финальный hold.

### 2. Autonomous closeout recovery

Система должна пройти фазы:

1. `closeout_inconsistency_detected`
2. `repair_directive_issued`
3. `runtime_authored_repair`
4. `closeout_revalidation`
5. `terminal_hold_reconciliation`
6. `autonomous_closeout_complete`

### 3. Human-facing truth during repair

Human monitor не должен скрывать сам факт repair-phase.

Он должен различать:

- `repair_in_progress`
- `protocol_inconsistent`
- `closeout_revalidation`
- `terminal_complete`

### 4. Publishable repair evidence

После benchmark должны существовать не только итоговые truth files, но и отдельные repair artifacts:

- diagnosis trace;
- runtime-authored repair trace;
- final revalidation trace;
- итоговый closeout package.

## Expected Result

После успешного прогона должны существовать:

1. evidence исходного closeout inconsistency;
2. одна observer directive, которая не подменяет runtime-local repair собой;
3. runtime-authored repair evidence;
4. one-step or bounded closeout revalidation;
5. финальный terminal hold с matching ack;
6. human-facing monitor, который честно показывает recovery path.

Подробная expected signature зафиксирована в:

[../expected_results/GT-003-expected_result.md](../expected_results/GT-003-expected_result.md)

## Expected Process

### Обязательные участники

В правильном процессе должны быть явно задействованы:

1. `observer`
2. `execution-plane`
3. `runtime-under-repair`
4. `human-monitor-layer`
5. при необходимости `peer-runtime` как источник wave context

### Обязательные артефакты процесса

Минимально должны появиться:

- один diagnosis artifact;
- один repair directive trace;
- один runtime-authored repair artifact;
- один revalidation artifact;
- один final closeout artifact;
- минимум одна learning-запись о качестве recovery path.

### Обязательные проверки

Должны быть явно проверены:

1. repair инициирован observer directive, а не прямой observer-side правкой truth files;
2. локальные runtime truth files обновлены самим runtime;
3. final hold и ack согласованы по одному `directive_id`;
4. human monitor не показывал ложный terminal success до recovery completion;
5. repair path оставил comparison-ready evidence.

## Допустимые отклонения

Допускается:

- вариация в конкретных названиях repair-файлов;
- различие в деталях revalidation step;
- различие в деталях monitor messaging, если truth semantics совпадает;
- различие в глубине repair summary.

Не допускается:

- observer-side переписывание runtime-local truth files как способ "закрыть" benchmark;
- отсутствие runtime-authored repair evidence;
- финальный success без recovery trace;
- отсутствие final hold reconciliation;
- скрытый переход в `terminal_complete` до завершения recovery.

## Критерии провала

Прогон считается неуспешным, если:

- repair фактически делает observer прямой правкой локальных truth files;
- runtime не оставляет собственных recovery artifacts;
- невозможно восстановить, как closeout inconsistency была устранена;
- human monitor показывает успех раньше raw reconciliation;
- closeout восстановлен narrative-описанием, но не артефактами;
- system-level closeout не пригоден для comparison и learning.
