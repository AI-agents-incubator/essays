# CURRENT MISSION: Claude Code Runtime

> Версия файла: `v3.0`
> Дата версии: `2026-03-17`
> Тип документа: `active runtime loop`
> Runtime: `Claude Code`
> Текущая фаза: `GT-001 completed / GT-002 launch-ready`

## Исходное состояние

Текущая benchmark wave `GT-001` завершена и консистентно закрыта.

Локальный baseline этой sandbox уже существует. Следующая подготовленная работа для этой sandbox:

- `RUN-002`
- benchmark: `GT-002`
- launch brief: `runs/RUN-002_GT-002_launch_brief.md`

Сейчас этот runtime не должен сам ничего запускать. Он должен оставаться observer-directed и быть готовым к следующей волне.

## Главная цель этого файла

Подготовить `Claude Code` к следующему observer-approved запуску `GT-002`, не разрушая завершённое состояние `GT-001`.

Это означает:

- runtime не должен самовольно стартовать `RUN-002`;
- следующий шаг начинается только после новой observer directive;
- при появлении новой wave runtime обязан читать не только control-файлы, но и launch brief `GT-002`;
- runtime обязан уметь отражать не только локальный progress, но и wave-level coordination state.

## Обязательный порядок чтения перед следующим действием

1. `workspace/CLAUDE.md`
2. `runs/RUNTIME_STATUS.md`
3. `control/observer_runtime_protocol.md`
4. `control/OBSERVER_DIRECTIVE.md`
5. `control/RUNTIME_ACK.md`

Если новая директива относится к `GT-002`, дополнительно обязательно прочитать:

6. `runs/RUN-002_GT-002_launch_brief.md`
7. `../../core/benchmarks/GT-002-wave-synchronized-orchestration.md`
8. `../../core/expected_results/GT-002-expected_result.md`

## Логика поведения

### Если directive = `hold`

- обновить `RUNTIME_ACK.md` в состояние `seen` или `accepted`;
- не запускать новый run;
- не менять структуру sandbox без отдельной директивы;
- сохранить завершённое состояние текущей wave.

### Если directive = `continue_with_next_run`

- сначала определить, к какой wave относится директива;
- если это `GT-002`, обязательно прочитать launch brief `RUN-002_GT-002_launch_brief.md`;
- обновить `RUNTIME_ACK.md` в `accepted`;
- перевести `RUNTIME_STATUS.md` в `in_progress`;
- выполнить только observer-approved run;
- после завершения оставить summary, evaluation и обновлённый status/ack.

### Если directive = `prepare_comparison`

- подготовить comparison или closeout package;
- не запускать новый engineering run;
- оставить evidence stage barrier, final hold или wave-closeout, если это требуется по `GT-002`.

### Если directive = `repair_current_state`

- принять директиву через `RUNTIME_ACK.md`;
- выполнить только repair-задачу;
- не превращать repair в новый run без отдельного разрешения.

### Если directive = `human_review_required`

- остановиться;
- обновить `RUNTIME_ACK.md` в состояние, сигнализирующее о необходимости человека;
- ждать внешнего решения.

## Особое правило для GT-002

Если запускается `GT-002`, runtime обязан:

- не считать локальный `completed` финалом всей wave автоматически;
- честно отражать состояния `waiting_peers`, если peer-runtime ещё не дошёл до barrier;
- не считать final hold достаточным, пока observer directive и runtime ack не совпали по одному `directive_id`;
- оставить coordination trace, а не только локальный run trace.

## Ограничения

- Нельзя менять `core/`
- Нельзя менять `comparison/`
- Нельзя менять `runtimes/codex/`
- Нельзя начинать новый run без observer directive

## Что считается успешным результатом

Успех этого слоя означает, что `Claude Code`:

- умеет сохранять завершённый baseline без самовольного перезапуска;
- готов к observer-approved запуску `GT-002`;
- умеет читать launch brief следующей wave;
- умеет подтверждать observer directive через `RUNTIME_ACK.md`;
- умеет участвовать в общей wave-coordination, а не только в локальном run.
