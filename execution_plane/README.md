# Execution Plane

> Версия файла: `v1.1`
> Дата версии: `2026-03-18`
> Тип документа: `runtime launcher layer`

## Зачем нужен этот слой

`Control plane` сам по себе недостаточен.

Он умеет:

- принимать сигнал от runtime;
- хранить директивы наблюдателя;
- хранить подтверждения runtime.

Но он не умеет **поднимать или резюмировать самого агента**.

Именно это и создаёт главный разрыв:

- протокол уже есть;
- runtime уже ждёт директиву;
- observer уже может её записать;
- но никто не исполняет переход `директива -> фактический запуск агента`.

`Execution plane` закрывает именно этот разрыв.

## Что делает execution plane

Этот слой:

- читает `control_plane`
- смотрит, есть ли активная observer directive
- проверяет, не запущен ли уже соответствующий runtime
- если нужно, автоматически резюмирует или запускает runtime через CLI
- выполняет `observer-auto` шаг перед dispatch, чтобы closed loop не рвался после `run = completed`

Для текущей машины используются:

- `codex exec resume --last`
- `claude --continue --print`

## Что execution plane не делает

Он не заменяет продуктовый judgement человека.

Он:

- не принимает продуктовые решения;
- не пишет сравнения за человека;
- не выдумывает произвольный следующий run вне backlog/evaluation.

Но теперь он делает две связанные функции:

1. `observer-auto`
   Из завершённого run строит следующую директиву, если следующий шаг однозначен из backlog/evaluation.

2. `directive -> фактический headless runtime launch`
   После появления директивы запускает соответствующий runtime без участия человека.

Таким образом, loop больше не должен останавливаться после каждого completed run только потому, что никто вручную не выписал следующую команду.

## Terminal Closeout Rule

Если open improvement backlog ещё есть, `observer-auto` выпускает следующий `continue_with_next_run`.

Если open backlog уже пуст, loop не должен выглядеть как зависание.

Поэтому `observer-auto` делает ещё один обязательный шаг:

1. выпускает terminal directive `prepare_comparison`;
2. runtime выполняет closeout/comparison package;
3. только после этого loop фиксирует `autonomous_cycle_complete`.

Это убирает ложную паузу вида:

`completed -> тишина -> пользователь думает, что система зависла`

и заменяет её на:

`completed -> terminal closeout task -> autonomous cycle complete`

## Retry Budget Enforcement

`Execution plane` не должен быть нейтральным к repeated relaunch.

Если runtime многократно перезапускается по одной и той же observer directive, execution layer обязан различать два состояния:

- допустимый ограниченный repair loop;
- бесконечный дефектный redispatch.

Для этого execution plane должен поддерживать:

- retry counter на уровень `directive_id`;
- retry budget;
- watchdog, который не только убивает stalled runtime, но и учитывает это как одну из попыток;
- terminal transition после exhaustion, а не новый бесконечный launch.

После исчерпания retry budget execution plane больше не должен автоматически поднимать тот же runtime по той же директиве. Вместо этого он обязан перевести control layer в один из двух terminal paths:

- `human_review_required`
- `wave_failed`

## Wave-Level Failure Semantics

На уровне benchmark wave execution plane обязан различать:

- `terminal_complete`
- `partial_success`
- `human_review_required`
- `wave_failed`

Это важно, потому что system-level truth не равна локальной truth одного runtime.

Например:

- один runtime может честно завершить свою часть;
- другой может дойти до `retry_budget_exhausted`;
- итог wave в этом случае не `terminal_complete`, а failure-bearing terminal outcome, который сохраняет локальный успех peer-runtime, но честно признаёт провал всей волны.

## Human Monitor Truth Rule

`HUMAN_PROGRESS.md` не должен сглаживать неудобную правду.

Он обязан строиться по наиболее строгой трактовке сырых артефактов control plane и runtime plane.

Это означает:

- финальный успех нельзя показывать, если `observer directive` и `runtime ack` ещё не согласованы;
- при рассинхроне протокола human monitor обязан показывать degraded или inconsistent state;
- при `retry_budget_exhausted` human monitor обязан явно показывать, что дальнейший автоматический прогон запрещён;
- если один runtime завершён, а второй нет, human monitor не должен называть всю wave завершённой.

## Основные файлы

- [orchestrator.py](./orchestrator.py)
- [orchestrator_protocol.md](./orchestrator_protocol.md)
- [HUMAN_PROGRESS.md](./HUMAN_PROGRESS.md)
- [monitor_live.sh](./monitor_live.sh)

## Куда смотреть человеку

Если нужен один человеко-читаемый канал прогресса, смотреть нужно сюда:

- [HUMAN_PROGRESS.md](./HUMAN_PROGRESS.md)

Этот файл обновляется самим оркестратором на каждом polling cycle и показывает:

- какой сейчас `run` у каждого runtime;
- жив ли worker process;
- какая активная observer directive;
- в каком состоянии `ack`;
- каков возраст status/ack сигнала в секундах;
- каков возраст и размер worker log, чтобы видеть внутреннюю активность даже когда `RUNTIME_STATUS` ещё не сменился;
- какая текущая фаза observer-loop;
- есть ли открытый backlog item для автоматического продолжения;
- есть ли `needs_human` или `blocking_issue`;
- согласован ли финальный `directive_id` с `runtime_ack`;
- не исчерпан ли retry budget;
- является ли system-level итог `terminal_complete`, `partial_success`, `human_review_required` или `wave_failed`;
- последние события execution plane.

Если нужен живой терминальный просмотр без ручного переоткрытия файла:

```bash
/Users/alexeykrolmini/Code/essays/execution_plane/monitor_live.sh
```

## Важное ограничение

Этот слой может автоматически разбудить или резюмировать runtime-сессию.

Но он не может "разбудить" именно этот чат сам по себе.

Поэтому execution plane устраняет ручную пересылку prompt-ов к runtime, но не превращает текущий разговор в полноценный background daemon UI.
