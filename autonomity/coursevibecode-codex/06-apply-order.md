# Apply Order For Coursevibecode

This file explains in what order to apply the templates to the real project.

## Recommended Order

### Step 1. User-level Codex config

Apply first:
- `01-user-config-template.toml`

Target:
- `~/.codex/config.toml`

Why first:
- it defines the global autonomy baseline
- it controls approvals, sandbox, model, and trust

What to verify after applying:
- the project `/Users/alexeykrolmini/Code/coursevibecode` is trusted
- `approval_policy = "never"`
- `sandbox_mode = "workspace-write"`

### Step 2. Project-level config

Apply second:
- `02-project-config-template.toml`

Target:
- `/Users/alexeykrolmini/Code/coursevibecode/.codex/config.toml`

Why second:
- it sharpens behavior specifically for this repository
- it avoids pushing project-specific policy into the global user config

What to verify after applying:
- the file exists
- Codex is opening the trusted project
- the project-level overrides are being used

### Step 3. Root instructions

Apply third:
- `03-root-agents-template.md`

Target:
- `/Users/alexeykrolmini/Code/coursevibecode/AGENTS.md`

Why third:
- it resets the repo’s main behavioral contract around course authoring
- it aligns Codex with the actual goal of this repository

Warning:
- the current root `AGENTS.md` contains framework-adapter instructions
- replacing it should be done carefully
- you may prefer to merge rather than overwrite

### Step 4. Narrow book instructions

Apply fourth:
- `04-codex-book-agents-template.md`

Target:
- `/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/AGENTS.md`

Why fourth:
- narrow instructions are safer than global ones
- Codex reads nearer `AGENTS.md` files later in the chain, so these can override broader rules for the book area

### Step 5. Backlog

Apply fifth:
- `05-codex-book-backlog-template.md`

Suggested target:
- `/Users/alexeykrolmini/Code/coursevibecode/2_lessons/codex-book/BACKLOG.md`

Why fifth:
- this is what turns “general autonomy” into “ordered autonomous execution”

## Practical Rule

Do not apply all files at once blindly.
Apply one layer, verify behavior, then move to the next.
