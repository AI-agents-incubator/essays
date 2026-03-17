# Runtime Status: Codex

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `runtime signal`

- runtime: `Codex`
- current_run: `RUN-002`
- status: `planned`
- started_at: `not_started`
- updated_at: `2026-03-17`
- summary_file: `not_set`
- evaluation_file: `not_set`
- needs_human: `no`
- next_run: `not_set`
- blocking_issue: `none`

## Правило

Этот файл является главным сигналом состояния для наблюдателя.

Агент обязан:

- перевести `status` в `in_progress` при старте работы;
- обновлять `updated_at` при изменении состояния;
- перевести `status` в `completed`, `blocked`, `escalation_required` или `failed` при завершении run;
- заполнить `summary_file` и `evaluation_file`, если run завершён с артефактами.
