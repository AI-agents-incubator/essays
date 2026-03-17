# Autonomy Model

Autonomy level: controlled autonomy within sandbox boundaries.

Allowed autonomous actions:
- Create and update artifacts inside the sandbox.
- Create run traces and evaluation traces.
- Update the local state layer schema and registry.

Escalation required:
- Any changes to `core/` source-of-truth documents.
- Any writes outside the allowed sandbox scope.
- Any structural changes that remove required GT-001 artifacts.

Autonomy constraints:
- Follow the bootstrap sequence before making structure changes.
- Record every cross-stage handoff in `execution/handoff_log.md`.
- Log benchmark and learning outcomes after execution completion.
