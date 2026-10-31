# Shared Workspace — Full Plan (Neocoder + Neohelper, owner: Soham)

_Status: SETTLED 2026-10-30 — move complete, Phase 2 10/10, diary debb53. Living in the new home; buildout/trials/unfreezes locked until owner unlock. Next: owner-declared stability → post-move buildout._

## 1. The home
- `F:/CD/Projects` (created on pilot day). One git repo, ten project folders:
  Clipping, custom opebwebui, jonwilcox, `lucas - ai dm setter`, n8n,
  neodev-portal, neodev-website, random stuff, smoke-test, tmg.
- Pilot: neodev-portal moves first. Verify at the new address before removing
  the source; grep absolute old paths and repoint every reference (workflows,
  configs, docs, n8n) in the same sitting. Rest move only after T+24h proves out.
- Neocoder's old Projects folder goes read-only on verification day, kept 2 weeks
  per folder, then removed by Neohelper cron cleanup. Move, never copy.

## 2. Who does what
- Equals, no fixed roles. Per file: one writer per file per day.
- Neocoder builds and edits; Neohelper maps, reviews, verifies.
- Move week ran folder-by-folder with owner nods (locked 2026-10-29; single-run override for the 2026-10-29 execution, rule resumes for any future multi-folder work). Progress reported BOTH here and in Discord #alerts. Owner breaks ties after joint research.

## 3. Staying in sync
- Sundays 5 PM, both houses, automatic. Pull-with-autostash, three push retries,
  stage logging, silent when clean, Discord alert on failure (NeoSpacee #alerts,
  live-tested 2026-10-29; failure alerts only, no other messaging).
- Projects home gets a backup line before pilot day (verifies each project's own remote pushes + will snapshot the shared MEMORY file — created during post-move buildout — into Neohelper's Sunday backup), plus a
  `.MIGRATING` flag the backup respects (skip while set).
- Old sources KEPT 2 weeks after verification, then deleted by Neohelper cron cleanup (owner decision 2026-10-29; sweeper job old-source-sweeper active, Sundays 5:30 PM, verify-each + parity + age gates, first due ~11-12 Nov).
  Old copies go read-only on verification day; clock runs per folder (each folder deleted 2 weeks after its own verify date).
- Dual drills: both agents fully rebuild their own houses from their own backups (locked 2026-10-29).
- Standards: per-stack gitignore sections, bot identity for auto-commits (Neocoder Bot <neocoder-bot@local> for the vault/Neocoder repos; Neohelper Bot <neohelper-bot@local> for the Hermes home; never impersonate the owner), kebab-case renames for spaced folders, LFS for binaries.
- Nobody backs up anybody else's house. Neocoder's house and the vault need
  their own backup lines.

## 4. Secrets
- Gitignored before any repo init. Owner-only file rights on every credential.
- Agents reference secrets by variable name only, never by value, in anything
  the other agent can read. Separate keys per agent (separate audit and
  revocation, not walls, on shared instances).
- Offsite copy DONE: RAR5 AES-256 archive of .env in owner's Drive + password in Bitwarden (verified 2026-10-29).
- Leak-scan on commit.

## 5. Memory — how it grows itself (includes all 8 research amendments)
- Two tiers: one MEMORY file in Projects for working truths, the vault
  (`F:/CD/LSTM`) for lasting ones. Both agents read the vault index every session.
- Shared file: BOTH agents hold equal rights (owner decision: equals over caution).
  Both proposal-only in the fixed 4-line shape: claim, proof with date, conflicts with,
  cost if wrong. Nothing moves up without proof. One writer per file per day.
- Tiered proof: tips need one where-used line; claims need two real uses on two
  different days. Safe small proposals auto-approve after 12h unless vetoed;
  big or destructive ones always wait for the owner.
- Expiry: learnings expire after 90 days, reuse refreshes; names, addresses,
  standing rules carry never-expire tags; owner override always wins.
- Ops log from pilot day: every write/promotion/conflict/stale-catch in 2-line
  rows (`MEMORY-OPS-LOG.md`); monthly numbers come from the log.
- Author tag on every entry (`Hermes`/`Neocoder`/`owner`/`drill`/`eval`);
  tag-vs-`git-blame` mismatch quarantined; quarterly forgery drill.
- Named trials with pass/fail bars + sunset clauses: expiry 30-vs-90, prune A/B,
  gate log, 4-week calibration.
- Conflicts freeze with both versions visible until the owner picks explicitly
  (ask max 3 times, then incumbent stands). Uncontested items stand after 14
  days without veto. Queue capped at 10, oldest drops to draft. Away-time drafts
  are facts-only, 48h expiry. Neohelper spot-checks 1 in 5.
- Neocoder's house memory stays its own diary; divergence checks are
  read-only and filed as proposals.
- Monthly 15-minute owner check, five pass/fail numbers: oldest proposal <7d,
  backup OKs at 100%, zero expired drafts, conflicts not rising, owner minutes
  flat or falling. Dual rebuild drills before pilot, then quarterly (pass = clean rebuild, ~2h allowed).
- Whole-file sharing kept per owner decision (against research advice; revisit
  when briefings feel heavy).

## 6. Frozen — two-tier (adopted 2026-10-29, Neocoder reconciliation approved by owner)
- Move freeze (no version upgrades, Finance edits, Tavily install, Playground wiring, new memory paths, map refreshes on the moving folder): lifts per folder at that folder's T+24h green.
- Buildout freeze (memory machinery buildout, 4-week trials, unfreezed upgrades): lifts only at all-ten-stable per §10 POST-MOVE DEFINITION.

## 7. Neocoder pre-move fixes (verified against live files)
1. Repoint the five relative skill paths (`../../.opencode/...`) to absolute
   `F:\CD\Opencode\.opencode\...` entries.
2. Rewrite the stale `Projects` path memories to `F:/CD/Projects/...`.
3. Drop `Projects` from graft `includeDirs` and rebuild.
4. Update AGENTS.md project-path lines to `F:/CD/Projects/`.
5. Split workspace backup from project pushes; alert if Projects is empty.
6. Fix the `memory.json` → `memory.jsonl` typo in the child config.
7. Close all sessions before the move; start fresh after.
8. Update `verify-inheritance.ps1` project root and re-run.
9. Replicate guard rules in the new repo (owner locked: replicate all 4 layers).
Keystone: run `setup-env-vars.ps1` PORTABILITY FIX (installer rewrite), not
hand-relativizing. New: `setup-secret-scanning.ps1:32` hardcodes the workspace
root — resolve from script path like `fix-task-scheduler.ps1` does.
Freeze during move week per §6.

## 8. Pilot sequence
- BEFORE, owner-side (done 2026-10-29): offsite secrets verified; Discord NeoSpacee
  #alerts live-tested; Neocoder fixes verified against live files, then executed.
- BEFORE, build-mode (2026-10-29 evening, completed): dual rebuild drills — Neohelper PASS (hash + file count exact); Neocoder drill PASS (fresh backup 23/23); task #0 amendment record committed (6db05fa); memory rewrite owner-approved; remaining
  pre-move batch per §7; per-project gitignore + LFS + bot identity committed; lock conventions
  tested; one observed end-to-end backup run; per-project remotes verified (no collective code repo per owner decision 2026-10-29 — each project keeps its own repo; shared MEMORY file lives at F:/CD/Projects root, snapshotted by Neohelper's Sunday backup).
- DAY (2026-10-29 evening → 2026-10-30 ~04:30, completed): pilot neodev-portal verified, then owner-ordered single continuous run of all remaining 9 (smallest-first, pins before first open, sessions confirmed per folder, stop-on-red never triggered). AFTER (done): all 10 green both sides, vault committed (0195862 on 224c4ca), old sources kept read-only with 2-week per-folder clocks.
- Session-history gate (mandatory per folder, owner decision 2026-10-29): moving a folder orphans its sessions — opencode resolves project ID per opened directory (GitHub/SSH remote-hash → .git/opencode pin file → root commit; verified live: portal's 70 sessions under old remote-hash id 66a315c2, new clone auto-cemented empty root id 1a08d9ed). Fix per folder, BEFORE first opencode open in the new location: write the old project ID into new-clone/.git/opencode (reversible, git-safe untracked file; e.g. website → 4dec77c4, pilot → 66a315c2). Then confirm the old sessions list before the owner nod. (Pin-file method adopted 2026-10-30 — supersedes both the root-commit assumption and the DB-remap; upstream issues #29703/#34737.)
- AFTER (done 2026-10-30): all scheduled backups observed; .MIGRATING cleared in Phase 1 (backups unblocked); old sources kept, rollback path intact throughout (stop-on-red never triggered).

## 9. Locked — do not re-ask the owner
Shared box at `F:/CD/Projects`; ten folders; neodev-portal pilot; equals;
per-folder owner nods; GitHub-only backups; Discord alerts; old entries die only with
owner yes; Sunday 5 PM; changer rebuilds map; 12h safe auto-approve; conflict
freeze; facts-only drafts; spot-checks; hybrid-10 ruleset; diary split (both agents equal rights
in shared Projects MEMORY, proposal-only, owner approves; house memories separate); all 8 research amendments; whole-file sharing.

## 10. Still open
Offsite secrets DONE (RAR5 AES-256 in Drive + password in Bitwarden, test-extract verified 2026-10-29).
Move executed 2026-10-29 evening → 2026-10-30 ~04:30: single continuous run, all 10 green both sides, vault committed (0195862).
Pending owner nods (Neocoder old-session plan): Phase 1 hygiene DONE except vault commit (log backfilled + summary refreshed + .MIGRATING cleared 2026-10-30, backups unblocked; log/summary commit awaiting owner nod); Phase 2 stable-check now (locked); old sources stay read-only till clocks expire (locked).
Hybrid Gate-4 design impact. v2 upgrade. 11 stale maps (Neocoder to enumerate: graft indexes, not memory notes). Neocoder memory record triage DONE during run (memory rewrite owner-approved, verified).
Tavily install post-move. Playground knowledge source. Finance edits post-move.
4-week trials post-move (owner decision 2026-10-29, over skip recommendation): (a) split private/shared notes further, (b) shared task list; keep/drop at week 4 on miss/re-cut counts.
Doc cross-links post-move: §11 points at Neocoder's vault index; its handoff copy points at this file. Federation drift-check ADOPTED 2026-10-29: Sunday 5-min contract-vs-record diff, quote-by-reference-with-date for overlaps.
POST-MOVE DEFINITION locked 2026-10-29: memory machinery buildout, 4-week trials, unfrozen upgrades start only after ALL ten folders are moved and stable (not pilot T+24h).

## 11. Research basis (summary)
51-round dossier at `F:/CD/Hermes Agent/cache/scratch/multi-agent-memory-research/`
(45 key sources in SOURCES.md): frameworks, memory systems, big-tech deployments, failure
postmortems, evaluation metrics, replication, red-teams, runbooks, costs,
pre-mortem, merge rules, benchmarks, protocols, cross-agent learning, audit,
steelman + rebuttal. Verdict: keep the hybrid-10; the 5 evidence-demanded
changes are folded into §5 above. Simulation figures (20,000 trials, queue 72,
idle 50%) are genuine outputs of `cache/scratch/sim_option_y.py` (seed 7, assumptions
listed in-file); kept with that caveat, not as measured data. Start reading at `OWNER-SUMMARY.md`.

## 12. ADOPTED as the common memory standard (owner decision 2026-10-29 — both agents implement post-move)
Same machinery both sides: frontmatter envelopes, lifecycle states, intake template, erase-before-write, write/read phase split, gated retrieval, hot/warm/cold tiers, checklist-style storage. Meaning-search recipe banked until grep fails.
PARITY LOCK approved 2026-10-29: symmetric components, symmetric rights, separate house diaries (same kind of component, same rules), one shared file. (Enters Neocoder's amendment record at build-mode Go.)
1. **Frontmatter envelopes** — Reason: every memory machine-readable (id/type/owner/state/version/importance/tags/source/supersedes), MemOS MemCube pattern. Source: MemOS paper arXiv:2505.22101 + repo MemTensor/MemOS (Apache 2.0).
2. **Lifecycle states (Active/Merged/Archived/Expired/Frozen)** — Reason: explicit states replace vague "old notes"; git = rollback. Source: MemOS MemLifecycle + docs lifecycle page.
3. **Intake template** — Reason: forces type/tags/importance/expiry/ACL before writing; kills malformed memories at birth. Source: MemOS MemReader-lite pattern.
4. **Erase-before-write** — Reason: contradiction-check before every append; old line deleted first. Source: MemT-1.0 GDN-2 erase gate (arXiv:2610.26825 §2.2.2).
5. **Write/read phase split** — Reason: distill sessions to memory at session end; retrieve slices at task start; never interleave. Source: MemT-1.0 storage vs utilization split (§2.2.2).
6. **Gated retrieval** — Reason: retrieved memory supplements context through a relevance gate, never raw-pasted. Source: MemT-1.0 gated readout (`A = A_ori + A_mem`).
7. **Hot/warm/cold tiers + shared tag vocabulary** — Reason: file by strongest weight; separate read-routing from write-routing. Source: MemT-1.0 Mixture-of-Storage (§2.3).
8. **Checklist-style storage** — Reason: store distilled "how we fixed X", not raw logs; load checklist at task start. Source: MemT-1.0 experience-guided coding (SWE-bench match).
9. **Meaning-search recipe (banked)** — Reason: adopt only when grep starts missing; we are 40–80x below that line. Source: DenseRAG/hybrid recipe (bge-small + SQLite-vec + FTS5 + RRF k=60 + rerank top-8).
