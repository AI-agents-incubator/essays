# RUN-007: Claude Code Launch Brief for GT-007

> Версия файла: `v1.0`
> Дата версии: `2026-03-18`
> Тип документа: `execution launch brief`
> Основание:
> - [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
> - [../../../agent_org_tz_claudecode.md](../../../agent_org_tz_claudecode.md)
> - [../../../core/benchmarks/GT-007-runtime-authored-failure-package.md](../../../core/benchmarks/GT-007-runtime-authored-failure-package.md)
> - [../../../core/expected_results/GT-007-expected_result.md](../../../core/expected_results/GT-007-expected_result.md)
>

## Цель прогона

Выполнить `GT-007` для `Claude Code` внутри `runtimes/claudecode/` так, чтобы failed runtime до окончательного closeout сам оставил publishable failure package, пригодный для comparison и learning.

## Порядок чтения перед запуском

Перед началом реализации агент должен прочитать материалы в таком порядке:

1. [../../../agent_org_tz_core.md](../../../agent_org_tz_core.md)
2. [../../../agent_org_tz_claudecode.md](../../../agent_org_tz_claudecode.md)
3. [../../../core/benchmarks/GT-007-runtime-authored-failure-package.md](../../../core/benchmarks/GT-007-runtime-authored-failure-package.md)
4. [../../../core/expected_results/GT-007-expected_result.md](../../../core/expected_results/GT-007-expected_result.md)
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

В рамках `RUN-007 / GT-007` `Claude Code` должен:

1. если локальный успех невозможен, не ограничиваться голым failed state;
2. выпустить собственный structured failure package;
3. зафиксировать diagnosis, retry history, exhaustion reason и impacted artifacts;
4. оставить suggested next actions для следующей волны;
5. не мешать сохранению peer-success package;
6. обновить evaluation и learning artifacts так, чтобы failed ветка тоже была comparison-ready.

## Что считается хорошим результатом

Хороший результат — это не success любой ценой.

Хороший результат — это failed branch, которая оставляет качественный publishable package и не выпадает из общей аналитики.

## Что считать недопустимым

Недопустимо:

- закрыть failure только observer-side narrative;
- не оставить собственного failure package;
- стереть peer-success package;
- оставить failed ветку почти пустой по сравнению с successful peer.

## Формат результата прогона

После завершения `RUN-007` должны быть обновлены:

- `runtimes/claudecode/control/`
- `runtimes/claudecode/workspace/`
- `runtimes/claudecode/runs/`
- `runtimes/claudecode/evaluation/`

И отдельно должен существовать run summary с:

- описанием failure path;
- перечислением локальных failure artifacts;
- описанием связи с system-level closeout;
- указанием, где лежит comparison-ready failure package.
