# CURRENT MISSION: Claude Code Runtime

> Версия файла: `v2.0`
> Дата версии: `2026-03-17`
> Тип документа: `active runtime loop`
> Runtime: `Claude Code`
> Текущая фаза: `post-RUN-002 / observer-directed`

## Исходное состояние

`RUN-002` завершён.

Сейчас runtime должен уметь не только выполнять run, но и:

- ждать следующую директиву наблюдателя;
- подтверждать, что директива увидена;
- стартовать новый run только после явной команды через локальный runtime-facing control layer.

## Главная цель этого файла

Сделать следующий цикл работы `Claude Code` **observer-directed**.

Это означает:

- runtime не должен самовольно стартовать `RUN-003`;
- переход к следующему шагу идёт через `OBSERVER_DIRECTIVE.md`;
- runtime обязан обновлять локальный `RUNTIME_ACK.md`.

## Обязательный порядок чтения перед следующим действием

1. `workspace/CLAUDE.md`
2. `runs/RUNTIME_STATUS.md`
3. `control/observer_runtime_protocol.md`
4. `control/OBSERVER_DIRECTIVE.md`
5. `control/RUNTIME_ACK.md`

## Логика поведения

### Если directive = `hold`

- обновить `RUNTIME_ACK.md` в состояние `seen` или `accepted`
- не запускать новый run
- не менять структуру sandbox без отдельной директивы
- ждать следующую команду наблюдателя

### Если directive = `continue_with_next_run`

- обновить `RUNTIME_ACK.md` в состояние `accepted`
- перевести `RUNTIME_STATUS.md` из `completed` в `in_progress`
- стартовать следующий явно разрешённый run
- после завершения снова обновить и `RUNTIME_STATUS.md`, и `RUNTIME_ACK.md`

### Если directive = `repair_current_state`

- принять директиву через `RUNTIME_ACK.md`
- выполнить только repair-задачу, указанную наблюдателем
- не превращать repair в новый широкий run без отдельного разрешения

### Если directive = `prepare_comparison`

- подготовить требуемый comparison package
- не запускать новый engineering run
- не менять `current_run`, если директива относится к closeout уже завершённого run
- перевести `RUNTIME_ACK.md` в `completed`, когда comparison/closure package готов
- не начинать следующий engineering run автоматически

### Если directive = `human_review_required`

- остановиться
- обновить `RUNTIME_ACK.md` в `needs_clarification` или эквивалентное состояние
- ждать человека

## Ограничения

- Нельзя менять `core/`
- Нельзя менять `comparison/`
- Нельзя менять `runtimes/codex/`
- Нельзя начинать новый run без observer directive

## Что считается успешным результатом

Успех этого слоя означает, что `Claude Code`:

- умеет стоять в осознанном ожидании;
- умеет читать observer directive;
- умеет подтверждать её через `RUNTIME_ACK.md`;
- не стартует следующий run самовольно;
- может перейти к `RUN-003` только по внешней директиве.
