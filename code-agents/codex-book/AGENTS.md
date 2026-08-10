# Codex Book Instructions

## Scope

These instructions apply to:
- `code-agents/codex-book`

## Goal

Build a full, self-sufficient book on Codex for non-technical readers.
This is not a developer manual.
This is not a terse outline.
This is not a glossary with fragments.
Each chapter should read like part of a practical book.

## Audience

- Non-programmers
- Domain experts
- People who may freeze on every unfamiliar interface detail

## Core Writing Standard

Whenever the text says that the user should do something, explain:
- where they are on the screen
- what they should see
- what button or UI element to look for
- what may be written on that button
- what should happen after clicking
- what to do if they do not see the expected thing

## Chapter Structure

Each chapter should include:
- who the chapter is for
- what the reader will be able to do after it
- conceptual explanation in simple language
- detailed practical steps
- bad and good examples
- common mistakes
- a practical exercise
- glossary
- reference links only as supporting material

## Workflow Rules

- One chapter = one file.
- After each new chapter, update:
  - `code-agents/codex-book/README.md`
  - root `README.md`
- Keep the chapter self-sufficient.
- Do not require the reader to leave the chapter to understand the chapter.

## Style Rules

- Plain Russian
- Calm, precise, non-hype tone
- No unnecessary developer slang
- No "just do X" without interface explanation
- No hidden assumptions about Git, terminal, IDEs, or repo structure

## Autonomy Rules

- Continue through P1 backlog items without asking after every chapter.
- Pause only for editorial forks, scope changes, or uncertainty that would change the book's structure.

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
