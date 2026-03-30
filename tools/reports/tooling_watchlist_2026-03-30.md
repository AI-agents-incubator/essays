# Tooling Watchlist -- Code & Agents

> **Отчёт за неделю:** 24--30 марта 2026
> **Дата генерации:** 30 марта 2026
> **Версия спецификации:** 3.1

---

## Executive Summary

- **Claude Code: Auto Mode (24 марта) и Computer Use (23 марта)** -- две ключевые фичи, радикально меняющие уровень автономии агента. Auto Mode заменяет ручное одобрение каждого действия на AI-классификатор (Sonnet 4.6), который блокирует опасные операции и пропускает безопасные. Computer Use позволяет Claude управлять мышью, клавиатурой и браузером на рабочем столе пользователя.
- **Claude Code выпустил 5 релизов (v2.1.82--2.1.86)** с managed-settings.d (drop-in политики для команд), sandbox.failIfUnavailable (жёсткий отказ при отсутствии песочницы), CLAUDE_CODE_SUBPROCESS_ENV_SCRUB (удаление секретов из субпроцессов), условные хуки и поиск по транскриптам.
- **Codex CLI 0.117.0 (26 марта)** -- плагиновая система стала first-class: TUI-меню `/plugins`, marketplace, авто-установка MCP-серверов при активации плагина. Multi-Agent v2 с человекочитаемыми адресами агентов (`/root/agent_a`). App-server TUI включён по умолчанию.
- **Gemini CLI v0.35.0 (24 марта)** -- настраиваемые горячие клавиши, SandboxManager с bubblewrap/seccomp изоляцией на Linux, JIT Context Discovery для уменьшения контекстного шума, Vim-моды.
- **Тема недели: автономия агентов.** Claude Code Auto Mode -- первый масштабный эксперимент с AI-классификатором разрешений (0.4% FPR, 17% FNR на реальном трафике). Это сигнал всей индустрии: вопросы безопасности решаются не через «отключить всё» или «разрешить всё», а через специализированные классификаторы.

---

## По инструментам

---

### Приоритет 1: Claude Code / Cowork (Anthropic)

**5 релизов за неделю: v2.1.82 -- v2.1.86 (20--27 марта 2026)**
**2 крупных запуска: Computer Use (23 марта) и Auto Mode (24 марта)**

#### Новые фичи

**1. Auto Mode -- AI-классификатор разрешений (24 марта, research preview)**

- **Что это:** Новый режим разрешений, в котором AI-классификатор на базе Sonnet 4.6 автоматически решает, какое действие безопасно, а какое требует одобрения пользователя. Запуск: `claude --enable-auto-mode` или в сессии через `Shift+Tab` (переключение между режимами). В VS Code: Settings -- Claude Code -- Enable auto mode.
- **Зачем это нужно:** До этого разработчики стояли перед выбором: либо отвечать на 93% одобрений (по данным Anthropic), теряя время, либо использовать `--dangerously-skip-permissions`, рискуя безопасностью. Auto Mode -- средний путь: безопасные действия выполняются автоматически, опасные блокируются.
- **Как работает под капотом:**
  - **Слой 1 -- Prompt Injection Probe (вход):** Серверный зонд сканирует вывод инструментов перед попаданием в контекст Claude. Если обнаружен prompt injection -- добавляется предупреждение.
  - **Слой 2 -- Transcript Classifier (выход):** Классификатор на базе Sonnet 4.6 проверяет каждое действие перед выполнением. Этап 1: быстрый однотоковый фильтр (Yes/No). Этап 2: chain-of-thought анализ (только если Этап 1 сработал). Критично: классификатор «reasoning-blind» -- видит только сообщения пользователя и вызовы инструментов, но НЕ рассуждения Claude. Это значит, что Claude не может «уговорить» классификатор пропустить опасное действие.
- **Что блокируется (примеры из документации):**
  - Пользователь просит «почисти старые ветки» -- Claude удаляет remote-ветки. Блокировка: запрос расплывчатый, действие необратимо.
  - Claude натыкается на ошибку авторизации и начинает искать другие API-токены в env. Блокировка: эти токены для других задач.
  - Claude пытается опубликовать скрипт через GitHub Gist. Блокировка: содержимое может быть конфиденциальным.
- **Метрики (n=10 000 реальных действий):**
  - False Positive Rate (безопасное заблокировано): **0.4%**
  - False Negative Rate (опасное пропущено, n=52): **17%**
  - Синтетические атаки эксфильтрации (n=1000): **5.7% FNR**
- **Пример использования:**
  ```bash
  # Запуск с auto mode
  claude --enable-auto-mode

  # Проверка текущих настроек
  claude auto-mode defaults

  # В сессии: Shift+Tab для переключения между Default / Auto / YOLO режимами
  ```
- **Доступность:** Research preview для Claude Team. Enterprise и API -- «в ближайшие дни». Только Sonnet 4.6 и Opus 4.6.
- Источники: [TechCrunch -- Auto Mode](https://techcrunch.com/2026/03/24/anthropic-hands-claude-code-more-control-but-keeps-it-on-a-leash/), [9to5Mac](https://9to5mac.com/2026/03/24/claude-code-gives-developers-auto-mode-a-safer-alternative-to-skipping-permissions/), [Sid Saladi -- подробный разбор с метриками](https://sidsaladi.substack.com/p/now-claude-code-gets-new-features)

**2. Computer Use -- управление рабочим столом (23 марта, research preview)**

- **Что это:** Claude может управлять мышью, клавиатурой, браузером и приложениями на рабочем столе пользователя. Включается в настройках Claude Desktop. Поддерживает только macOS.
- **Зачем это нужно:** Когда для задачи нет MCP-коннектора или API, Claude может выполнить её через графический интерфейс -- открыть браузер, заполнить форму, запустить IDE, проверить UI. Приоритет: сначала используются коннекторы (Slack, Google Calendar и т.п.), если их нет -- управление экраном.
- **Защитные механизмы:**
  - Автоматическое сканирование активаций модели для обнаружения prompt injection.
  - Claude всегда запрашивает разрешение перед доступом к новым приложениям.
  - Пользователь может остановить Claude в любой момент.
- **Интеграция с Dispatch:** Можно назначить задачу через телефон (Claude iOS/Android), Claude выполнит её на рабочем столе, пока вы в пути. Примеры: утренний брифинг по почте, запуск тестов и создание PR в IDE, мониторинг 3D-печати.
- Источник: [Anthropic Blog -- Put Claude to work on your computer](https://claude.com/blog/dispatch-and-computer-use), [Claude Help Center](https://support.claude.com/en/articles/12138966-release-notes)

**3. `managed-settings.d/` -- drop-in директория для командных политик (v2.1.83)**

- **Что это:** Новая директория рядом с `managed-settings.json`, куда разные команды могут класть независимые policy-фрагменты. Файлы сортируются в алфавитном порядке и сливаются.
- **Зачем это нужно:** В больших организациях разные команды (безопасность, DevOps, platform) хотят добавлять свои правила без конфликтов. Ранее один `managed-settings.json` требовал координации. Теперь каждая команда кладёт свой файл в `.d/`, и они автоматически объединяются.
- **Пример:**
  ```
  managed-settings.d/
    00-security-team.json    # запрет на rm -rf, ограничения MCP
    10-devops.json           # разрешённые bash-команды
    20-platform.json         # настройки песочницы
  ```

**4. `sandbox.failIfUnavailable` -- жёсткий отказ при отсутствии песочницы (v2.1.83)**

- **Что это:** Новая настройка: если песочница включена, но не может запуститься (отсутствуют зависимости), Claude Code завершается с ошибкой вместо того, чтобы работать без изоляции.
- **Зачем это нужно:** На прошлой неделе мы сообщали об исправлении тихого отключения песочницы (v2.1.78). Новая настройка -- более строгий вариант: вместо предупреждения -- полный отказ. Для enterprise-окружений, где работа без песочницы недопустима.
- **Пример (`settings.json`):**
  ```json
  {
    "sandbox": {
      "failIfUnavailable": true
    }
  }
  ```

**5. `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` -- удаление секретов из субпроцессов (v2.1.83)**

- **Что это:** Переменная окружения, которая удаляет все Anthropic и облачные провайдерские креденшиалы (API-ключи, сессионные токены) из окружения субпроцессов: Bash tool, хуки, MCP stdio-серверы.
- **Зачем это нужно:** Если MCP-сервер или хук-скрипт скомпрометированы, они не могут получить доступ к API-ключам из окружения родительского процесса. Критично для защиты от supply-chain атак через плагиновую экосистему.
- **Пример:**
  ```bash
  CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1 claude
  # Теперь ни один субпроцесс не увидит ANTHROPIC_API_KEY
  ```

**6. Условные хуки с полем `if` (v2.1.85)**

- **Что это:** Хуки теперь поддерживают поле `if` с синтаксисом правил разрешений (например, `Bash(git *)`) для фильтрации, когда они должны срабатывать. Это уменьшает количество порождаемых процессов.
- **Зачем это нужно:** Ранее хук срабатывал на КАЖДЫЙ вызов инструмента, даже если он релевантен только для определённых команд. Теперь можно точно указать: «этот хук только для git-команд» или «только для записи в src/».
- **Пример:**
  ```json
  {
    "hooks": {
      "PreToolUse": [{
        "if": "Bash(git *)",
        "type": "command",
        "command": "echo 'Git operation detected' >> /tmp/audit.log"
      }]
    }
  }
  ```

**7. `TaskCreated` хук (v2.1.84)**

- **Что это:** Новое событие хука, которое срабатывает при создании задачи через `TaskCreate`. Позволяет автоматически реагировать на новые задачи -- логировать, оповещать, добавлять контекст.

**8. PowerShell tool для Windows (v2.1.84, opt-in preview)**

- **Что это:** Claude Code теперь может использовать PowerShell как инструмент на Windows вместо Bash. Opt-in через настройки.
- **Зачем это нужно:** Windows-разработчики получают нативный опыт вместо адаптации через WSL/Git Bash.
- **Документация:** https://code.claude.com/docs/en/tools-reference#powershell-tool

**9. Поиск по транскриптам -- `/` в транскриптном режиме (v2.1.83)**

- **Что это:** В режиме транскрипта (`Ctrl+O`) можно нажать `/` для поиска, `n`/`N` для перехода между совпадениями.
- **Зачем это нужно:** В длинных сессиях с сотнями сообщений стало необходимо быстро находить конкретные моменты -- команду, ошибку, решение.

**10. Дополнительные изменения**

- **`X-Claude-Code-Session-Id` header (v2.1.86):** Новый заголовок в API-запросах, позволяющий прокси-серверам агрегировать запросы по сессии без парсинга тела запроса.
- **`CLAUDE_CODE_MCP_SERVER_NAME`/`_URL` env vars (v2.1.85):** Для MCP `headersHelper`-скриптов -- один скрипт может обслуживать несколько серверов.
- **`initialPrompt` frontmatter (v2.1.83):** Агенты могут автоматически отправлять первый запрос при запуске.
- **`--bare -p` ускорение на ~14% (v2.1.83):** Ускорение до API-запроса в SDK-паттерне.
- **MCP tool descriptions ограничены 2 KB (v2.1.84):** Предотвращает раздувание контекста от OpenAPI-генерированных серверов.
- **Исправление `--mcp-config` в обход `allowedMcpServers`/`deniedMcpServers` (v2.1.83):** Безопасность -- CLI-флаг больше не обходит managed-политики.
- **WebFetch теперь идентифицирует себя как `Claude-User` (v2.1.83):** Для опознания и whitelisting в `robots.txt`.

#### Кейсы использования

**Кейс: Auto Mode заменяет rubber-stamping разрешений**
- **Проблема:** 93% разрешений в Claude Code одобрялись пользователями без чтения. Это худший вариант, чем AI-классификатор -- пользователи не смотрят на действия, но формально «одобрили».
- **Решение:** Auto Mode с двухслойным классификатором (prompt injection probe + transcript classifier). Запуск: `claude --enable-auto-mode`. Классификатор «reasoning-blind» -- не видит рассуждения Claude, только действия.
- **Результат:** 0.4% FPR (почти не блокирует безопасное), 17% FNR на реальных overeager-действиях (52 кейса). Массивное улучшение безопасности по сравнению с `--dangerously-skip-permissions`. Источник: [Sid Saladi -- Auto Mode Guide](https://sidsaladi.substack.com/p/now-claude-code-gets-new-features)

**Кейс: Computer Use + Dispatch -- работа агента на рабочем столе, пока вы в дороге**
- **Проблема:** Множество задач требуют взаимодействия с GUI-приложениями, для которых нет API или MCP-коннекторов.
- **Решение:** Включить Computer Use в настройках Claude Desktop (macOS). Назначить задачу через Dispatch с телефона. Claude управляет рабочим столом: открывает браузер, заполняет формы, запускает IDE.
- **Результат:** Новый класс задач, ранее недоступных для агента: утренние брифинги с открытием почты, создание презентаций в Google Slides, мониторинг приложений через GUI. Источник: [Anthropic Blog](https://claude.com/blog/dispatch-and-computer-use)

#### Оценка: Да -- тестировать на этой неделе

Auto Mode -- ключевая фича для всех, кто использует `--dangerously-skip-permissions`. Computer Use -- для задач, требующих GUI. managed-settings.d и sandbox.failIfUnavailable -- для enterprise-команд.

---

### Приоритет 1: Codex (OpenAI)

**1 релиз CLI: v0.117.0 (26 марта). Codex App 26.323 и 26.318.**

#### Новые фичи

**1. Плагины как first-class workflow (CLI v0.117.0)**

- **Что это:** Полностью пересмотренная плагиновая система. Codex теперь автоматически синхронизирует product-scoped плагины при запуске, предлагает TUI-меню `/plugins` для просмотра, установки и удаления плагинов с полноценной авторизацией. Плагины могут включать MCP-серверы, которые автоматически устанавливаются при активации плагина.
- **Зачем это нужно:** Ранее плагины были экспериментальными и требовали ручной настройки. Теперь это полная экосистема: marketplace с курированными плагинами, git-синхронизация, life-cycle management. Плагины -- это способ упаковать skills + MCP-серверы + app-интеграции в единый переиспользуемый пакет.
- **Пример использования:**
  ```bash
  # Просмотр доступных плагинов
  codex
  /plugins

  # Установка плагина из marketplace
  # (плагины появляются в /plugins с описанием и авторизацией)

  # Упоминание плагина в чате
  @my-plugin deploy the staging environment
  ```
- Источники: [Codex Changelog](https://developers.openai.com/codex/changelog/), [Reddit -- Codex v0.117.0 plugins](https://www.reddit.com/r/codex/comments/1s517gl/codex_v01170_now_supports_plugins_heres_a_simple/)

**2. Multi-Agent v2 с человекочитаемыми адресами (CLI v0.117.0)**

- **Что это:** Sub-агенты теперь используют path-based адреса вместо UUID: `/root/agent_a`, `/root/agent_b/sub_agent_1`. Структурированные межагентные сообщения и listing агентов для multi-agent v2 workflow.
- **Зачем это нужно:** UUID-адреса были нечитаемыми в логах и дебаг-выводе. Path-based система делает иерархию агентов понятной: кто родитель, кто потомок, какова структура. Упрощает debugging и мониторинг сложных multi-agent сессий.
- **Пример:** Вместо `agent_7b2f3a91-4c5e-...` теперь `/root/code_reviewer` -- сразу понятно, что это и где в иерархии.

**3. App-server TUI включён по умолчанию (CLI v0.117.0)**

- **Что это:** App-server-backed TUI (terminal user interface) теперь включён для всех по умолчанию. Старые flags убраны.
- **Зачем это нужно:** App-server TUI поддерживает расширенные функции: `!` shell-команды, наблюдение за файловой системой (filesystem watch), подключение к удалённым websocket-серверам с bearer-token авторизацией. Это база для будущих интеграций.

**4. Удаление legacy-инструментов (CLI v0.117.0)**

- **Что это:** Удалены старые `read_file`, `grep_files` обработчики и legacy artifact tool. Чистка инструментов для уменьшения контекстного шума.
- **Зачем это нужно:** Меньше инструментов в контексте -- лучше качество выбора инструментов моделью. Legacy code занимал место и мог вызывать путаницу.

**5. Codex App 26.323 -- поиск по тредам и синхронизация настроек**

- **Что это:** Поиск по всем прошлым тредам в приложении Codex (sidebar shortcut + горячие клавиши). Одним кликом -- архивирование всех локальных тредов в проекте. Ключевые настройки теперь синхронизируются между Codex App и VS Code extension.
- **Зачем это нужно:** При активной работе накапливаются десятки тредов. Поиск и архивирование -- базовая гигиена для productivity. Синхронизация настроек -- не нужно дважды настраивать один и тот же проект.

**6. Codex App 26.318 -- skills в @ меню и быстрый поиск**

- **Что это:** Skills теперь доступны через `@` меню в композере рядом с другими упоминаниями. `Cmd/Ctrl+F` начинает поиск с текущего выделения текста.

#### Кейсы использования

**Кейс: Плагиновая экосистема Codex -- стандартизация рабочих процессов**
- **Проблема:** Команды создают одни и те же настройки (MCP-серверы, skills, app-интеграции) в каждом репозитории заново. Это дублирование и источник ошибок.
- **Решение:** Упаковка всего в плагин: MCP-сервер + skills + конфигурация. Установка через `/plugins` в одном клике. Синхронизация через git.
- **Результат:** Стандартизированные рабочие процессы между репозиториями и командами. Plugin-creator system skill позволяет создавать плагины прямо из Codex. Источник: [Codex Plugins Documentation](https://developers.openai.com/codex/plugins?install-scope=global)

#### Оценка: Да -- тестировать на этой неделе

Плагиновая система -- ключевая для команд, которые хотят стандартизировать workflow. Multi-agent v2 -- для сложных параллельных задач. Обновиться до 0.117.0: `npm install -g @openai/codex@0.117.0`.

---

### Приоритет 2: Google (Stitch / AI Studio / Jules / Gemini CLI)

#### Gemini CLI v0.35.0 (24 марта 2026)

- **Настраиваемые горячие клавиши:** Пользователи теперь могут настроить любые keyboard shortcuts, включая поддержку Kitty-протокола и буквенных bindings.
- **Vim Mode улучшения:** Добавлены X, ~, r, f/F/t/T motions и yank/paste с unnamed регистром. Для vim-пользователей -- Gemini CLI стало значительно более usable.
- **SandboxManager с bubblewrap/seccomp изоляцией (Linux):** Новый менеджер песочницы изолирует инструменты, порождающие процессы, через bubblewrap и seccomp. Это системный уровень изоляции (как gVisor на прошлой неделе, но с более низкоуровневым подходом).
- **JIT Context Discovery:** Just-In-Time обнаружение контекста для file system tools -- вместо загрузки всего контекста заранее, подгружается только то, что необходимо для текущего шага. Уменьшает шум в контекстном окне и улучшает точность модели.
- Источники: [Gemini CLI Changelogs](https://geminicli.com/docs/changelogs/), [Releasebot -- Gemini CLI](https://releasebot.io/updates/google/gemini-cli)

Патчи v0.35.1--v0.35.3 вышли 26--27 марта с minor fixes.

#### Google Stitch -- инкрементальные улучшения

- Обновлённый интерфейс с более современным дизайном.
- In-place редактирование: теперь можно редактировать генерации прямо на canvas без регенерации всего экрана.
- Pro/Experimental режим увеличен до 200 генераций/месяц (ранее 50).
- Источник: [NxCode -- Stitch Pricing Guide](https://www.nxcode.io/resources/news/google-stitch-pricing-plans-complete-guide-2026)

#### Jules -- без новых релизов на этой неделе

Последний значимый релиз -- интеграция Gemini 3.1 Pro (9 марта). На этой неделе без изменений.

#### Оценка: Возможно позже

Gemini CLI v0.35.0 интересен для vim-пользователей и для тех, кому важна изоляция на Linux. JIT Context Discovery -- хороший технический шаг, но ещё ранний. Stitch продолжает дорабатываться.

---

### Приоритет 3: xAI (Grok -- инструменты для кода и агентов)

#### Grok 4.20 -- стабилизация, без новых релизов

- Grok 4.20 Beta 2 (3 марта) остаётся текущей версией. Beta 3 в разработке (подтверждено Маском 12 марта), но не выпущена.
- Grok 5 пропустил Q1 2026 deadline. Новый прогноз -- Q2 2026.
- API цены: $2 input / $15 output за 1M токенов (Beta 2). Контекстное окно: 2M токенов.
- Источник: [NxCode -- Grok 5 Release Date](https://www.nxcode.io/resources/news/grok-5-release-date-latest-news-2026)

#### grok-cli -- без новых релизов на этой неделе

Последний релиз -- v1.0.0-rc3. Без изменений за прошедшую неделю.

#### Оценка: Нет -- наблюдать

Никаких новых технических релизов от xAI на этой неделе. Beta 3 Grok 4.20 ждём -- обещаны «many fixes and functionality gains».

---

## Таблица сравнения

| Инструмент | Новые фичи | Новые кейсы | Влияние | Тесты на этой неделе |
|---|---|---|---|---|
| **Claude Code** | Auto Mode (AI-классификатор разрешений), Computer Use (управление рабочим столом), managed-settings.d, sandbox.failIfUnavailable, SUBPROCESS_ENV_SCRUB, условные хуки, PowerShell tool | Auto Mode: 0.4% FPR, замена rubber-stamping. Computer Use + Dispatch: агентное управление рабочим столом с телефона | **Высокое** | **Да** |
| **Codex CLI** | Плагины first-class (/plugins, marketplace, MCP auto-install), Multi-Agent v2 (path-based адреса), App-server TUI по умолчанию, Codex App поиск по тредам, синхронизация настроек | Плагиновая экосистема: стандартизация workflow между репозиториями | **Высокое** | **Да** |
| **Google Gemini CLI / Stitch / Jules** | Gemini CLI v0.35.0: настраиваемые клавиши, Vim mode, SandboxManager bubblewrap/seccomp, JIT Context Discovery. Stitch: in-place editing, 200 pro генераций | -- | **Среднее** | **Нет** |
| **xAI (Grok)** | Без новых релизов. Beta 3 в разработке. Grok 5 отложен на Q2 | -- | **Низкое** | **Нет** |

---

## Рекомендации на неделю

1. **Включить Auto Mode в Claude Code и оценить влияние на workflow.** Если вы используете `--dangerously-skip-permissions` -- Auto Mode безопасная замена. Если вы вручную одобряете каждое действие -- Auto Mode сэкономит 90%+ времени на permission prompts. Запуск: `claude --enable-auto-mode`. Отслеживайте блокировки в первые дни -- это покажет, какие ваши паттерны считаются рискованными.

2. **Обновить Codex CLI до 0.117.0 и попробовать плагиновую систему.** `npm install -g @openai/codex@0.117.0`. Откройте `/plugins`, просмотрите marketplace. Если у вас есть повторяющиеся настройки между репозиториями -- это идеальный кандидат для плагина. Multi-agent v2 с path-based адресами упрощает debugging -- проверьте на сложных параллельных задачах.

3. **Для enterprise-команд: настроить `sandbox.failIfUnavailable` и `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` в Claude Code.** Два новых механизма безопасности, которые должны быть включены в любых prod-окружениях: жёсткий отказ при отсутствии песочницы и удаление секретов из субпроцессов. Также рассмотрите `managed-settings.d/` для разделения политик между командами.

---

## Источники

- [Claude Code Changelog (GitHub)](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) -- официальные release notes v2.1.81--2.1.86
- [Claude Help Center -- Release Notes](https://support.claude.com/en/articles/12138966-release-notes) -- Computer Use (23 марта), Interactive Apps (25 марта)
- [Anthropic Blog -- Put Claude to work on your computer](https://claude.com/blog/dispatch-and-computer-use) -- анонс Computer Use и Dispatch
- [TechCrunch -- Anthropic hands Claude Code more control](https://techcrunch.com/2026/03/24/anthropic-hands-claude-code-more-control-but-keeps-it-on-a-leash/) -- Auto Mode announcement
- [9to5Mac -- Claude Code auto mode](https://9to5mac.com/2026/03/24/claude-code-gives-developers-auto-mode-a-safer-alternative-to-skipping-permissions/) -- Auto Mode details
- [InfoWorld -- Claude Code AI tool getting auto mode](https://www.infoworld.com/article/4150226/claude-code-ai-tool-getting-auto-mode.html) -- Auto Mode технические детали
- [Sid Saladi -- Auto Mode Complete Guide](https://sidsaladi.substack.com/p/now-claude-code-gets-new-features) -- подробный разбор Auto Mode с метриками
- [Codex CLI Changelog](https://developers.openai.com/codex/changelog/) -- официальные release notes v0.117.0
- [Releasebot -- Codex Release Notes](https://releasebot.io/updates/openai/codex) -- Codex App 26.323, 26.318
- [Codex Plugins Documentation](https://developers.openai.com/codex/plugins?install-scope=global) -- документация плагиновой системы
- [Reddit -- Codex v0.117.0 plugins](https://www.reddit.com/r/codex/comments/1s517gl/codex_v01170_now_supports_plugins_heres_a_simple/) -- обсуждение плагинов
- [Gemini CLI Changelogs](https://geminicli.com/docs/changelogs/) -- v0.35.0 release notes
- [Releasebot -- Gemini CLI](https://releasebot.io/updates/google/gemini-cli) -- v0.35.0--v0.35.3
- [NxCode -- Google Stitch Pricing 2026](https://www.nxcode.io/resources/news/google-stitch-pricing-plans-complete-guide-2026) -- Stitch обновления и цены
- [NxCode -- Grok 5 Release Date](https://www.nxcode.io/resources/news/grok-5-release-date-latest-news-2026) -- Grok 4.20 status и Grok 5 прогноз
