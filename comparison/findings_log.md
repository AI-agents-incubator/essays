# Findings Log

Этот файл предназначен для накопления сравнительных наблюдений.

Для каждой записи желательно фиксировать:
- дату;
- benchmark;
- сравниваемые версии;
- краткое наблюдение;
- структурную причину;
- рекомендацию:
  - перенести в core;
  - оставить runtime-specific;
  - проверить в следующем прогоне.

## 2026-03-17 / GT-001 / Codex vs Claude Code

- Краткое наблюдение: обе реализации успешно собрали одинаковый минимальный `agent_org/`, но Claude Code добавил более явный governance-layer, а Codex сохранил более компактный runtime-layer.
- Структурная причина: runtime-механизмы Claude Code естественно выражаются через `.claude/rules/` и `.claude/hooks/`, тогда как Codex делает акцент на прямой конфигурации, agents и skills.
- Рекомендация: перенести в `core` обязательный bootstrap contract, state layer и run/evaluation traces; governance-файлы и формат runtime-конфигурации оставить runtime-specific.
