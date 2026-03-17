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
