# Runtime Status: Codex

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `runtime signal`

- runtime: `Codex`
- current_run: `RUN-007`
- status: `completed`
- started_at: `2026-03-17 13:09:31 PDT`
- updated_at: `2026-03-17 13:28:10 PDT`
- summary_file: `runs/RUN-007_projection_watcher_adaptive_refresh_summary.md`
- evaluation_file: `evaluation/RUN-007_projection_watcher_adaptive_refresh_evaluation.md`
- needs_human: `no`
- next_run: `none`
- blocking_issue: `none`

## Правило

Этот файл является главным сигналом состояния для наблюдателя.

Агент обязан:

- перевести `status` в `in_progress` при старте работы;
- обновлять `updated_at` при изменении состояния;
- перевести `status` в `completed`, `blocked`, `escalation_required` или `failed` при завершении run;
- заполнить `summary_file` и `evaluation_file`, если run завершён с артефактами.
