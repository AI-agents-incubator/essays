# GT-007 Expected Result

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `expected result signature`
> Основание:
> - [expected_result_template.md](./expected_result_template.md)
> - [../benchmarks/GT-007-runtime-authored-failure-package.md](../benchmarks/GT-007-runtime-authored-failure-package.md)
>

## Result Identity

- benchmark: `GT-007`
- expected result version: `v1.0`

## Итоговые свойства результата

После успешного прогона система должна демонстрировать не просто terminal failure outcome, а **полноценный runtime-authored failure package, который делает failed runtime сравнимым по качеству следов с successful peer-runtime**.

## Обязательные результатные сигнатуры

### 1. Runtime-authored failure package

Должно быть возможно восстановить:

- локальный diagnosis;
- retry history;
- exhaustion or escalation reason;
- impacted artifacts;
- suggested next actions;
- terminal statement from the failed runtime itself.

### 2. System-level closeout linked to runtime evidence

Должно быть видно, что observer и system-level closeout опираются не только на raw control-plane signals, но и на runtime-authored failure package.

### 3. Preserved peer-success package

Успешная ветка wave должна остаться доступной в comparison-ready форме и не теряться из-за провала другой ветки.

### 4. Comparison-ready asymmetry handling

В comparison layer должно быть возможно:

- сравнивать success package одной ветки;
- сравнивать failure package другой ветки;
- делать выводы не на основании пустого failed state, а на основании содержательного failed package.

### 5. Human monitor consistency

Human monitor обязан:

- показывать failure-bearing terminal outcome;
- показывать, что failed runtime оставил собственный package;
- не подменять runtime-authored truth observer-only explanation.

## Expected Process Signature

Правильный процесс должен оставить evidence следующих фаз:

1. `failure_path_confirmed`
2. `runtime_authored_failure_package_created`
3. `peer_success_package_preserved`
4. `system_closeout_linked_to_failure_package`
5. `comparison_ready_dual_package_state`
6. `post_wave_learning`

## Failure Signature

Признаками failure считаются:

- у failed runtime нет собственного failure package;
- observer-side closeout полностью заменяет локальную failure truth;
- peer-success package остаётся, а failed side почти пустая;
- comparison layer не может опираться на runtime-authored failure evidence;
- monitor создаёт ложное ощущение, что observer narrative сам по себе достаточен.
