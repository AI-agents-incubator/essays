# RUN-003: Claude Code Launch Brief for GT-003

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `execution launch brief`
> Основание:
> - [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
> - [../../../agent_org_tz_claudecode.md](../../../agent_org_tz_claudecode.md)
> - [../../../core/benchmarks/GT-003-autonomous-closeout-recovery.md](../../../core/benchmarks/GT-003-autonomous-closeout-recovery.md)
> - [../../../core/expected_results/GT-003-expected_result.md](../../../core/expected_results/GT-003-expected_result.md)
>

## Цель прогона

Выполнить `GT-003` для `Claude Code` внутри `runtimes/claudecode/` так, чтобы closeout inconsistency была устранена самим runtime, а не observer-side правкой runtime-local truth files.

## Порядок чтения перед запуском

Перед началом реализации агент должен прочитать материалы в таком порядке:

1. [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
2. [../../../agent_org_tz_claudecode.md](../../../agent_org_tz_claudecode.md)
3. [../../../core/benchmarks/GT-003-autonomous-closeout-recovery.md](../../../core/benchmarks/GT-003-autonomous-closeout-recovery.md)
4. [../../../core/expected_results/GT-003-expected_result.md](../../../core/expected_results/GT-003-expected_result.md)
5. [../workspace/README.md](../workspace/README.md)
6. [../control/README.md](../control/README.md)
7. [../evaluation/README.md](../evaluation/README.md)

## Write Scope

Во время этого прогона разрешено писать только в:

- `runtimes/claudecode/workspace/`
- `runtimes/claudecode/control/`
- `runtimes/claudecode/runs/`
- `runtimes/claudecode/evaluation/`

Нельзя изменять:

- `core/`
- `comparison/`
- `runtimes/codex/`
- центральный `control_plane/`

## Что именно нужно сделать

В рамках `RUN-003 / GT-003` `Claude Code` должен:

1. диагностировать closeout inconsistency по raw artifacts;
2. выполнить repair так, чтобы локальные truth files были обновлены самим runtime;
3. оставить evidence recovery path как publishable artifacts;
4. не объявлять финальный success без closeout revalidation;
5. участвовать в final hold reconciliation после repair;
6. обновить evaluation и learning artifacts так, чтобы было видно:
   - где был closeout drift;
   - как runtime его исправил;
   - почему terminal closeout теперь корректен.

## Что считается хорошим результатом

Хороший результат — это локальный runtime trace, по которому видно:

- в чём был разрыв closeout;
- какую repair-oriented directive увидел runtime;
- какие truth artifacts он обновил сам;
- как был подтверждён final hold после repair.

## Что считать недопустимым

Недопустимо:

- observer-side переписывание runtime-local truth files как способ закрыть benchmark;
- финальный success без recovery trace;
- отсутствие runtime-authored repair evidence;
- narrative closeout без артефактов;
- запись вне своей runtime-sandbox.

## Формат результата прогона

После завершения `RUN-003` должны быть обновлены:

- `runtimes/claudecode/control/`
- `runtimes/claudecode/workspace/`
- `runtimes/claudecode/runs/`
- `runtimes/claudecode/evaluation/`

И отдельно должен существовать run summary с:

- описанием closeout inconsistency;
- перечислением runtime-authored repair artifacts;
- указанием, где лежит revalidation trace;
- указанием, где лежит evidence final hold reconciliation.
