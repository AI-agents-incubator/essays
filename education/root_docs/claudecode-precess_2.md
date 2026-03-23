> Версия файла: `v1.1`
> Дата версии: `2026-03-16`
> Тип документа: `локальный process-гайд`
> Источник и актуальность:
> - основан на официальной документации Anthropic по Claude Code;
> - у сайта документации нет стабильного публичного номера версии страницы;
> - поэтому в этом репозитории практическим эквивалентом версии источника считается дата проверки;
> - текущий ориентир актуальности источников: `по состоянию на 16 марта 2026`.
>

Проверил по официальной документации Anthropic на `16 марта 2026`. Ниже уже не просто список ссылок, а практический гайд по тому, как в `Claude Code` устроены `subagents`, `tools`, `permissions`, `hooks`, `MCP` и автономная работа.

Часть ниже — это прямое изложение документации. Где я делаю выводы о том, как это лучше применять на практике, я буду явно писать `мой вывод`.

**1. Главная модель Claude Code**
`Claude Code` — это не “один чат в терминале”, а агентная оболочка вокруг модели. По официальному overview, она умеет:
- читать кодовую базу;
- редактировать файлы;
- запускать команды;
- работать через terminal, IDE, desktop app и browser;
- подключать внешние инструменты и источники данных через `MCP`;
- запускать специализированных субагентов под отдельные задачи.  
Источник: [Overview](https://code.claude.com/docs/en/overview)

`Мой вывод`: Claude Code лучше понимать как систему из нескольких слоёв:
- модель;
- локальные инструменты;
- память и инструкции;
- policy layer;
- расширения;
- execution surfaces.

То есть управлять надо не “Claude целиком”, а каждым слоем отдельно.

**2. Чем реально управляют поведение Claude Code**
Есть три разных типа управления.

`Soft guidance`
- `CLAUDE.md`
- `.claude/rules/*.md`
- `skills`
- prompt’ы subagents

Это влияет на поведение, но не является жёстким запретом.

`Hard control`
- `.claude/settings.json`
- `.claude/settings.local.json`
- `~/.claude/settings.json`
- managed settings
- permission rules
- hooks
- sandbox

Это уже реальное ограничение возможностей.

`Execution mode`
- интерактивный REPL
- headless mode
- SDK
- GitHub Actions
- API-level `computer use`

Это определяет, где и как агент выполняется.

**3. Где лежат основные файлы управления**
По официальным docs:

`Settings`
- `~/.claude/settings.json`
- `.claude/settings.json`
- `.claude/settings.local.json`

`Subagents`
- `~/.claude/agents`
- `.claude/agents`

`Skills`
- `~/.claude/skills/<skill-name>/SKILL.md`
- `.claude/skills/<skill-name>/SKILL.md`

`Project memory / instructions`
- `~/.claude/CLAUDE.md`
- `../../CLAUDE.md`
- `../../.claude/CLAUDE.md`

`MCP`
- user/local state в `~/.claude.json`
- project-scoped servers в `.mcp.json`  
Источники: [Settings](https://code.claude.com/docs/en/settings), [Memory](https://code.claude.com/docs/en/memory), [Subagents](https://code.claude.com/docs/en/sub-agents), [Skills](https://code.claude.com/docs/en/slash-commands), [MCP](https://code.claude.com/docs/en/mcp)

**4. Приоритет настроек**
Официальный порядок precedence в Claude Code такой:
1. managed settings
2. command line arguments
3. `.claude/settings.local.json`
4. `.claude/settings.json`
5. `~/.claude/settings.json`  
Источник: [Settings](https://code.claude.com/docs/en/settings)

Это очень важный момент.  
`Мой вывод`: если хочешь по-настоящему управлять Claude Code, главный рычаг — не prompt, а именно правильное распределение правил по этим уровням.

Ещё один практический вывод после реального инцидента:
`.claude/settings.local.json` нельзя считать harmless-файлом "для мелких локальных настроек".
Если пользователь бездумно одобряет команды с inline creds через `Allow`, local settings layer может накопить secret-bearing command strings.

Поэтому operational rule должен быть таким:

- не разрешать команды, где секрет уже лежит прямо в строке;
- держать реальные креды отдельно;
- периодически просматривать local permission-layer;
- защищать `.claude/settings.local.json` как минимум от попадания в git.

**5. Что такое subagents в Claude Code**
По docs, subagents — это специализированные AI-ассистенты, которые:
- работают в отдельном context window;
- имеют свой system prompt;
- могут иметь свой набор tools;
- имеют независимые permissions;
- получают задачу от главного Claude и возвращают результат.  
Источник: [Subagents](https://code.claude.com/docs/en/sub-agents)

Claude выбирает subagent на основе его `description`. Поэтому качество `description` критично.

Есть:
- built-in subagents;
- user subagents;
- project subagents;
- session-only subagents через CLI JSON.

Из docs:
- project subagents: `.claude/agents`
- user subagents: `~/.claude/agents`
- CLI-defined subagents существуют только в текущей сессии.  
Источник: [Subagents](https://code.claude.com/docs/en/sub-agents), [CLI reference](https://code.claude.com/docs/en/cli-reference)

**6. Как устроен файл subagent**
Subagent — это markdown-файл с YAML frontmatter. В frontmatter задаются:
- `name`
- `description`
- `tools`
- `disallowedTools`
- `model`
- `permissionMode`
- `maxTurns`
- `skills`

Ключевые нюансы из docs:
- `name` и `description` обязательны;
- если `tools` не указать, subagent унаследует все tools;
- `skills` не наследуются от родительского диалога автоматически;
- subagent получает свой prompt, а не весь internal system prompt Claude Code.  
Источник: [Subagents](https://code.claude.com/docs/en/sub-agents)

Практический минимальный пример:

```md
---
name: code-reviewer
description: Review changed code for correctness, risks, and missing tests.
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: plan
---

Review the current changes.
Focus on correctness, regressions, security, and missing tests.
Return findings ordered by severity.
```

**7. Когда subagents реально полезны**
Официально docs рекомендуют subagents для:
- verbose tasks;
- параллельных независимых исследований;
- жёсткого ограничения инструментов;
- self-contained work, которое может вернуться как summary.  
Источник: [Subagents](https://code.claude.com/docs/en/sub-agents)

Из важных ограничений:
- subagents могут работать в foreground и background;
- background subagents получают approvals заранее;
- если у background subagent не хватает разрешений, его можно потом перевести в foreground;
- subagents не могут порождать другие subagents;
- subagent можно resume, его transcript хранится отдельно;
- compaction главного диалога не уничтожает transcript subagent.  
Источник: [Subagents](https://code.claude.com/docs/en/sub-agents)

`Мой вывод`: subagents — это не просто “второй чат”. Это лучший механизм для:
- изоляции шумных задач;
- разделения исследований;
- безопасного делегирования с урезанными tool permissions.

**8. Skills: чем они отличаются от subagents**
По docs, skills — это `SKILL.md`, который расширяет возможности Claude Code. Он:
- может вызываться напрямую через `/skill-name`;
- может подхватываться автоматически, если релевантен;
- может включать supporting files и scripts;
- может работать в main context, а не в отдельном контексте subagent.  
Источник: [Skills](https://code.claude.com/docs/en/slash-commands)

Где они живут:
- `~/.claude/skills/...`
- `.claude/skills/...`
- plugin scope
- enterprise scope

Из docs:
- custom commands фактически слиты со skills;
- skill и command с одинаковым именем дают приоритет skill;
- bundled skills могут читать файлы, спавнить parallel agents и адаптироваться к кодовой базе.  
Источник: [Skills](https://code.claude.com/docs/en/slash-commands)

`Мой вывод`:
- `skill` — когда нужен повторяемый workflow или knowledge pack;
- `subagent` — когда нужен отдельный контекст и отдельные permissions;
- `CLAUDE.md` — когда нужна постоянная фоновая инструкция для проекта.

**9. CLAUDE.md, rules и память**
Официально `CLAUDE.md` — это persistent instructions layer. Он может жить:
- в `~/.claude/CLAUDE.md`
- в `../../CLAUDE.md`
- в `../../.claude/CLAUDE.md`  
Источник: [Memory](https://code.claude.com/docs/en/memory)

Критичные нюансы:
- Claude читает `CLAUDE.md` при старте сессии;
- он поднимается вверх по дереву директорий и может брать несколько `CLAUDE.md`;
- можно делать `@imports`;
- external imports требуют approval при первом использовании;
- docs рекомендуют держать `CLAUDE.md` компактным;
- `CLAUDE.md` — это контекст, а не неотменяемая системная политика.  
Источник: [Memory](https://code.claude.com/docs/en/memory)

Особенно важно:
- `CLAUDE.md` подаётся как user-level context после system prompt;
- для system-level поведения Anthropic рекомендует `--append-system-prompt`.  
Источник: [Memory](https://code.claude.com/docs/en/memory), [Settings](https://code.claude.com/docs/en/settings)

Есть ещё `.claude/rules`:
- rules можно раскладывать по файлам;
- они могут быть path-scoped;
- это удобнее для больших проектов, чем раздувать один `CLAUDE.md`.  
Источник: [Memory](https://code.claude.com/docs/en/memory)

**10. Какие инструменты есть у Claude Code**
В settings docs перечислено, что Claude Code работает с набором internal tools для:
- чтения;
- записи;
- редактирования;
- поиска;
- листинга файлов;
- bash-команд;
- web fetch/search;
- orchestration subagents.  
Источник: [Settings](https://code.claude.com/docs/en/settings)

В SDK hooks docs прямо названы built-in tool names, например:
- `Bash`
- `Read`
- `Write`
- `Edit`
- `Glob`
- `Grep`
- `WebFetch`
- `Agent`
и другие. Для MCP формат такой:
- `mcp__<server>__<action>`  
Источник: [Agent SDK hooks](https://platform.claude.com/docs/en/agent-sdk/hooks)

`Мой вывод`: tools — это не абстракция. Именно их имена потом используются:
- в permission rules;
- в hook matchers;
- в allow/deny политике.

**11. Permissions: где начинается настоящая автономность**
В Claude Code permissions задаются через:
- `allow`
- `ask`
- `deny`
- `additionalDirectories`
- `defaultMode`
- `disableBypassPermissionsMode`  
Источник: [Settings](https://code.claude.com/docs/en/settings)

Пример базового безопасного settings:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Bash(curl *)"
    ],
    "ask": [
      "Bash(git push *)",
      "WebFetch"
    ],
    "allow": [
      "Bash(npm test *)",
      "Bash(npm run lint *)"
    ],
    "defaultMode": "acceptEdits"
  }
}
```

В docs есть два важных слоя оценки.

Для Claude Code settings:
- deny rules first
- потом ask
- потом allow
- first matching rule wins  
Источник: [Settings](https://code.claude.com/docs/en/settings)

Для Agent SDK более низкоуровневый runtime order:
- hooks
- deny rules
- permission mode
- allow rules
- `canUseTool` callback  
Источник: [Agent SDK permissions](https://platform.claude.com/docs/en/agent-sdk/permissions)

`Мой вывод`: если нужна controlled autonomy, то мыслить надо так:
- `CLAUDE.md` говорит, как агенту лучше работать;
- `permissions` говорят, что агент вообще может делать;
- `hooks` дают динамический контроль прямо на лету.

**12. Permission modes**
В docs фигурируют режимы:
- `default`
- `acceptEdits`
- `dontAsk`
- `bypassPermissions`
- `plan`  
Источники: [Subagents](https://code.claude.com/docs/en/sub-agents), [Agent SDK permissions](https://platform.claude.com/docs/en/agent-sdk/permissions)

Из документации:
- `acceptEdits` автоодобряет file operations;
- `dontAsk` фактически auto-deny для того, что заранее не разрешено;
- `bypassPermissions` пропускает все permission checks;
- `plan` не исполняет tools, а планирует.  
Источник: [Agent SDK permissions](https://platform.claude.com/docs/en/agent-sdk/permissions)

Критичный нюанс:
- если включён `bypassPermissions`, subagents это наследуют;
- docs отдельно предупреждают, что subagents могут вести себя менее constrained, чем main agent.  
Источник: [Agent SDK permissions](https://platform.claude.com/docs/en/agent-sdk/permissions)

`Мой вывод`: для реальной работы безопасный default — `acceptEdits` или `default`.  
`bypassPermissions` — только для очень контролируемой среды.

**13. Hooks: самый сильный механизм контроля**
Hooks в Claude Code запускаются на событиях lifecycle и tool execution.  
Официально есть события вроде:
- `PreToolUse`
- `PermissionRequest`
- `PostToolUse`
- `PostToolUseFailure`
- `SubagentStart`
- `SubagentStop`
- `Stop`
- `UserPromptSubmit`
- другие session/config events  
Источники: [Hooks](https://code.claude.com/docs/en/hooks), [Agent SDK hooks](https://platform.claude.com/docs/en/agent-sdk/hooks)

Что умеет hook:
- логировать;
- разрешать;
- запрещать;
- просить подтверждение;
- модифицировать tool input;
- добавлять контекст Claude;
- работать через command hook или HTTP hook.  
Источник: [Hooks](https://code.claude.com/docs/en/hooks)

Особенно важен `PreToolUse`:
- он может `allow`, `deny` или `ask`;
- может менять input до исполнения.  
Источник: [Hooks](https://code.claude.com/docs/en/hooks)

`Мой вывод`: если permissions — это firewall по шаблонам, то hooks — это policy engine с логикой.

Пример практического use case:
- разрешать только read-only SQL в Bash;
- блокировать запись в прод-конфиги;
- автоматически запускать formatter после Edit/Write;
- логировать все вызовы `mcp__*`.

**14. Sandbox**
В settings есть отдельный `sandbox` блок. Он контролирует:
- sandboxing bash commands;
- разрешённые write/read paths;
- сетевые домены;
- unix sockets;
- local binding;
- escape hatch для unsandboxed commands.  
Источник: [Settings](https://code.claude.com/docs/en/settings)

Это уже отдельный security boundary, а не просто permission rules.

`Мой вывод`: если работаешь с чувствительным кодом, sandbox надо включать, а `allowUnsandboxedCommands` по возможности запрещать.

**15. MCP: как Claude Code получает новые инструменты**
`MCP` — это официальный способ подключать внешние tools, APIs, DB, docs и сервисы.  
Официально docs покрывают:
- local stdio servers;
- remote HTTP servers;
- remote SSE servers;
- scopes;
- precedence;
- OAuth-authenticated servers;
- MCP prompts as commands;
- MCP resources через `@mentions`.  
Источник: [MCP](https://code.claude.com/docs/en/mcp)

Что особенно полезно:
- MCP prompt может стать slash-командой вида `/mcp__github__list_prs`
- MCP resource можно сослать как `@server:protocol:/resource/path`
- Claude Code сам может выступать как MCP server через `claude mcp serve`  
Источники: [MCP](https://code.claude.com/docs/en/mcp), [Skills / slash commands](https://code.claude.com/docs/en/slash-commands)

`Мой вывод`: MCP — это правильный путь, если хочешь, чтобы Claude Code работал не только с локальными файлами, но и с:
- GitHub;
- Jira;
- Sentry;
- Figma;
- внутренними API;
- БД;
- browser/devtools toolchains.

**16. Автономная работа: как она реально выглядит**
В Claude Code есть несколько уровней автономности.

`Интерактивный агент`
- работаешь в REPL;
- Claude спрашивает approvals;
- может запускать subagents;
- может выполнять tools локально.

`Headless mode`
- `claude -p ...`
- без интерактивного UI;
- годится для scripts и automation;
- можно задавать `--allowedTools`, `--permission-mode`, `--output-format`, `--max-turns`, `--cwd`.  
Источники: [CLI reference](https://code.claude.com/docs/en/cli-reference), [Claude Code SDK / headless](https://docs.anthropic.com/en/docs/claude-code/sdk)

`SDK`
- TypeScript / Python / CLI;
- можно запускать Claude Code как subprocess/agent harness programmatically;
- это уже путь к своим агентным системам и orchestration.  
Источник: [Claude Code SDK](https://docs.anthropic.com/en/docs/claude-code/sdk)

`GitHub Actions`
- Claude Code можно запускать прямо в GitHub Actions;
- есть quickstart через `/install-github-app`;
- нужны repo secrets и GitHub app permissions.  
Источник: [GitHub Actions](https://code.claude.com/docs/en/github-actions)

`Мой вывод`: “автономность” в Claude Code — это не один переключатель, а связка:
- headless/SDK/CI surface;
- tools;
- permissions;
- hooks;
- MCP.

**17. Browser/UI automation и заполнение форм**
Здесь важно разделять две вещи.

`Claude Code`
- умеет web-related operations;
- умеет MCP integration;
- может подключать browser-oriented tooling через MCP.  
Источники: [Overview](https://code.claude.com/docs/en/overview), [MCP](https://code.claude.com/docs/en/mcp)

`Anthropic platform computer use`
- отдельный API-level tool;
- даёт screenshot capture;
- mouse control;
- keyboard input;
- desktop automation;
- требует agent loop, где твое приложение исполняет tool requests Claude в sandboxed environment.  
Источник: [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)

Ключевой нюанс:
- Claude сам “не нажимает кнопки напрямую” магически;
- он запрашивает action;
- твоя среда исполняет action;
- результат возвращается в agent loop.  
Источник: [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)

`Мой вывод`: если тебе нужен настоящий “открыть страницу, кликнуть, ввести текст, пройти форму”, то правильный официальный механизм у Anthropic — это `computer use` или браузерные MCP-инструменты. Это уже не просто vanilla Claude Code prompt.

**18. Security best practices**
Официальные рекомендации Anthropic для Claude Code:
- read-only by default;
- review suggested changes before approval;
- use project-specific permission settings;
- consider devcontainers/VMs for isolation;
- audit permissions through `/permissions`;
- be careful with untrusted content;
- do not blindly trust third-party MCP servers.  
Источник: [Security](https://docs.anthropic.com/en/docs/claude-code/security)

`Мой вывод`: базовая безопасная стратегия такая:
- secrets закрыть через `permissions.deny`;
- сеть ограничить sandbox/MCP allowlist;
- опасные bash workflows вынести в `ask`;
- subagents делать узкими и с минимальным набором tools;
- hooks использовать как policy layer для production-sensitive операций.

**19. Что я бы рекомендовал настроить тебе на практике**
Это уже мой прикладной вывод из документации.

1. В `~/.claude/settings.json` задать личную политику:
- deny для `.env`, secrets, credentials;
- ask для `git push`, сетевых вызовов и deploy-команд;
- sandbox on, если среда позволяет.

2. В каждом репозитории держать короткий `CLAUDE.md`:
- архитектура;
- команды build/test/lint;
- code conventions;
- known pitfalls.

3. В `.claude/rules` вынести path-specific rules:
- API;
- database;
- tests;
- frontend.

4. Сделать 3-5 project subagents:
- `code-reviewer`
- `debugger`
- `test-runner`
- `db-reader`
- `release-prep`

5. Сделать 3-5 skills:
- `deploy`
- `release-check`
- `migration-checklist`
- `incident-triage`
- `docs-scan`

6. Подключать MCP только к доверенным системам.

7. Headless и GitHub Actions включать только после локального dry-run той же задачи.

**20. Короткая карта принятия решений**
Если задача:
- повторяемая и prompt-like, делай `skill`
- требует отдельного контекста или отдельных permissions, делай `subagent`
- должна быть всегда в фоне проекта, клади в `CLAUDE.md` или `.claude/rules`
- требует реального запрета/разрешения, делай `settings` или `hooks`
- требует внешних сервисов, подключай `MCP`
- должна работать без UI, используй `headless` или `SDK`
- должна бежать в CI, используй `GitHub Actions`
- должна реально кликать по UI, смотри `computer use`

**Источники**
- [Claude Code overview](https://code.claude.com/docs/en/overview)
- [Claude Code settings](https://code.claude.com/docs/en/settings)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Hooks reference](https://code.claude.com/docs/en/hooks)
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)
- [Extend Claude with skills](https://code.claude.com/docs/en/slash-commands)
- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [CLI reference](https://code.claude.com/docs/en/cli-reference)
- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [Claude Code SDK](https://docs.anthropic.com/en/docs/claude-code/sdk)
- [Agent SDK permissions](https://platform.claude.com/docs/en/agent-sdk/permissions)
- [Agent SDK hooks](https://platform.claude.com/docs/en/agent-sdk/hooks)
- [Handle approvals and user input](https://platform.claude.com/docs/en/agent-sdk/user-input)
- [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- [Claude Code security](https://docs.anthropic.com/en/docs/claude-code/security)

Если хочешь, следующим сообщением я могу сделать уже совсем прикладной пакет под тебя:
1. шаблон `~/.claude/settings.json`,
2. шаблон `CLAUDE.md`,
3. набор из 5 субагентов,
4. набор из 5 skills,
5. рекомендуемую policy-схему для безопасной автономной работы на твоём Mac.
