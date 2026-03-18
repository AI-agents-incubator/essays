# GT-006: Retry Budget Exhaustion Closeout With Human Review or Wave Failure

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `canonical golden task`
> Основание:
> - [golden_task_template.md](./golden_task_template.md)
> - [../../agent_org_tz_core.md](../../agent_org_tz_core.md)
> - [GT-005-graceful-failure-escalation.md](./GT-005-graceful-failure-escalation.md)
> - [../../control_plane/observer_runtime_protocol.md](../../control_plane/observer_runtime_protocol.md)
> - [../../execution_plane/README.md](../../execution_plane/README.md)
>

## Идентификатор задачи

`GT-006`

## Название

`Retry Budget Exhaustion Closeout With Human Review or Wave Failure`

## Цель

Проверить, способна ли система после исчерпания retry budget не оставаться в бесконечном repair-cycle и не висеть в ambiguous escalation, а честно закрывать wave через `human_review_required` или `wave_failed`.

Если `GT-005` проверял, умеет ли система вообще дойти до graceful escalation, то `GT-006` проверяет следующий переход:

**умеет ли система завершать escalation не разговором, а строгим terminal closeout после exhaustion.**

## Контекст

На практике многие агентные системы умеют:

- замечать сбой;
- ограниченно повторять запуск;
- даже признавать, что нужен человек.

Но часто они всё равно зависают в промежуточном состоянии:

- escalation уже как будто случилась;
- retry path как будто уже исчерпан;
- но wave формально остаётся "в работе";
- monitor, observer и runtime truth files перестают совпадать.

`GT-006` специально закрывает именно этот разрыв.

## Вход

Входящий внешний сигнал:

> Проведи wave, в которой retry budget исчерпывается. После exhaustion система обязана запретить дальнейший автоматический redispatch и оформить terminal closeout как `human_review_required` или `wave_failed`, сохранив при этом already-earned peer progress.

Runtime и observer получают в качестве доступных данных:

- [../../agent_org_tz_core.md](../../agent_org_tz_core.md)
- [GT-005-graceful-failure-escalation.md](./GT-005-graceful-failure-escalation.md)
- [../expected_results/GT-006-expected_result.md](../expected_results/GT-006-expected_result.md)
- [../../control_plane/observer_runtime_protocol.md](../../control_plane/observer_runtime_protocol.md)
- [../../execution_plane/README.md](../../execution_plane/README.md)
- runtime-specific addendum:
  - [../../agent_org_tz_codex.md](../../agent_org_tz_codex.md)
  - [../../agent_org_tz_claudecode.md](../../agent_org_tz_claudecode.md)

## Ограничения

Система обязана:

- считать retry budget finite;
- явно фиксировать момент exhaustion;
- запрещать новый automatic redispatch после exhaustion;
- переходить в `human_review_required` или `wave_failed`;
- сохранять `partial_success`, если peer-runtime завершил свою часть wave;
- оставлять closeout package, пригодный для comparison и learning.

Не допускается:

- новый автоматический retry после `retry_budget_exhausted`;
- ambiguous state "как будто failed, но всё ещё active";
- стирание peer-runtime success;
- terminal success без raw closeout evidence.

## Что именно проверяется

### 1. Retry budget accounting

Должно быть видно:

- какой `directive_id` исчерпал budget;
- сколько попыток было разрешено;
- на какой попытке наступило exhaustion.

### 2. Exhaustion recognition

Система должна явно фиксировать состояние:

- `retry_budget_exhausted`

как отдельный факт, а не как неявную догадку из логов.

### 3. Exhaustion closeout

После exhaustion должен происходить один из двух terminal transitions:

- `human_review_required`
- `wave_failed`

### 4. Preservation of peer success

Если peer-runtime уже завершил свою ветку, его результат должен остаться в system-level truth как `partial_success`.

### 5. Human-facing truth

Human monitor должен:

- показывать exhaustion как отдельный рубеж;
- показывать, что дальнейший automatic retry запрещён;
- честно показывать terminal failure-bearing outcome;
- объяснять, почему wave уже не active.

## Expected Result

После успешного прогона должны существовать:

1. retry budget trace;
2. exhaustion evidence;
3. terminal closeout package;
4. preserved peer-progress evidence;
5. learning signal о качестве exhaustion closeout.

Подробная expected signature зафиксирована в:

[../expected_results/GT-006-expected_result.md](../expected_results/GT-006-expected_result.md)

## Expected Process

### Обязательные участники

1. `observer`
2. `execution-plane`
3. `runtime-exhausting-budget`
4. `peer-runtime`
5. `human-monitor-layer`

### Обязательные артефакты процесса

Минимально должны появиться:

- один retry budget trace;
- один exhaustion artifact;
- один terminal closeout artifact;
- один system-level terminal explanation;
- минимум одна learning-запись о качестве exhaustion closeout.

### Обязательные проверки

Должны быть явно проверены:

1. остановился ли automatic redispatch после exhaustion;
2. переведена ли wave в честный terminal state;
3. сохранился ли peer-runtime success;
4. не осталась ли система в ambiguous active state;
5. пригоден ли closeout package для comparison.

## Допустимые отклонения

Допускается:

- различие в деталях exhaustion trace;
- различие в выборе между `human_review_required` и `wave_failed`, если оно честно обосновано;
- различие в глубине learning trace.

Не допускается:

- repeated relaunch после exhaustion;
- "мягкая" деградация без terminal closeout;
- потеря peer success;
- ложный healthy status в monitor после exhaustion.

## Критерии провала

Прогон считается неуспешным, если:

- retry budget нельзя восстановить по артефактам;
- exhaustion не оформлен как явное состояние;
- automatic redispatch продолжается после exhaustion;
- system-level terminal outcome не оформлен;
- peer-runtime progress потерян;
- monitor врёт о состоянии wave после exhaustion.
