Ниже — структурированная версия в формате Markdown. Я убрал шум начала разговора, повторы и сбои распознавания, но сохранил все содержательные идеи, distinctions, примеры, pipeline, роли агентов, skills, tools, автономный запуск, Figma → ТЗ → frontend/database → SQLite → Supabase → deploy → Playwright. Исходный файл: 

---

# Компаньон и автономия: как организовать Claude Code как систему оркестратора, skills, субагентов и tools

## Введение

Этот материал посвящён тому, как превратить Claude Code из обычного кодового ассистента в управляемую агентную систему. Центральная идея простая: есть оркестратор, который принимает решение, **кого** вызвать; есть skills, которые описывают, **как** выполнять работу; есть субагенты, которые изолированно выполняют подзадачи; и есть tools, которые дают доступ к внешним возможностям — API, браузеру, Figma, Supabase и другим сервисам.  

Дальше эта архитектура разворачивается в практический pipeline: от анализа экранов в Figma и генерации технического задания — до автономной реализации интерфейса, проектирования базы данных, локального тестирования на SQLite, миграции в Supabase, деплоя и финальной проверки через Playwright.  

---

## 1. Где в Claude Code находится “системный промпт”

В Claude Code роль системного промпта фактически выполняют файлы `CLAUDE.md`. Они читаются по иерархии: глобальный `~/.claude/CLAUDE.md`, затем `CLAUDE.md` в корне проекта, затем `CLAUDE.md` в подкаталогах. Именно здесь описывается routing: при каких условиях какой skill читать, какого субагента вызывать и как вести себя в разных типах задач. Дополнительно используются `.claude/settings.json` для настройки инструментов и разрешений, а `.claude/commands/` — для кастомных slash-команд. 

Пример логики маршрутизации:

```md
## Task Routing

- If the task involves frontend UI → use the design system in /components, follow patterns in /docs/ui-guide.md
- If the task involves data pipeline → reference /scripts/pipeline/ and follow Make.com integration patterns
- If the task involves Telegram bot → check /bots/telegram/ and use the existing webhook structure
- For content processing → follow the AI filtering workflow in /docs/content-pipeline.md
```

---

## 2. Что такое skills в Claude Code

В самом Claude Code нет встроенной магической папки skills “из коробки” в том виде, как она может существовать в чат-интерфейсе. Но этот паттерн можно воспроизвести самостоятельно. Идея такая: создать папку `skills/`, внутри которой каждая задача оформляется как отдельный `SKILL.md`. Тогда Claude Code сможет перед началом задачи читать соответствующий файл и следовать его инструкциям. 

Пример структуры:

```text
your-project/
├── CLAUDE.md
├── .claude/
│   ├── commands/
│   │   ├── create-doc.md
│   │   ├── process-content.md
│   │   └── deploy.md
│   └── settings.json
├── skills/
│   ├── telegram-bot/
│   │   └── SKILL.md
│   ├── content-filter/
│   │   └── SKILL.md
│   └── make-automation/
│       └── SKILL.md
```

А в `CLAUDE.md` это может выглядеть так:

```md
## Skill Routing

Before starting any task, check if a relevant skill exists in /skills/.
Read the SKILL.md first and follow its instructions.

- Telegram publishing → /skills/telegram-bot/SKILL.md
- Content filtering → /skills/content-filter/SKILL.md
- Make.com blueprints → /skills/make-automation/SKILL.md
```

Смысл skills: это **методология**, SOP, инструкция, playbook. Один skill не создаёт нового контекста — он просто направляет текущее мышление Claude внутри текущей сессии.  

---

## 3. Что такое субагенты

Субагенты — это уже не инструкции, а отдельные изолированные исполнители. В описанном диалоге они привязаны к `Task tool`: основной Claude может породить дочерний агент, передать ему только нужный кусок контекста, дождаться результата и продолжить orchestration. У таких субагентов собственное окно контекста; они подходят для разбиения большой задачи на независимые части. Важная характеристика, зафиксированная в диалоге: субагенты не видят весь родительский разговор и не должны бесконтрольно разрастаться в глубину. 

Пример routing в `CLAUDE.md`:

```md
## Sub-Agent Routing

When a task has multiple independent parts, use the Task tool to delegate:

- Code review: Spawn a sub-agent focused only on reviewing code quality
- Test writing: Spawn a sub-agent to write tests separately
- Documentation: Spawn a sub-agent to update docs after code changes

### Rules:
- Always break large tasks into sub-agents when they touch 3+ files
- Each sub-agent gets only the files it needs
- Main agent synthesizes results at the end
```

---

## 4. Где описывать поведение субагентов

В разговоре отдельно проясняется важный момент: жёстко заданной “официальной” папки для субагентов нет, но удобно сделать собственную структуру, например `.claude/agents/`. Тогда `CLAUDE.md` остаётся только маршрутизатором, а конкретное поведение каждого субагента лежит в его `.md`-файле. 

Пример структуры:

```text
your-project/
├── CLAUDE.md
├── .claude/
│   ├── commands/
│   └── agents/
│       ├── code-reviewer.md
│       ├── content-filter.md
│       ├── translator.md
│       └── telegram-publisher.md
```

Пример описания агента:

```md
# Code Reviewer Agent

## Role
You are a code review specialist.

## Instructions
- Focus only on the files provided
- Check for security issues, performance, readability
- Output a structured review with severity levels

## Output Format
...
```

А в `CLAUDE.md`:

```md
## Sub-Agent Definitions

When using the Task tool, load the appropriate agent profile:

- Code review tasks → read .claude/agents/code-reviewer.md and pass its contents as the prompt
- Content filtering → read .claude/agents/content-filter.md
- Translation → read .claude/agents/translator.md
- Telegram publishing → read .claude/agents/telegram-publisher.md

Always read the agent file BEFORE spawning the sub-agent.
Pass the file contents as part of the Task instruction.
```

---

## 5. Разница между skills и субагентами

Это один из центральных вопросов диалога. Формула там дана очень чёткая:

* **Skills** — это инструкции для самого Claude в текущей сессии.
* **Sub-agents** — это отдельные экземпляры Claude со своим изолированным контекстом. 

То есть skill — это “почитай методичку и действуй”. Субагент — это “отправь отдельного исполнителя выполнить кусок работы и принести результат”.

Сравнение:

| Параметр        | Skill                              | Sub-agent                         |
| --------------- | ---------------------------------- | --------------------------------- |
| Контекст        | Общий, текущая сессия              | Изолированный                     |
| Когда применять | Нужна методология для одной задачи | Есть несколько независимых частей |
| Аналогия        | Поваренная книга                   | Делегирование сотруднику          |
| Стоимость       | Без отдельного спауна              | Требует отдельного запуска        |
| Роль            | “Как делать”                       | “Кто делает”                      |

Именно поэтому в зрелой системе они работают вместе: субагент может читать skill и использовать его как playbook. 

---

## 6. Может ли субагент использовать skills

Да. В диалоге это подтверждается прямо: субагенту можно явно указать прочитать один или несколько `SKILL.md` и действовать по ним. Более того, skill сам по себе тоже может рекомендовать spawn других субагентов, если задача многошаговая. 

Пример:

```md
# .claude/agents/content-processor.md

## Role
You are a content processing specialist.

## Skills to use
- Read and follow /skills/content-filter/SKILL.md
- Read and follow /skills/translator/SKILL.md

## Instructions
1. First filter the content using the content-filter skill
2. Then translate using the translator skill
3. Return structured result
```

Итоговая схема:

```text
CLAUDE.md          → WHO to call (routing only)
agents/*.md        → WHAT to do + WHICH skills to use
skills/*/SKILL.md  → HOW to do it (methodology)
```

Эта трёхслойная модель специально подчёркивается как более поддерживаемая, чем попытка запихнуть всё в один `CLAUDE.md`. 

---

## 7. Что такое tools

Tools в этой архитектуре — это внешние возможности: API, сервисы, скрипты, MCP-серверы, кастомные интеграции. Они настраиваются через `.claude/settings.json`. То есть skill говорит **как** делать, субагент определяет **кто** делает, а tool даёт возможность **чем именно** воспользоваться: получить данные, отправить сообщение, открыть браузер, обратиться к базе и так далее. 

Пример:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["@notion-mcp/server"],
      "env": { "NOTION_API_KEY": "..." }
    },
    "telegram": {
      "command": "node",
      "args": ["./tools/telegram-server.js"]
    },
    "airtable": {
      "command": "npx",
      "args": ["@airtable-mcp/server"]
    }
  },
  "allowedTools": ["notion", "telegram", "airtable"]
}
```

И агент может прямо ссылаться на эти инструменты:

```md
# .claude/agents/content-processor.md

## Role
Content processing specialist

## Skills
- /skills/content-filter/SKILL.md

## Tools available
- Use Notion tool to fetch source content
- Use Telegram tool to publish results
- Use Airtable tool to log processing status

## Workflow
1. Fetch content from Notion
2. Filter using content-filter skill
3. Publish via Telegram
4. Log result to Airtable
```

---

## 8. Можно ли через tools вызывать другие AI API

Да. В разговоре прямо говорится, что tool может быть узкой функцией, которая внутри вызывает внешний AI API — например OpenAI, Anthropic или локальную модель. В этом случае Claude Code превращается в оркестратор нескольких моделей и сервисов. 

Пример:

```javascript
// tools/ai-evaluator.js — MCP tool that calls OpenAI
{
  name: "evaluate_content",
  description: "Uses GPT-4 to evaluate content quality",
  async execute({ content }) {
    const response = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [{ role: "user", content: `Rate this: ${content}` }]
    });
    return response.choices[0].message.content;
  }
}
```

В терминах Make.com это описано так:

```text
Make.com world          →  Claude Code world
─────────────────────────────────────────────
Module                  →  Tool (MCP)
Scenario                →  Agent + Skills
Router                  →  CLAUDE.md routing
HTTP Request module     →  Tool calling external AI API
```

---

## 9. Figma как источник ТЗ и фронтенд-реализации

Следующий большой блок диалога посвящён Figma. Основная мысль: чтобы Claude Code реально “видел” макеты, сначала нужно подключить Figma MCP сервер в `.claude/settings.json`, а уже потом давать ссылки на конкретные фреймы и просить либо написать код, либо сначала построить техническую спецификацию. 

Пример подключения:

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["figma-developer-mcp", "--figma-api-key=твой_ключ"]
    }
  }
}
```

Дальше workflow такой:

1. Открыть нужный экран в Figma и скопировать ссылку.
2. Передать эту ссылку Claude Code.
3. Claude Code через `get_design_context` получает скриншот, структуру элементов, цвета, шрифты, размеры, ассеты.
4. На основе этих данных либо пишет React-компонент, либо строит ТЗ. 

Пример прямого запроса:

```text
Вот дизайн экрана логина: https://figma.com/design/ABC123/MyApp?node-id=1-2
Реализуй его на React с Tailwind CSS.
```

Но более надёжный подход, зафиксированный в разговоре, — не просить код сразу, а сначала попросить **подробное техническое задание**: какие экраны есть, какие компоненты нужны, какие используются цвета и шрифты, какая структура проекта оптимальна. После этого ТЗ проверяется и уточняется, и только потом запускается реализация. 

---

## 10. Самопроверка ТЗ против оригинальных макетов

Из Figma можно не только извлечь спецификацию, но и проверить саму спецификацию на полноту. В диалоге это выделено как ключевая идея: после генерации ТЗ имеет смысл попросить Claude Code сравнить ТЗ с оригинальными экранами и найти дыры. Именно в этот момент всплывают дорогостоящие недосказанности: нет экрана восстановления пароля, неясен источник данных в таблице, непонятно, что делает кнопка после нажатия, отсутствует мобильная версия. 

Пример такого запроса:

```text
Теперь сравни ТЗ которое ты написал с оригинальными макетами.
Проверь:
1. Все ли экраны учтены?
2. Все ли элементы на каждом экране описаны?
3. Все ли переходы между экранами есть?
4. Какие вопросы у тебя остались — что неясно из макетов?
```

Из этого вырастает замкнутый цикл:

```text
Макеты в Figma
  → Claude Code анализирует
  → Генерирует ТЗ
  → Сам сравнивает ТЗ с макетами
  → Список вопросов тебе
  → Ты отвечаешь
  → Обновлённое ТЗ
  → Реализация
  → Сравнение результата с макетами
```

---

## 11. Pipeline: от Figma до автономного ТЗ

Диалог дальше разворачивает полноценный поэтапный pipeline. На подготовительном этапе создаётся Figma API ключ, настраивается MCP сервер, проверяется доступ к инструментам через `/tools`, создаётся структура проекта с `CLAUDE.md`, `.claude/agents/`, `skills/`, `specs/` и списком ссылок в `figma-links/screens.md`. 

Пример структуры проекта:

```text
project/
├── CLAUDE.md
├── .claude/
│   ├── settings.json
│   ├── agents/
│   │   ├── design-analyzer.md
│   │   ├── spec-writer.md
│   │   ├── spec-reviewer.md
│   │   └── question-generator.md
│   └── commands/
│       └── figma-to-spec.md
├── skills/
│   ├── figma-analysis/SKILL.md
│   └── spec-writing/SKILL.md
├── specs/
└── figma-links/
    └── screens.md
```

Потом создаётся список экранов:

```md
# Экраны приложения

## Auth Flow
- Login: https://figma.com/design/XXX/App?node-id=1-2
- Register: https://figma.com/design/XXX/App?node-id=3-4
- Forgot Password: https://figma.com/design/XXX/App?node-id=5-6

## Main Flow
- Dashboard: https://figma.com/design/XXX/App?node-id=7-8
- Profile: https://figma.com/design/XXX/App?node-id=9-10
- Settings: https://figma.com/design/XXX/App?node-id=11-12

## Примечания
- Целевой стек: React + Tailwind
- Нужна адаптивная верстка
- API пока нет, использовать моки
```

После этого следуют роли:

* анализатор дизайна;
* генератор ТЗ;
* ревьюер ТЗ;
* генератор вопросов;
* цикл ответов и обновления спецификации;
* финальная секция “Инструкция для автономной реализации”. 

---

## 12. User flow как предшественник Figma и базы данных

Отдельно в разговоре поднимается мысль, что реальный pipeline начинается ещё раньше, чем дизайн. User flow рассматривается как визуальная форма бизнес-логики: на нём сразу проявляются экраны, действия, данные, роли и условия. Из этого естественным образом вырастает структура базы данных. Например, flow регистрации немедленно раскрывает сущности `users`, `profiles`, `plans` и, скажем, поле `email_verified`. 

Схема дана так:

```text
User Flow (логика)
  → Структура БД (данные)
  → Wireframes (скелеты экранов)
  → Figma дизайн (визуал)
  → ТЗ
  → Реализация
```

---

## 13. Параллельные ветки: frontend и database

Следующая ключевая идея: как только на выходе появляется хорошее ТЗ, можно запускать две параллельные ветки. Одна строит интерфейс на React с моками и правильными именами переменных. Вторая строит схему данных, таблицы, поля, миграции и seed. Обе ветки должны использовать один и тот же словарь сущностей и полей. 

В разговоре это оформлено как необходимость общего **data contract**:

```text
ТЗ (из Figma + User Flow)
  │
  ▼
Субагент 0: Data Contract Generator
  → Список сущностей
  → Имена полей
  → Типы данных
  → Связи
  → API эндпоинты
  → specs/data-contract.md
  │
  ├──────────────────┐
  ▼                  ▼
Субагент 1:        Субагент 2:
Frontend           Database
  │                  │
  ▼                  ▼
React компоненты   Схема БД
с заглушками       миграции и seed
  │                  │
  └──────┬───────────┘
         ▼
  Субагент 3: Integration
```

Важно, что позже в разговоре допускается и другой вариант: data contract можно запускать не только **до**, но и **после** двух параллельных веток — как тест на расхождения. Смысл остаётся тем же: синхронизация имён и типов должна быть, иначе фронтенд назовёт поле `userName`, а база — `user_name`, или фронт будет ждать массив, а база вернёт объект. 

---

## 14. Data contract как тест

Эта мысль доводится до конца: data contract — это, по сути, разновидность теста. Не отдельная философия, а проверка консистентности. В том же ряду стоят сравнение ТЗ с макетами, визуальная проверка UI против Figma и тест покрытия всех user flows. Все эти операции сводятся к одному паттерну: взять два артефакта, сравнить, найти дельту, исправить. 

Список тестов-агентов выглядит так:

* сравнение ТЗ с Figma — тест на полноту;
* сравнение имён между фронтом и базой — тест на консистентность;
* сравнение готового UI с макетами — визуальный тест;
* проверка, что все роуты из user flow реализованы — тест на покрытие. 

---

## 15. SQLite как промежуточная среда

Очень важный практический блок — локальная БД. Если на раннем этапе не хочется сразу поднимать Supabase, то для проверки бизнес-логики можно использовать SQLite. В диалоге это названо “идеальным промежуточным шагом”: SQLite даёт настоящую реляционную модель, но живёт в одном файле и не требует деплоя. Можно автономно тестировать создание, чтение, связи и логику данных, а потом уже механически мигрировать в Supabase. 

Схема трёх сред:

```text
- Моки     → проверяем только UI
- SQLite   → проверяем бизнес-логику локально
- Supabase → проверяем продакшен-реальность
```

Переходы между ними минимальны, а не требуют переписывания с нуля. 

---

## 16. Production pipeline: Supabase, deploy, Playwright

Когда всё работает локально, pipeline продолжается:

1. Claude Code получает `.env` с ключами Supabase.
2. Создаёт таблицы, RLS, edge functions.
3. Переключает фронтенд с локального API на Supabase.
4. Тестирует подключение.
5. Делает deploy на Vercel или Netlify.
6. Назначает production environment variables.
7. Запускает Playwright тесты уже на задеплоенной версии. 

Итоговая схема из диалога:

```text
User Flow (Figma)
  → Анализ + ТЗ
  → Параллельно: Frontend (React) + Database (SQLite)
  → Тест на консистентность
  → Локальное тестирование (Vite + SQLite)
  → Всё ок?
  → Миграция на Supabase
    → Claude Code получает .env с ключами
    → Создаёт таблицы, RLS, edge functions
    → Переключает фронт на Supabase API
    → Тестирует подключение
  → Деплой на Vercel/Netlify
    → Назначает env переменные
    → Билдит и деплоит
  → Playwright тесты на задеплоенной версии
    → Проходит все user flows
    → Заполняет формы, кликает кнопки
    → Проверяет что данные реально пишутся в Supabase
    → Скриншоты каждого экрана → сравнение с Figma
```

Playwright здесь закрывает сразу три задачи: функциональное тестирование, визуальное сравнение и регрессию. Также прямо проговаривается, что Claude Code способен сам написать Playwright-тесты на основе уже построенного ТЗ и user flows. 

---

## 17. Полный список агентов, skills и tools для автономного pipeline

В финале диалога собирается формальная схема автономной системы. Для фазы анализа и ТЗ предлагаются агенты:

* `01-design-analyzer`
* `02-spec-writer`
* `03-spec-reviewer`
* `04-spec-finalizer`

Для фазы реализации:

* `05-frontend-builder`
* `06-database-architect`

Для интеграции и проверки:

* `07-local-integrator`
* `08-consistency-checker`
* `09-visual-tester`

Для production:

* `10-supabase-migrator`
* `11-api-switcher`
* `12-deployer`
* `13-e2e-tester` 

Список skills:

```text
skills/
├── react-components/
├── tailwind-styling/
├── database-design/
├── supabase-setup/
├── playwright-testing/
├── api-design/
└── deployment/
```

Для tools предлагаются как минимум Figma, Supabase и Playwright MCP серверы. Пример конфигурации:

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["figma-developer-mcp", "--figma-api-key=XXX"]
    },
    "supabase": {
      "command": "npx",
      "args": ["supabase-mcp-server"],
      "env": {
        "SUPABASE_URL": ".",
        "SUPABASE_SERVICE_KEY": "."
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp-server"]
    }
  },
  "allowedTools": [
    "Edit", "Write", "Bash",
    "mcp__figma__get_design_context",
    "mcp__figma__get_screenshot",
    "mcp__supabase__query",
    "mcp__supabase__migrate",
    "mcp__playwright__navigate",
    "mcp__playwright__screenshot"
  ]
}
```

Это сопровождается orchestrator-файлом `CLAUDE.md`, в котором явно описывается порядок фаз и правило: после Phase 1, где нужен человек для ответов на вопросы, Phase 2 и Phase 3 могут выполняться полностью автономно.   

---

## 18. Автономность Claude Code

В диалоге автономность Claude Code описывается через headless mode и флаги `-p`, `--allowedTools`, `--max-turns`. Выделяются три уровня автономии:

* Interactive — Claude спрашивает разрешение на изменения и команды.
* Semi-autonomous — часть инструментов заранее разрешена.
* Full autonomous — headless режим без участия человека. 

Пример команды:

```bash
claude -p "Read specs/content-pipeline.md and implement it" \
  --allowedTools "Edit,Write,Bash" \
  --max-turns 50
```

Также уточняется важная деталь: синтаксис `claude -p` и идея `--allowedTools` приводятся как реальные, но конкретные имена MCP tools зависят от того, что реально экспонирует настроенный MCP сервер. Проверять их нужно через интерактивный запуск `claude`, а затем `/tools`. Отдельно сделана оговорка, что в зависимости от версии CLI некоторые флаги могли измениться, поэтому полезно сверяться с `claude --help`. 

---

## 19. Ограничения и оговорки

Внутри самого диалога есть несколько мест, где источник честно признаёт неопределённость. Например, сравнение архитектуры OpenAI Codex с Claude Code описано как частичное и неполное, без уверенности в поддержке субагентов и глубине настройки. Это важно сохранить, потому что материал задуман не как безошибочная спецификация продукта, а как инженерная модель и практический паттерн организации работы. 

То же относится и к CLI-синтаксису: логика headless mode, `-p` и `--allowedTools` в статье отражает содержимое исходного диалога, но конкретные флаги и названия инструментов стоит сверять по текущей версии установленного Claude Code. 

---

## Заключение

В сжатом виде логика всей системы такая:

* `CLAUDE.md` решает, **кто** и **когда** работает;
* `agents/*.md` описывают, **что именно** делает каждый исполнитель;
* `skills/*/SKILL.md` описывают, **как** делать конкретную работу;
* `.claude/settings.json` и MCP tools дают доступ к внешним возможностям;
* Figma превращается в источник спецификации;
* user flow помогает выявить бизнес-логику и структуру БД;
* frontend и database можно строить параллельно;
* SQLite служит дешёвой средой проверки логики;
* Supabase, deploy и Playwright переводят проект в production-ready цикл;
* автономность достигается не магией, а хорошей спецификацией, грамотным routing и правильно выстроенными этапами проверки.  

Уверенность в том, что я корректно **структурировал именно содержимое файла**: 97%.
Уверенность в том, что все продуктовые и CLI-детали внутри самого диалога актуальны на сегодня: ниже, потому что сам источник местами это оговаривает.  

Могу следующим сообщением сделать вторую версию: уже не “бережно структурированную”, а более “редакторскую” — гладкую статью без разговорных следов и с более сильной логикой подачи.
