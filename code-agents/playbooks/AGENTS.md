# Playbooks Instructions

## Scope

These instructions apply to:
- `code-agents/playbooks`

## Goal

Build self-sufficient practical playbooks for non-technical readers.
Each playbook should help the reader complete one real scenario without needing to reconstruct the process.

## Audience

- Non-programmers
- Domain experts
- Readers who need explicit interface guidance

## Parent Layer Note

This repository does not use a section-level `2_lessons` layer anymore.
For work inside `code-agents/playbooks`, this local file is the primary authoring layer.
Use the repository root [README.md](../../README.md) as the upper repo context.

## Writing Rules

- Plain Russian
- Calm, precise tone
- One playbook = one scenario
- Explain interface actions literally
- When useful, separate steps for Codex and Claude Code
- Prefer practical action over abstract theory

## Structure

Each playbook should include:
- who it is for
- when to use it
- what result the reader should expect
- preparation
- detailed steps
- examples of prompts
- common mistakes
- exercise
- glossary
- source links as supporting material

## Session Startup Rule

If a new session starts directly inside `code-agents/playbooks`, first read:
1. `AGENTS.md`
2. `SESSION-HANDOFF.md`
3. `BACKLOG.md`
4. `README.md`
5. `../../README.md`

Then resume from the nearest unfinished playbook.

## Autonomy Rule

- Continue by backlog without micro-confirmations
- Update readmes and indexes after meaningful additions
- Pause only on structural forks, conflicts, or real risk

## Pipeline Model Selection

- When a pipeline/API model choice arises, consult [GPT-5.6 Model Selection Guide](/Users/alexeykrolmini/Code/GPT-5.6-model-selection-guide-ru.md), map its **Model × Reasoning** recommendation to the provider/model supported by this project, and do not default to mini/nano by habit.
- For a cross-provider audit or model-refresh recommendation, read [Pipeline Model-Selection Handoff](/Users/alexeykrolmini/Code/CLAUDE_CODE_PIPELINE_MODEL_SELECTION_HANDOFF.md), ground it in live code and current official provider documentation, and return a read-only evaluation plan before changing any runtime route.

<!-- BEGIN: CODEX_AUTONOMOUS_ORCHESTRATION -->
## Autonomous Orchestration

This project inherits the global Codex orchestration policy from
`/Users/alexeykrolmini/.codex/AGENTS.md`.

- Codex is the orchestrator and integrator for work inside the approved scope:
  it owns decomposition, session/sub-agent creation, supervision, evidence
  review, integration, verification, and session lifecycle.
- Create parallel or successor sessions whenever independent ownership,
  worktree isolation, assurance, long-running work, recovery, or context
  separation makes them useful. Transcript capacity is only one trigger.
- Use `/Users/alexeykrolmini/.codex/skills/handoff/SKILL.md` for task charters,
  continuations, recovery, and silent control-plane rollover. The user is not
  responsible for copying prompts or coordinating sessions.
- Preserve one accountable controller/integrator, one writer for shared
  contracts, unrelated dirty-tree work, and truthful evidence states.
- Stop for explicit Product Owner approval before any production mutation or
  spending action unless an applicable strict pre-approved strategy states the
  exact targets, limits, expiry, evidence, rollback, and remaining stop gates.
- Project rules may narrow authority or add checks; they do not transfer routine
  orchestration and integration mechanics back to the user.

<!-- END: CODEX_AUTONOMOUS_ORCHESTRATION -->
