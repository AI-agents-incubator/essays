# Codex Baseline Package

> Версия файла: `v1.0`
> Дата версии: `2026-03-17`
> Тип документа: `runtime baseline package`
> Runtime: `Codex`

## Что это

Это baseline-пакет метафайлов для `Codex`.

Он нужен для того, чтобы новый `Codex`-runtime не стартовал с пустого состояния, а сразу получал:

- instruction layer;
- config layer;
- baseline agents;
- baseline skills;
- autonomy-first настройки по умолчанию.

## Профиль baseline

Этот baseline-профиль рассчитан на:

- высокую автономность;
- работу внутри writable workspace;
- отключённую сеть по умолчанию;
- наличие нескольких параллельных agent threads;
- старт с уже подготовленным набором ролей и workflows.

## Основные файлы

- [AGENTS.md](./AGENTS.md)
- [.codex/config.toml](./.codex/config.toml)
- [BASELINE_MANIFEST.md](./BASELINE_MANIFEST.md)

## Что восстанавливать

При установке baseline в новый runtime должны восстанавливаться:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/agents/`
- `.agents/skills/`

## Что идёт поверх baseline

Поверх этого baseline уже накладывается project overlay:

- project-specific mission;
- project-specific status layer;
- project-specific entrypoint details;
- project-specific артефакты организации.
