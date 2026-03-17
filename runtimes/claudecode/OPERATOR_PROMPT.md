# Claude Code Operator Prompt

Скопируйте этот текст как первое сообщение в отдельный тред для `Claude Code`.

```text
Работай только внутри /Users/alexeykrolmini/Code/essays/runtimes/claudecode/.

Сначала прочитай:
1. /Users/alexeykrolmini/Code/essays/runtimes/claudecode/workspace/CLAUDE.md
2. /Users/alexeykrolmini/Code/essays/runtimes/claudecode/runs/CURRENT_MISSION.md

После этого автономно выполни текущую mission.

Правила:
- пиши только в /Users/alexeykrolmini/Code/essays/runtimes/claudecode/workspace/, /Users/alexeykrolmini/Code/essays/runtimes/claudecode/runs/ и /Users/alexeykrolmini/Code/essays/runtimes/claudecode/evaluation/
- не меняй /Users/alexeykrolmini/Code/essays/core/, /Users/alexeykrolmini/Code/essays/comparison/ и /Users/alexeykrolmini/Code/essays/runtimes/codex/
- не проси у меня пошагового управления, если только не возникла критическая неопределённость или policy-блокер
- работай как автономный runtime внутри уже заданной архитектуры

В конце оставь:
- run summary
- evaluation trace
- обновление state layer
- краткое описание следующего рекомендуемого run
```
