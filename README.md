# essays

Репозиторий с учебными и рабочими материалами по `Codex`, `Claude Code`, code agents, automation-пайплайнам и архитектуре knowledge-систем. Это не одна линейная книга, а несколько связанных контуров: основной учебный курс, инженерные заметки по автоматизации, стратегические мемо и тематические заготовки под будущие разделы.

## Если вы пришли с конкретной проблемой

- Если вы только заходите в тему и не понимаете, с чего начать, откройте [code-agents/README.md](/code-agents/README.md), а затем learning paths в [code-agents/root_docs/README.md](/code-agents/root_docs/README.md).
- Если вы не можете выбрать между `Codex` и `Claude Code`, начните с [playbook 1](/code-agents/playbooks/01-how-to-choose-between-codex-and-claude-code.md), затем посмотрите сравнительные документы в [code-agents/root_docs/README.md](/code-agents/root_docs/README.md).
- Если вам нужен первый безопасный старт без хаоса и лишнего риска, идите в [playbooks](/code-agents/playbooks/README.md), особенно к сценариям про первый обзор проекта и первую маленькую правку.
- Если агент угадывает лишнее, забывает правила или часто требует ручного сопровождения, смотрите материалы про task design, память проекта, настройки и рост автономности в [code-agents/README.md](/code-agents/README.md), а также [claude_code_auto_mode_guide.md](/claude_code_auto_mode_guide.md) и [claude_code_loop_guide.md](/claude_code_loop_guide.md).
- Если вы хотите перевести работу с агентом из разовых удач в repeatable workflows, weekly cycles или team setup, начинайте с [code-agents/playbooks/README.md](/code-agents/playbooks/README.md) и глав 6–9 в книгах внутри [code-agents](/code-agents/README.md).
- Если вам нужен media/knowledge automation pipeline, идите в [automations/README.md](/automations/README.md): там есть кейсы про YouTube-публикацию, Vimeo-миграцию, course generation, semantic indexing и RAG-ready knowledge base.
- Если вы не уверены, нужен ли вам вообще `RAG`, embeddings или векторная база, читайте [beforerag.md](/beforerag.md), [Vectorization_Decision_Framework.md](/Vectorization_Decision_Framework.md) и [automations/semantic_index.md](/automations/semantic_index.md).
- Если вам нужен стратегический слой, а не только инструментальный, идите в [strategy/README.md](/strategy/README.md): там материалы про judgment, moat, сегментацию и выбор направления в эпоху агентов.
- Если вам нужно отслеживать рынок code agents и не терять важные обновления инструментов, используйте [code-agents/reports/README.md](/code-agents/reports/README.md), [code-agents/tooling_watchlist.md](/code-agents/tooling_watchlist.md) и [code-agents/twitter_product_filter.md](/code-agents/twitter_product_filter.md).
- Если вам нужен reference по официальной документации `Claude Code`, откройте [claude_code_docs_map.md](/claude_code_docs_map.md) и [llms.md](/llms.md).
- Если вас интересуют реальные ограничения, sandboxes и передача данных между средами, полезен [EVOLUTION-OF-APPROACH.md](/EVOLUTION-OF-APPROACH.md).

## Карта репозитория

### [code-agents](/code-agents/README.md)

Главный учебно-методический раздел по агентной разработке.

- [code-agents/root_docs/README.md](/code-agents/root_docs/README.md) — быстрые гайды, learning paths, comparisons и reference notes, уже разложенные по кейсам.
- [code-agents/codex-book/README.md](/code-agents/codex-book/README.md) — структурированная книга по `Codex`.
- [code-agents/claude-code-book/README.md](/code-agents/claude-code-book/README.md) — структурированная книга по `Claude Code`.
- [code-agents/playbooks/README.md](/code-agents/playbooks/README.md) — прикладные сценарии работы.
- [code-agents/reports/README.md](/code-agents/reports/README.md) — watchlist-отчеты по инструментам.
- [code-agents/The_Anatomy_of_an_Agent_Harness.md](/code-agents/The_Anatomy_of_an_Agent_Harness.md) — отдельный переводной материал про harness design.

### [automations](/automations/README.md)

Раздел про автоматизацию публикации, миграцию видеоархива и подготовку knowledge base.

- проектирование пайплайнов Vimeo → YouTube;
- AI-генерация метаданных и обложек;
- подготовка видеоархива к RAG;
- semantic indexing большого Markdown-массива.

### [strategy](/strategy/README.md)

Небольшой блок стратегических мемо о том, куда двигаться в эпоху агентных систем, как устроены moat, judgment и контентные/продуктовые направления.

### Технические заготовки

- [Playwright/README.md](/Playwright/README.md) — будущий раздел про браузерную автоматизацию и extraction workflows.
- [SQLite/README.md](/SQLite/README.md) — будущий раздел про local-first storage, FTS и структуру знаний.
- [Supabase/README.md](/Supabase/README.md) — будущий раздел про managed Postgres, storage и backend-интеграции.

### [tools](/tools/README.md)

Небольшой переходный раздел для отдельных импортированных или переводных материалов, которые еще не встроены в основной учебный контур.

## Важные документы в корне

В корне лежат материалы, которые задают общий контекст для нескольких разделов сразу:

- [claude_code_auto_mode_guide.md](/claude_code_auto_mode_guide.md) — guide по Auto Mode в Claude Code.
- [claude_code_loop_guide.md](/claude_code_loop_guide.md) — guide по циклическим задачам и `/loop`.
- [claude_code_docs_map.md](/claude_code_docs_map.md) — карта документации Claude Code.
- [EVOLUTION-OF-APPROACH.md](/EVOLUTION-OF-APPROACH.md) — кейс эволюции extraction pipeline для большого курса.
- [beforerag.md](/beforerag.md) — эссе о том, почему не стоит начинать с RAG слишком рано.
- [Vectorization_Decision_Framework.md](/Vectorization_Decision_Framework.md) — практическая рамка, когда не нужна векторизация, когда хватает open-source, а когда имеет смысл платить.
- [llms.md](/llms.md) — собранная карта официальной документации Claude Code.

## С чего начать

Маршрут зависит от задачи:

1. Если нужен системный вход в code agents, начни с [code-agents/README.md](/code-agents/README.md).
2. Если нужен вход через проблемы и осознаваемые боли, открой [code-agents/root_docs/README.md](/code-agents/root_docs/README.md).
3. Если интересуют automation-конвейеры для контента и knowledge base, переходи в [automations/README.md](/automations/README.md).
4. Если интересует стратегический слой, читай [strategy/README.md](/strategy/README.md).
5. Если задача про data architecture и преждевременный `RAG`, полезно читать вместе [beforerag.md](/beforerag.md), [Vectorization_Decision_Framework.md](/Vectorization_Decision_Framework.md) и [automations/semantic_index.md](/automations/semantic_index.md).

## Служебные файлы

- [manifest.md](/manifest.md) задает тип проекта.
- [AGENTS.md](/AGENTS.md) описывает, где брать проектный манифест.
- [CLAUDE.md](/CLAUDE.md) относится к локальной агентной среде.
- Локальные IDE/workspace-файлы могут существовать рядом с репозиторием, но не являются частью основного контентного индекса.

## Примечание

Названия публичных документов лучше считать стабильными: на часть файлов уже могут ссылаться внешние заметки, документы и публикации.
