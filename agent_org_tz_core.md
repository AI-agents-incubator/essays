# Agent Organization Infrastructure: Core Technical Assignment

> Версия файла: `v1.2`
> Дата версии: `2026-03-18`
> Тип документа: `инвариантное ядро технического задания`
> Основание:
> - [agent_operating_system.md](./agent_operating_system.md)
> - [agent_organization.md](./agent_organization.md)
> - [agent_organization_design.md](./agent_organization_design.md)
> - [agent_organization_self_learning.md](./agent_organization_self_learning.md)
> - [agent_org_tz_codex.md](./agent_org_tz_codex.md)
> - [agent_org_tz_claudecode.md](./agent_org_tz_claudecode.md)
>

## Аннотация

Это **главный и инвариантный** документ для построения первой версии инфраструктуры агентной организации.

Он задаёт:
- общую цель;
- общие требования;
- единый состав целевых артефактов;
- единый benchmark-контур;
- единые критерии оценки;
- единую стратегию state layer;
- единые правила изоляции двух реализаций.

Этот документ является **source of truth** для обеих runtime-версий:
- `Codex`;
- `Claude Code`.

Runtime-специфичные документы не должны переписывать это ядро. Они должны только отвечать на вопрос:

**как именно одна и та же целевая архитектура воплощается в конкретной агентной среде.**

## 1. Цель

Создать не один markdown-файл и не абстрактное описание, а **реальную инфраструктуру агентной организации** как внешнюю систему:
- папок;
- файлов;
- форматов артефактов;
- состояния и долгоживущей памяти;
- ролей;
- правил handoff;
- правил эскалации;
- benchmark-контура;
- learning-контура.

Эта инфраструктура должна позволять:
- независимо запускать два разных agent runtime;
- получать две отдельные реализации;
- не допускать пересечения их рабочих пространств;
- сравнивать результаты по одному и тому же ядру требований.

## 2. Главный принцип

Первичным продуктом является не агент и не промпт.

Первичным продуктом является **артефактная инфраструктура**, внутри которой агент:
- читает правила;
- принимает первую роль;
- создаёт новые рабочие состояния;
- при необходимости порождает новые роли и контексты;
- двигает цикл организации вперёд.

То есть сначала существует **внешняя организационная система**, и только потом агент её инстанцирует в работе.

## 3. Базовая архитектура репозитория

В репозитории должна существовать следующая верхнеуровневая структура:

```text
core/
  benchmarks/
  expected_results/
  evaluation/
  state/
runtimes/
  codex/
    workspace/
    runs/
    evaluation/
  claudecode/
    workspace/
    runs/
    evaluation/
comparison/
```

Смысл этой структуры такой:

- `core/` хранит общее и неизменное ядро эксперимента;
- `runtimes/` хранит две независимые песочницы исполнения;
- `comparison/` хранит результаты сопоставления.

## 4. Правило изоляции

Это одно из главных требований.

Оба агентных runtime должны работать **в разных execution-sandbox**, чтобы:
- не затирать результаты друг друга;
- не менять одни и те же runtime-файлы;
- не смешивать логи;
- не смешивать benchmark-прогоны;
- не смешивать собственные эволюционные изменения.

Правило простое:

- `Codex` пишет только внутри `runtimes/codex/`;
- `Claude Code` пишет только внутри `runtimes/claudecode/`;
- общее ядро в `core/` меняется только как осознанное изменение source of truth;
- итоговое сравнение живёт в `comparison/`.

## 5. Что считается общим source of truth

В `core/` должны жить именно инварианты эксперимента:

- ядро ТЗ;
- benchmark-templates;
- expected result templates;
- comparison criteria;
- state model and storage strategy;
- общие правила оценки;
- общая методология сравнения.

В `core/` не должны жить runtime-specific файлы:
- `AGENTS.md`;
- `CLAUDE.md`;
- `.codex/config.toml`;
- `.claude/settings.json`;
- runtime-specific agents;
- runtime-specific skills.

## 6. Что считается runtime-specific

В `runtimes/<runtime>/` должны жить:
- собственный workspace;
- собственные runtime-файлы;
- собственные логи прогонов;
- собственные evaluation-артефакты;
- собственные промежуточные результаты;
- собственные локальные версии целевой инфраструктуры.

Именно там оба агента должны независимо реализовывать одну и ту же архитектуру.

## 7. Что должно быть создано в каждой runtime-песочнице

Внутри каждого runtime workspace должна появиться одна и та же целевая организационная инфраструктура:

```text
runtimes/<runtime>/workspace/agent_org/
  charter/
    mission.md
    scope_and_boundaries.md
    role_map.md
    autonomy_model.md
  policies/
    escalation_policy.md
    risk_policy.md
    quality_gates.md
    artifact_change_policy.md
  intake/
    external_signals.md
    demand_queue.md
    triage_rules.md
  product/
    product_brief_template.md
    active_product_briefs/
  engineering/
    engineering_spec_template.md
    task_graph.md
    contract_registry.md
    dependency_map.md
  execution/
    work_orders/
    status_board.md
    handoff_log.md
    integration_log.md
  knowledge/
    decision_log.md
    domain_glossary.md
    pattern_library.md
    failure_library.md
  evaluation/
    golden_tasks.md
    benchmark_results.md
    process_audits.md
    metric_dashboard.md
  state/
    README.md
    state_registry.md
    storage_strategy.md
    sqlite_schema.sql
    supabase_migration_path.md
  evolution/
    improvement_backlog.md
    change_proposals.md
    approved_changes.md
  bootstrap/
    startup_sequence.md
    first_run_protocol.md
```

Это обязательный целевой каркас для обеих реализаций.

## 7a. Инвариантное требование к state layer

Обе реализации должны содержать отдельный слой состояния.

Он нужен для того, чтобы организация могла жить:
- не минуты, а недели и месяцы;
- не только как набор документов, но и как operational system;
- с восстановимым контекстом;
- с накоплением run history;
- с накоплением benchmark/evaluation history.

Базовая стратегия для v1:
- локальный `SQLite` внутри каждой runtime-песочницы;
- файловый слой остаётся control plane и explainability layer;
- позже допускается миграция в `Supabase / Postgres` как более устойчивый backend.

State layer не заменяет артефакты. Он дополняет их.

## 8. Инвариантные требования к содержанию артефактов

Каждый обязательный файл в `agent_org/` должен содержать не пустую заглушку, а **минимально рабочий шаблон**.

В шаблоне должны быть:
- назначение файла;
- владелец артефакта;
- обязательные поля;
- правила обновления;
- связи с соседними артефактами.

Запрещён формальный подход вида:
"здесь позже будет описание".

Нужно сразу фиксировать:
- кто создаёт артефакт;
- кто его читает;
- кто его изменяет;
- в какой момент цикла он обновляется;
- какой downstream-эффект он вызывает.

## 9. Инвариантный набор ролей

В обеих реализациях должен существовать один и тот же минимальный role set:

1. `business-sponsor-interface`
2. `product-lead`
3. `engineering-manager`
4. `implementation-agent`
5. `review-and-integration-agent`
6. `benchmark-and-audit-agent`
7. `learning-agent`

Для каждой роли должны быть одинаково определены:
- цель;
- зона ответственности;
- допустимые входы;
- ожидаемые выходы;
- право на делегирование;
- право на эскалацию;
- ограничения.

## 10. Инвариантный bootstrap

Обе реализации должны запускаться по одной и той же логике:

1. агент читает входной bootstrap-файл;
2. агент принимает первую роль;
3. агент проверяет состояние workspace;
4. агент создаёт недостающие базовые артефакты;
5. агент фиксирует первый рабочий цикл;
6. агент создаёт новые роли и контексты только по правилам структуры;
7. агент после завершения цикла возвращает систему в режим ожидания.

## 11. Инвариантный рабочий цикл

В обеих реализациях должен существовать один и тот же базовый цикл:

1. внешний сигнал;
2. triage;
3. product brief;
4. engineering spec;
5. task graph;
6. work orders;
7. handoff;
8. integration;
9. benchmark / audit;
10. change proposal;
11. обновление постоянных артефактов;
12. возврат к ожиданию.

Этот цикл должен быть выражен:
- в тексте;
- в структуре файлов;
- в логике переходов между артефактами.

## 11a. Инвариантный failure-governance контур

Обе реализации должны содержать не только happy-path цикл, но и один и тот же ограниченный контур работы со сбоем.

Это означает:

- у каждой observer directive должен быть явный `retry counter`;
- у каждой observer directive должен быть явный `retry budget`;
- repeated relaunch или repeated repair не могут считаться нормальной бесконечной работой;
- после исчерпания retry budget система обязана перейти в терминальное состояние, а не продолжать redispatch;
- peer-runtime, который свою часть выполнил, не должен терять свой результат из-за сбоя другой стороны.

Минимальный обязательный набор состояний для зрелой baseline-модели:

- `partial_success`
- `retry_budget_exhausted`
- `human_review_required`
- `wave_failed`

Базовое правило такое:

- пока retry budget не исчерпан, система может делать ограниченный repair/relaunch;
- если retry budget исчерпан, observer обязан зафиксировать `retry_budget_exhausted`;
- после этого система обязана оформить либо `human_review_required`, либо `wave_failed`;
- после этого дальнейший автоматический redispatch по той же директиве запрещён.

Это требование считается инвариантным, потому что без него агентная организация легко превращается в систему, которая не умеет честно завершать неуспешную wave и маскирует сбой под бесконечную активность.

## 12. Инвариантный self-learning контур

Обе реализации обязаны содержать один и тот же learning-контур:

- наблюдения из реальной работы;
- failure cases;
- canonical golden task;
- benchmark results;
- process audit;
- improvement backlog;
- controlled change proposals;
- approved changes.

Самообучение трактуется только как **управляемое изменение организационного слоя**, а не как свободное переписывание системы.

Learning trace должен иметь связь со state layer, чтобы накопленный operational контекст не терялся между циклами.

В этот learning-контур обязательно должны попадать:

- случаи `retry_budget_exhausted`;
- случаи `partial_success`;
- случаи `wave_failed`;
- lessons learned о том, почему repair path оказался недостаточным;
- предложения по изменению policies, barriers и quality gates, которые должны уменьшать повторение таких сценариев.

## 13. Инвариантная canonical golden task

Обе реализации должны использовать одну и ту же первую контрольную задачу.

Для неё должны быть единообразно заданы:
- вход;
- expected result;
- expected process;
- обязательные промежуточные артефакты;
- ожидаемые роли;
- ожидаемые handoff;
- допустимые отклонения;
- критерии провала.

## 14. Что должно лежать в `core/benchmarks/`

В `core/benchmarks/` должны лежать:
- benchmark templates;
- описание первой canonical golden task;
- правила benchmark-прогона;
- расширяемая структура для последующих golden tasks.

## 15. Что должно лежать в `core/expected_results/`

В `core/expected_results/` должны лежать:
- expected result templates;
- expected process templates;
- шаблон описания допустимых отклонений;
- шаблон фиксации критериев успеха и провала.

## 16. Что должно лежать в `core/evaluation/`

В `core/evaluation/` должны лежать:
- comparison criteria;
- score interpretation rules;
- единый шаблон сравнения двух runtime-реализаций;
- правила фиксации сильных и слабых сторон.

## 16a. Что должно лежать в `core/state/`

В `core/state/` должны лежать:
- state storage strategy;
- state entity model;
- SQLite-first schema template;
- маршрут миграции в долгоживущий backend;
- правила разделения artifact layer и state layer.

## 17. Что должно лежать в `runtimes/<runtime>/runs/`

В каждом `runs/` должны накапливаться:
- отдельные прогоны;
- лог запуска;
- версия исходного ядра;
- версия runtime-adapter;
- краткое описание того, что именно выполнялось;
- ссылка на итоговые артефакты.

## 18. Что должно лежать в `runtimes/<runtime>/evaluation/`

В каждом `evaluation/` должны накапливаться:
- локальные benchmark results;
- локальные process audit;
- локальные выявленные дефициты;
- локальные предложения по изменению реализации.

Это важно, потому что обе реализации должны иметь независимый evaluation-trace.

## 19. Что должно лежать в `comparison/`

В `comparison/` должны накапливаться:
- scorecards;
- findings;
- структурные различия двух реализаций;
- сравнительные выводы;
- решения о том, что переносится в общее ядро, а что остаётся runtime-specific.

## 20. План первой сборки инфраструктуры

Первая сборка должна идти по шагам:

1. создать `core/`;
2. создать `runtimes/`;
3. создать `comparison/`;
4. положить в `core/` инвариантные шаблоны;
5. создать две runtime-песочницы;
6. создать runtime-addendum для `Codex` и `Claude Code`;
7. подготовить структуру для независимых прогонов;
8. подготовить структуру для последующего сравнения.

## 21. Критерии готовности этой фазы

Фаза считается завершённой, если:

- существует единое инвариантное ТЗ;
- существует каркас `core / runtimes / comparison`;
- обе runtime-версии описаны как addendum, а не как отдельные несвязанные ТЗ;
- физически разведены места для независимого исполнения;
- физически разведены места для независимой оценки;
- существует ясный путь к следующему шагу: реальной реализации инфраструктуры в двух песочницах.

## 22. Главный смысл этой перестройки

Эта архитектура нужна для того, чтобы сравнивать не два разных задания, а **две независимые реализации одной и той же организационной системы**.

Только в такой схеме можно честно увидеть:
- где агент сильнее;
- где runtime удобнее;
- где лучше governance;
- где лучше bootstrap;
- где лучше artifact architecture;
- где лучше benchmark и learning trace.

## 23. Следующий шаг после этой фазы

После создания этого каркаса следующая работа уже прикладная:

1. выбрать первую canonical golden task;
2. заполнить core benchmark templates;
3. отдать `Codex` и `Claude Code` их runtime-addendum;
4. запустить две независимые реализации;
5. собрать результаты в `comparison/`.
