# Claude Code Baseline Package

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `runtime baseline package`
> Runtime: `Claude Code`

## Что это

Это baseline-пакет метафайлов для `Claude Code`.

Он нужен для того, чтобы новый `Claude Code`-runtime не стартовал с пустого состояния, а сразу получал:

- instruction layer;
- settings layer;
- governance layer;
- baseline agents;
- baseline skills;
- автономный режим работы по умолчанию.

## Профиль baseline

Этот baseline-профиль рассчитан на:

- высокую автономность;
- sandbox-on поведение;
- отказ от unsandboxed commands по умолчанию;
- project-ready instruction layer;
- готовый governance-контур через rules и hooks.
- secret-free permission layer по умолчанию.

## Основные файлы

- [CLAUDE.md](./CLAUDE.md)
- [.claude/settings.json](./.claude/settings.json)
- [BASELINE_MANIFEST.md](./BASELINE_MANIFEST.md)

## Что восстанавливать

При установке baseline в новый runtime должны восстанавливаться:

- `CLAUDE.md`
- `.claude/settings.json`
- `.claude/rules/`
- `.claude/hooks/`
- `.claude/agents/`
- `.claude/skills/`

## Что идёт поверх baseline

Поверх этого baseline уже накладывается project overlay:

- project-specific mission;
- project-specific status layer;
- project-specific entrypoint details;
- project-specific артефакты организации.

## Security invariant для local permissions

Для `Claude Code` baseline должен предполагать ещё одно обязательное правило:

- `.claude/settings.local.json` считается local override-файлом, а не местом хранения секретов;
- inline creds нельзя закреплять через `Allow`;
- репозиторий должен явно защищать `.claude/settings.local.json` от коммита;
- preflight должен проверять, что local permission layer не содержит secret-bearing command strings.
