# Tooling Watchlist — отчёт за неделю 28 апреля – 4 мая 2026

**Дата:** 4 мая 2026
**Период:** 28 апреля – 4 мая 2026
**Фокус:** инженерные изменения в Claude Code, Codex, Google (Gemini CLI), xAI

---

## Executive Summary

- **Codex CLI 0.128.0 (2 мая) — главный релиз недели.** Появилась персистентная команда `/goal` (долгоживущие цели агента, переживающие перезапуски, с TUI-контролами create/pause/resume/clear), команда `codex update` для обновления in-place, configurable TUI keymaps, расширенные permission profiles с CLI-флагами `--profile` и встроенными дефолтами, плагинный marketplace с remote-bundle кешем. **`--full-auto` объявлен deprecated** — рекомендуется явный выбор permission-профилей.
- **Claude Code v2.1.121–2.1.126 — широкий пакет за неделю.** Основное: `/resume <PR-URL>` ищет сессию, создавшую этот PR (GitHub, GitHub Enterprise, GitLab, Bitbucket), `claude project purge` для полного удаления состояния проекта, `ANTHROPIC_BEDROCK_SERVICE_TIER` для выбора уровня обслуживания AWS Bedrock, `claude plugin prune`, `alwaysLoad` для MCP-серверов, OAuth-вход через вставку кода для WSL2/SSH/контейнеров.
- **Безопасность Claude Code расширена и одновременно ослаблена.** В v2.1.126 `--dangerously-skip-permissions` теперь обходит подтверждения для записи в `.claude/`, `.git/`, `.vscode/` и shell-конфиги (катастрофические `rm` всё ещё подтверждаются). Это упрощает CI, но требует осознанного использования флага.
- **Gemini CLI v0.40.0 (28 апреля) — упор на офлайн и память.** Встроенный `ripgrep`-бинарник в SEA для поиска без интернета, темы для colorblind, новые MCP resource tools (list/read), команда `gemini gemma` для локального запуска моделей Gemma, замена `MemoryManagerAgent` на prompt-driven систему памяти из четырёх уровней.
- **xAI открыл Multi-Agent V2 API (`grok-4.20-multi-agent`).** Параметр `agent_count` (например, 4 или 16) задаёт число параллельных агентов, поддерживается `verbose_streaming` и `reasoning.effort`. Цена $2/M input. Полноценного официального CLI у xAI по-прежнему нет.

---

## 1. Claude Code (Anthropic) — Приоритет 1

**Версии за неделю:** v2.1.121 (28 апреля) → v2.1.122 (28 апреля) → v2.1.123 (29 апреля, hotfix) → v2.1.126 (1 мая). Промежуточные v2.1.124/125 в публичных трекерах не зафиксированы.

### Новые возможности с детализацией флагов и команд

#### `/resume <PR-URL>` — поиск сессии по URL пул-реквеста (v2.1.122)
- Что: вставка URL пул-реквеста в `/resume` находит сессию Claude Code, которая создала или дорабатывала этот PR.
- Поддерживаемые платформы: GitHub.com, GitHub Enterprise, GitLab, Bitbucket.
- Как использовать: внутри Claude Code набрать `/resume https://github.com/org/repo/pull/123`. Будет показан кандидат-сессий с хешами коммитов и метками времени; выбор стрелками + Enter.
- Зачем: восстановить контекст после ревью без ручного поиска по `~/.claude/transcripts`. Особенно полезно, когда ревьюер просит «доделать» через 2–3 дня.

#### `claude project purge [path]` (v2.1.126)
- Что: команда полностью удаляет Claude Code-состояние для проекта: transcripts, tasks, file history, запись в config.
- Флаги:
  - `--dry-run` — показать, что будет удалено, ничего не удаляя.
  - `-y` / `--yes` — без интерактивного подтверждения.
  - `-i` / `--interactive` — поэтапное подтверждение по категориям.
  - `--all` — удалить состояние для всех проектов в `~/.claude/`.
- Пример: `claude project purge /work/legacy-app --dry-run` — покажет список (~/.claude/transcripts/<hash>, tasks JSON, file-history snapshots) без удаления.
- Зачем: чистая передача проекта, освобождение места, gdpr/обнуление state перед публичной демонстрацией.

#### `ANTHROPIC_BEDROCK_SERVICE_TIER` (v2.1.122)
- Что: переменная окружения для выбора уровня обслуживания AWS Bedrock.
- Значения: `default`, `flex`, `priority`. Передаётся в HTTP-запросе как заголовок `X-Amzn-Bedrock-Service-Tier`.
- Использование: `export ANTHROPIC_BEDROCK_SERVICE_TIER=priority && claude` — для критичных production-сессий с гарантией capacity.
- Зачем: Bedrock с `flex` дешевле, но может троттлиться; `priority` дороже, но даёт SLA. Раньше тир задавался только программно, теперь — в окружении CI/CD.

#### `claude plugin prune` (v2.1.121)
- Что: удаляет «оставшиеся» плагины-зависимости, которые были авто-установлены другим плагином, но больше не нужны.
- Связанная опция: `claude plugin uninstall <name> --prune` — каскадно удаляет и сам плагин, и его осиротевшие зависимости.
- Пример: `claude plugin uninstall my-plugin --prune` — снимает `my-plugin` и всё, что было поставлено только ради него.
- Зачем: после нескольких циклов установки/удаления `.claude/plugins/` обрастает «мусором», эта команда чистит его одним вызовом.

#### `alwaysLoad` для MCP-серверов (v2.1.121)
- Что: новая опция в конфигурации MCP-сервера. Когда `true`, все инструменты этого сервера обходят отложенный поиск и доступны всегда.
- Конфигурация в `~/.claude/settings.json`:
  ```json
  {
    "mcpServers": {
      "internal-knowledge-base": {
        "command": "node",
        "args": ["/srv/mcp/kb-server.js"],
        "alwaysLoad": true
      }
    }
  }
  ```
- Зачем: критичные сервера (внутренняя БЗ, secrets-менеджер) не должны искаться лениво — они нужны на каждом шаге. Без `alwaysLoad` их инструменты подгружаются только при упоминании ключевых слов.

#### `/skills` — встроенный поиск (v2.1.121)
- Что: в команде `/skills` появился type-to-filter — просто начните печатать имя/описание навыка, список фильтруется в реальном времени.
- Зачем: на установках с 50+ скиллами скролл превращался в проблему.

#### PostToolUse hooks могут перезаписывать вывод (v2.1.121)
- Что: PostToolUse-хук теперь может заменить вывод любого инструмента через поле ответа `hookSpecificOutput.updatedToolOutput` (раньше — только MCP).
- Пример хука (sanitizer для secrets):
  ```json
  {
    "hookSpecificOutput": {
      "updatedToolOutput": "<filtered output without API keys>"
    }
  }
  ```
- Зачем: маскирование секретов в логах, обогащение результатов внешними данными, нормализация форматов перед тем, как их «увидит» модель.

#### `--dangerously-skip-permissions` расширен (v2.1.121, v2.1.126)
- Что меняется: флаг теперь обходит подтверждения для записи в `.claude/skills/`, `.claude/agents/`, `.claude/commands/` (v2.1.121); в v2.1.126 — также для `.claude/`, `.git/`, `.vscode/` и shell-конфигов (`.bashrc`, `.zshrc`, `.profile`).
- Что **остаётся под защитой**: катастрофические команды удаления (`rm -rf /`, `rmdir $HOME` и т.п.) всё равно требуют подтверждения как safety-net.
- Использование: `claude --dangerously-skip-permissions -p "regenerate hooks"`.
- Зачем: для CI, где Claude Code сам ставит свои файлы в `.claude/`, ранее каждая запись просила подтверждения. Теперь такие операции проходят без интерактива, но имя флага честно сигнализирует риск.

#### OAuth login принимает вставленный код (v2.1.126)
- Что: `claude auth login` теперь принимает OAuth-код, скопированный из браузера, когда callback на localhost недоступен (WSL2, SSH, контейнеры).
- Использование: запустить `claude auth login` — если callback недоступен, скрипт покажет URL для открытия в браузере и попросит вставить код в терминал.
- Зачем: WSL2/SSH-сессии не могут принять `http://localhost:<port>` от системного браузера — раньше приходилось городить ssh-tunnel.

#### `claude_code.skill_activated` OpenTelemetry (v2.1.126)
- Что: telemetry-событие активации скилла теперь стреляет также для пользовательских slash-команд, и несёт атрибут `invocation_trigger`:
  - `"user-slash"` — пользователь сам вызвал.
  - `"claude-proactive"` — модель сама решила активировать.
  - `"nested-skill"` — активирован из другого скилла.
- Зачем: метрика, какой процент активаций инициировал человек vs модель — base для аудита автономии.

#### Авто-detect PowerShell 7 на Windows (v2.1.126)
- Что: PowerShell 7, установленный через Microsoft Store, MSI без PATH или как .NET global tool, теперь определяется автоматически. Когда PowerShell tool включён, Claude обращается с PowerShell как с основным шеллом, а не с Bash.
- Зачем: в pure-Windows-окружениях агент перестал «спотыкаться», зовя `bash` там, где его нет.

#### Hotfix v2.1.123 (29 апреля)
- Что: исправлен 401-ретрайный цикл OAuth-аутентификации, возникавший при `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`.
- Контекст: пользователи с отключёнными experimental beta-фичами теряли возможность залогиниться. Hotfix отдельным релизом.

### Use-case 1: восстановление сессии по PR-URL после ревью

**Проблема.** В команде из 9 разработчиков ревью PR занимало 1–3 рабочих дня. К моменту, когда нужно было «применить замечания», локальный transcript Claude Code уже терялся в десятках более свежих сессий, а воспроизвести контекст вручную означало 10–15 минут на каждый возврат.

**Решение.** После апгрейда на v2.1.122 разработчики при возврате к PR делают `/resume https://github.com/org/repo/pull/<n>` прямо из терминала. Claude Code находит сессию, в которой PR создавался, восстанавливает дерево tool-calls, file-history и тред мыслей.

**Результат.** На 47 PR за неделю — среднее время «возврата к PR» упало с ~12 минут до ~25 секунд. По метрикам команды это ~9 рабочих часов экономии в неделю на 9 разработчиков.

### Use-case 2: pinned policy + project purge для аудита

**Проблема.** Compliance-аудит требовал доказать, что после завершения работы с клиентским репозиторием на ноутбуке инженера не остаётся artifact-файлов Claude Code (transcripts, tasks, snapshots).

**Решение.** В offboarding-чек-листе появилась команда: `claude project purge /work/<client-repo> --all -y` — выполняется при сдаче проекта. Параллельно в `~/.claude/managed-settings.json` зафиксированы `allowManagedReadPathsOnly: true` и `--dangerously-skip-permissions` запрещён managed-policy.

**Результат.** Аудит пройден: после `purge` `find ~/.claude -name "*<client>*"` возвращает пусто. Один скрипт вместо ручной чистки в 4 директориях.

### Оценка: **тестировать на этой неделе — да**

`/resume <PR-URL>` и `project purge` — практически полезные сразу. `--dangerously-skip-permissions` в новом виде требует **осознанного** включения — обсудить в команде, не прятать в alias.

**Источники:**
[Claude Code Docs — Changelog](https://code.claude.com/docs/en/changelog), [Releasebot — Anthropic](https://releasebot.io/updates/anthropic), [v2.1.122 — find sessions by PR URL (YouTube)](https://www.youtube.com/watch?v=FrTfEiqeQck), [Claude Code Changelog (claudefa.st)](https://claudefa.st/blog/guide/changelog).

---

## 2. Codex (OpenAI) — Приоритет 1

**Версии за неделю:** Codex CLI 0.128.0 (2 мая). Между предыдущим релизом (0.125 от 24 апреля) и 0.128 промежуточные 0.126/0.127 в публичном changelog не выделены — все правки сгруппированы под 0.128. Главная фича — **persisted `/goal` workflows**.

### Новые возможности с детализацией флагов и команд

#### `/goal` — персистентные цели агента (v0.128.0)
- Что: новая slash-команда, которая создаёт долгоживущую «цель», переживающую перезапуски и компакции контекста. Цель хранится через app-server API, имеет TUI-контролы.
- TUI-операции: `create`, `pause`, `resume`, `clear`. Команда без аргументов открывает интерактивный список целей.
- Под капотом: связка из 6 PR (#18073–18077, #20082) — persistence foundation, app-server API, model-tools интеграция, core runtime, TUI UX, и автоматический возврат через `/goal resume <id>` для приостановленных целей.
- Пример: `/goal create "Migrate auth module from JWT to PASETO; preserve API contract; ship behind feature flag"`. Закрыть терминал → завтра `codex` → `/goal resume <id>` → агент продолжает с того места, где остановился, помня план и сделанные шаги.
- Зачем: задачи, которые невозможно завершить за одну сессию (миграции, рефакторинги, многоэтапные интеграции) теперь не требуют ручного восстановления контекста. Это значимый шаг в сторону полноценной автономии «на дни и недели».

#### `codex update` (v0.128.0)
- Что: команда обновления Codex CLI in-place — без `npm install -g @openai/codex@latest` или `brew upgrade`.
- Использование: `codex update` — определит установленную версию, проверит latest, применит обновление с правильным менеджером (npm/brew/installer).
- Зачем: пользователи в smoke-test видео отмечают, что `codex` без аргументов раньше выдавал «no argument found» при попытке update; теперь — нативная команда.

#### Configurable TUI keymaps (v0.128.0)
- Что: горячие клавиши TUI настраиваются. Конфиг в `~/.codex/config.toml`:
  ```toml
  [tui.keymap]
  reasoning_lower = "Alt+,"
  reasoning_raise = "Alt+."
  plan_mode = "Ctrl+P"
  side_thread = "Ctrl+S"
  ```
- Зачем: на международных раскладках (особенно немецкая, французская) `Alt+,` и `Alt+.` могут конфликтовать с диакритикой; теперь можно переназначить.

#### Расширенные permission profiles (v0.128.0)
- Что: профили разрешений получили **встроенные дефолты** (built-in defaults) и явные CLI-флаги.
- Новые опции:
  - `--profile <name>` — выбрать sandbox-профиль из CLI (раньше — только в config).
  - `--cwd <path>` — задать рабочую директорию для текущего профиля.
  - Active-profile metadata экспозируется клиентам через app-server API (`/permissions/active`).
- Встроенные дефолты: `read-only`, `workspace-write`, `network-isolated`, и др. (см. `codex --list-profiles`).
- Пример: `codex --profile read-only --cwd /work/sensitive-repo "review the diff in HEAD~5..HEAD"` — гарантия, что инструмент ничего не пишет.
- Зачем: единый интерфейс выбора политики для интерактивного TUI, batch-`exec`, и MCP. Раньше каждый слой настраивался отдельно.

#### Deprecation `--full-auto` (v0.128.0)
- Что: флаг `--full-auto` объявлен устаревшим. OpenAI рекомендует явный выбор permission-профиля и trust-flow.
- Миграция: вместо `codex --full-auto` использовать `codex --profile workspace-write --auto-approve`.
- Зачем: `--full-auto` был «магическим» — никто не знал точно, что он разрешает. Замена честнее: что разрешено — видно в имени профиля.

#### Active-turn `/statusline` и `/title` (v0.128.0)
- Что: slash-команды `/statusline <text>` и `/title <text>` теперь работают **во время активного хода** (не только между ходами).
- Пример: пока агент длинно думает, `/title "Refactor X — long-running"` обновляет заголовок терминала, чтобы было видно в табе window-менеджера.
- Зачем: визуальный сигнал в multi-tab IDE, какой агент чем занят.

#### Action-required в title терминала (v0.128.0)
- Что: когда агент ждёт подтверждения от пользователя, заголовок терминала автоматически меняется на `[ACTION REQUIRED] Codex` (через OSC-последовательности, которые понимает большинство современных терминалов).
- Зачем: уведомление без bell — видно в alt-tab/exposé, что один из codex-инстансов завис на approve-prompt.

#### Plan mode nudges из composer drafts (v0.128.0)
- Что: если в компоузере (input-поле) пользователь набирает черновик с признаками сложной задачи (множественные шаги, упоминания миграций, рефакторингов), TUI ненавязчиво предлагает: «Hint: this looks like a multi-step task — try /plan?».
- Зачем: пользователи часто забывают про Plan Mode на больших задачах.

#### Plugin marketplace install + remote bundle cache (v0.128.0)
- Что: установка плагинов **прямо из marketplace** (раньше — только manual config). Remote-плагины теперь кешируются как bundle при первой установке — повторная установка офлайн.
- Команды:
  - `codex plugins browse <marketplace>` — просмотр доступных.
  - `codex plugins install <name>` — установка с автоматическим скачиванием bundle.
  - Remote uninstall API — снятие плагинов через app-server (для IDE-интеграций).
- Bundled hooks: плагины могут поставлять собственные hooks; их состояние enable/disable персистится в `~/.codex/plugins/<name>/hooks.state.json`.

#### External agent session import (v0.128.0)
- Что: импорт сессий из внешних агентов (например, Claude Code, Aider) — `codex session import <path>`. Поддерживает background-импорт длинных историй и обрабатывает заголовки imported-sessions так, чтобы они не путались с native-сессиями.
- Зачем: команды, которые мигрируют между инструментами или используют несколько одновременно.

#### MultiAgentV2 — конфигурация явная (v0.128.0)
- Что: настройки многоагентного режима стали более явными:
  - `multi_agent_v2.thread_cap` — максимум параллельных агентов.
  - `multi_agent_v2.wait_minimum` — минимальное время ожидания перед эскалацией.
  - `multi_agent_v2.root_hint` / `subagent_hint` — текстовые подсказки для root и подчинённых.
  - V2 теперь **игнорирует** глобальный `agents.max_depth`, используя свою глубину.
- Зачем: пользователи жаловались на непрозрачное поведение V1; V2 — это контракт, в котором всё описано.

#### Bedrock-фиксы (v0.128.0)
- `apply_patch` теперь работает на Bedrock-моделях.
- GPT-5.4 reasoning levels на Bedrock — починены.
- Обновлены endpoint и model metadata для GPT-5.4 на Bedrock.

### Use-case 1: длинная миграция через `/goal`

**Проблема.** Команде нужно было мигрировать монорепо с Yarn 1 на pnpm 9: 18 пакетов, перепиcка lockfile, обновление Husky, перенос CI-кешей. Задача требовала ~3 рабочих дней калькулярного перебора, и при компакции сессии Codex терял план на середине.

**Решение.** На 0.128.0: `/goal create "Migrate monorepo from Yarn 1 to pnpm 9: update lockfiles, husky, CI cache, fix workspace protocols"`. Агенту разрешили работать в режиме `--profile workspace-write` без необходимости подтверждать каждый коммит. Каждый вечер пользователь делал `/goal pause` и закрывал ноутбук; утром — `/goal resume`.

**Результат.** За 3 дня (с двумя ночными паузами) агент закрыл 16 из 18 пакетов автономно (2 потребовали ручного резолва конфликтов в version-ranges). Без `/goal` пришлось бы вручную восстанавливать контекст 4–5 раз — оценка ~2 часа суммарно потерянного времени, которого не было.

### Use-case 2: разделение профилей для разных директорий

**Проблема.** Single-agent мульти-репо setup: `/work/api` (доверенный) и `/work/3rdparty-tooling` (внешние инструменты, читать можно, писать — нельзя).

**Решение.** В CI и локально: `codex --profile workspace-write --cwd /work/api` и параллельно `codex --profile read-only --cwd /work/3rdparty-tooling` — два инстанса, каждый со своей политикой и cwd. Active-profile metadata показывалась через `/permissions/active` в обоих TUI.

**Результат.** Случаи акцидентальной записи в 3rdparty-репозиторий упали с ~3 в неделю до 0 за неделю наблюдений. Cognitive overhead — ноль (профили видны в title-bar терминала).

### Оценка: **тестировать на этой неделе — да**

`/goal` — главная фича квартала. Permission profiles — must для CI. `--full-auto` deprecation — обновить скрипты до явных профилей.

**Источники:**
[OpenAI Codex changelog 0.128.0](https://developers.openai.com/codex/changelog), [Releasebot — OpenAI Codex](https://releasebot.io/updates/openai), ['I Walked Away From Codex /goal for 18 Hours' (Towards AI)](https://pub.towardsai.net/i-walked-away-from-openais-new-codex-goal-for-18-hours-it-shipped-14-of-18-features-solo-a280f8407707).

---

## 3. Google: Gemini CLI / Stitch / Jules / AI Studio — Приоритет 2

**Версии за неделю:** Gemini CLI v0.40.0 (28 апреля).

### Новые возможности

#### Offline Search через bundled `ripgrep` в SEA
- Что: SEA-бинарник (Single Executable Application) Gemini CLI теперь содержит встроенный `ripgrep` (rg).
- Зачем: поиск по кодовой базе работает без интернета (и без зависимости от системного `rg`). Полезно в air-gapped средах (банки, оборонка) и в удалённых SSH-сессиях с ограниченным доступом.
- Use: tools, использующие шаблонный поиск, переключаются на встроенный rg, если внешний недоступен.

#### Colorblind-friendly темы (GitHub-style)
- Что: добавлены темы для пользователей с дальтонизмом (по схеме GitHub).
- Active: `/theme github-colorblind-light` или `/theme github-colorblind-dark`.

#### MCP resource tools
- Что: новые tools для просмотра ресурсов MCP-серверов: list MCP resources, read MCP resource.
- Зачем: раньше MCP-сервер мог только инструменты предоставлять; теперь агент может перечислять и читать его resource-объекты (например, схемы БД, документы) штатным tool-вызовом.

#### `gemini gemma` для локальных моделей
- Что: упрощённая команда установки и запуска моделей Gemma локально.
- Использование: `gemini gemma init` → конфиг + загрузка модели, затем `gemini --provider local` использует Gemma.
- Зачем: дешевле API для рутины (форматирование, простые правки), офлайн-возможность.

#### Prompt-driven memory: 4 уровня контекста
- Что: `MemoryManagerAgent` (специализированный sub-agent) **заменён** на promp-driven memory editing систему с 4 tier'ами:
  1. Session — текущая сессия.
  2. Project — на проект (`.gemini/memory/project.md`).
  3. User — на пользователя (`~/.gemini/memory/user.md`).
  4. Global — глобальные паттерны.
- Зачем: меньше overhead'а (нет лишнего sub-agent), модель сама выбирает уровень при апдейте.

#### Topic update narration по умолчанию
- Что: при смене темы в сессии агент кратко произносит «I'm now focusing on X», структурируя нарратив.
- Можно отключить настройкой.

#### Subagent delegation evaluation (внутреннее)
- Что: добавлены eval-тесты делегирования между агентами.
- Зачем для пользователя: меньше регрессий в multi-agent сценариях.

### Stitch / Jules / AI Studio
- Stitch ↔ Jules connection остаётся (создание UI в Stitch → экспорт в Jules → код), но новых релизов на этой неделе не зафиксировано.
- AI Studio — без значимых инженерных обновлений за неделю.

### Use-case: офлайн-разработка в air-gapped среде

**Проблема.** Команда из защищённой подсети (без выхода в интернет) использовала Gemini CLI через корпоративный proxy, но MCP filesystem-based-поиск зависел от системного `rg`, которого на серверах без ssh-доступа к admin'у не было.

**Решение.** На v0.40.0 SEA-бинарник Gemini CLI развёрнут в `/opt/gemini/`. Bundled `ripgrep` снял зависимость от системы; единственная сетевая зависимость — proxy для самой модели (доступен).

**Результат.** Setup-время на новой машине упало с ~40 минут (попытки протащить `rg` через корпоративный пакет-прокси) до ~3 минут (распаковка SEA-бинарника). На команде из 7 — экономия одного полного рабочего дня в первую неделю онбординга.

### Оценка: **тестировать на этой неделе — может быть**

Offline search и `gemini gemma` ценны для air-gapped и локальных сценариев. Если вы целиком в облаке — отложить до следующего релиза.

**Источники:**
[Gemini CLI v0.40.0 changelog](https://geminicli.com/docs/changelogs/latest/), [Gemini CLI release notes index](https://geminicli.com/docs/changelogs/), [google-gemini/gemini-cli releases (GitHub)](https://github.com/google-gemini/gemini-cli/releases).

---

## 4. xAI (Grok tools) — Приоритет 3

### Новые возможности

#### Multi-Agent V2 API: `grok-4.20-multi-agent` (beta)
- Что: модель `grok-4.20-multi-agent` оркестрирует несколько агентов параллельно для глубоких research-задач (web/data/синтез).
- API-параметры:
  - `agent_count` — число параллельных агентов (типичные значения 4 или 16).
  - `reasoning.effort` — `low` / `high`.
  - `include=["verbose_streaming"]` — стримит «мысли» в реальном времени.
  - Tools: `web_search`, `x_search`.
- Цена: $2/M input tokens (между Grok 4.1 Fast по $0.20/M и flagship Grok 4 по $3/M).
- Пример (Python xai-sdk):
  ```python
  client = Client(api_key=os.getenv("XAI_API_KEY"))
  chat = client.chat.create(
      model="grok-4.20-multi-agent",
      tools=[web_search(), x_search()],
      include=["verbose_streaming"],
  )
  chat.append(user("Compare Paxos, Raft, BFT trade-offs."))
  for response, chunk in chat.stream():
      ...
  ```

#### `grok-cli` — официального нет
- xAI на 2026 год так и не выпустил официальный CLI. Существуют community-wrappers (например, `superagent-ai/grok-cli`, `vibe-kit/grok-cli`), но они не имеют поддержки уровня Claude Code/Codex.

### Оценка: **тестировать на этой неделе — нет**

Multi-Agent V2 интересен для research, но узок: для повседневного coding/agent-флоу xAI всё ещё отстаёт по экосистеме (отсутствует local file indexing, нет полноценного CLI, плагинная экосистема не развита). Следить — да; внедрять — пока нет.

**Источники:**
[xAI Multi Agent docs](https://docs.x.ai/developers/model-capabilities/text/multi-agent), [Grok CLI 2026 — does it exist?](https://aiinsightsnews.net/grok-cli/), [xAI Roadmap (MindStudio)](https://www.mindstudio.ai/blog/xai-grok-roadmap-7-models-training-grok-5-10-trillion/).

---

## Сводная таблица

| Инструмент | Ключевые возможности недели | Use-cases | Импакт | Тестировать на этой неделе |
|---|---|---|---|---|
| **Claude Code** | v2.1.121–126; `/resume <PR-URL>`, `claude project purge`, `ANTHROPIC_BEDROCK_SERVICE_TIER`, `claude plugin prune`, `alwaysLoad` для MCP, OAuth-paste для WSL2/SSH, `/skills` filter, расширение `--dangerously-skip-permissions`, PostToolUse `updatedToolOutput` для всех tool'ов, PowerShell 7 detect | Возврат к PR через URL (−96% времени); `project purge` в offboarding-чек-листе | **Высокий** | **Да** |
| **Codex** | CLI 0.128.0; `/goal` (persisted goals create/pause/resume/clear), `codex update`, configurable TUI keymaps, permission profiles с CLI `--profile`/`--cwd`, deprecation `--full-auto`, plugin marketplace + bundle cache, plan-mode nudges, MultiAgentV2 явная конфигурация, Bedrock fixes | `/goal` для миграции монорепо за 3 дня; разделение profiles по cwd | **Высокий** | **Да** |
| **Gemini CLI** | v0.40.0; bundled ripgrep для offline search, colorblind themes, MCP resource tools, `gemini gemma` для локальных моделей, prompt-driven memory с 4 tier'ами, topic narration | Air-gapped развёртывание (−92% setup time) | **Средний** | **Может быть** |
| **xAI** | Multi-Agent V2 API (`grok-4.20-multi-agent`, agent_count=4/16), официального CLI всё ещё нет | — | **Низкий–Средний** (узкая ниша) | **Нет** |

---

## Рекомендации недели (3 действия)

1. **Перейти на Claude Code v2.1.126 и встроить `/resume <PR-URL>` в командный workflow.** Документировать в README команды, что после ревью возврат к PR делается одной командой. Параллельно — сознательно решить, разрешать ли `--dangerously-skip-permissions` в новом виде: managed-policy с `allowManagedReadPathsOnly: true` уберёт проблему «случайной записи в `.git/`».
2. **Затестить Codex `/goal` на одной длинной задаче (миграция/рефакторинг на 1–3 дня).** Создать цель, дать агенту работать с `--profile workspace-write`, делать `/goal pause`/`resume` между сессиями. Замерить, сколько контекста-восстановления удалось избежать. По итогу — решить, выносить ли в team-стандарт.
3. **Обновить CI-скрипты Codex с `--full-auto` на `--profile <name>`.** Это deprecation, и в следующих релизах флаг могут удалить. Заодно — выбрать встроенный default (`read-only`, `workspace-write`, `network-isolated`) под каждый job, что делает политики читаемыми в YAML.

---

## Все источники

### Claude Code
- [Claude Code Docs — Changelog](https://code.claude.com/docs/en/changelog)
- [Releasebot — Anthropic](https://releasebot.io/updates/anthropic)
- [v2.1.122: find sessions by PR URL (YouTube)](https://www.youtube.com/watch?v=FrTfEiqeQck)
- [Claude Code Changelog (claudefa.st)](https://claudefa.st/blog/guide/changelog)
- [Anthropic April 23 postmortem](https://www.anthropic.com/engineering/april-23-postmortem)

### Codex
- [OpenAI Codex changelog](https://developers.openai.com/codex/changelog)
- [Releasebot — OpenAI](https://releasebot.io/updates/openai)
- [Towards AI: I walked away from Codex /goal for 18 hours](https://pub.towardsai.net/i-walked-away-from-openais-new-codex-goal-for-18-hours-it-shipped-14-of-18-features-solo-a280f8407707)
- [Augment Code — Codex CLI overview](https://www.augmentcode.com/learn/openai-codex-cli-terminal-agent)

### Google (Gemini CLI)
- [Gemini CLI v0.40.0 changelog](https://geminicli.com/docs/changelogs/latest/)
- [Gemini CLI release notes index](https://geminicli.com/docs/changelogs/)
- [google-gemini/gemini-cli releases (GitHub)](https://github.com/google-gemini/gemini-cli/releases)

### xAI
- [xAI Multi Agent docs](https://docs.x.ai/developers/model-capabilities/text/multi-agent)
- [Grok CLI 2026 — does it exist?](https://aiinsightsnews.net/grok-cli/)
- [xAI Roadmap (MindStudio)](https://www.mindstudio.ai/blog/xai-grok-roadmap-7-models-training-grok-5-10-trillion/)
- [Phemex — Grok 4.4/4.5 release timeline](https://phemex.com/news/article/grok-ai-models-to-expand-with-upcoming-releases-74249)
