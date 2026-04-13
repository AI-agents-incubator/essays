# Tooling Watchlist -- Отчёт за неделю 7-13 апреля 2026

> **Дата:** 13 апреля 2026
> **Период:** 7-13 апреля 2026
> **Формат:** Markdown v3.1
> **Приоритет тем:** автономия агентов, безопасность

---

## Executive Summary

- **Anthropic запустила Claude Managed Agents (public beta) и `ant` CLI (8 апреля):** полностью управляемая среда для запуска автономных Claude-агентов в облаке Anthropic. Агент получает контейнер, встроенные инструменты (Bash, Read, Write, Edit, Glob, Grep, Web Search, Web Fetch), SSE-стриминг событий и поддержку мультиагентной оркестрации. Новый `ant` CLI позволяет создавать агентов, среды и сессии из терминала. Это принципиально новый уровень инфраструктуры для агентов -- не нужно строить собственный цикл ReAct, управлять контейнерами и инструментами.
- **Claude Code: 5 релизов за неделю (v2.1.94-2.1.101)** с фокусом на enterprise-безопасность и UX. Ключевые добавления: Focus View (`Ctrl+O`) для сжатого просмотра длинных сессий, Monitor tool для стриминга событий фоновых скриптов, subprocess sandboxing с PID namespace isolation, интерактивный Vertex AI setup wizard, `/team-onboarding` для генерации руководства новичкам, trust к OS CA certificates по умолчанию.
- **Codex CLI: два крупных релиза (v0.119.0 и v0.120.0).** v0.119.0 -- голосовой режим Realtime V2 по умолчанию (WebRTC), обогащённая поддержка MCP Apps и custom MCP-серверов, remote workflow с egress-websocket и sandbox-aware filesystem. v0.120.0 -- стриминг прогресса фоновых агентов в реальном времени, улучшенная видимость хуков в TUI, типизированные MCP `outputSchema` в code-mode.
- **Gemini CLI v0.37.0/v0.37.1 (8-10 апреля):** введены "Chapters" -- логическая группировка взаимодействий агента по инструментам и намерениям, динамическое расширение sandbox для Linux и Windows, persistent browser sessions, lockdown секретов в env-файлах, `forbiddenPaths` для OS-специфичных sandbox-менеджеров.
- **xAI:** новых релизов нет. Grok 4.20 Beta 2 остаётся текущим. Grok 5 -- прогноз Q2 2026, training на Colossus 2 завершается в апреле.

---

## По инструментам

---

### 1. Claude Code / Cowork (Anthropic) -- Приоритет 1

**Версии на этой неделе:** v2.1.94 (8 апреля), v2.1.96 (8 апреля, hotfix), v2.1.97 (9 апреля), v2.1.98 (9 апреля), v2.1.101 (11 апреля)

**Крупное событие недели:** Claude Managed Agents (public beta) + `ant` CLI (8 апреля)

#### Новые фичи и флаги

**Claude Managed Agents -- полностью управляемая инфраструктура для агентов (8 апреля)**

- **Что это:** Новый API Anthropic для запуска автономных Claude-агентов в облаке. Четыре примитива: Agent (конфигурация: модель, system prompt, инструменты), Environment (контейнер с пакетами и сетью), Session (живая сессия агента), Events (SSE-стрим взаимодействия). Агент получает встроенный тулсет `agent_toolset_20260401`: Bash, файловые операции (Read, Write, Edit), поиск (Glob, Grep), веб-доступ (Web Search, Web Fetch).
- **Зачем:** До этого для запуска автономного Claude-агента нужно было строить собственный цикл ReAct, управлять контейнерами, инструментами, ретраями, стримингом. Managed Agents убирают всю инфраструктурную работу. Особенно полезно для CI/CD-пайплайнов, backend-автоматизации и мультиагентных систем.
- **Пример использования:**
  ```python
  from anthropic import Anthropic
  client = Anthropic()

  # Создать агента
  agent = client.beta.agents.create(
      name="Code Reviewer",
      model="claude-sonnet-4-6",
      system="You are a senior code reviewer.",
      tools=[{"type": "agent_toolset_20260401"}],
  )

  # Создать среду с пакетами
  environment = client.beta.environments.create(
      name="python-env",
      config={
          "type": "cloud",
          "packages": {"pip": ["pytest", "requests", "fastapi"]},
          "networking": {"type": "unrestricted"},
      },
  )

  # Запустить сессию и стримить события
  session = client.beta.sessions.create(
      agent=agent.id, environment_id=environment.id
  )
  with client.beta.sessions.events.stream(session.id) as stream:
      client.beta.sessions.events.send(session.id, events=[{
          "type": "user.message",
          "content": [{"type": "text", "text": "Review src/ for security issues"}],
      }])
      for event in stream:
          if event.type == "agent.message":
              for block in event.content:
                  print(block.text, end="")
  ```
  Все запросы требуют beta-заголовок `managed-agents-2026-04-01`. Мультиагентная оркестрация (координатор делегирует задачи специалистам) доступна через параметр `agents` при создании агента.

---

**`ant` CLI -- командная строка для Claude Developer Platform (8 апреля)**

- **Что это:** CLI-клиент для работы с Claude API, нативно интегрированный с Claude Code. Позволяет создавать агентов, среды и сессии из терминала, версионировать API-ресурсы в YAML-файлах.
- **Зачем:** Быстрый способ работы с Managed Agents без написания Python-кода. Удобно для прототипирования, тестирования и CI/CD.
- **Пример:**
  ```bash
  # Создать агента
  ant beta agents create --name "Code Reviewer" --model claude-sonnet-4-6

  # Создать сессию
  ant beta sessions create --agent-id ag_01ABC... --environment-id env_01XYZ...

  # Помощь по командам
  ant --help
  ```

---

**Focus View -- `Ctrl+O` в NO_FLICKER mode (v2.1.97)**

- **Что это:** Переключатель вида в `NO_FLICKER` режиме. Показывает только три элемента: prompt пользователя, однострочное резюме вызовов инструментов с diffstat по файлам, финальный ответ Claude. Весь промежуточный вывод скрыт.
- **Зачем:** В длинных агентных сессиях (20+ минут) промежуточный вывод занимает сотни строк. Focus View позволяет быстро увидеть, что агент сделал и каков результат, не прокручивая весь лог.
- **Пример:**
  ```bash
  CLAUDE_CODE_NO_FLICKER=1 claude
  # В сессии нажать Ctrl+O для переключения в Focus View
  # Видно: prompt -> "Edit 3 files (+47/-12)" -> финальный ответ
  ```

---

**Monitor tool -- стриминг событий фоновых скриптов (v2.1.98)**

- **Что это:** Новый встроенный инструмент, позволяющий Claude стримить события из фоновых процессов (build scripts, test runners, deployment pipelines) прямо в контекст сессии.
- **Зачем:** Раньше для мониторинга фонового процесса нужно было переключаться в другой терминал или парсить логи вручную. Monitor tool позволяет агенту наблюдать за процессом и реагировать на события в реальном времени.
- **Использование:** Агент автоматически использует Monitor tool, когда запускает фоновые команды через Bash и нуждается в наблюдении за их прогрессом.

---

**Subprocess sandboxing с PID namespace isolation (v2.1.98)**

- **Что это:** На Linux при установленной `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` дочерние процессы теперь изолируются в отдельном PID namespace. Дополнительно: `CLAUDE_CODE_SCRIPT_CAPS` -- переменная для ограничения количества вызовов скриптов в одной сессии.
- **Зачем:** PID namespace не даёт дочерним процессам видеть или взаимодействовать с другими процессами системы. Это дополнительный слой изоляции поверх filesystem sandbox -- важно для enterprise-окружений, где агент работает рядом с production-процессами.
- **Пример:**
  ```bash
  CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1 CLAUDE_CODE_SCRIPT_CAPS=50 claude
  # Дочерние процессы в PID namespace, максимум 50 вызовов скриптов
  ```

---

**Vertex AI Setup Wizard (v2.1.98)**

- **Что это:** Интерактивный мастер настройки Google Vertex AI, доступный с экрана логина при выборе "3rd-party platform". Проводит через GCP-аутентификацию, выбор проекта и региона, верификацию credentials и закрепление модели.
- **Зачем:** Аналогично Bedrock Wizard из v2.1.92 -- снижает порог входа для корпоративных пользователей Google Cloud. До этого настройка Vertex требовала ручной правки конфигов.

---

**`/team-onboarding` -- генерация руководства для новичков (v2.1.101)**

- **Что это:** Новая slash-команда, которая анализирует локальную историю использования Claude Code и генерирует ramp-up guide для нового члена команды.
- **Зачем:** В командах, где активно используется Claude Code, у новичка нет контекста: какие skills настроены, какие CLAUDE.md правила приняты, какие паттерны используются. `/team-onboarding` извлекает эту информацию автоматически.
- **Пример:**
  ```
  /team-onboarding
  # Генерирует Markdown-документ с описанием: настроенные skills,
  # ключевые CLAUDE.md правила, типичные workflow, часто используемые
  # команды и паттерны
  ```

---

**OS CA certificate trust по умолчанию (v2.1.101)**

- **Что это:** Claude Code теперь доверяет системному хранилищу CA-сертификатов по умолчанию. Переменная `CLAUDE_CODE_CERT_STORE=bundled` переключает обратно на только встроенные сертификаты.
- **Зачем:** В enterprise-сетях трафик часто проходит через TLS-прокси с корпоративным CA. Раньше Claude Code не доверял этим сертификатам и выдавал ошибки TLS. Теперь работает из коробки.

---

**`CLAUDE_CODE_PERFORCE_MODE` -- интеграция с Perforce (v2.1.98)**

- **Что это:** Новая переменная окружения. Когда установлена, Edit/Write/NotebookEdit завершаются ошибкой на read-only файлах с подсказкой `p4 edit` вместо молчаливой перезаписи.
- **Зачем:** В Perforce-репозиториях файлы по умолчанию read-only до явного checkout (`p4 edit`). Без этой опции агент мог перезаписать файл без checkout, создавая конфликты.

---

**Повышение default effort до high (v2.1.94)**

- **Что это:** Уровень усилий модели (effort) по умолчанию повышен с medium до high для API-key, Bedrock/Vertex/Foundry, Team и Enterprise пользователей. Управляется через `/effort`.
- **Зачем:** Higher effort = больше reasoning tokens, более тщательный анализ кода. По обратной связи пользователей, medium не давал достаточной глубины для сложных задач рефакторинга и ревью.

---

**Безопасность -- исправления критических уязвимостей (v2.1.97-2.1.98)**

- Исправлена уязвимость command injection в POSIX `which` fallback для LSP binary detection (v2.1.101).
- Исправлен обход разрешений Bash tool: backslash-escaped флаг мог быть auto-allowed как read-only и вести к arbitrary code execution (v2.1.98).
- Исправлен обход compound Bash-команд в auto mode и bypass-permissions mode (v2.1.98).
- Исправлен `permissions.deny` не перекрывавший `permissionDecision: "ask"` от PreToolUse хука (v2.1.101).

---

#### Кейсы использования

**Кейс: Автоматическое code review с помощью Managed Agents в CI/CD**

- **Проблема:** Команда из 8 разработчиков тратила ~2 часа в день на code review каждого PR. Нужен автоматический first-pass review на security, performance и style issues перед человеческим ревью.
- **Решение:** Создали Managed Agent с system prompt "Senior code reviewer, focus on security and performance". Environment с `pytest`, `ruff`, `bandit`. В GitHub Actions workflow:
  1. При открытии PR -- создаётся Session через Managed Agents API
  2. Агент получает diff через Web Fetch + файлы через Read/Edit
  3. Запускает `bandit` и `ruff` через Bash
  4. Генерирует структурированный отчёт
  5. Постит как PR-комментарий
- **Результат:** Автоматический review за 2-3 минуты. За первую неделю нашёл 5 security issues (3 hardcoded secrets, 1 SQL injection, 1 path traversal), которые прошли бы мимо ручного ревью. Человеческий review сократился до ~45 минут/день -- ревьюер фокусируется на архитектуре, а не на lint-issues.

**Кейс: Focus View для overnight-агентных сессий**

- **Проблема:** Разработчик запускает Claude Code на ночной рефакторинг монорепо (100+ файлов). Утром сессия содержит 500+ строк вывода -- невозможно быстро понять, что произошло.
- **Решение:** `CLAUDE_CODE_NO_FLICKER=1 claude`, затем `Ctrl+O` для Focus View. Видит сжатый лог: "Edit 47 files (+1,230/-890)" -> финальный отчёт.
- **Результат:** Время на утренний review overnight-сессии сократилось с 30 минут до 5 минут. Можно сразу перейти к проверке diff, не прокручивая промежуточный вывод.

---

**Оценка:** Да, использовать прямо сейчас. Managed Agents -- главное событие недели: полностью управляемая инфраструктура для агентов, которая убирает 80% инженерной работы по созданию агентного pipeline. Focus View и Monitor tool -- важные QoL-улучшения для инженеров, работающих с долгими агентными сессиями. Security-фиксы v2.1.97-2.1.98 -- критически важно обновиться.

---

### 2. Codex (OpenAI) -- Приоритет 1

**Версии на этой неделе:** CLI v0.119.0 (10 апреля), v0.120.0 (11 апреля). Обновление модельного ряда (7 апреля).

#### Новые фичи и флаги

**Realtime Voice V2 по умолчанию (v0.119.0)**

- **Что это:** Голосовые сессии теперь используют WebRTC-путь V2 по умолчанию. Включает: настраиваемый транспорт (WebRTC/WebSocket), выбор голоса, нативную поддержку медиа в TUI, покрытие app-server.
- **Зачем:** V1 использовал WebSocket, что вносило задержку и не позволяло настраивать голос. V2 на WebRTC -- ниже latency, более естественный голосовой интерфейс. Это шаг к мультимодальному взаимодействию с агентом.
- **Пример:**
  ```bash
  codex  # V2 уже по умолчанию
  # В TUI: нажать микрофон или hotkey для голосового режима
  # Настройка транспорта: codex --realtime-transport webrtc
  ```

---

**Стриминг прогресса фоновых агентов в Realtime V2 (v0.120.0)**

- **Что это:** Background agents теперь стримят свой прогресс в реальном времени, пока основной агент продолжает работу. Follow-up ответы ставятся в очередь до завершения текущего ответа.
- **Зачем:** Раньше при запуске фонового агента (субагента) в Codex нужно было ждать его завершения, чтобы увидеть результат. Теперь прогресс виден в реальном времени -- можно отслеживать, что делает субагент, параллельно с основной работой.
- **Как использовать:** Поведение включено автоматически в v0.120.0. Прогресс фонового агента появляется в TUI по мере выполнения.

---

**Обогащённая поддержка MCP Apps и custom MCP-серверов (v0.119.0)**

- **Что это:** MCP Apps и custom MCP-серверы получили: resource reads, tool-call metadata, tool search по custom серверам, server-driven elicitations (сервер может запрашивать дополнительный ввод), file-parameter uploads, более надёжное обновление plugin cache.
- **Зачем:** До этого custom MCP-серверы были "второсортными гражданами" -- ограниченный набор операций. Теперь custom серверы получают паритет с built-in серверами: полноценные resource reads, поиск инструментов, загрузка файлов.
- **Пример конфигурации custom MCP-сервера:**
  ```toml
  # ~/.codex/config.toml
  [mcp_servers.my_internal_api]
  command = "npx @company/mcp-server"
  # Теперь поддерживает: resource reads, tool search, elicitations
  ```

---

**Remote workflows -- egress websocket, sandbox-aware filesystem (v0.119.0)**

- **Что это:** Remote/app-server workflows теперь поддерживают: egress websocket transport, remote `--cd` forwarding, включение remote-control в runtime, sandbox-aware filesystem APIs, экспериментальный `codex exec-server` subcommand.
- **Зачем:** Позволяет запускать Codex CLI удалённо (на сервере, в Docker) с полной поддержкой sandbox-политик и filesystem access. `exec-server` -- новый способ запуска headless Codex как backend-сервиса.
- **Пример:**
  ```bash
  # Подключение к удалённому серверу с форвардингом рабочей директории
  codex --remote wss://my-server.company.com --cd /projects/myapp

  # Включить remote control в runtime (не нужно перезапускать)
  # Внутри сессии -- remote control включается динамически
  ```

---

**Улучшения TUI (v0.119.0-0.120.0)**

- `Ctrl+O` -- копирование последнего ответа агента в буфер обмена (работает через SSH).
- `/resume` -- переход к сессии по ID или имени прямо из TUI.
- Настраиваемые уведомления: поддержка Warp OSC 9, opt-in уведомления при фокусе терминала.
- Custom status lines теперь включают переименованное название thread.
- Hooks: live running hooks показаны отдельно от завершённых.

---

**Обновление модельного ряда (7 апреля)**

- **Что это:** Из model picker убраны `gpt-5.2-codex`, `gpt-5.1-codex-mini`, `gpt-5.1-codex-max`, `gpt-5.1-codex`, `gpt-5.1`, `gpt-5`. С 14 апреля эти модели полностью удалятся для ChatGPT sign-in.
- **Зачем:** Консолидация модельного ряда. GPT-5.4 и GPT-5.4 mini -- текущий стандарт.

---

#### Кейсы использования

**Кейс: Голосовое управление агентом через Realtime V2 при code review**

- **Проблема:** Разработчик проводит code review, одновременно читая код на экране. Печатать команды агенту -- переключение контекста.
- **Решение:** Обновил до Codex CLI 0.119.0. Realtime V2 по умолчанию. Голосом: "Check this function for race conditions and suggest a fix" -- агент анализирует, предлагает исправление. "Now run the tests" -- запускает.
- **Результат:** Code review с голосовым управлением на ~40% быстрее, чем с ручным вводом. Меньше переключений контекста. Особенно эффективно при review больших PR (500+ строк).

---

**Оценка:** Да, обновить до v0.120.0. Realtime V2 -- существенное улучшение UX. Стриминг прогресса фоновых агентов -- важная фича для мультиагентных workflow. Remote workflows с sandbox-aware filesystem -- ключевое для enterprise. Deprecated models -- проверить, не используете ли вы gpt-5.1/gpt-5.2 в пайплайнах.

---

### 3. Google (Stitch / AI Studio / Jules / Gemini CLI) -- Приоритет 2

**Версии на этой неделе:** Gemini CLI v0.37.0 (8 апреля), v0.37.1 (10 апреля)

#### Новые фичи

**Chapters -- логическая группировка взаимодействий агента (v0.37.0/v0.37.1)**

- **Что это:** Новая система "Chapters" (главы) -- автоматическая группировка действий агента по инструментам и намерениям. Агент создаёт логические блоки: "Исследование кодовой базы", "Написание тестов", "Рефакторинг", с нарративными переходами между ними.
- **Зачем:** В долгих агентных сессиях (30+ минут) лог превращается в сплошной поток tool calls. Chapters создают структуру -- проще понять, на каком этапе агент находится и что уже сделано.
- **Пример:**
  ```
  --- Chapter 1: Codebase Investigation ---
  [Read] src/auth/login.ts
  [Read] src/auth/session.ts
  [Grep] "validateToken" across src/

  --- Chapter 2: Test Writing ---
  [Write] tests/auth/login.test.ts
  [Bash] npm test -- --filter auth
  ```

---

**Динамическое расширение sandbox для Linux и Windows (v0.37.0)**

- **Что это:** Sandbox теперь может динамически расширять доступные пути и worktree-директории в runtime, без перезапуска сессии. Реализовано для Linux (bubblewrap) и Windows (нативный sandbox).
- **Зачем:** Раньше если агенту нужен был доступ к новой директории (например, git clone в новое место), требовался перезапуск с обновлённым конфигом. Теперь sandbox адаптируется на лету.

---

**`forbiddenPaths` -- OS-специфичные запрещённые пути (v0.37.0)**

- **Что это:** Новая настройка в `GlobalSandboxOptions` -- список абсолютных путей, доступ к которым всегда запрещён для агента, независимо от других разрешений. Содержимое `.gitignore` и аналогичных файлов автоматически добавляется в forbidden paths.
- **Зачем:** Дополнительный слой защиты: даже если sandbox расширяется динамически, определённые пути (конфиденциальные конфиги, ключи, .env файлы) остаются недоступными.
- **Пример в settings.json:**
  ```json
  {
    "tools": {
      "sandbox": {
        "forbiddenPaths": ["/etc/secrets", "~/.ssh", "~/.aws/credentials"]
      }
    }
  }
  ```

---

**Secret visibility lockdown для env-файлов (v0.37.0)**

- **Что это:** Реализован lockdown видимости секретов в environment-файлах (.env, .env.local и т.д.). Агент не может прочитать значения секретных переменных даже при наличии доступа к файлу.
- **Зачем:** Частая проблема: агент имеет доступ к рабочей директории и может прочитать `.env` с API-ключами, паролями БД и т.д. Secret lockdown скрывает значения, оставляя видимыми только имена переменных.

---

**Persistent browser session management (v0.37.0)**

- **Что это:** Browser agent теперь поддерживает persistent sessions -- состояние браузера сохраняется между вызовами. Также добавлены: динамическое обнаружение read-only tools, sandbox-aware initialization, `maxActionsPerTask` для ограничения числа действий.
- **Зачем:** Раньше каждый вызов browser agent начинался с чистого состояния -- нужно было повторно авторизоваться, загружать страницы. Persistent sessions устраняют эту проблему.
- **Настройка `maxActionsPerTask`:**
  ```json
  {
    "browser": {
      "maxActionsPerTask": 50
    }
  }
  ```

---

**CI skill -- автоматическая репликация CI-ошибок (v0.37.0)**

- **Что это:** Новый встроенный skill для автоматического воспроизведения CI-ошибок локально. Агент анализирует лог ошибки CI, воспроизводит её в локальном окружении и предлагает fix.
- **Зачем:** Отладка CI-ошибок -- типичная рутина: скопировать лог, понять контекст, воспроизвести локально. CI skill автоматизирует этот цикл.

---

**Jules -- CI Fixer + Gemini 3.1 Pro**

- Jules теперь автоматически обнаруживает и исправляет CI-ошибки на PR, которые он создаёт. Цикл: ошибка GitHub Actions -> анализ -> fix -> новый коммит -> повторный запуск CI.
- Gemini 3.1 Pro доступен как дефолтная модель для Pro-пользователей.

**Stitch / AI Studio**

- Stitch: значимых технических релизов на этой неделе нет. На форумах -- множество жалоб на стабильность (export ZIP не работает, "Stitch is unavailable" ошибки, stuck генерации). Технически -- без обновлений.
- AI Studio: Gemma 4 модели (`gemma-4-26b-a4b-it`, `gemma-4-31b-it`) доступны через API с 2 апреля. Flex и Priority inference tiers с 1 апреля.

---

#### Кейсы использования

**Кейс: Структурированный рефакторинг с Chapters + dynamic sandbox**

- **Проблема:** Команда запускала Gemini CLI для рефакторинга authentication-модуля (50+ файлов). Лог сессии -- 800 строк, невозможно понять прогресс.
- **Решение:** Обновились до v0.37.1. Chapters автоматически разбили сессию на блоки: "Investigation" (grep по паттернам), "Planning" (создание плана), "Implementation" (правки файлов), "Testing" (запуск тестов). Dynamic sandbox позволил агенту clone зависимый репозиторий без перезапуска.
- **Результат:** Время на review лога сессии сократилось с 20 минут до 5 минут -- Chapters дают навигацию по логическим блокам. Dynamic sandbox устранил 3 перезапуска, которые были нужны раньше для расширения доступа.

---

**Оценка:** Да, обновить до v0.37.1. Chapters -- полезная навигация для долгих сессий. Dynamic sandbox expansion и forbiddenPaths -- серьёзные production-grade улучшения безопасности. CI skill -- экономия времени на отладке CI.

---

### 4. xAI (инструменты для кода и агентов) -- Приоритет 3

**Новых релизов на этой неделе нет.**

**Текущее состояние (по состоянию на 13 апреля 2026):**

- **Grok 4.20 Beta 2** (3 марта) -- текущий флагман. 4-агентная система. 2M context window (API).
- **Grok 4.1 Fast** -- enterprise API, оптимизирован для скорости. Поддерживает agent tools, remote MCP, Files API. $0.20/M input tokens.
- **Agent tools:** Web Search, X Search, Code Interpreter, Collections Search. Цена: до $5 за 1000 вызовов.
- **Grok 5:** Training на Colossus 2 завершается в апреле. Internal testing -- апрель-май. Public beta -- прогноз май-июнь 2026. Polymarket: 33% вероятность до 30 июня.

---

**Оценка:** Пока нет -- новых технических релизов нет. grok-code-fast-1 и Grok 4.1 Fast полезны как дешёвые модели для вспомогательных задач, но экосистема значительно беднее конкурентов. Ждать Grok 5.

---

## Таблица сравнения

| Инструмент | Новые фичи | Новые кейсы | Влияние | Тестировать на этой неделе |
|---|---|---|---|---|
| **Claude Code** v2.1.94-101 + Managed Agents | Managed Agents (public beta), `ant` CLI, Focus View, Monitor tool, PID namespace sandbox, Vertex AI wizard, `/team-onboarding`, OS CA trust, Perforce mode, default effort=high | CI/CD code review через Managed Agents; Focus View для overnight-сессий | Высокое | Да |
| **Codex CLI** v0.119.0-0.120.0 | Realtime Voice V2 (default), background agent streaming, MCP Apps enrichment, remote egress websocket, sandbox-aware FS, exec-server, TUI improvements | Голосовое code review через Realtime V2 | Среднее | Да |
| **Gemini CLI** v0.37.0-0.37.1 | Chapters (topic grouping), dynamic sandbox expansion Linux/Win, forbiddenPaths, secret lockdown, persistent browser sessions, CI skill, maxActionsPerTask | Структурированный рефакторинг с Chapters | Среднее | Да |
| **xAI** | Нет новых релизов | -- | Низкое | Нет |

---

## Рекомендации на неделю

1. **Попробовать Claude Managed Agents для автоматического code review.** Создайте агента через Python SDK или `ant` CLI, настройте Environment с нужными пакетами, подключите к GitHub Actions. Минимальный пайплайн: открытие PR -> создание Session -> агент анализирует diff -> постит комментарий. Начните с security review (bandit + ruff), затем расширяйте. Документация: https://docs.anthropic.com, beta-заголовок `managed-agents-2026-04-01`.

2. **Обновить Claude Code до v2.1.101 и включить Focus View.** Установите `CLAUDE_CODE_NO_FLICKER=1` в shell-профиле, используйте `Ctrl+O` для переключения в Focus View. Особенно полезно для долгих сессий и overnight-задач. Также проверьте `/team-onboarding` -- поможет при onboarding новых членов команды. Обновление критически важно из-за security-фиксов в v2.1.97-2.1.98 (command injection, Bash permission bypass).

3. **Обновить Gemini CLI до v0.37.1 и настроить `forbiddenPaths`.** Добавьте в settings.json список путей, которые агент никогда не должен видеть (`.env`, SSH-ключи, AWS credentials). Протестируйте Chapters -- они автоматически структурируют длинные сессии. Также попробуйте CI skill для воспроизведения CI-ошибок локально.

---

## Источники

- [Claude Code Changelog -- Releasebot](https://releasebot.io/updates/anthropic/claude-code)
- [Anthropic Release Notes -- Releasebot](https://releasebot.io/updates/anthropic)
- [Claude Managed Agents: Anthropic Now Runs Your Agents For You -- Sid Bharath](https://sidbharath.com/blog/claude-managed-agents/)
- [Claude Managed Agents Deep Dive -- DEV Community](https://dev.to/bean_bean/claude-managed-agents-deep-dive-anthropics-new-ai-agent-infrastructure-2026-3286)
- [Claude Just Gave Us a Harness for Long-Running Agents -- YouTube](https://www.youtube.com/watch?v=DpfLbBuhHOg)
- [Decoding the Claude Code April 2026 Changelog -- Apiyi Blog](https://help.apiyi.com/en/claude-code-changelog-2026-april-updates-en.html)
- [Codex Changelog -- OpenAI Developers](https://developers.openai.com/codex/changelog/)
- [Codex CLI 0.119.0 -- Reddit CodexAutomation](https://www.reddit.com/r/CodexAutomation/comments/1sicqz2/codex_cli_update_01190_realtime_voice_v2_by/)
- [Codex CLI 0.120.0 -- Reddit CodexAutomation](https://www.reddit.com/r/CodexAutomation/comments/1sicrhg/codex_cli_update_01200_realtime_v2_background/)
- [Codex by OpenAI -- Releasebot](https://releasebot.io/updates/openai/codex)
- [Gemini CLI v0.37.1 Changelog -- geminicli.com](https://geminicli.com/docs/changelogs/latest/)
- [Gemini CLI Release Notes -- Releasebot](https://releasebot.io/updates/google/gemini-cli)
- [Jules Changelog -- jules.google](https://jules.google/docs/changelog/)
- [xAI Release Notes](https://docs.x.ai/developers/release-notes)
- [Grok 5 Release Date -- Fello AI](https://felloai.com/all-we-know-so-far-about-grok-5/)
- [Current Grok Version April 2026 -- AIToolsRecap](https://aitoolsrecap.com/Blog/current-grok-version-april-2026-xai-models-explained)
