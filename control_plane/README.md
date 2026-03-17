# Control Plane

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `communication layer`

## Назначение

Этот каталог задаёт **примитивный двусторонний коммуникационный слой** между:

- работающими runtime-песочницами;
- наблюдателем / координатором;
- в будущем watcher-ом или демоном.

До этого у нас был только односторонний сигнал:

- `runtime -> observer` через `RUNTIME_STATUS.md`

Теперь добавляется и обратный канал:

- `observer -> runtime` через `OBSERVER_DIRECTIVE.md`
- `runtime -> observer` через `RUNTIME_ACK.md`

Но даже после этого протокол остаётся пассивным, если нет слоя, который умеет реально резюмировать paused runtime sessions.

Именно поэтому поверх `control_plane` теперь существует ещё и `execution_plane`.

## Почему это отдельный слой

Этот слой вынесен из `runtimes/` специально.

Причины:

- не смешивать живую sandbox с внешним управлением;
- не ломать работающие run-артефакты;
- отделить внутреннюю работу runtime от внешнего наблюдения и команд;
- получить основу для будущего watcher / daemon loop.

## Что входит в control plane

- [observer_runtime_protocol.md](./observer_runtime_protocol.md) — формальный протокол двусторонней коммуникации.
- [observer_loop.md](./observer_loop.md) — схема реакции наблюдателя на завершение этапов.
- [codex/OBSERVER_DIRECTIVE.md](./codex/OBSERVER_DIRECTIVE.md) — текущая директива наблюдателя для `Codex`.
- [codex/RUNTIME_ACK.md](./codex/RUNTIME_ACK.md) — подтверждение или ответ runtime для `Codex`.
- [claudecode/OBSERVER_DIRECTIVE.md](./claudecode/OBSERVER_DIRECTIVE.md) — текущая директива наблюдателя для `Claude Code`.
- [claudecode/RUNTIME_ACK.md](./claudecode/RUNTIME_ACK.md) — подтверждение или ответ runtime для `Claude Code`.

## Базовая идея

После завершения run runtime не должен просто “замолкать”.

Он:

- обновляет `RUNTIME_STATUS.md`;
- оставляет `summary` и `evaluation`;
- ждёт следующую директиву наблюдателя.

Наблюдатель:

- читает `RUNTIME_STATUS.md`;
- читает `summary` и `evaluation`;
- формулирует следующую директиву;
- записывает её в `control_plane/<runtime>/OBSERVER_DIRECTIVE.md`.

Это и есть первый рабочий вариант двусторонней связи.
