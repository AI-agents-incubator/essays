# Claude Code Baseline Manifest

> Версия baseline: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `baseline manifest`

## Пакет метафайлов

### 1. Instruction layer

- `CLAUDE.md`

### 2. Runtime settings

- `.claude/settings.json`

### 3. Governance layer

- `.claude/rules/governance.md`
- `.claude/hooks/README.md`

### 4. Baseline agents

- `.claude/agents/org-bootstrap.md`
- `.claude/agents/product-lead.md`
- `.claude/agents/engineering-manager.md`
- `.claude/agents/integration-reviewer.md`
- `.claude/agents/benchmark-auditor.md`
- `.claude/agents/learning-coordinator.md`

### 5. Baseline skills

- `.claude/skills/org-intake.md`
- `.claude/skills/brief-to-spec.md`
- `.claude/skills/task-graph-sync.md`
- `.claude/skills/golden-task-audit.md`
- `.claude/skills/change-proposal-review.md`

## Default autonomy profile

- language: `russian`
- permissions default mode: `acceptEdits`
- bypass permissions mode: `disabled`
- sandbox enabled: `true`
- auto allow bash if sandboxed: `true`
- unsandboxed commands: `false`

## Security invariants

- `.claude/settings.local.json` is treated as a local override file, not a secrets file
- permission approvals must stay secret-free
- inline credentials must never be normalized into persistent permission entries
- repository policy should protect `.claude/settings.local.json` from git
- preflight should audit local permission state before long autonomous runs

## Комментарий

Это baseline-профиль "автономность внутри контролируемой песочницы".

Если проект требует дополнительных ограничений, они накладываются поверх baseline через project overlay.
