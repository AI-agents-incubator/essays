# Tooling Watchlist — Code & Agents

Еженедельный отчёт · 16-22 марта 2026 · Выпуск #2

## 1. Executive Summary

- **Cursor Composer 2: дешевле на 86%, но скандал с Kimi K2.5.** Cursor выпустил Composer 2 (19 марта) на базе open-source Kimi K2.5 (Moonshot AI) с RL-дообучением. CursorBench 61.3 (бьёт Claude Opus 4.6), цена $0.50/M input Standard. В тот же день обнаружен model ID kimi-k2p5-rl-0317 — Cursor не указал базовую модель. После критики сообщества Cursor признал базу; Moonshot подтвердил авторизованное партнёрство через Fireworks AI.

- **OpenAI приобретает Astral (uv, Ruff, ty) + GPT-5.4 mini/nano.** 19 марта OpenAI объявила о покупке Astral — авторов uv, Ruff и ty, которыми пользуются миллионы Python-разработчиков. Параллельно вышли GPT-5.4 mini (2x быстрее, 30% квоты Codex) и nano ($0.20/M input). Стратегия: встроить Codex во весь жизненный цикл разработки.

- **Claude Code: 6 релизов за неделю + Cowork Dispatch.** Anthropic выпустил v2.1.76-2.1.81 за 6 дней: StopFailure hook, --bare флаг для CI, MCP push-каналы (--channels), видимость rate limits в statusline, -80MB RAM на старте. Cowork Dispatch (17 марта) — управление десктопным агентом с телефона через persistent thread.

- **Google Stitch: «vibe design» обрушил Figma на 7-10%.** Google перезапустил Stitch (18 марта) как AI-дизайн-канвас: бесконечный холст, voice-дизайн, DESIGN.md формат, MCP-сервер для экспорта в Claude Code/Cursor. Акции Figma упали 7-10%. AI Studio получил full-stack vibe coding с Firebase и Next.js.

- **xAI: Grok Computer «скоро» + Grok 4.20 GA.** В коде Grok обнаружен флаг enable_grok_computer — компьютерный агент на базе Grok + Tesla. Маск подтвердил: «скоро». Grok 4.20 вышел из бета (2M контекст, 230 tok/sec, $2/$6). grok-cli v1.0.0-rc3 добавил sub-agents, MCP, Telegram-управление.

## 2. По инструментам

### Claude Code / Cowork (Anthropic)

**Новые фичи:**

- 6 релизов за неделю (v2.1.76 - v2.1.81): StopFailure hook (обработка ошибок API), plugin persistent state, streaming line-by-line, VSCode /remote-control, --console auth, turn duration toggle.
- v2.1.80: rate limits видны в statusline (использование 5-часового и 7-дневного окон), --channels research preview (MCP серверы могут push-ить сообщения в сессию), -80MB RAM на старте для 250K-файловых репо.
- v2.1.81: --bare флаг для headless CI/CD скриптинга (без hooks, LSP, plugins), MCP output collapsing (сворачивание выхода в одну строку).
- v2.1.77: Opus 4.6 output tokens: 64K default / 128K max. Фикс критической уязвимости: PreToolUse hooks с allow обходили deny-правила.
- Cowork Dispatch (17 марта): persistent thread между десктопом и телефоном. Отправляете задачу с iPhone/Android, Claude выполняет на десктопе. Research preview для Max, затем Pro.
- Промо 2x лимитов (13-28 марта): двойные лимиты в off-peak часы для Free/Pro/Max/Team. Бонусное использование НЕ считается против недельных лимитов.

**Кейсы:**

- Rakuten: реализация функции в vLLM (12.5M строк кода) за 7 часов автономной работы, 99.9% числовая точность.
- TELUS: 500,000+ часов сэкономлено, код доставляется на 30% быстрее, 13,000+ внутренних AI-решений.
- Viget: Node.js CLI-менеджер — /debug нашёл root cause (storage.js:24, тихое обрезание описаний >200 символов) без изменений кода; Issue #2: 4 файла, 17 новых тестов, PR — за один промпт.
- Anthropic внутренне: 90% кода — AI-written, 60% работы с AI (было 28% год назад), 60-100 внутренних релизов/день.

**Оценка:** Полезно прямо сейчас — да. --bare флаг для CI и --channels (MCP push) — ключевые для автоматизации. Cowork Dispatch пока research preview с ~50/50 надёжностью, но концепция управления агентом с телефона — практичная для длинных задач. 6 релизов за неделю показывают максимальную скорость итераций среди всех инструментов.

---

### Codex (OpenAI)

**Новые фичи:**

- GPT-5.4 mini (17-18 марта): 2x быстрее предшественника, 400K контекст, 30% квоты Codex (сессии в 3.3x длиннее). API: $0.75/$4.50/M. GPT-5.4 nano: API-only, $0.20/$1.25/M — для классификации и лёгких субагентов.
- Приобретение Astral (19 марта): uv, Ruff и ty входят в экосистему Codex. 2M+ WAU подтверждено, 3x рост пользователей с января 2026. Оценка сделки ~$500M+.
- CLI 0.115.0 (16 марта): full-res image inspection, Python SDK для filesystem RPCs, Smart Approvals с guardian-маршрутизацией, realtime websocket transcription.
- CLI 0.116.0 (19 марта): device-code ChatGPT sign-in, userpromptsubmit hook (перехват промптов), memory citations в сообщениях агента. Регрессия на Debian 12.
- Codex App 26.312: custom themes, revamped Automations (local vs worktree, custom model и reasoning level на автоматизацию, templates).
- Скандал со скоростью (21 марта): пользователи сообщают об эффективном 2x замедлении; /fast режим теперь сжигает кредиты 2x быстрее. Обычная скорость стала «заблокированной за paywall».

**Кейсы:**

- WorkOS: 4-5 параллельных задач обслуживания утром, 85-90% success rate (было 40-60%). 2-3 готовых PR к завтраку.
- Nathan Lambert: GPT-5.4 + /fast + xhigh reasoning как execution-стадия после планирования в Claude Opus. Никогда не попадает в rate limit на $200/мес плане.
- Enterprise RBAC рефакторинг: Express.js auth middleware > role-based access > тесты > self-correct > PR. Ноль ручных вмешательств, +47/-12 строк, 4 теста пройдены.

**Оценка:** Полезно прямо сейчас — да. Приобретение Astral — стратегический шаг: uv/Ruff/ty встроятся в Codex-экосистему. GPT-5.4 mini как субагент-модель — экономичная замена основной модели для рутинных задач. Скандал с /fast (2x кредитов за прежнюю скорость) — серьёзный минус для пользователей Pro-плана.

---

### Cursor

**Новые фичи:**

- Composer 2 (19 марта): собственная модель на базе Kimi K2.5 + RL. CursorBench 61.3 (Composer 1.5: 44.2), Terminal-Bench 61.7 (бьёт Claude Opus ~58). Цена: $0.50/$2.50 Standard (-86% от Composer 1.5). Отдельный пул кредитов от Claude/GPT.
- Compaction-in-the-loop RL: модель учится сжимать собственный контекст до ~1000 токенов при достижении лимита. Это часть обучающего сигнала — многочасовые сессии без деградации.
- Security Automation Templates (16 марта): 4 шаблона из внутренней security-команды Cursor. Agentic Security Review (тысячи PR, сотни предотвращённых проблем), Vuln Hunter, Anybump (автопатч зависимостей), Invariant Sentinel (ежедневный drift-мониторинг).
- Скандал Kimi K2.5 (19-22 марта): разработчик нашёл model ID kimi-k2p5-rl-0317. Moonshot AI подтвердил токенизатор. Лицензия Kimi требует UI-атрибуцию при >$20M/мес выручки; у Cursor ~$2B ARR. Cursor признал базу, назвал отсутствие disclosure «промахом». Moonshot подтвердил легитимность партнёрства.

**Кейсы:**

- Money Forward (1000+ сотрудников): 15-20 часов экономии на инженера/неделю. QA: -70% времени на тест-кейсы (Jira/Notion > Playwright через MCP). Дизайнеры итерируют по live-фронтенду прямо в Cursor.
- Cursor Security: Anybump полностью автоматизировал патчинг зависимостей. Agentic Security Review предотвратил сотни проблем за 2 месяца.
- Разработчик: сложная UI-задача за 1 час (vs 2.5 часа на Gemini 3.1 Pro). SaaS-фича за 5-10 минут (vs 30-45 с Claude). Слабость: 6.4M токенов на модификацию типов переводов — провал.

**Оценка:** Полезно прямо сейчас — да, с оговорками. Composer 2 Standard — лучшее соотношение цена/качество на рынке для повседневных задач. Security templates — бесплатная отправная точка для DevSecOps. Риск: скандал с Kimi подорвал доверие; если Anthropic определит, что K2.5 дистиллирован из Claude, доступ Cursor к Claude может быть ограничен.

---

### Google (AI Studio / Stitch / Jules / Gemini CLI)

**Новые фичи:**

- Google Stitch «vibe design» (18 марта): перезапуск как AI-канвас. Бесконечный холст (5 экранов одновременно), voice-дизайн, DESIGN.md-формат для портативности дизайн-систем, Agent Manager для параллельных направлений, MCP-сервер + SDK, экспорт в AI Studio/Antigravity/Figma/React. Бесплатно: 350 генераций/мес. Акции Figma -7-10%.
- AI Studio full-stack vibe coding (19 марта): Antigravity-агент в Build mode. Firebase auto-provisioning (Firestore + Auth), Secrets Manager, Next.js, автоустановка библиотек (Framer Motion, Shadcn), persistent state между сессиями, мультиплеер.
- Gemini CLI v0.34.0 (17 марта): gVisor sandboxing, LXC контейнеры (экспериментально), tracker CRUD-инструменты, A2A timeout до 30 мин, фикс OOM на длинных сессиях. Plan Mode по умолчанию (из v0.33.0).
- Jules: CI Fixer (авто-цикл fix > commit > resubmit на упавших GitHub Actions), Planning Critic (-9.5% отказов задач), Gemini 3.1 Pro по умолчанию, до 60 параллельных задач на Ultra.
- Antigravity: ценовая реструктуризация сильно урезала квоты Pro ($20/мес). Ultra ($250/мес) теперь необходим для стабильного доступа к продвинутым моделям. Первый официальный Codelab (16 марта).
- Скрытое изменение safety-фильтра в AI Studio: полное удаление ответа при любом триггере (вместо soft stop). >50% ответов удаляются, токены расходуются. Нет официального ответа от Google.

**Кейсы:**

- Gemini CLI + Jules стек: Rust/WebAssembly Mandelbrot-приложение. CLI сгенерировал конфиг ESLint, SonarJS, Dependency Cruiser, Vitest, GitHub Actions. 3 Jules-агента (security, performance, UI) создают ежедневные PR, мерж с телефона.
- Stitch > AI Studio: от дизайна до deploy за 20-25 минут. Извлечение дизайн-системы из URL, 5 экранов одновременно, voice для вариантов, экспорт в AI Studio для кода.
- AI Studio: мультиплеерная 3D-игра Neon Arena из одного промпта (Three.js + WebSocket + Firebase Auth + leaderboard).
- Gemini CLI Plan Mode: миграция БД — CLI читает схему, проверяет GitHub issues, генерирует план, разработчик редактирует inline, затем Flash выполняет.

**Оценка:** Полезно прямо сейчас — да (Stitch + Jules + Gemini CLI Plan Mode). Stitch с DESIGN.md и MCP — первый бесплатный инструмент дизайна, который встраивается в код-пайплайн. Jules CI Fixer по-прежнему лучший бесплатный инструмент для ночных проверок. Минус: ценовая реструктуризация Antigravity и молчание Google по safety-фильтру.

---

### xAI (Grok)

**Новые фичи:**

- Grok 4.20 GA (18 марта): вышел из бета. 2M контекст, 230 tok/sec (быстрее Gemini Flash и GPT-5.4 на output), $2/$6/M. Multi-agent: 4 или 16 агентов через API параметр agent_count.
- enable_grok_computer (22 марта): флаг обнаружен в коде Grok. Маск: «Coming out soon». Совместная разработка с Tesla (проект Macrohard). Компьютерный агент: Grok рассуждает, агент управляет экраном/клавиатурой/мышью.
- grok-cli v1.0.0-rc3 (22 марта): open-source терминальный агент. Sub-agents по умолчанию, MCP, headless JSON (CI), Telegram remote control. Дефолтная модель: grok-code-fast-1.
- Grok Build (18 марта): локальный open-source агент, 8 параллельных агентов (Planner, Search, Coder, Reviewer, Tester). Нет облачных зависимостей, нет API-затрат.
- Provisioned Throughput (12 марта, adoption 16-17): $10/unit/day, SLA 99.9%. grok-4-1-fast-reasoning: 31,500 input TPM/unit.
- Collections API (активен на неделе): встроенный RAG — до 100K файлов / 100GB. DeepCodeBench: 86% (Gemini Pro 3: 85%, GPT-5.1: 81%). $2.50/1000 поисков.
- Найм с Wall Street (17 марта): трейдеры, банкиры, кредитные аналитики для обучения Grok финансовому моделированию.

**Кейсы:**

- grok-code-fast-1 в Copilot Free: автоматический выбор в VS Code/JetBrains/Xcode. 70.8% SWE-Bench, 92 tok/sec, 256K контекст, >90% prompt cache hit.
- Grok 4.20 multi-agent (16 агентов): высокая производительность на tau2-Bench (69.6%). Потребляет значительно больше токенов.
- grok-cli: headless JSON output для CI, Telegram remote control для длительных задач, sub-agents по умолчанию.

**Оценка:** Возможно позже (Grok Computer, Grok Build) / уже полезно (grok-code-fast-1 как fast tier). enable_grok_computer — самый интригующий анонс недели, но до релиза — неизвестно. grok-cli с Telegram-управлением — интересная альтернатива для CI/CD. Основной gap: Claude Sonnet 5 чинит баги в 1.6x быстрее и на 56% дешевле. Ждём результатов ребилда к Q3.

---

## 3. Таблица сравнения

| Инструмент | Новые фичи | Новые кейсы | Влияние | Тесты? |
|---|---|---|---|---|
| Claude Code / Cowork | 6 релизов (v2.1.76-81); --bare CI; --channels MCP push; Dispatch; 2x лимиты промо | Rakuten 99.9% точность; TELUS 500K+ часов; Viget debug в 1 промпт; 90% AI-кода Anthropic | Высокое | Да |
| Codex (OpenAI) | GPT-5.4 mini/nano; Astral (uv/Ruff/ty); CLI 0.115-0.116; Automations revamp; /fast скандал | WorkOS 85-90% success; RBAC auto-refactor; Claude+Codex 2-model workflow | Высокое | Да |
| Cursor | Composer 2 (-86% цена, Kimi K2.5 база); Security Templates (4 шт.); Kimi скандал | Money Forward -20ч/нед; Security auto-patch; UI задача 1ч vs 2.5ч; 6.4M токенов fail | Высокое | Да |
| Google (AI Studio / Stitch / Jules) | Stitch vibe design + MCP; AI Studio full-stack; Gemini CLI v0.34; Jules CI Fixer; Safety-фильтр проблема | Gemini CLI+Jules стек; Stitch > deploy 20 мин; Neon Arena мультиплеер; Plan Mode миграции | Среднее-высокое | Да (Stitch) |
| xAI (Grok) | Grok 4.20 GA; enable_grok_computer; grok-cli rc3; Grok Build local; Collections RAG | grok-code-fast-1 в Copilot; 16-agent research; grok-cli CI+Telegram | Среднее | Нет (ждать) |

## 4. Рекомендации на неделю

1. **Протестировать Google Stitch для нового проекта:** импортировать дизайн-систему из существующего сайта через URL, сгенерировать 5 экранов, экспортировать DESIGN.md в Claude Code или Cursor через MCP. Это бесплатно (350 генераций/мес) и потенциально заменяет ручной дизайн-этап. Документация: https://stitch.withgoogle.com

2. **Настроить Claude Code --bare для CI/CD пайплайна:** создать headless скрипт, который запускает Claude Code без hooks/LSP/plugins для автоматизированного code review или test generation в GitHub Actions. --bare + ANTHROPIC_API_KEY — чистый CI без побочных эффектов. Документация: https://code.claude.com/docs/en/cli-reference

3. **Начать использовать GPT-5.4 mini как модель субагентов в Codex:** переключить exploration-задачи и code review на GPT-5.4 mini (30% квоты, 2x скорость). Оставить GPT-5.4 для планирования и архитектурных решений. Команда: `codex --model gpt-5.4-mini`

## Источники

1. Releasebot — Claude Code v2.1.76-81 — https://releasebot.io/updates/anthropic/claude-code
2. Anthropic — Release Notes / Dispatch — https://support.claude.com/en/articles/12138966-release-notes
3. Forbes — Claude Dispatch — https://www.forbes.com/sites/ronschmelzer/2026/03/20/claude-dispatch-lets-you-control-claude-cowork-with-your-phone/
4. Neil Dave — 5 Claude Code Features — https://theneildave.substack.com/p/5-claude-code-features-shipped-in
5. Anthropic 2026 Agentic Coding Report — https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf
6. Viget — Using Claude Code Intentionally — https://www.viget.com/articles/using-claude-code-intentionally
7. OpenAI — GPT-5.4 mini и nano — https://community.openai.com/t/introducing-gpt-5-4-mini-and-nano-our-most-capable-small-models-yet/1377015
8. OpenAI — Acquiring Astral — https://openai.com/index/openai-to-acquire-astral/
9. CNBC — OpenAI Astral acquisition — https://www.cnbc.com/2026/03/19/openai-to-acquire-developer-tooling-startup-astral.html
10. OpenAI Codex Changelog (CLI 0.115-0.116) — https://developers.openai.com/codex/changelog/
11. Zack Proser — Codex Review 2026 — https://zackproser.com/blog/openai-codex-review-2026
12. Nathan Lambert — GPT-5.4 for Codex — https://www.interconnects.ai/p/gpt-54-is-a-big-step-for-codex
13. Cursor — Composer 2 — https://cursor.com/blog/composer-2
14. Cursor — Security Agents — https://cursor.com/blog/security-agents
15. Cursor — Money Forward — https://cursor.com/blog/money-forward
16. VentureBeat — Composer 2 vs Opus — https://venturebeat.com/technology/cursors-new-coding-model-composer-2-is-here-it-beats-claude-opus-4-6-but
17. Hacker News — Kimi K2.5 скандал — https://news.ycombinator.com/item?id=47452404
18. Google Blog — Stitch vibe design — https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/
19. Google Blog — AI Studio full-stack — https://blog.google/innovation-and-ai/technology/developers-tools/full-stack-vibe-coding-google-ai-studio/
20. Gemini CLI Changelog v0.34.0 — https://geminicli.com/docs/changelogs/
21. Jules Changelog — https://jules.google/docs/changelog/
22. DEV Community — Gemini CLI + Jules stack — https://dev.to/rowan_m/gemini-cli-and-jules-my-march-2026-stack-4146
23. The AI Corner — Google Stitch guide — https://www.the-ai-corner.com/p/google-stitch-ai-design-tool-guide-2026
24. xAI Release Notes — https://docs.x.ai/developers/release-notes
25. TechFlow — Grok Computer flag — https://www.techflowpost.com/en-US/newsletter/117513
26. GitHub — grok-cli v1.0.0-rc3 — https://github.com/superagent-ai/grok-cli
27. TechCrunch — xAI Starting Over — https://techcrunch.com/2026/03/13/not-built-right-the-first-time-musks-xai-is-starting-over-again-again/
28. Business Insider — Figma stock sinks — https://www.businessinsider.com/figma-stock-sinks-google-vibe-design-stitch-ai-tool-2026-3
