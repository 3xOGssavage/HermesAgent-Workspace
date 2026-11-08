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
- Session-specific numbers (box sizes, pending counts, HEAD hashes) go stale within hours — re-measure in the turn you use them, never quote yesterday's. The pending queue changes under you while you compose (background reviews stage files, owner clicks land rejects), so recount it in the hand-over turn and regenerate any table whose membership changed.
- When the owner must click through a queue, hand the whole list as small tables with every ID verified present that same turn: ID, the exact slash command in click order, a plain-words description, and a plain-words reason that names where the fact already lives safe — because an owner who cannot see why will not click, and a bare ID list fails them. New arrivals since the last table go in explicitly, and any item contradicting a saved line is held out with the conflict stated, never smuggled into an approve or reject.
- After the owner runs a click sequence, confirm the set difference before reporting progress: list which IDs left the queue and verify the survivors are exactly the planned remainder — because a silent failure (wrong ID, skipped line) looks identical to success until the next recount. When a relayed click list arrives partially executed, recount the live queue first and hand only the verified remainder in locked order, never the stale full list.
- When the other board names a saved item your board cannot place (picks saved vs batch waiting), resolve by reading your own box lines and naming exact line numbers: never guess the mapping, never leave it in neither list — because an unmapped item slips exactly by being in neither Done nor Left.
- When the owner reports a shared channel or link as done with a screenshot, verify the channel name and server from the image, confirm hookup ownership (who configures delivery, who posts whose lines, what the first live test is) in the same turn — because a sighted channel without an agreed poster and test date leaves delivery unowned and the link silently dead.
- When the owner picks backlog keepers for a cross-agent veto, send keeper texts verbatim plus skill file with line or section plus rejected original IDs in the same turn — because names alone cannot be vetoed and stall the other board.
- When the owner says keep-all but standing locks forbid some, save what fits the locks and park the rest naming the lock, then ask the owner to confirm park or overrule — because silent defiance and silent over-saving both break trust while a named hold keeps the tie-break with the owner.
- When a shared spec is lost on both sides (grep proves zero verbatim hits), the author side re-authors labeled v2 from review record + schema + locked decisions, never restores as original — because retyping from memory repeats the paraphrase failure while a labeled v2 keeps verification honest.
- Harden delete-dated reminders to self-denying in the same turn they are kept: state the date asks for a fresh owner word plus gates and that the line alone never authorizes deletion — because a live box line reading as standing approval bypasses the explicit-word lock on the date.
- A guild-resolving invite proves server identity only, not channel write access — confirm stored channel webhook, scheduled poster, fallback, and one observed test post before declaring a hookup live, because a valid link with no write path leaves delivery silently dead.
- Label a shared % ledger as chat-agreement ruler unless a file holds it: grep the vault for the numbers before citing them as filed metric — because the other side will grep, find zero hits, and the number loses trust it did not need to lose.
- For cross-house file review, try the temp path first and report readable-or-not in one line, falling back to a shared-folder staged copy — because temp is fragile and possibly outside the other house's readable roots while the shared record stays readable to both.
- When one owner word could cover multiple gated steps, confirm the gated order in plain words before acting — because downstream steps read filed truth from upstream ones and running out of order rebuilds on unfiled temp.
