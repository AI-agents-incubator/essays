# Agent SDK как платформенный сдвиг: от bash-костылей к нативной оркестрации

## Статус документа

Инсайт, зафиксирован 2026-03-20. Требует исследования и проектирования.

## Контекст

Мы построили работающую автономную агентную организацию на базе:
- `bash loop` (run_book_agent.sh, run_runtime.sh)
- `claude -p` (one-shot CLI вызовы)
- Файловая система как единственный канал коммуникации
- `nohup` как механизм отвязки от UI

Это работает — доказано экспериментом (48 глав книги, 48 runs, 0 остановок). Но это костыльная архитектура.

## Инсайт

Anthropic выпустил **Agent SDK** — Claude Code, вывернутый наизнанку и превращённый в библиотеку. Это не обёртка над API, а полноценный агентный фреймворк с автономным циклом выполнения.

Ключевое: SDK сам крутит loop (prompt → tool_use → execute → result → next). То, что мы делаем вручную через bash, SDK делает нативно.

## Что это меняет

### Проблемы текущей архитектуры

1. **Нет памяти между runs** — каждый `claude -p` начинает с нуля, перечитывает файлы
2. **Нет оркестрации** — один агент за раз, параллельность через отдельные bash-процессы
3. **Нет кастомных инструментов** — только встроенные Read/Write/Bash/Grep
4. **Координация через файлы** — медленно, хрупко, нет типизации
5. **Bash loop как "оркестратор"** — нет error handling, нет retry, нет graceful shutdown

### Что решает Agent SDK

| Проблема | Текущее решение | Agent SDK решение |
|----------|----------------|-------------------|
| Контекст между runs | Перечитываем файлы | Сессии с сохранением |
| Параллельность | Отдельные bash-процессы | Субагенты (async) |
| Кастомные инструменты | Нет | @tool декоратор |
| Координация | Файловая система | Прямая коммуникация |
| Оркестрация | bash while loop | Python async loop |
| Демонизация | nohup + & | systemd / docker |
| Error handling | `|| true` | try/except + retry |

### Что сохраняется

Всё знание, накопленное в экспериментах:
- Pipeline: intake → brief → spec → execution → review
- Принцип: автономность = непрерывный loop, качество вторично
- Принцип: один run = одна задача
- Принцип: агент живёт на уровне ОС, не UI
- Принцип: state-based координация работает
- Scaffold: структура agent_org/, policies, templates

## Архитектурное видение (v2)

```python
# orchestrator.py — ЭТО и есть организация

from claude_agent_sdk import Agent, AgentDefinition, tool, query

# Кастомные инструменты
@tool("check_progress", "Check book writing progress")
async def check_progress(args):
    # Читает PROGRESS.md, возвращает structured data
    ...

@tool("submit_chapter", "Submit completed chapter for review")
async def submit_chapter(args):
    # Коммитит, обновляет прогресс, запускает review
    ...

# Субагенты = роли организации
agents = {
    "product-manager": AgentDefinition(
        description="Создаёт product briefs, определяет scope",
        tools=["Read", "Write", "check_progress"],
        model="sonnet"  # быстрый для планирования
    ),
    "writer": AgentDefinition(
        description="Пишет главы книги",
        tools=["Read", "Write", "submit_chapter"],
        model="opus"  # качественный для контента
    ),
    "reviewer": AgentDefinition(
        description="Проверяет качество, даёт фидбек",
        tools=["Read", "Grep"],
        model="sonnet"
    )
}

# Главный loop — ЭТО оркестратор
async def run_organization():
    while not all_done():
        next_task = get_next_pending()

        # Product manager планирует
        brief = await query("Создай brief для главы X", agent="product-manager")

        # Writer пишет
        result = await query("Напиши главу по этому brief", agent="writer")

        # Reviewer проверяет
        review = await query("Проверь эту главу", agent="reviewer")

        # Если review плохой — writer переписывает
        if review.needs_rework:
            result = await query("Перепиши с учётом фидбека", agent="writer")
```

## Что НЕ нужно делать

- Не переписывать текущую версию — она работает и является baseline
- Не выбрасывать scaffold, policies, templates — они переиспользуемы
- Не начинать без исследования SDK — сначала понять реальные возможности vs маркетинг

## Следующие шаги

1. **Исследование SDK** — установить, попробовать базовые сценарии
2. **PoC** — минимальный оркестратор на SDK, одна задача
3. **Сравнение** — тот же тест (одна глава книги) через bash и через SDK
4. **Решение** — migrate или coexist
5. **Реализация** — в отдельной ветке/worktree

---

*Инсайт зафиксирован: 2026-03-20*
*Источник: информация от Alex о выходе Agent SDK*
