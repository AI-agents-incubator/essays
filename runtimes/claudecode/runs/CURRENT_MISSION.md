# CURRENT MISSION: Claude Code Runtime

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `active runtime mission`
> Runtime: `Claude Code`
> Текущий run: `RUN-002`

## Исходное состояние

`RUN-001` уже завершён. В sandbox существует минимальный operational scaffold:

- `agent_org/`
- runtime-specific agents, skills, rules и hooks
- benchmark trace
- evaluation trace
- базовый state layer

Следующий run нужен не для повторного bootstrap, а для перехода от первого scaffold к следующей стадии автономной работы.

## Цель RUN-002

Выполнить первый autonomous continuation run для `Claude Code`, не ломая уже созданную структуру.

## Обязательные шаги

1. Прочитать `CLAUDE.md` и восстановить нормативный контекст.
2. Проверить текущее состояние sandbox после `RUN-001`.
3. Провести audit текущих артефактов и найти структурные пробелы или несогласованности.
4. Если live SQLite DB file ещё отсутствует, создать его в `agent_org/state/` на основе `sqlite_schema.sql`.
5. Синхронизировать `state_registry.md` с фактическим состоянием state layer.
6. Проверить, достаточно ли текущего governance-layer для следующего автономного run, и при необходимости усилить его.
7. Обновить evaluation-артефакты так, чтобы было видно, что sandbox перешёл от scaffold к operational continuation.
8. Зафиксировать хотя бы одно improvement decision для следующего run.
9. Оставить новый run summary и новую evaluation trace.

## Что нужно обновить минимум

- `runtimes/claudecode/workspace/agent_org/state/`
- `runtimes/claudecode/workspace/agent_org/evaluation/`
- `runtimes/claudecode/workspace/agent_org/evolution/`
- `runtimes/claudecode/workspace/.claude/`
- `runtimes/claudecode/runs/`
- `runtimes/claudecode/evaluation/`

## Рекомендуемые выходные артефакты

- `runtimes/claudecode/runs/RUN-002_state_activation_summary.md`
- `runtimes/claudecode/evaluation/RUN-002_state_activation_evaluation.md`

Если в ходе run выяснится, что более точное имя итоговых файлов лучше отражает результат, агент может выбрать другое имя, но оно должно:

- начинаться с `RUN-002`
- быть понятным по смыслу
- явно относиться к этому run

## Ограничения

- Нельзя менять `core/`
- Нельзя менять `comparison/`
- Нельзя менять `runtimes/codex/`
- Нельзя повторно “строить всё заново”, если задача решается эволюцией существующей структуры

## Что считается успешным результатом

Успешный run означает, что `Claude Code`:

- самостоятельно восстановил контекст;
- автономно выполнил continuation work;
- усилил state layer и governance-layer;
- оставил trace принятых решений;
- явно подготовил основу для `RUN-003`.
