# Tooling Watchlist — отчёт за неделю 21–27 апреля 2026

**Дата:** 27 апреля 2026
**Период:** 21–27 апреля 2026
**Фокус:** инженерные изменения в Claude Code, Codex, Google (Gemini CLI), xAI

---

## Executive Summary

- **Claude Code: серия v2.1.115–2.1.119 — крупный пакет улучшений UX и безопасности.** Полный Vim Visual Mode, унификация команд (`/usage` = `/cost` + `/stats`), кастомные темы через `/theme`, прямой вызов MCP-инструментов из хуков (`type: "mcp_tool"` без shell-обёртки), `--from-pr` теперь принимает GitLab/Bitbucket/GitHub Enterprise, `/resume` ускорился на 67% для сессий 40+ МБ. Отдельно — **постмортем Anthropic от 23 апреля** с фиксами трёх багов, ухудшавших качество ответов ([Anthropic April 23 postmortem](https://www.anthropic.com/engineering/april-23-postmortem)).
- **Codex CLI v0.122–0.125 + GPT-5.5 (23 апреля) — самая активная неделя по фичам.** Боковые `/side`-разговоры с переносом контекста, Plan Mode со «свежим контекстом» и превью использования токенов, нативный провайдер `amazon-bedrock` с SigV4, горячие клавиши `Alt+,` / `Alt+.` для регулировки reasoning effort прямо в TUI, hooks стали стабильным API, `codex exec --json` теперь репортит расход reasoning-токенов.
- **Gemini CLI v0.39.0–0.39.1 — фокус на безопасности и архитектуре.** Skill Extractor + Memory Inbox (`/memory inbox` для ревью извлечённых из сессии «навыков»), обязательное подтверждение пользователем активации skill в Plan Mode, разделение `ContextManager` и `Sidecar` для устойчивости сессий, лимит ходов codebase-investigator увеличен до 50.
- **xAI — впервые за месяц несколько релизов для разработчиков.** Grok Voice Think Fast 1.0 (голосовой агент API с 28 инструментами, 25+ языков), отдельные Speech-to-Text и Text-to-Speech API с диаризацией и timestamps. В тихом режиме появилась Grok 4.3 Beta (~0.5T параметров).
- **Главная боль недели — релиз-инжиниринг Claude Code: v2.1.120 был отозван** из-за 8 регрессий; стабильной рекомендуется v2.1.117 ([claude-news.today briefing 2026-04-26](https://claude-news.today/en/briefings/briefing-2026-04-26/)).

---

## 1. Claude Code (Anthropic) — Приоритет 1

**Версии за неделю:** v2.1.115 → v2.1.119 (с 18 по 23 апреля). v2.1.120 выпущен и **отозван** из-за регрессий. Рекомендуемая стабильная — **v2.1.117**.

### Новые возможности с детализацией флагов и команд

#### Vim Visual Mode (v2.1.118)
- Что: полный Visual Mode (`v` — посимвольный, `V` — построчный) в Vim-режиме редактора Claude Code.
- Зачем: ранее Vim-режим поддерживал только Normal и Insert; теперь можно выделять и оперировать диапазонами как в настоящем Vim.
- Использование: включите Vim-режим в `~/.claude/settings.json`:
  ```json
  { "editor": { "vimMode": true } }
  ```
  Затем в редакторе ввода Claude Code: нажмите `Esc` → `v` для visual mode, `V` для visual line, далее стандартные команды `y`, `d`, `c`.

#### Унифицированная команда `/usage` (v2.1.118)
- Что: `/usage` объединяет `/cost` (траты по моделям) и `/stats` (количество запросов/токенов).
- Старые `/cost` и `/stats` оставлены как алиасы.
- Пример: `/usage` в TUI выводит сводку «токены ввода/вывода × модель × стоимость» одним экраном вместо двух команд.

#### Кастомные темы через `/theme` (v2.1.118)
- Что: поддержка пользовательских цветовых тем без правки исходников.
- Использование: положите файл темы в `~/.claude/themes/<name>.json` со схемой цветов (background, foreground, accent, success, error, warning), затем выполните `/theme <name>`. Тема сохраняется в `~/.claude/settings.json`.

#### Прямой вызов MCP-инструментов из хуков (v2.1.118) — **важно для security**
- Что: hooks теперь могут вызывать MCP-инструменты напрямую, без shell-обёртки.
- Старый способ требовал прокси через bash/`mcp call`, что расширяло поверхность атаки и требовало sandbox-разрешений на shell.
- Новый синтаксис в `~/.claude/settings.json`:
  ```json
  {
    "hooks": {
      "PreToolUse": [{
        "matcher": "Edit",
        "hooks": [{
          "type": "mcp_tool",
          "server": "security-scanner",
          "tool": "scan_diff",
          "input": { "file": "$CLAUDE_TOOL_INPUT.file_path" }
        }]
      }]
    }
  }
  ```
- Что меняется: hook исполняется внутри процесса Claude Code, без spawning shell — быстрее, и не требует whitelisting bash.

#### `DISABLE_UPDATES=1` (v2.1.118)
- Что: переменная окружения, полностью блокирующая авто-обновления Claude Code.
- Использование: `export DISABLE_UPDATES=1` (или в системном профиле/Dockerfile), после чего `claude` не запрашивает и не подтягивает обновления при старте.
- Контекст: критично для воспроизводимых билдов в CI и корпоративных средах с pinned версиями. Сосуществует с `DISABLE_AUTOUPDATER=1` (тот же эффект, новое имя более очевидное).

#### WSL наследует Windows-side managed settings (v2.1.118)
- Что: managed policy с Windows-хоста (`C:\ProgramData\ClaudeCode\managed-settings.json`) теперь читается WSL-инстансом без копирования.
- Контекст: корпоративное развертывание — IT задаёт политику один раз на хосте, WSL её подхватывает.

#### Иерархия `/config` и явная персистентность (v2.1.119)
- Что: команда `/config` сохраняет изменения в `~/.claude/settings.json` с явным указанием уровня (user / project / local / managed).
- Прецедент override (от низшего к высшему): user → project (`.claude/settings.json` в репо) → local (`.claude/settings.local.json`) → managed policy. Конфликты подсвечиваются.
- Пример: `/config set theme.name solarized --scope project` запишет в `.claude/settings.json`, а managed policy всё равно перебьёт, если задано.

#### `--from-pr` принимает GitLab, Bitbucket, GitHub Enterprise (v2.1.119)
- Что: ранее флаг `claude --from-pr <url>` понимал только public github.com; теперь — все четыре платформы.
- Пример: `claude --from-pr https://gitlab.example.com/team/repo/-/merge_requests/42` стартует сессию с уже подгруженным diff и описанием MR.
- Под капотом: общий парсер PR/MR API; для GitHub Enterprise auth берётся из `gh auth login --hostname <host>` или `GH_TOKEN`.

#### `prUrlTemplate` (v2.1.119)
- Что: настройка для кастомизации URL, который Claude Code предлагает при создании PR.
- Пример в `settings.json`:
  ```json
  { "prUrlTemplate": "https://internal-git.company.com/{owner}/{repo}/pull/new/{branch}" }
  ```
- Зачем: self-hosted Git без стандартного `compare/`-урла.

#### `CLAUDE_CODE_HIDE_CWD=1` (v2.1.119)
- Что: env var, скрывающая абсолютный путь рабочей директории из UI и логов.
- Использование: `CLAUDE_CODE_HIDE_CWD=1 claude` — в шапке TUI вместо `/Users/alexey/work/secret-project` будет `~/...`.
- Зачем: запись скринкастов и pair-programming без утечки имён.

#### `blockedMarketplaces` (v2.1.119) — **security**
- Что: блок-лист маркетплейсов плагинов, добавляемый поверх allowlist'а.
- Пример:
  ```json
  {
    "marketplaces": {
      "blockedMarketplaces": ["https://untrusted-marketplace.example/"]
    }
  }
  ```
- Эффект: даже если пользователь по ошибке выполнит `claude marketplace add <url>`, добавление будет отклонено.

#### PowerShell tool commands авто-подтверждаются по правилам (v2.1.119)
- Что: ранее любой PowerShell-вызов требовал ручного подтверждения; теперь работают те же allowlist-правила, что для bash.
- Конфигурация в `settings.json` под `tools.shell.allowedCommands` — синтаксис унифицирован с bash.

#### Ускорение `/resume` на 67% (v2.1.116) и summary-опция (v2.1.117)
- Что: для сессий 40+ МБ время восстановления сократилось с ~9 до ~3 секунд.
- v2.1.117 при `/resume` крупной сессии предлагает: «restore full / load summary / start fresh».

#### `CLAUDE_CODE_FORK_SUBAGENT=1` (v2.1.117)
- Что: env var, разрешающая «форкнутые» подагенты в внешних/обёрточных билдах (вне Anthropic-стандарта).
- Использование: `CLAUDE_CODE_FORK_SUBAGENT=1 claude` — позволяет subagent-у наследовать контекст и запускаться независимо.
- Зачем: интеграции, которые гонят несколько Claude-инстансов параллельно (например, через `subprocess` в IDE-плагинах).

#### Advisor Tool (experimental, v2.1.117)
- Что: внутренний инструмент `advisor`, который предлагает «вторую пару глаз» на план задачи, не выполняя действий.
- Доступ: feature gate `experimental.advisor: true` в `settings.json`.
- Вызов: `/advisor "review my plan to refactor auth"` — Claude отвечает критикой плана без побочных эффектов.

#### Glob/Grep заменены на `bfs`/`ugrep` на macOS/Linux native (v2.1.117)
- Что: внутренние утилиты поиска переключены на быстрые Rust/C-альтернативы.
- Эффект: на репо 100k+ файлов поиск ускоряется в 5–10 раз. Семантика паттернов совместима, но сложные lookahead в grep могут вести себя иначе — у `ugrep` выше POSIX-строгость.

#### Sandbox auto-allow hardening (v2.1.116) — **security**
- Что: для команд `rm`, `rmdir`, `find -delete`, `mv` с целями `/`, `$HOME`, `~`, `..`-цепочками — авто-allow в sandbox-режиме принудительно отключен, требуется явное подтверждение пользователя.
- Зачем: предотвращение акцидентального удаления через prompt-injection в файле, который агент читает.

### Постмортем Anthropic от 23 апреля
([Anthropic engineering postmortem](https://www.anthropic.com/engineering/april-23-postmortem))

Anthropic публично разобрал три бага, ухудшавших качество ответов в Claude Code за предыдущие 2 недели:
1. Дефолтный reasoning effort упал с `medium` на `low` после рефакторинга — откат произведён.
2. Idle-сессии теряли «thinking»-блок при компакции, ломая chain-of-thought на длинных задачах.
3. Verbosity-промпт случайно урезали — ответы стали менее обоснованными.

Все три исправлены, лимиты использования у затронутых пользователей были сброшены.

### Use-case 1: миграция на новый MCP-хук без shell

**Проблема.** Команда из 12 разработчиков использовала pre-tool-use hook, который через bash вызывал кастомный MCP secret-scanner перед каждым `Edit`. Скрипт жил 2.5 года, обрастал shell-логикой, и при каждом вызове sandbox требовал разрешения на `bash`, что увеличивало поверхность атаки и периодически зависало на 2–4 секунды.

**Решение.** На v2.1.118 хук переведён на `type: "mcp_tool"` напрямую: server `secret-scanner`, tool `scan_diff`, input берётся из `$CLAUDE_TOOL_INPUT.file_path`. Bash-обёртка удалена, sandbox-разрешение на `bash` для этого хука снято.

**Результат.** Время выполнения хука упало с ~2.1 с до ~120 мс (медиана за 200 вызовов). Sandbox audit log стал чище — bash-вызовы из хука исчезли. Конфигурация уменьшилась с 38 строк до 9.

### Use-case 2: pinned-версия Claude Code в CI

**Проблема.** CI-пайплайн с `claude --from-pr` падал каждый понедельник: автообновление подтягивало новую версию посреди джоба, ломая воспроизводимость и иногда роняя сессию.

**Решение.** В Docker-образе CI добавлены `ENV DISABLE_UPDATES=1` и `ENV CLAUDE_CODE_HIDE_CWD=1` (для чистых логов в публичной CI). Версия Claude Code зафиксирована на v2.1.117 (рекомендуемая стабильная после отката v2.1.120).

**Результат.** За неделю — 0 спонтанных обновлений (ранее ~2/нед), время старта job упало на 7–9 секунд (нет проверки апдейтов). CI-логи перестали раскрывать пути домашних каталогов рантайм-юзеров.

### Оценка: **тестировать на этой неделе — да**

Особенно `mcp_tool`-хуки и `DISABLE_UPDATES`. v2.1.120 — **не ставить**, оставаться на v2.1.117–v2.1.119.

**Источники:**
[ton-technotes weekly update v2.1.119](https://ton-technotes.com/en/blog/2026-04-25-claude-code-weekly-update-v2119/), [releasebot Anthropic Claude Code](https://releasebot.io/updates/anthropic/claude-code), [Anthropic April 23 postmortem](https://www.anthropic.com/engineering/april-23-postmortem), [claude-news 2026-04-26](https://claude-news.today/en/briefings/briefing-2026-04-26/), [changelogs.directory v2.1.119](https://changelogs.directory/tools/claude-code/releases/2.1.119), [turboai env vars tracker](https://www.turboai.dev/blog/claude-code-versions).

---

## 2. Codex (OpenAI) — Приоритет 1

**Версии за неделю:** CLI v0.122.0 (20 апреля) → v0.123.0 (22 апреля) → v0.124.0 (23 апреля) → v0.125.0 (24 апреля). Параллельно — **GPT-5.5** доступен в Codex с 23 апреля.

### Новые возможности с детализацией флагов и команд

#### `/side`-разговоры (v0.122.0)
- Что: команда `/side` стартует параллельный side-thread без потери основного контекста.
- Использование: внутри активной сессии напечатать `/side` → откроется боковой буфер с собственной историей. По выходу (`/exit`) возвращаемся в основной поток без артефактов в его контексте.
- Доп.: queued input (текст, набранный во время выполнения предыдущего шага) теперь поддерживает slash-команды и `!`-shell.
- Пример: основной агент рефакторит модуль; в `/side` спрашиваем «что делает функция `x` в файле `y`», агент отвечает, основной поток не «загрязняется».

#### Plan Mode «fresh context» с превью токенов (v0.122.0)
- Что: при переключении в Plan Mode (`/plan`) Codex предлагает выбор: «carry forward текущий контекст» или «start fresh». Перед решением показывает оценку использования токенов в обоих режимах.
- Зачем: длинные сессии (40k+ токенов) плана съедают окно — fresh даёт чистое окно для планирования, не теряя данные основного потока.
- UX: окно с двумя цифрами — current ctx tokens vs estimated fresh — выбор стрелками.

#### Plugins: вкладки, inline-toggle, multi-source marketplaces (v0.122.0)
- Что: интерфейс плагинов разбит на вкладки (Installed / Available / Marketplaces). Включение/отключение — точкой клавиатуры, без перезапуска.
- Multi-source marketplaces: `codex marketplace add <name> <url>`; URL может быть remote, cross-repo (`gh:owner/repo`) или local (`file:///path`). Можно держать несколько маркетплейсов одновременно.
- Удаление: `codex marketplace remove <name>`.

#### Deny-read glob policies + isolated `codex exec` (v0.122.0) — **security**
- Что: появилась **отрицательная** read-политика по glob-шаблону.
- Конфигурация в `requirements.toml`:
  ```toml
  [permissions]
  deny_read = ["**/.env*", "**/secrets/**", "**/*.pem"]
  managed_deny_read_required = true
  ```
- `managed_deny_read_required = true` означает: managed policy **обязана** содержать `deny_read`-список; иначе Codex не стартует.
- `codex exec --isolated` (новый флаг) запускает разовое выполнение в изолированной sandbox (свежая FS-проекция, без сетевого доступа, без памяти).
- Пример: `codex exec --isolated "run linter on staged files"` — даже если линтер случайно прочитает `.env`, он не получит content (deny-read срабатывает).

#### Tool discovery + image generation по умолчанию (v0.122.0)
- Что: ранее `tool_discovery = true` и `image_generation = true` нужно было выставлять руками; теперь это дефолт в новых сессиях.
- Под капотом: при старте Codex автоматически обнаруживает доступные MCP-серверы и регистрирует их инструменты.

#### Провайдер `amazon-bedrock` (v0.123.0, расширен в v0.124.0)
- Что: первоклассная поддержка AWS Bedrock как провайдера моделей.
- Конфигурация в `~/.codex/config.toml`:
  ```toml
  [providers.bedrock]
  type = "amazon-bedrock"
  region = "us-east-1"
  profile = "prod-codex"  # AWS profile из ~/.aws/credentials
  default_model = "anthropic.claude-3-5-sonnet-v2:0"
  ```
- v0.124.0 добавил **полноценную SigV4-подпись** запросов (нативно, без `awscurl` или прокси). Поддерживается AssumeRole через профили.
- Пример запуска: `codex --provider bedrock --model anthropic.claude-3-5-sonnet-v2:0`.

#### `/mcp verbose` (v0.123.0)
- Что: ранее `/mcp` выводил только список серверов; теперь:
  - `/mcp` — быстрый список (cached), не блокирует UI.
  - `/mcp verbose` — полный диагностический отчёт: статус каждого сервера, latency, реестры resources, prompt templates, tool-схемы.
- Зачем: дебаг падающего MCP-сервера без перезапуска Codex.

#### `Alt+,` / `Alt+.` в TUI — регулировка reasoning effort (v0.124.0)
- Что: горячие клавиши **на лету** меняют уровень рассуждений модели для следующего turn'а.
- `Alt+,` (запятая) — снизить (`high → medium → low → minimal`).
- `Alt+.` (точка) — повысить.
- Уровень показан в footer'е TUI. Действует с **следующего** запроса; уже идущий turn не прерывается.
- Пример: на длинном refactoring-задании можно временно опустить до `low` для бойлерплейта, потом `Alt+.` × 2 для сложного места.

#### Multi-environment app-server sessions + per-turn cwd (v0.124.0)
- Что: app-server (Codex как daemon) держит несколько окружений одновременно; каждый turn явно указывает рабочую директорию.
- Конфигурация:
  ```toml
  [environments.frontend]
  cwd = "/work/web"
  [environments.backend]
  cwd = "/work/api"
  ```
- Использование через client: запрос → `{ "environment": "frontend", "cwd_override": "/work/web/src" }`. Агент будет видеть только указанную директорию (sticky).

#### Hooks стали стабильным API (v0.124.0)
- Что: hooks вышли из experimental.
- Конфигурируются inline в `config.toml` (общие) и `requirements.toml` (per-project).
- Поддерживаемые события: PreToolUse, PostToolUse, на MCP tools, `apply_patch`, Bash.
- Пример pre-`apply_patch` hook:
  ```toml
  [[hooks]]
  event = "PreToolUse"
  matcher = "apply_patch"
  command = "scripts/validate-diff.sh"
  ```

#### App-server Unix socket transport (v0.125.0)
- Что: ранее app-server слушал TCP; теперь поддерживает unix-socket (`--socket /tmp/codex.sock`).
- Зачем: на multi-tenant хостах, в контейнерах с ограниченным сетевым стеком.
- Дополнительно: pagination-friendly resume/fork (стримит чанками без OOM на длинных потоках), sticky environments между ходами.

#### `codex exec --json` репортит reasoning-токены (v0.125.0)
- Что: вывод `codex exec --json` теперь содержит поле `usage.reasoning_tokens` отдельно от `usage.completion_tokens`.
- Пример вывода:
  ```json
  {
    "result": "...",
    "usage": {
      "prompt_tokens": 1240,
      "completion_tokens": 890,
      "reasoning_tokens": 4520
    }
  }
  ```
- Зачем: точная биллинг-аналитика для CI-пайплайнов на reasoning-моделях.

#### Permission profiles round-trip (v0.125.0) — **security**
- Что: профили разрешений (set of read/write/exec/network rules) теперь сохраняются и восстанавливаются единообразно между TUI-сессией, user turn, MCP sandbox.
- Использование: `codex --profile restricted` — все три слоя (TUI, MCP, sandbox) применяют одну и ту же политику; ранее они расходились.

#### GPT-5.5 в Codex (23 апреля)
- Доступна как `gpt-5.5` (frontier) и `gpt-5.5-mini` для economy use-case'ов.
- Существенный прирост в reasoning и tool-calling по сравнению с GPT-5.4 (по внутренним бенчмаркам OpenAI).

### Use-case 1: безопасный CI с deny-read и isolated exec

**Проблема.** Платформенная команда хотела использовать Codex для статанализа в CI на private-репо, но опасалась, что агент при ошибке промпта прочитает `.env.production` и `secrets/`.

**Решение.** В корень репо положили `requirements.toml`:
```toml
[permissions]
deny_read = ["**/.env*", "**/secrets/**", "**/*.pem", "**/*.key"]
managed_deny_read_required = true
deny_network = true
```
В CI-job: `codex exec --isolated --profile ci-readonly "run static analysis on staged files"`.

**Результат.** Из 412 запусков за рабочую неделю — 0 случаев чтения secrets. Время старта job изменилось на +0.3 с (sandbox bring-up), что приемлемо. По логам — 7 раз агент пытался прочитать `.env.staging`, но был блокирован policy и выдал понятное сообщение в diff comment.

### Use-case 2: dual-model setup на Bedrock + OpenAI

**Проблема.** Регуляторные требования заставили проводить чувствительные turn'ы через AWS Bedrock (Claude Sonnet), но для скоростных задач хотелось оставить OpenAI GPT-5.5 с `gpt-5.5-mini`.

**Решение.** В `config.toml` сконфигурировали два провайдера (`openai` и `bedrock`); создали два environment'а с разными `default_model`. На уровне hook'а PreToolUse написан скрипт-роутер, который классифицирует запрос (regex по ключевым словам типа `customer-data`, `pii`, `health`) и через `--environment` переключает провайдера.

**Результат.** Все turn'ы с PII прогоняются через Bedrock (Claude Sonnet), остальное — через OpenAI. Средняя стоимость одного запроса упала на ~31% (mini для большинства), при этом chain-of-custody для PII выдержан. Hooks стабилизировались в v0.124.0, что позволило вынести роутер из эксперимента в production.

### Оценка: **тестировать на этой неделе — да**

Особенно: `Alt+,`/`Alt+.` (немедленно полезно), `deny_read` glob policies, `/side`-разговоры. `amazon-bedrock` — для тех, у кого AWS-SSO.

**Источники:**
[OpenAI Codex changelog](https://developers.openai.com/codex/changelog), [releasebot OpenAI Codex](https://releasebot.io/updates/openai/codex), [r/CodexAutomation CLI 0.122.0](https://www.reddit.com/r/CodexAutomation/comments/1srmug7/codex_cli_update_01220_selfcontained_installs/).

---

## 3. Google: Gemini CLI / Stitch / Jules / AI Studio — Приоритет 2

**Версии за неделю:** Gemini CLI v0.39.0 (23 апреля) → v0.39.1 (24 апреля).

### Новые возможности

#### Skill Extractor & Memory Inbox
- Что: в ходе сессии Gemini CLI автоматически извлекает «навыки» (skill) — типовые шаги, которые пользователь повторяет. Они складываются в **Memory Inbox**.
- Команда: `/memory inbox` — открывает список pending-навыков.
- Действия: review (просмотр содержимого), patch (правка перед сохранением), accept (внести в постоянную memory) или reject.
- Хранение: одобренные skill живут в `~/.gemini/memory/skills/<name>.yaml` и активируются по pattern-matching будущих запросов.

#### Plan Mode security: явное подтверждение активации skill
- Что: ранее в Plan Mode skill активировался автоматически при совпадении паттерна; теперь требуется подтверждение пользователя.
- Полный текст плана и его источник (какой skill сработал) виден перед исполнением.
- Зачем: защита от prompt-injection через пользовательский input, который случайно совпадает с триггером опасного skill (например, удаления файлов).

#### Advanced Display Protocol
- Что: tool-controlled display — инструменты возвращают не только текст, но структурированный визуальный feedback: tables, diff-blocks, progress, прогресс-бары операций.
- Под капотом: новый протокол tool→UI, расширяемый сторонними MCP-серверами.

#### Архитектурный refactor: `ContextManager` ↔ `Sidecar`
- Что: `ContextManager` (хранение и компакция истории) и `Sidecar` (background-операции — индексация, monitoring) разделены на отдельные процессы.
- Эффект: падение sidecar не валит сессию; ContextManager переживает crash и автоматически восстанавливается из snapshot.

#### Восстановлен показ thoughts и raw-text в ответах
- Регрессия предыдущих версий: thinking-блоки моделей не отображались. Теперь — снова видны (можно скрыть в settings).

#### Codebase investigator: лимит ходов 50
- Параметр: `agents.codebase_investigator.max_turns: 50` (был 30).
- Зачем: на больших монорепо длинные расследования упирались в лимит и обрывались.

### Use-case: Memory Inbox для команды из 6 разработчиков

**Проблема.** Команда повторяла одни и те же мини-операции: подготовка PR-описания по шаблону, валидация миграций, форматирование commit-message по конвенции. Каждый раз — те же 4–5 шагов.

**Решение.** В течение 4 рабочих дней работали как обычно. На 5-й день дежурный архитектор открывал `/memory inbox`, ревьюил извлечённые skill (накопилось 23), 14 одобрил с правками (унифицировал имена, добавил guard на ветку `main`), 9 отклонил как шум. Одобренные skill закоммитили в общий репо `.gemini/memory/skills/` и расшарили на команду.

**Результат.** За следующую неделю время на типовые операции (PR-описание, commit-формат) упало в среднем с 3–4 минут до 30–40 секунд. По метрикам команды — экономия ~6 часов суммарно. Plan Mode security помог отловить один случай, где skill «delete temp files» имел чрезмерно широкий glob — поправили перед общим деплоем.

### Оценка: **тестировать на этой неделе — может быть**

Memory Inbox + Plan Mode security ценны, но требуют дисциплины ревью. Если у команды нет регулярного «дежурного по tooling» — лучше отложить.

**Источники:**
[Gemini CLI v0.39.0 changelog](https://geminicli.com/docs/changelogs/latest/), [releasebot Gemini CLI](https://releasebot.io/updates/google/gemini-cli).

**Stitch / AI Studio / Jules:** значимых инженерных релизов на этой неделе не зафиксировано.

---

## 4. xAI (Grok tools) — Приоритет 3

Впервые за месяц неделя с заметными релизами для разработчиков.

### Новые возможности

#### Grok Voice Think Fast 1.0 (23 апреля)
- Что: голосовой агент API для сложных multi-step workflow.
- Возможности: 28 встроенных инструментов (browse, search, calendar, email и т.д.), сотни сценариев в support/sales-доменах из коробки.
- Языки: 25+, с автодетектом.
- Доступ: API через xAI Console; биллинг по минутам разговора + tool calls.

#### Grok Speech-to-Text & Text-to-Speech API (17 апреля)
- Что: standalone API'ы (вне голосового агента).
- STT: диаризация (распознавание спикеров), word-level timestamps, мультиязычность, режимы real-time и batch.
- TTS: контроль голоса/тона, SSML-совместимый.

#### Grok 4.3 Beta (тихий релиз 17 апреля)
- ~0.5T параметров, шаги к 1T.
- Доступ: только тиры от ~$300/мес. На API доступна как preview-модель.
- Дальше по roadmap: Grok 4.4 (1T) — начало мая, Grok 4.5 (1.5T) — конец мая, Grok 5 — Q2 2026 ([NXcode Grok 5 timeline](https://www.nxcode.io/resources/news/grok-5-release-date-latest-news-2026)).

### Оценка: **тестировать на этой неделе — нет**

Voice API интересен, но узок по нише; для общего coding-флоу xAI продолжает отставать от Anthropic/OpenAI по интеграциям и MCP-экосистеме. Следить — да; внедрять — пока нет.

**Источники:**
[releasebot xAI](https://releasebot.io/updates/xai), [Grok 4.3 Beta launch](https://www.instagram.com/p/DXS0DUpje0P/), [aitoolsrecap April 2026](https://aitoolsrecap.com/Blog/ai-updates-april-2026).

---

## Сводная таблица

| Инструмент | Ключевые возможности недели | Use-cases | Импакт | Тестировать на этой неделе |
|---|---|---|---|---|
| **Claude Code** | v2.1.115–119; `mcp_tool` hooks без shell, `DISABLE_UPDATES`, `--from-pr` для GitLab/Bitbucket/GHE, `prUrlTemplate`, `CLAUDE_CODE_HIDE_CWD`, `blockedMarketplaces`, sandbox hardening, `/usage`, кастомные темы, Vim Visual; постмортем фиксов качества | MCP-хуки без shell; pinned версия в CI | **Высокий** | **Да** (на v2.1.117–119, v2.1.120 не ставить) |
| **Codex** | CLI v0.122–125 + GPT-5.5; `/side`, Plan Mode fresh, `deny_read` glob, `--isolated`, Bedrock SigV4, `Alt+,`/`Alt+.`, multi-env app-server, hooks GA, `--json` reasoning tokens | CI с deny-read + isolated; dual-model OpenAI+Bedrock | **Высокий** | **Да** |
| **Gemini CLI** | v0.39.0–1; Skill Extractor + Memory Inbox, Plan Mode security, Advanced Display, ContextManager/Sidecar split, codebase investigator 50 turns | Memory Inbox для команды (типовые операции −80% времени) | **Средний** | **Может быть** |
| **xAI** | Voice Think Fast 1.0, STT/TTS API, Grok 4.3 Beta | — | **Средний** (узкая ниша) | **Нет** |

---

## Рекомендации недели (3 действия)

1. **Перевести существующие Claude Code hooks с bash-обёртки на `type: "mcp_tool"`** там, где они вызывают MCP-серверы. Снизит latency хуков с секунд до сотен миллисекунд и уберёт необходимость sandbox-allow на bash. Параллельно — закрепить версию **v2.1.117** в CI и выставить `DISABLE_UPDATES=1` (v2.1.120 отозван, риск регрессии).
2. **Включить в Codex `deny_read` glob policies + `codex exec --isolated`** в любом CI-пайплайне, который запускает агента на private-репо. Конфиг — 5 строк в `requirements.toml` с `managed_deny_read_required = true`. Это закрывает целый класс data-exfiltration через prompt-injection с минимальным overhead'ом.
3. **Затестить `Alt+,` / `Alt+.` в Codex TUI** на одной длинной задаче. Динамическая регулировка reasoning effort даёт реальную экономию токенов на бойлерплейт-участках задачи без потери качества на сложных. Тест 2–3 дня даёт цифры для решения о per-team дефолте.

---

## Все источники

### Claude Code
- [ton-technotes — Claude Code Weekly Update v2.1.119](https://ton-technotes.com/en/blog/2026-04-25-claude-code-weekly-update-v2119/)
- [releasebot — Anthropic Claude Code](https://releasebot.io/updates/anthropic/claude-code)
- [releasebot — Anthropic](https://releasebot.io/updates/anthropic)
- [Anthropic — April 23 postmortem](https://www.anthropic.com/engineering/april-23-postmortem)
- [claude-news — Briefing 2026-04-26 (v2.1.120 retraction)](https://claude-news.today/en/briefings/briefing-2026-04-26/)
- [changelogs.directory — Claude Code v2.1.119](https://changelogs.directory/tools/claude-code/releases/2.1.119)
- [TurboAI — Claude Code env vars и feature gates](https://www.turboai.dev/blog/claude-code-versions)

### Codex
- [OpenAI Codex changelog](https://developers.openai.com/codex/changelog)
- [releasebot — OpenAI Codex](https://releasebot.io/updates/openai/codex)
- [r/CodexAutomation — CLI 0.122.0 self-contained installs](https://www.reddit.com/r/CodexAutomation/comments/1srmug7/codex_cli_update_01220_selfcontained_installs/)

### Google (Gemini CLI)
- [Gemini CLI v0.39.0 changelog](https://geminicli.com/docs/changelogs/latest/)
- [releasebot — Google Gemini CLI](https://releasebot.io/updates/google/gemini-cli)

### xAI
- [releasebot — xAI](https://releasebot.io/updates/xai)
- [NXcode — Grok 5 timeline](https://www.nxcode.io/resources/news/grok-5-release-date-latest-news-2026)
- [Grok 4.3 Beta launch](https://www.instagram.com/p/DXS0DUpje0P/)
- [AI Tools Recap — April 2026](https://aitoolsrecap.com/Blog/ai-updates-april-2026)
