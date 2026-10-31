---
name: standing-goal
description: Use when executing a persistent standing goal.
version: 1.0.0
author: Neohelper
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [standing-goal, orchestration, research, delegation]
---

# Standing Goal Execution

A standing goal arrives as the same prompt every turn with a stop condition. Each turn is one concrete step forward, never a summary of intent.

## When to Use

Any persistent goal with a verification contract, time gates, and a stop-when clause: multi-round research, long audits, quota-driven sweeps.

## Procedure

1. Read the stop condition first. If it is already met (time passed plus deliverable verified), say so briefly and take no further action. Never fabricate work to look busy.
2. Each turn does exactly one concrete step: one verification, one patch batch, one fan-out, or one time check. End the turn after it lands.
3. Fan out with delegate_task at the widest allowed parallelism (10 tasks per round here). Give every child its full context; children know nothing of the conversation.
4. Log every round in the deliverable itself: delegation id, task list, completion state. Keep a time.log with start, each gate, and end entries from the time tool, never from memory.
5. Synthesize child results into the deliverable before the next round. Verify child claims on load-bearing points yourself; a child reporting success is not proof.
6. No installs, no edits outside the goal folder, no paid services unless the goal allows them.
7. Background batches arrive as separate messages — handle the unit that arrived (file its synthesis, log it, fan out the next round), then end the turn. Never poll transcripts or wait on siblings.

## Pitfalls

- Claiming done before the stop condition is fully met — the log must show the full span and the deliverable must exist and verify.
- Skipping a missed gate silently — log missed gates as missed with the reason, then continue; a gap in the log with no note reads as fabrication.
- Rewriting history after the fact — the log is append-only: user-ordered rounds after completion get dated EXTRA entries marked as outside the original box, never folded into it; user-caught factual corrections get a dated CORRECTION entry plus the patched line, never a silent edit.
- Repeating the plan instead of acting — a response that only describes next steps with no tool calls is a wasted turn.
- Trusting remembered file contents for patches — re-read the file fresh when a patch fails to match; stale memory of the text causes repeated failures.
- Overwriting a synthesis file a child already wrote — a write refusal means the child filed it first, so read it fresh and patch a header or extend it; never clobber a child's verified content with your own draft.
- Filing a name, repo path, or count you only saw mentioned inside another source — verify every identifier against its own live page before it enters the deliverable; a transitive mention is not a verification.
- Leaving child-filed companion files out of the round log — when helpers write extra files beside your synthesis, name each one in the log entry so nothing is orphaned.
- Answering a replayed goal prompt with invented progress to look busy — when the stop condition is met and there is no new input, the correct turn is a one-line complete-and-idle close, not a fake status update.
