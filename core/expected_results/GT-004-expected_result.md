# GT-004 Expected Result

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `expected result signature`
> Основание:
> - [expected_result_template.md](./expected_result_template.md)
> - [../benchmarks/GT-004-no-mid-wave-operator-tuning.md](../benchmarks/GT-004-no-mid-wave-operator-tuning.md)
>

## Result Identity

- benchmark: `GT-004`
- expected result version: `v1.0`

## Итоговые свойства результата

После успешного прогона система должна демонстрировать не "удобный" исход, а **честный terminal outcome, достигнутый без mid-wave operator tuning и без изменения frozen operational contracts**.

## Обязательные результатные сигнатуры

### 1. Frozen contract evidence

Должно быть возможно восстановить:

- какие operational contracts считались замороженными;
- когда именно wave стартовала на этих контрактах;
- что эти контракты не менялись по ходу прогона.

### 2. Honest wave progression under frozen rules

Должно быть видно, что system-level progress, repair и closeout происходили в рамках уже заданных правил.

### 3. Terminal outcome without operator rescue

Финальный исход обязан принадлежать множеству:

- `terminal_complete`
- `partial_success`
- `human_review_required`
- `wave_failed`

Но при этом он не должен зависеть от mid-wave изменения prompts, entrypoints или protocol semantics.

### 4. Human monitor consistency

Human monitor обязан:

- не скрывать failure-bearing outcome;
- не рисовать успех там, где его добились ручной подстройкой;
- объяснять, что система дошла до terminal state на frozen contracts.

### 5. Learning signal about contract adequacy

После `GT-004` должна появиться learning-запись о том:

- каких контрактов оказалось достаточно;
- каких контрактов не хватило;
- какие изменения надо вносить уже после wave, а не в середине неё.

## Expected Process Signature

Правильный процесс должен оставить evidence следующих фаз:

1. `contracts_frozen`
2. `wave_open`
3. `runtime_progress_under_frozen_rules`
4. `bounded_repair_or_direct_progress`
5. `terminal_outcome_under_frozen_rules`
6. `post_wave_learning`

## Failure Signature

Признаками failure считаются:

- mid-wave изменение operator prompt, entrypoint или protocol semantics;
- невозможность доказать, что contracts действительно были frozen;
- terminal success, достигнутый через ручной rescue;
- human monitor скрывает факт mid-wave tuning;
- отсутствие learning signal о качестве frozen contracts.
