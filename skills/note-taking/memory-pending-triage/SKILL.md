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

1. Measure first: byte-count both box files and sum the payload sizes of everything planned for approval. Never approve blind into a box with less free space than the payload. Simulate every staged batch before writing it: apply the planned ops to in-memory copies of both box files and assert the result fits the caps (run scripts/box_fit.py against the box files plus the pending JSON); stage only a fitting simulation, and re-simulate after every approve or reject since each action moves the boxes.
2. Read every pending item's full content — the pending list shows truncated summaries, so open the backing store. Group by topic, never present a long queue as a flat list.
3. Classify each group: KEEP (new fact), MERGE (same fact as another pending or a saved line — keep one, reject the rest), STALE (superseded by a later decision — reject), SKILL-RESIDENT (already lives in a skill file, which has no size limit — reject from memory, it costs box space for zero gain).
4. Resolve conflicts before approving: when two pendings say opposite things, present both with sources and let the owner pick; never approve both.
4b. Present lists to the owner as small ASCII tables with machine-checked equal widths (ID | DO | WHAT IT IS | WHY IN SIMPLE WORDS) plus the full `/memory approve <id>` / `/memory reject <id>` lines in click order: the owner is a non-coder who does not know most pendings, so each WHY states in simplest words what the note is and where its words already live safe. Define any A/B/C shorthand in full sentences every time (A = identity card, B = behavior card, C = settings card). State the safety rule behind every reject (rejects delete copies only; the original already sits in a batch, box, or skill file), and isolate any genuine contradiction — pending-vs-pending or pending-vs-saved-box — as its own owner question with no command attached until picked.
5. Compress before filling: if the box cannot hold the keepers, stage ONE combined batch per box that patches (shortens) saved lines and adds the new lines together — the cap is checked on the batch result, so shrink-plus-add in one batch passes where add-alone fails. Approve compressions first, in dependency order.
6. Approve in rejects-first order: run every planned reject BEFORE any approve, because an approved batch can resurrect a line a later reject was meant to kill (owner-locked forever rule: rejects first, always). Then approve in size order: compressions, then small keepers, then large ones. Re-measure free space and re-read the box files after every single approve or reject before staging or running the next one — each action changes the box, and spans valid one minute ago can already be stale. If any approve fails on size, STOP and shrink further — do not keep approving around the failure.
7. Verify after: re-read both box files and confirm the final content holds every kept fact.
8. Keeper-to-skill flow for backlog picks: when the owner keeps old notes but boxes are full, file short pointers in the governing skill file (verified written), leave boxes untouched, then reject the bulky originals — and build the cross-agent review package in the same turn (keeper texts verbatim + skill file + line/section + rejected IDs), because a name-only handoff cannot be vetoed and stalls the other board. Run backlog in rounds of 4 (one line each, reply numbers/all/none); each round holds read-first, save-safe-short, reject-bulky, park-secrets-or-duplicates — because one repeated pattern lets the other house veto same-turn without re-learning the rules.

## Pitfalls

- Patch spans must match the live file byte-for-byte — re-read the box files right before staging a compression batch, because earlier approvals in the same session already changed them.
- When a span misses, check the file mtime before blaming your transcription: if the mtime predates your last write the box never moved and the span is yours to fix from the fresh read; if the mtime is newer something else wrote first and every staged span needs re-deriving — because guessing which side moved wastes a rebuild cycle.
- Never hand-retype a patch span from memory — copy it character-for-character from the read output, because a paraphrased span looks right to the eye and fails only at apply time.
- When batches depend on each other (B patches A's output), simulate the whole chain in order with a per-op assert, never each batch alone — a batch that fits solo still breaks on a predecessor's changed text.
- A staged batch that was never approved can be withdrawn by deleting its pending file — disclose the withdrawal openly, rebuild from the live box, and treat the replacement as a brand-new file needing a fresh countersign, never as an edit of the old one.
- One patch op covers exactly one entry: the § separator is an entry boundary the matcher will not cross, so a span reaching across two entries always fails. To merge two entries, patch one of them to the combined text and remove the other in the same batch.
- A refused batch applies nothing — all-or-nothing. Read the failing op number and the closest-entries hint in the refusal, retry with that verbatim text, and converge on spans before growing the batch. The refusal's closest-entries text is authoritative over your own re-read: file display and tool store can differ subtly (parentheticals, punctuation), so when your byte-exact span still fails, copy the hint text character-for-character instead of re-typing from the file.
- Rejecting a pending write never frees saved space; only a patch (shorten) or remove on a saved entry does, and only inside an approved batch.
- Folding without a trace strands the queue: when a compression batch absorbs keeper facts, write the absorbed source pending IDs into the batch summary the same turn, because the follow-up reject pass can only drop what it can name — untraced folds leave duplicates the next triage must rediscover.
- Pending write IDs exist only in the pending store — never resolve one as a git revision, branch, or commit. A lookup miss in git proves nothing about the write; open the pending file by ID from the pending directory instead.
- Validate every ID in a hand-built approve/reject list against the pending directory before giving it to the owner — one mistyped character turns a reject into a 'not found' while the real dupe survives. Reconcile counts at the end: files on disk must equal IDs listed, zero missing, zero phantom.
- Session numbers go stale within hours — re-measure box sizes and pending counts in the turn you use them, never quote yesterday's measurement, because approvals, withdrawals, and background arrivals move every number.
- After the owner runs part of a click list, recount the live pending directory before handing the next list: confirm which IDs left, verify the survivors are exactly the planned remainder, and hand only the verified remainder in locked order — because a silent failure looks identical to success until the next recount, and re-handing the stale full list re-asks for done work.
- Every op in a staged batch must carry its entry pin (`matched_entry`): patch/remove ops pin the exact live entry they touch, add ops pin empty strings — a batch written without pins is refused at approve time as predating entry pinning, no matter how correct its spans are. Build pinned batches by machine-copying entries from the live read, never by retyping.
- Type slash commands with no space after the slash — a space after / triggers command search instead of running.
- When an owner-ordered memory write fails for box size, stage a trim-only batch first that shortens only boring setup lines, ask the owner to approve that trim in plain words, then stage the owner picks after it lands — because dropping owner picks silently to fit the box breaks trust while a visible trim-then-save keeps every word.
- Related but separate: the shared vault (lstm-bridge) is read-only with its own proposal path — never mix vault edits into a box-triage batch.
- When a second reviewer must countersign a compression batch, split it into a facts batch and a behavior-rules batch and approve each separately — a facts pass cannot bless standing orders, and a behavior pass cannot be mistaken for a factual record; one mixed batch forces an all-or-nothing vote on two different trust questions.
- Cite pending ops by content quote plus position, never by bare number, when exchanging references with another agent — numbering schemes differ between writers, so map their numbers to your content lines explicitly before answering, or you will confirm different ops while both sides believe you agreed.
- Park (never reject) a keeper the owner picked but a standing lock forbids saving: park keeps it recoverable in queue for an explicit owner word, reject deletes the only copy — because an overruled keep-all still needs the owner's final park-or-save call.
- Distinguish secret values from secrets-adjacent details when applying the never-save-secrets lock: values (passwords, keys, tokens) are never saved anywhere readable, details (file sizes, script names, addresses) save only as short pointers or park — because calling details a leak causes needless alarm while saving details raw still breaks hygiene.
- Announce only counts derived from the verified list length — assert the spoken N equals len(listed IDs) before sending, because a remembered total with a short list stalls the other board hunting a phantom item.
- Make every date-triggered reminder self-denying — state in the line itself that it alone never authorizes the action and names the required fresh word plus gates, because a live line reading as an order on its date gets executed as standing approval.
- Clear secrets-scan hits in context before ruling — a substring pattern fires inside ordinary words, so quote the surrounding text when a hit lands and mark false hits cleared with method shown, because a silent pass hides hygiene while an unlabeled flag causes needless alarm.
