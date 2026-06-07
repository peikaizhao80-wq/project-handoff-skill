# Project Handoff Skill

`project-handoff` is a Codex-packaged skill built around an agent-neutral handoff format.

One agent can use it to leave a structured project handoff at the end of a work session, and the next agent can use the same packet to resume work with minimal rediscovery. The packet format itself is portable: plain Markdown plus a tiny JSON manifest that any agent can read.

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

## Agent Compatibility

This repository is packaged as a Codex skill, but the handoff protocol is designed to work across agents:

- Codex can call it directly as a skill
- other agents can read and write the same `LATEST.md` and snapshot files
- the handoff format avoids hidden state, proprietary storage, or model-specific fields
- the manifest is plain JSON so orchestration tools can index the latest snapshot

In practice, that means you can use this repo as:

- a native Codex skill
- a reusable handoff convention for any CLI agent
- a lightweight protocol between multiple agents working in the same project

## Repository Layout

```text
.
├─ SKILL.md
├─ agents/openai.yaml
├─ assets/handoff-template.md
├─ references/handoff-checklist.md
├─ references/agent-neutral-contract.md
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

If you are not using Codex, you can still adopt the same handoff format and helper script in any agent workflow that can read and write Markdown files.

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

Generic non-Codex usage:

```text
Read work/agent-handoff/LATEST.md, verify drift, then continue the task from the recorded next actions.
```

## Handoff Output

The skill prefers one of these project-local locations:

1. `<PROJECT_ROOT>/work/agent-handoff/`
2. `<PROJECT_ROOT>/.agent-handoff/`

Legacy fallback:

- `<PROJECT_ROOT>/.codex-handoff/`

Inside that directory it manages:

- `LATEST.md`
- `handoff-YYYYMMDD-HHMMSS-<slug>.md`
- `manifest.json`

These files are intentionally simple so any agent can consume them without extra tooling.

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

Compatibility rules:

- keep the packet human-readable first
- keep the manifest machine-readable second
- avoid agent-specific fields in the packet body unless clearly labeled
- prefer stable file paths and section names

It is intentionally not a diary or retrospective tool.

## License

MIT
