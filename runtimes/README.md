# Runtimes

Этот каталог содержит **две независимые execution-sandbox**:
- `codex/`
- `claudecode/`

Обе песочницы должны реализовывать одно и то же ядро требований, но не мешать друг другу.

В рамках этого baseline-репозитория эти песочницы следует трактовать как **reference sandbox layout**, а не как основное место для долгоживущих live-wave экспериментов. Для активных параллельных прогонов лучше использовать отдельную рабочую среду.

## Правило

Каждый runtime работает только в своей директории.

Сравнение результатов происходит отдельно, в [comparison/README.md](../comparison/README.md).

## Текущее состояние

- `RUN-001 / GT-001` выполнен в `codex/` и `claudecode/`.
- Сводное сравнение зафиксировано в [comparison/RUN-001_GT-001_scorecard.md](../comparison/RUN-001_GT-001_scorecard.md).
- `GT-002` в этом репозитории зафиксирован как specification + launch package, а не как живая baseline-wave.

## Как запускать сейчас

- операторский протокол: [parallel_launch_protocol.md](./parallel_launch_protocol.md)
- сигнальный протокол: [runtime_status_protocol.md](./runtime_status_protocol.md)
- стартовый prompt для `Codex`: [codex/OPERATOR_PROMPT.md](./codex/OPERATOR_PROMPT.md)
- стартовый prompt для `Claude Code`: [claudecode/OPERATOR_PROMPT.md](./claudecode/OPERATOR_PROMPT.md)
