# GT-004: No Mid-Wave Operator Tuning Under Frozen Operational Contracts

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `canonical golden task`
> Основание:
> - [golden_task_template.md](./golden_task_template.md)
> - [../../agent_org_tz_core.md](../../agent_org_tz_core.md)
> - [GT-003-autonomous-closeout-recovery.md](./GT-003-autonomous-closeout-recovery.md)
> - [../../control_plane/observer_runtime_protocol.md](../../control_plane/observer_runtime_protocol.md)
> - [../../execution_plane/README.md](../../execution_plane/README.md)
>

## Идентификатор задачи

`GT-004`

## Название

`No Mid-Wave Operator Tuning Under Frozen Operational Contracts`

## Цель

Проверить, способна ли система пройти benchmark wave на заранее зафиксированных operational contracts, без ручной подстройки правил, prompts, entrypoints и protocol semantics в середине волны.

Если `GT-003` проверял, может ли closeout recovery происходить автономно, то `GT-004` проверяет следующий переход:

**достаточны ли заранее заданные правила и контракты для целой wave, или система держится только за счёт mid-wave operator tuning.**

## Контекст

Этот benchmark возникает из типичной деградации агентных систем:

- до запуска всё выглядит формально правильно;
- но при первом же напряжении оператор начинает руками подправлять prompts, entrypoints, monitor semantics или правила closeout;
- система вроде бы продолжает двигаться, но фактически benchmark уже перестаёт проверять саму архитектуру и начинает проверять изобретательность человека.

`GT-004` специально запрещает этот паттерн.

## Вход

Входящий внешний сигнал:

> Проведи benchmark wave на полностью замороженных operational contracts. Не меняй правила, prompts и entrypoints в середине волны. Система должна либо дойти до корректного terminal outcome, либо честно показать failure-bearing terminal state на тех правилах, которые были заданы до старта.

Runtime и observer получают в качестве доступных данных:

- [../../agent_org_tz_core.md](../../agent_org_tz_core.md)
- [GT-003-autonomous-closeout-recovery.md](./GT-003-autonomous-closeout-recovery.md)
- [../expected_results/GT-004-expected_result.md](../expected_results/GT-004-expected_result.md)
- [../../control_plane/observer_runtime_protocol.md](../../control_plane/observer_runtime_protocol.md)
- [../../execution_plane/README.md](../../execution_plane/README.md)
- runtime-specific addendum:
  - [../../agent_org_tz_codex.md](../../agent_org_tz_codex.md)
  - [../../agent_org_tz_claudecode.md](../../agent_org_tz_claudecode.md)

## Ограничения

После открытия wave запрещено вручную менять:

- entrypoint files;
- operator prompts;
- runtime baseline contracts;
- control-plane semantics;
- benchmark definition;
- expected result definition.

Допустимы только:

- observer directives внутри уже существующего протокола;
- runtime-authored артефакты внутри своей sandbox;
- bounded failure handling, если он уже предусмотрен baseline-контрактами.

## Что именно проверяется

### 1. Frozen contract discipline

Должно быть видно, что operational contract был зафиксирован до старта wave и не менялся по ходу выполнения.

### 2. Sufficiency of upfront rules

Проверяется, хватает ли заранее заданных:

- observer rules;
- execution-plane behavior;
- runtime instructions;
- failure-governance semantics.

### 3. Honest terminal outcome under frozen rules

Хорошим считается не только terminal success.

Хорошим считается любой честный terminal outcome, если он достигнут без mid-wave tuning:

- `terminal_complete`
- `partial_success`
- `human_review_required`
- `wave_failed`

### 4. Absence of hidden operator rescue

Система не должна проходить benchmark через незадокументированные ручные правки управляющих артефактов в середине wave.

### 5. Human-facing truth

Human monitor должен честно отражать ситуацию под frozen contracts:

- активный прогресс;
- bounded repair;
- terminal success;
- terminal failure.

## Expected Result

После успешного прогона должны существовать:

1. evidence того, что operational contracts были frozen на старте;
2. trace wave, которая шла без mid-wave tuning;
3. terminal outcome, достигнутый на исходных правилах;
4. learning signal о достаточности или недостаточности upfront contracts.

Подробная expected signature зафиксирована в:

[../expected_results/GT-004-expected_result.md](../expected_results/GT-004-expected_result.md)

## Expected Process

### Обязательные участники

1. `observer`
2. `execution-plane`
3. `codex-runtime`
4. `claudecode-runtime`
5. `human-monitor-layer`

### Обязательные артефакты процесса

Минимально должны появиться:

- один frozen-contract declaration artifact;
- один wave trace без contract mutation;
- один terminal outcome package;
- минимум одна learning-запись о достаточности frozen contracts.

### Обязательные проверки

Должны быть явно проверены:

1. не менялись ли управляющие контракты после старта;
2. был ли terminal outcome достигнут без mid-wave operator tuning;
3. если возник failure, был ли он оформлен честно в рамках имеющихся правил;
4. не подменялся ли benchmark ручными спасательными правками.

## Допустимые отклонения

Допускается:

- различие в деталях локальных runtime artifacts;
- различие в глубине learning trace;
- различие в конкретном terminal outcome, если он получен честно на frozen contracts.

Не допускается:

- mid-wave изменение operator prompt, entrypoint или protocol semantics;
- скрытая ручная подстройка правил под конкретную проблему;
- narrative о frozen contracts без evidence;
- terminal success, достигнутый за счёт ручного rescue вне baseline-контрактов.

## Критерии провала

Прогон считается неуспешным, если:

- по ходу wave менялись управляющие контракты;
- система требовала mid-wave operator tuning, чтобы двигаться дальше;
- terminal outcome невозможно объяснить исходными правилами;
- human monitor скрывает факт ручного вмешательства;
- frozen-contract discipline не оставляет trace.
