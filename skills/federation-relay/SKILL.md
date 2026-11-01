---
name: federation-relay
description: Use when relaying a second agent's output to the owner.
version: 1.0.0
author: Neohelper
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [relay, verification, multi-agent]
    related_skills: [memory-pending-triage]
---

# Federation Relay

Owner pastes the second agent's text plus screenshots; you verify every checkable claim against your own disk, then relay a paste-ready block back. Trust nothing from the text alone.

## When to Use

Every turn where the owner forwards another agent's output and expects verification, a decision route, or a forwardable reply.

## Procedure

1. Vision-check every attached image first — screenshots are provenance, and the text is usually complete without them; if an image fails to load, say so and rule from the text alone.
2. Verify each checkable claim on your own disk (file presence, sizes, box math, log lines) before accepting it — quote the disk result, not the text.
3. Track sequence explicitly: the latest owner word always supersedes earlier relays, and a reply aimed at an old relay is stale, not wrong — say which text it answered and re-relay the newer word.
4. Relay back as a verbatim paste-ready block the owner can forward untouched — no placeholders, no missing IDs.
5. Route owner decisions as plain-words choices with the recommendation first; if the owner says they did not understand, drop one level simpler with a concrete example and ask again — never re-ask the same wording. If the owner stalls on a multi-step procedure, stop listing steps and offer a single-step guided walkthrough — one yes-or-no per step started by a one-word reply — because a wall of IDs stalls a non-coder while one tap at a time moves.
6. Disclose your own errors in the open (wrong ID, paraphrased span, stale relay) with the fix in the same message — a found-by-you error reported by you costs nothing; a found-by-them error costs trust.

## Pitfalls

- Never approve or relay-approve a contradictory pair unreconciled — when two staged lines disagree, the owner picks one before either moves.
- A typo'd pending ID fails the click while the real dupe survives — run one existence check over the full reject/approve list in the same turn you compose it, and verify every ID exists on disk before handing the list over.
- Standing owner picks (rejects-first, no-expiry, named holds) ride along silently in every list — restate them when a condensed list could read as overriding them.
- Session-specific numbers (box sizes, pending counts, HEAD hashes) go stale within hours — re-measure in the turn you use them, never quote yesterday's.
