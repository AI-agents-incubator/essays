> Версия файла: `v1.1`
> Дата версии: `2026-03-16`
> Тип документа: `локальный process-гайд`
> Источник и актуальность:
> - основан на официальной документации OpenAI по Codex и связанным tool-страницам;
> - у сайтов документации обычно нет удобного публичного номера версии страницы;
> - поэтому в этом репозитории практическим эквивалентом версии источника считается дата проверки;
> - текущий ориентир актуальности источников: `по состоянию на 16 марта 2026`.
>

Проверил официальные документы OpenAI на `16 марта 2026`. Ниже практический гайд по тому, как устроены `subagents`, `skills`, `tools`, автономность, веб-доступ и что именно управляет поведением Codex.

**Короткий вывод**
- Да, субагенты в актуальном Codex уже официально есть и включены в текущих релизах по умолчанию, но Codex должен запускать их только когда ты явно просишь о делегировании или параллельной агентной работе.  
- Да, skills тоже официально есть и это уже отдельный механизм расширения поведения агента.  
- Да, инструменты и внешние возможности подключаются через built-in tools и MCP.  
- Да, автономность настраивается отдельно через `sandbox`, `approval policy`, `rules`, `web_search`, `MCP`, `AGENTS.md`, `config.toml`.  
- Для полноценного “открыть страницу, кликнуть, ввести текст, заполнить форму” есть два официальных пути:
  - `Computer use` в OpenAI API
  - browser MCP tools в Codex, например `Playwright` или `Chrome DevTools`
- В текущей конкретной сессии мои реальные возможности зависят не только от продукта Codex вообще, но и от того, какие инструменты включены именно в этот runtime.

**1. Базовая модель управления Codex**
Нужно мыслить так:

1. `Model`  
Это базовый мозг: какой именно Codex/GPT-модель используется и с каким reasoning effort.

2. `Instructions`  
Это правила и стиль поведения:
- глобальные инструкции
- `AGENTS.md`
- project-scoped инструкции
- custom instructions

3. `Tools`  
Это то, чем агент реально может пользоваться:
- shell
- web search
- apply patch
- MCP servers
- file search
- computer use
- custom functions

4. `Runtime controls`  
Это границы автономности:
- `sandbox_mode`
- `approval_policy`
- `network_access`
- `rules`

5. `Workflow extensions`  
Это higher-level механика:
- `subagents`
- `skills`
- `automations`
- `worktrees`

Официальный обзор Codex app: [Codex app](https://developers.openai.com/codex/app)

**2. Что такое субагенты**
По официальной документации, Codex умеет запускать специализированных агентов параллельно и потом собирать их результаты в один ответ. Это удобно для:
- codebase exploration
- review
- triage
- tests/log analysis
- многосоставных задач, которые естественно разбиваются на независимые куски

Официальные страницы:
- [Subagents](https://developers.openai.com/codex/subagents)
- [Subagent concepts](https://developers.openai.com/codex/concepts/subagents)

Ключевые правила:
- субагенты не должны стартовать автоматически без явной просьбы пользователя о делегировании или parallel agent work;
- subagent workflows стоят дороже по токенам, потому что каждый агент выполняет свою собственную model/tool работу;
- current Codex releases enable subagent workflows by default;
- активность субагентов сейчас официально видна в `Codex app` и `CLI`.

Что важно practically:
- главный агент держит требования, решения и финальную сборку ответа;
- субагенты лучше всего использовать на sidecar-задачи:
  - исследование
  - тесты
  - документация
  - браузерная диагностика
- параллельные write-heavy workflows требуют осторожности, потому что они повышают риск конфликтов.

**3. Built-in subagents и custom agents**
Из коробки у Codex есть built-in агенты:
- `default`
- `worker`
- `explorer`

Официально это задокументировано здесь: [Subagents](https://developers.openai.com/codex/subagents)

Custom agents определяются TOML-файлами:
- personal scope: `~/.codex/agents`
- project scope: `.codex/agents`

Типичная форма custom agent:

```toml
name = "reviewer"
description = "PR reviewer focused on correctness, security, and missing tests."
model = "gpt-5.4"
model_reasoning_effort = "high"
sandbox_mode = "read-only"

developer_instructions = """
Review code like an owner.
Prioritize correctness, security, behavior regressions, and missing test coverage.
"""
```

Что можно задавать агенту:
- `model`
- `model_reasoning_effort`
- `sandbox_mode`
- `mcp_servers`
- `skills.config`
- `developer_instructions`

Есть и глобальные лимиты подагентов:
- `agents.max_threads`
- `agents.max_depth`
- `agents.job_max_runtime_seconds`

**4. Что такое skills**
Skills — это способ дать Codex новую специализированную компетенцию без переписывания базового поведения агента.

Официальная документация:
- [Agent Skills](https://developers.openai.com/codex/skills)

Ключевая идея:
- skill — это директория с `SKILL.md`
- опционально там могут быть `scripts`, `references`, `assets`
- Codex использует progressive disclosure:
  - сначала видит только metadata skill
  - полный `SKILL.md` читает только когда реально решает skill использовать

Это важно, потому что skills не забивают контекст сразу.

Skill можно активировать двумя путями:
1. Явно:
- через mention skill в prompt
- в CLI/IDE через `/skills` или `$skill-name`

2. Неявно:
- Codex сам решает использовать skill, если task совпадает с `description`

Минимальный skeleton:

```md
---
name: my-skill
description: Explain exactly when this skill should and should not trigger.
---

Skill instructions for Codex to follow.
```

Где хранить:
- user/global
- repo/project
- system/admin layers

Их можно включать и выключать через `config.toml`:

```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

**5. Что такое MCP**
MCP — это основной путь подключить к Codex новые внешние инструменты и контекст.

Официальная документация:
- [Model Context Protocol](https://developers.openai.com/codex/mcp)

MCP нужен, чтобы дать Codex доступ, например, к:
- документации
- браузеру
- Figma
- GitHub
- Sentry
- Chrome DevTools
- Playwright

Поддерживаемые типы MCP:
- `STDIO servers`
- `Streamable HTTP servers`

Что можно настраивать:
- `command`
- `args`
- `env`
- `cwd`
- `url`
- `bearer_token_env_var`
- `http_headers`
- `enabled_tools`
- `disabled_tools`
- `required`
- `startup_timeout_sec`
- `tool_timeout_sec`

CLI-путь:
```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

Конфиг-путь:
```toml
[mcp_servers.chrome_devtools]
url = "http://localhost:3000/mcp"
enabled_tools = ["open", "screenshot"]
startup_timeout_sec = 20
tool_timeout_sec = 45
enabled = true
```

Это очень важный момент: в Codex полноценный browser control чаще приходит не “сам по себе”, а через MCP browser tools.

**6. Что такое `AGENTS.md`**
`AGENTS.md` — это проектный слой инструкций для Codex.

Официальная документация:
- [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)

Codex читает `AGENTS.md` до начала работы и собирает instruction chain по слоям.

Порядок discovery:
1. Global scope:
- `~/.codex/AGENTS.override.md`
- или `~/.codex/AGENTS.md`

2. Project scope:
- от project root до текущей директории
- в каждой папке смотрит `AGENTS.override.md`, потом `AGENTS.md`

3. Merge order:
- от корня вниз
- более близкие к cwd инструкции перекрывают более общие

Практически именно здесь ты задаёшь:
- стиль работы
- code review policy
- запреты
- форматы ответов
- как пользоваться skills
- когда делегировать subagents
- как обращаться с git
- проектные соглашения

Если хочешь управлять мной предметно, `AGENTS.md` — один из главных рычагов.

**7. Что такое `config.toml`**
Это главный runtime-конфиг Codex.

Официальная документация:
- [Config basics](https://developers.openai.com/codex/config-basic)
- [Configuration Reference](https://developers.openai.com/codex/config-reference)

Главные пути:
- user-level: `~/.codex/config.toml`
- project-level: `.codex/config.toml`

Precedence:
1. CLI flags / `--config`
2. profile values
3. project config files
4. user config
5. system config
6. built-in defaults

Главные поля, которые реально важны для управления автономностью:
- `model`
- `model_reasoning_effort`
- `approval_policy`
- `sandbox_mode`
- `web_search`
- `mcp_servers.*`
- `skills.config`
- `shell_environment_policy`
- `log_dir`

Базовый пример:

```toml
model = "gpt-5.4"
model_reasoning_effort = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"

[sandbox_workspace_write]
network_access = false
```

**8. Approval policy и sandbox**
Это главный блок управления автономной работой.

Официальная документация:
- [Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security)

Официальная модель состоит из двух слоёв:
1. `sandbox mode`
- что технически можно делать

2. `approval policy`
- когда Codex обязан остановиться и спросить разрешение

Основные sandbox modes:
- `read-only`
- `workspace-write`
- `danger-full-access`

Основные approval policies:
- `untrusted`
- `on-request`
- `never`

Ключевые официальные режимы:
- `--full-auto`
  - это shorthand для `workspace-write + on-request`
  - агент может читать, редактировать и запускать команды в workspace автоматически
  - но попросит approval для выхода за workspace или сети
- `--yolo`
  - это `dangerously-bypass-approvals-and-sandbox`
  - без sandbox и без approvals
  - docs прямо помечают это как elevated risk / not recommended

Практический смысл:
- `read-only` — режим анализа и планирования
- `workspace-write` — нормальный рабочий режим
- `danger-full-access` — только если ты точно понимаешь последствия

**9. Rules**
Если хочется не просто “разрешать/запрещать всё”, а управлять конкретными командами, нужны rules.

Официальная документация:
- [Rules](https://developers.openai.com/codex/rules)

Rules позволяют контролировать, какие команды Codex может запускать вне sandbox.

Пример:

```rules
prefix_rule(
  pattern = ["gh", "pr", "view"],
  decision = "prompt",
  justification = "Viewing PRs is allowed with approval",
  match = [
    "gh pr view 7888",
    "gh pr view --repo openai/codex"
  ]
)
```

Возможные `decision`:
- `allow`
- `prompt`
- `forbidden`

Это один из самых полезных способов безопасно автоматизировать работу, не давая агенту unrestricted shell power.

**10. Web search и веб-доступ**
Надо различать две вещи:

1. `Web search` в Codex  
Это доступ модели к поиску и веб-результатам.

Официальная документация:
- [Web search](https://platform.openai.com/docs/guides/tools-web-search)
- [Config basics](https://developers.openai.com/codex/config-basic)

В local Codex по docs:
- по умолчанию `web_search = "cached"`
- `cached` использует OpenAI-maintained cache/index
- `live` получает более свежие веб-результаты
- `disabled` выключает web search

Это снижает риск prompt injection по сравнению с полностью live browsing, но docs всё равно советуют считать веб-результаты недоверенными.

2. `Agent internet access`  
Это уже не просто поиск, а сетевой доступ агента во время agent phase, особенно в cloud environments.

Официальная документация:
- [Agent internet access](https://developers.openai.com/codex/cloud/internet-access)

Там OpenAI рекомендует:
- включать интернет только когда нужно
- ограничивать домены allowlist’ом
- ограничивать HTTP methods
- по возможности оставлять только `GET/HEAD/OPTIONS`

Это особенно важно из-за prompt injection и возможной exfiltration.

**11. Может ли Codex открывать страницы, нажимать кнопки и заполнять формы**
Да, но тут есть важное разделение.

1. В Codex как продукте  
Это возможно через browser-oriented tools, обычно через MCP:
- `Playwright`
- `Chrome DevTools`

Официально MCP docs прямо говорят, что через MCP можно дать Codex доступ к браузеру и developer tools:  
[Model Context Protocol](https://developers.openai.com/codex/mcp)

2. В OpenAI API в целом  
Есть отдельный официальный инструмент:
- [Computer use](https://platform.openai.com/docs/guides/tools-computer-use)

Он предназначен именно для:
- clicking
- typing
- scrolling
- form filling
- browser workflows

То есть да, официальный механизм для “зайти на страницу, нажать кнопку, ввести текст в форму” существует.

3. Но это не означает, что любой конкретный runtime уже умеет всё это прямо сейчас  
Текущая сессия может иметь:
- только web search
- только open/click/find по страницам
- или полноценный browser/computer tool
- или MCP browser server
- или ничего из этого

Поэтому правильный вопрос всегда двухуровневый:
- умеет ли это Codex/OpenAI вообще? `да`
- включено ли это в моей конкретной сессии? `зависит от среды`

**12. Что умею именно я в текущей логике управления**
В любой конкретной сессии мои реальные возможности определяются так:

1. Системные и developer instructions  
Они могут прямо разрешить или запретить:
- subagents
- tool calls
- internet
- file editing
- approvals

2. Набор реально подключённых tools  
Если tool не подключён, я не смогу им пользоваться, даже если он существует в продукте вообще.

3. Среда исполнения  
Например:
- sandbox
- доступ к сети
- доступ к локальным файлам
- есть ли browser MCP
- есть ли computer use tool

4. Project instructions  
`AGENTS.md`, `rules`, local policy

То есть “функция существует в Codex” и “я могу сделать это прямо сейчас в этой сессии” — это не одно и то же.

**13. Практическая схема управления Codex**
Если ты хочешь управлять поведением системно, вот правильный стек.

1. `~/.codex/config.toml`
- дефолтная модель
- approval policy
- sandbox
- web search
- MCP servers
- skill toggles

2. `AGENTS.md`
- проектные правила
- стиль
- git policy
- формат ответов
- как вести review
- когда делегировать

3. `.codex/agents/*.toml`
- custom subagents
- исследователь
- reviewer
- browser debugger
- docs researcher

4. `.agents/skills/*/SKILL.md`
- навыки под повторяющиеся workflows

5. `rules`
- точечный контроль опасных команд

6. `automations`
- фоновые recurring tasks в app

**14. Рекомендуемая стратегия настройки**
Я бы советовал такой режим.

1. Для обычной разработки
```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"

[sandbox_workspace_write]
network_access = false
```

2. Для исследовательского безопасного режима
```toml
approval_policy = "on-request"
sandbox_mode = "read-only"
web_search = "cached"
```

3. Для почти полного автомата, но ещё без безумия
```toml
approval_policy = "untrusted"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

4. `--yolo` / `danger-full-access`
- только для изолированных сред
- только когда ты осознанно принимаешь риск

**15. Automations**
Если хочешь recurring background work, это уже отдельный официальный слой.

Официальная документация:
- [Automations](https://developers.openai.com/codex/app/automations)

Что важно:
- automations run in background in the Codex app
- app must be running
- project must be available on disk
- в git-репозиториях можно выбрать:
  - local project
  - отдельный `worktree`
- automations используют твои default sandbox settings
- automation can explicitly call a skill using `$skill-name`
- docs рекомендуют сначала прогонять prompt вручную, а уже потом ставить schedule

**16. Что тебе полезно сделать practically**
Если твоя цель — “полноценно этим управлять”, я бы шёл так:

1. Завести аккуратный `~/.codex/config.toml`
- с 2-3 профилями:
  - `readonly`
  - `default`
  - `full_auto`

2. Сделать глобальный `~/.codex/AGENTS.md`
- общие правила стиля и безопасности

3. В каждом важном проекте иметь свой `AGENTS.md`
- project-specific constraints

4. Вынести повторяющиеся workflows в skills
- docs lookup
- release prep
- project audit
- browser QA
- repo triage

5. Для сложных работ настроить 2-4 custom subagents
- `explorer`
- `reviewer`
- `docs_researcher`
- `browser_debugger`

6. Подключить MCP servers
- docs
- browser
- GitHub
- Figma
- Sentry

7. Ограничить опасные команды через `rules`

**17. Самые полезные официальные ссылки**
- Codex app: [https://developers.openai.com/codex/app](https://developers.openai.com/codex/app)
- Codex app features: [https://developers.openai.com/codex/app/features](https://developers.openai.com/codex/app/features)
- Codex app settings: [https://developers.openai.com/codex/app/settings](https://developers.openai.com/codex/app/settings)
- Subagents: [https://developers.openai.com/codex/subagents](https://developers.openai.com/codex/subagents)
- Subagent concepts: [https://developers.openai.com/codex/concepts/subagents](https://developers.openai.com/codex/concepts/subagents)
- Skills: [https://developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)
- AGENTS.md: [https://developers.openai.com/codex/guides/agents-md](https://developers.openai.com/codex/guides/agents-md)
- MCP: [https://developers.openai.com/codex/mcp](https://developers.openai.com/codex/mcp)
- Rules: [https://developers.openai.com/codex/rules](https://developers.openai.com/codex/rules)
- Config basics: [https://developers.openai.com/codex/config-basic](https://developers.openai.com/codex/config-basic)
- Config reference: [https://developers.openai.com/codex/config-reference](https://developers.openai.com/codex/config-reference)
- Agent approvals & security: [https://developers.openai.com/codex/agent-approvals-security](https://developers.openai.com/codex/agent-approvals-security)
- Automations: [https://developers.openai.com/codex/app/automations](https://developers.openai.com/codex/app/automations)
- Agent internet access: [https://developers.openai.com/codex/cloud/internet-access](https://developers.openai.com/codex/cloud/internet-access)
- Using tools: [https://platform.openai.com/docs/guides/tools](https://platform.openai.com/docs/guides/tools)
- Web search tool: [https://platform.openai.com/docs/guides/tools-web-search](https://platform.openai.com/docs/guides/tools-web-search)
- Computer use tool: [https://platform.openai.com/docs/guides/tools-computer-use](https://platform.openai.com/docs/guides/tools-computer-use)

Если хочешь, следующим сообщением я могу сделать уже совсем прикладную вещь:
1. готовый шаблон `~/.codex/config.toml`
2. готовый шаблон глобального `AGENTS.md`
3. набор из 3-4 полезных custom subagents
4. набор из 3-5 базовых skills
5. безопасный профиль для твоей машины под твой стиль работы
