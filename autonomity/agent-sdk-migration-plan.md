# План миграции: bash + claude-p → Agent SDK

## Статус: ЧЕРНОВИК (не реализовывать, только план)

Дата: 2026-03-20

## Результаты исследования SDK

Agent SDK — реальный инструмент, не маркетинг. Ключевые возможности подтверждены:

| Возможность | Статус | Практичность |
|-------------|--------|-------------|
| Автономный цикл (query loop) | ✅ Работает | Заменяет наш bash loop |
| Сессии с сохранением контекста | ✅ Работает | Заменяет перечитывание файлов |
| Субагенты | ✅ Работает | Заменяет параллельные nohup процессы |
| Кастомные инструменты (@tool) | ✅ Работает | Новая возможность — нет аналога сейчас |
| Hooks (перехват вызовов) | ✅ Работает | Audit, safety, redirect |
| MCP серверы | ✅ Работает | GitHub, Postgres, HTTP API |
| Демон-режим | ⚠️ Нет нативного | Но обычный Python loop + systemd = то же самое |
| Кросс-машинные сессии | ❌ Нет | Сессии локальные, нужно копировать файлы |

## Что даёт миграция

### Для книжного проекта (текущий тест)

Сейчас:
```bash
# 48 одинаковых вызовов, каждый с нуля
while true; do
    claude -p "Прочитай AUTONOMOUS_MISSION.md..."
done
```

После:
```python
async with ClaudeSDKClient(options=options) as client:
    while pending_chapters():
        chapter = next_pending()
        await client.query(f"Напиши главу {chapter}")
        # Контекст сохраняется! Агент помнит предыдущие главы.
```

**Выигрыш:** Continuity. Агент помнит что уже написал, может ссылаться на предыдущие главы, держать стиль.

### Для агентной организации

Сейчас: один агент делает всё последовательно.

После:
```python
agents = {
    "intake": AgentDefinition(
        description="Нормализует входной запрос",
        tools=["Read", "Write", "mcp__normalize__process"],
        model="sonnet"  # быстрый
    ),
    "planner": AgentDefinition(
        description="Создаёт product brief и task graph",
        tools=["Read", "Write"],
        model="opus"  # умный
    ),
    "executor": AgentDefinition(
        description="Выполняет задачи",
        tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
        model="opus"
    ),
    "reviewer": AgentDefinition(
        description="Проверяет результат",
        tools=["Read", "Grep"],  # только чтение!
        model="sonnet"
    )
}
```

**Выигрыш:** Разделение ролей, разные модели для разных задач, параллельность, ограничение прав (reviewer не может писать).

### Кастомные инструменты — новое измерение

```python
@tool("check_progress", "Показать прогресс написания книги")
async def check_progress(args):
    # Парсит PROGRESS.md, возвращает structured data
    done = count_done()
    pending = count_pending()
    return {"content": [{"type": "text", "text": f"Done: {done}, Pending: {pending}"}]}

@tool("submit_to_review", "Отправить главу на проверку")
async def submit_to_review(args):
    # Коммитит, обновляет статус, запускает review субагента
    git_commit(args["file"])
    update_progress(args["chapter"], "review")
    return {"content": [{"type": "text", "text": "Submitted for review"}]}

@tool("search_drafts", "Найти релевантные черновики автора")
async def search_drafts(args):
    # Семантический поиск по drafts/
    results = search(args["query"], "drafts/")
    return {"content": [{"type": "text", "text": format_results(results)}]}
```

**Выигрыш:** Агент получает инструменты специфичные для задачи, а не generic Read/Write.

## Ограничения SDK (важно!)

1. **Субагенты не могут порождать своих субагентов** — только один уровень вложенности
2. **Сессии локальные** — нельзя перенести на другую машину без копирования файлов
3. **Нет нативного демона** — нужен свой loop + systemd/launchd
4. **bypassPermissions игнорирует allowed_tools** — нужно использовать disallowed_tools
5. **Windows: длинные промпты для субагентов ломаются** (лимит 8191 символов) — не наша проблема (macOS)

## Архитектура v2 (Agent SDK)

```
orchestrator.py (Python, systemd/launchd)
├── intake_agent (sonnet) — нормализация запроса
├── planner_agent (opus) — brief + task graph
├── executor_agent (opus) — выполнение задач
│   └── [кастомные tools: check_progress, submit_chapter, search_drafts]
├── reviewer_agent (sonnet, read-only) — проверка
└── hooks
    ├── PreToolUse: audit log, safety checks
    ├── PostToolUse: progress tracking
    └── Notification: Slack/email alerts
```

Координация: через сессии (контекст сохраняется) + файловая система (state).

## План реализации (5 этапов)

### Этап 0: Установка и проверка (1 час)
- `pip install claude-agent-sdk`
- Минимальный тест: `query("напиши hello world")`
- Убедиться что API ключ работает, всё ставится

### Этап 1: PoC — одна глава книги через SDK (2-3 часа)
- Заменить один вызов `claude -p` на `query()`
- Проверить: пишет? коммитит? обновляет прогресс?
- Сравнить качество с bash-версией

### Этап 2: Loop с сессиями (3-4 часа)
- ClaudeSDKClient с continue_conversation
- Написать 5 глав подряд с сохранением контекста
- Проверить: помнит ли предыдущие главы? держит стиль?

### Этап 3: Субагенты + кастомные tools (1 день)
- Определить 2-3 субагента (writer, reviewer)
- Определить 2-3 кастомных tool (check_progress, submit_chapter)
- Один полный цикл: plan → write → review → fix → commit

### Этап 4: Полный оркестратор (2-3 дня)
- orchestrator.py — полная замена bash loop
- Все роли как субагенты
- Hooks для audit и safety
- Launchd plist для macOS (настоящий демон)
- Тест: написать всю книгу заново через v2

### Этап 5: Distribution v2 (потом)
- Обновить install.sh — установка Python зависимостей
- Обновить scaffold — orchestrator.py вместо run_agent.sh
- Обновить handoff — SDK-native workflow

## Что НЕ менять

- Scaffold (agent_org/ структура) — переиспользуема
- Policies, templates, charter — переиспользуемы
- PROGRESS.md / INBOX.md формат — работает
- Pipeline концепция (intake → brief → spec → execution → review) — работает
- AUTONOMOUS_MISSION.md подход — работает

## Решение: новая ветка, не перезапись

Реализация в отдельной ветке (например `agent-sdk-v2`), не в текущей.
Текущая версия (bash) — рабочий baseline, не трогать.
Сравнение v1 (bash) vs v2 (SDK) на одной задаче — потом решаем.

---

*План составлен: 2026-03-20*
*Статус: черновик, ждёт решения о начале реализации*
