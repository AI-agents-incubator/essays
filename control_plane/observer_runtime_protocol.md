# Observer <-> Runtime Protocol

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `bidirectional protocol`

## Зачем нужен этот протокол

Одного `RUNTIME_STATUS.md` недостаточно.

Он позволяет понять, что runtime завершил этап или упёрся в блокер, но не позволяет:

- передать runtime следующую команду;
- зафиксировать, что runtime эту команду увидел;
- различать "runtime завершил run" и "runtime ждёт следующую директиву".

Поэтому нужен двусторонний контур.

## Три артефакта протокола

### 1. `RUNTIME_STATUS.md`

Это канал:

`runtime -> observer`

Он сообщает:

- в каком run сейчас runtime;
- завершён ли run;
- нужен ли человек;
- где лежат итоговые артефакты.

### 2. `OBSERVER_DIRECTIVE.md`

Это канал:

`observer -> runtime`

Он сообщает:

- какую следующую команду наблюдатель даёт runtime;
- относится ли она к текущему run или к следующему;
- должен ли runtime продолжать, ждать, исправлять, эскалировать или останавливаться.

### 3. `RUNTIME_ACK.md`

Это канал:

`runtime -> observer`

Он сообщает:

- увидел ли runtime директиву;
- принял ли её;
- нужна ли дополнительная ясность;
- завершил ли выполнение этой директивы.

## Базовый цикл

### Шаг 1. Runtime завершает run

Runtime:

- обновляет `RUNTIME_STATUS.md`
- выставляет `completed`, `blocked`, `failed` или `escalation_required`
- указывает `summary_file` и `evaluation_file`

### Шаг 2. Observer читает итог

Observer:

- читает `RUNTIME_STATUS.md`
- читает `summary_file`
- читает `evaluation_file`
- делает вывод: что дальше

### Шаг 3. Observer пишет директиву

Observer обновляет `OBSERVER_DIRECTIVE.md`.

Типы директив:

- `hold`
- `continue_with_next_run`
- `repair_current_state`
- `prepare_comparison`
- `stop`
- `human_review_required`

### Шаг 4. Runtime подтверждает

Перед следующим активным шагом runtime обязан прочитать `OBSERVER_DIRECTIVE.md` и обновить `RUNTIME_ACK.md`.

Статусы подтверждения:

- `not_seen`
- `seen`
- `accepted`
- `needs_clarification`
- `completed`
- `rejected`

## Почему это лучше, чем просто “человек что-то говорит в чат”

Потому что здесь появляется внешний, проверяемый, версионируемый control layer.

То есть:

- команда не теряется в истории треда;
- runtime и observer работают через артефакты;
- появляется основа для automation;
- появляется возможность строить watcher без изменения логики протокола.

## Минимальное правило ожидания

Если runtime завершил run и не получил новую директиву, он должен считаться находящимся в режиме:

**"awaiting observer directive"**

Это состояние пока не добавляется в `RUNTIME_STATUS.md` как отдельный статус, чтобы не ломать уже принятый простой протокол.

На первом этапе это состояние выражается так:

- `RUNTIME_STATUS.md` уже `completed`
- в `OBSERVER_DIRECTIVE.md` стоит `hold`
- в `RUNTIME_ACK.md` ещё нет принятой новой команды

## Следующий уровень

Когда понадобится полный automation-loop, этот же протокол можно будет обслуживать watcher-ом или демоном.

То есть future daemon не заменит протокол, а просто начнёт его автоматически обслуживать.
