# Runtimes

Этот каталог содержит **две независимые execution-sandbox**:
- `codex/`
- `claudecode/`

Обе песочницы должны реализовывать одно и то же ядро требований, но не мешать друг другу.

## Правило

Каждый runtime работает только в своей директории.

Сравнение результатов происходит отдельно, в [comparison/README.md](../comparison/README.md).

## Текущее состояние

- `RUN-001 / GT-001` выполнен в `codex/` и `claudecode/`.
- Сводное сравнение зафиксировано в [comparison/RUN-001_GT-001_scorecard.md](../comparison/RUN-001_GT-001_scorecard.md).

## Как запускать сейчас

- операторский протокол: [parallel_launch_protocol.md](./parallel_launch_protocol.md)
- стартовый prompt для `Codex`: [codex/OPERATOR_PROMPT.md](./codex/OPERATOR_PROMPT.md)
- стартовый prompt для `Claude Code`: [claudecode/OPERATOR_PROMPT.md](./claudecode/OPERATOR_PROMPT.md)
