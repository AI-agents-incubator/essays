# Вход - план

Ниже полный TODO-план именно **в рамках текущей задачи**, а не всего репозитория.

**Что уже сделано**
- Создан общий индекс: [COURSE-INDEX.md](/Users/alexeykrolmini/Code/coursevibecode/COURSE-INDEX.md)
- Создано оглавление книги по Codex: [README.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/README.md)
- Создана и сильно доработана глава 1 по Codex: [01-codex-first-contact.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/01-codex-first-contact.md)
- Сохранены конспекты-траектории:
  - [codex-agent-learning-path.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-agent-learning-path.md)
  - [claude-code-agent-learning-path.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/claude-code-agent-learning-path.md)
- Добавлена быстрая навигация в [README.md](/Users/alexeykrolmini/Code/coursevibecode/README.md)
- Снят игнор с новых файлов в [.gitignore](/Users/alexeykrolmini/Code/coursevibecode/.gitignore)

**Главный текущий риск**
- Для GitHub текущие внутренние ссылки еще нужно нормализовать.
- Сейчас часть новых файлов использует локальные абсолютные пути. Для работы на GitHub нужны относительные ссылки внутри репозитория.

**TODO 1. Довести навигационную структуру до publish-ready**
- Создать [README.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/README.md) как индекс раздела `2_lessons`
- Создать папку книги по Claude Code: `/Users/alexeykrolmini/Code/coursevibecode/2_lessons/claude-code-book`
- Создать [README.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/claude-code-book/README.md)
- Перевести внутренние ссылки в [COURSE-INDEX.md](/Users/alexeykrolmini/Code/coursevibecode/COURSE-INDEX.md) на относительные GitHub-friendly
- Перевести внутренние ссылки в [README.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/README.md) на относительные
- Перевести внутренние ссылки в будущих chapter-файлах на относительные
- Решить, как показывать ссылки на `/Users/alexeykrolmini/Code/essays`
- Вариант решения: оставить эти пути как обычный текст без ссылки
- Вариант решения: перенести ключевые reference-файлы внутрь репозитория
- После этого обновить [README.md](/Users/alexeykrolmini/Code/coursevibecode/README.md), чтобы его навигация тоже была GitHub-friendly

**TODO 2. Завершить книгу по Codex**
- Создать [02-codex-task-design.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/02-codex-task-design.md)
- Тема: как ставить задачи Codex так, чтобы он не угадывал лишнего
- Внутри: плохие и хорошие запросы, scope, expected result, ограничения, проверка понимания

- Создать [03-codex-project-memory.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/03-codex-project-memory.md)
- Тема: постоянные инструкции, `AGENTS.md`, память проекта
- Внутри: где лежит файл, как создать, что туда писать, как это влияет на ответы агента

- Создать [04-codex-settings-and-safety.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/04-codex-settings-and-safety.md)
- Тема: настройки, разрешения, безопасные границы, локальный и облачный режимы
- Внутри: где это находится, что реально менять новичку, чего не трогать на старте

- Создать [05-codex-first-edits-and-checkpoints.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/05-codex-first-edits-and-checkpoints.md)
- Тема: первые правки, как ограничивать область изменений, как проверять результат, как делать точки возврата

- Создать [06-codex-repeatable-workflows.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/06-codex-repeatable-workflows.md)
- Тема: переход от разовых запросов к повторяемому рабочему процессу
- Внутри: шаблоны запросов, порядок “обзор -> план -> изменение -> проверка”, типовые сценарии

- Создать [07-codex-autonomy-and-reliability.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/07-codex-autonomy-and-reliability.md)
- Тема: как повышать самостоятельность агента без роста хаоса
- Внутри: уровни автономности, какие задачи можно делегировать, какие нельзя

- Создать [08-codex-agent-operating-system.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/08-codex-agent-operating-system.md)
- Тема: переход к собственной системе работы с агентом
- Внутри: baseline, project rules, preflight, контроль качества простым языком

- Создать [09-codex-agent-organization.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/09-codex-agent-organization.md)
- Тема: как из работы с одним агентом вырастает агентная организация
- Внутри: роли, маршруты задач, контроль человека, когда это уже имеет смысл

**TODO 3. Собрать книгу по Claude Code**
- Создать [01-claude-code-first-contact.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/claude-code-book/01-claude-code-first-contact.md)
- Создать [02-claude-code-task-design.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/claude-code-book/02-claude-code-task-design.md)
- Создать [03-claude-code-project-memory.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/claude-code-book/03-claude-code-project-memory.md)
- Создать [04-claude-code-settings-and-permissions.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/claude-code-book/04-claude-code-settings-and-permissions.md)
- Создать [05-claude-code-first-edits-and-checkpoints.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/claude-code-book/05-claude-code-first-edits-and-checkpoints.md)
- Создать [06-claude-code-repeatable-workflows.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/claude-code-book/06-claude-code-repeatable-workflows.md)
- Создать [07-claude-code-autonomy-and-reliability.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/claude-code-book/07-claude-code-autonomy-and-reliability.md)
- Создать [08-claude-code-agent-operating-system.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/claude-code-book/08-claude-code-agent-operating-system.md)
- Создать [09-claude-code-agent-organization.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/claude-code-book/09-claude-code-agent-organization.md)

**TODO 4. Привести все главы к единому учебному шаблону**
- В начале каждой главы фиксировать аудиторию
- В начале каждой главы объяснять, что человек сможет после нее
- В каждой главе давать пошаговые действия без скрытых интерфейсных предположений
- В каждой главе добавлять хорошие и плохие примеры запросов
- В каждой главе добавлять блок “частые ошибки”
- В каждой главе добавлять практическое упражнение
- В каждой главе добавлять словарь терминов
- В конце каждой главы оставлять справочные ссылки, но не опирать на них понимание

**TODO 5. Сделать единый редакторский проход**
- Проверить, что терминология не уезжает в язык разработчиков
- Проверить, что англоязычные слова оставлены только там, где без них нельзя
- Проверить, что каждый интерфейсный шаг объяснен буквально
- Проверить, что нет скачков сложности между главами
- Проверить, что одни и те же понятия объясняются одинаково в Codex и Claude Code
- Убрать дубли, где главы будут повторять друг друга слишком сильно

**TODO 6. Подготовить GitHub-версию структуры**
- Проверить, что все новые `.md` видны в `git status`
- Проверить, что все нужные файлы действительно отслеживаются git
- Проверить, что внутренние ссылки работают как относительные ссылки GitHub
- Проверить, что при открытии папки `2_lessons` GitHub показывает `README.md`
- Проверить, что при открытии `codex-book` и `claude-code-book` GitHub показывает оглавление раздела
- При необходимости добавить еще один короткий навигационный блок в корневой [README.md](/Users/alexeykrolmini/Code/coursevibecode/README.md)

**TODO 7. Рабочий порядок выполнения**
1. Сначала закончить всю книгу по Codex
2. После каждой новой главы обновлять [README.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/README.md) и [COURSE-INDEX.md](/Users/alexeykrolmini/Code/coursevibecode/COURSE-INDEX.md)
3. После завершения Codex сделать короткий выравнивающий проход по всей книге
4. Потом начать книгу по Claude Code
5. После завершения Claude Code сделать единый проход по всей второй линии уроков
6. В конце сделать отдельный GitHub-проход по ссылкам, индексам и структуре

**Что я считаю ближайшим следующим шагом**
- Писать [02-codex-task-design.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/02-codex-task-design.md)

Если хочешь, следующим сообщением я превращу этот план в короткий production-backlog с приоритетами `P1/P2/P3`.

# Что нужно?

Я хочу понять, что надо сделать и настроить в твоих настройках, чтобы ты мог выполнить всё. План автономно без пауз. Где конкретно надо что настроить?

Да. Чтобы я мог идти **длинным автономным проходом без пауз**, нужно настроить не одну вещь, а **4 слоя**:

1. убрать технические паузы;
2. зафиксировать доверие и границы доступа;
3. записать проектные правила так, чтобы мне не приходилось спрашивать;
4. если нужна работа “пока тебя нет”, включить облачный режим.

У тебя уже часть сделана.

**Что уже настроено**
Я проверил:
- [config.toml](/Users/alexeykrolmini/.codex/config.toml)
- [AGENTS.md](/Users/alexeykrolmini/Code/coursevibecode/AGENTS.md)

Сейчас уже есть:
- `model = "gpt-5.4"`
- `model_reasoning_effort = "xhigh"`
- `approval_policy = "never"`
- проект `/Users/alexeykrolmini/Code/coursevibecode` уже `trusted`

Это значит: **паузы из-за approval у тебя в основном уже сняты**.

Проблема теперь не в approvals, а в двух вещах:
- не зафиксирован явный `sandbox_mode`
- в проекте нет нормальной авторской инструкции под эту задачу; текущий [AGENTS.md](/Users/alexeykrolmini/Code/coursevibecode/AGENTS.md) описывает framework adapter, а не правила написания курса

**Что надо настроить обязательно**

**1. Явно задать sandbox**
Сейчас у тебя `approval_policy = "never"`, но `sandbox_mode` в user config явно не задан. Для предсказуемой автономной работы это надо зафиксировать.

Официально Codex поддерживает:
- `read-only`
- `workspace-write`
- `danger-full-access`

И отдельно для `workspace-write` можно включить сеть (`sandbox_workspace_write.network_access = true`). Источник: [Config basics](https://developers.openai.com/codex/config-basic), [Config reference](https://developers.openai.com/codex/config-reference).

Я рекомендую так:

Глобально, в [config.toml](/Users/alexeykrolmini/.codex/config.toml):
```toml
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
approval_policy = "never"
sandbox_mode = "workspace-write"
sandbox_workspace_write.network_access = true

[projects."/Users/alexeykrolmini/Code/coursevibecode"]
trust_level = "trusted"
```

Почему так:
- глобально не надо давать полный доступ ко всей машине;
- для обычной автономной работы по проекту этого хватает.

**2. Сделать project override именно для этого репозитория**
Если хочешь, чтобы именно в `coursevibecode` я мог работать максимально свободно, создай файл:
- [.codex/config.toml](/Users/alexeykrolmini/Code/coursevibecode/.codex/config.toml)

И положи туда:
```toml
approval_policy = "never"
sandbox_mode = "danger-full-access"
```

Это даст максимум автономии именно в этом проекте.

Если хочешь чуть безопаснее:
```toml
approval_policy = "never"
sandbox_mode = "workspace-write"
sandbox_workspace_write.network_access = true
```

Практически:
- `workspace-write` — хороший рабочий режим для курса
- `danger-full-access` — только если ты реально хочешь “не тормозить вообще” и доверяешь репозиторию полностью

Официально project config загружается только для trusted-проектов. Источник: [Config basics](https://developers.openai.com/codex/config-basic).

**3. Сузить trust scope**
У тебя сейчас в [config.toml](/Users/alexeykrolmini/.codex/config.toml) есть слишком широкий trust:
- `[projects."/Users/alexeykrolmini"] trust_level = "trusted"`

Это лишнее и рискованно.

Я рекомендую:
- оставить trusted только для конкретных нужных репозиториев
- удалить trust на весь home directory

То есть **оставить**:
```toml
[projects."/Users/alexeykrolmini/Code/coursevibecode"]
trust_level = "trusted"
```

И **убрать**:
```toml
[projects."/Users/alexeykrolmini"]
trust_level = "trusted"
```

**4. Добавить нормальные project instructions под книгу**
Это сейчас главный недостающий слой.

По официальной логике Codex читает `AGENTS.md` до начала работы и умеет наслаивать инструкции: global -> repo -> более близкие папки. Источник: [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md).

Значит, тебе нужно не просто root [AGENTS.md](/Users/alexeykrolmini/Code/coursevibecode/AGENTS.md), а **узкий файл ближе к рабочей зоне**, например:
- [AGENTS.md](/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/AGENTS.md)

Именно туда надо записать правила этой задачи.

Минимум, что там должно быть:
```md
# Codex Book Instructions

## Audience
- Readers are non-technical domain experts.
- Explain everything in plain Russian.
- Every interface action must be described step by step.

## Output Rules
- One chapter = one file.
- Do not expand old chapter files indefinitely.
- After each new chapter, update:
  - COURSE-INDEX.md
  - 2_lessons/codex-book/README.md

## Style
- This is not an outline.
- Write full, self-sufficient chapters.
- Every chapter must include:
  - who it is for
  - practical steps
  - common mistakes
  - exercise
  - glossary

## GitHub Rules
- Use relative markdown links inside the repository.
- Do not use local absolute links in GitHub-facing docs.

## Autonomy
- Continue through P1 tasks without pausing.
- Ask only if a decision changes course structure, chapter order, or publication policy.
```

Это резко уменьшит число пауз “по смыслу”.

**5. Добавить backlog-файл, чтобы я видел очередь без вопросов**
Нужен еще один файл:
- `/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/BACKLOG.md`

Туда надо положить:
- список глав
- статус каждой главы
- приоритет
- правило остановки

Пример:
```md
# Codex Book Backlog

## P1
- [ ] 02-codex-task-design.md
- [ ] 03-codex-project-memory.md
- [ ] 04-codex-settings-and-safety.md
- [ ] 05-codex-first-edits-and-checkpoints.md

## P2
- [ ] 06-codex-repeatable-workflows.md
- [ ] 07-codex-autonomy-and-reliability.md
- [ ] 08-codex-agent-operating-system.md
- [ ] 09-codex-agent-organization.md

## Working Rule
- Finish all P1 chapters before stopping.
- After each chapter update README and COURSE-INDEX.
- Do not ask for confirmation between P1 chapters unless blocked.
```

Без такого файла автономность всегда хуже, потому что мне приходится держать очередь только в диалоге.

**6. Если хочешь реальную фоновую работу без открытой локальной сессии**
Тогда уже недостаточно локальных настроек.

Нужен **Codex web / cloud**:
- подключить GitHub аккаунт
- настроить environment
- запускать фоновые задачи в облаке

Официально Codex web умеет работать в фоне и параллельно в своем cloud environment. Источник: [Codex web](https://developers.openai.com/codex/cloud).

Это нужно, если ты хочешь:
- закрыть ноутбук
- уйти
- вернуться позже к готовым результатам

**Где конкретно это настраивать**
- Глобальные настройки: [config.toml](/Users/alexeykrolmini/.codex/config.toml)
- Настройки только для этого проекта: [config.toml](/Users/alexeykrolmini/Code/coursevibecode/.codex/config.toml)
- Общие project instructions: [AGENTS.md](/Users/alexeykrolmini/Code/coursevibecode/AGENTS.md)
- Узкие инструкции именно для книги: `/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/AGENTS.md`
- Очередь работы: `/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/BACKLOG.md`

**Что я бы рекомендовал как минимально достаточный набор**
Сделать ровно это:

1. В [config.toml](/Users/alexeykrolmini/.codex/config.toml)
- оставить `approval_policy = "never"`
- добавить `sandbox_mode = "workspace-write"`
- добавить `sandbox_workspace_write.network_access = true`

2. Удалить широкий trust на `/Users/alexeykrolmini`

3. Создать [config.toml](/Users/alexeykrolmini/Code/coursevibecode/.codex/config.toml)
- либо `workspace-write + network_access`
- либо `danger-full-access`, если хочешь максимум автономии

4. Создать `2_lessons/codex-book/AGENTS.md`

5. Создать `2_lessons/codex-book/BACKLOG.md`

**Итог**
Если сделать это, то:
- технические паузы почти исчезнут;
- смысловые паузы сильно сократятся;
- я смогу идти по главам подряд без постоянных подтверждений;
- останавливаться буду только там, где реально нужен выбор автора, а не из-за недонастроенной среды.

Источники:
- [Config basics](https://developers.openai.com/codex/config-basic)
- [Configuration reference](https://developers.openai.com/codex/config-reference)
- [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [Codex CLI features](https://developers.openai.com/codex/cli/features)
- [Codex web](https://developers.openai.com/codex/cloud)

Если хочешь, следующим сообщением я могу **сам сразу подготовить для тебя все 3 файла**:
1. project `.codex/config.toml`
2. `2_lessons/codex-book/AGENTS.md`
3. `2_lessons/codex-book/BACKLOG.md`