# Supabase Migration Path

> Версия файла: `v1.0`
> Дата версии: `2026-03-16`
> Тип документа: `путь миграции state layer`

## Когда пора переходить с SQLite

Переход на `Supabase / Postgres` нужен, когда хотя бы часть этих условий становится устойчивой:

- прогоны длятся днями и неделями;
- несколько процессов должны читать общее состояние;
- нужна удалённая надёжность хранения;
- локальный файл базы начинает мешать параллельной работе;
- требуется richer query layer и observability;
- нужна интеграция с внешними сервисами и автоматизациями.

## Что не должно меняться при миграции

При переходе на `Supabase` должны оставаться неизменными:
- artifact layer;
- benchmark definitions;
- expected result definitions;
- comparison criteria;
- логика ролей, handoff и evaluation.

Меняется только operational backend.

## Рекомендуемый путь миграции

1. Зафиксировать v1 SQLite schema как stable baseline.
2. Нормализовать naming и entity IDs.
3. Подготовить Postgres-compatible schema.
4. Развести write access по runtime и средам.
5. Сохранить runtime isolation на логическом уровне.
6. Добавить migration scripts.
7. Проверить совместимость benchmark history.
8. Только потом переключать активный state backend.

## Принцип безопасности

Даже после миграции в `Supabase`:
- runtime-specific isolation должна сохраняться;
- source of truth остаётся в `core/`;
- comparison и evaluation остаются аудируемыми;
- состояние не должно становиться opaque black box.
