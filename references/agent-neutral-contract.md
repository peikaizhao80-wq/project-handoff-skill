# Agent-Neutral Contract

Use this contract when the handoff must remain usable across different agents or orchestration systems.

## Required invariants

1. Keep the handoff body in plain Markdown.
2. Keep the pointer metadata in plain JSON.
3. Keep the section names stable unless there is a migration note.
4. Use explicit facts, not hidden memory or agent-local assumptions.
5. Record unknowns and unverified claims clearly.

## Packet contract

Every published handoff should preserve these sections:

1. `Goal and current status`
2. `What changed in this session`
3. `Files and artifacts that matter`
4. `Validation already run`
5. `Open issues, blockers, and risks`
6. `Recommended next actions`
7. `Commands, URLs, or evidence worth reusing`
8. `Assumptions that need re-checking`

## Compatibility guidance

When adding agent-specific notes:

1. Label them clearly, for example `Agent-specific note:`.
2. Keep them optional rather than central to the packet.
3. Do not replace shared facts with framework-specific shorthand.

## Drift policy

The next agent should assume:

1. goals may still be valid
2. validation may be stale
3. running services or ports may have changed
4. temporary files may no longer exist

So the packet should optimize for re-verification, not blind trust.
