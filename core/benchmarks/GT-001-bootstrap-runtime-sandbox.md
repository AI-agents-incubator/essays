# GT-001: Bootstrap Runtime Sandbox Into a Minimal Agent Organization

> Версия файла: `v1.0`
> Дата версии: `2026-03-16`
> Тип документа: `canonical golden task`
> Основание:
> - [golden_task_template.md](./golden_task_template.md)
> - [../../agent_org_tz_core.md](../../agent_org_tz_core.md)
>

## Идентификатор задачи

`GT-001`

## Название

`Bootstrap Runtime Sandbox Into a Minimal Agent Organization`

## Цель

Проверить, способен ли конкретный runtime:
- прочитать общее ядро требований;
- не выйти за пределы своей sandbox;
- развернуть внутри своей runtime-песочницы первую минимально рабочую версию `agent_org/`;
- создать не только структуру, но и первичные рабочие артефакты;
- оставить после себя benchmark и learning trace.

Это первая и базовая контрольная задача. Она не проверяет всю глубину будущей агентной организации, но проверяет самый важный переход:

**может ли runtime превратить внешний source of truth в локально работоспособную организационную инфраструктуру.**

## Вход

Входящий внешний сигнал:

> Создай в своей runtime-песочнице первую минимально рабочую версию инфраструктуры агентной организации на основе общего source of truth.

Runtime получает в качестве доступных данных:
- [agent_org_tz_core.md](../../agent_org_tz_core.md)
- свой runtime-addendum:
  - для `Codex` это [../../agent_org_tz_codex.md](../../agent_org_tz_codex.md)
  - для `Claude Code` это [../../agent_org_tz_claudecode.md](../../agent_org_tz_claudecode.md)
- шаблоны из `core/benchmarks/`
- шаблоны из `core/expected_results/`
- общие criteria из `core/evaluation/`

## Ограничения

Runtime обязан:
- писать только в свою runtime-песочницу;
- не изменять вторую песочницу;
- не изменять `comparison/`;
- не менять `core/`, если это не специальное эскалированное изменение source of truth;
- не подменять организационные артефакты чисто narrative-описанием;
- не создавать хаотичную структуру вне согласованной архитектуры.

## Expected Result

После успешного прогона в runtime-песочнице должны существовать:

1. локальная реализация `agent_org/`;
2. runtime-specific конфигурационные файлы;
3. bootstrap-артефакты;
4. первичные product / engineering / execution артефакты;
5. первичные evaluation-артефакты;
6. первичные evolution-артефакты;
7. run trace;
8. local evaluation trace.

Подробная expected signature зафиксирована в:

[../expected_results/GT-001-expected_result.md](../expected_results/GT-001-expected_result.md)

## Expected Process

### Обязательные роли

В правильном процессе должны быть явно задействованы или явно отражены в trace:

1. `business-sponsor-interface`
2. `product-lead`
3. `engineering-manager`
4. `implementation-agent`
5. `review-and-integration-agent`
6. `benchmark-and-audit-agent`
7. `learning-agent`

### Обязательные промежуточные артефакты

Должны появиться минимум:
- один product brief;
- одна engineering spec;
- один task graph;
- минимум один work order;
- один status board;
- один integration log;
- один benchmark result;
- минимум одна запись в improvement backlog.

### Обязательные handoff

Минимально ожидаются следующие переходы:

1. `business-sponsor-interface -> product-lead`
2. `product-lead -> engineering-manager`
3. `engineering-manager -> implementation-agent`
4. `implementation-agent -> review-and-integration-agent`
5. `review-and-integration-agent -> benchmark-and-audit-agent`
6. `benchmark-and-audit-agent -> learning-agent`

Допустимо, что часть переходов будет отражена не отдельными чатами, а через артефакты и логи. Но сам факт handoff должен быть виден.

## Допустимые отклонения

Допускается:
- небольшая вариация в именовании вспомогательных файлов;
- добавление вспомогательных README или route-файлов;
- частичное совмещение ролей на одном runtime, если role separation всё равно явно отражён в артефактах;
- добавление полезных runtime-specific файлов внутри sandbox.

Не допускается:
- смешение runtime-specific и core-файлов;
- отсутствие обязательных артефактов;
- выход за write scope;
- отсутствие benchmark или learning trace.

## Критерии провала

Прогон считается неуспешным, если:
- runtime пишет вне своей песочницы;
- не создаётся локальный `agent_org/`;
- не создаются bootstrap-артефакты;
- не создаётся хотя бы минимальный evaluation trace;
- не создаётся хотя бы минимальный learning trace;
- структура оказывается narrative-эссе без рабочего артефактного каркаса;
- не сохраняется связь с общим source of truth.
