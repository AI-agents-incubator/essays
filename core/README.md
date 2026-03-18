# Core

Этот каталог хранит **общее ядро эксперимента**.

Именно здесь живёт source of truth, одинаковый для обеих runtime-реализаций:
- benchmark templates;
- expected result templates;
- comparison criteria;
- state-layer strategy;
- общая логика оценки.

Этот каталог не должен хранить runtime-specific конфигурацию.

Также этот каталог не должен превращаться в live execution-workspace. Если какой-то урок уже доказан в отдельной runtime-среде, сюда нужно переносить не сырой runtime-output, а только новый инвариант, benchmark definition или expected-result contract.

## Подкаталоги

- [benchmarks/README.md](./benchmarks/README.md) — benchmark-шаблоны и canonical golden tasks.
- [expected_results/README.md](./expected_results/README.md) — expected result и expected process templates.
- [evaluation/README.md](./evaluation/README.md) — общие правила сравнения и оценки.
- [state/README.md](./state/README.md) — стратегия состояния, SQLite-first схема и маршрут миграции к долгоживущему backend.
