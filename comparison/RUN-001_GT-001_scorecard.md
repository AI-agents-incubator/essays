# RUN-001 GT-001 Scorecard

> Версия файла: `v1.1`
> Дата версии: `2026-03-17`
> Тип документа: `comparison workfile`
> Основание:
> - [../core/benchmarks/GT-001-bootstrap-runtime-sandbox.md](../core/benchmarks/GT-001-bootstrap-runtime-sandbox.md)
> - [../core/expected_results/GT-001-expected_result.md](../core/expected_results/GT-001-expected_result.md)
> - [../core/evaluation/comparison_criteria.md](../core/evaluation/comparison_criteria.md)
>

## Сравниваемые реализации

- Runtime A: `Codex`
- Runtime B: `Claude Code`
- Версия core ТЗ: `agent_org_tz_core.md v1.1`
- Benchmark: `GT-001`
- Дата сравнения: `2026-03-17`

## Критерии

### 1. Полнота структуры

- Codex: `PASS`. Создан полный `agent_org/` с `40` артефактами и отдельный runtime-layer из `12` Codex-specific файлов.
- Claude Code: `PASS`. Создан полный `agent_org/` с `40` артефактами и отдельный runtime-layer из `14` Claude Code-specific файлов.

### 2. Ясность bootstrap

- Codex: entrypoint в `AGENTS.md` задаёт точный порядок чтения, write scope, цель прогона и обязательные выходные артефакты.
- Claude Code: entrypoint в `CLAUDE.md` задаёт тот же порядок чтения и write scope, плюс сразу указывает bootstrap entrypoints в `agent_org/bootstrap/`.

### 3. Качество role separation

- Codex: роли и повторяемые workflows разведены чисто через `.codex/agents/` и `.agents/skills/`. Разделение выглядит минималистично и инженерно прозрачно.
- Claude Code: тот же базовый набор ролей и skills, но поверх добавлен runtime-governance слой через `.claude/rules/` и `.claude/hooks/`.

### 4. Качество artifact architecture

- Codex: покрыты все обязательные домены `charter -> policies -> intake -> product -> engineering -> execution -> knowledge -> evaluation -> state -> evolution -> bootstrap`.
- Claude Code: покрыты те же домены. Архитектура симметрична Codex-реализации, но часть engineering-артефактов дополнительно разведена по подкаталогам (`engineering/specs/`).

### 5. Benchmark trace

- Codex: есть `RUN-001_GT-001_summary.md`, `RUN-001_GT-001_local_evaluation.md` и `agent_org/evaluation/benchmark_results.md`. Статус прогона: `pass`.
- Claude Code: есть `RUN-001_GT-001_summary.md`, `RUN-001_GT-001_evaluation.md` и `agent_org/evaluation/benchmark_results.md`. Статус прогона: `passed`.

### 6. Learning trace

- Codex: learning trace оформлен через `improvement_backlog.md` и `change_proposals.md`; в локальной evaluation есть ссылка на `CP-001`.
- Claude Code: learning trace оформлен через `improvement_backlog.md`, `change_proposals.md` и явный блок `Next Actions` в evaluation.

### 7. Качество state layer и долгоживущей памяти

- Codex: есть `state_registry.md`, `storage_strategy.md`, `sqlite_schema.sql` и путь миграции в Supabase. Реальная БД пока не поднята.
- Claude Code: есть тот же обязательный комплект state-layer артефактов и такой же SQLite-first подход. Реальная БД пока тоже не поднята.

### 8. Удобство независимой валидации

- Codex: валидацию удобно читать за счёт компактного summary и отдельного local evaluation trace. Картина прогона быстро восстанавливается.
- Claude Code: валидацию удобно читать за счёт более развёрнутого evaluation с audit, findings и next actions; дополнительно виден governance-layer.

### 9. Готовность к следующему автономному запуску

- Codex: готов. Следующий запуск может опираться на уже собранный bootstrap и state scaffold, остаётся только перейти от схемы к живым данным.
- Claude Code: готов. Следующий запуск может начинаться сразу из `CLAUDE.md`; открытый зазор тот же: поднять реальный SQLite DB file для следующего run.

## Итог

- Что лучше у Codex: более строгий минимализм runtime-layer, чистое разделение `agents` и `skills`, компактная и очень читаемая run/evaluation-связка.
- Что лучше у Claude Code: более богатый governance-контур за счёт `rules` и `hooks`, чуть более самодостаточный entrypoint, более развёрнутый audit narrative.
- Что переносится в core: обязательный entrypoint с точным read order, write scope и bootstrap pointers; обязательный state layer; обязательные run summary, local evaluation и learning next step; единое ожидание, что GT-001 завершается готовностью к следующему автономному run.
- Что остаётся runtime-specific: формат конфигурации (`config.toml` против `settings.json`), структура runtime-папок (`.codex` и `.agents` против `.claude`), а также механизмы governance вокруг правил и hooks.
