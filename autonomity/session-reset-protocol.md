# Session Reset Protocol

## Purpose

This protocol is used when agent autonomy has visibly started to drift during a long session.

## Core Principle

Reset is not a cosmetic step.
It is a control mechanism for restoring the working contract.

## Soft Reset

Use a reset prompt inside the current session when:
- drift is still mild;
- the agent only started to over-ask or lose step slightly;
- the session is still mostly coherent.

Expected result:
- the operating contract returns to the top of active attention.

Limit:
- soft reset does not remove accumulated session noise.

## Hard Reset

Start a new session when:
- autonomy drift is already visible;
- the agent keeps asking unnecessary questions after reset;
- the session has too many side branches;
- the next phase is important enough to deserve a clean baseline.

Expected result:
- base instructions, handoff files, and backlog become primary context again.

## Recommended Sequence

1. Detect drift.
2. Try one short soft reset.
3. If autonomy does not recover in 1-2 turns, start a new session.
4. In the new session, use explicit handoff files and a preflight prompt.

## Preflight Checklist For New Session

- correct project path
- correct active folder
- local `AGENTS.md`
- local `BACKLOG.md`
- session handoff file
- explicit next resume point
- explicit stop rule

## Rule Of Thumb

If the question is important enough to ask whether reset is needed, hard reset is often the safer choice.
