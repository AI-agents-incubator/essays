# RUN-004: Claude Code Launch Brief for GT-004

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `execution launch brief`
> Основание:
> - [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
> - [../../../agent_org_tz_claudecode.md](../../../agent_org_tz_claudecode.md)
> - [../../../core/benchmarks/GT-004-no-mid-wave-operator-tuning.md](../../../core/benchmarks/GT-004-no-mid-wave-operator-tuning.md)
> - [../../../core/expected_results/GT-004-expected_result.md](../../../core/expected_results/GT-004-expected_result.md)
>

## Цель прогона

Выполнить `GT-004` для `Claude Code` внутри `runtimes/claudecode/` так, чтобы весь benchmark wave прошёл на frozen operational contracts, без mid-wave operator tuning.

## Порядок чтения перед запуском

Перед началом реализации агент должен прочитать материалы в таком порядке:

1. [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
2. [../../../agent_org_tz_claudecode.md](../../../agent_org_tz_claudecode.md)
3. [../../../core/benchmarks/GT-004-no-mid-wave-operator-tuning.md](../../../core/benchmarks/GT-004-no-mid-wave-operator-tuning.md)
4. [../../../core/expected_results/GT-004-expected_result.md](../../../core/expected_results/GT-004-expected_result.md)
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
- `CLAUDE.md`
- `OPERATOR_PROMPT.md`
- benchmark и expected-result документы

## Что именно нужно сделать

В рамках `RUN-004 / GT-004` `Claude Code` должен:

1. пройти wave на уже заданных правилах;
2. не менять управляющие контракты по ходу работы;
3. использовать только те repair и closeout paths, которые уже предусмотрены baseline;
4. честно оформить terminal outcome, даже если это не full success;
5. оставить evidence того, что contracts действительно оставались frozen;
6. обновить evaluation и learning artifacts так, чтобы было видно:
   - достаточно ли было исходных правил;
   - где система упёрлась;
   - что надо менять уже после wave.

## Что считается хорошим результатом

Хороший результат — это не обязательно success любой ценой.

Хороший результат — это честный terminal outcome, достигнутый на frozen contracts и без mid-wave operator tuning.

## Что считать недопустимым

Недопустимо:

- менять `CLAUDE.md`, prompts или protocol semantics по ходу wave;
- спасать benchmark ручной подстройкой правил;
- объявлять success, если он достигнут за счёт mid-wave rescue;
- писать вне своей runtime-sandbox.

## Формат результата прогона

После завершения `RUN-004` должны быть обновлены:

- `runtimes/claudecode/control/`
- `runtimes/claudecode/workspace/`
- `runtimes/claudecode/runs/`
- `runtimes/claudecode/evaluation/`

И отдельно должен существовать run summary с:

- описанием frozen contracts;
- перечислением terminal outcome;
- указанием, были ли попытки bounded repair;
- указанием, где лежит evidence отсутствия mid-wave tuning.
