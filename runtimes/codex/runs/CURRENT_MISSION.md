# CURRENT MISSION: Codex Runtime

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `active runtime mission`
> Runtime: `Codex`
> Текущий run: `RUN-002`

## Исходное состояние

`RUN-001` уже завершён. В sandbox существует минимальный operational scaffold:

- `agent_org/`
- runtime-specific agents и skills
- benchmark trace
- evaluation trace
- базовый state layer

Следующий run нужен не для повторного bootstrap, а для перехода от первого scaffold к следующей стадии автономной работы.

## Цель RUN-002

Выполнить первый autonomous continuation run для `Codex`, не ломая уже созданную структуру.

## Обязательные шаги

1. Прочитать `AGENTS.md` и восстановить нормативный контекст.
2. Проверить текущее состояние sandbox после `RUN-001`.
3. Провести audit текущих артефактов и найти структурные пробелы или несогласованности.
4. Если live SQLite DB file ещё отсутствует, создать его в `agent_org/state/` на основе `sqlite_schema.sql`.
5. Синхронизировать `state_registry.md` с фактическим состоянием state layer.
6. Обновить evaluation-артефакты так, чтобы было видно, что sandbox перешёл от scaffold к operational continuation.
7. Зафиксировать хотя бы одно improvement decision для следующего run.
8. Оставить новый run summary и новую local evaluation trace.

## Что нужно обновить минимум

- `runtimes/codex/workspace/agent_org/state/`
- `runtimes/codex/workspace/agent_org/evaluation/`
- `runtimes/codex/workspace/agent_org/evolution/`
- `runtimes/codex/runs/`
- `runtimes/codex/evaluation/`

## Рекомендуемые выходные артефакты

- `runtimes/codex/runs/RUN-002_state_activation_summary.md`
- `runtimes/codex/evaluation/RUN-002_state_activation_evaluation.md`

Если в ходе run выяснится, что более точное имя итоговых файлов лучше отражает результат, агент может выбрать другое имя, но оно должно:

- начинаться с `RUN-002`
- быть понятным по смыслу
- явно относиться к этому run

## Ограничения

- Нельзя менять `core/`
- Нельзя менять `comparison/`
- Нельзя менять `runtimes/claudecode/`
- Нельзя повторно “строить всё заново”, если задача решается эволюцией существующей структуры

## Что считается успешным результатом

Успешный run означает, что `Codex`:

- самостоятельно восстановил контекст;
- автономно выполнил continuation work;
- усилил state layer;
- оставил trace принятых решений;
- явно подготовил основу для `RUN-003`.
