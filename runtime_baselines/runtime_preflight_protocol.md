# Runtime Preflight Protocol

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `preflight protocol`

## Назначение

Этот документ фиксирует обязательный шаг, который должен происходить **до любого автономного запуска агента**.

Этот шаг называется `runtime preflight`.

Его задача — убедиться, что агент стартует не как голый assistant, а как уже подготовленный runtime с установленной операционной системой.

## Главный принцип

Нельзя запускать агент прямо на проектную mission, если перед этим не установлен baseline-пакет метафайлов.

Правильный порядок такой:

1. восстановить `runtime baseline`
2. наложить `project overlay`
3. проверить preflight
4. только потом запускать `active run`

## Что входит в baseline

Минимум должен существовать:

- основной instruction-файл (`AGENTS.md` или `CLAUDE.md`)
- runtime config (`config.toml` или `settings.json`)
- базовый policy/governance слой
- baseline roles / agents
- baseline skills
- правила безопасной автономности

## Что такое project overlay

Это уже не default-пакет, а проектная адаптация baseline.

Сюда входят:

- project-specific entrypoint
- mission files
- runtime status signal
- project-specific rules
- project-specific skills или agents, если они нужны

## Preflight checklist

Перед запуском нужно проверить:

1. baseline действительно установлен
2. установлены правильные версии метафайлов
3. настроен режим автономности
4. включены нужные ограничения безопасности
5. есть baseline roles и baseline skills
6. project overlay не противоречит baseline
7. есть entrypoint текущего проекта
8. есть active mission
9. есть signal layer для статуса run
10. local permission files не содержат inline creds и защищены от git

## Что считается ошибкой

Методологическая ошибка — это ситуация, когда:

- проектная миссия уже написана;
- runtime sandbox уже создан;
- агент уже запущен;
- но его baseline layer не был заранее установлен и проверен.

Именно это создаёт разрыв между нашей теорией и практикой.

Точно так же ошибкой считается ситуация, когда:

- `.claude/settings.local.json` уже накопил реальные секреты;
- файл не защищён как часть политики репозитория;
- но long autonomous run всё равно запускается как будто среда безопасна.

## Что делать правильно дальше

Для каждого нового запуска:

- сначала брать baseline-пакет нужного runtime;
- потом создавать или обновлять project overlay;
- только потом запускать агента на mission.

Так `Agent Operating System` становится не абстрактной идеей, а реально установленным слоем.
