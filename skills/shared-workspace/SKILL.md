---
name: shared-workspace
category: autonomous-ai-agents
description: "Use when two AI agents share one working folder and memory."
version: 1.0.0
author: Neohelper
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [multi-agent, shared-workspace, memory, collaboration]
    related_skills: [hermes-mcp-setup, lstm-bridge]
---

# Shared Workspace for Cooperating Agents

One folder both agents read and write, one memory both agents learn from, rules that keep two writers from corrupting each other. Default layout for this owner: F:/CD/Projects holds all projects in one repo; each agent keeps its own private home beside it.

## When to Use

Setting up or changing a shared project folder for two agents, defining who may write what, designing the shared memory and review ritual, or moving projects into the shared home.

## Procedure

1. Agree the shape before moving anything: one repo with project folders (not one repo per project), pilot the biggest project first, rest after the pilot proves out.
2. Move, never copy: verify presence at the new address before removing the source; grep for absolute old paths and repoint every reference (workflows, configs, docs) as part of the move, not later.
3. Lock secrets out of the shared tree first: gitignore secrets, tokens, sessions, and pairings in every repo before init; owner-only file rights on every credential; leak-scan on commit. Agents reference secrets by variable name only, never by value, in anything the other agent can read.
4. Roles are equals unless the owner assigns otherwise for a specific concern (locked 2026-10-28: owner chose equals over fixed builder/verifier split). Owner breaks ties. Any file change gets a one-line note first.
5. Memory in two tiers only: one MEMORY file in the shared root for working truths, the shared vault for lasting ones. Both agents read the vault index every session; both propose, owner alone approves.
6. Evolve on a loop: propose (either agent, never silent) -> use twice in real work -> promote to vault -> distill to a skill only when it becomes procedure. Conflicts freeze with both versions visible until the owner picks explicitly — no auto-wins (locked 2026-10-28; the 14-day newest-stands rule applies only to uncontested items).

## Owner communication (standing)

- Explain in simple words — the owner is not a coder; no jargon without a one-line gloss.
- Ask decisions in MCQ form (options as choices, recommended first); never bury a decision in prose.
- Match reply length to the ask: one-line question, short answer; finished work gets what changed, what is verified, what is left — never a replay of the process.

## Locked owner decisions (2026-10-28, do not re-ask)
- Shared home holds ten project folders (early twelve was an unverified guess; corrected 2026-10-28).
- Secrets offsite copy: RAR5 AES-256 archive of .env in the owner's cloud drive + password in Bitwarden (verified 2026-10-29; Bitwarden-note split abandoned — free notes cap at 10k chars vs 30k file). GitHub never holds secrets.
- Bot identities (locked 2026-10-30): Neocoder Bot <neocoder-bot@local> for the vault/Neocoder repos, Neohelper Bot <neohelper-bot@local> for the Hermes home — repo-local config only, never global, never the owner's identity; past commits stay as-is.
- Memory conflicts freeze: keep both versions visible until the owner picks explicitly — no auto-win for conflicts. Uncontested items stand after 14 days without veto.
- Failure alerts go to Discord NeoSpacee #alerts (live-tested; alert jobs must send a browser-like User-Agent or Discord 403s the post); progress during moves is reported both in chat and #alerts.
- Backup runs Sundays 5 PM IST (owner chose Sunday-only over daily); quiet nights stay silent.
- Move week freezes: no map refreshes, no version upgrades, no workflow edits, no Tavily install, no new memory paths until 24h after the move.
- Proposals must carry proof (where used + date); used-twice means two different real tasks on two different days; queue capped at 10 with oldest dropping to draft; DRAFT-USE allowed while the owner is away; conflicts ask max 3 times then stick with the incumbent.
- Move week: folder-by-folder, owner nods each folder before the next moves (locked 2026-10-29, replaces batch approval). Old copies go read-only on verification day with a per-folder 2-week clock, then Neohelper cron cleanup — read-only blocks drift-back, the clock blocks 'temporary' becoming permanent.
- Safe small proposals auto-approve after 12h unless vetoed; big/destructive always wait for the owner (locked 2026-10-28).
- Conflicts freeze: nothing wins until the owner picks explicitly — no 14-day auto-win for conflicts (locked 2026-10-28). The 14-day newest-stands rule applies only to uncontested items.
- DRAFT entries: plain facts only, never instructions/URLs/credentials; expire 48h (locked 2026-10-28).
- Spot-checks: Neohelper re-verifies 1 in 5 approved notes against real usage (locked 2026-10-28).

## Amendment 2026-10-28 (owner-approved as compiled, mirrors Neocoder vault)
- Hybrid ruleset ADOPTED (big-rules minus bottleneck, small-rules plus backstops).
- Diary split: BOTH agents hold equal rights in the shared Projects MEMORY file (owner decision 2026-10-29: equals over caution). Both proposal-only, owner approves; one writer per file per day. House memories stay separate (Neohelper vault notes, Neocoder diary).
- Backups Sunday 5 PM both houses (first joint Sunday Nov 1); vault gets GitHub backup with leak review first.
- Roles stay equals; mix approval stands; Tavily frozen; email parked; Discord live (NeoSpacee #alerts, tested 2026-10-29).
- Ten folders, full-history moves, old remotes retired, Finance = two n8n workflows frozen till 24h post-move.
- Standing: offsite secrets DONE (RAR5+Drive+Bitwarden password, test-extract verified); Discord webhook live-tested 2026-10-29; Neocoder 9 fixes executed during the 2026-10-29 move; single-run completed 2026-10-30 ~04:30 (all 10 green both sides, vault 0195862, Phase 2 10/10, diary debb53); status now SETTLED — living in the new home, buildout locked until owner unlock.

## Research amendments 2026-10-28 (deep-research box, owner-approved, all 8 adopted)
- R1 split notebooks: private scratchpad per agent (free use) + team MEMORY (proposal-only). Nothing moves up without proof.
- R2 expiry with never-expire tags: learnings expire 90d, reuse refreshes; names/addresses/standing rules tagged never-expire; owner override always.
- R3 ops log: every write/promotion/conflict/stale-catch logged in 2 lines from pilot day; monthly numbers from the log.
- R4 restore drill 2026-10-29: BOTH agents drill separately on their own houses (owner decision); Neohelper PASS 2026-10-29 (hash + file count exact); Neocoder's runs at Go; pass = clean rebuild, ~2h allowed (owner: correctness over speed). Move postpones only on drill errors, not slowness.
- R5 narrow freeze: freeze only irreversible steps + goal conflicts; small staleness flows with a visible marker.
- R6 author tags on every entry (Hermes/Neocoder/owner/drill/eval); git-blame mismatch quarantined; quarterly forgery drill.
- R7 named trials with pass/fail: expiry 30-vs-90, prune A/B, gate log, 4-week calibration; sunset clauses on experiments.
- R8 tiered proof: tips need one where-used line; claims need two real uses on two different days.
- Whole-file sharing kept per owner decision (against research advice; revisit when briefings feel heavy).

## ADOPTED common memory standard 2026-10-29 (both agents, post-move)
- Same components both sides: frontmatter envelopes, lifecycle states, intake template,
  erase-before-write, write/read phase split, gated retrieval, hot/warm/cold tiers,
  checklist-style storage. SQLite search banked until grep fails.
- Post-move defined: buildout/trials/unfreeze start only after ALL ten folders moved and stable.
- Federation ADOPTED: Sunday 5-min contract-vs-record drift check; overlaps quote-by-reference-with-date.
7. Back up on the owner's schedule to the owner's remote (locked: Sundays 5 PM IST) plus one cold copy before adding the second project. Alert on failure in the owner's chosen channel. The job must pull-rebase before pushing, retry the push, log every stage to a file, and stay silent only when nothing changed. See references/backup-job.md for the recipe.

## Pitfalls

- Never assert an unfamiliar external fact from memory: search the web (or the authoritative docs/repo) first, then state it with the source beside it — because a confident wrong technical claim (encryption strength, session-storage internals) costs more trust than the 60-second check ever costs.
- Never let a map outlive its code: whoever changes code rebuilds that project's index the same sitting, because a stale map plus fresh code produces confident wrong answers. whoever changes code rebuilds that project's index the same sitting, because a stale map plus fresh code produces confident wrong answers.
- Never run two writers on one file the same day without an owner assignment; last-writer-wins is silent data loss, not collaboration.
- Never let approval queues pile up: safe small items auto-approve after 12 hours unless vetoed (owner-locked), big or destructive items always wait, otherwise the owner becomes the bottleneck and learning halts.
- Never build ceremony for a two-agent team that only pays off at twenty: one repo, one memory file, delete-on-touch beats tiers, boards, and quarterly reviews that die in three weeks.
- Never write the backup job as a Windows .cmd that shells to Unix tools: cmd.exe has no tail/head and misreports errorlevels through pipes, so failures hide. Write it in PowerShell and log every stage to a file, because a silent exit is indistinguishable from success.
- Never push without pulling first: unstaged churn blocks rebase pulls, so pull with autostash and retry the push at least three times with a wait between attempts, because the pipe stalls and killed pushes look like completed ones.
- Never stage the whole tree blindly: add an explicit pathspec of settings, docs, skills, memories, and scripts only, and skip runtime databases, state files, and caches, because they bloat every push and widen the corruption window.
- Never trust a fresh git init to keep repo-level config: re-initing wipes credential-helper and identity, so re-apply them immediately and keep durable settings at global level too.
- Never assume nested config keys route to the secrets file the way top-level keys do: scan the whole config for plaintext secret patterns after every credential change, because one nested oauth block can publish a live secret.
- Never leave the secrets file as the single copy: it is gitignored by design, so a dead disk means total secret loss. Keep one encrypted offsite copy and record the recovery steps where the owner can find them.
- Never cross a credential between agents: each agent holds its own keys, and a shared instance means shared visibility — separation is audit and revocation, never walls.
- Never assume the editor shows your repo: a nested program checkout inside the home makes the source panel display upstream history, because the panel follows the open file. Open any root-level file to switch it back.
- Never paste a large secrets file into free password-manager notes: Bitwarden free Secure Notes cap at 10,000 characters (a 30k file fails even in quarters), so prefer a password-protected RAR5 AES-256 archive in the owner's cloud drive with only the password in Bitwarden — test-extract before trusting. In WinRAR choose RAR format, never ZIP: WinRAR's ZIP option uses weak legacy encryption while RAR 5.0 gives AES-256 — and tick encrypt-file-names so the archive hides contents and names.
- Never trust a stored Discord webhook without a live test post: a 403 on a fresh URL can mean the sender's User-Agent is blocked rather than a dead webhook, so first retry with a browser-like User-Agent and only then regenerate in channel settings — test-post before relying on it, because a dead webhook fails silently on every alert.
- Never rewrite history to purge a secret from a commit that was never pushed: delete the repo database and re-init clean, because no clone exists yet and surgery risks more than it saves.
- Never change a locked plan decision in one place only: re-read the whole plan doc for stale lines (status line, before-lists, day-schedules, old rules) after every decision change, because a contradiction between two sections breeds build-day confusion no checklist catches.
- Never let a number into the shared plan without its source: every figure needs the generating script or run plus its assumptions recorded beside it, because an unsourced number becomes a cross-agent dispute the moment the other side cannot reproduce it.
- Never mark queued work as done in a shared checklist: write QUEUED with the step that completes it, because a false green opens the day on a proven falsehood in the one document supposed to prevent that.
- Never approve the other agent's completed step on screenshots alone: re-run the load-bearing check yourself with independent commands (hash match, file count, zero-stale-grep, per-line parse), because a screenshot shows the claim, not the result — and a no-op command can print a passing-looking zero. At a final gate, re-run every check fresh in the same turn as the decision, because hours-old evidence may predate the latest write.
- Never layer a collective backup repo over per-project remotes that already cover recovery: re-pushing tens of gigabytes duplicates history for no gain, so verify what the existing remotes already protect first and let the shared home be folders plus the memory file with the file snapshotted in an existing backup.
- Never move a dirty or feature-branch checkout as the canonical state: move the stable line and leave WIP plus dirty files in the old location as fallback, because the pilot must test the move, not uncommitted work.
- Never dispute the other agent's quote before searching your own house: grep your skills, memories, and scratch scripts for the figure first, because the other side may be quoting your own run back at you and the retraction costs more than the check.
- Never grep Windows paths in one slash form only: plan docs write forward slashes while tools write backslashes, so run both forms (and a bare-keyword pass) before declaring zero refs — a single-form grep reports false clean and hides live stale addresses.
- Never treat one failed listing as proof of absence: confirm a missing repo, file, or dir with a direct second check (rev-parse, explicit path test), because a bad grep or truncated listing manufactures a scare out of intact state.
- Never compare hashes across agents without naming the algorithm: SHA-1 and SHA-256 of identical files print completely different strings, so every hash claim states the algorithm — an algorithm mismatch looks exactly like file corruption and triggers a false incident.
- Never hand a zero-context fresh session a resume note that asks it to trust prior verification: the handoff carries identity, record paths, current state, and exact ordered steps, and instructs re-verify-everything-first, because a recovered session that assumes is a session that ships the glitch forward.
- Never keep writing when your own tool calls misfire: two malformed or empty calls in a row means stop all mutation, switch to read-only, and report — a corrupted-but-valid call that slips through costs more than the whole night's progress.
- Never assume chat sessions follow a moved opencode project: the new path registers empty while history sits orphaned under the old path — see references/opencode-session-carryover.md for the pin-file method (write old project id into new clone's `.git/opencode` before first open) and the live-DB proof queries. Verify with the database, not theory, and confirm the old sessions list in the new home before the owner nod.
