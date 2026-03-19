# Agent Organization Project Starter

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `deployable starter kit`

## Зачем нужен этот пакет

Этот каталог превращает baseline-репозиторий из набора методологических документов в **plug-and-play starter kit** для нового проекта.

Целевая схема работы такая:

1. пользователь создаёт пустую папку под новый проект;
2. starter kit разворачивает в ней минимально рабочую структуру агентной организации;
3. пользователь заполняет один верхнеуровневый входной артефакт;
4. runtime читает bootstrap и intake;
5. после этого агентная организация сама строит:
   - уточняющие вопросы;
   - product brief;
   - engineering spec;
   - task graph;
   - work orders;
   - execution trace;
   - evaluation and learning trace.

## Что входит в starter kit

- [install_project_scaffold.sh](./install_project_scaffold.sh) — shell-скрипт развёртывания starter scaffold в новую папку проекта.
- [SCAFFOLD_MANIFEST.md](./SCAFFOLD_MANIFEST.md) — описание того, какие папки и файлы создаются и зачем они нужны.
- [PLUG_AND_PLAY_USER_FLOW.md](./PLUG_AND_PLAY_USER_FLOW.md) — верхнеуровневое product-описание starter kit с точки зрения пользователя. Внутри: целевой user flow, границы автономности, этапы handoff и признаки готовности формата.
- [template_project/](./template_project/) — минимальная проектная структура, которая копируется в новый проект.

## Как использовать

### Шаг 1. Создать папку проекта

Пример:

```bash
mkdir -p /path/to/new-project
```

### Шаг 2. Развернуть scaffold

```bash
/Users/alexeykrolmini/Code/essays/project_starter/install_project_scaffold.sh /path/to/new-project
```

### Шаг 3. Заполнить входной артефакт

После развёртывания в новом проекте нужно заполнить:

- `project_input/PROJECT_REQUEST.md`

Это не ТЗ в инженерном смысле, а верхнеуровневое описание:

- что вы хотите сделать;
- для кого;
- какой результат нужен;
- какие ограничения есть;
- что уже известно;
- что пока неясно.

### Шаг 4. Передать управление агентной организации

После этого runtime должен начать чтение в таком порядке:

1. `START_HERE.md`
2. `project_input/PROJECT_REQUEST.md`
3. `agent_org/bootstrap/ORG_BOOTSTRAP.md`
4. `agent_org/charter/mission.md`
5. `agent_org/charter/autonomy_model.md`
6. `agent_org/policies/escalation_policy.md`
7. `agent_org/policies/quality_gates.md`
8. `agent_org/intake/intake_protocol.md`

Затем организация обязана:

1. подтвердить понимание project request;
2. сформулировать недостающие вопросы, если они действительно нужны;
3. создать `product brief`;
4. создать `engineering spec`;
5. создать `task graph`;
6. перейти к execution cycle.

## Что этот пакет не делает

Этот starter kit:

- не выбирает за пользователя конкретный runtime;
- не поднимает автоматически background execution plane;
- не делает project-specific content без входного project request;
- не заменяет runtime baselines для `Codex` и `Claude Code`.

Он решает более базовую задачу:

**даёт переносимую стартовую организационную оболочку для нового проекта.**

## Связь с baseline

Этот пакет не является отдельной альтернативной системой.

Он является прикладной упаковкой того, что уже описано в:

- [../agent_org_tz_core.md](../agent_org_tz_core.md)
- [../agent_organization_design.md](../agent_organization_design.md)
- [../agent_operating_system.md](../agent_operating_system.md)
- [../runtime_baselines/README.md](../runtime_baselines/README.md)

## Признак готовности starter kit

Starter kit считается готовым к использованию, если:

- его можно развернуть в пустую папку проекта одной командой;
- в проекте появляется минимальная рабочая структура агентной организации;
- у пользователя есть один понятный входной файл;
- у runtime есть один понятный bootstrap path;
- handoff от человека к агентной организации не требует ручного изобретения новых правил.
