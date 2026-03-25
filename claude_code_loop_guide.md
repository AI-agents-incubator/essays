# Claude Code `/loop` — Полное руководство
### Циклические задачи для анализа, исследований и создания контента

> **Версия:** Claude Code v2.1.72+ (март 2026)  
> **Аудитория:** Создатели контента, исследователи, предприниматели — без фокуса на программирование

---

## Содержание

1. [Что такое `/loop` и как это работает](#1-что-такое-loop-и-как-это-работает)
2. [Три режима scheduling](#2-три-режима-scheduling)
3. [Синтаксис и команды](#3-синтаксис-и-команды)
4. [Технические ограничения](#4-технические-ограничения)
5. [10 практических кейсов](#5-10-практических-кейсов)
6. [Паттерны построения задач](#6-паттерны-построения-задач)
7. [Интеграция с внешними сервисами](#7-интеграция-с-внешними-сервисами)
8. [Сравнение: `/loop` vs альтернативы](#8-сравнение-loop-vs-альтернативы)

---

## 1. Что такое `/loop` и как это работает

`/loop` — это встроенный skill в Claude Code, который позволяет запускать любой промпт автоматически по расписанию, пока сессия открыта. По сути, это способ превратить Claude из интерактивного ассистента в **фонового рабочего агента**.

### Принцип работы

Когда ты вводишь `/loop 5m проверь логи`, Claude:
1. Парсит интервал (`5m` → каждые 5 минут)
2. Конвертирует в cron-выражение (`*/5 * * * *`)
3. Регистрирует задачу с уникальным 8-символьным ID
4. Подтверждает расписание и ID в терминале
5. Запускает задачу в фоне между твоими ответами

Задачи выполняются **между твоими turns** — Claude не прервёт текущий ответ ради scheduled задачи. Если он занят — задача встаёт в очередь и выполняется как только освобождается.

### Что Claude может делать в задаче

- Искать в вебе (web search встроен)
- Читать и записывать файлы на твоём диске
- Вызывать другие skills и slash-команды
- Взаимодействовать с подключёнными MCP-серверами (Notion, n8n, Gmail и др.)
- Делать HTTP-запросы к API

---

## 2. Три режима scheduling

Важно понимать разницу между тремя вариантами — они решают разные задачи.

| Режим | Где работает | Персистентность | Лучше для |
|-------|-------------|-----------------|-----------|
| **`/loop` в CLI** | Терминал | Только пока сессия открыта (макс. 3 дня) | Быстрый polling во время активной работы |
| **Desktop scheduled tasks** | Claude Desktop app | Переживает рестарты, пока приложение открыто | Ежедневная/еженедельная автоматизация |
| **Cloud scheduled tasks** | Серверы Anthropic | Полностью автономно, машина может быть выключена | Production-уровень, always-on агенты |

### Когда что использовать

**`/loop` в CLI** — если ты сейчас работаешь в сессии и хочешь, чтобы Claude параллельно что-то мониторил. Например, исследуешь один аспект вручную, а Claude в фоне обрабатывает остальные девять.

**Desktop tasks** — для регулярных задач, которые нужны каждый день. Утренний дайджест, еженедельный отчёт, мониторинг конкурентов. Машина должна быть включена.

**Cloud tasks** — самый мощный вариант. Подключаешь репозиторий или MCP-серверы, задаёшь расписание — Claude просыпается на серверах Anthropic и выполняет задачу независимо от твоего устройства.

---

## 3. Синтаксис и команды

### Базовый синтаксис

```
/loop [интервал] [промпт]
```

Интервал опционален (по умолчанию 10 минут). Может стоять в начале или в конце.

```bash
# Интервал в начале
/loop 30m проверь новые публикации по теме AI mentoring

# Интервал в конце
собери упоминания бренда за последний час /loop 1h

# Без интервала (каждые 10 минут по умолчанию)
/loop проверь статус деплоя
```

### Единицы времени

| Символ | Значение | Примечание |
|--------|----------|------------|
| `s` | секунды | Округляется до 1 минуты |
| `m` | минуты | Минимум 1m |
| `h` | часы | |
| `d` | дни | |

Нестандартные интервалы (7m, 90m) округляются до ближайшего чистого — Claude сообщит что выбрал.

### Управление задачами

```bash
# Посмотреть все активные задачи
покажи все запущенные cron задачи

# Отменить конкретную задачу по ID
отмени задачу c21d95a0

# Отменить все задачи
отмени все scheduled задачи

# Одноразовое напоминание (не recurring)
напомни мне через 2 часа проверить результаты экспорта
```

### Вызов skills внутри loop

```bash
# Если у тебя есть кастомный skill /research-topic
/loop 0s /research-topic "habit formation in e-learning"

# Skill запускается по расписанию как будто ты сам его вызвал
```

---

## 4. Технические ограничения

Знать ограничения важно, чтобы не строить на `/loop` то, что он не потянет.

### Жёсткие ограничения

- **Сессионность:** Все задачи умирают при закрытии терминала. Нет recovery, нет catchup.
- **Срок жизни:** Recurring задачи автоматически удаляются через **3 дня**. Задача срабатывает последний раз и самоудаляется.
- **Максимум задач:** 50 на сессию.
- **Параллельность:** Задачи выполняются **последовательно**, не параллельно. Если Claude занят — следующая ждёт.
- **Минимальный интервал:** 1 минута (cron-ограничение).

### Практические следствия

**Нет параллельности** — для 10 аспектов исследования задачи будут выполняться одна за другой. Если каждая занимает 5 минут, 10 аспектов = ~50 минут. Это нормально, но нужно планировать.

**Нет catchup** — если задача должна была сработать в 14:00, а Claude был занят до 14:07, она сработает в 14:07 один раз, а не семь.

**Контекстное окно растёт** — при длинных сессиях с множеством задач контекст накапливается. Для многочасовых сессий рекомендуется периодически компактировать контекст (`/compact`).

---

## 5. Десять практических кейсов

### 🔍 Анализ и мониторинг

---

#### Кейс 1. Мониторинг конкурентов

**Задача:** Автоматически отслеживать новые публикации, продукты и изменения на сайтах конкурентов без ручного мониторинга.

**Промпт:**
```
/loop 6h Visit [competitor1.com/blog] and [competitor2.com]. 
Check for any new articles, product announcements, or pricing changes 
published since the last check. 
Compare with the previous findings in ./intel/competitors.md.
Append only NEW items with today's date and a brief summary.
If nothing new — write "No changes at [time]".
```

**Как это работает:**
Claude открывает страницы каждые 6 часов, сравнивает с предыдущим состоянием из файла, дописывает только новое. Утром ты видишь чистый лог изменений.

**Что получаешь на выходе (`./intel/competitors.md`):**
```markdown
## 2026-03-25 09:00
- competitor1.com: Новая статья "10 способов автоматизации обучения"
- competitor2.com: Изменена страница цен — добавлен Enterprise план от $299/мес

## 2026-03-25 15:00
No changes at 15:00
```

**Вариации:** Мониторить вакансии конкурентов (показывает в каком направлении растут), отслеживать изменения в публичных роадмапах, следить за активностью в их блогах.

---

#### Кейс 2. Трекинг упоминаний ниши

**Задача:** Радар по ключевым темам и трендам в твоей области — без ручного Feedly, Twitter и Google.

**Промпт:**
```
/loop 12h Search the web for new publications about "AI mentoring", 
"personalized learning systems", and "educational AI agents" 
from the last 12 hours.

For each relevant result:
- Title and source
- 2-sentence summary
- Relevance score 1-10 (10 = directly about my niche)
- Key insight or quote

Filter: only include items with score 7+.
Append to ./research/mentions.md with timestamp.
```

**Почему это работает лучше ручного мониторинга:** Claude не просто агрегирует — он оценивает релевантность и фильтрует шум. Ты получаешь только то, что реально важно.

---

#### Кейс 3. Анализ трендов по неделям

**Задача:** Еженедельный snapshot того, что растёт в твоей нише — для планирования контента и продукта.

**Промпт:**
```
/loop 7d Today is [date]. Search for:
1. Top 5 growing topics in "online education" and "AI tools for creators" this week
2. Any viral content or discussions in these areas
3. Emerging terminology or concepts appearing for the first time

For each trend: describe it, estimate growth signal (mentions, engagement), 
explain why it's growing, and suggest one content angle for my audience.

Save to ./trends/week_[date].md
```

**Результат:** Еженедельный intelligence-отчёт, который заменяет часы ручного скроллинга и превращается в контент-план.

---

### 📚 Исследования для курса

---

#### Кейс 4. Последовательное исследование 10 аспектов

**Задача:** Создать исследовательскую базу для курса — каждый аспект глубоко проработан, без ручного участия.

**Архитектура:** Запускаешь 10 задач с `0s` интервалом (немедленно, одна за другой). Claude обрабатывает их последовательно.

**Промпты:**
```bash
/loop 0s Research ASPECT 1: Psychology of motivation in self-directed learning.
Cover: key theories (SDT, expectancy-value), common failure points, 
what actually works based on research, practical interventions.
Write structured report with headers to ./course/aspect_01_motivation.md
Mark file as [DONE] when complete.

/loop 0s Research ASPECT 2: Habit formation for online learners.
Cover: habit loop mechanics, implementation intentions, 
why online courses fail at habit building, proven frameworks.
Write to ./course/aspect_02_habits.md
```

...и так для всех 10.

**Важный приём — файл-очередь:**

Создай `./course/aspects_queue.txt`:
```
PENDING: Psychology of motivation
PENDING: Habit formation
PENDING: Spaced repetition
...
```

И один цикличный промпт:
```
/loop 15m Take the first PENDING item from ./course/aspects_queue.txt.
Research it deeply using web search. Write a structured report to 
./course/[aspect_name].md. Mark item as DONE in the queue file.
If no PENDING items remain, cancel this task.
```

Claude сам управляет очередью.

---

#### Кейс 5. Fact-checking банка утверждений

**Задача:** У тебя есть список тезисов для курса. Нужно проверить каждый перед публикацией.

**Подготовка — файл `./course/claims.txt`:**
```
UNCHECKED: 70% людей бросают онлайн-курсы на первой неделе
UNCHECKED: Spaced repetition улучшает запоминание в 2-3 раза
UNCHECKED: Видео-формат эффективнее текста для моторных навыков
...
```

**Промпт:**
```
/loop 20m Take the first UNCHECKED claim from ./course/claims.txt.
Search the web for research supporting or refuting it.
Find at least 2 sources. Assess: VERIFIED, DISPUTED, or NUANCED.
Add source links and a brief note.
Update the file: change UNCHECKED to the verdict.
Stop if no UNCHECKED items remain.
```

**Результат:**
```
VERIFIED: 70% людей бросают онлайн-курсы на первой неделе
  → Source: MIT study 2023 (link), Coursera report 2024 (link)
  
NUANCED: Видео эффективнее текста для моторных навыков
  → Depends on skill type. True for physical skills, not conceptual.
  → Source: Journal of Educational Psychology 2024 (link)
```

---

### ✍️ Создание контента

---

#### Кейс 6. Генерация идей для постов по трендам

**Задача:** Каждое утро получать свежие идеи для контента, адаптированные под актуальную повестку дня.

**Промпт (Desktop scheduled task, запускается в 8:00):**
```
Today's date: use current date.
Search for the top 3 trending discussions in [твоя ниша] right now.

For each trend, generate:
- 2 LinkedIn post ideas (professional angle, 150-200 words)
- 2 Telegram post ideas (conversational, 50-80 words)  
- 1 long-form article angle (if trend has depth)

Format each idea as:
HOOK: [первое предложение, которое останавливает скроллинг]
ANGLE: [уникальная точка зрения]
CTA: [призыв к действию]

Append to ./content/ideas_[date].md
```

**Почему это работает:** Идеи привязаны к тому, что обсуждается прямо сейчас — а не к вечнозелёным темам, которые ты уже сто раз видел.

---

#### Кейс 7. Конвейер переработки контента

**Задача:** У тебя есть папка с лекциями, статьями, заметками. Нужно переработать каждый файл в несколько форматов для публикации.

**Структура папок:**
```
./raw_content/     ← сюда кладёшь исходники
./formatted/       ← Claude пишет сюда готовые форматы
./processed/       ← сюда Claude перемещает обработанные файлы
```

**Промпт:**
```
/loop 30m Check ./raw_content/ for any files NOT marked as [DONE].
Take the first unprocessed file. Read its content.

Create in ./formatted/[filename]/: 
1. linkedin.md — LinkedIn post (200 words, professional tone, 3 key insights)
2. telegram.md — Telegram post (80 words, conversational, one strong idea)
3. tweets.md — 3 tweet variants (under 280 chars each, different angles)
4. summary.md — Executive summary (5 bullet points, what and why it matters)

After creating all files, move the original to ./processed/ 
and mark it as [DONE] in a log file ./content_log.md
```

Загружаешь 20 файлов — возвращаешься через час к готовым форматам для публикации.

---

### 📊 Дайджесты и отчёты

---

#### Кейс 8. Ежедневный AI-дайджест

**Задача:** Автоматический дайджест по AI-новостям для публикации в Telegram-канале — каждый день, без ручного сбора.

**Промпт (Desktop task, 7:30 ежедневно):**
```
Today is [current date]. Search for the most important AI news 
from the last 24 hours. Focus on: new model releases, 
significant research, product launches, industry shifts.

Select exactly 5 stories. For each:
- 📌 Headline (your own words, punchy)
- What happened (2 sentences max)
- Why it matters for AI practitioners and creators (1 sentence)
- Link to source

Format as a ready-to-publish Telegram message.
Start with: "🤖 AI Дайджест [date]"
End with: "Подписывайся — каждый день в 8:00"

Save to ./digest/[date].md
```

**Результат:** Готовый пост, который ты либо публикуешь напрямую, либо редактируешь за 2 минуты. Не пишешь с нуля.

---

#### Кейс 9. Еженедельный отчёт по проектам

**Задача:** Автоматический intelligence-отчёт по своим проектам — что сделано, что в процессе, что застряло.

**Промпт (Desktop task, пятница 18:00):**
```
Review all files modified this week in ./projects/ and ./research/.
Check ./tasks/active.md and ./tasks/completed.md.

Write a weekly executive report to ./reports/week_[date].md:

## Завершено
[список с кратким описанием]

## В процессе
[статус и % готовности по ощущениям из файлов]

## Застряло / требует решения
[что не двигается и почему, исходя из содержимого файлов]

## Следующая неделя
[3 приоритета на основе незавершённого]

## Инсайты недели
[любые интересные паттерны или наблюдения из контента]
```

**Бонус:** Добавь в конец промпта инструкцию отправить отчёт через n8n webhook в Telegram или Notion — получаешь еженедельный briefing прямо в мессенджер.

---

### 🧠 Личная продуктивность

---

#### Кейс 10. Умный фоновый советник

**Задача:** Claude периодически "думает" над твоим списком задач и приносит инсайты — не ты управляешь им, а он проактивно работает на тебя.

**Промпт:**
```
/loop 3h Read ./tasks/active.md and ./projects/context.md.

For each active task or project:
1. Search the web: is there any new information, tool, or approach 
   published in the last week that changes how I should approach this?
2. Are there any dependencies or blockers I might be missing?
3. Is the priority still correct given what's happening in the field?

Write a brief advisory note to ./advisor/update_[timestamp].md.
Flag anything URGENT in red (use ⚠️).
Keep each note under 150 words. Be direct, skip pleasantries.
```

**Что это даёт:** Ты не следишь за новостями и не проверяешь каждую задачу вручную. Claude сам замечает, если появился инструмент, который делает твою задачу проще — или если контекст изменился.

---

## 6. Паттерны построения задач

Все 10 кейсов строятся на нескольких базовых паттернах. Понимая их, ты можешь создавать свои задачи.

### Паттерн 1: Source → Filter → Append

Самый частый. Claude берёт данные из источника, фильтрует по критериям, дописывает в файл.

```
Search [source] for [topic] from [timeframe].
Filter: only include [criteria].
Append to [file] with [timestamp].
```

Использован в кейсах: 1, 2, 3, 8.

### Паттерн 2: Queue Processing

Файл-очередь со статусами. Claude берёт первый элемент, обрабатывает, меняет статус, переходит к следующему.

```
Take first [STATUS] item from [queue_file].
Process: [что делать].
Update status to [DONE/VERIFIED/etc].
Stop if no [STATUS] items remain.
```

Использован в кейсах: 4, 5.

### Паттерн 3: Folder Watch

Claude следит за папкой, обрабатывает новые файлы, перемещает обработанные.

```
Check [input_folder] for unprocessed files.
Take first unprocessed. 
Create [output_files] in [output_folder].
Move original to [processed_folder].
```

Использован в кейсе: 7.

### Паттерн 4: State Comparison

Claude сохраняет состояние в файл, при следующем запуске сравнивает — сообщает только об изменениях.

```
Read current state from [state_file].
Check [source] for current data.
Compare. Report only CHANGES.
Update [state_file] with new state.
```

Использован в кейсе: 1.

### Паттерн 5: Advisory Review

Claude периодически анализирует контекст и инициирует рекомендации без запроса.

```
Read [context_files].
Search web for [relevant_updates].
Write advisory note: [format].
Flag [urgent_criteria] with [marker].
```

Использован в кейсе: 10.

---

## 7. Интеграция с внешними сервисами

`/loop` сам по себе работает с файлами и вебом. Для отправки результатов наружу нужны MCP-коннекторы.

### Отправка в Notion

Если подключён Notion MCP:
```
/loop 1d [исследуй тему].
Write the result as a Notion page in database [Database Name].
Properties: Name=[title], Date=[today], Status=Draft, Tags=[relevant tags].
```

### Отправка через n8n

Если подключён n8n MCP:
```
/loop 1d [собери дайджест].
After compilation, send the result to n8n webhook "daily-digest".
Include fields: content, date, item_count.
```

n8n принимает данные и роутит дальше — в Telegram, email, Airtable, куда угодно.

### Схема для Twitter/X мониторинга

Twitter не имеет официального MCP, но реализуется через n8n:

```
n8n (cron trigger каждые 2h)
  → Twitter/X node (читает аккаунты по списку)
  → Filter node (базовая фильтрация по ключевым словам)
  → Claude API (глубокий анализ по критериям)
  → If node (найдено что-то важное?)
    → Yes: Notion (сохранить) + Telegram (уведомить)
    → No: Log (записать "no match")
```

Это надёжнее чем `/loop` для внешних API — n8n персистентен и не зависит от открытой сессии.

---

## 8. Сравнение: `/loop` vs альтернативы

| Критерий | `/loop` CLI | Desktop Tasks | Cloud Tasks | n8n + Claude API |
|----------|------------|---------------|-------------|------------------|
| Настройка | Секунды | Минуты | Минуты | Часы |
| Персистентность | Нет | Частичная | Полная | Полная |
| Параллельность | Нет | Нет | Нет | Да |
| Внешние API | Через MCP | Через MCP | Через MCP | Нативно |
| Стоимость | Включено в план | Включено в план | Включено в план | API pay-per-use |
| Сложность | Минимальная | Низкая | Низкая | Средняя |
| Лучше для | Сессионный мониторинг | Ежедневные задачи | Always-on агенты | Сложные пайплайны |

### Рекомендация

Начни с **`/loop`** для экспериментов и простых задач внутри рабочей сессии. Переноси в **Desktop Tasks** то, что нужно каждый день. Используй **n8n** когда нужна реальная параллельность, внешние API (Twitter, Telegram-боты), или надёжность production-уровня.

Оптимальная связка для большинства задач: **Claude Code Desktop Tasks** (исследование, анализ, генерация контента) + **n8n** (роутинг результатов в нужные каналы).

---

*Документ подготовлен на основе Claude Code v2.1.76, март 2026.*  
*Функциональность `/loop` требует Claude Code v2.1.72 или новее.*  
*Проверь версию: `claude --version`*
