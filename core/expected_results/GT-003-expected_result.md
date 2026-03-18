# GT-003 Expected Result

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `expected result signature`
> Основание:
> - [expected_result_template.md](./expected_result_template.md)
> - [../benchmarks/GT-003-autonomous-closeout-recovery.md](../benchmarks/GT-003-autonomous-closeout-recovery.md)
>

## Result Identity

- benchmark: `GT-003`
- expected result version: `v1.0`

## Итоговые свойства результата

После успешного прогона система должна демонстрировать не просто финальный `completed`, а **доказуемо восстановленный terminal closeout**, где repair выполнен самим runtime и не был подменён observer-side правкой truth files.

## Обязательные результатные сигнатуры

### 1. Closeout inconsistency diagnosis

Должно быть возможно восстановить:

- что именно было inconsistent в closeout;
- какая observer directive была выписана для repair;
- почему closeout ещё нельзя было считать завершённым на момент diagnosis.

Минимально ожидаются:

- один diagnosis artifact;
- одно human-readable объяснение несогласованности;
- evidence, что terminal success ещё не был допустим.

### 2. Runtime-authored repair

В результате должно быть видно, что локальные truth artifacts были обновлены самим runtime.

Минимально ожидаются:

- один runtime-authored repair artifact;
- один trace того, какие truth files были приведены в консистентность;
- one-step or bounded repair narrative, связанный с raw artifacts.

### 3. Raw protocol consistency after repair

В финальном состоянии у runtime обязано выполняться:

- `observer_directive.action = hold`
- `observer_directive.directive_status = completed`
- `runtime_ack.directive_id = observer_directive.directive_id`
- `runtime_ack.ack_status` принадлежит множеству:
  - `accepted`
  - `completed`
- final `RUNTIME_STATUS.md` не противоречит terminal state.

### 4. Human-facing recovery truth

Human monitor обязан:

- показывать repair-phase до реального завершения;
- различать `protocol_inconsistent`, `repair_in_progress`, `closeout_revalidation` и `terminal_complete`;
- быть восстановимым из файлов, а не из narrative в чате;
- объяснять, почему success допустим именно сейчас.

### 5. Publishable closeout package

После `GT-003` должен существовать comparison-ready package, в который входят:

- diagnosis evidence;
- repair evidence;
- revalidation evidence;
- final closeout evidence;
- learning signal о качестве recovery path.

## Expected Process Signature

Правильный процесс должен оставить evidence следующих фаз:

1. `closeout_inconsistency_detected`
2. `repair_directive_issued`
3. `runtime_authored_repair`
4. `closeout_revalidation`
5. `final_hold_reconciliation`
6. `autonomous_closeout_complete`

## Failure Signature

Признаками failure считаются:

- observer сам переписывает runtime-local truth files;
- нет runtime-authored repair evidence;
- final closeout есть, но не видно recovery path;
- human monitor показывает успех до protocol reconciliation;
- repair не оставляет publishable comparison-ready material.
