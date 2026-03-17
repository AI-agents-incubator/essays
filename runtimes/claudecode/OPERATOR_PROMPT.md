# Claude Code Operator Prompt

Скопируйте этот текст как первое сообщение в отдельный тред для `Claude Code`.

```text
Работай только внутри /Users/alexeykrolmini/Code/essays/runtimes/claudecode/.

Сначала прочитай:
1. /Users/alexeykrolmini/Code/essays/runtimes/claudecode/workspace/CLAUDE.md
2. /Users/alexeykrolmini/Code/essays/runtimes/claudecode/runs/CURRENT_MISSION.md
3. /Users/alexeykrolmini/Code/essays/runtimes/claudecode/runs/RUNTIME_STATUS.md
4. /Users/alexeykrolmini/Code/essays/runtimes/claudecode/control/observer_runtime_protocol.md
5. /Users/alexeykrolmini/Code/essays/runtimes/claudecode/control/OBSERVER_DIRECTIVE.md
6. /Users/alexeykrolmini/Code/essays/runtimes/claudecode/control/RUNTIME_ACK.md

После этого автономно выполни текущую mission.

Правила:
- пиши только в /Users/alexeykrolmini/Code/essays/runtimes/claudecode/workspace/, /Users/alexeykrolmini/Code/essays/runtimes/claudecode/runs/, /Users/alexeykrolmini/Code/essays/runtimes/claudecode/evaluation/ и /Users/alexeykrolmini/Code/essays/runtimes/claudecode/control/
- не меняй /Users/alexeykrolmini/Code/essays/core/, /Users/alexeykrolmini/Code/essays/comparison/ и /Users/alexeykrolmini/Code/essays/runtimes/codex/
- не проси у меня пошагового управления, если только не возникла критическая неопределённость или policy-блокер
- работай как автономный runtime внутри уже заданной архитектуры
- веди /Users/alexeykrolmini/Code/essays/runtimes/claudecode/runs/RUNTIME_STATUS.md как главный статус run
- веди /Users/alexeykrolmini/Code/essays/runtimes/claudecode/control/RUNTIME_ACK.md как локальное подтверждение observer directive
- не начинай новый run без observer directive
- если я спрашиваю тебя о текущем состоянии, перед ответом заново перечитай `RUNTIME_STATUS.md`, `OBSERVER_DIRECTIVE.md` и `RUNTIME_ACK.md`; не отвечай по памяти сессии

В конце оставь:
- run summary
- evaluation trace
- обновление state layer
- краткое описание следующего рекомендуемого run
- финальный статус в RUNTIME_STATUS.md
- обновлённый RUNTIME_ACK.md
```
