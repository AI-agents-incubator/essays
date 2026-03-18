# RUN-003 GT-003 Evaluation Template

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `локальный evaluation template`
> Основание:
> - [../../../core/benchmarks/GT-003-autonomous-closeout-recovery.md](../../../core/benchmarks/GT-003-autonomous-closeout-recovery.md)
> - [../../../core/expected_results/GT-003-expected_result.md](../../../core/expected_results/GT-003-expected_result.md)
>

## Run Identity

- run id: `RUN-003`
- benchmark: `GT-003`
- runtime: `Codex`
- core version:
- addendum version:

## Статус

- `passed`
- `passed with deviations`
- `failed`

## Diagnosis Audit

Опишите:

- какая closeout inconsistency была обнаружена;
- как она была диагностирована;
- было ли ясно, почему final success ещё невозможен.

## Repair Ownership Audit

Проверьте:

- сделал ли repair сам runtime;
- не было ли observer-side прямой правки локальных truth files;
- есть ли runtime-authored repair evidence.

## Protocol Recovery Audit

Проверьте:

- совпадают ли `observer_directive` и `runtime_ack` после repair;
- есть ли финальный matching `directive_id`;
- был ли human-facing статус честным во время recovery.

## Result Audit

Опишите:

- какие repair artifacts были обновлены;
- какие обязательные evidence отсутствуют;
- что получилось у локального runtime;
- где виден финальный closeout trace.

## Deviations

Опишите:

- какие отклонения от `GT-003` произошли;
- являются ли они допустимыми;
- относятся ли они к core, observer/execution plane или к самому runtime.

## Findings

Опишите сильные и слабые стороны реализации:

- diagnosis quality;
- repair ownership;
- protocol recovery quality;
- final hold reconciliation;
- learning trace quality.

## Next Actions

Укажите:

- что менять перед следующим wave-run;
- что переносить в comparison;
- какие улучшения нужны в observer/execution plane.
