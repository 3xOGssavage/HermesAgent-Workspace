---
name: memory-pending-triage
description: Triage /memory pending under box caps.
version: 1.0.0
author: Neohelper
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [Memory, Triage, Approvals]
    related_skills: [lstm-bridge, obsidian]
---

# Memory Pending Triage

Built-in memory has hard per-box character caps. Approving into a full box fails, and rejecting pendings never frees saved space. Triage before approving.

## When to Use

The pending queue is long, approvals fail on box size, staged writes need dedupe, or the owner asks what each pending item is about.

## Procedure

1. Measure first: byte-count both box files and sum the payload sizes of everything planned for approval. Never approve blind into a box with less free space than the payload.
2. Read every pending item's full content — the pending list shows truncated summaries, so open the backing store. Group by topic, never present a long queue as a flat list.
3. Classify each group: KEEP (new fact), MERGE (same fact as another pending or a saved line — keep one, reject the rest), STALE (superseded by a later decision — reject), SKILL-RESIDENT (already lives in a skill file, which has no size limit — reject from memory, it costs box space for zero gain).
4. Resolve conflicts before approving: when two pendings say opposite things, present both with sources and let the owner pick; never approve both.
5. Compress before filling: if the box cannot hold the keepers, stage ONE combined batch per box that patches (shortens) saved lines and adds the new lines together — the cap is checked on the batch result, so shrink-plus-add in one batch passes where add-alone fails. Approve compressions first, in dependency order.
6. Approve in size order: compressions, then small keepers, then large ones. If any approve fails on size, STOP and shrink further — do not keep approving around the failure.
7. Verify after: re-read both box files and confirm the final content holds every kept fact.

## Pitfalls

- Patch spans must match the live file byte-for-byte — re-read the box files right before staging a compression batch, because earlier approvals in the same session already changed them.
- Rejecting a pending write never frees saved space; only a patch (shorten) or remove on a saved entry does, and only inside an approved batch.
- Type slash commands with no space after the slash — a space after / triggers command search instead of running.
- Related but separate: the shared vault (lstm-bridge) is read-only with its own proposal path — never mix vault edits into a box-triage batch.
