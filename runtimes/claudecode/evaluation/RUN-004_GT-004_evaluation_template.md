# RUN-004 GT-004 Evaluation Template

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `локальный evaluation template`
> Основание:
> - [../../../core/benchmarks/GT-004-no-mid-wave-operator-tuning.md](../../../core/benchmarks/GT-004-no-mid-wave-operator-tuning.md)
> - [../../../core/expected_results/GT-004-expected_result.md](../../../core/expected_results/GT-004-expected_result.md)
>

## Run Identity

- run id: `RUN-004`
- benchmark: `GT-004`
- runtime: `Claude Code`
- core version:
- addendum version:

## Статус

- `passed`
- `passed with deviations`
- `failed`

## Frozen Contract Audit

Опишите:

- какие contracts считались замороженными;
- были ли попытки их менять;
- есть ли evidence, что mid-wave tuning не происходил.

## Result Audit

Опишите:

- какой terminal outcome получен;
- достигнут ли он в рамках исходных правил;
- потребовались ли bounded repair steps;
- где лежит итоговый closeout trace.

## Operator Tuning Audit

Проверьте:

- не было ли mid-wave изменения entrypoint, prompt или protocol semantics;
- не был ли benchmark фактически спасён ручной подстройкой;
- не противоречат ли raw artifacts frozen-contract claim.

## Deviations

Опишите:

- какие отклонения от `GT-004` произошли;
- являются ли они допустимыми;
- относятся ли они к core, observer/execution plane или к самому runtime.

## Findings

Опишите сильные и слабые стороны реализации:

- frozen-contract discipline;
- adequacy of upfront rules;
- honesty of terminal outcome;
- quality of learning trace.

## Next Actions

Укажите:

- что менять перед следующим wave-run;
- что переносить в comparison;
- какие правила надо усиливать уже после wave.
