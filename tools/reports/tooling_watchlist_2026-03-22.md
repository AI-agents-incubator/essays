# Tooling Watchlist — Code & Agents

Еженедельный отчёт · 22 марта 2026 · Первый выпуск

## 1. Executive Summary

- **Claude Code: 1M-контекст без наценки + Agent Teams.** С 13 марта Anthropic сделал 1M-токенный контекст GA по стандартной цене. Одновременно вышел экспериментальный Agent Teams — несколько агентов Claude с собственными контекстными окнами общаются peer-to-peer. Для соло-разработчика это значит: загрузить целый проект в один сеанс без чанкинга; для сложных аудитов — параллельные агенты.

- **Codex: GPT-5.4 + субагенты из experimental.** OpenAI выпустила GPT-5.4 с режимом /fast (1.5x скорость) и нативным computer use. Субагенты теперь стабильная фича (TOML-конфиг под роли). Codex Security сканирует уязвимости в коде — за месяц бета нашёл 792 критические и 10 561 высокие уязвимости в открытых проектах.

- **Cursor: Composer 2 — на 57-86% дешевле + Automations.** Cursor выпустил собственную модель Composer 2 ($0.50/M input Standard vs $3.50 у предыдущей). Automations — облачные агенты, работающие по триггерам (Slack, GitHub PR, cron). Скандал: модель построена на китайской open-source Kimi k2.5; Cursor не раскрыл это при запуске.

- **Google: AI Studio теперь full-stack + Jules CI Fixer.** Antigravity-агент в AI Studio автоматически поднимает Firebase-бэкенд, мультиплеер, Next.js. Jules получил MCP-интеграции (Supabase, Linear), CI Fixer автоматически чинит упавшие GitHub Actions.

- **xAI: признание отставания + хайры из Cursor.** Маск публично заявил, что инструменты xAI для кода были построены неправильно с первого раза. Наняты два product-лида Cursor (Andrew Milich, Jason Ginsberg). Grok 4.20 Multi-Agent вышел в Enterprise API ($2/$6 за M токенов). Ожидаемый срок конкуренции — середина 2026.

## 2. По инструментам

### Claude Code / Cowork (Anthropic)

**Новые фичи:**

- 1M-контекстное окно GA (13 марта) — стандартная цена, без наценки за длинный контекст. MRCR v2: 78.3% (Gemini: 26.3%). 15% меньше компакций.
- Agent Teams (experimental, v2.1.76) — несколько независимых Claude-агентов с peer-to-peer mailbox-коммуникацией. Каждый агент — своё 1M-окно. Скорость ~2x, стоимость токенов ~3–4x.
- Hooks: 22 события жизненного цикла, 4 типа хэндлеров (command, HTTP, prompt, agent). PreToolUse блокирует опасные команды детерминированно — LLM не может обойти.
- MCP Elicitation — MCP-серверы запрашивают ввод mid-task без прерывания агентного цикла.
- Auto-Plan — Claude сам входит в режим планирования на сложных промптах.
- Voice mode (/voice) — голосовой ввод в CLI, раскатка с 5% пользователей с 3 марта.
- Cowork Dispatch (17 марта) — управление десктопным агентом с телефона через QR-пару. Preview, ~50/50 надёжность.
- Cowork Projects (20 марта) — per-project изоляция с контекстом, задачами и расписанием.
- 38+ коннекторов (Jira, Slack, Salesforce, Snowflake, Figma и др.). Microsoft Copilot Cowork ($99/user/month с 1 мая).

**Кейсы:**

- Соло-разработчик использует Claude Code Max как полную бизнес-ОС: утренний брифинг из 5 источников за 30 секунд, voice-to-task маршрутизация, 993 passing теста, 573 обработанных анкеты.
- Jira > implementation > test > status update в одной терминальной сессии (Builder.io). Экономия ~15 мин контекст-свитчинга на тикет.
- Spotify: 90% сокращение инженерного времени на миграции кода.
- Anthropic внутренне: ~90% кода Claude Code написано самим Claude Code; 60–100 внутренних релизов/день.

**Оценка:** Полезно прямо сейчас — да. 1M-контекст и Hooks-система — самые практичные обновления для соло-разработчика. Загрузить весь средний проект в одну сессию без чанкинга; авто-запуск Prettier/ESLint после каждого файлового edit через Hooks. Agent Teams — для квартальных масштабных аудитов.

### Codex (OpenAI)

**Новые фичи:**

- GPT-5.4 в Codex (5 марта) — SWE-Bench Pro: 57.7%. Режим /fast: 1.5x скорость, 2x кредитов. 1M-контекст (экспериментальный, 2x rate). Нативный computer use.
- Playwright Interactive Skill — Codex визуально тестирует UI в live-браузере во время разработки. Self-correcting frontend loop.
- Codex Security (6 марта, research preview) — за 30 дней бета: 792 critical + 10 561 high в 1.2M коммитов. 14 CVE (OpenSSH, GnuTLS, PHP, Chromium). False positive rate снижен >50%.
- Субагенты вышли из experimental (~17 марта) — TOML-конфигурация ролей в /.codex/agents/. Параллельные/последовательные агенты с настройкой модели и reasoning effort для каждого.
- GPT-5.4 mini/nano (17–18 марта) — 2x быстрее GPT-5 mini, приближается к GPT-5.4 на SWE-Bench Pro. Идеальный «рабочий» модель для субагентов.
- CLI 0.115.0 / 0.116.0 — Full-res image inspection, Python SDK для filesystem RPCs, userpromptsubmit хук, realtime transcription. NB: регрессия на Debian 12 в 0.116.0.

**Кейсы:**

- WorkOS: 85–90% success rate на TypeScript/JS задачах обслуживания (было 40–60%). 2–3 готовых PR к утру из 4–5 ночных задач.
- Multi-agent оркестрация: GPT-5.4 high (orchestrator) + GPT-5.3-Codex medium (контекст) + GPT-5.3-Codex high (код) + GPT-5.3-Codex high (review PASS/REVISE).
- NETGEAR: Codex Security описан как «впечатляюще ясный и полный, как опытный исследователь безопасности рядом».

**Оценка:** Полезно прямо сейчас — да. GPT-5.4 /fast и субагенты — самые важные изменения. Playwright Interactive Skill особенно актуален для JS-разработчика: self-correcting frontend. Ограничение: cold-start sandbox 30–120с на простых задачах; качество кода на архитектурных задачах ниже Claude.

### Cursor

**Новые фичи:**

- Cursor Automations (5 марта) — облачные event-driven агенты по триггерам: Slack, GitHub PR, Linear, PagerDuty, cron, webhook. Агенты имеют memory tool — учатся на прошлых запусках.
- Composer 2 (19 марта) — собственная модель Cursor. CursorBench: 61.3 (бьёт Claude Opus 4.6 ~55). Цена: $0.50/M input Standard — на 86% дешевле Composer 1.5. Построена на Kimi k2.5 (Moonshot AI) — Cursor не раскрыл при запуске, признал 22 марта.
- 30+ плагинов Marketplace (11 марта) — Datadog, GitLab, PlanetScale, Atlassian, Glean, Hugging Face. Плагины = MCP + agent skill (инструкция для агента), надёжнее сырых MCP.
- v2.6 MCP Apps — интерактивные HTML-интерфейсы (charts, diagrams) прямо в агентском чате в sandboxed iframe.
- JetBrains ACP (4 марта) — Cursor-агент внутри PyCharm/IntelliJ/WebStorm. Бесплатно для платных подписчиков Cursor.

**Кейсы:**

- Money Forward (1000+ инженеров): 15–20 часов экономии на инженера в неделю, 70% ускорение QA, 10x оптимизация Rails.
- Rippling: cron-автоматизация каждые 2 часа — агрегация meeting notes, action items, GitHub PRs, Jira, Slack mentions в единый дашборд.
- Reddit-разработчик: 80K-строчный TypeScript monorepo — Composer 2 для реализации, Claude Opus для планирования. Лучшее соотношение цена/качество.

**Оценка:** Полезно прямо сейчас — да. Composer 2 — прямая экономия на повседневных задачах. Automations полезны для соло-разработчика: тесты по расписанию, triage багов из Slack. Риск: скандал с Kimi вызывает вопросы доверия (но технически модель работает). Конкуренция Claude Code усиливается для автономных задач.

### Google (Antigravity / Genie / AI Studio / Jules)

**Новые фичи:**

- AI Studio full-stack vibe coding (18 марта) — Antigravity-агент в Build mode: Firebase-бэкенд (Firestore + Auth), мультиплеер, Next.js, Secrets Manager. Сотни тысяч приложений за последние месяцы.
- Gemini Code Assist: Finish Changes GA (Option+F) — завершает код из псевдокода/TODO-комментариев. File Outlines (Option+O) — AI-навигация по файлу. Бесплатно, VS Code + IntelliJ.
- Gemini 3.1 Pro + 3.0 Flash в Code Assist (13 марта, Preview) — для agent mode, чата и кодогенерации.
- Jules: Gemini 3.1 Pro по умолчанию (Pro). MCP серверы (Linear, Supabase, Neon). CI Fixer — автоматически чинит упавшие GitHub Actions. Planning Critic: -9.5% отказов задач.
- Stitch «Vibe Design» (18 марта) — AI-канвас с voice, DESIGN.md, экспорт в AI Studio и Antigravity.
- Gemini CLI v0.34 (17 марта) — Plan Mode по умолчанию, gVisor/LXC sandboxing, A2A HTTP auth.
- Genie 3 (GDC, 9–13 марта) — экспериментальный, миры теряют связность через минуты. Нет API. Только US AI Ultra ($250/мес).

**Кейсы:**

- Ночной 7-бот Jules пайплайн: 3 scheduled-агента (security, performance, UX) + 3 code-review бота + финализатор. Ежедневные PR без ручной работы.
- Родитель с новорождённым: voice-диктует задачи Jules на прогулке > через 30–45 мин готовый PR.
- AI Studio: мультиплеерная 3D-игра Neon Arena из одного промпта (Three.js + WebSocket + Firebase).
- Stitch > AI Studio: от дизайна до deploy за <1 час (community-отчёты: -70% design-to-code, -60% time-to-market).

**Оценка:** Полезно прямо сейчас — да (Jules + Finish Changes). Jules Scheduled Tasks + CI Fixer — бесплатно и практично: ночные security/deps/test проверки. Finish Changes (Option+F) — лучший underrated feature для написания кода через TODO-комментарии. AI Studio vibe coding — идеален для прототипов, но не для production.

### xAI (Grok)

**Новые фичи:**

- Grok 4.20 + Multi-Agent API (10 марта) — 3 варианта: multi-agent (4 агента: координатор, исследователь, кодер, критик), reasoning, non-reasoning. $2/$6 за M токенов — самая дешёвая западная frontier модель.
- xAI нанял двух product-лидов Cursor (12–13 марта). Маск: инструменты «были построены неправильно». Ожидаемый catch-up: середина 2026.
- Grok Build — CLI-агент через npm (8 параллельных агентов, Arena Mode). Local-first: код не покидает машину. Но без IDE-интеграции и GitHub.
- grok-code-fast-1 — $0.20/$1.50 за M токенов, 160 tok/sec. Доступен в Cursor, Cline, Copilot, opencode. 256K контекст.
- Batch API: image/video generation + JSONL upload (15 марта). Provisioned Throughput для Enterprise (12 марта).

**Кейсы:**

- React-рефакторинг: Grok 15с vs Claude 45с. Разработчик использует Grok для ~75% задач (рутина), Claude для сложной архитектуры.
- 16-агентный Grok 4.20 Heavy: WebGL GLSL шейдер — работает с первой попытки (обычно нужно несколько итераций).
- Паттерн «fast tier»: Grok Code Fast в Cline/opencode для 60–75% рутинных задач; Claude для сложных — экономия ~40% vs одного Claude.

**Оценка:** Возможно позже. grok-code-fast-1 как дешёвый быстрый tier — полезен уже сейчас в Cline/opencode. Но у xAI нет первоклассного CLI-агента уровня Claude Code/Codex; Grok Build сырой, без IDE и GitHub. Ждём результатов ребилда под руководством ex-Cursor лидов к Q3 2026.

## 3. Таблица сравнения

| Инструмент | Новые фичи | Новые кейсы | Влияние | Тесты? |
|---|---|---|---|---|
| Claude Code / Cowork | 1M контекст GA; Agent Teams; 22 Hooks; MCP Elicitation; Auto-Plan; Voice; Dispatch | Соло бизнес-ОС; Jira > prod в терминале; Spotify -90% времени; 90% AI-кода внутри Anthropic | Высокое | Да |
| Codex (OpenAI) | GPT-5.4 + /fast; Playwright Interactive; Codex Security; Субагенты GA; GPT-5.4 mini/nano | WorkOS 85–90% success; Multi-agent оркестрация; NETGEAR security; OpenAI self-bootstrap | Высокое | Да |
| Cursor | Automations; Composer 2 (-86% цена); 30+ плагинов; MCP Apps; JetBrains ACP | Money Forward -20ч/нед; Rippling ops; 80K TS monorepo; Internal security pipeline | Высокое | Да |
| Google AI Studio / Jules | Full-stack vibe coding; Finish Changes GA; Gemini 3.1 Pro; Jules MCP + CI Fixer; Stitch; Gemini CLI v0.34 | 7-бот ночной пайплайн; voice > PR на прогулке; мультиплеер из промпта; Stitch > deploy <1ч | Среднее-высокое | Да |
| xAI (Grok) | Grok 4.20 Multi-Agent API ($2/$6); Cursor лиды наняты; Grok Build CLI; Batch API | React 15с vs 45с; WebGL shader 1st try; fast tier pattern 60–75% рутины | Низкое-среднее | Нет (ждать Q3) |

## 4. Рекомендации на неделю

1. **Настроить Hooks в Claude Code:** создать PreToolUse-блокировку опасных команд (drop table, rm -rf) и PostToolUse авто-запуск prettier/eslint после Edit/Write. Это 15-минутная настройка с постоянной отдачей — детерминированная защита, которую LLM не может обойти. Документация: https://code.claude.com/docs/en/hooks-guide

2. **Протестировать Composer 2 в Cursor на реальном проекте:** переключить модель на Composer 2 Standard ($0.50/M) для повседневных задач (рефакторинг, CRUD, тесты), оставив Claude Opus для планирования. Это снизит расходы в 5–7 раз по сравнению с Composer 1.5 при сравнимом качестве.

3. **Запустить Jules Scheduled Tasks для одного репозитория:** настроить 2–3 ежедневных агента (security audit, dependency updates, TODO resolution). Бесплатный tier покрывает 15 задач/день. Результат: ежедневные PR с улучшениями без ручного инициирования. Документация: https://jules.google/docs/changelog

## Источники

1. Anthropic 1M Context GA — https://claude.com/blog/1m-context-ga
2. Claude Code Hooks Docs — https://code.claude.com/docs/en/hooks-guide
3. Neil Dave — 5 Claude Code Features — https://theneildave.substack.com/p/5-claude-code-features-shipped-in
4. ClaudeFast — Agent Teams Guide — https://claudefa.st/blog/guide/agents/agent-teams
5. OpenAI — Introducing GPT-5.4 — https://openai.com/index/introducing-gpt-5-4/
6. OpenAI — Codex Security — https://openai.com/index/codex-security-now-in-research-preview/
7. Zack Proser — Codex Review 2026 — https://zackproser.com/blog/openai-codex-review-2026
8. Cursor — Automations — https://cursor.com/blog/automations
9. Cursor — Composer 2 — https://cursor.com/blog/composer-2
10. Cursor — Money Forward — https://cursor.com/blog/money-forward
11. TechCrunch — Composer 2 + Kimi — https://techcrunch.com/2026/03/22/cursor-admits-its-new-coding-model-was-built-on-top-of-moonshot-ais-kimi/
12. Google — Full-Stack Vibe Coding — https://blog.google/innovation-and-ai/technology/developers-tools/full-stack-vibe-coding-google-ai-studio/
13. Google — Finish Changes & Outlines — https://developers.googleblog.com/introducing-finish-changes-and-outlines-now-available-in-gemini-code-assist-extensions-on-intellij-and-vs-code/
14. Jules Changelog — https://jules.google/docs/changelog/
15. TechCrunch — xAI Starting Over — https://techcrunch.com/2026/03/13/not-built-right-the-first-time-musks-xai-is-starting-over-again-again/
16. xAI Release Notes — https://docs.x.ai/developers/release-notes
17. Builder.io — Claude Code + Jira — https://www.builder.io/blog/claude-code-with-jira
18. Reddit r/ClaudeCode — Use Cases — https://www.reddit.com/r/ClaudeCode/comments/1rmd5d8/claude_code_use_cases_what_i_actually_do/
19. Forbes — Cursor Dominance — https://www.forbes.com/sites/annatong/2026/03/05/cursor-goes-to-war-for-ai-coding-dominance/
20. Ry Walker — Grok Build — https://rywalker.com/research/grok-build
