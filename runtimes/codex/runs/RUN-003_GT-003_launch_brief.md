# RUN-003: Codex Launch Brief for GT-003

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `execution launch brief`
> Основание:
> - [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
> - [../../../agent_org_tz_codex.md](../../../agent_org_tz_codex.md)
> - [../../../core/benchmarks/GT-003-autonomous-closeout-recovery.md](../../../core/benchmarks/GT-003-autonomous-closeout-recovery.md)
> - [../../../core/expected_results/GT-003-expected_result.md](../../../core/expected_results/GT-003-expected_result.md)
>

## Цель прогона

Выполнить `GT-003` для `Codex` внутри `runtimes/codex/` так, чтобы closeout inconsistency была устранена самим runtime, а не observer-side правкой runtime-local truth files.

## Порядок чтения перед запуском

Перед началом реализации агент должен прочитать материалы в таком порядке:

1. [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
2. [../../../agent_org_tz_codex.md](../../../agent_org_tz_codex.md)
3. [../../../core/benchmarks/GT-003-autonomous-closeout-recovery.md](../../../core/benchmarks/GT-003-autonomous-closeout-recovery.md)
4. [../../../core/expected_results/GT-003-expected_result.md](../../../core/expected_results/GT-003-expected_result.md)
5. [../workspace/README.md](../workspace/README.md)
6. [../control/README.md](../control/README.md)
7. [../evaluation/README.md](../evaluation/README.md)

## Write Scope

Во время этого прогона разрешено писать только в:

- `runtimes/codex/workspace/`
- `runtimes/codex/control/`
- `runtimes/codex/runs/`
- `runtimes/codex/evaluation/`

Нельзя изменять:

- `core/`
- `comparison/`
- `runtimes/claudecode/`
- центральный `control_plane/`

## Что именно нужно сделать

В рамках `RUN-003 / GT-003` `Codex` должен:

1. диагностировать closeout inconsistency по raw artifacts;
2. выполнить repair так, чтобы локальные truth files были обновлены самим runtime;
3. не подменять repair narrative-объяснением без артефактов;
4. оставить evidence recovery path;
5. участвовать в final hold reconciliation после repair;
6. обновить evaluation и learning artifacts так, чтобы было видно:
   - что было inconsistent;
   - что именно исправил runtime;
   - почему финальный closeout теперь допустим.

## Что считается хорошим результатом

Хороший результат — это не просто красивый финальный `completed`, а локальный repair package, по которому можно восстановить:

- где был разрыв closeout;
- какая observer directive инициировала repair;
- какие truth artifacts runtime сам привёл в консистентность;
- почему terminal success теперь честный.

## Что считать недопустимым

Недопустимо:

- observer-side переписывание runtime-local truth files как способ пройти benchmark;
- отсутствие runtime-authored repair evidence;
- скрытый переход в финальный success без recovery trace;
- старт нового run вместо closeout recovery;
- запись вне своей runtime-sandbox.

## Формат результата прогона

После завершения `RUN-003` должны быть обновлены:

- `runtimes/codex/control/`
- `runtimes/codex/workspace/`
- `runtimes/codex/runs/`
- `runtimes/codex/evaluation/`

И отдельно должен существовать run summary с:

- описанием closeout inconsistency;
- перечислением runtime-authored repair artifacts;
- указанием, где лежит revalidation trace;
- указанием, где лежит evidence final hold reconciliation.
