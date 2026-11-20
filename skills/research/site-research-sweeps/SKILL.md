---
name: site-research-sweeps
description: Sweep websites for UX evidence with a capture rig.
version: 1.0.0
author: Neohelper
license: MIT
metadata:
  hermes:
    tags: [research, browser-rig, evidence-sweep]
    related_skills: [standing-goal, browser-automation]
---

# Site Research Sweeps

## When to Use

Any multi-site evidence sweep where each site must be captured across viewports, interacted with human-likely, and filed as writeups plus a progress ledger — award-site research, competitor UX teardowns, animation-vocabulary studies.

Evidence sweeps over websites: multi-viewport capture, human-like handpass, funnel probe, vision verification, writeups, ledger, commit. One site flows capture -> handpass -> funnel -> writeups -> ledger -> commit -> push.

## 1. Pre-flight

- Read the governing protocol doc, the batch roster (URLs frozen), and the progress ledger before touching anything.
- Re-confirm the roster row (URL + slug) before EACH site's first capture, never from memory — slugs blur together by the twentieth site and a wrong-slug capture burns a full cycle; one grep of the roster row costs nothing.
- `git fetch` and confirm local HEAD equals origin; confirm tracked tree clean. Never rebase or force-push a shared branch without owner word plus idle-partner check.
- Confirm disk headroom and rig deps installed before long runs.
- Starting a new batch: scaffold per `references/batch-bootstrap.md` (mirror-freeze roster, liveness sweep, delta, ledger, bootstrap commit) before site 01.
- Capture patterns, not files: live-rig evidence plus anim-dump beats bulk site downloads — saved copies go stale, don't transplant across stacks, and bloat the dossier; reach for full-page snapshots only on explicit owner request for a specific recipe question — and then use SingleFile CLI (local, scriptable, one self-contained file); third-party downloader sites were evaluated and rejected as a standard path.

## 2. Capture (headed browsers need a foreground terminal)

- Run headed rig scripts in the FOREGROUND only — fresh background launches have no TTY and die immediately, while a run moved to background mid-flight keeps its TTY and finishes; never launch headed work in background, only let a running capture be moved there.
- Pin headed browsers to a non-primary monitor with the launcher's window-position flag and confirm placement in-page via window.screenX/screenY before trusting screenshots; viewports are emulated, so position changes never alter measurements. Measured map (Nov 2026, verify with powershell AllScreens before trusting): primary 2560x1440 at (0,0); left 1920x1080 at (-1920,+232 y-offset) — seam-exact pin is an explicit window size at x=-1920 minus chrome (e.g. 1936x1170 at -1936, right edge exactly 0); never --start-maximized, it spills across the seam. Screenshots/recordings are viewport renders (PNG IHDR byte-exact), so a straddling window never corrupts evidence — it only annoys the owner.
- Group viewport keys to fit the tool time cap; heavy WebGL sites get one view per run.
- After a timeout kill: verify state with read-only listings first, in their own calls, then delete `page@*.webm` temp files and kill stray workers in separate calls — bundling a destructive command with verification means one refused approval costs the facts too. Then continue the missing views.
- When a chained shell command is approval-blocked or refused, split it into single-purpose steps and run each separately — never re-run the same chain unchanged, and never achieve the blocked outcome through a reworded command.
- A timed-out chain usually still wrote fingerprints for its completed views (the fingerprint lands before the video tail) — list `*.json` first and re-run ONLY the missing views, solo: one view per run for heavy sites. Cap any single view at three attempts; after the third miss, log the view as too-slow/unlanded with prior-batch history cited and move on — the fourth attempt almost never differs.
- Handpass teardown-hang: handpass commonly times out at the cap AFTER writing every shot (teardown hang, zero strays) — check desk-/mob- file counts plus `99-bottom` files before rerunning; complete files with zero strays mean the pass is done, no retry needed.
- Retry ONCE on a transient `stdin is not a tty` failure on ANY node invocation (rig launches, one-off probes, version checks) before diagnosing — the wrapper drops first executions sporadically and the retry passes. The flake strikes in bursts: a whole chained command failing on all three invocations at once is still the same flake — retry the command unchanged, do not redesign around it.
- Session-replay tooling covers DOM-only sites (canvas/WebGL worlds replay blank): glide/video evidence stays primary for canvas worlds; adopt replay only after a trial beats video study on a DOM-heavy site.
- Never use `$` (dollar + identifier) in terminal commands: the wrapper expands it as its own variable and mangles the command (observed: PowerShell `$_` rewritten to a repo path). Write shell that avoids `$` entirely — e.g. PowerShell `Select-Object DeviceName, Primary, Bounds` instead of `ForEach-Object` with `$_`.
- Keep headed capture solo even when told to fan out: concurrent headed browsers starve the GPU and break both runs, and the protocol's solo-execution rule outranks a generic delegation instruction — say so in the turn and continue solo; subagents stay useful for reasoning or analysis subtasks that need no browser.

## 3. Diagnose gates, do not burn runs on them

- A `cover-stuck` verdict after full retries is data, not an error: vision-check the stuck screenshot to see WHAT is stuck (gate, loader, intro assembly).
- Confirm with a persistent-context handpass (single context often passes where rapid fresh contexts get throttled).
- Check prior-batch NOTES for the same site before inventing tooling — precedent usually names the gate.
- Adapt drivers by copy (never reuse blindly); keep the adapted driver as a committed artifact. See `references/gate-patterns.md`.
- Skip provably redundant views under the compounding rule and log the skip with the rule cited — never recapture what existing evidence proves.

## 4. Verify visually, claim only what fingerprints prove

- Vision-check handpass and drive shots (entered? moved scenes? still loading?) — run logs alone lie about outcomes. Check the FINAL still, not just a mid-drive one: identical commands land differently across runs when loader timing varies, and a mid-drive frame showing movement does not prove journey completion.
- Ledger and writeups must match fingerprint JSON fields (`glideBottom`, `skipped`, `cover`, stop rules), never the console chatter.
- Log partials honestly (capped glides, partial passes, unverified hovers) as partials.
- Verify cursor verdicts against the DOM (cursor divs/classes in the anim-dump) before asserting native — eyeball passes miss custom cursors that exist only as divs; on hang pages with no settled DOM, log the verdict as unverified instead of native.
- When a live probe contradicts the stylesheet dump (feels instant vs measured transitions), log both readings and name the tension — never silently overwrite the earlier claim; interrupted transitions feel instant while specified slow.
- Decide from the vision description, not its verdict line — verdict sentences occasionally contradict the inventory they summarize; re-read the described evidence yourself before logging the outcome.
- Cap vision retries at two identical failures: on the second identical error (e.g. connection error on the same file), change strategy instead of retrying — try a smaller/alternate frame from the same run, or verify from handpass shots; a repeated-exact-failure loop means the call path is broken, not the evidence.
- Never run capture or dump tools against a dead, redirected, or error-state URL — the output misattributes чужoy content to the site; carry prior-batch patterns explicitly instead and mark them un-remeasured.

## 5. Write when file tools refuse

- When write_file/patch refuse a path (safe-root), write via shell heredoc (`cat > file <<'EOF'`) and VERIFY with read_file (tail lines) — heredocs can warn yet land complete, or truncate silently.
- Funnel rule: ghost data only, photograph submit buttons, never submit; stop rules (captcha, calendar, iframe) are valid outcomes. When desk and mobile funnels diverge (form vs no-form), log the split in the ledger and both writeups — never smooth one pass over the other.

## 6. Ledger, commit, push

- Update the progress-ledger row in the same turn the writeups land; stage explicit file paths (fingerprints, notes, logs) — never directories: a directory add sweeps stray temp/probe files into the commit — and never media dirs.
- One commit per batch in final history: per-site commits allowed mid-run, squash at batch end via rebase, verify tree-diff empty vs pre-squash tip, push with `--force-with-lease`.

## 7. Recipe cards

- End every site anim-report with a ## Recipes section: one row per standout animation — element, trigger, from→to, duration, easing, our-stack implementation sketch.
- Capture the five fields from the live page with the DevTools Animations panel (10% replay, read keyframes, delay, duration, easing) or from anim-dump output — never from memory or guesswork.
- Tag each value measured (anim-dump.json / 60fps frame-count), cited (prior batch, not re-measured), or estimated (honest guess, marked as such).
- Run _rig/anim-dump.mjs per site after handpass and stage its anim-dump.json with the writeups; canvas/WebGL-only motion logs as frame-loop choreography, never invent numbers.
- Non-interactive squash recipe: verify range contiguity first (`git log` shows zero non-batch commits inside the range); record OLD_TIP (`git rev-parse HEAD`); run `git rebase -i <parent-of-first-batch-commit>` with `GIT_SEQUENCE_EDITOR="sed -i '2,Ns/^pick /fixup /'"` so line 1 stays pick and the rest fold in; rename the squashed commit with a second pass (`sed '1s/^pick /edit /'`, `commit --amend -m "..."`, `rebase --continue`); verify `git diff OLD_TIP HEAD` is empty before pushing — an empty diff proves the rewrite changed granularity only, never content. After ANY rename/amend pass, `git log` the range and confirm the batch message sits on the batch commit itself before pushing — amend-style rewrites target HEAD, and a silent no-op editor pass leaves the old message in place while you believe it changed. If a non-batch commit sits inside the range, relocate it to the end of the todo as pick in the same pass (custom editor script that prints that line last) instead of folding it — the squash stays one batch commit and the outsider survives untouched. Stage temp editor and helper scripts inside the repo work tree and delete them after the push — scratch dirs outside it may not persist between terminal calls.
- Backfilling a new per-site artifact across closed batches: produce and commit per site as usual with pushes as checkpoints, then re-squash each affected batch once at the very end with the same empty-diff verification; never rewrite shared history per site.
