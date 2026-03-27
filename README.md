# essays

Репозиторий содержит материалы по `Codex`, `Claude Code`, AI-assisted разработке, automation-пайплайнам и построению knowledge-систем поверх текстов и видеоархивов.

Сейчас он организован не как одна книга, а как несколько смысловых зон:

- основной учебно-методический контур по code agents;
- отдельный automation-раздел про медиа- и knowledge-пайплайны;
- набор root-level reference-документов и обзорных заметок.

## Основные разделы

### 1. Code Agents

Главный контентный блок находится в [code-agents/README.md](/Users/alexeykrolmini/Code/essays/code-agents/README.md).

Что там лежит:

- [code-agents/root_docs](/Users/alexeykrolmini/Code/essays/code-agents/root_docs) — guides, explainers, comparisons, learning paths и reference notes.
- [code-agents/codex-book/README.md](/Users/alexeykrolmini/Code/essays/code-agents/codex-book/README.md) — книга по `Codex`.
- [code-agents/claude-code-book/README.md](/Users/alexeykrolmini/Code/essays/code-agents/claude-code-book/README.md) — книга по `Claude Code`.
- [code-agents/playbooks/README.md](/Users/alexeykrolmini/Code/essays/code-agents/playbooks/README.md) — прикладные пошаговые сценарии.
- [code-agents/reports/README.md](/Users/alexeykrolmini/Code/essays/code-agents/reports/README.md) — weekly watchlist reports.
- [code-agents/tooling_watchlist.md](/Users/alexeykrolmini/Code/essays/code-agents/tooling_watchlist.md) — спецификация мониторинга инструментов для кода и агентных систем.
- [code-agents/twitter_product_filter.md](/Users/alexeykrolmini/Code/essays/code-agents/twitter_product_filter.md) — фильтр продуктовых сигналов из X/Twitter.

### 2. Automations

Отдельный automation-раздел находится в [automations/README.md](/Users/alexeykrolmini/Code/essays/automations/README.md).

Что там лежит:

- [automations/video-youtube.md](/Users/alexeykrolmini/Code/essays/automations/video-youtube.md) — дизайн автоматической публикации видео на YouTube.
- [automations/vimeo-migration.md](/Users/alexeykrolmini/Code/essays/automations/vimeo-migration.md) — high-level roadmap миграции Vimeo-архива.
- [automations/vimeo-youtube.md](/Users/alexeykrolmini/Code/essays/automations/vimeo-youtube.md) — детальный Vimeo → YouTube transport pipeline.
- [automations/RAGprepare.md](/Users/alexeykrolmini/Code/essays/automations/RAGprepare.md) — подготовка видеоархива к RAG-ready knowledge base.
- [automations/semantic_index.md](/Users/alexeykrolmini/Code/essays/automations/semantic_index.md) — семантический индекс и инвентаризация большого Markdown-архива.

### 3. Root-Level Guides And Notes

В корне лежат отдельные документы, которые не являются частью книг или playbooks, но задают важный контекст:

- [claude_code_auto_mode_guide.md](/Users/alexeykrolmini/Code/essays/claude_code_auto_mode_guide.md) — подробный guide по Claude Code Auto Mode.
- [claude_code_loop_guide.md](/Users/alexeykrolmini/Code/essays/claude_code_loop_guide.md) — guide по `/loop` и циклическим задачам в Claude Code.
- [claude_code_docs_map.md](/Users/alexeykrolmini/Code/essays/claude_code_docs_map.md) — auto-generated карта документации Claude Code.
- [EVOLUTION-OF-APPROACH.md](/Users/alexeykrolmini/Code/essays/EVOLUTION-OF-APPROACH.md) — разбор эволюции pipeline: от ручного парсинга к параллельной автоматизации.
- [beforerag.md](/Users/alexeykrolmini/Code/essays/beforerag.md) — essay про SQLite-first подход, структуру данных и преждевременный RAG.
- [llms.md](/Users/alexeykrolmini/Code/essays/llms.md) — ссылочный список по документации Claude Code.

## Дополнительные тематические директории

В корне также присутствуют тематические каталоги:

- [Playwright](/Users/alexeykrolmini/Code/essays/Playwright)
- [SQLite](/Users/alexeykrolmini/Code/essays/SQLite)
- [Supabase](/Users/alexeykrolmini/Code/essays/Supabase)

Сейчас они выглядят как отдельные рабочие пространства или заготовки под будущие материалы.

## Start Here

Если нужен быстрый маршрут по репозиторию:

1. Начни с [code-agents/README.md](/Users/alexeykrolmini/Code/essays/code-agents/README.md), если интересуют книги, guides и playbooks по code agents.
2. Открой [automations/README.md](/Users/alexeykrolmini/Code/essays/automations/README.md), если интересуют media/knowledge automation pipelines.
3. Прочитай [claude_code_auto_mode_guide.md](/Users/alexeykrolmini/Code/essays/claude_code_auto_mode_guide.md) и [claude_code_loop_guide.md](/Users/alexeykrolmini/Code/essays/claude_code_loop_guide.md), если нужен быстрый вход в новые возможности Claude Code.
4. Используй [claude_code_docs_map.md](/Users/alexeykrolmini/Code/essays/claude_code_docs_map.md), если нужен полный обзор официальной документации.
5. Перейди к [beforerag.md](/Users/alexeykrolmini/Code/essays/beforerag.md) и [automations/semantic_index.md](/Users/alexeykrolmini/Code/essays/automations/semantic_index.md), если интересует knowledge-инженерия и semantic indexing.

## Repo Notes

- [CLAUDE.md](/Users/alexeykrolmini/Code/essays/CLAUDE.md) и [`.claude/settings.local.json`](/Users/alexeykrolmini/Code/essays/.claude/settings.local.json) относятся к локальной среде и правилам работы агента.
- Названия публичных файлов лучше считать стабильными, если на них уже ссылаются внешние материалы.
