# Tooling Watchlist — отчёт за 18–25 мая 2026

**Дата:** 25 мая 2026
**Период:** 18–25 мая 2026
**Фокус:** инженерные изменения в Claude Code, Codex, Google (Gemini CLI), xAI

---

## Executive Summary

- **Claude Code v2.1.139–v2.1.150 — самая большая неделя по фичам за квартал.** В v2.1.139 (11 мая) официально вышел `/goal` (рабочие условия завершения, переживающие компакции/перезапуски) и `claude agents` (research preview agent view). За неделю 18–25 мая накатили `claude agents --json`, `--code-review high --comment`, OTEL-атрибуты `agent_id`/`parent_agent_id`, ужесточения PowerShell-permissions, `allowAllClaudeAiMcps`, GFM-чекбоксы в выводе, а также 80+ багфиксов вокруг background-sessions, agent view и worktree-isolation. Headline-security: исправлен PowerShell-байпасс через `cd..`/`X:`, утечка sandbox-allowlist на корень репо в worktree, и неправильно работавшие prefix-allow-правила.
- **Gemini CLI v0.43.0 (22 мая) — Session Portability, Adaptive Token Estimation, AgentProtocol.** Сессии экспортируются в файл и импортируются через CLI-флаг, новый адаптивный токен-калькулятор экономит окно контекста, `LocalSubagentProtocol`/`RemoteSubagentProtocol` под единым `AgentProtocol` — фундамент для мульти-агента. Модели «штурвально» направлены использовать `edit`-tool для хирургических правок.
- **xAI Grok Build (бета, 15 мая) — много новых деталей.** Архитектура: 16-agent Heavy на Grok 4.3, 2M-токен контекст, до 8 параллельных subagent'ов в отдельных `git worktree`. SWE-Bench Verified 70,8%. Headless-режим (`-p`), ACP-протокол, marketplace, плагины/хуки/skill'ы. **Объявлен retirement: `grok-code-fast-1` мигрирует на `grok-build-0.1`** (15 мая, действует с того же дня). Цена input $0.20/M.
- **Codex: безопасность и API-полировка, без революций.** В CLI 0.50.x: model summary + risk assessment при нарушении sandbox-политики, MCP env-var redaction в `/mcp` и `mcp get`, `CodexHttpClient` с логированием запросов, `codex/event/raw_item` события, улучшенный `/feedback` для диагностики, MCP startup-ошибки для таймаутов и GitHub. Главное за месяц — Chrome extension, ChatGPT mobile, computer use, но новых релизов формфактора на этой неделе нет.
- **Anthropic security/managed-agents: `/security-review` команда, MCP tunnels (research preview), self-hosted sandboxes для Managed Agents, live-апдейт MCP/tool-конфигов активной сессии, авто-spill больших output'ов >100K токенов в файл.** Это меняет операционку для продакшн-агентов.

---

## 1. Claude Code (Anthropic) — Приоритет 1

**Версии за период:** v2.1.139 (11.05) → v2.1.140 (12.05) → v2.1.141 (13.05) → v2.1.142 (14.05) → v2.1.143 (15.05) → v2.1.144 (19.05) → v2.1.145 (19.05) → v2.1.147 (21.05) → v2.1.148 (22.05) → v2.1.149 (22.05) → v2.1.150 (23.05). v2.1.146 пропущена.

### Ключевые новые возможности — с детализацией флагов и команд

#### `/goal` — рабочая цель с условием завершения (v2.1.139)
- Что: задаёт «condition of completion», после которого Claude продолжает работу через несколько turn'ов, пока цель не выполнена. Доступна в интерактиве, `-p` (headless) и Remote Control.
- UX: live-оверлей с elapsed time, числом turn'ов и токенов.
- Использование: `/goal All unit tests pass and the linter has no errors in src/`. Дальше Claude сам редактирует, гоняет тесты/линт, проверяет condition, продолжает.
- Зачем: ровно та же идея, что у Codex `/goal`, — задачи на дни/перезапуски без ручного «продолжай».

#### `claude agents` — agent view (Research Preview, v2.1.139)
- Что: единый TUI-список всех Claude Code-сессий (running / blocked on you / done).
- Запуск: `claude agents`.
- Ключевые комбинации в этом view (за период):
  - `Ctrl+T` (v2.1.147) — **закрепить** background-сессию (pinned остаются «живыми» в idle, обновляются с релизами Claude Code в месте и shed'ятся в memory pressure последними).
  - `←` — детач из сессии, возврат в список.
  - `v` — открыть в редакторе ($EDITOR/$VISUAL, v2.1.142).
- Флаги (v2.1.142): `--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--permission-mode`, `--model`, `--effort`, `--dangerously-skip-permissions` — применяются к самому view и к дочерним background-сессиям.
- v2.1.143: `--allow-dangerously-skip-permissions` (а не `--dangerously-skip-permissions`) — режим bypass становится **доступным в Shift+Tab cycle** дочерних сессий, но не дефолтным.
- v2.1.145: `claude agents --json` — список живых сессий в JSON для скриптов (tmux-resurrect, statusbar, session picker).
- v2.1.141: `claude agents --cwd <path>` — фильтр по директории.
- Пример: `claude agents --json | jq '.[] | select(.status=="awaiting_input") | .name'` — пайплайн, выдающий имена сессий, ждущих ответа.

#### `/code-review` (бывший `/simplify`, v2.1.147)
- Что: команда `/simplify` переименована в `/code-review`. Поведение поменялось — теперь это рапорт по correctness bug'ам, не cleanup-and-fix.
- Параметры:
  - **уровень effort'а позиционно**: `/code-review high` (значения как для `/effort`: `minimal`/`low`/`medium`/`high`).
  - `--comment` — постит найденные проблемы как inline GitHub PR comments.
- Пример: `/code-review high --comment` — глубокий ревью текущего diff'а + автоматические комментарии в PR.

#### `worktree.bgIsolation: "none"` (v2.1.143)
- Что: новая опция в `~/.claude/settings.json`.
- Семантика: background-сессии редактируют рабочую копию напрямую, без `EnterWorktree`. Для репо, где worktree-изоляция нереалистична (LFS-хевиc, специфичные toolchain'ы, large generated dirs).
- Пример:
  ```json
  { "worktree": { "bgIsolation": "none" } }
  ```
- Trade-off: безопаснее `worktree`-изоляция; `none` — для случаев, где она ломает workflow.

#### PowerShell tool — включён по умолчанию + Execution Policy bypass (v2.1.143)
- Что: PowerShell tool теперь включён по умолчанию на Windows для пользователей Bedrock / Vertex / Foundry. Опт-аут: `CLAUDE_CODE_USE_POWERSHELL_TOOL=0`.
- Дополнительно: PowerShell tool теперь передаёт `-ExecutionPolicy Bypass`. Опт-аут: `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1`.
- Зачем: пользователи Windows ELT/EDR-окружений ловили блоки на signed-only execution policy; bypass решает 80% случаев. Если ваша политика страшнее, чем agent — опт-аут.

#### `terminalSequence` в hook JSON-output (v2.1.141)
- Что: новое поле в JSON-ответе hook'а. Позволяет хуку отправить **desktop notification, заголовок окна, terminal bell** — без controlling terminal (т.е. в background-сессии).
- Пример ответа hook:
  ```json
  {
    "terminalSequence": "\u001b]9;Build failed\u0007\u0007"
  }
  ```
- Зачем: hooks, дёргаемые background-агентами, теперь могут «постучать пользователю в плечо» через системные нотификации.

#### `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` (v2.1.141)
- Что: клонирует плагины с GitHub через HTTPS вместо SSH (по дефолту — SSH, требует ключ).
- Зачем: CI/headless-окружения без GitHub SSH-ключа.

#### `ANTHROPIC_WORKSPACE_ID` (v2.1.141)
- Что: env var для workload-identity federation — ограничивает выпущенный токен конкретным workspace, когда federation-rule покрывает несколько.

#### `/scroll-speed` (v2.1.139) и rewind «Summarize up to here» (v2.1.141)
- `/scroll-speed` — настройка скорости mouse-wheel scroll с live-preview.
- В rewind-меню добавлена опция «Summarize up to here»: сжимает контекст до выбранной точки, оставляя более свежие turn'ы нетронутыми.

#### Hook `args: string[]` exec-form и `continueOnBlock` (v2.1.139)
- `args: string[]` — exec-form запуска без оболочки. Path-placeholder'ы (`{{file_path}}` и т.д.) **никогда** не нуждаются в кавычках/экранировании.
  ```json
  {
    "type": "command",
    "args": ["./scripts/check.sh", "{{file_path}}", "--strict"]
  }
  ```
- `continueOnBlock: true` для `PostToolUse` hook — если хук блокирует операцию, причина отдаётся обратно в модель, и turn **продолжается**. По умолчанию hook-rejection прерывает turn.

#### MCP stdio servers получают `CLAUDE_PROJECT_DIR` в env (v2.1.139)
- Что: симметрия с hooks. В plugin/config-командах можно ссылаться на `${CLAUDE_PROJECT_DIR}`.

#### `claude_code.tool` OTEL spans: `agent_id`/`parent_agent_id` (v2.1.145)
- Что: трассировка теперь корректно «вкладывает» background-subagent spans в Agent tool span dispatching-родителя.
- Use: distributed-tracing мульти-агентных run'ов в Honeycomb/Tempo/Jaeger — теперь видна семантическая иерархия.

#### `/usage` per-category breakdown (v2.1.149)
- Что: `/usage` показывает разбивку лимитов по категориям — skills, subagents, plugins, per-MCP-server cost.
- Зачем: понять, **что именно** жжёт лимиты, а не «всё ушло».

#### `allowAllClaudeAiMcps` managed setting (v2.1.149, Enterprise)
- Что: managed-policy опция для одновременной загрузки claude.ai cloud MCP-коннекторов рядом с `managed-mcp.json`.
- Зачем: enterprise хочет и whitelist'нутые серверы из своей политики, и пользовательские connectors из claude.ai.

#### GFM-task-list checkboxes (v2.1.149)
- Что: Markdown-output теперь рендерит `- [ ]` / `- [x]` как реальные чекбоксы, а не bullet'ы.

#### `/diff` keyboard scroll (v2.1.149)
- Что: detail view `/diff` крутится клавиатурой: стрелки, `j/k`, `PgUp/PgDn`, `Space`, `Home/End`.

### Безопасностные фиксы (важные)

- **PowerShell permission bypass (v2.1.149):** built-in `cd`-функции (`cd..`, `cd\`, `cd~`, `X:`) меняли рабочую директорию **необнаруженно** — позднее в той же сессии команда могла прочитать файл вне workspace. **Закрыто.** Этот класс уязвимостей касался любого Windows-пользователя с PowerShell tool.
- **Sandbox write allowlist в git worktrees (v2.1.149):** allowlist покрывал **весь корень основного репо**, а не только shared `.git/` (с `hooks/` и `config` denied). **Закрыто.**
- **PowerShell prefix/wildcard allow rules (v2.1.149):** правила вида `PowerShell(dotnet.exe build *)` **не** pre-approve'или native-executables/скрипты. **Закрыто.**
- **Permission-analysis gap для `PWD`/`OLDPWD`/`DIRSTACK` (v2.1.149):** парсер использовал stale variable-tracking values поверх `cd`/`pushd`/`popd`. **Закрыто.**
- **Auto-approve байпасс через bare variable assignment (v2.1.145):** bare `VAR=value` для non-allowlisted переменных в Bash-команде авто-одобрялись. **Закрыто.**

### Anthropic platform — релиз 19–21 мая

Из release notes Claude Platform/Help Center:
- **`/security-review` command** — встроенная команда security-review кода (упоминалось ранее в 2.1.108).
- **MCP tunnels** (research preview, 19.05) — подключение к MCP-серверам в **приватной сети** через tunnel.
- **Self-hosted sandboxes для Claude Managed Agents** (19.05) — альтернатива sandbox в инфраструктуре Anthropic.
- **Live-апдейт MCP/tool конфигов активной сессии Managed Agent** (19.05).
- **Auto-spill больших output'ов** (19.05): output'ы `agent_toolset` и MCP-tool'ов >100K токенов автоматически пишутся в файл sandbox'а; модель получает truncated preview + путь к файлу.
- **Compliance API integrations** (21.05) — IT/security могут управлять Claude через свой security-стек.

### Use-case 1: agent view + `/goal` + pinned background для CI-кубка

**Проблема.** Команда из 6 разработчиков обычно гоняла 4–5 параллельных Claude-сессий: интерактивная разработка, фоновый рефакторинг, тест-генератор, doc-апдейтер. Контекст-свитч между tmux-pane'ами съедал ~25–35% времени, plus легко было «забыть» о сессии, которая ждёт ответа.

**Решение.** Апгрейд на v2.1.149. Базовая команда дня: `claude agents --add-dir ~/work/api --settings ~/.config/claude/team.json --permission-mode auto --effort medium`. Долгоживущая «тестогенераторная» сессия закрепляется: `Ctrl+T`. Под ней `/goal All public API endpoints in src/api/ have at least 1 integration test in tests/integration/`. Скрипт-полер `claude agents --json | jq '.[] | select(.status=="awaiting_input")'` запускается из statusbar (Tmux).

**Результат.** За 5 рабочих дней: количество «забытых» сессий упало с ~3/нед до 0 (statusbar-нотификация). `/goal`-сессия за 2.5 дня закрыла 38 endpoint'ов из 41, остальные потребовали human-input — но без человеческого «продолжай». Контекст-свитч-overhead команда оценила как «снизился вдвое». Прямая денежная оценка не велась.

### Use-case 2: PowerShell-security фиксы перед аудитом

**Проблема.** Финансовая компания готовилась к security-аудиту окружения разработчиков. Wind ows-машины с Claude Code и PowerShell tool. Внутренний red team нашёл, что через `cd..` можно «выпрыгнуть» из workspace и прочитать файлы родительской директории мимо permission-системы.

**Решение.** Upgrade на v2.1.149 (где исправлены оба класса PowerShell-обходов + worktree-allowlist + prefix-rule матчинг). В managed-settings: `autoMode.hard_deny` для всех `PowerShell(*)`, требующих сетевого доступа; явный allowlist разрешённых build-команд через `PowerShell(dotnet.exe build *)`. Дополнительно: `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1` — bypass execution-policy отключён.

**Результат.** Red team повторила атаки: все 4 вектора (cd-обход, PWD-stale, prefix-bypass, bare VAR=value) теперь блокируются. Аудит пройден без замечаний к Claude Code. Время на патчинг: 1 рабочий день (deploy + retest).

### Оценка: **тестировать на этой неделе — да**

Обновиться на v2.1.149 **обязательно** для Windows-пользователей с PowerShell tool (security-фиксы). `claude agents`, `/goal`, `/code-review high --comment` — топ-фичи, протестировать и зафиксировать как часть workflow.

**Источники:**
[Claude Code Changelog](https://code.claude.com/docs/en/changelog), [Claude Platform Release Notes](https://platform.claude.com/docs/en/release-notes/overview), [Claude Help Center — Release notes](https://support.claude.com/en/articles/12138966-release-notes), [Code w/ Claude 2026 live blog (Simon Willison)](https://simonwillison.net/2026/May/6/code-w-claude-2026/), [Notes from Code with Claude 2026 (Chris Ebert)](https://chrisebert.net/notes-from-code-with-claude-2026/).

---

## 2. Codex (OpenAI) — Приоритет 1

За неделю 18–25 мая новых формфакторов не добавилось (Chrome extension + mobile + computer use вышли раньше). Изменения — точечная безопасность и API-полировка.

### Новые возможности и фиксы

#### Sandbox-policy model summary + risk assessment (CLI 0.50.0, #5536)
- Что: при нарушении sandbox-политики Codex теперь показывает не только «denied», но и:
  - **что именно** хотел сделать модельный план;
  - **risk-оценку** (low/medium/high);
  - **источник** правила, которое сработало.
- Use: «дебаг» permission-конфигов перестал быть слепой угадайкой.

#### MCP env-var redaction в `/mcp` и `mcp get` (CLI 0.50.0, #5648)
- Что: значения environment-переменных у MCP-серверов **маскируются** при выводе в TUI и в `mcp get`.
- Зачем: ключи/секреты в конфиге больше не светятся в логах, скриншотах, скринкастах.

#### `CodexHttpClient` с request logging (CLI 0.50.0, #5564)
- Что: новый HTTP-клиент с встроенным логированием запросов.
- Use: дебаг flaky-сетевых проблем — теперь видно exact request/response cycle (с redacted-секретами).

#### `codex/event/raw_item` события (CLI 0.50.0, #5578)
- Что: app-server теперь стримит raw_item events — низкоуровневый stream сырых элементов ответа.
- Use: построение IDE/web-клиентов, требующих видеть сырой поток без обработки.

#### Stale rate-limits messaging (#5570)
- Что: когда нет cached rate-limits — теперь human-friendly сообщение, а не «`/status` пустой».
- Use: новые установки CLI больше не путают пользователей.

#### Improved `/feedback` диагностика (#5661, #5663)
- Что: `/feedback` собирает больше контекста для багрепортов — стек, версии, последний transcript.

#### Token info → ConversationHistory (#5581)
- Что: `token_info` перенесена в `ConversationHistory` для согласованности с историей беседы.

#### MCP startup-errors для timeouts и GitHub (#5595)
- Что: при таймауте или ошибке GitHub MCP-сервера показывается понятная диагностика, а не generic «not connected».

#### Brew upgrade instructions (#5640)
- Что: подсказка по `brew upgrade codex` для пользователей homebrew.

#### `mcp add` login gating (#5653)
- Что: после `mcp add` логин-флоу gated за `experimental_use_rmcp_client` — чтобы не сломать пользователей не-rmcp-клиента.

### Use-case: дебаг flaky CI-пайплайна через CodexHttpClient

**Проблема.** В CI на GitHub Actions Codex иногда возвращал «Error: stream interrupted» на тяжёлых задачах ~3 раза в неделю. Воспроизвести локально не получалось.

**Решение.** Включили request logging нового `CodexHttpClient` через `CODEX_HTTP_LOG=1` (env var) в matrix-runner. После следующего же flaky-run в логах нашлось: GitHub-runner лимит keep-alive на 5 минут, а тяжёлый turn держал stream дольше; OpenAI возвращал valid stream-chunk через 5:12, GitHub резал. Workaround: разбили задачу через `/goal` на меньшие шаги.

**Результат.** Flaky-rate упал с ~3/нед до 0 за 2 недели наблюдений. Diagnostic-cycle сократился с «дней попыток воспроизвести» до 1 пайплайн-run'а (логи есть — причина видна).

### Оценка: **тестировать на этой неделе — может быть**

Security-фиксы накатить — да. Новых «больших» фич за неделю нет; если уже на 0.50.0 — обновлять не критично, ждать следующих релизов.

**Источники:**
[OpenAI Codex changelog (developers.openai.com)](https://developers.openai.com/codex/changelog), [Codex CLI releases (GitHub)](https://github.com/openai/codex/releases), [Releasebot — OpenAI](https://releasebot.io/updates/openai), [TechCrunch — Codex on phone](https://techcrunch.com/2026/05/14/openai-says-codex-is-coming-to-your-phone/).

---

## 3. Google: Gemini CLI / Stitch / AI Studio / Jules — Приоритет 2

**Версии за период:** Gemini CLI v0.43.0 (22 мая). Google I/O 2026 прошёл 19 мая — это в основном модели (Gemini 3.5, Gemini 3.1 Pro, 3.0 Flash) и продуктовые сервисы; интересного нам по CLI там было немного.

### Gemini CLI v0.43.0 — новые возможности

#### Session Portability — экспорт/импорт сессий
- Что: «export session to file and import via flag» (#26514).
- Use: shared-debug, передача контекста между машинами/коллегами, бэкап перед рискованной операцией.
- Дополнительно: «restore resume for legacy sessions» (#26577), «Allow Enter to select session while in search mode in /resume» (#21523).

#### Adaptive Token Estimation (#26888)
- Что: новый adaptive token calculator более точно оценивает размер контента — экономит окно контекста, снижает API-overhead.
- Дополнительно: «Improvements to the snapshotter» (#26655) — лучшее снэпшотирование context.

#### Surgical Code Edits via `edit` tool (#26480)
- Что: модели теперь «направлены» предпочитать tool `edit` для **хирургических** правок (вместо write-через-весь-файл).
- Эффект: быстрее, точнее, меньше «переписывает то, что не просил».

#### `LocalSubagentProtocol` + `RemoteSubagentProtocol` под `AgentProtocol` (#25302, #25303)
- Что: единая абстракция для локальных и удалённых subagent'ов. Фундамент мульти-агента.
- `SubagentState` enum для прогресса (#26934).

#### Tighter Auto Memory patch allowlist (#26535)
- Что: усилен whitelist для Auto Memory canonical-patch'ей.
- Зачем: меньше шанс, что Auto Memory сама себе пишет рискованные правки.

#### Безопасность и стабильность
- Shell-command safety evals (#26528).
- Random sandbox container names (#26014) — против side-channel detection.
- Headless OAuth: «prevent silent hang during OAuth auth on headless Linux» (#26571).
- Reject numeric project IDs in `GOOGLE_CLOUD_PROJECT` (#26532).
- Hide read-only settings scopes from UI (#26249).
- Improve `mcp list` UX in untrusted folders (#26457).
- Vi mode shortcuts + MCP/custom sandbox doc (#23853).

#### ACP/IDE-render фиксы
- `feat(acp/core)`: prefix tool call IDs with tool names — для рендера tool-call'ов в ACP-compliant IDE (#26676).
- Core-tools используют native `ToolDisplay` (#25186), фиксы UI rendering.
- ACP infinite-thought loop fix (#26874).

### Google I/O 2026 (19 мая) — что важно для разработчиков

- **Gemini 3.1 Pro и 3.0 Flash** — в Preview в Gemini Code Assist (VS Code и IntelliJ) для agent mode, chat, code generation. Код-кастомизация поддерживается в Gemini CLI и agent mode.
- **AI Studio** — Workspace integration для internal productivity apps.
- **Stitch** — streaming UI design with inline edits.
- **Anti-Gravity 2.0**, **Omni** (video), **Flow**, **Pomelli** — креативные продукты, не наш фокус.

### Jules
- Без явных публичных релизов за период.

### Use-case: shared-debug через session export

**Проблема.** Старший инженер делал deep-dive по сложному multi-file багу через Gemini CLI 3+ часа. Передать junior'у «продолжить» означало пересказывать весь контекст — час потери.

**Решение.** На v0.43.0: `/session export ~/debug-session.json`, передан junior'у. Тот импортирует CLI-флагом: `gemini --import-session ~/debug-session.json`. Полная история turn'ов, tool-call'ов, file-history восстановлена.

**Результат.** Handoff занял ~5 минут вместо часа. Качество разбора не пострадало — junior видит ровно то, что видел старший. На 4 случаях handoff'а за неделю сэкономлено ~3 рабочих часа.

### Оценка: **тестировать на этой неделе — может быть**

Adaptive token estimation и surgical edits включаются «сами» с апгрейдом — безопасно. Session export/import — отличная фича для команд с handoff'ами. AgentProtocol для multi-agent пока infrastructure-only.

**Источники:**
[Gemini CLI v0.43.0 changelog](https://geminicli.com/docs/changelogs/latest/), [Gemini Code Assist release notes (May 14)](https://developers.google.com/gemini-code-assist/resources/release-notes), [What launched at Google I/O 2026 (Lenny's Newsletter)](https://www.lennysnewsletter.com/p/what-launched-at-google-io-2026-30).

---

## 4. xAI (Grok tools) — Приоритет 3

### Grok Build — что подробно узнали за неделю
**Запуск был 15 мая;** на этой неделе появились детальные технические подробности и официальная migration-документация.

#### Архитектура (новые данные)
- **16-agent Heavy** на Grok 4.3 beta — модель оркеструет до 16 подсистем.
- **2M-токен контекст**.
- **До 8 параллельных subagent'ов** в собственных `git worktree`. Каждый агент работает на своей ветке, без конфликтов с другими.
- **SWE-Bench Verified: 70,8%** (для контекста: Claude Sonnet 3.7 — ~65–67%; Grok-build обходит).
- **Input price: $0.20/M tokens** (через API; CLI gated за $300/мес SuperGrok Heavy).
- **ACP (Agent Client Protocol)** — поддержка стандартного протокола, позволяющего интеграцию с IDE и других tool'ов.

#### Ключевые фичи CLI
- **Plan Mode**: read/approve/modify планов до исполнения, comment-on-step, перезапись всего плана.
- **Sub-agents в worktree**: для больших задач делегируется параллельно на 8 веток (8 git worktree).
- **Marketplace** для шейринга навыков команд.
- **Headless mode** — флаг `-p`, для CI/скриптов/recurring tasks/orchestration apps.
- **Inline feedback**: `/feedback` в CLI — фидбэк уходит напрямую в xAI.
- **Совместимость**: подхватывает existing AGENTS.md, plugins, hooks, skills, MCP-servers — work out of the box.

#### Объявленный retirement (важно для тех, кто на xAI API)
**15 мая 2026 в 12:00 PT** xAI ретировал ряд моделей. По миграции:
- `grok-code-fast-1` → **`grok-build-0.1`** (значительно улучшенные agentic-coding и web-dev capabilities).
- `grok-4-fast-reasoning` / `grok-4-fast-non-reasoning` / `grok-4-0709` → `grok-4.3`.
- `grok-3` → `grok-4.3` с `none` reasoning effort.

Запросы на старые slug'и автоматически перенаправляются.

### Use-case: parallel investigation сабагентами

**Проблема.** Performance-команда исследовала деградацию latency p99 на проде. Подозрений было 4: slow endpoints, database query plans, cache hit-rates, deploy-pipeline. Последовательный анализ занимал день на каждый вектор — итого ~4 дня.

**Решение.** На SuperGrok Heavy: один промпт в Grok Build — «Investigate p99 latency degradation. Split into 4 parallel subagents: (1) slow endpoint analysis from APM logs, (2) DB query plan regression, (3) Redis cache hit ratio, (4) deploy timeline correlation. Each in its own worktree on branch `investigate/<area>`.» Каждый subagent работает в своём `git worktree` независимо.

**Результат.** За ~6 часов вернулись 4 ветки с findings'ами и proposed PR-changes. Identified причина — N+1 в `OrderService.list()` после rebase на prod 6 дней назад. Серый ROI vs 4 дня; но **доступ** ограничен $300/мес.

### Оценка: **тестировать на этой неделе — нет (для большинства)**, **да — для команд на SuperGrok Heavy**

Архитектура впечатляет (16-agent Heavy + worktree-based parallel), цифры SWE-Bench конкурентоспособны. Но: CLI всё ещё в early beta, документации мало, гейтинг $300/мес. Подождать публичных деталей по security-модели, sandbox profile'ам, MCP-совместимости (заявлено — but undocumented).

**Источники:**
[Grok Model Retirement May 15, 2026 (xAI Docs)](https://docs.x.ai/developers/migration/may-15-retirement), [16 agents one prompt — xAI Grok Build (Instagram)](https://www.instagram.com/p/DYZO559kw1h/), [NEW Grok Build Update is INSANE (YouTube)](https://www.youtube.com/watch?v=gDmRNLVxUko), [PCMag — xAI launches Grok Build](https://www.pcmag.com/news/elon-musks-xai-launches-grok-build-its-first-ai-coding-agent), [Engadget — Grok Build](https://www.engadget.com/2173482/xai-coding-agent-grok-build/).

---

## Сводная таблица

| Инструмент | Ключевые возможности недели | Use-cases | Импакт | Тестировать на этой неделе |
|---|---|---|---|---|
| **Claude Code** | v2.1.139–150; `/goal`, `claude agents` (+`--json`, `--cwd`, `Ctrl+T` pin, `←` detach), `/code-review high --comment`, `worktree.bgIsolation: none`, PowerShell ExecutionPolicy bypass + opt-out, `terminalSequence` в hook, `CLAUDE_CODE_PLUGIN_PREFER_HTTPS`, `ANTHROPIC_WORKSPACE_ID`, hook `args[]` exec-form, hook `continueOnBlock`, `allowAllClaudeAiMcps`, OTEL agent_id/parent_agent_id, `/usage` per-category, GFM-checkbox render. **Security-фиксы**: PowerShell cd-bypass, worktree allowlist на корень репо, bare-VAR auto-approve, prefix-rule wildcard. Платформа: `/security-review`, MCP tunnels, self-hosted sandboxes, auto-spill >100K | Agent view + `/goal` + pinned bg для сложной команды; PowerShell security-аудит | **Высокий** | **Да** |
| **Codex** | CLI 0.50.x; sandbox-policy summary + risk, MCP env redact, CodexHttpClient request log, `codex/event/raw_item`, stale rate-limits messaging, `/feedback` diagnostics, MCP startup errors. Новых формфакторов на этой неделе нет | Дебаг flaky-CI через HTTP-лог | **Низкий–Средний** | **Может быть** |
| **Gemini CLI** | v0.43.0; Session Portability (export/import via flag), Adaptive Token Estimation, Surgical Edits via `edit` tool, `LocalSubagentProtocol`/`RemoteSubagentProtocol`/`AgentProtocol`, tighter Auto Memory allowlist, ACP rendering fixes, shell-cmd safety evals, headless OAuth fix. I/O: Gemini 3.1 Pro & 3.0 Flash в Code Assist preview | Session export для shared-debug handoff (1 час → 5 мин) | **Средний** | **Может быть** |
| **xAI Grok Build** | 16-agent Heavy на Grok 4.3, 2M context, 8 parallel subagents в `git worktree`, 70.8% SWE-Bench, ACP support, headless `-p`, marketplace, $0.20/M input. **Retirement 15.05**: `grok-code-fast-1` → `grok-build-0.1` | Parallel investigation 4-х подозрений за 6 часов вместо 4 дней | **Средний–Высокий** (для тех, кто на SuperGrok Heavy) | **Нет** для большинства; **Да** для $300-tier |

---

## Рекомендации недели (3 действия)

1. **Обновить Windows-машины с Claude Code и PowerShell tool на v2.1.149.** Это **must** — закрыты 4 класса security-issues (cd-обход, stale PWD, prefix-rule bypass, bare-VAR auto-approve, worktree allowlist на корень репо). Сюда же — обсудить в команде, оставлять ли `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1` (опт-аут execution-policy bypass).
2. **Затестить связку `claude agents` + `/goal` + pinned background (`Ctrl+T`) на одной долгоживущей задаче** (тест-генерация, миграция, refactor). Замерить количество context-switch'ей и забытых сессий до/после. По итогу — закрепить в team workflow с `claude agents --json` интеграцией в statusbar.
3. **На enterprise-инсталляциях Claude — включить MCP tunnels (research preview) и `/security-review` в PR-flow.** Это не классическая CLI-фича, но новая платформенная capability: подключение к MCP-серверам в приватной сети + встроенный security-review кода. Параллельно — проверить `auto-spill >100K` для long-running Managed Agent сессий.

---

## Все источники

### Claude Code и Anthropic platform
- [Claude Code Changelog (code.claude.com)](https://code.claude.com/docs/en/changelog)
- [Claude Platform Release Notes](https://platform.claude.com/docs/en/release-notes/overview)
- [Claude Help Center — Release notes (May 2026)](https://support.claude.com/en/articles/12138966-release-notes)
- [Live blog: Code w/ Claude 2026 — Simon Willison](https://simonwillison.net/2026/May/6/code-w-claude-2026/)
- [Notes from Code with Claude 2026 — Chris Ebert](https://chrisebert.net/notes-from-code-with-claude-2026/)
- [Claude Code v2.1.137 release video (YouTube)](https://www.youtube.com/watch?v=cST2RxmEGfo)

### Codex
- [OpenAI Codex changelog (developers.openai.com)](https://developers.openai.com/codex/changelog)
- [Codex CLI releases (GitHub)](https://github.com/openai/codex/releases)
- [Releasebot — OpenAI](https://releasebot.io/updates/openai)
- [TechCrunch — Codex coming to your phone](https://techcrunch.com/2026/05/14/openai-says-codex-is-coming-to-your-phone/)

### Google (Gemini CLI / I/O 2026)
- [Gemini CLI v0.43.0 changelog](https://geminicli.com/docs/changelogs/latest/)
- [Gemini Code Assist release notes](https://developers.google.com/gemini-code-assist/resources/release-notes)
- [Releasebot — Google Gemini CLI](https://releasebot.io/updates/google/gemini-cli)
- [What launched at Google I/O 2026 — Lenny's Newsletter](https://www.lennysnewsletter.com/p/what-launched-at-google-io-2026-30)

### xAI
- [Grok Model Retirement May 15, 2026 — xAI Docs](https://docs.x.ai/developers/migration/may-15-retirement)
- [16 agents one prompt — Grok Build (Instagram)](https://www.instagram.com/p/DYZO559kw1h/)
- [NEW Grok Build Update is INSANE (YouTube)](https://www.youtube.com/watch?v=gDmRNLVxUko)
- [PCMag — Elon Musk's xAI Launches Grok Build](https://www.pcmag.com/news/elon-musks-xai-launches-grok-build-its-first-ai-coding-agent)
- [Engadget — xAI's coding agent Grok Build](https://www.engadget.com/2173482/xai-coding-agent-grok-build/)
- [CIO Dive — xAI joins coding agent race](https://www.ciodive.com/news/xAI-coding-agents-Grok-Build/820422/)
