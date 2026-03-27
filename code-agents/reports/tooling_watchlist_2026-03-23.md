# Tooling Watchlist — Code & Agents

> **Отчёт за неделю:** 17–23 марта 2026  
> **Дата генерации:** 23 марта 2026  
> **Версия спецификации:** 3.1

---

## Executive Summary

- **Claude Code выпустил 5 релизов (v2.1.77–2.1.81)** с критическими изменениями для CI/CD-пайплайнов (`--bare`), безопасности хуков и нового механизма каналов (`--channels`). Opus 4.6 получил лимит вывода 64K/128K токенов — существенно расширяет возможности для длинных кодогенераций.
- **Codex CLI 0.116.0** добавил хук `userpromptsubmit` для перехвата и модификации промптов до выполнения — ключевая фича для enterprise-безопасности и автоматизации. В Codex App обновлены Automations с поддержкой разных моделей и уровней рассуждения на задачу.
- **Google Stitch перезапущен как «vibe design»** — бесконечный AI-канвас с голосовым управлением, одновременной генерацией 5 экранов, MCP-сервером и экспортом в AI Studio/Figma/React. Gemini CLI v0.34.0 включил Plan Mode по умолчанию и gVisor-песочницу.
- **Grok 4.20 вышел из беты** — 2M контекст, 230 tok/sec, мультиагентная система через параметр API `agent_count`. В коде обнаружен флаг `enable_grok_computer` — Musk подтвердил скорый запуск computer-use.
- **Тема недели: безопасность агентов.** Claude Code исправил критическую уязвимость с тихим отключением песочницы и обходом `deny`-правил в хуках. Codex добавил `userpromptsubmit` как гейткипер перед выполнением. Gemini CLI встроил gVisor. Тренд — все инструменты усиливают изоляцию выполнения.

---

## По инструментам

---

### 🔵 Приоритет 1: Claude Code / Cowork (Anthropic)

**5 релизов за неделю: v2.1.77 → v2.1.81 (17–20 марта 2026)**

#### Новые фичи

**1. Флаг `--bare` для headless CI/CD (v2.1.81)**

- **Что это:** CLI-флаг, который запускает Claude Code без hooks, LSP, синхронизации плагинов и обхода директорий скиллов. Синтаксис: `claude --bare -p "текст промпта" [--output-format json]`.
- **Зачем нужен:** В CI/CD-окружениях (GitHub Actions, Jenkins) IDE-функционал не нужен и вызывает ошибки — нет терминала для интерактива, нет LSP-сервера. `--bare` убирает всё лишнее, оставляя только ядро агента.
- **Пример использования:**
  ```bash
  # В GitHub Actions workflow
  claude --bare -p "Review this PR for security issues" --output-format json > review.json
  
  # В скрипте автоматической проверки
  claude --bare -p "Run lint and fix all TypeScript errors in src/" --output-format stream-json
  ```
- **Дополнительно:** снижение потребления RAM на ~80 МБ за счёт отказа от загрузки плагинов.

**2. Флаг `--channels` — push-сообщения от MCP-серверов (v2.1.81, research preview)**

- **Что это:** Экспериментальный флаг, позволяющий MCP-серверам отправлять сообщения прямо в сессию Claude Code в реальном времени. Синтаксис: `claude --channels`.
- **Зачем нужен:** До этого MCP-серверы могли только отвечать на запросы (pull-модель). С `--channels` сервер может сам инициировать отправку данных — например, уведомление о завершении CI-билда, алерт от мониторинга, обновление от другого агента.
- **Пример использования:**
  ```bash
  # Запуск с включёнными каналами
  claude --channels
  
  # MCP-сервер мониторинга может push'ить:
  # "Деплой staging завершён, 2 теста упали: test_auth.py, test_api.py"
  # Прямо в контекст текущей сессии
  ```
- **Статус:** Research preview — API каналов может измениться.

**3. `StopFailure` hook event (v2.1.78)**

- **Что это:** Новое событие в системе хуков, которое срабатывает, когда turn агента завершается из-за API-ошибки (rate limit, сбой авторизации, сетевая ошибка). Конфигурация в `.claude/settings.json` или `CLAUDE.md`.
- **Зачем нужен:** Раньше при падении API-вызова сессия просто останавливалась. Теперь можно автоматически реагировать: отправить уведомление в Slack, записать в лог, переключиться на fallback-модель, или подождать и повторить.
- **Пример использования:**
  ```json
  {
    "hooks": {
      "StopFailure": [{
        "type": "command",
        "command": "curl -X POST $SLACK_WEBHOOK -d '{\"text\": \"Claude Code сессия упала: rate limit\"}'"
      }]
    }
  }
  ```

**4. `${CLAUDE_PLUGIN_DATA}` — персистентное состояние плагинов (v2.1.78)**

- **Что это:** Переменная окружения, указывающая на директорию, где плагины могут хранить данные, которые сохраняются между обновлениями плагина. При `plugin uninstall` — запрос подтверждения перед удалением.
- **Зачем нужен:** Ранее обновление плагина удаляло все его данные (кеши, настройки, историю). Теперь плагины могут хранить конфигурацию и состояние в `${CLAUDE_PLUGIN_DATA}`, и оно переживает reinstall/update.
- **Пример:** Плагин для управления задачами хранит свой state в `${CLAUDE_PLUGIN_DATA}/tasks.json` — при обновлении плагина данные на месте.

**5. Frontmatter `effort`, `maxTurns`, `disallowedTools` для плагинных агентов (v2.1.78)**

- **Что это:** Новые поля frontmatter, которые плагины могут задавать в своих скиллах и агентах: `effort` (уровень усилия модели), `maxTurns` (максимальное число шагов), `disallowedTools` (список запрещённых инструментов).
- **Зачем нужен:** Позволяет плагин-авторам ограничивать поведение агента — например, review-плагин может запретить агенту использовать Bash и ограничить до 5 шагов, чтобы тот только читал код и писал комментарии, не выполняя команды.
- **Пример (frontmatter в skill файле):**
  ```yaml
  ---
  effort: low
  maxTurns: 5
  disallowedTools: ["Bash", "Write"]
  ---
  Review the PR and provide inline comments only.
  ```

**6. Opus 4.6 — выходные токены 64K по умолчанию / 128K максимум (v2.1.77)**

- **Что это:** Лимит выходных токенов для Opus 4.6 увеличен до 64K по умолчанию (ранее 16K), с возможностью до 128K.
- **Зачем нужен:** При генерации длинных файлов (миграции, большие рефакторинги, documentation) модель раньше обрезала вывод. Теперь можно генерировать целые модули за один шаг.

**7. `allowRead` sandbox setting (v2.1.77)**

- **Что это:** Новая настройка песочницы: `sandbox.filesystem.allowRead` — разрешает чтение определённых путей вне рабочей директории.
- **Зачем нужен:** В монорепозиториях агенту часто нужно читать shared-конфигурации или зависимости за пределами текущего пакета. `allowRead` разрешает чтение без разрешения записи — баланс безопасности и удобства.
- **Пример (`settings.json`):**
  ```json
  {
    "sandbox": {
      "filesystem": {
        "allowRead": ["/shared/configs", "/node_modules/.cache"]
      }
    }
  }
  ```

**8. Инструмент `ExitWorktree` (v2.1.79)**

- **Что это:** Новый встроенный инструмент, позволяющий агенту программно завершить работу в worktree и вернуться в основной рабочий каталог.
- **Зачем нужен:** При работе с git worktrees (параллельные ветки) агент может застрять в worktree после завершения задачи. `ExitWorktree` позволяет чисто выйти.

**9. `CLAUDE_CODE_DISABLE_CRON` env var (v2.1.79)**

- **Что это:** Переменная окружения для отключения фоновых cron-задач Claude Code. Синтаксис: `CLAUDE_CODE_DISABLE_CRON=1 claude`.
- **Зачем нужен:** В CI/CD и тестовых окружениях фоновые задачи мешают — запускают ненужные проверки, конкурируют за ресурсы. Этот флаг полностью отключает cron-подсистему.

**10. Исправление стоимости: prompt cache fix (v2.1.79–80)**

- **Что это:** Исправлена ошибка кеширования промптов, которая приводила к повторным запросам вместо использования кеша.
- **Зачем нужен:** Снижение стоимости API-вызовов **до 12x** для сессий с повторяющимся контекстом. Критично для команд с активным использованием — экономия может составить сотни долларов в месяц.

#### Исправления безопасности

- **Тихое отключение песочницы (v2.1.78):** Если `sandbox.enabled: true`, но зависимости песочницы отсутствовали, Claude Code молча работал без изоляции. Теперь показывается предупреждение при старте.
- **Обход deny-правил в хуках (v2.1.77):** PreToolUse хуки с `allow` могли перекрывать `deny`-правила — агент видел и пытался использовать заблокированные MCP-инструменты. Исправлено: `deny` теперь приоритетнее `allow`.
- **Защищённые директории в bypassPermissions (v2.1.78):** `.git`, `.claude` и другие защищённые директории были доступны на запись в режиме `bypassPermissions`. Исправлено.

#### Оптимизации производительности

- `--resume` стал на **45% быстрее** (v2.1.77).
- Старт на macOS ускорен на **~60 мс** (v2.1.77).
- Потребление RAM снижено на **~80 МБ** (v2.1.81).

#### Кейсы использования

**Кейс: Claude Code как most-used AI coding tool (опрос The Pragmatic Engineer, март 2026)**
- **Проблема:** Инженерам нужен был инструмент, который не просто автодополняет, а выполняет задачи end-to-end — рефакторинг, миграции, полные фичи.
- **Решение:** По данным [опроса The Pragmatic Engineer](https://dev.to/alexmercedcoder/ai-weekly-claude-code-dominates-mcp-goes-mainstream-week-of-march-5-2026-15af) (~1000 инженеров), Claude Code стал самым используемым AI coding tool, обогнав GitHub Copilot и Cursor за 8 месяцев. 75% инженеров в небольших компаниях используют его как основной инструмент.
- **Результат:** 55% инженеров регулярно используют AI-агентов (а не просто автокомплит). Среднее — 2–4 инструмента одновременно.

#### Оценка: Да — тестировать на этой неделе

`--bare` — критически важен для CI/CD интеграций. Исправления безопасности хуков обязательны к обновлению. `--channels` стоит попробовать если используете MCP.

---

### 🟢 Приоритет 1: Codex (OpenAI)

**2 релиза CLI: v0.115.0 (16 марта) и v0.116.0 (19 марта). Codex App v26.312.**

#### Новые фичи

**1. Хук `userpromptsubmit` (CLI v0.116.0)**

- **Что это:** Хук, который срабатывает после того, как пользователь отправил промпт, но до того, как агент начнёт его выполнять. Хук может заблокировать промпт, модифицировать его или добавить контекст. Промпт не попадает в историю, пока хук не одобрит его.
- **Зачем нужен:** Enterprise-безопасность: можно фильтровать промпты на наличие секретов, PII, или запрещённых действий до выполнения. Автоматизация: можно дополнять промпт контекстом из внешних систем (Jira-тикет, последний коммит).
- **Пример использования:**
  ```python
  # Hook script: augment_prompt.py
  import sys, json
  
  data = json.load(sys.stdin)
  prompt = data["prompt"]
  
  # Блокировка если содержит секреты
  if "API_KEY" in prompt or "password" in prompt:
      print(json.dumps({"action": "block", "reason": "Prompt contains secrets"}))
  else:
      # Добавить контекст из текущей ветки
      import subprocess
      branch = subprocess.check_output(["git", "branch", "--show-current"]).strip()
      augmented = f"[Branch: {branch}] {prompt}"
      print(json.dumps({"action": "allow", "prompt": augmented}))
  ```

**2. Device-code ChatGPT sign-in (CLI v0.116.0)**

- **Что это:** Новый метод авторизации через ChatGPT: CLI генерирует device-code, пользователь авторизуется через браузер на ChatGPT. Также поддержка обновления существующих токенов ChatGPT.
- **Зачем нужен:** На headless-серверах и в WSL нет возможности открыть браузер для OAuth-потока. Device-code позволяет авторизоваться с любого устройства, введя код.

**3. Full-resolution image inspection (CLI v0.115.0)**

- **Что это:** Модели могут запрашивать полноразмерное изображение через `view_image` и `codex.emitImage(..., detail: "original")` вместо downsized версии.
- **Зачем нужен:** Для точных визуальных задач — проверка пикселей в UI-скриншотах, анализ диаграмм, работа с дизайн-макетами, где сжатие теряет детали.

**4. Python SDK для filesystem RPCs (CLI v0.115.0)**

- **Что это:** Python SDK получил прямой доступ к файловой системе Codex через RPC-вызовы. Можно читать, писать, перемещать файлы программно из Python-скриптов.
- **Зачем нужен:** Скрипты автоматизации (тесты, деплой, обработка данных) могут напрямую взаимодействовать с файловой системой Codex без костылей через shell-команды.

**5. Smart Approvals — guardian subagent (CLI v0.115.0)**

- **Что это:** Система маршрутизации через sub-агента-«стража», который решает, нужно ли одобрение пользователя для конкретного действия. Автоматически одобряет безопасные операции, запрашивает подтверждение для рискованных.
- **Зачем нужен:** Баланс между скоростью (не спрашивать одобрение на `cat file.txt`) и безопасностью (спрашивать перед `rm -rf` или деплоем). Guardian-агент анализирует контекст и риск каждого действия.

**6. Codex App v26.312 — обновлённые Automations**

- **Что это:** Полностью переработанные Automations в десктопном приложении Codex. Теперь можно настраивать: local vs. worktree execution, кастомную модель и уровень reasoning на каждую автоматизацию.
- **Зачем нужен:** Разные задачи требуют разных моделей: быстрый lint — дешёвая модель без reasoning, сложный рефакторинг — мощная модель с deep reasoning. Теперь это настраивается per-automation.

**7. `--channels` для realtime websocket (CLI v0.115.0)**

- **Что это:** Поддержка websocket-каналов для realtime-коммуникации между CLI и серверами. Аналогично Claude Code `--channels`.
- **Зачем нужен:** Стриминг обновлений от внешних систем прямо в сессию Codex — CI-статусы, результаты тестов, уведомления.

#### Кейсы использования

**Кейс: WorkOS — 85–90% success rate на maintenance-задачах (Zack Proser, Applied AI team)**
- **Проблема:** Команда Applied AI в WorkOS поддерживает несколько full-stack JavaScript-приложений (Cloudflare, Vercel). Ежедневные maintenance-задачи (фиксы TypeScript-ошибок, обновление API-схем, миграции middleware) съедали 30–40% утреннего времени.
- **Решение:** Инженер параллельно ставит 4–5 задач в Codex утром до начала deep work: «Fix TypeScript error in onboarding flow», «Update webhooks endpoint for new event schema», «Add error boundaries to admin dashboard», «Migrate legacy auth middleware». Codex работает параллельно во время кофе.
- **Результат:** Success rate вырос с 40–60% до **85–90%** для well-scoped maintenance-задач. Двухуровневый подход: Codex для рутины, Claude Code/Cursor для архитектурных задач. Источник: [Zack Proser — Codex Review 2026](https://zackproser.com/blog/openai-codex-review-2026).

#### Оценка: Да — тестировать на этой неделе

`userpromptsubmit` — ключевая фича для команд, которые хотят автоматизировать и контролировать промпты. Smart Approvals меняет баланс «скорость vs. безопасность». Стоит обновиться до 0.116.0.

---

### 🟡 Приоритет 2: Google (Stitch / AI Studio / Jules / Gemini CLI)

#### Google Stitch — перезапуск как «vibe design» (18 марта 2026)

- **Что это:** Радикальное обновление Stitch — из простого генератора макетов в полноценную AI-платформу дизайна с бесконечным канвасом. Ключевые возможности:
  - **Одновременная генерация 5 экранов** — можно описать весь flow приложения, и Stitch сгенерирует набор экранов с единым дизайном.
  - **Голосовые команды** — описание изменений голосом прямо в канвасе.
  - **DESIGN.md** — агент-friendly markdown-файл для экспорта/импорта дизайн-системы между проектами и инструментами.
  - **MCP-сервер + SDK** — Stitch как MCP-сервер для интеграции в агентные пайплайны (2.4K stars на GitHub).
  - **Экспорт:** AI Studio, Antigravity, Figma (с Auto Layout), React-компоненты, HTML/Tailwind CSS.
- **Бесплатный тариф:** 350 генераций/месяц.
- **Для инженеров:** URL-based design extraction — вставляешь URL, Stitch анализирует дизайн-систему (цвета, типографика, spacing, стиль компонентов) и создаёт макеты в том же стиле.
- Источник: [Google Blog — Introducing «vibe design» with Stitch](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/)

#### Gemini CLI v0.34.0 (17 марта 2026)

- **Plan Mode включён по умолчанию** — CLI теперь по умолчанию разбивает сложные задачи на шаги и выполняет их последовательно. Ранее нужно было активировать вручную.
- **gVisor (runsc) sandboxing** — нативная поддержка gVisor для изоляции выполнения команд. Это production-grade песочница от Google (используется в GKE). Экспериментальная поддержка LXC-контейнеров.
- **A2A (agent-to-agent) timeout увеличен до 30 минут** — для длительных задач между агентами.
- Источник: [Gemini CLI Changelogs](https://geminicli.com/docs/changelogs/)

#### Jules — обновления марта

- **CI Fixer** — автоматическое исправление упавших CI-тестов.
- **Planning Critic** — sub-агент, который ревьюит план выполнения перед стартом.
- **Gemini 3.1 Pro** стал моделью по умолчанию.
- **Важно:** С 25 марта бесплатный тариф Gemini ограничен Flash-моделями; Pro-модели только по подписке.

#### Оценка: Возможно позже

Stitch интересен для прототипирования UI — стоит попробовать если есть задачи по дизайну. MCP-сервер Stitch может быть полезен в агентных пайплайнах. Gemini CLI gVisor — хороший шаг для безопасности, но если уже используете Claude Code/Codex — не срочно.

---

### ⚪ Приоритет 3: xAI (Grok — инструменты для кода и агентов)

#### Grok 4.20 — выход из беты (март 2026)

- **2M контекстное окно**, скорость вывода **~230 tok/sec**, цена API: **$2 input / $6 output за 1M токенов**.
- **Мультиагентная система** через параметр API `agent_count`: 4 специализированных агента (координатор + исследователь + логик + креативный), режим «Heavy» — до 16 агентов для глубоких задач.
- Источник: [xAI Release Notes](https://docs.x.ai/developers/release-notes)

#### `enable_grok_computer` — computer-use на подходе

- Флаг обнаружен в коде (22 марта). Musk подтвердил «coming soon» — Grok получит возможность управлять компьютером (по аналогии с Claude computer use). Деталей реализации пока нет.

#### grok-cli v1.0.0-rc3

- Sub-агенты, MCP-поддержка, headless JSON-режим, удалённое управление через Telegram.
- Источник: [GitHub — superagent-ai/grok-cli](https://github.com/superagent-ai/grok-cli/releases)

#### grok-code-fast-1 в GitHub Copilot Free

- Модель доступна через auto model selection в Copilot Free на VS Code, JetBrains, Xcode, Eclipse.
- Источник: [GitHub Blog — Grok Code Fast 1 in Copilot Free](https://github.blog/changelog/2026-03-04-grok-code-fast-1-is-now-available-in-copilot-free-auto-model-selection/)

#### Оценка: Нет — наблюдать

Мультиагентная система Grok 4.20 интересна концептуально, но экосистема инструментов пока незрелая. `enable_grok_computer` стоит отслеживать — если реализация будет на уровне Claude computer use, это станет значимым.

---

## Таблица сравнения

| Инструмент | Новые фичи | Новые кейсы | Влияние | Тесты на этой неделе |
|---|---|---|---|---|
| **Claude Code** | `--bare` для CI/CD, `--channels` (MCP push), `StopFailure` hook, frontmatter ограничения агентов, Opus 4.6 64K/128K токенов, исправления безопасности хуков и песочницы | #1 AI coding tool по опросу (75% в малых компаниях) | **Высокое** | **Да** |
| **Codex CLI** | `userpromptsubmit` хук, device-code auth, Smart Approvals guardian, full-res image inspection, Python SDK filesystem, обновлённые Automations | WorkOS: 85–90% success rate, 4–5 параллельных задач утром | **Высокое** | **Да** |
| **Google Stitch / Gemini CLI / Jules** | Stitch «vibe design» перезапуск (MCP, DESIGN.md, 5 экранов, голос), Gemini CLI Plan Mode + gVisor, Jules CI Fixer + Planning Critic | — | **Среднее** | **Нет** |
| **xAI (Grok)** | Grok 4.20 GA (2M ctx, мультиагент), `enable_grok_computer` обнаружен, grok-cli rc3, grok-code-fast-1 в Copilot Free | — | **Низкое** | **Нет** |

---

## Рекомендации на неделю

1. **Обновить Claude Code до v2.1.81 и проверить `--bare` в CI/CD.** Если используете Claude Code в GitHub Actions или любых пайплайнах — `--bare` убирает overhead и предотвращает ошибки от IDE-зависимостей. Заодно проверьте, что песочница не была тихо отключена (исправление из v2.1.78).

2. **Обновить Codex CLI до v0.116.0 и настроить `userpromptsubmit` хук.** Даже простой вариант — логирование всех промптов или фильтр секретов — значительно повышает безопасность и traceability. Для команд — обязательно.

3. **Попробовать Google Stitch MCP-сервер для прототипирования UI.** Если в проекте есть задачи по дизайну интерфейсов — Stitch с DESIGN.md и экспортом в React может сэкономить дни работы. Бесплатные 350 генераций достаточно для полноценного теста.

---

## Источники

- [Claude Code Changelog](https://code.claude.com/docs/en/changelog) — официальные release notes v2.1.77–2.1.81
- [Claude Code GitHub Releases](https://github.com/anthropics/claude-code/releases) — исходный код и бинарные релизы
- [Codex CLI Changelog](https://developers.openai.com/codex/changelog/) — официальные release notes v0.115.0–0.116.0
- [Zack Proser — OpenAI Codex Review 2026](https://zackproser.com/blog/openai-codex-review-2026) — кейс WorkOS, daily use
- [Kingy AI — The Codex App Super Guide](https://kingy.ai/ai/the-codex-app-super-guide-2026-from-hello-world-to-worktrees-skills-mcp-ci-and-enterprise-governance/) — обзор Codex App и Automations
- [Google Blog — Introducing «vibe design» with Stitch](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/) — анонс перезапуска Stitch
- [NxCode — Google Stitch Tutorial](https://www.nxcode.io/resources/news/google-stitch-tutorial-design-first-app-2026) — практический гайд по Stitch
- [MindStudio — How to Use Google Stitch](https://www.mindstudio.ai/blog/how-to-use-google-stitch-website-design-system) — обзор экспорта в React и AI Studio
- [Gemini CLI Changelogs](https://geminicli.com/docs/changelogs/) — release notes v0.34.0
- [xAI Release Notes](https://docs.x.ai/developers/release-notes) — Grok 4.20 GA
- [GitHub Blog — Grok Code Fast 1 in Copilot Free](https://github.blog/changelog/2026-03-04-grok-code-fast-1-is-now-available-in-copilot-free-auto-model-selection/)
- [superagent-ai/grok-cli Releases](https://github.com/superagent-ai/grok-cli/releases) — grok-cli v1.0.0-rc3
- [DEV Community — AI Weekly: Claude Code Dominates](https://dev.to/alexmercedcoder/ai-weekly-claude-code-dominates-mcp-goes-mainstream-week-of-march-5-2026-15af) — опрос The Pragmatic Engineer
- [Releasebot — Claude Release Notes](https://releasebot.io/updates/anthropic/claude) — Cowork persistent thread (17 марта)
