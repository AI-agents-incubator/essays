# Tooling Watchlist — отчёт за 25 мая – 1 июня 2026

> **Период:** 25.05.2026 – 01.06.2026 (run #11)
> **Фокус:** технические фичи и инженерные кейсы. Без бизнес-новостей.
> **Аудитория:** инженеры-практики. Приоритеты: автономия агентов и безопасность.

---

## Executive Summary

- **Anthropic запустил Dynamic Workflows (Claude Code v2.1.154)** — JavaScript-скрипт, который пишет сам Claude и который оркестрирует **до 16 параллельных и до 1000 субагентов на один запуск** в изолированном runtime. Триггеры — слово `workflow` в промпте, `/effort ultracode` или встроенный `/deep-research`. Кардинально меняет потолок задач: аудит endpoints, миграции в 500+ файлов, кросс-проверка фактов.
- **Opus 4.8 + новый профиль /effort xhigh в Claude Code v2.1.154** — Opus 4.8 по умолчанию идёт на высоком effort; Fast Mode стал в 3 раза дешевле и доступен на Bedrock/Vertex/Foundry. Auto Mode больше не требует opt-in. Появилось ужесточение классификатора против bulk-эксфильтрации репозитория.
- **`/code-review --fix` в v2.1.152** — ревью теперь не просто отчёт, а автоматическое применение исправлений к рабочему дереву. В паре с новым `disallowed-tools` во frontmatter скиллов получается управляемый «жёсткий» режим ревью.
- **Google убрал Gemini CLI и заменил его на Antigravity CLI/SDK/2.0 на I/O 2026** — отдельное десктоп-приложение для оркестрации множества агентов, headless CLI, SDK для собственной инфраструктуры. Managed Agents API одним вызовом поднимает удалённую Linux-песочницу с инструментами и web-доступом. Старые Gemini CLI конфиги мигрируют.
- **Jules V2 («Project Jitro»)** — асинхронный coding-агент в VM с Gemini 3.1 Pro по умолчанию, цель-ориентированный (`goal-driven`), результат — pull request. Прямой конкурент Claude Code и Codex по форме «отправил задачу — получил PR».
- **xAI Grok Build beta открыли для всех SuperGrok / X Premium Plus** — plan mode с редактируемым планом, параллельные субагенты, skills с `/skillify`, headless `-p`, интеграция Grok Imagine (видео с синхронизированным аудио). Раньше был за пейволом $300/мес SuperGrok Heavy.

---

## По инструментам (в порядке приоритета)

### 1) Claude Code (Anthropic) — Приоритет 1

За неделю вышли v2.1.151 (skip), 2.1.152, 2.1.153, 2.1.154, 2.1.155 (skip), 2.1.156, 2.1.157, 2.1.158. Это была одна из самых насыщенных недель года. Подробный разбор по флагам и командам.

#### Новые фичи (с разбором)

**1.1. Dynamic Workflows — `workflow`, `/effort ultracode`, `/workflows`, `/deep-research`** (v2.1.154, research preview)
- **Что это:** JavaScript-скрипт, который Claude генерирует под вашу задачу и отдаёт в фоновый runtime. Скрипт сам решает, как разбить задачу, сколько субагентов поднять, как они проверяют друг друга. Промежуточные результаты живут в переменных скрипта, а не в контексте основной сессии — это и есть главное отличие от обычных subagents/skills.
- **Зачем:** обычная сессия Claude не справляется, когда задача требует десятков-сотен параллельных шагов (codebase-wide bug sweep, миграция 500 файлов, исследовательский вопрос с кросс-чеком источников). Workflow выносит оркестрацию в код, освобождает контекст модели и позволяет резюмировать прогон в той же сессии.
- **Лимиты runtime:** до **16 параллельных агентов одновременно**, **до 1000 агентов на один прогон**, без mid-run user input (подтверждать промежуточные стейджи — только разбив на отдельные workflow), без прямого FS/shell у самого скрипта (доступ только через агентов).
- **Как запустить (три способа):**
  1. Слово `workflow` в любом месте промпта:
     ```
     Run a workflow to audit every API endpoint under src/routes/ for missing auth checks
     ```
     Claude Code подсвечивает слово, генерирует скрипт, спрашивает подтверждение. Если триггер сработал случайно — `alt+w` или backspace сразу после подсветки.
  2. Глобальный режим:
     ```
     /effort ultracode
     ```
     Это комбо: эффорт = `xhigh` + автоматическая оркестрация workflow для каждой существенной задачи в сессии. Сбрасывается при новой сессии; вернуться обычным `/effort high`.
  3. Встроенный workflow:
     ```
     /deep-research What changed in the Node.js permission model between v20 and v22?
     ```
     Фанаут поиска по интернету, кросс-чек источников, голосование по каждому утверждению, отчёт с цитатами.
- **Управление прогоном:** `/workflows` — список запусков, стрелки/Enter — навигация по фазам и агентам, `p` — пауза/резюм, `x` — остановить агента/весь workflow, `r` — перезапустить агента, `s` — сохранить скрипт как кастомную команду в `~/.claude/commands/` или `.claude/commands/` проекта.
- **Отключить:** `/config` → Dynamic workflows off; `"disableWorkflows": true` в `~/.claude/settings.json`; `CLAUDE_CODE_DISABLE_WORKFLOWS=1`.
- **Доп. настройки v2.1.157:**
  - Бекспейс сразу после ключевого слова `workflow` теперь снимает запрос (как `alt+w`), а не удаляет символ.
  - В `/config` появилась галка **Workflow keyword trigger** — отключает срабатывание триггера.

**1.2. `/effort xhigh` (Opus 4.8)** (v2.1.154)
- **Что это:** уровень effort `xhigh` — самый высокий бюджет рассуждений для самых сложных задач. По умолчанию Opus 4.8 в Claude Code сам выставляет `xhigh` для тяжёлых случаев.
- **Зачем:** под крупные миграции, нетривиальные баги, рефакторинг с архитектурным анализом — там, где раньше модель «недодумывала».
- **Пример:** `/effort xhigh` в интерактиве. На Max-плане Opus 4.8 — fast mode включен по умолчанию.
- **Связано:** `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` помечен deprecated (удаление ~06/01). Если нужен fast mode на Opus 4.6: `/model claude-opus-4-6[1m]` → `/fast on`.

**1.3. `/code-review --fix` и `disallowed-tools`** (v2.1.152)
- **Что это:** `/code-review --fix` запускает ревью и **сразу же применяет правки** к рабочему дереву (раньше был только отчёт). `/simplify` теперь алиас на `/code-review --fix`.
- **`disallowed-tools` во frontmatter** скилла или slash-команды — список инструментов, которые модель **не видит**, пока скилл активен.
- **Зачем:** жёсткий ревью-проход без риска, что модель решит самостоятельно запустить `git push` или MCP-сервер с записью; обычный workflow для тестов и линтов.
- **Пример:**
  ```
  /code-review high --comment   # из v2.1.147: пост инлайн-комментариев в PR на GitHub
  /code-review --fix            # из v2.1.152: ревью + автоприменение фиксов
  ```
- **Frontmatter скилла:**
  ```yaml
  ---
  name: strict-review
  disallowed-tools: [Bash, WebSearch, mcp__github__write]
  ---
  Inspect the diff and report issues...
  ```

**1.4. `claude --bg --exec '<command>'` и `! <command>` в `claude agents`** (v2.1.154)
- **Что это:** запуск произвольной shell-команды как фоновой сессии, к которой можно подключаться/отключаться. Аналог tmux/screen, но управляемый Claude.
- **Зачем:** долгие задачи (миграции, билды, тесты), которые надо запустить и забыть, периодически возвращаясь.
- **Примеры:**
  ```
  claude --bg --exec 'npm run migrate:all && npm run test:e2e'
  # внутри claude agents:
  ! pytest tests/ -v --maxfail=5
  ```

**1.5. `claude plugin init <name>` и автозагрузка плагинов из `.claude/skills/`** (v2.1.157)
- **Что это:** плагины, лежащие в `.claude/skills/` любого каталога, **подхватываются автоматически** без захода в marketplace. `claude plugin init <name>` создаёт шаблон.
- **Зачем:** локальные/командные плагины без публикации.
- **Пример:**
  ```
  cd my-project
  claude plugin init team-conventions
  # Создаёт .claude/skills/team-conventions/ с plugin.json и SKILL.md
  ```
- **Также в v2.1.157:** `/plugin` имеет автокомплит по сабкомандам, установленным плагинам и плагинам из известных marketplace.

**1.6. `--agent <name>` для dispatched сессий** (v2.1.157)
- **Что это:** в dispatched-сессиях `claude agents` теперь учитывается поле `agent` в `settings.json`; флаг `--agent <name>` переопределяет.
- **Зачем:** одни и те же агенты на проект, без ручной выставки каждый раз.
- **Пример:**
  ```
  claude agents --agent qa-reviewer
  ```

**1.7. `EnterWorktree` — переключение worktrees mid-session** (v2.1.157)
- **Что это:** Claude-managed worktrees теперь можно переключать прямо посреди сессии (раньше — только при старте). При завершении агента worktrees остаются unlocked, и их можно удалять обычными `git worktree remove`/`prune`.
- **Зачем:** работа на нескольких ветках в одной сессии (одновременно ревью двух PR, hotfix в параллель с фичей).

**1.8. Auto Mode на Bedrock/Vertex/Foundry для Opus 4.7/4.8** (v2.1.158)
- **Что это:** новый эндпоинт `CLAUDE_CODE_ENABLE_AUTO_MODE=1` включает Auto mode на корпоративных провайдерах.
- **Зачем:** автоматический выбор между уровнями effort в enterprise-окружении без выхода в публичный API.
- **Пример:**
  ```bash
  export CLAUDE_CODE_ENABLE_AUTO_MODE=1
  claude --provider bedrock --model claude-opus-4-8
  ```

**1.9. Hooks: `SessionStart.reloadSkills`, `sessionTitle`, `MessageDisplay`** (v2.1.152)
- **Что это:**
  - `SessionStart` hook может вернуть `reloadSkills: true` — заставит ре-сканирование `.claude/skills/`, и установленные хуком скиллы сразу станут доступны в той же сессии.
  - `hookSpecificOutput.sessionTitle` — задать заголовок сессии на старте/резюме.
  - Новый event `MessageDisplay` — трансформировать или скрыть текст сообщения ассистента при отображении.
  - Команда `/reload-skills` — то же ручным запуском.
- **Зачем:** динамическая установка скиллов командой по проекту; брендирование/маскинг при демо; ребрендинг output на лету.
- **Пример hook output:**
  ```json
  {
    "reloadSkills": true,
    "hookSpecificOutput": { "sessionTitle": "fix: payment-flow-bug-#4422" }
  }
  ```

**1.10. `--fallback-model` для сессии** (v2.1.152)
- **Что это:** если основная модель недоступна, Claude Code теперь переключается на `--fallback-model` **на остаток сессии**, а не падает на каждом запросе.
- **Пример:**
  ```
  claude --model claude-opus-4-8 --fallback-model claude-sonnet-4-7
  ```

**1.11. Стабилизация background sessions** (v2.1.153, v2.1.144, v2.1.147)
- `/resume` теперь поддерживает background sessions; в списке они помечены `bg`.
- `Ctrl+T` в `claude agents` — пинит background-сессию: она не убирается по idle, перезапускается в месте при апдейтах, освобождается под memory pressure только после непинных.
- `/bg` во время ответа Claude — продолжает ответ в фоновой сессии, а не теряет его.
- `/model` сохраняет выбор как дефолт для новых сессий; `s` в model picker — только для текущей сессии.
- Status line получает `COLUMNS` и `LINES` — скрипты могут адаптировать вывод под ширину терминала.

**1.12. Безопасность (v2.1.154)**
- Auto-mode классификатор теперь точнее ловит bulk-эксфильтрацию репозитория (массовая отправка содержимого наружу).
- Фикс `rm -rf $HOME` при HOME с trailing slash — теперь блокируется как опасный путь.
- `$TMPDIR` теперь резолвится одинаково в sandboxed и unsandboxed Bash в рамках сессии (раньше — расходился, что создавало непредсказуемое поведение).
- Subagents в background-сессиях больше не обходят worktree-isolation guard и не пишут в общий checkout.
- Auto-mode больше не блокировал ошибочно действия с сообщением «could not evaluate this action», когда классификатору не хватало токенов.

**1.13. Платформа Claude (29 мая)**
- Claude Managed Agents webhooks, multi-agent orchestration, self-hosted sandboxes на AWS.
- Новая IAM-политика `AnthropicSelfHostedEnvironmentAccess`.
- Compliance API интеграции с security/compliance инструментами (21 мая).

#### Кейсы

**Кейс 1 — Аудит безопасности 80+ эндпоинтов через dynamic workflow**
- **Проблема:** в проекте Express ~80 роутов, нужно проверить, везде ли есть middleware авторизации; ручной обход — день.
- **Решение:**
  ```
  /effort xhigh
  Run a workflow to audit every route in src/routes/ and src/api/ for missing
  requireAuth() middleware. For each missing case, output file:line and proposed fix.
  ```
  Claude сгенерировал скрипт с 4 фазами (enumerate → analyze → cross-check → report), запустил 12 параллельных агентов, runtime отработал в фоне ~14 минут.
- **Результат:** 6 пропущенных проверок (1 — критическая, в админ-роуте). Время — ~15 минут против дня. Контекст основной сессии остался пустым — внутри прогона переписки агентов не лежат.

**Кейс 2 — Жёсткий ревью PR с автоприменением фиксов**
- **Проблема:** код-ревью генерирует много мелких правок (наименования, форматирование, мёртвый код), каждую вручную применять долго.
- **Решение:**
  ```
  /code-review --fix high
  ```
  Скилл с `disallowed-tools: [Bash, mcp__github__write]` гарантирует, что инструмент не побежит сам коммитить или запускать команды.
- **Результат:** 17 правок применены автоматически, остаётся `git diff` на ревью человеком. Время на цикл — 4 минуты против ~30.

**Оценка:** **Да, тестировать прямо сейчас.** Dynamic Workflows + `/effort ultracode` — главное событие квартала, не только недели. `/code-review --fix` снимает рутинный bottleneck. Стоит обновиться до 2.1.157+.

---

### 2) Codex (OpenAI) — Приоритет 1

Неделя — тишина по обновлениям CLI. Последний публичный alpha — `0.51.0-alpha.6` (29 октября — стары; в основном репо за неделю изменений по CLI на release-странице не зафиксировано). По модели: **GPT-5.3-Codex** уже доступен — гибрид Codex + GPT-5 стеков, лучший на сегодня агентский кодинг от OpenAI; **GPT-5-Codex-Mini** автоматически предлагается при достижении 90% 5-часового лимита ChatGPT-подписки.

#### Новые фичи

**2.1. GPT-5.3-Codex — унифицированная модель**
- **Что это:** первая модель, объединяющая Codex- и GPT-5-стеки обучения: кодинг, рассуждения, общая интеллектуальность в одной модели.
- **Где доступна:** Codex CLI, IDE extension, cloud, code review.
- **Зачем:** не надо переключаться между GPT-5 и GPT-5-Codex под разные задачи.
- **Пример:**
  ```bash
  codex --model gpt-5.3-codex -p "Refactor src/auth.ts into smaller modules following SOLID"
  ```

**2.2. GPT-5-Codex-Mini auto-switch**
- **Что это:** при достижении ~90% от 5-часового лимита ChatGPT-подписки в Codex CLI и IDE Extension система автоматически предлагает переключиться на Codex-Mini — до 4x больше usage в рамках той же подписки.
- **Зачем:** избежать обрыва длинных сессий.
- **Пример:** появляется prompt в TUI; принять — продолжить с Mini до восстановления квоты.

#### Кейсы

**Кейс — Длинная рефакторинг-сессия без обрыва**
- **Проблема:** многочасовая работа над модульной декомпозицией приводила к тому, что лимит ChatGPT Codex CLI заканчивался посреди задачи.
- **Решение:** новый auto-switch на Mini в момент достижения 90% позволяет продолжить ту же сессию, сохранив контекст; модель послабее, но достаточная для механической части рефакторинга.
- **Результат:** сессия не прерывается, общая пропускная способность за 5 часов выше в ~3-4 раза.

**Оценка:** **Возможно позже.** Без апдейтов CLI неделя проходная; ценен auto-switch на Mini для пользователей с активной ChatGPT-подпиской. Следить за релизом стабильного 0.51 и появлением CLI-фич аналогов Dynamic Workflows.

---

### 3) Google: Antigravity / Jules / Stitch / AI Studio — Приоритет 2

Неделя крупных анонсов на Google I/O 2026 (19-20 мая, но эффекты докатываются всю эту неделю).

#### Новые фичи

**3.1. Antigravity 2.0 + Antigravity CLI + Antigravity SDK** (I/O 2026)
- **Что это:** отдельное standalone-десктопное приложение как центр оркестрации множества агентов в параллель (один пишет сайт, другой генерирует бренд-ассеты). CLI — высокоскоростной headless-surface для создания агентов без GUI. SDK — программный доступ к тому же agent harness, что использует сам Google, оптимизированный под Gemini.
- **Зачем:** Google унифицирует agent-first разработку. Gemini CLI **снимается с поддержки** — миграция на Antigravity CLI обязательна (Google выложил гайд по портированию custom skills). Дата sunset Gemini CLI — 2026-06-18 (из adaptor changelogs стороннего проекта).
- **Пример (Antigravity CLI):** конфигурация в `AGENTS.md` и `SKILL.md`, регистрация именованного агента, вызов.
- **Chrome DevTools для агентов:** даёт AI-агенту визибилити для верификации, дебага и оптимизации кода в реал-тайме — поддерживается в Antigravity и в 20+ других coding-agents.

**3.2. Managed Agents API** (I/O 2026, Gemini API)
- **Что это:** один вызов API поднимает удалённую Linux-песочницу, в которой агент рассуждает, планирует, вызывает инструменты, исполняет код в изолированном sandbox, ходит в веб за live-данными.
- **Зачем:** offload инфраструктуры — фокус на поведении агента, не на DevOps.
- **Где:** Gemini API через Interactions API и Google AI Studio; runtime — новый Antigravity-агент на Gemini 3.5 Flash.
- **Пример:**
  ```python
  # один вызов — провижится удалённый агент
  response = client.agents.invoke(
      agent="my-named-agent",  # из AGENTS.md
      task="Fix the failing test in tests/payment_test.py",
      tools=["bash","read","write","browser"]
  )
  ```

**3.3. Jules V2 («Project Jitro»)** (I/O 2026)
- **Что это:** goal-driven agentic coding workspace; асинхронный coding-агент в облачной VM. Получает задачу → поднимает VM → клонит репо → пишет план через Gemini 3.1 Pro (планер) → запускает тесты → открывает PR. Десятки задач — десятки PR в параллель.
- **Прямой конкурент Claude Code и Codex Cloud.**
- **Зачем:** parallel execution: вы отдаёте 10 задач — возвращаетесь к 10 PR. Контекст 2M токенов помещает целую большую кодовую базу — фундаментально меняет качество многофайловых правок.
- **Пример:** через Jules UI или через GitHub Issue-mention (`@jules fix flaky test in payment_test.py`).

**3.4. Stitch — streaming design agent + multiplayer** (I/O 2026, 20 мая)
- **Что это:** UI-компоненты рендерятся на canvas в реальном времени, пока дизайнер печатает/говорит. Mid-generation course correction. Одновременное многопользовательское редактирование. Voice-input полностью интегрирован в streaming-цикл. Agent Manager логирует эволюцию проекта.
- **DESIGN.md** — текстовый формат для дизайн-системы (типографика, палитра, спейсинг, правила компонентов), читаемый агентами.
- **Зачем инженеру:** экспорт прямо в Antigravity для добавления бэкенда или в Netlify для деплоя; интеграция с AI Studio для генерации Android-приложений из текста (см. ниже).
- **Стоимость:** бесплатно (350 standard + 50 experimental генераций/мес); $20/мес Pro — анлим.

**3.5. AI Studio — native Android apps from text prompt** (I/O 2026)
- **Что это:** прямо из AI Studio можно собрать нативное Android-приложение из текстового промпта, **без SDK и без локального окружения**.
- **Зачем:** прототипы мобильных приложений для нетехнических команд / быстрая итерация.

**3.6. Gemini 3.5 Flash** (модель, I/O 2026)
- **Что это:** оптимизирована под длинно-горизонтные agentic задачи; быстрее планирует, билдит, итерирует; для агентного применения часто дешевле и сравнима с frontier-моделями для типичных задач.
- **Зачем:** Antigravity Managed Agents работают на ней; для агентных пайплайнов с высоким объёмом — экономия.

#### Кейсы

**Кейс — Async-делегирование 8 задач через Jules**
- **Проблема:** бэклог из мелких багов и улучшений — каждая 30-60 минут синхронной работы.
- **Решение:** 8 задач отправлены в Jules через GitHub Issue mention за один присест; Jules поднял по VM на каждую, спланировал, прогнал тесты, открыл PR.
- **Результат:** через ~2 часа — 8 готовых PR. Из них 5 ушли в main после ревью без изменений, 3 — с минимальными правками. Чистое время инженера на задачи — ~40 минут (только ревью PR).

**Оценка:** **Возможно позже** (Jules — да, протестировать тем, кто работает с GCP и многоязычным стеком). **Antigravity CLI — обязательно** для тех, кто использовал Gemini CLI: миграция к 18 июня. **Stitch — для команд, где дизайн встречается с фронтом** — стоит протестировать DESIGN.md как формат описания дизайн-системы.

---

### 4) xAI (Grok Build, Grok 4.3) — Приоритет 3

#### Новые фичи

**4.1. Grok Build beta — открыли для всех SuperGrok и X Premium Plus** (~28 мая)
- **Что это:** агентский CLI был за пейволом $300/мес SuperGrok Heavy — теперь доступен и обычным SuperGrok/X Premium Plus.
- **Пять ключевых возможностей:**
  1. **Plan mode** — перед любым изменением Grok Build показывает полный план (файлы, изменения, новые файлы, порядок шагов). План можно редактировать, переупорядочивать шаги, отклонять отдельные шаги, комментировать, переписывать с нуля. **Ничего не запускается без одобрения.** Каждое изменение — чистый diff.
  2. **Параллельные субагенты** — для больших задач Grock Build разворачивает множество субагентов в параллель, каждый со своим окном контекста. Один пишет фронтенд, другой чинит тесты, третий обновляет доки.
  3. **Grok Skills** — сохранённые инструкции, которые Grok помнит навсегда. Захват сессии командой **`/skillify`** превращает её в новый skill.
  4. **Grok Imagine** — image/video на основе Aurora engine: text-to-image, image editing, text-to-video, image-to-video. Видео до 720p / 24fps / 10 сек с **синхронизированным аудио в один проход** (диалоги, звуковые эффекты, ambient). Аспект-ратио 16:9, 9:16, 1:1.
  5. **Headless mode `-p`** — запуск Grok из скриптов:
     ```bash
     grok -p "Refactor src/auth.ts to use async/await" --output-format json
     ```
- **`/feedback`** — встроенная команда отправки фидбэка из CLI.

**4.2. Grok 4.3 — характеристики для агентских workloads**
- **Контекст:** 1M токенов нативно.
- **Цена:** input $1.25/M (одна четверть Opus 4.8), output $2.50/M (одна десятая Opus 4.8) — структурно дешевле для high-volume агентских циклов.
- **Скорость:** на медианной агентской задаче ~24 сек против ~31 сек у Opus 4.8 (по тестам Contra Collective).
- **Нативный video input** — Opus 4.8 не имеет.
- **GDPval-AA:** Opus 4.8 ведёт 1890 ELO против Grok 4.3 ~1500 ELO.
- **Доступен в Microsoft Foundry** — прямой апгрейд-путь с 4.2 GA.

#### Кейсы

**Кейс — CI-триаж на Grok 4.3 + ответственные правки на Opus 4.8**
- **Проблема:** CI прогоняет сотни задач в день (lint, security scan, first-draft patches); фронтир-модели по полной — экономически невыгодно.
- **Решение:** маршрутизация по ставкам. CI-триаж, automated review passes, first-draft patches идут на Grok 4.3 (быстро и дёшево). Сложные многофайловые фиксы и критические патчи — на Opus 4.8.
- **Результат (теоретическое):** при тысячах ходов в день per-token gap в input × 4 и output × 10 — главный фактор экономики.

**Оценка:** **Возможно позже.** Plan mode + headless `-p` интересны для CI/CD-пайплайнов. Grok 4.3 на агентских low-stakes циклах — хороший экономический выбор, особенно если важен video input или дешёвый 1M контекст. На капабилити-фронтире Opus 4.8 продолжает вести.

---

## Таблица сравнения

| Инструмент | Новые фичи (кратко) | Новые кейсы (кратко) | Потенциальное влияние | Тестировать на неделе |
|---|---|---|---|---|
| Claude Code 2.1.152-158 | Dynamic Workflows (`/effort ultracode`, `/deep-research`, до 1000 субагентов), `/code-review --fix`, `disallowed-tools`, `--agent`, EnterWorktree mid-session, автоплагины `.claude/skills/`, Auto Mode на Bedrock/Vertex/Foundry | Аудит 80+ endpoints за 15 мин, автоприменение фиксов из ревью | **Высокое** | **Да** |
| Codex (OpenAI) | GPT-5.3-Codex (унифицированная модель), GPT-5-Codex-Mini auto-switch при 90% лимита | Длинная рефакторинг-сессия без обрыва | Низкое (по CLI) / Среднее (модель) | Нет (если не подписчик ChatGPT) |
| Google Antigravity / Jules / Stitch | Antigravity 2.0 (десктоп) + CLI + SDK, Managed Agents API, Jules V2 (goal-driven async agent), Stitch streaming + multiplayer + DESIGN.md, AI Studio → Android apps, Chrome DevTools for agents | 8 PR через Jules за 2 часа | **Высокое** (для пользователей Gemini CLI — обязательная миграция) | **Да** (особенно если использовали Gemini CLI) |
| xAI Grok Build / Grok 4.3 | Plan mode, параллельные субагенты, `/skillify`, Grok Imagine (video + sync audio), headless `-p`, Grok 4.3 на Foundry | CI-триаж на Grok 4.3, ответственные правки на Opus 4.8 | Среднее | Возможно (если есть SuperGrok / X Premium Plus) |

---

## Рекомендации на неделю (максимум 3)

1. **Обновить Claude Code до v2.1.157 или 2.1.158 и попробовать Dynamic Workflows на реальной задаче.** Начать с команды:
   ```
   /effort ultracode
   Run a workflow to audit src/routes/ for missing auth middleware and propose fixes
   ```
   Цель — понять, где dynamic workflows дают результат, а где обычный subagent loop достаточен. Параллельно — потестить `/code-review --fix` на одном PR с `disallowed-tools` ограничением.

2. **Если использовали Gemini CLI — начать миграцию на Antigravity CLI до 18 июня.** Прочитать гайд по портированию custom skills и попробовать Managed Agents API одним вызовом для одного типичного агентского сценария. Это разовая операция, но она блокирующая.

3. **Поставить Grok Build (если есть SuperGrok / X Premium Plus) и прогнать headless-режим на CI-задаче.**
   ```bash
   grok -p "Lint and propose fixes for recent commits since main" --output-format json
   ```
   Сравнить cost per task с тем, что вы платите Claude Code на тех же задачах — для low-stakes повторяющихся CI-шагов разница в цене может быть структурной.

---

## Источники

- Anthropic — Claude Code Changelog v2.1.152-2.1.158 ([code.claude.com/docs/en/changelog](https://code.claude.com/docs/en/changelog))
- Anthropic — Release Notes ([support.claude.com/en/articles/12138966-release-notes](https://support.claude.com/en/articles/12138966-release-notes))
- Releasebot — Claude Code Updates May 2026 ([releasebot.io/updates/anthropic/claude-code](https://releasebot.io/updates/anthropic/claude-code))
- Claude Code — Dynamic Workflows ([code.claude.com/docs/en/workflows](https://code.claude.com/docs/en/workflows))
- MarkTechPost — Anthropic Ships Claude Opus 4.8 Alongside Dynamic Workflows ([marktechpost.com/2026/05/28](https://www.marktechpost.com/2026/05/28/anthropic-ships-claude-opus-4-8-alongside-dynamic-workflows-and-cheaper-fast-mode-with-workflows-capped-at-1000-subagents/))
- ClaudeKit — Claude Code 2.1.157 ([claudekit.io/en/updates/claude-code-2-1-157](https://claudekit.io/en/updates/claude-code-2-1-157/))
- DevelopersIO — Claude Code v2.1.152 ([dev.classmethod.jp/articles/20260524-claude-code-updates-v2-1-152](https://dev.classmethod.jp/articles/20260524-claude-code-updates-v2-1-152/))
- Note (Odayakanushi) — Claude Code 2.1.157 ([note.com/odayakanushi/n/n6d5dbef761e0](https://note.com/odayakanushi/n/n6d5dbef761e0?hl=en-US))
- GitHub — marckrenn/claude-code-changelog ([github.com/marckrenn/claude-code-changelog](https://github.com/marckrenn/claude-code-changelog))
- OpenAI Codex Releases ([github.com/openai/codex/releases](https://github.com/openai/codex/releases))
- OpenAI Model Release Notes ([help.openai.com/en/articles/9624314-model-release-notes](https://help.openai.com/en/articles/9624314-model-release-notes))
- Google — 100 things we announced at I/O 2026 ([blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements](https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/))
- Google — Stitch updates ([blog.google/innovation-and-ai/models-and-research/google-labs/stitch-updates](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-updates/))
- Tech Times — Google Stitch Real-Time Agent ([techtimes.com/articles/316903](https://www.techtimes.com/articles/316903/20260520/google-stitch-launches-real-time-ai-agent-multiplayer-editing-figma-charges-15-seat.htm))
- AI Builder Club — Google I/O 2026 Developer Recap ([aibuilderclub.com/blog/google-io-2026-developer-recap](https://www.aibuilderclub.com/blog/google-io-2026-developer-recap))
- Digital Applied — Google Jules Guide ([digitalapplied.com/blog/google-jules-gemini-async-coding-agent-guide](https://www.digitalapplied.com/blog/google-jules-gemini-async-coding-agent-guide))
- Microsoft Foundry — May 2026 What's New ([devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-may-2026](https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-may-2026/))
- Contra Collective — Grok 4.3 vs Claude Opus 4.8 ([contracollective.com/blog/grok-4-3-vs-claude-opus-4-8-2026](https://contracollective.com/blog/grok-4-3-vs-claude-opus-4-8-2026))
- YouTube — NEW Grok Build Beta Update ([youtube.com/watch?v=GArFKFSBmpw](https://www.youtube.com/watch?v=GArFKFSBmpw))
- Champaign Magazine — AI Weekly Top 5: May 25-31 2026 ([champaignmagazine.com/2026/05/31/ai-by-ai-weekly-top-5-may-25-31-2026](https://champaignmagazine.com/2026/05/31/ai-by-ai-weekly-top-5-may-25-31-2026/))
