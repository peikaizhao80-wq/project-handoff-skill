# Handoff Checklist

## Closeout Checklist

Use this before publishing `LATEST.md`.

1. Confirm the goal is named explicitly.
2. State whether the session ended `done`, `partial`, `blocked`, or `unknown`.
3. Name the files changed or inspected that matter for the next step.
4. Separate verified facts from assumptions.
5. Record test or validation status honestly.
6. Record blockers, missing data, approvals, or environment constraints.
7. Give the next agent a first action, not just a vague direction.
8. Publish the finished snapshot into `LATEST.md`.

## Takeover Checklist

Use this before acting on the prior packet.

1. Read `LATEST.md` first.
2. Check whether a newer timestamped snapshot exists.
3. Verify that the key files still exist.
4. Check workspace drift with `git status` or equivalent inspection.
5. Re-check the most critical claim if it is cheap, risky, or likely to have changed.
6. Call out contradictions between the handoff and the current workspace.
7. Decide the first next action before doing broader exploration.

## Drift Heuristics

Re-verify these first because they go stale quickly:

1. Test results
2. Running services or ports
3. Generated artifacts
4. Branch or PR status
5. Temporary workarounds
6. Pending approvals or secrets

## Quality Bar

A useful handoff lets a new agent answer these questions quickly:

1. What is the actual goal?
2. What is already finished?
3. What is still risky or blocked?
4. Where in the code or files should I look first?
5. What should I do next?
