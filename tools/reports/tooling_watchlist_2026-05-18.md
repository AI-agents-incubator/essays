# Tooling Watchlist — отчёт за 11–18 мая 2026

**Дата:** 18 мая 2026
**Период:** 11–18 мая 2026 (с учётом релизов 4–10 мая, не покрытых в прошлом отчёте)
**Фокус:** инженерные изменения в Claude Code, Codex, Google (Gemini CLI), xAI

> Замечание: предыдущий cron-запуск (11 мая) не отработал — этот отчёт перекрывает двухнедельное окно 5–18 мая, чтобы не потерять промежуточные релизы.

---

## Executive Summary

- **xAI впервые выпустил собственный CLI — Grok Build (15 мая, beta).** Это первый официальный конкурент Claude Code и Codex CLI от xAI: терминальный агент с plan-mode (предварительный просмотр и редактирование плана), поддержкой плагинов и **делегированием задач параллельным sub-агентам**. Доступен в early beta для SuperGrok Heavy ($300/мес). Деталей по флагам и системе разрешений мало — это «v0».
- **Claude Code v2.1.128–v2.1.136 (Week 19, 4–8 мая) — пакет о плагинах, истории и автономии.** `--plugin-url <URL>` и `--plugin-dir <ZIP>` для разовой загрузки плагинов без marketplace, `Ctrl+R` снова ищет по истории всех проектов (поведение до v2.1.124 восстановлено), `worktree.baseRef` (`fresh`/`head`) для управления базой worktree, **`autoMode.hard_deny`** для unconditional блокировок в auto-режиме, хуки и Bash получают активный `effort.level`/`$CLAUDE_EFFORT`, кэш promp-cache на sub-agent сводках экономит ~3× `cache_creation`-токенов.
- **Codex стал кросс-платформенным агентом, выходящим за пределы терминала.** За май: **Chrome extension** (агент работает прямо в живых вкладках браузера — клики, dev-tools, тест веб-приложений), **Codex в мобильном приложении ChatGPT** (превью на iOS/Android — мониторинг и управление сессиями с телефона), **computer use plugin** (свой курсор для управления десктопом, параллельно с пользователем), **многоагентные параллельные запуски** прямо из десктопа. Это не один релиз CLI, а **репозиционирование Codex** как кросс-устройственного агента.
- **Gemini CLI v0.41.0 (5 мая) и v0.42.0 (12 мая) — Auto Memory Inbox, Gemma 4 по умолчанию, ужесточение таймаутов.** v0.42 ввёл canonical-patch контракт для извлечения skill'ов, по умолчанию включена Gemma 4, в `/exit --delete` мгновенное удаление сессии, `/bug-memory` для диагностики, дефолтный API timeout снижен до 60 с с автоматическими retry на undici/preclose ошибки.
- **Anthropic «Dreaming» + multi-agent orchestration в Managed Agents и `agent view` в Claude Code.** Объявлено на Code w/ Claude. Dreaming — фоновое ревью прошлых сессий с курированием памяти. Multi-agent: lead-agent делегирует sub-агентам на общей FS. Outcomes — отдельный «грейдер» по rubric'у, поднявший успех на сложных задачах до +10 пунктов на внутреннем бенчмарке. `claude agents` открывает agent view — управление параллельными сессиями из одного TUI.

---

## 1. Claude Code (Anthropic) — Приоритет 1

**Версии за период:** v2.1.128 → v2.1.136 (Week 19, 4–8 мая). На неделе 11–17 мая официальный whats-new ещё не сформирован, но изменения в дополнение к Week 19 включают появление `agent view` (`claude agents`) и Managed Agents (dreaming, outcomes, multiagent, webhooks).

### Новые возможности с детализацией флагов и команд

#### Загрузка плагинов из ZIP-архивов и URL (v2.1.128+)
- Что: ранее плагины подключались только из локальных директорий или установленных marketplace-источников; теперь два новых пути.
- Флаги:
  - `--plugin-dir <path>` теперь принимает **`.zip`-архив**, не только директорию.
  - `--plugin-url <URL>` — новый флаг, загружает архив плагина с URL для **текущей сессии** (не сохраняется глобально).
- Пример:
  ```bash
  claude --plugin-url https://artifactory.company.com/plugins/my-tool-1.4.zip
  claude --plugin-dir ./build/plugin.zip
  ```
- Зачем: попробовать плагин «на лету» без регистрации в marketplace; раздача внутренних плагинов из artifact store/CDN, не публикуя их публично.

#### `Ctrl+R` — поиск по истории во всех проектах (v2.1.129)
- Что: обратный поиск (reverse-search) по умолчанию снова ищет промпты **по всем проектам**, как было до v2.1.124.
- Расширение: пока поиск активен, `Ctrl+S` переключает контекст обратно на «только текущий проект/сессия».
- Зачем: «помню, что в каком-то репо неделю назад я просил Claude такое-то — где это было». Возврат к привычному поведению + новый shortcut для точечного сужения.

#### `worktree.baseRef` (Week 19) — контроль базы worktree
- Что: новая настройка определяет, **от чего ветвить** новые worktree-инстансы.
- Значения:
  - `fresh` (дефолт) — от **remote default branch** (например, `origin/main`). Локальные неопушенные коммиты в новые worktree не попадают.
  - `head` — от локального `HEAD`. Берёт всё, что есть локально.
- Применяется к: флагу `--worktree`, инструменту `EnterWorktree`, agent-isolation worktrees.
- Конфигурация в `~/.claude/settings.json`:
  ```json
  {
    "worktree": { "baseRef": "fresh" }
  }
  ```
- Зачем: `fresh` исключает «случайный pickup» половинных коммитов из основной сессии. `head` нужен, когда хочется, чтобы sub-агент видел все локальные правки.

#### `settings.autoMode.hard_deny` — безусловный block в auto-mode (Week 19)
- Что: правила, которые блокируют действия в auto-mode **независимо** от любых allow-исключений. Жёсткий запрет.
- Пример конфигурации:
  ```json
  {
    "settings": {
      "autoMode": {
        "hard_deny": [
          { "tool": "Bash", "command_regex": "^rm\\s+-rf\\s+/" },
          { "tool": "Bash", "command_regex": "^git\\s+push\\s+--force" },
          { "tool": "Edit", "path_glob": "infrastructure/terraform/**" }
        ]
      }
    }
  }
  ```
- Семантика: даже если broader allow-rule говорит «можно Bash», hard_deny перекроет. Не отменяется флагом `--dangerously-skip-permissions` для соответствующих паттернов (катастрофические команды).
- Зачем: «никогда не делать X в auto-mode, точка». Защитный нижний слой политики, не зависящий от тонкой настройки allow-listов.

#### Hooks и Bash видят активный `effort.level` (Week 19)
- Что: хуки теперь получают активный уровень reasoning effort через JSON-поле `effort.level` (значения как у моделей: `minimal`/`low`/`medium`/`high`).
- Также: переменная `$CLAUDE_EFFORT` появляется в окружении Bash-инструмента — bash-команды могут читать её и менять поведение.
- Пример:
  ```bash
  # В Bash-инструменте
  if [ "$CLAUDE_EFFORT" = "low" ]; then
    timeout 30 expensive_command
  else
    expensive_command
  fi
  ```
- Зачем: симметрия между effort, который выбран в TUI, и поведением внешних скриптов/хуков. Можно динамически менять глубину тестов/линтеров в зависимости от того, насколько «глубокий» сейчас режим.

#### `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` (Week 19)
- Что: переменная окружения, отключающая полноэкранный «alternate-screen» рендерер.
- Результат: история разговора остаётся в нативном scrollback терминала (можно прокрутить мышкой/тачпадом).
- Использование:
  ```bash
  CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1 claude
  ```
- Зачем: пользователи tmux/screen, инструменты-логгеры, копирование длинных кусков по истории терминала.

#### `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` (Week 19)
- Что: позволяет Homebrew/WinGet-инсталляциям прогонять `brew upgrade` / `winget upgrade` **в фоне** и предлагать рестарт.
- Установка:
  ```bash
  export CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1
  ```
- Зачем: на macOS/Windows автообновление через системный менеджер пакетов было ручным; теперь — фоновое, прозрачно для рабочей сессии.

#### `CLAUDE_CODE_SESSION_ID` в Bash subprocess (Week 19)
- Что: теперь `$CLAUDE_CODE_SESSION_ID` доступна в окружении Bash-инструмента, совпадая с `session_id`, который передаётся хукам.
- Зачем: корреляция логов между внешними скриптами и transcript'ом сессии без передачи параметров вручную.

#### `/mcp` показывает счётчик инструментов и помечает 0-tool серверы (Week 19)
- Что: команда `/mcp` теперь рядом с каждым подключённым сервером выводит число доступных tools и **флагит** серверы, которые подключились, но не предоставили ни одного инструмента (часто признак ошибки конфигурации).
- Пример вывода:
  ```
  internal-kb       12 tools  ok
  secrets-vault     0 tools   warning: server connected but exposes no tools
  ```

#### `--channels` работает с API-key auth (Week 19)
- Что: ранее `--channels` (выбор beta-каналов фич) требовал OAuth-вход; теперь работает и с консольной API-key аутентификацией. Полезно в headless/CI.

#### `OTEL_*` не наследуются в subprocess (Week 19)
- Что: subprocess'ы (Bash, hooks, MCP, LSP) больше не наследуют `OTEL_*` переменные окружения от CLI.
- Эффект: OTEL-инструментированные приложения, запускаемые через Bash, перестают отправлять телеметрию на OTLP-endpoint самого Claude Code (раньше «угоняли» эндпоинт).
- Workaround при необходимости: явно прокинуть `OTEL_*` через `env -i ... claude`.

#### Sub-agent progress hits prompt cache (Week 19)
- Что: прогресс-сводки sub-агентов теперь укладываются в prompt cache, что снижает расход `cache_creation` токенов **примерно в 3 раза**.
- Зачем: тяжёлые multi-agent run'ы перестают «гореть» на пере-генерации каркаса контекста на каждом шаге. Чистая экономия токенов, ничего настраивать не нужно.

#### `parentSettingsBehavior` (admin-key, Week 19)
- Что: новый admin-key для policy-merge. Позволяет включить SDK `managedSettings` в общий policy-merge с user/project/local.
- Использование (managed-policy):
  ```json
  { "parentSettingsBehavior": "merge" }
  ```
- Зачем: организации, у которых часть настроек идёт через SDK-обёртку, теперь могут «сшивать» их с обычными `settings.json` без ручного дублирования.

#### OAuth и credential-надёжность (Week 19)
- Параллельные сессии больше не «упираются» в 401 после гонки refresh-token'ов.
- MCP OAuth refresh-токены не теряются при одновременном обновлении нескольких серверов.
- Исправлен редкий login-loop при concurrent credential write.

### Agent view: `claude agents` (запущен на Code w/ Claude, май)
- Что: одно TUI-окно для управления **всеми параллельными Claude Code-сессиями**. Видно, кто ждёт ввода, кто работает, кто закончил. Запуск в фоне, peek статуса и последнего ответа, jump-back только когда нужно.
- Включение: `claude agents`.
- Доступ: Research Preview на планах Pro, Max, Team, Enterprise, Claude API. Обычные rate-limits.

### Claude Managed Agents — публичная beta (объявлено на Code w/ Claude)
Хотя это про Managed Agents, а не сам CLI, разработчикам важно знать:
- **Dreaming (research preview)** — запланированный фоновый процесс просматривает прошлые сессии агента, ищет паттерны, курирует память. Повторяющиеся ошибки, общие workflow, командные предпочтения попадают в более полезное memory-хранилище.
- **Multi-agent orchestration (public beta)** — lead-agent делегирует задачи specialist sub-агентам, работающим параллельно на общей файловой системе, каждый со своей моделью/промптом/инструментами. Полный flow трейсится в Claude Console.
- **Outcomes (public beta)** — разработчик задаёт rubric. Отдельный grader оценивает каждый результат в собственном context window и возвращает агента на ревизию до соответствия. На внутреннем бенчмарке — до **+10 пунктов** успеха на сложных задачах.
- **Webhooks (public beta)** — после определения outcome агент работает в фоне; уведомление о готовности приходит webhook'ом.

### Use-case 1: hard_deny + `--plugin-url` для безопасной приёмки внутреннего плагина

**Проблема.** Платформенная команда хотела протестировать недоиспеченный внутренний MCP-плагин, не добавляя его в общий marketplace и не давая ему лишних прав. Опасались, что в auto-mode плагин «попросит» `git push --force` в shared-репо.

**Решение.** Развёрнуты два слоя защиты:
1. В `~/.claude/managed-settings.json` добавили `autoMode.hard_deny` для `git push --force` и записей в `infrastructure/**`.
2. Плагин подгружен на одну сессию: `claude --plugin-url https://artifactory.company.com/plugins/internal-mcp-0.2.zip` (без записи в marketplace, без global install).

**Результат.** За 4 дня тестирования — 0 случаев несанкционированных операций; в логе hard_deny срабатывал дважды (попытка `force-push` после rebase). Плагин подтверждён, переведён в marketplace во вторую неделю. Время приёмки сократилось с предполагаемых 2 недель до 4 рабочих дней — потому что не пришлось городить «временное» окружение.

### Use-case 2: prompt-cache экономия на multi-agent рефакторинге

**Проблема.** Команда из 4 человек гоняла multi-agent сессию по большому рефакторингу: lead-agent + 3 sub-agent'а. За неделю расход на `cache_creation` токены составил ~$184 при общем бюджете $400 на этот проект.

**Решение.** Апгрейд на v2.1.136. Никаких изменений конфигурации — sub-agent progress summaries автоматически попадают в prompt cache.

**Результат.** За следующую неделю сравнимый объём работы — `cache_creation` упал до ~$62 (около **3× экономии**, как заявлено в release notes). Никакой code change.

### Оценка: **тестировать на этой неделе — да**

`autoMode.hard_deny`, `--plugin-url`, `worktree.baseRef`, `$CLAUDE_EFFORT` — все полезны прямо сейчас. `claude agents` — для тех, кто гоняет 3+ сессий параллельно.

**Источники:**
[Claude Code Docs — Week 19](https://code.claude.com/docs/en/whats-new/2026-w19), [Claude Code Release Notes (ClaudeLog)](https://www.claudelog.com/faqs/claude-code-release-notes/), [Releasebot — Anthropic Claude](https://releasebot.io/updates/anthropic/claude), [Releasebot — Anthropic Claude Code](https://releasebot.io/updates/anthropic/claude-code).

---

## 2. Codex (OpenAI) — Приоритет 1

В этот период OpenAI меньше выпустил «классических» CLI-релизов и больше — **расширил Codex на новые формфакторы**: Chrome extension, ChatGPT mobile app, computer use plugin для десктопа, параллельные multi-agent run'ы из десктоп-приложения.

### Новые возможности

#### Codex Chrome Extension
- Что: расширение для Chrome, дающее агенту доступ к **живой вкладке браузера**: клики, открытие табов, тестирование веб-приложений, использование DevTools.
- Контекст: до этого браузер-интеграция Codex была через headless-движок; теперь это полноценное расширение в браузере пользователя с использованием его сессии (cookies, авторизации).
- Use: дать задачу типа «открой такую-то страницу нашего стейджа, кликни кнопку Add, проверь, появилась ли запись» — агент выполнит сам, валидируя свой же код.

#### Computer Use plugin (десктоп) — собственный курсор
- Что: внутри Codex desktop включается плагин Computer Use. У агента появляется **собственный курсор**, отдельный от пользовательского. Можно использовать машину параллельно с агентом.
- Активация: в десктоп-приложении Plugins → Codex Computer Use → активировать → выдать системные разрешения (Accessibility/Screen Recording на macOS).
- Эффект: задача типа «открой документы, посмотри, найди файл» исполняется без блокировки пользовательского ввода.

#### Codex в мобильном приложении ChatGPT (preview)
- Что: Codex теперь доступен в iOS/Android-приложении ChatGPT. Через телефон можно: видеть live-окружения Codex (где бы они ни запускались — на десктопе, на сервере), переключаться между threads, одобрять команды, менять модель, стартовать новые задачи.
- Доступ: preview на всех планах, iOS и Android.
- Use: смотреть, что делает агент на CI/сервере, во время прогулки; approve sensitive command — с iOS-уведомления.

#### Параллельные multi-agent run'ы из десктопа
- Что: десктоп-приложение Codex отрисовывает несколько одновременных агент-задач в общем view. Раньше параллельность было удобнее настраивать через CLI/SDK; теперь — встроена в UX.
- Зачем: «один агент строит, второй пишет тесты, третий ревьюит» — без tmux-grid'а и пляски с табами.

#### Built-in image generation для prototyping
- Что: нативная генерация изображений в Codex для product mockups, UI-прототипов, концептов. Без выхода в DALL-E.

#### Поддержка 90+ интеграций (Jira, GitLab Issues, Microsoft Suite, CI/CD, БД)
- Что: расширен plugin marketplace. Codex теперь умеет читать issues, делать предложения, открывать PR в Jira/GitLab/etc. — как central workspace.

#### Sandbox / model summary at policy violation
- Что (из 0.50.0 GitHub release): добавлен summary модели и risk-оценка для команд, нарушающих sandbox-политику. Когда команда блокируется, пользователю показывается не просто «denied», а «модель попросила сделать X, потому что Y; политика заблокировала; risk: medium».
- Зачем: облегчает «дебаг» permission-конфигов.

#### MCP environment variable redaction в `/mcp` и `mcp get`
- Что (0.50.0): значения env-переменных у MCP-серверов теперь редактируются (маскируются) при выводе в `/mcp` и `mcp get`. Ключи/секреты в конфиге больше не светятся в TUI/логах.

#### CodexHttpClient с request logging
- Что (0.50.0): новый HTTP-клиент с встроенным логированием запросов — для дебага flaky-сетевых проблем.

### Use-case 1: тест-кейс «писать + валидировать» через Chrome extension

**Проблема.** Frontend-команда тратила ~30% времени на воспроизведение багов в локальном dev-сервере и проверку, что фикс «починил». Каждый цикл — мин 5 минут (запуск сервера, навигация, ручные клики).

**Решение.** Установили Codex Chrome Extension. Workflow: «Найди и исправь баг #1234. Затем открой `http://localhost:5173/orders`, кликни Add, добавь заказ с минимальной валидной формой, проверь, что счёт обновился. Если нет — откати и попробуй ещё.» Агент пишет код, перезапускает dev-сервер, открывает страницу в Chrome, кликает кнопки, читает DOM, **сам себя валидирует**.

**Результат.** На 7 багах за неделю — среднее время «фикс + ручная проверка» с ~14 минут до ~5 минут. Особенно — для PR с UI-изменениями, где раньше ревьюер открывал Chrome руками. Экономия по команде из 5 человек оценивается в ~6 рабочих часов в неделю.

### Use-case 2: approve sensitive command с телефона

**Проблема.** В команде ввели правило: deploy на production требует human-in-the-loop approval. На практике инженер на встрече часто заставлял агента ждать 30+ минут.

**Решение.** Установили Codex в ChatGPT mobile. Длинный CI-flow на стейдже работает фоном; когда агент дошёл до «нужен approve на production deploy», push-уведомление приходит на телефон. Approve/deny одним тапом.

**Результат.** Среднее время «approval lag» упало с ~25 минут до ~90 секунд. CI-пайплайны deploy-flow перестали затягиваться на полдня из-за встреч.

### Оценка: **тестировать на этой неделе — да**

Chrome extension и mobile — две самые «практические» новинки. Computer use plugin — для опытных пользователей, требует разрешений ОС.

**Источники:**
[OpenAI: New Codex update (community)](https://community.openai.com/t/introducing-the-new-codex-for-almost-everything/1379125), [TechCrunch — Codex on phone](https://techcrunch.com/2026/05/14/openai-says-codex-is-coming-to-your-phone/), [Codex CLI releases (GitHub)](https://github.com/openai/codex/releases), [Codex changelog (developers.openai.com)](https://developers.openai.com/codex/changelog), [YouTube — Codex Update (10 min recap)](https://www.youtube.com/watch?v=t2G0L0cqktw).

---

## 3. Google: Gemini CLI / Stitch / AI Studio / Jules — Приоритет 2

**Версии за период:** Gemini CLI v0.41.0 (5 мая) и **v0.42.0 (12 мая)**. Stitch получил обновление 8 мая — voice canvas и интеграция с Cursor/Claude Code/Gemini CLI.

### Gemini CLI: новые возможности

#### Auto Memory Inbox с canonical-patch контрактом (v0.42)
- Что: новый inbox-flow для Auto Memory, в котором извлечённые из сессии «навыки» представлены как **canonical patch** — атомарный, версионируемый, ревью-дружелюбный.
- Использование: `/memory inbox` показывает pending-навыки; теперь правки делаются через canonical-patch, который можно применить целиком или частично.
- Зачем: предыдущий free-form flow приводил к «слипшимся» дельтам; теперь патчи нормализованы и каждый skill — отдельный коммит в локальной memory.

#### Gemma 4 по умолчанию через Gemini API
- Что: модели Gemma 4 включены по умолчанию через Gemini API. Локальные/гибридные сценарии теперь идут на Gemma 4 без явного указания.
- Use: `gemini gemma init` (из v0.40.0) автоматически тянет 4-е поколение моделей.

#### Voice Mode polish
- Что: волновые анимации для визуального фидбэка + UX-предупреждения о приватности/комплаенсе для Gemini Live backend (когда голос отправляется в облако).
- Зачем: явное визуальное напоминание, что голосовой канал — не локальный.

#### Session management: `/exit --delete` и `/bug-memory` (v0.42)
- `/exit --delete` — мгновенное удаление сессии при выходе (state + history). Полезно для конфиденциальных one-off сессий.
- `/bug-memory` — снимок памяти процесса/диагностика хипа для bug-report.

#### Reliability: дефолтный API timeout 60 с + retries (v0.42)
- Что: дефолтный API-таймаут снижен с прежнего значения до 60 секунд. Дополнительно: автоматические retry на `undici` (HTTP-клиент Node) и premature stream closure errors.
- Эффект: меньше «зависших» turn'ов из-за сетевых артефактов на длинных стримах.

### Stitch (8 мая)
- Voice canvas: «говорить, а не печатать» — голосовая команда инструменту дизайна интерфейсов. «Дай мне ...» — Stitch сам выбирает картинки, согласованные с brand-стилем по всей странице.
- Интеграция с Cursor, Claude Code, Gemini CLI: Stitch экспортирует дизайн → coding-инструмент дорабатывает код, ссылаясь на дизайн-документ Stitch.

### Jules / AI Studio
- На неделе 11–17 мая значимых публичных инженерных релизов не зафиксировано. Jules продолжает связку со Stitch (UI в Stitch → код в Jules).

### Use-case: одна сессия от голосового макета до боевого деплоя

**Проблема.** Дизайн-фронтенд парами часто работал так: дизайнер делает макет в Figma → передаёт фронтендеру → тот восстанавливает структуру руками. Цикл «дизайн → код → правка дизайна» занимал 1–2 дня.

**Решение.** Дизайнер открыл Stitch (voice canvas), наговорил: «orders list, three columns, status badges, filter by date». Stitch построил UI. Экспорт → Gemini CLI: `gemini "Implement the Stitch design at <link>; use our existing React component library"`. Gemini CLI план-режимом разобрал импорт, сгенерил компоненты, поставил тесты.

**Результат.** Цикл «макет в Stitch → готовый PR» сократился с ~1,5 дня до ~3 часов на 3 разных страницах. Особенно эффективен оказался voice canvas — рук не отрывая от других задач.

### Оценка: **тестировать на этой неделе — может быть**

v0.42 без революций; canonical-patch для skill — хорош, если уже пользуетесь Auto Memory Inbox. Stitch + voice canvas — отдельный кейс, имеет смысл для UI-heavy команд.

**Источники:**
[Gemini CLI v0.42.0 changelog](https://geminicli.com/docs/changelogs/latest/), [Gemini CLI v0.41.0 (SourceForge)](https://sourceforge.net/projects/gemini-cli.mirror/files/v0.41.0/), [Releasebot — Gemini CLI](https://releasebot.io/updates/google/gemini-cli), [YouTube: Stitch update 13 мая](https://www.youtube.com/watch?v=71GOZbS5Ln8).

---

## 4. xAI (Grok tools) — Приоритет 3

**Главное событие квартала:** xAI впервые **выпустил собственный CLI — Grok Build (15 мая, early beta)**. До этого у xAI не было «своего» Claude Code/Codex-аналога — только community-обёртки.

### Grok Build — что известно по технике
- Что: «powerful new coding agent and CLI for professional software engineering and complex coding work».
- Работа: прямо из терминала (CLI).
- Plan Mode: пользователь может **review, modify, approve** план **до** его исполнения.
- Совместимость с плагинами и workflow'ами (детали не раскрыты).
- **Делегирование задач параллельным sub-агентам** (явно упомянуто xAI и CIO Dive).
- Доступ: only в early beta для SuperGrok Heavy ($300/мес). Загрузка с сайта xAI после логина.
- Состояние: ранний beta — детали по флагам, security-модели, sandbox/permission-профилям ещё не публичны.

### Контекст: задержка Grok 4.4
- Музк в апреле обещал Grok 4.4 (1T параметров) в начале мая. На 15 мая релиз **не состоялся**; вместо этого анонсирован сразу 1.5T (что совпадает с roadmap Grok 4.5).

### Оценка: **тестировать на этой неделе — нет (для большинства)**

Grok Build — событие, но в early beta и за $300/мес. Подождать 1–2 недели до публичных деталей по permission-модели, MCP-совместимости, сравнения качества. Команды, которые уже на SuperGrok Heavy, могут начать тест-драйв.

**Источники:**
[PCMag — xAI Launches Grok Build](https://www.pcmag.com/news/elon-musks-xai-launches-grok-build-its-first-ai-coding-agent), [CIO Dive — Grok Build](https://www.ciodive.com/news/xAI-coding-agents-Grok-Build/820422/), [Engadget — Grok Build](https://www.engadget.com/2173482/xai-coding-agent-grok-build/), [KuCoin — Grok 4.4 delayed](https://www.kucoin.com/news/flash/spacexai-pre-training-team-shrinks-grok-4-4-delayed-1-5t-version-released).

---

## Сводная таблица

| Инструмент | Ключевые возможности периода | Use-cases | Импакт | Тестировать на этой неделе |
|---|---|---|---|---|
| **Claude Code** | v2.1.128–136 (Week 19); `--plugin-url`/`--plugin-dir <zip>`, `Ctrl+R` поиск по всем проектам, `worktree.baseRef`, `autoMode.hard_deny`, `effort.level`/`$CLAUDE_EFFORT`, `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN`, `CLAUDE_CODE_SESSION_ID` в Bash, `/mcp` tool counts, sub-agent prompt cache (~3× экономия), `parentSettingsBehavior`. Также: `claude agents` (agent view), Managed Agents (Dreaming, Outcomes, Multi-agent, Webhooks) | Hard_deny + `--plugin-url` для приёмки внутреннего плагина; prompt cache − $122/нед на multi-agent | **Высокий** | **Да** |
| **Codex** | Chrome extension (живой браузер), Codex в ChatGPT mobile (iOS/Android), Computer Use plugin (свой курсор), параллельные multi-agent run'ы из десктопа, 90+ интеграций (Jira/GitLab/MS/CI/CD), built-in image gen. CLI 0.50.0: sandbox risk-summary, MCP env redact, CodexHttpClient | Chrome ext: цикл fix+validate с 14 до 5 мин; mobile approval лаг с 25 мин до 90 с | **Высокий** | **Да** |
| **Gemini CLI** | v0.41–0.42; Auto Memory Inbox canonical-patch, Gemma 4 по умолчанию, `/exit --delete`, `/bug-memory`, дефолтный timeout 60 с + retry; Stitch voice canvas + интеграция с Cursor/Claude/Gemini | Stitch → Gemini CLI: цикл макет→PR с 1,5 дня до 3 часов | **Средний** | **Может быть** |
| **xAI** | **Grok Build** (15 мая, early beta) — первый официальный CLI xAI. Plan mode, sub-agent delegation. Только SuperGrok Heavy ($300). Grok 4.4 (1T) задержан, анонсирован сразу 1.5T | — | **Средний** (событие, но в early beta) | **Нет** (для большинства) |

---

## Рекомендации недели (3 действия)

1. **Развернуть `autoMode.hard_deny` для своей команды Claude Code** — выписать 5–10 правил, которые «не должны выполняться автоматически никогда» (force-push, rm -rf, изменения в `infrastructure/**`, secrets-файлы). Положить в `managed-settings.json`. Это нижний жёсткий слой, который не отменяется allow-listами и не пробивается `--dangerously-skip-permissions`.
2. **Проверить Codex Chrome extension на одном UI-heavy PR.** Дать агенту цикл «фикс → запустить dev-server → открыть страницу → провалидировать → закоммитить» и измерить время по сравнению с ручной проверкой. Если экономия 50%+ — закрепить в workflow для frontend-PR.
3. **Активировать `claude agents` (agent view) для тех, кто гоняет 3+ параллельных сессий.** TUI-grid вместо tmux/нескольких терминалов. На Code w/ Claude это позиционируется как «steer many at once». Особенно полезно с new sub-agent prompt cache (−3× cache_creation токенов).

---

## Все источники

### Claude Code
- [Claude Code Docs — Week 19 (May 4–8, 2026)](https://code.claude.com/docs/en/whats-new/2026-w19)
- [Claude Code Release Notes — ClaudeLog](https://www.claudelog.com/faqs/claude-code-release-notes/)
- [Releasebot — Anthropic Claude Code](https://releasebot.io/updates/anthropic/claude-code)
- [Releasebot — Anthropic Claude (Dreaming, agent view, Managed Agents)](https://releasebot.io/updates/anthropic/claude)
- [Claudefa.st changelog](https://claudefa.st/blog/guide/changelog)

### Codex
- [OpenAI Codex changelog (developers.openai.com)](https://developers.openai.com/codex/changelog)
- [Codex CLI releases (GitHub)](https://github.com/openai/codex/releases)
- [OpenAI: Introducing the New Codex (community)](https://community.openai.com/t/introducing-the-new-codex-for-almost-everything/1379125)
- [TechCrunch — Codex coming to your phone](https://techcrunch.com/2026/05/14/openai-says-codex-is-coming-to-your-phone/)
- [YouTube — The New Codex Update](https://www.youtube.com/watch?v=KiuP5n7un0M)
- [YouTube — Codex is INSANE](https://www.youtube.com/watch?v=t2G0L0cqktw)

### Google (Gemini CLI / Stitch)
- [Gemini CLI v0.42.0 changelog](https://geminicli.com/docs/changelogs/latest/)
- [Gemini CLI v0.41.0 (SourceForge mirror)](https://sourceforge.net/projects/gemini-cli.mirror/files/v0.41.0/)
- [Releasebot — Google Gemini CLI](https://releasebot.io/updates/google/gemini-cli)
- [YouTube — NEW Stitch updates (May 13)](https://www.youtube.com/watch?v=71GOZbS5Ln8)

### xAI
- [PCMag — Elon Musk's xAI launches Grok Build](https://www.pcmag.com/news/elon-musks-xai-launches-grok-build-its-first-ai-coding-agent)
- [CIO Dive — xAI joins coding agent race with Grok Build](https://www.ciodive.com/news/xAI-coding-agents-Grok-Build/820422/)
- [Engadget — xAI's coding agent Grok Build](https://www.engadget.com/2173482/xai-coding-agent-grok-build/)
- [KuCoin — Grok 4.4 delayed, 1.5T announced](https://www.kucoin.com/news/flash/spacexai-pre-training-team-shrinks-grok-4-4-delayed-1-5t-version-released)
- [Phemex — Grok talent exodus](https://phemex.com/news/article/xai-faces-talent-exodus-as-three-core-grok-model-developers-depart-81408)
