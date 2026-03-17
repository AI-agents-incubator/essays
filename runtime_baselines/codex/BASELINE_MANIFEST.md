# Codex Baseline Manifest

> Версия baseline: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `baseline manifest`

## Пакет метафайлов

### 1. Instruction layer

- `AGENTS.md`

### 2. Runtime config

- `.codex/config.toml`

### 3. Baseline agents

- `.codex/agents/org-bootstrap.md`
- `.codex/agents/product-lead.md`
- `.codex/agents/engineering-manager.md`
- `.codex/agents/integration-reviewer.md`
- `.codex/agents/benchmark-auditor.md`
- `.codex/agents/learning-coordinator.md`

### 4. Baseline skills

- `.agents/skills/org-intake.md`
- `.agents/skills/brief-to-spec.md`
- `.agents/skills/task-graph-sync.md`
- `.agents/skills/golden-task-audit.md`
- `.agents/skills/change-proposal-review.md`

## Default autonomy profile

- model: `gpt-5.4`
- reasoning: `high`
- approval policy: `never`
- sandbox: `workspace-write`
- network access in workspace sandbox: `false`
- max threads: `6`
- max depth: `2`

## Комментарий

Это baseline-профиль "сначала готовность к автономной работе".

Если проект требует более жёсткой безопасности, baseline не отменяется, а сужается project overlay-слоем.
