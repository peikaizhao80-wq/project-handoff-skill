---
name: project-handoff
description: Create and consume structured project handoff packets between agents. Use when any coding agent finishes a project, task, bugfix, feature branch, or investigation and needs to leave a precise progress summary for the next agent, or when a new agent needs to resume from the latest handoff with minimal rediscovery. Trigger on requests to write a handoff, summarize project progress, record current status, continue from previous work, read the last agent's notes, resume an interrupted task, or bootstrap context in an unfamiliar workspace.
---

# Project Handoff

## Overview

Use this skill in two modes:

1. `closeout`: create a new handoff packet at the end of a work session.
2. `takeover`: load the latest handoff packet, verify what is still true, and continue work.

Prefer a stable handoff location inside the project so future agents do not need to guess where context lives.

Treat the handoff packet as an agent-neutral protocol:

1. Keep the packet format plain Markdown plus a small JSON manifest.
2. Make sure another agent can read it without this skill, this repo, or Codex-specific memory.
3. Use tooling to generate the packet if helpful, but keep the packet itself portable.

## Canonical Location

Use the bundled script to resolve the handoff directory:

```powershell
python scripts/handoff_packet.py prepare-closeout --project-root <PROJECT_ROOT>
python scripts/handoff_packet.py prepare-takeover --project-root <PROJECT_ROOT>
```

Directory selection rules:

1. Use `<PROJECT_ROOT>/work/agent-handoff/` when `<PROJECT_ROOT>/work/` already exists.
2. Otherwise use `<PROJECT_ROOT>/.agent-handoff/`.
3. If an older `<PROJECT_ROOT>/.codex-handoff/` already exists, treat it as a legacy location and keep using it until explicitly migrated.

Keep these files there:

1. `LATEST.md`: stable entrypoint for the next agent.
2. `handoff-YYYYMMDD-HHMMSS-<slug>.md`: immutable snapshots.
3. `manifest.json`: machine-readable pointer to the latest snapshot.

## Closeout Workflow

### Step 1: Gather only high-signal state

Inspect the current workspace before writing anything:

1. Identify the active goal and whether it is finished, partial, blocked, or unknown.
2. Check changed files, generated artifacts, test status, and unresolved risks.
3. Record only facts you verified in this session. Mark assumptions explicitly.

If the project is a git repo, inspect `git status`, recent diffs, and any relevant logs or test output. If it is not a git repo, inspect the files and artifacts that define the current state.

### Step 2: Scaffold the packet

Run:

```powershell
python scripts/handoff_packet.py prepare-closeout --project-root <PROJECT_ROOT> --title <SHORT_TITLE>
```

This creates a new snapshot file from `assets/handoff-template.md` and prints the exact paths to update.

### Step 3: Fill the mandatory sections

Write the snapshot so another agent can act without re-discovering basic context. Keep it compact, but do not omit decision-critical information.

Required sections:

1. `Goal and current status`
2. `What changed in this session`
3. `Files and artifacts that matter`
4. `Validation already run`
5. `Open issues, blockers, and risks`
6. `Recommended next actions`
7. `Commands, URLs, or evidence worth reusing`
8. `Assumptions that need re-checking`

Good handoffs are:

1. Specific about what is done and not done.
2. Honest about what was not tested.
3. Actionable enough that the next agent can pick the first next step in under five minutes.

Bad handoffs:

1. Narrative diaries.
2. Vague statements like "fixed some bugs".
3. Claims about tests or behavior that were not verified.

### Step 4: Publish the stable pointer

After finishing the snapshot, mirror it into `LATEST.md`:

```powershell
python scripts/handoff_packet.py publish-latest --project-root <PROJECT_ROOT> --source <SNAPSHOT_PATH>
```

Do not skip this step. The next agent should be able to start from `LATEST.md` without guessing which timestamped file is current.

## Takeover Workflow

### Step 1: Discover the latest handoff

Run:

```powershell
python scripts/handoff_packet.py prepare-takeover --project-root <PROJECT_ROOT>
```

Use the returned paths to read, in order:

1. `LATEST.md`
2. The latest timestamped snapshot
3. `manifest.json` if needed for metadata

If no handoff exists, create the directory, note that there is no prior packet, and proceed with normal project discovery.

### Step 2: Verify drift before trusting the packet

Treat every handoff as a starting hypothesis, not ground truth. Re-check the most drift-prone facts:

1. Confirm the key files still exist and still match the described role.
2. Re-check git status or equivalent workspace state.
3. Verify unresolved blockers are still unresolved.
4. Re-run or inspect the most important validation when cheap and safe.

Use `references/handoff-checklist.md` as the default verification checklist.

### Step 3: Build a resume summary

Before continuing, produce a short internal resume note with:

1. Facts confirmed from the handoff.
2. Facts that are stale, missing, or contradictory.
3. The first next action you will take.

Then continue the actual task instead of stopping at orientation.

## Writing Rules

Use imperative wording and compact sections.

1. Prefer bullets over long prose inside the handoff packet.
2. Include exact file paths, commands, branch names, issue numbers, ports, or URLs when relevant.
3. Mark unknowns with `Unknown:` instead of guessing.
4. Mark unrun validation with `Not run:` and explain why.
5. Keep the handoff focused on the next agent's decisions, not on retrospective storytelling.

## Resources

### `scripts/handoff_packet.py`

Use this script to:

1. Resolve the canonical handoff directory.
2. Create timestamped snapshot drafts from the template.
3. Publish a snapshot to `LATEST.md`.
4. Discover the latest packet during takeover.

### `assets/handoff-template.md`

Use this template as the starting structure for each snapshot.

### `references/handoff-checklist.md`

Read this when you need a stricter checklist for closeout quality or takeover verification.

### `references/agent-neutral-contract.md`

Read this when you need to preserve compatibility across different agents, orchestrators, or local workflows.
