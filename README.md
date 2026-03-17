# essays

Репозиторий с текстовыми материалами про ИИ, агентные системы, современную практику разработки, а также локальными и авторскими материалами по Claude Code и Codex. Основной контент хранится в markdown-документах.

Крупные `process`-файлы и сравнительные гайды в этом репозитории содержат в начале блока версию локального файла и дату актуальности источников. Если у внешней документации нет явного номера версии страницы, практическим эквивалентом версии считается дата проверки.

## Документы

- [README.md](./README.md) — индекс репозитория и краткое описание материалов.
- [agent_operating_system.md](./agent_operating_system.md) — короткий методологический конспект про переход `Ad hoc -> ТЗ -> Agent Operating System`. Внутри: три уровня зрелости работы с агентом, их задачи, ограничения и практический смысл проектных файлов правил и настроек.
- [agent_organization.md](./agent_organization.md) — продолжение методологической модели: переход от одного автономного агента к мультиагентной организации. Внутри: класс задач, которые требуют такой системы, роли виртуальной компании, вертикальная и горизонтальная коммуникация, общая шина, артефакты, эскалация и организационная агентность.
- [agent_organization_design.md](./agent_organization_design.md) — развёрнутая проектная спецификация агентной организации. Внутри: точный состав артефактов, их функции, связи между ними, рекомендуемая файловая структура, ownership ролей и полный циклический контур работы.
- [agent_organization_self_learning.md](./agent_organization_self_learning.md) — методология самообучения агентной организации. Внутри: внешний и внутренний циклы, golden tasks, benchmark-suite, process audit, controlled change, risk of reward hacking и контур эволюции самой архитектуры.
- [agent_org_tz_core.md](./agent_org_tz_core.md) — инвариантное ядро технического задания для всей инфраструктуры агентной организации. Внутри: единое source of truth, правило изоляции runtime-песочниц, общий состав артефактов, benchmark, learning-контур и критерии сравнения.
- [agent_org_tz_codex.md](./agent_org_tz_codex.md) — runtime-addendum для `Codex`. Внутри: только Codex-specific способ исполнения общего ядра, write scope, runtime-файлы, execution trace и evaluation trace.
- [agent_org_tz_claudecode.md](./agent_org_tz_claudecode.md) — runtime-addendum для `Claude Code`. Внутри: только Claude Code-specific способ исполнения общего ядра, write scope, runtime-файлы, execution trace и evaluation trace.
- [core/README.md](./core/README.md) — каталог общего source of truth для эксперимента. Внутри: benchmark templates, expected results и общие evaluation criteria.
- [runtimes/README.md](./runtimes/README.md) — каталог двух независимых execution-sandbox для `Codex` и `Claude Code`.
- [comparison/README.md](./comparison/README.md) — каталог для сравнительной оценки двух реализаций.
- [core/benchmarks/GT-001-bootstrap-runtime-sandbox.md](./core/benchmarks/GT-001-bootstrap-runtime-sandbox.md) — первая canonical golden task. Она проверяет, может ли runtime развернуть внутри своей песочницы минимально рабочую инфраструктуру агентной организации и оставить benchmark plus learning trace.
- [core/expected_results/GT-001-expected_result.md](./core/expected_results/GT-001-expected_result.md) — expected result signature для `GT-001`.
- [runtimes/codex/runs/RUN-001_GT-001_launch_brief.md](./runtimes/codex/runs/RUN-001_GT-001_launch_brief.md) — первый подготовленный launch-brief для запуска `Codex` в собственной sandbox.
- [VibeCoding.md](./VibeCoding.md) — большой аналитический отчет о феномене vibe coding в 2025-2026 годах. Внутри: сообщества и платформы, Discord-экосистемы, Twitter/X, Reddit, Telegram, события в Bay Area, стек инструментов, риски и стратегические рекомендации.
- [claudecode_process_1.md](./claudecode_process_1.md) — большой рабочий документ про то, как превращать ИИ из чата в управляемую систему. Внутри: оркестратор, skills, субагенты, tools, user flow, ТЗ, data contract, SQLite, Supabase, deploy, Playwright, тезаурус, а также большой блок про Claude Code, агентные пайплайны и примеры конфигураций.
- [claudecode-precess_2.md](./claudecode-precess_2.md) — более структурированный гайд по Claude Code на базе официальной документации Anthropic. Внутри: settings, приоритеты настроек, subagents, skills, `CLAUDE.md`, rules, tools, permissions, hooks, sandbox, MCP, headless/SDK/GitHub Actions, browser automation и security practices.
- [codex_process_1.md](./codex_process_1.md) — практический гайд по актуальному устройству Codex на базе официальной документации OpenAI. Внутри: subagents, skills, tools, MCP, `AGENTS.md`, `config.toml`, approval policy, sandbox, веб-доступ, automations и набор официальных ссылок для дальнейшего изучения.
- [cc_managment.md](./cc_managment.md) — структурированный прикладной гайд по устройству и настройке `Claude Code`. Внутри: `settings.json`, `CLAUDE.md`, permissions, hooks, skills, subagents, архитектурные схемы и рекомендуемая конфигурация для безопасной автономной работы.
- [cc_managment_readme.md](./cc_managment_readme.md) — короткая входная версия к гайду по `Claude Code`. Подходит как быстрый onboarding перед чтением полного документа.
- [codex_managment.md](./codex_managment.md) — структурированный прикладной гайд по устройству и настройке `Codex`. Внутри: `config.toml`, `AGENTS.md`, skills, subagents, rules, sandbox, MCP, automations, `exec`, `SDK` и архитектурные схемы.
- [codex_managment_readme.md](./codex_managment_readme.md) — короткая входная версия к гайду по `Codex`. Подходит как быстрый обзор перед чтением полного документа.
- [claudecode_vs_codex.md](./claudecode_vs_codex.md) — расширенный сравнительный документ по Claude Code и Codex на базе двух Claude Code гайдов и одного Codex гайда. Внутри: краткая аннотация для неразработчиков, платформенное сравнение, сравнение практических сценариев, простые правила выбора и тезаурус терминов.
- [claudecode_vs_codex2.md](./claudecode_vs_codex2.md) — альтернативный практический взгляд на сравнение Claude Code и Codex. Внутри: акцент не на списке функций, а на поведении в длинной работе, роли `Codex -> Claude Code -> Codex`, оговорки про зрелость обоих инструментов и рабочий, а не абсолютный характер такого разделения.
- [Use Claude Code Desktop.md](./Use%20Claude%20Code%20Desktop.md) — локальная копия документации по работе с Claude Code Desktop. Внутри: сессии, diff review, preview, PR monitoring, parallel worktrees, scheduled tasks, connectors и работа в local, SSH и cloud окружениях.
- [Claude Code settings.md](./Claude%20Code%20settings.md) — локальная копия документации по настройкам Claude Code. Внутри: configuration scopes, `settings.json`, managed settings, переменные окружения, приоритеты конфигурации и файловая структура настроек.
- [Configure permissions.md](./Configure%20permissions.md) — локальная копия документации по системе разрешений Claude Code. Внутри: permission modes, allow/ask/deny rules, синтаксис правил, wildcard-паттерны, managed policies и ограничения bypass-режима.

## Как читать

- Если нужен быстрый обзор репозитория, начните с этого файла.
- Если нужен самый короткий методологический вход в тему, начните с [agent_operating_system.md](./agent_operating_system.md).
- Если нужен следующий уровень после `Agent Operating System`, читайте [agent_organization.md](./agent_organization.md).
- Если нужен уже не обзор, а точная конструкция агентной организации как системы артефактов, читайте [agent_organization_design.md](./agent_organization_design.md).
- Если нужен контур самообучения, benchmark-логика и golden tasks для агентной организации, читайте [agent_organization_self_learning.md](./agent_organization_self_learning.md).
- Если нужен единый source of truth для будущих двух реализаций, читайте [agent_org_tz_core.md](./agent_org_tz_core.md).
- Если нужен runtime-specific brief для `Codex`, читайте [agent_org_tz_codex.md](./agent_org_tz_codex.md).
- Если нужен runtime-specific brief для `Claude Code`, читайте [agent_org_tz_claudecode.md](./agent_org_tz_claudecode.md).
- Если нужен уже не только документ, а каркас эксперимента с общим ядром, изолированными песочницами и полем сравнения, начните с [core/README.md](./core/README.md), затем [runtimes/README.md](./runtimes/README.md) и [comparison/README.md](./comparison/README.md).
- Если нужен первый реальный benchmark, начните с [core/benchmarks/GT-001-bootstrap-runtime-sandbox.md](./core/benchmarks/GT-001-bootstrap-runtime-sandbox.md), затем смотрите [core/expected_results/GT-001-expected_result.md](./core/expected_results/GT-001-expected_result.md).
- Если нужен уже готовый пакет для первого запуска в `Codex`, откройте [runtimes/codex/runs/RUN-001_GT-001_launch_brief.md](./runtimes/codex/runs/RUN-001_GT-001_launch_brief.md).
- Если нужен обзор экосистемы и культурного контекста вокруг AI-assisted разработки, читайте [VibeCoding.md](./VibeCoding.md).
- Если нужен методологический и прикладной материал по агентной работе с ИИ и Claude Code, читайте [claudecode_process_1.md](./claudecode_process_1.md).
- Если нужен более системный и официальный разбор самого устройства Claude Code, читайте [claudecode-precess_2.md](./claudecode-precess_2.md).
- Если нужен отдельный актуальный разбор устройства Codex и его механизмов управления, читайте [codex_process_1.md](./codex_process_1.md).
- Если нужен самый прикладной и структурированный гайд по устройству Claude Code, читайте [cc_managment.md](./cc_managment.md); для быстрого входа используйте [cc_managment_readme.md](./cc_managment_readme.md).
- Если нужен самый прикладной и структурированный гайд по устройству Codex, читайте [codex_managment.md](./codex_managment.md); для быстрого входа используйте [codex_managment_readme.md](./codex_managment_readme.md).
- Если нужен прямой и понятный неразработчику выбор между двумя агентами по функциям, ограничениям и типам кейсов, читайте [claudecode_vs_codex.md](./claudecode_vs_codex.md).
- Если нужен дополнительный практический угол зрения на распределение ролей между двумя агентами, читайте [claudecode_vs_codex2.md](./claudecode_vs_codex2.md).
- Если нужен практический справочник по самому Claude Code, начните с [Use Claude Code Desktop.md](./Use%20Claude%20Code%20Desktop.md), затем переходите к [Claude Code settings.md](./Claude%20Code%20settings.md) и [Configure permissions.md](./Configure%20permissions.md).
