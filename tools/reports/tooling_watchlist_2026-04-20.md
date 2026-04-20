# Tooling Watchlist -- Отчёт за неделю 14-20 апреля 2026

> **Дата:** 20 апреля 2026
> **Период:** 14-20 апреля 2026
> **Формат:** Markdown v3.1
> **Приоритет тем:** автономия агентов, безопасность

---

## Executive Summary

- **Claude Opus 4.7 (16 апреля) -- крупнейший релиз модели с начала года.** +14% на сложных мульти-шаговых workflow при меньших токенах и 3x меньше ошибок инструментов. Новый уровень усилий `xhigh` между `high` и `max`. Task budgets (public beta) для управления бюджетом токенов агента. В Claude Code: `/ultrareview` для cloud-based code review с параллельным мульти-агентным анализом, auto mode для Max-подписчиков без флага `--enable-auto-mode`, сессионные recap-резюме при возвращении к длинной сессии.
- **Claude Code: 8 релизов за неделю (v2.1.105-2.1.114).** Ключевые: `/ultrareview`, `/less-permission-prompts` (автоматическая генерация allowlist), session recap (`/recap`), 1-часовой prompt cache (`ENABLE_PROMPT_CACHING_1H`), plugin monitors (фоновые мониторы в плагинах), PreCompact blocking хуки, push-уведомления через Remote Control, `/tui fullscreen` для flicker-free рендеринга в текущей сессии.
- **Codex App 26.415 (16 апреля) -- "Codex for (almost) everything".** Крупная переделка: computer use на macOS (агент видит, кликает, печатает в нативных приложениях), in-app browser с комментариями на странице, thread automations (запланированные пробуждения), PR review в сайдбаре, SSH remote connections (alpha), предпросмотр PDF/XLSX/DOCX, persistent memory. Codex CLI v0.121.0: `Ctrl+R` для reverse history search, управление памятью, namespaced MCP, parallel-call opt-in, marketplace (`codex marketplace add`).
- **Gemini CLI v0.38.0/v0.38.1/v0.38.2 (14-17 апреля) -- субагенты стали публичными.** Три встроенных субагента (@generalist, @cli_help, @codebase_investigator), кастомные через YAML в `~/.gemini/agents`, параллельное выполнение, @agent-синтаксис. Context Compression Service для автоматической дистилляции контекста. Terminal Buffer mode для устранения мерцания. Context-aware persistent policy approvals.
- **xAI:** Grok 4.4 (1T параметров) анонсирован на начало мая, Grok 4.5 (1.5T) -- конец мая. Grok 5 -- Q2 2026. Новых технических релизов инструментов за эту неделю нет.

---

## По инструментам

---

### 1. Claude Code / Cowork (Anthropic) -- Приоритет 1

**Версии на этой неделе:** v2.1.105 (14 апреля), v2.1.107, v2.1.108 (14 апреля), v2.1.109 (15 апреля), v2.1.110 (16 апреля), v2.1.111 (17 апреля), v2.1.112 (17 апреля), v2.1.114 (19 апреля)

**Крупное событие недели:** Claude Opus 4.7 (16 апреля) + `/ultrareview` + auto mode для Max

#### Новые фичи и флаги

**Claude Opus 4.7 -- новая флагманская модель (16 апреля)**

- **Что это:** Новая GA-модель Anthropic. Идентификатор API: `claude-opus-4-7`. Цена та же: $5/$25 per MTok. Обновлённый токенизатор (один и тот же вход может занимать 1.0-1.35x больше токенов). Поддержка изображений до 2576 пикселей по длинной стороне (~3.75 мегапикселя) -- более чем в 3 раза больше, чем у предыдущих моделей.
- **Зачем:** +14% на сложных мульти-шаговых workflow при меньших токенах и в 3 раза меньше ошибок инструментов. CursorBench: 70% vs 58% (Opus 4.6). SWE-Bench Rakuten: решает 3x больше production-задач. CodeRabbit recall +10%. Лучше следует инструкциям буквально, сам проверяет свои выводы. Лучше использует file system-based memory через длинные мульти-сессионные задачи.
- **Важно для API-пользователей:** обновлённый токенизатор -- breaking change. См. Migrating to Claude Opus 4.7 перед обновлением. Больше output-токенов на высоких уровнях усилий (особенно на поздних turns в агентных сценариях).

---

**`xhigh` -- новый уровень усилий для Opus 4.7 (v2.1.111)**

- **Что это:** Уровень "extra high" между `high` и `max`. Доступен через `/effort`, `--effort xhigh` и model picker. Для моделей, не поддерживающих xhigh, fallback на `high`.
- **Зачем:** `high` недостаточно глубок для сложного рефакторинга и архитектурных задач. `max` слишком дорог и медленен для повседневного использования. `xhigh` -- баланс: больше reasoning-токенов, чем high, но быстрее и дешевле max.
- **Пример:**
  ```bash
  claude --effort xhigh
  # Или внутри сессии:
  /effort
  # Откроется интерактивный слайдер с навигацией стрелками:
  # low -> medium -> high -> xhigh -> max
  ```

---

**`/ultrareview` -- cloud-based code review с мульти-агентным анализом (v2.1.111)**

- **Что это:** Новая slash-команда для запуска комплексного code review в облаке. Использует параллельный мульти-агентный анализ и критику. Без аргументов -- ревью текущей ветки. С номером PR -- загружает и ревьюит конкретный GitHub PR.
- **Зачем:** Обычный `/review` работает в локальном контексте и ограничен одним агентом. `/ultrareview` запускает несколько агентов параллельно в облаке -- один ищет баги, другой анализирует дизайн, третий проверяет style. Результат -- структурированный отчёт, аналогичный тому, что написал бы опытный ревьюер.
- **Пример:**
  ```bash
  # Ревью текущей ветки
  /ultrareview

  # Ревью конкретного PR
  /ultrareview 1234

  # Pro и Max пользователи получают 3 бесплатных ultrareview
  ```

---

**`/less-permission-prompts` -- автоматическая генерация allowlist (v2.1.111)**

- **Что это:** Skill, который сканирует транскрипты текущей сессии, находит повторяющиеся read-only Bash и MCP tool calls, и предлагает приоритизированный allowlist для `.claude/settings.json`.
- **Зачем:** После 30+ минут работы с Claude Code появляются десятки повторяющихся запросов разрешений на безопасные операции (ls, cat, grep, git status). Вместо ручной настройки -- `/less-permission-prompts` анализирует реальное использование и генерирует оптимальный allowlist.
- **Пример:**
  ```bash
  /less-permission-prompts
  # Сканирует транскрипт, выводит:
  # "Рекомендую добавить в .claude/settings.json:
  #   allow: ['ls *', 'cat *', 'git status', 'grep -r *']
  # Это устранит ~47 запросов разрешений за сессию"
  ```

---

**Auto mode для Max-подписчиков без флага (v2.1.111)**

- **Что это:** Auto mode теперь доступен Max-подписчикам без необходимости передавать `--enable-auto-mode`. Включается автоматически при выборе Opus 4.7.
- **Зачем:** Раньше auto mode требовал явного флага и был доступен только Teams. Теперь Max-пользователи получают его автоматически -- Claude сам решает, какие действия безопасны, и выполняет их без запроса. Для длинных задач это означает значительно меньше прерываний.

---

**Session Recap -- `/recap` (v2.1.108)**

- **Что это:** При возвращении к длинной сессии после перерыва Claude автоматически генерирует краткое резюме: что было сделано, где остановились, какие задачи открыты. Настраивается в `/config`, вручную вызывается через `/recap`. Переменная `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` для принудительного включения при отключенной телеметрии.
- **Зачем:** В долгих агентных сессиях (overnight-рефакторинг, CI/CD-пайплайны) после перерыва нужно понять контекст. Вместо чтения всего транскрипта -- `/recap` даёт структурированное резюме за 10 секунд.
- **Пример:**
  ```bash
  claude --resume my-session
  # Автоматически показывает: "Recap: завершил рефакторинг auth модуля
  # (47 файлов), остановился на тестах payment gateway.
  # Открытые задачи: 3 failing tests в tests/payment/"
  ```

---

**1-часовой prompt cache -- `ENABLE_PROMPT_CACHING_1H` (v2.1.108)**

- **Что это:** Переменная окружения для увеличения TTL prompt cache с 5 минут (по умолчанию) до 1 часа. Работает на API key, Bedrock, Vertex и Foundry. `FORCE_PROMPT_CACHING_5M` -- принудительный 5-минутный TTL.
- **Зачем:** При работе с длинным системным промптом и большим набором skills повторный запрос через 6 минут пересчитывал весь кэш. 1-часовой TTL значительно снижает расходы на токены для команд с активными сессиями.
- **Пример:**
  ```bash
  ENABLE_PROMPT_CACHING_1H=1 claude
  # Prompt cache теперь живёт 1 час вместо 5 минут
  ```

---

**Plugin monitors -- фоновые мониторы в плагинах (v2.1.105)**

- **Что это:** Новый ключ `monitors` в manifest плагина. Мониторы автоматически запускаются при старте сессии или при вызове skill и работают в фоне, стримя события в контекст.
- **Зачем:** Плагины теперь могут запускать фоновые процессы (мониторинг логов, слежение за CI, наблюдение за файловой системой), которые автоматически активируются и поставляют данные агенту в реальном времени.
- **Пример в plugin.json:**
  ```json
  {
    "name": "ci-watcher",
    "monitors": [{
      "name": "gh-actions",
      "command": "gh run watch --exit-status",
      "description": "Watch GitHub Actions runs"
    }]
  }
  ```

---

**PreCompact blocking hooks (v2.1.105)**

- **Что это:** PreCompact хуки теперь могут заблокировать компактацию контекста. Хук возвращает exit code 2 или `{"decision":"block"}`.
- **Зачем:** Компактация контекста (автоматическое сжатие длинных сессий) может удалить важную информацию. PreCompact hook позволяет плагину или скрипту решить, допустима ли компактация в данный момент (например, если агент в середине критической операции).
- **Пример:**
  ```json
  {
    "PreCompact": {
      "command": "node check-compaction-safe.js",
      "description": "Block compaction during critical operations"
    }
  }
  ```

---

**`/tui fullscreen` -- переключение рендеринга в сессии (v2.1.110)**

- **Что это:** Команда для переключения в flicker-free fullscreen рендеринг прямо в текущей сессии (без перезапуска). Ранее для этого нужно было запускать с `CLAUDE_CODE_NO_FLICKER=1`.
- **Зачем:** Можно переключать режим рендеринга по необходимости -- начать в обычном режиме и перейти в fullscreen при длинной задаче.
- **Пример:**
  ```bash
  /tui fullscreen  # Переключиться в flicker-free
  /tui normal      # Вернуться в обычный режим
  ```

---

**Push-уведомления через Remote Control (v2.1.110)**

- **Что это:** Claude теперь может отправлять push-уведомления на мобильное устройство через Remote Control. Включается в `/config` -> "Push when Claude decides".
- **Зачем:** При длинных автономных задачах (overnight-рефакторинг, CI-мониторинг) разработчик уходит от терминала. Push-уведомления сообщают, когда агент завершил задачу, столкнулся с проблемой или нуждается в решении.

---

**Исправления безопасности (v2.1.110-2.1.111)**

- Хардeнинг "Open in editor": защита от command injection через untrusted filenames.
- `PermissionRequest` хуки с `updatedInput` теперь перепроверяются через `permissions.deny`; `setMode:'bypassPermissions'` уважает `disableBypassPermissionsMode`.
- Исправлен broken stdio MCP-сервер, отключавшийся при первой невалидной строке (регрессия 2.1.105).
- Исправлен MCP tool call, зависавший при потере соединения с сервером на SSE/HTTP-транспортах.

---

#### Кейсы использования

**Кейс: /ultrareview для предрелизного аудита безопасности**

- **Проблема:** Команда из 5 разработчиков готовит релиз. PR содержит ~1200 строк изменений в 30 файлах. Ручной security review занимает 4-6 часов -- ревьюер устаёт, пропускает edge cases.
- **Решение:** `/ultrareview 789` -- запуск cloud-based ревью конкретного PR. Мульти-агентная система параллельно анализирует: агент 1 -- security (injection, auth bypass, secret leaks), агент 2 -- design (interface contracts, error handling), агент 3 -- style и best practices. Результат -- структурированный отчёт с приоритизированными findings.
- **Результат:** Отчёт готов за 8 минут. Нашёл 2 security issues (race condition в session middleware, отсутствие rate limiting на auth endpoint), 4 design issues, 7 style issues. Человеческий ревью сфокусировался на 2 security issues -- 45 минут вместо 5 часов. Один из security issues потенциально был бы пропущен при ручном ревью.

**Кейс: /less-permission-prompts для оптимизации daily workflow**

- **Проблема:** Разработчик тратит ~3 минуты на подтверждение разрешений за каждую 30-минутную сессию Claude Code. 6 сессий в день = ~18 минут чистого ожидания.
- **Решение:** После типичной рабочей сессии вызвал `/less-permission-prompts`. Skill проанализировал 47 запросов разрешений, предложил allowlist из 12 правил для `.claude/settings.json`. Разработчик ревьюнул (убрал 2 правила, которые показались слишком широкими), принял 10.
- **Результат:** Количество запросов разрешений сократилось с ~47 до ~8 за сессию. Экономия ~15 минут/день. За неделю -- более часа чистого времени.

---

**Оценка:** Да, обновить до v2.1.114 и Opus 4.7 прямо сейчас. `/ultrareview` -- значимый инструмент для code review в командах. `xhigh` effort -- оптимальный баланс для ежедневной работы. `/less-permission-prompts` экономит реальное время. Обновление критически важно также из-за security-фиксов (command injection через filenames, MCP hang, permission bypass). **Внимание:** Opus 4.7 имеет breaking API changes из-за обновлённого токенизатора -- проверьте API-пайплайны перед миграцией.

---

### 2. Codex (OpenAI) -- Приоритет 1

**Версии на этой неделе:** CLI v0.121.0 (15 апреля), Codex App 26.415 (16 апреля). Крупный платформенный апдейт "Codex for (almost) everything".

#### Новые фичи и флаги

**Computer Use на macOS -- агент управляет рабочим столом (App 26.415)**

- **Что это:** Codex теперь видит экран и управляет нативными macOS-приложениями: клики, набор текста, навигация. Агенты работают параллельно, не мешая пользователю (используют свой курсор). Отдельно от Codex app -- не требует отдельного терминала.
- **Зачем:** Ранее Codex работал только с файлами и терминалом. Computer use расширяет границы: тестирование нативных приложений, GUI-automation, работа с приложениями без API. Для разработчиков: front-end тестирование, проверка мобильных симуляторов, работа с IDE-плагинами.
- **Ограничения:** Только macOS. Недоступен в EU/UK/Switzerland на старте.

---

**In-App Browser с комментариями на странице (App 26.415)**

- **Что это:** Встроенный браузер в Codex App. Открывает локальные и публичные страницы. Можно комментировать прямо на рендеренной странице -- Codex интерпретирует комментарии как инструкции.
- **Зачем:** Для фронтенд-разработки и гейм-итераций -- не нужно переключаться между браузером и кодом. Указал пальцем на элемент -> "сделай этот шрифт крупнее, добавь отступ, исправь цвет" -> Codex вносит изменения.
- **Пример использования:**
  ```
  1. Codex открывает localhost:3000
  2. Кликаешь на кнопку -> добавляешь комментарий "Make this button blue and 20px bigger"
  3. Codex вносит CSS-изменения, перезагружает страницу
  ```

---

**Thread Automations -- запланированные пробуждения (App 26.415)**

- **Что это:** Функция, позволяющая thread-у "просыпаться" по расписанию с сохранением контекста беседы. Можно настроить проверку долгих процессов, наблюдение за обновлениями, продолжение follow-up циклов.
- **Зачем:** Для CI/CD-мониторинга, отслеживания длинных build-ов, регулярной проверки состояния проекта. Thread не теряет контекст между пробуждениями.
- **Пример:**
  ```
  "Check if the build passed every 30 minutes and notify me when it's green"
  # Thread засыпает, просыпается через 30 минут,
  # проверяет CI, если зелёный -- уведомляет
  ```

---

**PR Review в сайдбаре (App 26.415)**

- **Что это:** GitHub pull requests теперь отображаются в сайдбаре Codex App. Можно просматривать diff, комментарии, изменённые файлы, а затем попросить Codex объяснить фидбэк, внести изменения и продолжить ревью.
- **Зачем:** Полный цикл PR review без переключения на GitHub. Ревьюер читает diff в Codex, кликает на комментарий -> Codex объясняет или исправляет -> пушит -> ревью продолжается.

---

**Codex CLI v0.121.0 -- memory, marketplace, MCP (15 апреля)**

**`Ctrl+R` -- reverse history search (v0.121.0)**

- **Что это:** Обратный поиск по истории команд в TUI, аналогичный shell-у. Плюс local recall для принятых slash-команд.
- **Зачем:** При частом повторении длинных промптов и slash-команд -- не нужно набирать заново.
- **Пример:** `Ctrl+R` -> набираешь "review" -> показывает последний промпт с "review" в тексте.

---

**Memory management -- persistent memory (v0.121.0)**

- **Что это:** Выделенное меню управления памятью: сброс, удаление отдельных записей, очистка расширений памяти. Phase 2 memory model обновлён до gpt-5.4.
- **Зачем:** Memory позволяет Codex запоминать предпочтения, конвенции проекта, recurring patterns между сессиями. Управление через меню -- возможность удалить устаревшие или неверные записи.

---

**`codex marketplace add` -- установка плагинов из маркетплейса (v0.121.0)**

- **Что это:** Новая команда для установки плагинов из различных источников: GitHub URLs, git URLs, локальные пути, marketplace.json.
- **Пример:**
  ```bash
  codex marketplace add github:user/plugin-name
  codex marketplace add /local/path/to/plugin
  codex marketplace add --from marketplace.json
  ```

---

**Namespaced MCP registration + parallel-call opt-in (v0.121.0)**

- **Что это:** MCP-серверы теперь регистрируются с namespace-ами (избегает конфликтов имён между серверами). Parallel-call opt-in: MCP-сервер может заявить о поддержке параллельных вызовов, Codex будет вызывать его инструменты одновременно.
- **Зачем:** При использовании 5+ MCP-серверов конфликты имён инструментов были частой проблемой. Namespace-ы устраняют это. Parallel calls ускоряют работу с серверами, поддерживающими конкурентность.

---

**Secure bubblewrap profile для Docker (v0.121.0)**

- **Что это:** Добавлен devcontainer-профиль sandbox-а: bubblewrap + Unix socket allowlist для macOS. Безопаснее, чем default Docker sandbox.
- **Зачем:** Docker-контейнеры не всегда поддерживают полноценный Landlock/seccomp. Bubblewrap-профиль даёт надёжный sandbox внутри Docker.

---

**90+ новых плагинов (App 26.415)**

- **Что это:** Более 90 плагинов при запуске: Jira, Confluence, GitLab Issues, Microsoft 365 (Outlook, Excel, Word, PowerPoint, Teams, SharePoint), Notion, Slack, HubSpot, Salesforce, Google Workspace, GitHub, Linear, Zendesk, CircleCI, CodeRabbit, Neon by Databricks, Render, Remotion.
- **Зачем:** Codex становится централизованным рабочим пространством. Не нужно покидать IDE/терминал для работы с Jira, Slack, email.

---

#### Кейсы использования

**Кейс: In-app browser для итераций фронтенд-дизайна**

- **Проблема:** Фронтенд-разработчик тратит ~40% рабочего времени на цикл "изменил CSS -> переключился в браузер -> проверил -> переключился назад в код -> повторил". Каждое переключение -- 5-10 секунд потерянного контекста.
- **Решение:** Обновил Codex App до 26.415. Открыл in-app browser на localhost:3000. Кликнул на header -> комментарий: "Reduce font-size to 16px, add 24px padding, change background to #1a1a2e". Codex внёс изменения, страница обновилась автоматически.
- **Результат:** Цикл итерации сократился с ~45 секунд (ручной) до ~15 секунд (с in-app browser). За 2-часовую сессию UI-polish -- экономия ~30 минут. Особенно эффективно для pixel-perfect правок, где нужно видеть результат немедленно.

---

**Оценка:** Да, обновить до CLI 0.121.0 и App 26.415. Computer use -- ещё в ранней стадии (только macOS, не EU), но in-app browser уже production-ready для фронтенд-разработки. Memory management и Ctrl+R -- значимые QoL-улучшения для ежедневной работы. Thread automations полезны для CI/CD-мониторинга. **Внимание:** 90+ плагинов аутентифицируются через OAuth -- IT-командам следует аудировать scopes и data-residency перед включением в организации.

---

### 3. Google (Stitch / AI Studio / Jules / Gemini CLI) -- Приоритет 2

**Версии на этой неделе:** Gemini CLI v0.38.0 (14 апреля), v0.38.1 (15 апреля), v0.38.2 (17 апреля)

#### Новые фичи

**Субагенты -- публичный релиз (v0.38.1)**

- **Что это:** Субагенты позволяют делегировать задачи специализированным изолированным агентам. Каждый субагент работает в своём контекстном окне с собственными инструментами, system instructions и MCP-серверами. Три встроенных субагента:
  - `@generalist` -- общий агент с полным набором инструментов (фактически копия основного)
  - `@cli_help` -- эксперт по Gemini CLI с доступом к документации
  - `@codebase_investigator` -- исследование кодовых баз, анализ архитектуры, поиск root cause
- **Зачем:** Основная проблема длинных агентных сессий -- context rot (деградация контекста). Субагенты решают это: тяжёлая работа (grep по 1000 файлов, batch-рефакторинг) выполняется в изолированном контексте, результат возвращается как сжатый summary. Основная сессия остаётся быстрой.
- **Пример:**
  ```bash
  # Явная делегация
  @codebase_investigator Map out the authentication flow and find all entry points
  @generalist Update the license headers across the whole project
  
  # Параллельное выполнение
  "Run @frontend-specialist on each package in parallel"
  
  # Управление субагентами
  /agents  # Показать все активные и настроенные субагенты
  ```
- **Кастомные субагенты:** Создаются как Markdown-файлы с YAML frontmatter в `~/.gemini/agents/`:
  ```yaml
  # ~/.gemini/agents/security-reviewer.md
  ---
  name: security-reviewer
  tools: [read_file, grep, web_search]
  ---
  You are a security code reviewer. Focus on OWASP Top 10...
  ```

---

**Context Compression Service (v0.38.0)**

- **Что это:** Выделенный сервис для управления контекстом. Автоматически дистиллирует историю разговора, сохраняя фокус и экономя токены. Настраивается порог компрессии в `/settings` (десятичное число с отображением в процентах).
- **Зачем:** В длинных сессиях (1+ час) контекстное окно заполняется, модель теряет фокус, ответы деградируют. Context Compression автоматически сжимает старые части разговора, сохраняя ключевую информацию.

---

**Terminal Buffer mode (v0.38.0)**

- **Что это:** Новый режим рендеринга для устранения мерцания при быстрых обновлениях инструментов. Включается/выключается в настройках (`terminalBuffer`).
- **Зачем:** При активной работе агента (десятки tool calls в минуту) терминал мерцает. Terminal Buffer mode буферизует обновления и рендерит их пакетами.

---

**Context-aware persistent policy approvals (v0.38.0)**

- **Что это:** Пользователь может выдать persistent approval с учётом контекста. Одобрение привязывается к конкретному инструменту + паттерну аргументов и сохраняется между сессиями.
- **Зачем:** Без этого каждая сессия начинается с нуля по разрешениям. Persistent approvals устраняют повторные запросы для доверенных операций (например, "всегда разрешать git status в этом проекте").

---

**Background memory + process monitoring (v0.38.0)**

- **Что это:** Фоновый сервис извлечения skills из поведения пользователя (auto configure memory). Инструменты для мониторинга и инспекции фоновых shell-процессов.
- **Зачем:** Memory автоматически запоминает, как пользователь работает. Process monitoring позволяет агенту следить за длинными фоновыми задачами (build, test, deploy) без блокировки основной сессии.

---

**`/stats` с разделением по ролям (v0.38.1)**

- **Что это:** Команда `/stats` теперь показывает отдельную статистику для основного агента, субагентов и utility-функций.
- **Зачем:** Понять, куда уходят токены -- основная работа или субагенты. Полезно для оптимизации cost при использовании параллельных субагентов.

---

**Stitch / Jules / AI Studio**

- **Google Stitch v2:** Выпущена вторая версия. Без конкретных технических release notes за эту неделю.
- **Jules:** Без новых релизов на этой неделе. Текущие возможности: Suggested Tasks (scan код, предлагает улучшения), Scheduled Tasks, Render integration для self-healing deployments, free tier (15 задач/день), Pro ($19.99/мес), CLI и Public API.
- **AI Studio / Gemini API:** Gemma 4 модели доступны через API. Flex и Priority inference tiers.

---

#### Кейсы использования

**Кейс: Параллельные субагенты для аудита безопасности монорепо**

- **Проблема:** Команда нуждалась в полном security-аудите монорепо (200+ файлов, 5 микросервисов). Ручной аудит одним человеком -- 3 дня.
- **Решение:** Gemini CLI v0.38.1 с кастомным субагентом `@security-reviewer`:
  ```
  Run @security-reviewer on each microservice in parallel.
  Check for: hardcoded secrets, SQL injection, path traversal,
  missing input validation, insecure deserialization.
  ```
  5 субагентов запустились параллельно, каждый в изолированном контексте. Основной агент собрал результаты в единый отчёт.
- **Результат:** Аудит завершён за 45 минут (вместо 3 дней). Найдено 12 issues (3 critical: hardcoded AWS key, SQL injection в legacy endpoint, path traversal в file upload). Основная сессия не замедлилась -- субагенты работали в изолированных контекстах.

---

**Оценка:** Да, обновить до v0.38.2. Субагенты -- ключевая фича для production-использования: параллельная работа, изоляция контекста, кастомные эксперты. Context Compression и persistent approvals -- значимые QoL-улучшения для длинных сессий.

---

### 4. xAI (инструменты для кода и агентов) -- Приоритет 3

**Новых технических релизов инструментов на этой неделе нет.**

**Текущее состояние (по состоянию на 20 апреля 2026):**

- **Grok 4.20 Beta 2** (3 марта) -- текущий флагман. 4-агентная система. 2M context window (API).
- **Grok 4.4** (~1T параметров) анонсирован на начало мая 2026. Training data до начала апреля.
- **Grok 4.5** (~1.5T параметров) -- конец мая 2026.
- **Grok 5** (~6T параметров, MoE) -- Q2 2026. Training на Colossus 2 завершается. Internal testing -- апрель-май. Public beta -- прогноз май-июнь. Polymarket: 33% вероятность до 30 июня.
- **Agent tools:** Web Search, X Search, Code Interpreter, Collections Search. GA. $5 за 1000 вызовов.
- **grok-code-fast-1** -- специализированная модель для agentic coding. ~314B параметров, 256K контекст, ~92 токена/сек.

---

**Оценка:** Пока нет. xAI активно готовит следующие модели (4.4, 4.5, 5), но за эту неделю новых инструментов или возможностей для разработчиков не появилось. Grok 4.4 в начале мая может быть интересен -- watch.

---

## Таблица сравнения

| Инструмент | Новые фичи | Новые кейсы | Влияние | Тестировать на этой неделе |
|---|---|---|---|---|
| **Claude Code** v2.1.105-114 + Opus 4.7 | Opus 4.7 (+14% workflow, 3x меньше ошибок), `xhigh` effort, `/ultrareview` (cloud multi-agent review), `/less-permission-prompts`, auto mode для Max, session recap, 1h prompt cache, plugin monitors, PreCompact hooks, `/tui fullscreen`, push notifications | /ultrareview для предрелизного security-аудита; /less-permission-prompts для оптимизации workflow | Высокое | Да |
| **Codex** CLI 0.121.0 + App 26.415 | Computer use (macOS), in-app browser, thread automations, PR review в сайдбаре, Ctrl+R, memory management, marketplace, namespaced MCP, parallel-call opt-in, bubblewrap Docker, 90+ плагинов, SSH alpha | In-app browser для фронтенд-итераций | Высокое | Да |
| **Gemini CLI** v0.38.0-0.38.2 | Субагенты (public): @generalist, @cli_help, @codebase_investigator, кастомные, параллельные; Context Compression; Terminal Buffer; persistent policy approvals; background memory; /stats по ролям | Параллельные субагенты для security-аудита монорепо | Среднее | Да |
| **xAI** | Нет новых релизов | -- | Низкое | Нет |

---

## Рекомендации на неделю

1. **Обновить Claude Code до v2.1.114 и попробовать Opus 4.7 с `xhigh` effort.** Запустите `claude update`, переключите модель на `claude-opus-4-7`, установите `/effort xhigh`. Попробуйте `/ultrareview` на текущем PR -- три бесплатных ревью для Pro/Max. Также запустите `/less-permission-prompts` для автоматической генерации allowlist -- это сэкономит реальные минуты каждый день. **Важно:** если используете Opus 4.7 через API -- проверьте Migrating to Claude Opus 4.7, есть breaking changes в токенизаторе.

2. **Обновить Codex App до 26.415 и протестировать in-app browser для фронтенд-разработки.** Откройте in-app browser на localhost, попробуйте добавлять комментарии прямо на странице. Для CLI: обновите до 0.121.0 (`npm install -g @openai/codex@0.121.0`), попробуйте `Ctrl+R` для поиска по истории и управление памятью. Thread automations полезны для мониторинга CI -- настройте автоматическую проверку build-статуса.

3. **Обновить Gemini CLI до v0.38.2 и попробовать субагенты.** Начните с встроенных: `@codebase_investigator` для исследования архитектуры, `@generalist` для batch-операций. Создайте кастомного субагента в `~/.gemini/agents/` для своего специфического workflow. `/stats` покажет, как распределяются токены между основным агентом и субагентами.

---

## Источники

- [Introducing Claude Opus 4.7 -- Anthropic](https://www.anthropic.com/news/claude-opus-4-7)
- [Claude Code Changelog -- Releasebot](https://releasebot.io/updates/anthropic/claude-code)
- [Anthropic Release Notes -- Releasebot](https://releasebot.io/updates/anthropic)
- [Claude Code Changelog -- claudefa.st](https://claudefa.st/blog/guide/changelog)
- [Claude Code Docs -- Week 15](https://code.claude.com/docs/en/whats-new/2026-w15)
- [Claude Code: What's New in April 2026 -- YouTube](https://www.youtube.com/watch?v=uLh6AB51QzU)
- [Introducing the New Codex for (almost) everything -- OpenAI Community](https://community.openai.com/t/introducing-the-new-codex-for-almost-everything/1379125)
- [Codex Changelog -- OpenAI Developers](https://developers.openai.com/codex/changelog/)
- [Codex Release Notes -- Releasebot](https://releasebot.io/updates/openai/codex)
- [OpenAI Releases a Major Update to Codex -- Thurrott](https://www.thurrott.com/a-i/openai-a-i/335030/openai-releases-a-major-update-to-codex)
- [Codex April 2026 Update -- Spicy Advisory](https://www.spicyadvisory.com/blog/openai-codex-april-2026-update-business-workflows-2026)
- [Claude Design, Codex CLI v0.121 -- jls42.org](https://jls42.org/en/news/ia-actualites-17-apr-2026)
- [Gemini CLI v0.38.1 Changelog -- geminicli.com](https://geminicli.com/docs/changelogs/latest/)
- [Gemini CLI Release Notes -- Releasebot](https://releasebot.io/updates/google/gemini-cli)
- [Subagents have arrived in Gemini CLI -- Google Developers Blog](https://developers.googleblog.com/subagents-have-arrived-in-gemini-cli/)
- [Gemini CLI v0.38.1: Subagents are here -- Reddit](https://www.reddit.com/r/GeminiCLI/comments/1snjfwx/gemini_cli_v0381_subagents_are_here/)
- [Google Embeds Subagents Inside Gemini CLI -- Developer Tech](https://www.developer-tech.com/news/google-embeds-subagents-inside-gemini-cli/)
- [xAI Release Notes](https://docs.x.ai/developers/release-notes)
- [Grok 5 Release Date -- NxCode](https://www.nxcode.io/resources/news/grok-5-release-date-latest-news-2026)
- [Grok AI Models to Expand -- Phemex News](https://phemex.com/news/article/grok-ai-models-to-expand-with-upcoming-releases-74249)
