# Tooling Watchlist — Отчёт за неделю 31 марта — 6 апреля 2026

> **Дата:** 6 апреля 2026  
> **Период:** 31 марта — 6 апреля 2026  
> **Формат:** Markdown v3.1  
> **Приоритет тем:** автономия агентов, безопасность

---

## Executive Summary

- **Claude Code выпустил 5 версий за неделю (v2.1.89–2.1.92)**: ключевые изменения касаются безопасности auto mode, новых хук-событий (`PermissionDenied`, `defer`), принудительной синхронизации managed-настроек (`forceRemoteSettingsRefresh`), ускорения работы с большими файлами и устранения проблем с PowerShell. Инструмент продолжает двигаться в сторону автономной работы с жёсткими барьерами безопасности.
- **Codex CLI v0.118.0 (31 марта)**: главные изменения — OS-уровневая изоляция сети в Windows sandbox (вместо env-var-костылей), поддержка `codex exec` с одновременным stdin и prompt, динамическое обновление bearer-токенов для корпоративных LLM-провайдеров. Ориентация на enterprise и CI/CD-пайплайны.
- **Gemini CLI v0.36.0 (1 апреля)**: крупный релиз — мультиреестровая архитектура для субагентов, нативный macOS Seatbelt и Windows sandbox, поддержка git worktree для параллельных изолированных сессий, JIT-инъекция контекста в субагенты. Серьёзный шаг в сторону production-grade агентной изоляции.
- **Claude Code — политика OpenClaw (4 апреля)**: с 4 апреля подписки Claude Code больше не покрывают использование через сторонние harness-обёртки (OpenClaw и аналоги). Использование через third-party клиентов требует отдельной оплаты по pay-as-you-go. Важно для команд, использующих Claude Code не через официальный CLI.
- **xAI**: новых релизов на этой неделе нет. Grok 4.20 Beta 2 остаётся текущим флагманом. grok-code-fast-1 доступен через API и ряд партнёрских IDE. Grok 5 — прогноз Q2 2026.

---

## По инструментам

---

### 1. Claude Code / Cowork (Anthropic) — Приоритет 1

**Версии на этой неделе:** v2.1.87 (28 марта), v2.1.88–v2.1.92 (31 марта — 4 апреля 2026)

#### Новые фичи и флаги

**`forceRemoteSettingsRefresh` — принудительная синхронизация managed-политик (v2.1.92)**

- **Что это:** Новая policy-настройка в managed-settings. Когда установлена, CLI при старте блокирует запуск до тех пор, пока не получит свежую копию managed-настроек с сервера. Если fetch не удался — CLI завершается с ошибкой (поведение "fail-closed").
- **Зачем:** В enterprise-окружениях managed-настройки (политики разрешений, запрещённые команды, допустимые модели) могут кэшироваться локально. Без этой опции агент мог запускаться со старой политикой, если сервер управления временно недоступен. Теперь, если свежие политики получить невозможно — агент не запустится вовсе.
- **Пример использования:** В managed-settings.json организации:
  ```json
  {
    "forceRemoteSettingsRefresh": true
  }
  ```
  После этого `claude` при запуске обязательно подтянет политики с сервера. Если сервер недоступен — завершится с ошибкой. Полезно в CI/CD, где нужна гарантия, что агент всегда работает по актуальной политике.

---

**`disableSkillShellExecution` — отключение инлайн-шелл-выполнения в skills (v2.1.91)**

- **Что это:** Настройка в `settings.json`, запрещающая инлайн-выполнение shell-команд из файлов skills, кастомных slash-команд и команд плагинов.
- **Зачем:** Skills могут содержать инлайн bash-блоки, которые выполняются автоматически при активации skill. В production-окружениях, где skills раздаются через managed-plugins, это открывает вектор для непреднамеренного или злонамеренного выполнения кода через skill-файлы. Опция позволяет полностью отключить этот путь.
- **Пример:**
  ```json
  {
    "disableSkillShellExecution": true
  }
  ```

---

**MCP tool result persistence override (v2.1.91)**

- **Что это:** Новая возможность для MCP-серверов: через аннотацию `_meta["anthropic/maxResultSizeChars"]` сервер может запросить сохранение результата размером до 500 КБ (вместо стандартного лимита).
- **Зачем:** Без этой опции большие результаты MCP-инструментов (схемы баз данных, большие JSON-ответы) усекались, что ломало рабочие процессы с большими схемами или ответами.
- **Пример использования в MCP-сервере:**
  ```json
  {
    "content": [...],
    "_meta": {
      "anthropic/maxResultSizeChars": 500000
    }
  }
  ```

---

**`PermissionDenied` хук + `retry: true` (v2.1.89)**

- **Что это:** Новое хук-событие, которое срабатывает после того, как классификатор auto mode заблокировал действие агента. Хук может вернуть `{retry: true}`, чтобы сигнализировать агенту о повторной попытке с изменённым подходом.
- **Зачем:** В auto mode агент мог "застрять" при блокировке опасного действия, не зная, что делать дальше. Теперь можно добавить логику в хук: например, залогировать блокировку и предложить агенту альтернативный путь.
- **Пример hooks.json:**
  ```json
  {
    "PermissionDenied": {
      "command": "node log-denial.js",
      "description": "Log blocked actions and optionally allow retry"
    }
  }
  ```
  Если скрипт вернёт `{"retry": true}` — агент попытается выполнить задачу другим способом.

---

**`defer` в PreToolUse хуках (v2.1.89)**

- **Что это:** Новое решение в PreToolUse хуках — `defer`. Позволяет headless-сессии "заморозить" выполнение на конкретном вызове инструмента и дождаться ручного одобрения через `-p --resume`.
- **Зачем:** В headless/CI-сценариях иногда нужно, чтобы агент остановился перед определённым классом действий (например, перед git push или деплоем) и дал человеку возможность одобрить. Раньше это требовало полной остановки сессии.
- **Пример:**
  ```json
  // PreToolUse хук возвращает:
  {"decision": "defer"}
  ```
  Агент останавливается. Потом: `claude -p --resume <session_id>` — хук перевычисляется, агент продолжает.

---

**`CLAUDE_CODE_NO_FLICKER=1` — рендеринг без мерцания (v2.1.88/89)**

- **Что это:** Переменная окружения, включающая flicker-free alt-screen рендеринг с виртуализированным скроллбэком.
- **Зачем:** В долгих сессиях с большим объёмом вывода (особенно в tmux, iTerm2) возникало заметное мерцание при обновлении UI. Это opt-in решение устраняет проблему.
- **Пример:**
  ```bash
  CLAUDE_CODE_NO_FLICKER=1 claude
  ```

---

**Интерактивный Bedrock Setup Wizard (v2.1.92)**

- **Что это:** При выборе "3rd-party platform" на экране логина теперь доступен пошаговый мастер настройки AWS Bedrock: аутентификация, регион, верификация credentials, закрепление модели.
- **Зачем:** До этого настройка Bedrock требовала ручной правки конфигов. Wizard снижает порог входа для корпоративных пользователей, использующих Claude через AWS.

---

**Производительность (v2.1.90–2.1.92)**

- Write tool — ускорение вычисления diff для больших файлов на **60%** (файлы с табуляцией, `&`, `$`).
- SSE-транспорт: обработка больших стриминговых фреймов теперь линейная (было квадратичной).
- SDK-сессии с длинными историями больше не замедляются квадратично при записи транскриптов.
- `/resume` — загрузка сессий по проектам теперь параллельная.

---

**Политика third-party harness (4 апреля)**

С 4 апреля 2026 Anthropic ограничила использование подписок Claude Code через сторонние обёртки (OpenClaw, OpenRouter и аналоги). Подписочные лимиты больше не применяются к этим клиентам — требуется отдельное pay-as-you-go. Официальная причина: "usage patterns of third-party tools weren't built into subscription model". Это касается именно подписочных планов, но не API-доступа.

---

#### Кейсы использования

**Кейс: Автономный overnight-анализ портфеля через Auto Mode + defer-хук**

- **Проблема:** Команда аналитиков использует Claude Code для ночной обработки финансовых данных (анализ 50+ CSV, построение отчётов). Auto mode позволяет не прерываться на каждое действие, но git push в конце пайплайна требует человеческого одобрения.
- **Решение:** Настроили PreToolUse хук с `defer` для команд `git push` и `gh pr create`. Агент запускается с auto mode в 23:00, обрабатывает данные, создаёт файлы и коммиты. Когда доходит до push — сессия "замораживается". Утром аналитик делает `claude -p --resume <id>`, просматривает дифф, одобряет.
- **Результат:** Обработка 50 файлов + подготовка PR занимает ~3 часа без участия человека. Утреннее ревью — 10 минут вместо 4 часов ручной работы.

**Кейс: Computer Use для тестирования UI-компонентов**

- **Проблема:** Разработчик компонентной библиотеки тратил 2 часа в день на ручной smoke-test: открыть браузер, пройти по 20 компонентам, проверить визуальное соответствие макету.
- **Решение:** Включил computer use в Claude Code CLI (`/mcp` → `computer-use` → Enable). Написал task: "открой localhost:3000/storybook, пройди по каждому компоненту, сделай скриншот, сравни с эталоном в /designs". Агент использует macOS accessibility API для навигации, берёт скриншоты, сохраняет отчёт.
- **Результат:** Smoke-test занимает 25 минут против 2 часов. Автоматически фиксирует регрессии. (Ограничение: macOS only, Pro/Max план.)

---

**Оценка:** Да, использовать прямо сейчас. Релизы этой недели — прежде всего production-hardening: безопасность (forceRemoteSettingsRefresh, disableSkillShellExecution, defer-хуки), производительность (60% ускорение Write tool) и стабильность долгих сессий. Особенно актуально для enterprise и CI/CD. Computer use — перспективно, но пока macOS only и в preview.

---

### 2. Codex (OpenAI) — Приоритет 1

**Версии на этой неделе:** CLI v0.118.0 (31 марта 2026), Codex Enterprise seat (2 апреля 2026)

#### Новые фичи и флаги

**Windows sandbox — OS-уровневая изоляция сети (v0.118.0)**

- **Что это:** Windows sandbox теперь использует egress-правила уровня операционной системы для ограничения сетевого трафика агента — вместо прежней схемы на основе environment variables.
- **Зачем:** Предыдущая схема (прокси через env vars) была обходима: процессы, игнорирующие env vars (например, часть .NET runtime), могли выходить в сеть в обход ограничений. OS-level egress не обходится через env vars.
- **Как использовать:** Включается автоматически при запуске Codex CLI на Windows в sandbox-режиме после обновления до v0.118.0:
  ```bash
  npm install -g @openai/codex@0.118.0
  codex --sandbox  # sandbox теперь использует OS-egress на Windows
  ```
  Для проверки: в изолированном сценарии попытка агента обратиться к внешнему URL должна блокироваться системой, а не только proxy-настройками.

---

**`codex exec` — prompt-plus-stdin (v0.118.0)**

- **Что это:** Команда `codex exec` теперь поддерживает одновременную передачу stdin-потока и отдельного prompt-аргумента.
- **Зачем:** Раньше при скриптовом использовании нужно было выбирать: либо передать prompt через аргумент, либо данные через stdin. Типичная задача — "проанализируй этот лог-файл" (данные через stdin) + "и найди аномалии" (prompt) — требовала либо конкатенации, либо промежуточных файлов.
- **Пример:**
  ```bash
  # Передаём лог через stdin + отдельный аналитический prompt
  cat server.log | codex exec "Find all 5xx errors and summarize the root causes"
  
  # Или через explicit piping в shell-скрипт:
  git diff HEAD~1 | codex exec "Review this diff for security issues and breaking changes"
  ```

---

**Динамическое обновление bearer-токенов для custom model providers (v0.118.0)**

- **Что это:** Custom model providers (корпоративные LLM-серверы, внутренние API) теперь могут возвращать короткоживущие bearer-токены, которые Codex CLI автоматически обновляет по мере истечения, через OAuth 2.0 client credentials flow.
- **Зачем:** В enterprise-средах внутренние API часто используют короткоживущие JWT (15–60 минут). Раньше это требовало либо статических токенов (небезопасно), либо внешних wrapper-скриптов для ротации. Теперь Codex CLI умеет делать это сам.
- **Конфигурация в `~/.codex/config.toml`:**
  ```toml
  [model_providers.my_internal_llm]
  base_url = "https://internal.company.com/v1"
  auth_type = "dynamic_bearer"
  token_endpoint = "https://auth.company.com/token"
  client_id = "codex-cli"
  client_secret_env = "INTERNAL_LLM_CLIENT_SECRET"
  ```

---

**ChatGPT device code login для app-server (v0.118.0)**

- **Что это:** App-server клиенты теперь могут аутентифицироваться через device code flow (6-значный код + подтверждение с другого устройства), а не только через browser callback.
- **Зачем:** В headless-средах (сервер без GUI, Docker-контейнер, remote SSH) browser callback недоступен. Device code flow решает это: запускаешь `codex login` в терминале, получаешь код, вводишь на телефоне.
- **Пример:**
  ```bash
  codex login  # показывает 6-значный код
  # Открываешь https://chatgpt.com/activate на телефоне
  # Вводишь код → авторизация завершена
  ```

---

**Codex Enterprise seat — отдельный тип лицензии (2 апреля)**

- **Что это:** В ChatGPT Enterprise теперь доступны "Codex-only seats" — лицензии, дающие доступ только к Codex без ChatGPT workspace. Оплата строго по потреблению (pay-as-you-go, token-based), без фиксированной ставки.
- **Зачем:** Позволяет организациям добавлять разработчиков в Codex-пайплайны без покупки полного ChatGPT-доступа. Удобно для пилотных проектов и команд, которым нужен только агент для кода.

---

#### Кейсы использования

**Кейс: CI/CD-пайплайн с анализом PR через `codex exec` + stdin**

- **Проблема:** Команда хотела автоматически анализировать каждый pull request на security issues и breaking changes до мержа. Предыдущее решение (передача diff через файл) требовало промежуточных шагов в GitHub Actions.
- **Решение:** В GitHub Actions workflow:
  ```yaml
  - name: Security review with Codex
    run: |
      git diff origin/main...HEAD | \
        codex exec "Review this diff: identify security vulnerabilities, breaking API changes, and missing tests. Output JSON."
  ```
  Результат JSON парсится и постится как review-комментарий к PR. Используется sandbox с OS-egress для изоляции (актуально на Windows runners).
- **Результат:** Security review для среднего PR (200-500 строк) — 45 секунд. Нашли 3 реальные уязвимости за первую неделю (hardcoded credential, SQL injection через format string, отсутствующая валидация на публичном endpoint).

---

**Оценка:** Да, использовать прямо сейчас — особенно `codex exec` с stdin в CI/CD. OS-level Windows sandbox важен для enterprise-команд с Windows-окружением. Dynamic bearer tokens — ключевое улучшение для корпоративных деплоев с внутренними LLM.

---

### 3. Google (Stitch / AI Studio / Jules / Gemini CLI) — Приоритет 2

**Версии на этой неделе:** Gemini CLI v0.36.0 (1 апреля 2026)

#### Новые фичи

**Мультиреестровая архитектура + изоляция инструментов субагентов**

- **Что это:** Новая архитектура для субагентов: каждый субагент работает в своём "реестре инструментов" (tool registry) с явной фильтрацией. Субагент видит только те инструменты, которые ему назначены, а не весь набор главного агента.
- **Зачем:** Без этой изоляции субагент мог случайно использовать инструменты, предназначенные только для главного агента (например, write_file, когда нужен только read_file). Это открывало пути для непреднамеренного изменения файлов или состояния через субагентные цепочки.
- **Активация:** В settings.json или через `GEMINI_SUBAGENT_TOOL_ISOLATION=true`. По умолчанию agents отключены (`chore(config): disable agents by default`), включить явно:
  ```json
  {
    "agents": {
      "enabled": true,
      "toolIsolation": true
    }
  }
  ```

---

**Нативный macOS Seatbelt + Windows sandbox (v0.36.0)**

- **Что это:** Строгий macOS sandboxing через Seatbelt (allowlist-based), нативный Windows sandbox. Также добавлен `SandboxManager` с refactored stateless архитектурой и явным Deny-интерфейсом.
- **Профили для macOS Seatbelt:**
  ```bash
  # Включить sandbox с профилем
  SEATBELT_PROFILE=permissive-closed gemini -s -p "run tests"
  # Профили: permissive-open (default), permissive-closed, permissive-proxied, restrictive-open, restrictive-closed
  
  # Через settings.json:
  {"tools": {"sandbox": "sandbox-exec"}}
  ```
- **Зачем:** До этого sandbox работал через Docker или bubblewrap. Seatbelt — нативный macOS механизм, не требует Docker, работает быстрее, меньше зависимостей.

---

**Git worktree support — параллельные изолированные сессии**

- **Что это:** Gemini CLI теперь поддерживает `git worktree` для запуска нескольких изолированных агентных сессий в одном репозитории одновременно. Каждая сессия работает в своём worktree, не затрагивая другие.
- **Зачем:** При параллельной работе нескольких агентов в одном репо без worktree они конкурируют за uncommitted изменения. Worktree-изоляция устраняет конфликты.
- **Пример использования:**
  ```bash
  # Запустить две параллельные агентные задачи
  gemini --worktree -p "Fix all TypeScript errors in /src/auth"
  gemini --worktree -p "Write unit tests for /src/payment"
  # Каждая задача в своём worktree, без конфликтов
  ```

---

**JIT-инъекция контекста в субагенты (v0.36.0)**

- **Что это:** Субагенты теперь получают контекст "just-in-time" — память и релевантный контекст из GEMINI.md инъецируются в момент запуска субагента (а не копируются полностью из главного агента). Обход вверх по дереву каталогов ограничен git root.
- **Зачем:** Полное копирование контекста главного агента в субагент приводило к раздуванию контекстного окна. JIT-подход даёт субагенту только нужный контекст.

---

**Plan mode в non-interactive режиме**

- **Что это:** Plan mode теперь работает без интерактивного ввода — можно запускать через скрипты и CI.
- **Пример:**
  ```bash
  gemini --plan --non-interactive -p "Refactor authentication module to use JWT"
  # Агент составит план и выполнит его без остановки на подтверждения
  ```

---

**Browser privacy controls (v0.36.0)**

- **Что это:** Новые элементы управления приватностью для browser agent: consent perм flow, sensitive action controls, read-only noise reduction. Добавлена security prompt при старте browser agent.
- **Зачем:** Browser agent имеет доступ к экрану и может перехватывать чувствительные данные. Новые контролы требуют явного разрешения перед первым запуском и перед sensitive действиями (формы с паролями, платёжные данные).

---

**Google Stitch / Jules / AI Studio**

- **Stitch:** Новых значимых технических релизов на этой неделе не зафиксировано. Основные возможности (Gemini 3, AI Canvas, voice design, instant prototypes, Design.md) — из обновления 19 марта.
- **Jules:** Новых релизов на этой неделе нет. Текущие возможности: async задачи через CLI (`jules-tools`), публичный API, free tier (15 задач/день), Pro ($19.99/мес).
- **AI Studio / Gemini API:** 1 апреля появились Flex и Priority inference tiers — больше вариантов оптимизации по цене/латентности. 2 апреля — выпуск `gemma-4-26b-a4b-it` и `gemma-4-31b-it`.

---

#### Кейсы использования

**Кейс: Параллельный рефакторинг монорепо через worktree + субагент изоляцию**

- **Проблема:** Команда из 3 разработчиков хотела параллельно рефакторить разные модули монорепо через Gemini CLI, не мешая друг другу uncommitted изменениями.
- **Решение:** Каждый разработчик запускает свою задачу через `gemini --worktree`. Агент изоляции инструментов (tool isolation) гарантирует, что субагенты внутри задачи не выходят за пределы своего модуля. Plan mode в non-interactive режиме для headless запуска.
- **Результат:** 3 параллельные задачи рефакторинга без git-конфликтов. По данным команды, общее время рефакторинга сократилось с 2 дней до 6 часов.

---

**Оценка:** Да, v0.36.0 — существенный релиз для production-окружений. Worktree support, Seatbelt sandbox и изоляция субагентов — это конкретные инженерные улучшения, а не маркетинг. Рекомендуется обновление и тест worktree-workflow для команд, работающих с монорепо.

---

### 4. xAI (инструменты для кода и агентов) — Приоритет 3

**Новых релизов на этой неделе нет.**

**Текущее состояние (по состоянию на 6 апреля 2026):**

- **Grok 4.20 Beta 2** (3 марта) — текущий флагман. 4-агентная система (Grok-координатор, Harper-исследователь, Benjamin-логик, Lucas-контрарианец). Версия Heavy — 16 специализированных агентов.
- **grok-code-fast-1** — специализированная модель для agentic coding. MoE-архитектура (~314B параметров), 256K контекст, ~92 токена/сек, SWE-bench Verified: 70.8%. Доступна через xAI API и партнёрские IDE.
- **API цены на agent tools:** снижены до $5 за 1000 успешных вызовов (снижение до 50%).
- **Grok 5:** training завершается в апреле, public beta прогнозируется в мае–июне. Colossus 2 расширяется до 1.5 ГВт к апрелю.

---

**Оценка:** Пока нет — новых технических релизов нет. grok-code-fast-1 интересен как дешёвая модель для субагентных coding-задач (30% стоимости относительно основного Grok), но экосистема значительно беднее Claude Code / Codex. Ждать Grok 5.

---

## Таблица сравнения

| Инструмент | Новые фичи | Новые кейсы | Влияние | Тестировать на этой неделе |
|---|---|---|---|---|
| **Claude Code** v2.1.89–92 | forceRemoteSettingsRefresh, disableSkillShellExecution, PermissionDenied хук, defer в PreToolUse, MCP result 500KB, Write tool +60%, Bedrock wizard | Overnight pipeline с defer-хуком; Computer use для UI smoke-test | Высокое | Да |
| **Codex CLI** v0.118.0 | OS-level Windows sandbox, codex exec stdin+prompt, dynamic bearer tokens, device code login | CI/CD PR security review через stdin pipe | Среднее | Да (если используете Windows или корпоративные LLM) |
| **Gemini CLI** v0.36.0 | Mультиреестровая субагент-изоляция, Seatbelt/Windows sandbox, git worktree, JIT context, plan non-interactive, browser privacy | Параллельный рефакторинг монорепо через worktree | Среднее | Да (для тех, кто использует Gemini CLI) |
| **xAI** | Нет новых релизов | — | Низкое | Нет |

---

## Рекомендации на неделю

1. **Протестировать `defer` хук в Claude Code для production-пайплайнов:** Если у вас есть headless/overnight агентные задачи, добавьте PreToolUse хук с `defer` для деструктивных операций (git push, деплой, удаление файлов). Это даёт автономность там, где она безопасна, и человека в петле — там, где нужно. Документация: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md

2. **Обновить Codex CLI до v0.118.0 и попробовать `codex exec` с stdin в CI:** Добавьте `git diff origin/main...HEAD | codex exec "Review for security issues, output JSON"` как шаг в PR workflow. Это занимает 5 минут на настройку и даёт автоматический security review на каждый PR. Установка: `npm install -g @openai/codex@0.118.0`

3. **Обновить Gemini CLI до v0.36.0 и попробовать `--worktree` для параллельных задач:** Если у вас монорепо и несколько агентных задач — запустите их через `gemini --worktree`. Seatbelt sandbox включите через `SEATBELT_PROFILE=permissive-closed` (macOS) для дополнительной изоляции. Установка: `npm install -g @google/gemini-cli@0.36.0`

---

## Источники

- [Claude Code Changelog — GitHub](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- [Claude Code Release Notes — Releasebot](https://releasebot.io/updates/anthropic/claude-code)
- [Codex Changelog — OpenAI Developers](https://developers.openai.com/codex/changelog/)
- [Codex CLI v0.118.0 — Reddit CodexAutomation](https://www.reddit.com/r/CodexAutomation/comments/1s8ysxk/codex_cli_update_01180_proxyonly_windows_sandbox/)
- [OpenAI Release Notes — Releasebot](https://releasebot.io/updates/openai)
- [Gemini CLI v0.36.0 Changelog](https://geminicli.com/docs/changelogs/latest/)
- [Gemini CLI Release Notes — Releasebot](https://releasebot.io/updates/google/gemini-cli)
- [Gemini CLI Sandboxing Docs](https://google-gemini.github.io/gemini-cli/docs/cli/sandbox.html)
- [xAI Release Notes](https://docs.x.ai/developers/release-notes)
- [Grok 5 Release Date — NxCode](https://www.nxcode.io/resources/news/grok-5-release-date-latest-news-2026)
- [Claude Code Computer Use — AI Blew My Mind](https://aiblewmymind.substack.com/p/claude-computer-use-guide-6-workflows-tested)
- [Anthropic Claude Code: OpenClaw policy — TechCrunch](https://techcrunch.com/2026/04/04/anthropic-says-claude-code-subscribers-will-need-to-pay-extra-for-openclaw-support/)
- [Codex CLI Technical Reference — Blake Crosley](https://blakecrosley.com/guides/codex)
- [Gemini CLI Worktree GitHub Issue #21901](https://github.com/google-gemini/gemini-cli/issues/21901)
