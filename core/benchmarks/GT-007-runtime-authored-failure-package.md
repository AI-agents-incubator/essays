# GT-007: Runtime-Authored Failure Package Before Terminal Closeout

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `canonical golden task`
> Основание:
> - [golden_task_template.md](./golden_task_template.md)
> - [../../agent_org_tz_core.md](../../agent_org_tz_core.md)
> - [GT-006-retry-budget-exhaustion-closeout.md](./GT-006-retry-budget-exhaustion-closeout.md)
> - [../../control_plane/observer_runtime_protocol.md](../../control_plane/observer_runtime_protocol.md)
> - [../../execution_plane/README.md](../../execution_plane/README.md)
>

## Идентификатор задачи

`GT-007`

## Название

`Runtime-Authored Failure Package Before Terminal Closeout`

## Цель

Проверить, способен ли runtime, который не смог успешно завершить свою часть wave, до окончательного system-level closeout сам выпустить publishable failure package, пригодный для comparison, audit и learning.

Если `GT-006` проверял, умеет ли система честно закрыть wave после `retry_budget_exhausted`, то `GT-007` проверяет следующий переход:

**может ли failed runtime до terminal closeout внести собственный структурированный вклад в итоговую правду о провале, а не быть описанным только observer-side сигналами.**

## Контекст

После exhaustion closeout часто остаётся важный разрыв:

- peer-runtime может иметь красивый success package;
- failed runtime может остаться только с голым `wave_failed` или `human_review_required`;
- comparison и learning тогда опираются преимущественно на observer perspective, а не на runtime-authored failure evidence.

`GT-007` закрывает именно этот разрыв.

## Вход

Входящий внешний сигнал:

> Проведи benchmark wave, в которой одна ветка доходит до failure-bearing terminal state. Перед окончательным closeout failed runtime должен сам выпустить structured failure package: diagnosis, retry history, exhaustion reason, impacted artifacts, limits of local repair path и рекомендации для следующей волны.

Runtime и observer получают в качестве доступных данных:

- [../../agent_org_tz_core.md](../../agent_org_tz_core.md)
- [GT-006-retry-budget-exhaustion-closeout.md](./GT-006-retry-budget-exhaustion-closeout.md)
- [../expected_results/GT-007-expected_result.md](../expected_results/GT-007-expected_result.md)
- [../../control_plane/observer_runtime_protocol.md](../../control_plane/observer_runtime_protocol.md)
- [../../execution_plane/README.md](../../execution_plane/README.md)
- runtime-specific addendum:
  - [../../agent_org_tz_codex.md](../../agent_org_tz_codex.md)
  - [../../agent_org_tz_claudecode.md](../../agent_org_tz_claudecode.md)

## Ограничения

Система обязана:

- не ограничиваться observer-side explanation of failure;
- требовать от failed runtime собственный failure package до окончательного closeout, если runtime ещё способен записывать артефакты;
- сохранять peer-runtime success package независимо;
- делать comparison-ready систему, где успешная и неуспешная ветки обе оставляют publishable материал.

Не допускается:

- failure closeout без runtime-authored failure artifacts, если runtime всё ещё способен их создать;
- system-level narrative, который полностью заменяет локальный failure package;
- утеря retry/exhaustion evidence;
- утеря suggested next actions from failed runtime.

## Что именно проверяется

### 1. Runtime-authored diagnosis

Должно быть видно, что failed runtime сам описал:

- что именно не удалось;
- где локальный repair path закончился;
- какие артефакты были затронуты;
- какие локальные ограничения сделали success невозможным.

### 2. Structured failure package

Минимальный publishable package должен содержать:

- diagnosis;
- retry history;
- exhaustion or escalation reason;
- impacted artifacts;
- suggested next actions;
- explicit statement of terminal outcome.

### 3. System-level reliance on runtime package

Observer и comparison layer должны опираться не только на raw control signals, но и на runtime-authored failure package.

### 4. Asymmetry handling

Система должна уметь жить с асимметрией:

- одна ветка успешна;
- другая неуспешна;
- обе оставляют comparison-ready material.

### 5. Human-facing truth

Human monitor должен показывать, что failure closeout теперь опирается не только на observer truth, но и на runtime-authored failure evidence.

## Expected Result

После успешного прогона должны существовать:

1. runtime-authored failure package;
2. preserved peer-success package;
3. system-level closeout, который явно ссылается на failure package;
4. learning signal о качестве failure package и о том, насколько он уменьшает разрыв между successful и failed ветками.

Подробная expected signature зафиксирована в:

[../expected_results/GT-007-expected_result.md](../expected_results/GT-007-expected_result.md)

## Expected Process

### Обязательные участники

1. `failed-runtime`
2. `peer-runtime`
3. `observer`
4. `execution-plane`
5. `comparison-layer`
6. `human-monitor-layer`

### Обязательные артефакты процесса

Минимально должны появиться:

- один runtime-authored failure package;
- один peer-success package;
- один system-level terminal closeout artifact;
- один comparison-ready bridge artifact, который связывает обе ветки;
- минимум одна learning-запись о качестве failure package.

### Обязательные проверки

Должны быть явно проверены:

1. создал ли failed runtime собственный failure package;
2. использовал ли observer этот package при closeout;
3. сохранился ли peer-success package;
4. уменьшился ли разрыв между successful и failed ветками в comparison-ready материале;
5. не был ли failure package полностью заменён observer narrative.

## Допустимые отклонения

Допускается:

- различие в глубине failure package;
- различие в деталях retry history;
- различие в формулировках suggested next actions;
- различие в глубине bridge artifact между success и failure ветками.

Не допускается:

- полное отсутствие runtime-authored failure package;
- failure closeout только на observer-side explanation;
- потеря peer-success package;
- отсутствие явного terminal statement со стороны failed runtime.

## Критерии провала

Прогон считается неуспешным, если:

- failed runtime не оставил собственного publishable failure package;
- system-level closeout не опирается на runtime-authored failure evidence;
- comparison-ready материал описывает success сторону глубоко, а failure сторону только поверхностно;
- learning layer не получает usable failure package;
- monitor скрывает отсутствие runtime-authored failure evidence.
