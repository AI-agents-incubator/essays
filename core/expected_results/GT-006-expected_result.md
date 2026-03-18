# GT-006 Expected Result

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `expected result signature`
> Основание:
> - [expected_result_template.md](./expected_result_template.md)
> - [../benchmarks/GT-006-retry-budget-exhaustion-closeout.md](../benchmarks/GT-006-retry-budget-exhaustion-closeout.md)
>

## Result Identity

- benchmark: `GT-006`
- expected result version: `v1.0`

## Итоговые свойства результата

После успешного прогона система должна демонстрировать не только escalation, а **жёстко оформленный terminal closeout после `retry_budget_exhausted`, с запретом дальнейшего automatic redispatch и сохранением peer progress**.

## Обязательные результатные сигнатуры

### 1. Retry budget trace

Должно быть возможно восстановить:

- какой `directive_id` имел ограниченный budget;
- сколько попыток было разрешено;
- на какой попытке budget закончился.

### 2. Exhaustion evidence

Должно быть видно, что состояние `retry_budget_exhausted` было выражено явно, а не выведено постфактум из narrative.

### 3. Terminal closeout after exhaustion

Финальный outcome обязан принадлежать множеству:

- `human_review_required`
- `wave_failed`

При этом automatic redispatch после exhaustion должен отсутствовать.

### 4. Preserved peer success

Если peer-runtime уже выполнил свою часть, system-level truth должна сохранить это как `partial_success`.

### 5. Human monitor consistency

Human monitor обязан:

- показывать exhaustion как отдельную фазу;
- показывать, что дальнейший automatic retry запрещён;
- честно отображать final terminal state;
- не рисовать active run после closeout.

## Expected Process Signature

Правильный процесс должен оставить evidence следующих фаз:

1. `bounded_retry_attempts`
2. `retry_budget_exhausted`
3. `automatic_redispatch_stopped`
4. `terminal_closeout_selected`
5. `peer_progress_preserved`
6. `wave_failed_or_human_review_required`

## Failure Signature

Признаками failure считаются:

- budget неявен или не восстановим;
- exhaustion не фиксируется как отдельное состояние;
- redispatch продолжается после exhaustion;
- wave остаётся ambiguous;
- peer-success теряется;
- monitor врёт о том, что система всё ещё healthy active.
