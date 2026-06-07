# Project Handoff Skill

`project-handoff` is a Codex skill for agent-to-agent project continuity.

It gives one agent a repeatable way to leave a structured handoff packet at the end of a work session, and gives the next agent a consistent way to resume from the latest handoff before continuing work.

## What It Solves

Without a handoff, a new agent usually has to rediscover:

- what the actual goal was
- what changed in the last session
- which files matter
- what was validated
- what is still risky or blocked
- what the very next action should be

This skill standardizes that process with:

- a `closeout` workflow for writing a handoff
- a `takeover` workflow for reading and verifying the latest handoff
- a canonical handoff directory inside the project
- a stable `LATEST.md` pointer plus timestamped snapshots

## Repository Layout

```text
.
├─ SKILL.md
├─ agents/openai.yaml
├─ assets/handoff-template.md
├─ references/handoff-checklist.md
└─ scripts/handoff_packet.py
```

## Install

Copy this repository into your Codex skills directory so the folder name is exactly `project-handoff`.

Typical location:

```text
~/.codex/skills/project-handoff
```

On this Windows setup, that would be:

```text
C:\Users\<you>\.codex\skills\project-handoff
```

## How To Call It

Use the skill explicitly in Codex:

```text
Use $project-handoff to write a handoff for this workspace before ending.
```

```text
Use $project-handoff to resume from the latest handoff in this workspace and continue the task.
```

Chinese examples:

```text
用 $project-handoff 给当前项目写一份交接总结，方便下一个 agent 接手
```

```text
用 $project-handoff 读取这个项目最新的交接记录，然后继续接手做下去
```

## Handoff Output

The skill prefers one of these project-local locations:

1. `<PROJECT_ROOT>/work/agent-handoff/`
2. `<PROJECT_ROOT>/.codex-handoff/`

Inside that directory it manages:

- `LATEST.md`
- `handoff-YYYYMMDD-HHMMSS-<slug>.md`
- `manifest.json`

## Script Helpers

The bundled script can scaffold and publish handoff packets:

```powershell
python scripts/handoff_packet.py prepare-closeout --project-root <PROJECT_ROOT> --title <SHORT_TITLE>
python scripts/handoff_packet.py publish-latest --project-root <PROJECT_ROOT> --source <SNAPSHOT_PATH>
python scripts/handoff_packet.py prepare-takeover --project-root <PROJECT_ROOT>
```

## Design Notes

The skill is optimized for:

- concise but decision-useful handoffs
- explicit validation status
- clear next actions
- low rediscovery cost for the next agent

It is intentionally not a diary or retrospective tool.

## License

MIT
