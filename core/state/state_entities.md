# State Entities

> Версия файла: `v1.0`
> Дата версии: `2026-03-16`
> Тип документа: `модель сущностей state layer`

## Базовые сущности

Ниже перечислен минимальный набор сущностей, которые должны существовать в state layer.

## 1. `organization_runs`

Что хранит:
- идентификатор прогона;
- runtime;
- benchmark id;
- стартовое время;
- конечное время;
- статус;
- ссылка на run summary.

## 2. `roles`

Что хранит:
- role id;
- run id;
- тип роли;
- текущий статус;
- scope;
- текущий owner context;
- timestamp последнего изменения.

## 3. `work_items`

Что хранит:
- work item id;
- run id;
- исходный сигнал;
- текущий этап;
- связанный product brief;
- связанная engineering spec;
- приоритет;
- статус.

## 4. `handoff_events`

Что хранит:
- handoff id;
- from role;
- to role;
- work item id;
- timestamp;
- статус handoff;
- ссылка на артефакт передачи.

## 5. `artifact_registry`

Что хранит:
- artifact id;
- тип артефакта;
- путь к файлу;
- связанный run id;
- связанный work item id;
- версия;
- timestamp обновления.

## 6. `benchmark_runs`

Что хранит:
- benchmark run id;
- benchmark id;
- runtime;
- run id;
- expected result version;
- итоговый статус;
- short notes.

## 7. `audit_findings`

Что хранит:
- finding id;
- benchmark run id;
- severity;
- finding category;
- описание;
- рекомендация.

## 8. `change_proposals`

Что хранит:
- proposal id;
- источник наблюдения;
- тип изменения;
- целевой артефакт;
- ожидаемый эффект;
- статус;
- ссылка на подтверждающий benchmark.

## 9. `state_variables`

Что хранит:
- key;
- value;
- scope;
- runtime;
- run id;
- updated_at.

Эта сущность нужна для operational переменных, которые неудобно хранить в narrative-файлах.

## Минимальный принцип проектирования

State layer не должен становиться хаотичным dump-хранилищем.

Каждая сущность должна отвечать на один из вопросов:
- где сейчас находится работа;
- кто сейчас отвечает за следующий шаг;
- какие артефакты уже созданы;
- какой benchmark уже был пройден;
- какие проблемы уже обнаружены;
- какие изменения готовятся.
