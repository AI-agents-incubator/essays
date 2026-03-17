# GT-002: Wave-Synchronized Orchestration With Shared Stage Barriers

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `canonical golden task`
> Основание:
> - [golden_task_template.md](./golden_task_template.md)
> - [../../agent_org_tz_core.md](../../agent_org_tz_core.md)
> - [GT-001-bootstrap-runtime-sandbox.md](./GT-001-bootstrap-runtime-sandbox.md)
>

## Идентификатор задачи

`GT-002`

## Название

`Wave-Synchronized Orchestration With Shared Stage Barriers`

## Цель

Проверить, способна ли вся система, а не только отдельный runtime:
- двигать две независимые runtime-песочницы по одной общей benchmark wave;
- не позволять одному runtime "убегать" вперёд в финальный closeout, пока второй не дошёл до нужного общего барьера;
- поддерживать единый и честный human-facing статус;
- завершать wave только тогда, когда observer, runtime status и runtime ack согласованы у обеих сторон.

Если `GT-001` проверял, может ли runtime вообще развернуть минимально рабочую агентную организацию, то `GT-002` проверяет следующий переход:

**может ли система из двух runtime вести одну общую волну как связанную организационную работу, а не как два независимых локальных цикла.**

## Контекст

Этот benchmark рождается из lesson learned после `GT-001`:
- локальные run могли быть успешны сами по себе;
- но wave-level прогресс и человеческий мониторинг расходились;
- один runtime мог закончить свою часть раньше;
- monitor и observer обязаны различать:
  - локальное завершение конкретного runtime;
  - ожидание peer-runtime;
  - полное завершение всей wave.

`GT-002` специально проверяет именно этот слой.

## Вход

Входящий внешний сигнал:

> Проведи обе runtime-песочницы через одну общую benchmark wave с обязательными stage barriers, общей observer-логикой и честным human-facing мониторингом.

Runtime и observer получают в качестве доступных данных:
- [agent_org_tz_core.md](../../agent_org_tz_core.md)
- [GT-001-bootstrap-runtime-sandbox.md](./GT-001-bootstrap-runtime-sandbox.md)
- [../expected_results/GT-002-expected_result.md](../expected_results/GT-002-expected_result.md)
- [../evaluation/comparison_criteria.md](../evaluation/comparison_criteria.md)
- runtime-specific addendum:
  - [../../agent_org_tz_codex.md](../../agent_org_tz_codex.md)
  - [../../agent_org_tz_claudecode.md](../../agent_org_tz_claudecode.md)

## Ограничения

Система обязана:
- сохранять физическую изоляцию двух runtime-песочниц;
- использовать единый observer и execution plane как общий coordination layer;
- не считать wave завершённой только на основании локального `completed` у одного runtime;
- не подменять stage barrier narrative-описанием без артефактов;
- не скрывать protocol mismatch и stale state в human monitor;
- не запускать следующую стадию, если общий barrier не выполнен.

## Что именно проверяется

### 1. Shared wave model

Должно быть видно, что существует одна общая wave, у которой есть:
- идентификатор;
- последовательность стадий;
- критерии перехода между стадиями;
- общее условие завершения.

### 2. Stage barriers

Минимально должны существовать общие стадии:
1. `wave_open`
2. `runtime_execution`
3. `peer_wait_or_sync`
4. `comparison_or_closeout`
5. `wave_complete`

Система должна явно фиксировать:
- кто из runtime уже дошёл до текущего барьера;
- кто ещё нет;
- почему wave пока не может перейти дальше.

### 3. Human-facing truth

Human monitor должен:
- не скрывать protocol mismatch;
- не показывать ложный `terminal_complete`, если final hold не подтверждён;
- различать:
  - `active`
  - `waiting_peers`
  - `protocol_stale`
  - `protocol_inconsistent`
  - `terminal_complete`

### 4. Closeout discipline

Wave считается завершённой только если:
- оба runtime закрыли локальную работу;
- observer выписал финальный `hold`;
- у обоих runtime есть matching `RUNTIME_ACK`;
- human monitor показывает согласованную wave-level картину.

## Expected Result

После успешного прогона должны существовать:

1. shared wave coordination artifacts;
2. stage barrier trace;
3. human-facing heartbeat, который честно интерпретирует raw protocol;
4. wave closeout trace;
5. comparison-ready package, пригодный для следующей benchmark wave.

Подробная expected signature зафиксирована в:

[../expected_results/GT-002-expected_result.md](../expected_results/GT-002-expected_result.md)

## Expected Process

### Обязательные участники

В правильном процессе должны быть явно задействованы:
1. `observer`
2. `execution-plane`
3. `codex-runtime`
4. `claudecode-runtime`
5. `human-monitor-layer`

### Обязательные артефакты процесса

Минимально должны появиться:
- один shared wave registry;
- один barrier-state artifact;
- один observer decision trace по переходам между стадиями;
- один human monitor snapshot с корректной интерпретацией;
- один closeout trace;
- минимум одна learning-запись про coordination quality.

### Обязательные проверки

Должны быть явно проверены:
1. переход `local runtime completion -> waiting_peers`;
2. переход `waiting_peers -> closeout allowed`;
3. переход `final hold issued -> matching runtime ack`;
4. переход `matching runtime ack -> terminal_complete`;
5. отсутствие ложного `terminal_complete` до схлопывания протокола.

## Допустимые отклонения

Допускается:
- вариация в конкретных названиях barrier-файлов;
- различие в структуре локальных runtime trace;
- различие в деталях мониторинга, если общий смысл статусов совпадает;
- дополнительные health-поля в heartbeat.

Не допускается:
- скрытый переход в `terminal_complete` при raw mismatch;
- локальный closeout одного runtime без учёта peer-runtime;
- отсутствие wave-level coordination trace;
- отсутствие human-readable интерпретации состояния;
- отсутствие явного final hold reconciliation.

## Критерии провала

Прогон считается неуспешным, если:
- один runtime завершает wave раньше системы и это не отражено как `waiting_peers`;
- monitor показывает ложный успех;
- raw protocol и human heartbeat системно расходятся;
- финальный hold не требует matching ack;
- observer не может отличить локальное завершение runtime от завершения всей wave;
- нет shared barrier trace и нет evidence общего coordination layer.
