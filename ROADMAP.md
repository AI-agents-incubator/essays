# Roadmap

> Версия файла: `v1.1`
> Дата версии: `2026-03-18`
> Тип документа: `project roadmap`

## Роль этого репозитория

Этот репозиторий является **reference baseline**.

То есть здесь должны жить:

- методология;
- инвариантное ядро требований;
- benchmark-спецификации;
- expected results;
- launch packages;
- базовые comparison templates.

Здесь **не должен** вестись живой длительный runtime-эксперимент, если для него уже создана отдельная рабочая среда.

## Что считается завершённым в baseline

### GT-001

Статус: `completed`

Что зафиксировано:

- bootstrap baseline;
- первые launch packets;
- первый scorecard;
- execution-plane reconciliation lessons.

### GT-002

Статус: `specified and packaged`

Что зафиксировано:

- benchmark;
- expected result;
- launch packets;
- execution package.

### GT-003

Статус: `specified and packaged`

Что зафиксировано:

- benchmark;
- expected result;
- launch packets;
- evaluation templates;
- comparison template.

## Следующая лестница benchmark-ов

Ниже перечислены **следующие уровни зрелости**, которые должны проверяться уже в отдельных execution-средах, а не обязательно внутри этого baseline-репозитория.

### GT-003

`Autonomous closeout recovery`

Проверяет:

- полностью автономный recovery path;
- closeout без observer-assisted правки runtime truth files;
- runtime-owned repair evidence.

### GT-004

`No mid-wave operator tuning`

Проверяет:

- frozen operational contracts;
- достаточность заранее заданных правил;
- отсутствие ручной подстройки в середине wave.

### GT-005

`Graceful failure escalation`

Проверяет:

- bounded retry discipline;
- честный escalation path;
- отсутствие бесконечного redispatch как “нормальной работы”.

### GT-006

`Retry budget exhaustion closeout`

Проверяет:

- retry counter per directive;
- retry budget enforcement;
- terminal `human_review_required` / `wave_failed`;
- partial-success preservation у peer-runtime.

### GT-007

`Runtime-authored failure package`

Проверяет следующий шаг после `GT-006`:

- может ли failed runtime до exhaustion-closeout сам выпустить publishable failure artifacts;
- может ли system-level closeout опираться не только на observer signal, но и на runtime-authored failure package;
- уменьшается ли разрыв между partial-success peer и failed runtime в comparison-ready материале.

## Что уже перенесено обратно в baseline

Из execution-экспериментов обратно в baseline уже возвращены следующие переносимые инварианты:

- `retry_budget`
- `retry_budget_exhausted`
- `human_review_required`
- `wave_failed`
- `partial_success`
- запрет бесконечного redispatch как "нормальной автономной работы"

## Что делать дальше

Для этого baseline-репозитория следующий практический шаг такой:

1. держать здесь в порядке спецификации и roadmap;
2. переносить сюда только инварианты, которые уже доказаны в отдельных execution-средах;
3. не смешивать baseline и живые прогоны в одном рабочем контуре.

## Что ещё переносить обратно в baseline

Смысл baseline не в том, чтобы копировать сюда весь runtime-output.

Сюда стоит переносить только:

- новые benchmark definitions;
- новые expected result signatures;
- новые comparison templates;
- методологические выводы, которые доказали переносимость;
- новые core-инварианты, которые ещё не были закреплены в baseline.

Если изменение остаётся runtime-specific, оно должно оставаться в отдельной execution-среде.
