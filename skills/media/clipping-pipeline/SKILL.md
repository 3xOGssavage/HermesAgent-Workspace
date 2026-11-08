---
name: clipping-pipeline
description: Run the Clipping video pipeline commands safely on Windows.
version: 0.1.0
author: Soham (soham), Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [Video, Clipping, Windows, Free]
    related_skills: [soham-video-pipeline, youtube-content]
---

# Clipping Pipeline

# I operate the live clipping folder at `F:/CD/Projects/Clipping`.
- I now own this pipeline's code too (Neocoder is out of video work).
  - I may edit clip.py and render_template.py, but only with a backup
    first, one change at a time, and a render plus qc test after each.
    - For every behavior change, write the failing scratch test FIRST
      (RED), then the minimal patch (GREEN): helper plus test, then
      wiring, then a same-timestamp before/after vision verdict per
      affected clip (FIXED / SAME / WORSE). SAME means the theory was
      wrong — re-diagnose from frames instead of shipping.
    - Write multi-line code patches as script files via write_file and run
      them; never compose patches inside terminal -c quoting — nested
      quoting silently corrupts the patch (wrong anchor matched, stray
      string terminators) and each mis-fire costs a full re-render to
      discover. Read the target region first, assert anchors are unique,
      verify the generated code reads correctly before running it.
      Insert a top-level def only before a top-level def — an indented
      comment inside a function body is not module level, and the file
      dies with IndentationError pasted into the wrong scope; check the
      anchor's column before placing the insert.
    - If a test fails, revert and report. Never rewrite whole files.
  - Hard lessons from the Nov 2026 audio upgrade: new filter text must
    land inside f-strings or ffmpeg sees literal {dur}; sidechain ducking
    can shorten audio, so always lock mix length with apad plus atrim;
    final mux uses -shortest, so a short mix silently cuts video; when a
    duration changes, bisect against the .bak before theorizing.
- clips.js merge lesson: committed dashboard file was a JS literal
  (unquoted keys), but the reader only parsed strict JSON — every
  render silently wiped other slugs. Fixed with tolerant prefix match
  plus one-time normalize to strict JSON, verified 18 entries survive.
- Scene cuts are wired into moments: every run probes cuts and snaps
  edges within 2s (window guard keeps bad snaps out). Static footage
  correctly returns unchanged moments — verified identical re-run.
- Per-moment anchor locks plus dynamic window width (framing features,
  all default-off for existing moments): set `"anchor"` on a moment
  dict to left / center / lock-left / lock-center (`_resolve_anchor`;
  lock-* also disables the face override). Use for burned-in graphics
  that live on one side (title cards, gauges): pick the side the
  graphic is on after checking audit strips. Corner-snap (2026-11-07):
  a window landing at 0<x<250 slices top-left DAY counters in half —
  snap x to 0 when the tracked face still fits in the left window
  (`_snap_corner`, face size probed only on landing in the zone).
  ASPECT LAW (2026-11-07, m31 distortion): a 9:16 window at full
  height cannot be wider than H*9/16 (607px at 1080p) — anything
  wider stretches the picture (23% thinner at 750px) because the
  scale to 1080x1920 is forced. The whole fit-cw/co-width system was
  built, proven distorting, and fully reverted. Never fit width by
  widening the crop: reposition x, lock an edge, pick another
  second, or replace the moment. Width helpers were deleted; the
  consolidated suite test_all.py pins their absence.
  frames and the wave proves SAME while the defect stands.
  Back up moments.json before any anchor/surgery/co edit
  (`cp moments.json moments.json.bak-<step>`) and delete only that
  moment's `*_v5_visual.mp4` before re-rendering — data edits strand
  the same stale caches as code edits.
- Co transplant (2026-11-07, m9 PASS): when a hook's 2 seconds are
  unframeable but a nearby 2s has whole faces + readable context,
  point the moment's "co" at the good seconds (probe source first,
  land hook t=1 on the clean frame, not on a fade boundary).
  Mid success doesn't fix hooks — transplant what works. When the
  hook fails but the mid passes, point "co" at the mid's verified
  second (co = start + dur/2 − 1) instead of hunting new seconds —
  the frame is already proven. For wide group shots, never let the
  hook fall back to a centered crop: the crowd veto (>2 boxes →
  None) centers the window and slices edge people, so pick a solo
  second (a PTC or reaction close-up) as the co instead.
- Face-aware text (2026-11-07, m2+m9 PASS): hook titles and caption
  pills covering faces are fixed with per-moment `text_y`
  {hook_top, cap_top} (clip.py passes through, template merges over
  style defaults, None = unchanged). Probe face boxes at hook + body
  thirds; title below high faces / top-sliver for huge faces, captions
  above low faces. Text-grade gate 0.3 with crowd veto kept (crop
- Co position override (2026-11-07, m22): per-moment `co_ax` 0..1
  places the cold-open window (`_co_x_for`: ax wins, else face,
  else center; lock still wins overall). For wide groups the face
  gate vetoes and center cuts edge people — set co_ax from probed
  face boxes. Snap still applies after.
- Hook pose rule (2026-11-07, m7): raised-arm celebration poses span
  wider than the 607 window and always sliver — hooks need arms-down
  seconds (probe 2-3 candidates, pick energy + intact limbs).
- Burned-in source subtitles (2026-11-07, m47): if the source itself
  has baked meme captions, our 607 window slices them into giant
  half-text AND double-captions — prove with source frames first;
  ranges with continuous baked subs are unwinnable, replace.
  (Template was proven clean via composition-HTML + Phase-B bisect.)
- Length rule (2026-11-07, owner lock): clips run 45-60s.
  Brief duration_min 45, duration_max 60. Applies to new clips;
  the 43 shipped shorter stand as postable unless owner says rework.

## When to Use

- Soham asks to download, transcribe, render, QC, or track a clip.
- New campaign work: moments, styles, ready_to_post review.
- Daily ops: cleanup old campaigns, learn top performers.

Scope note: clip.py and render_template.py edits are in scope (owned); everything else in that folder is run-only. Language: English-first for now.
Hindi and other languages are deferred, not removed.

## Prerequisites

- Working folder is the live Clipping folder, never mine.
- Its own venv: `F:/CD/Projects/Clipping/.venv/Scripts/python.exe`
  (Python 3.12.6). Never my Python. Never the system Python.
- Its own tools: `bin/ffmpeg.exe`, `bin/ffprobe.exe`, `bin/yt-dlp.exe`.
  ffmpeg is the 7.1.1 full build: verified filters include select, silenceremove, sidechaincompress, afftdn, loudnorm, afade — scene-detect, ducking, denoise, fades, lip-sync shift need clip.py code only, no new tools or licences.
- Node v22 for HyperFrames renders. All free, all local.

## How to Run

All commands run with cwd set to the live folder, using its venv python:

```
cd F:/CD/Projects/Clipping
./.venv/Scripts/python.exe clip.py new <youtube_url> <slug>
./.venv/Scripts/python.exe clip.py moments <slug> --no-docker
./.venv/Scripts/python.exe clip.py scenes <slug> [--threshold 0.3]
./.venv/Scripts/python.exe clip.py render <slug> --style hormozi-clean [--shift 0.15] [--only m2]
./.venv/Scripts/python.exe clip.py qc <slug>
./.venv/Scripts/python.exe clip.py track <slug> tiktok <views> <earnings>
./.venv/Scripts/python.exe clip.py learn
./.venv/Scripts/python.exe clip.py cleanup --days 30
```

Render uses `render-room/` (HyperFrames 0.8.26) plus ffmpeg NVENC.
Output goes to `ready_to_post/{tiktok,instagram,youtube}/`.
Review in `dashboard/index.html` opened in a browser.

- When Soham is working or gaming: run renders quiet — one background
  run at low priority (`nice -n 19`), and ALWAYS redirect a background
  run's output to a log file (`> log 2>&1`), never rely on the live
  transcript: a restarted session keeps the files but loses the
  transcript, and a failure with no log means re-running the whole
  batch to learn what happened. Grep the log file, not the scrollback.
  No browser windows (headless checks only: node --check, ffprobe,
  frame extracts), kill via
  process_manage on pause and resume from moments.json plus the log
  (moments already rendered stay valid — never restart the batch
  from scratch). Soham keeps random hours, so never schedule heavy
  renders for assumed idle windows; pause on ask, resume on ask.
- HyperFrames preflight flake (proven 2026-11-05): `clip.py render`
  can fail moments with `[HyperFrames] FFmpeg cannot start ...
  Failed to run "...ffmpeg.exe" -version` while the identical
  command passes on retry with zero changes (m10 failed then
  passed). Binary healthy, env identical — intermittent spawn
  under load, not a broken install. On this error: simply rerun
  the same command; do not touch ffmpeg installs or PATH.
  Single-clip proofs rerun until pass. (Earlier foreground-only
  note superseded: foreground flaked once too.)
  `run_hyperframes` retries ONCE on exactly this signature
  (`_is_preflight_flake`) — real failures still fail fast.
  Retry gates key on the failure signature alone, never on output
  existence: stale artifacts from prior runs make existence checks
  lie and silently disable the retry (four batch failures, zero
  retry lines, all from one `and not out.exists()` clause).
- Estimate batch time from a measured single-clip render (one timed
  48s clip = 2m06s HyperFrames-only, ~3-5 min per clip all-in),
  never guess: 44 clips ≈ 3h + 30 min verify/QC. Say the measured
  basis with the number.
- Visual cache forces stale proofs: `_derive_visual` returns True
  without re-deriving when the `*_v5_visual.mp4` exists, so a crop
  fix shows no change until that file is deleted. For before/after
  proofs: copy the old render aside, delete only the moment's
  `*_v5_visual.mp4`, re-render, compare same-timestamp frames.
- Leading-None stays None by design (2026-11-05, m20 t=2.2 vision
  verdict OLD-BETTER): never forward-fill leading no-face chunks
  with later face positions — entering subjects get cut out.
  Center is the neutral entrance choice; chunk-1+ keeps its own
  detections. Regression test `test_leading_none.py` pins this.
- Confidence gate MIN_SCORE=0.5 on all detector loops (2026-11-05:
  DAY61 title card scored 0.425 with zero persons and hijacked
  cold-open+crop; true heroes score 0.555-0.885).  Calibration table
  lives in the probe (`probe_scores.py`); if true faces ever score
  under 0.5, retune the one constant, never remove the gate.
- Wrap guards live on `.capline` + `#hook` (2026-11-05):
  `max-width:100%;overflow-wrap:anywhere` stops long tokens
  (DAY120, $250,000) clipping at the viewport edge. Sizes, colors,
  fonts untouched — taste changes (hook 92px, caption 96px) stay
  Soham's call, never bundled with defect fixes.
- Video zooms capped (2026-11-06): join punch 1.12->1.05, keyword
  punch + slow push 1.06->1.03 — the 6% edge crop was slicing heads
  near frame edges at joins and hot words. Timings kept. Word pops
  untouched.

## Procedure

0. The full day/week runbook lives in `references/sop.md` — follow its
   order (pull, pick, new, moments, render, qc, review, post, track).

1. Plan only first. Present the steps and get Soham's explicit go before
   any code change, install, delete, or render — running a `--help` or
   listing a folder needs no approval, changing anything does.
2. Start every run with `git status --short` in the live folder. Report
   dirt, never commit it unasked.
3. Confirm the slug and the campaign brief (`campaigns/<slug>/brief.yaml`
   or root `brief.yaml`). If source license is unknown, stop: QC blocks it.
4. Run one command at a time, in order: new, moments, render, qc.
   Moments must be story arcs, not fragments: single transcript segments
   run 2-10s and can never carry hook plus arc plus payoff, so always
   merge nearby segments (gap under ~2.5s) into 25-45s blocks
   (`_merge_blocks` in clip.py) and pick from those. Rank candidate blocks
   by FACE presence first, stakes-density second: sample 3-4 frames per
   block for face area, prefilter by stakes words ($, digits, win/lose)
   per second, keep the top face-rich blocks (count scales with job
   size — 10-moment jobs keep ~10), drop anything under ~20s. Length without a face is unwatchable — a long faceless block
   always loses to a shorter face-rich one. Then face-gate every
   kept moment: probe the first seconds for the largest-face frame and
   start there (`_face_gate`), or the opening freeze is a torso, a wall,
   or a blink. Then the cold-open pass (`references/cold-open.md`): best stable face from anywhere in the moment plays 2s under the hook title before the story.
   Clips under ~12s
   are a picker failure, not a render failure — fix moments, not styles.
   Yield calibration: one hour of talking-head source holds ~8-15 strong
   moments, of which ~5-10 survive the 7+ bar — that is the quota to promise, not 20.
   For full-video jobs ("clip the whole video"): rank every remaining block
   by stakes-score (money/numbers/emotion/questions per second) and render
   in score order across rounds; report postable / reworkable / cut counts
   per round and stop only when the ranked list is exhausted or Soham says
   stop — never stop after the first strict pass and call a low count final.
   - Soham's bar (2026-11-06): everything shipped is postable, always —
   every clip and every video we create. Reworkable gets fixed,
   cut gets cut, never posted. Report the honest count after every
   batch: postable X/44, reworked Y, cut Z with one-line reasons.
  Non-negotiable mechanism: the COUNT must reach 44 postable — cut
  clips get replaced with fresh ranked blocks (never re-ship the same
  file), reworkable get fixed, repeat until 44 postable or the ranked
  list is honestly exhausted.  Replacement blocks come from
  scripts/rank_fresh_blocks.py (set SLUG, run with the campaign venv).
  Replacement blocks must satisfy the brief minimums themselves:
  floor the ranker at duration_min — sub-minimum picks burn
  full renders and can never count. Before any fresh-hunt, prove
  supply exists: merge all moment ranges and list uncovered stretches
  at or above the target length — hunt only qualifying gaps, and if
  none exist say the transcript is exhausted instead of burning
  recon on regions the math already rules out. For fix waves, fan recon out to
  parallel subagents (4-6 at once, one moment each) with a fixed
  prompt: range from moments.json plus the named defect plus the
  owner bar, return exact start/end or REPLACE. Sequential
  self-recon is the bottleneck; one fan round triages the wave.
- Grading calibration (2026-11-07): grade to Soham's named defects —
  face cut off at edge, partial body only (hands/legs/torso with no
  face), half-cut text, empty no-subject frames, blur. Tight
  expressive close-ups (hair top cut, face fully visible) are Shorts
  style, not defects. Backs-to-camera and eyes-closed fail only when
  no face or emotion reads in either frame.
5. After render, read the QC verdict. Fix only what QC names.
6. Report back short, in simple words, verdict first: what ran, output
   file names, QC pass or fail, next step. No jargon, no replay.
7. Money truth lives in `ledger.csv` (gitignored). Never post it anywhere.

## Pitfalls

- Face detector hallucinates on confetti, bokeh, and busy blobs: one bad
  frame sprayed five overlapping giant boxes with confidence up to 0.67,
  outscoring a real face at 0.36 — confidence does NOT separate true from
  false. Two guards, both required: reject any frame with more than 2
  detections (no clear hero), and require the winning face to persist in
  neighboring seconds (stability check kills whip-pans, flashes, screen
  avatars). Apply both in `_face_area_at` callers, not just cold-open:
  any largest-face pick without them can land on garbage.
- ASR typos that survive into burned captions look unprofessional
  (STEPPE for SEPARATE). Keep a tiny whole-word correction map
  (`_ASR_FIX` in render_template.py, applied in the word loop) for
  classic Whisper confusions only — never rewrite speech, only fix
  obvious misspellings, whole-word match, uppercase-safe.
- Money numbers render as ONE span: punctuation-led fragments
  (,000 / .00) merge into the previous word's span at build time
  (`_captions_html_words`), so the amount highlights and scales as a
  unit. The old zero-margin CSS glue is superseded — do not re-add
  per-fragment spans for punctuation.
- Cold-open join needs a mask: a 0.18s white-flash div at the splice
  plus the hook title held ~3s turns a jarring hard cut into a
  professional transition. Without the flash the peak-first splice
  reads as a glitch.
- GSAP fromTo with a start position is NOT dormant before its time:
  it renders its FROM state at page load (immediateRender defaults on),
  so an overlay flash built with fromTo sits visible over every frame
  until its timestamp. Build delayed overlays as set plus to at the
  timestamp instead — set applies only when the playhead arrives.
  Verify overlay opacity reads 0 at load in a live browser before
  shipping any render that adds a timed overlay.
- Cold-open visuals need their OWN crop anchor: the 9:16 crop position is
  computed once per clip from the main moment's face, so a cold open cut
  from elsewhere in the source renders off-face (hero cropped out, edge
  graphics half-visible). Derive visuals per segment — cold-open seconds
  cropped on the cold-open face, remainder on the main anchor — then
  concat. Any prepended segment from a different timestamp needs the same
  treatment, or the best-face pick is wasted on the wrong slice.


- `cache/scratch/` is pruned after roughly 24h idle — whole research
  folders can vanish overnight. Promote durable findings into this skill
  or a references/ note before closing the session; never treat scratch
  as an archive.
- `openai-whisper` is in requirements but NOT installed. Use
  faster-whisper (already in venv). Never pip-install blindly; ask first.
- A later pip install in the same venv can silently swap a CUDA torch
  for a `+cpu` build while printing success — the resolver prefers the
  default index once new deps enter. After every install step, assert
  `torch.version.cuda` is not None before running anything; if it is
  None, force it back with `--force-reinstall --no-deps` pinned to the
  CUDA index, then re-verify. Keep experimental stacks (large new deps,
  different torch majors) in a disposable side venv so the working
  caption venv is never the place dependency conflicts get resolved.
- A beta or RC Python silently breaks compiled wheels: the provisioner
  matched a `cp311` torch wheel onto a 3.11.0b5 interpreter and every
  import died with WinError 127 (procedure not found — an ABI mismatch,
  not a missing CUDA install). Before letting any tool build a venv on
  an interpreter, assert `python -VV` prints a FINAL (no a/b/rc suffix).
- Three identical failures from re-running a provisioner is a systematic
  defect, not corruption — stop re-running and fix the root cause
  (interpreter, pin, or path) instead of burning another cycle.
- `ledger.csv` is header-only and `learn.json` is a stub. Real tracking
  starts when real views come in.
- Music defaults to WAIT for approval. Never auto-add music to a campaign
  whose brief says wait.
- openshorts/ is dead weight. Ignore it unless asked to remove it.
- TikTok and Instagram posting is manual from the phone until the upload
  repo arrives; agreed plan is manual for the first 2-3 weeks, then
  Postiz self-host for scheduling and posting (Docker + Postgres +
  Redis when that day comes; cloud tier is paid, skip it). No API is
  wired now. Never claim a video is posted until Soham confirms.
- Render-cache filenames must include the moment's start-end timestamps, not
  just the moment ID: moment IDs recycle across re-runs (m1, m2, ...), and a
  cache keyed on slug plus ID silently reuses a stale visual from an older,
  shorter moment, which then fails the duration gate. Any cache keyed on a
  recyclable ID has the same flaw — key on content coordinates instead.
- Future-tense talk is not an order — "I will say remove X" announces
  intent, it does not authorize deletion. Hold every removal until the
  exact list is confirmed with an explicit yes, then verify counts
  before and after.
- Check the skill's scripts/ before writing a scratch duplicate —
  rank_fresh_blocks.py already exists for replacement ranking, and a
  scratch fork silently diverges from it (different bounds, different
  overlap rule), so two runs rank different blocks. Extend the skill
  script; keep one-shot probes in scratch, never second copies of
  skill-owned tools.

## Verification

- Each command exits 0 and names its output files.
- Rendered MP4s exist under `ready_to_post/` for all three platforms.
- Every shipped MP4 decodes clean: `ffmpeg -v error -i file -f null -`
  must report zero NAL/packet errors. Existence is not validity —
  a corrupt mux (proven once: 973 NAL errors, file played) passes
every size and duration check, so decode-check every render before
grading it; on errors wipe that moment's visual/hf/master plus
outputs and re-render clean, never ship or grade the bad file.
- Rendered durations match the pre-render durations (ffprobe before and
  after); a changed duration means the mix chain shortened audio —
  bisect against the backup, do not ship.
- `qc` says pass before anything is called done.
- Never judge a render from one or two stills. After every render,
  extract frames across the FULL clip (hook at t≈1, mid, late — every
  2-4s for short clips) and vision-check each: hook readable, caption
  fill solid (zoom the caption band), faces centered and intact
  (edge-sliced faces mean the track missed — tighten chunks, don't
  accept the crop), no flash frames.
  For full-clip audits, extract at fps=1 and review second-by-second
  as contact-sheet grids — sparse sampling misses dead seconds, empty
  transitions, and caption drops hidden between samples. Grade every
  second for the vertical-crop failure set: head or body cutoff,
  hands-only or partial-body frames, half-cut source text, empty
  B-roll, duplicate stalls, missing captions.  Keep each grid at
  ~1920-2200px wide; when vision rejects a grid, re-export at 1080px
  and retry — size is the failure, not content. When grading stitched
  hook/mid pairs, tell vision to ignore the center seam and grade
  outer edges only — otherwise it fails faces and text the stitch
  itself bisected. A still catching a caption mid-phrase is temporal
  flow, not cut text — fail only text physically clipped by a frame
  edge. When vision fails on
  a path that used to work, `ls` the file first: a missing strip was
  once misreported as a connection error for five straight calls. Close every
  job with the 4-way check per moment (render exists, all three
  platform copies exist, duration sane, dashboard entry exists) and
  report verified/problems counts, never eyeball the folder.
- Whole-catalog re-render recipe (backup, cache clear, background
  batch, verify, grade, rework loop) lives in
  `references/full-batch-render.md` — follow it for full-batch jobs.
  Defect pattern to root cause to fix map lives in
  `references/defect-patterns.md` — consult it before diagnosing
  framing or text defects so a solved pattern is not re-debated.
  Soham compares against pro agency output frame by frame; a glance
  at two frames has missed real defects before.
- Rework waves prove out per clip, never by feel (2026-11-07):
  set before-frames aside, re-render, compare the same timestamp
  before vs after, and take a vision verdict per clip — FIXED, SAME,
  or WORSE. Match every background completion notice to its session_id
  before acting: stale notices replay old waves (a finished wave-3
  notice arrived mid-wave-4), and grading the wrong wave's files
  invents regressions. Check render file mtimes, not the notice text. SAME means the theory was wrong (a smaller zoom cannot
  save a head bigger than the crop window), so re-diagnose from the
  frames instead of shipping; WORSE means revert that clip first.
- When successive audits contradict each other on near-identical output (scores collapse while pixels did not change), stop rebuilding and measure objectively first: compare mean brightness, contrast, and a side-by-side of old versus new winner frames before touching code. A harsh audit of unchanged pixels is audit drift, not a regression — another rebuild round on drift destroys working output.
- When a frame looks wrong (wrong scene, strange content), check the
  SAME timestamp in the source file before blaming the render — cold
  opens and teasers live in the source, not in our edit.
- For multi-video study grids, build contact sheets with PIL paste,
  never ffmpeg tile: tile plus -loop repeats input zero in every cell,
  and single-frame inputs hit EOF so the rest render black.
- One ffmpeg call, two timestamps, one file: default stream selection
  maps input 0 to EVERY output, so the second timestamp silently
  renders the first frame twice (identical hook/mid rows caught only
  by vision). Run one ffmpeg call per timestamp, or add an explicit
  -map per output. Identical hook/mid rows mean broken extraction,
  not static content — re-extract before grading.
- When a render reports "done 0 clips", the bug is upstream of the mux: check moments.json is non-empty first, then read the FULL log file (never diagnosis from tail output — tail hides both the real exit code and the failing lines). Pipe to a file and grep it.
- Dashboard shows the clip cards with pass or fail marks.

## Standing Rules (Soham's standing orders)

- English-only audience for now. Hindi and other languages are parked
  as backup, not removed.
- Two tracks never mix: Track 1 = clipping others' videos for Whop pay.
  Track 2 = own unique content for platform monetization. Separate
  folders, accounts, channels. Clipping output never goes on own channels.
- Music: ALWAYS stop and ask Soham before any music goes on any clip.
  No exceptions, even if a brief says approved.
- Rejected tool: hermes-video-editor plugin evaluated Oct 2026 and refused — PolyForm Noncommercial licence bans monetized YouTube, 3-week-old beta with 1 star, clip.py already covers all Shorts needs. Revisit only for Track 2 long-form with a commercial licence.
- Fresh-start rule: old campaign files stay until the fresh setup proves
  itself. Soham creates campaign subfolders himself per video job.
- Precedence over research: if the research folder and this skill ever
  disagree on clip.py behavior, trust a fresh `--help` run first, and
  the skill's guardrails always (license first, music wait, never commit
  unasked, never claim a post unconfirmed).

## Session Handoff

- A Hermes end-of-session screen carries everything needed to resume:
  the `--resume` ID, the `-c` title, duration, message counts, and the
  shell prompt showing the cwd plus active venv. Read the prompt line
  first — it tells you which folder and which venv that session used,
  which may differ from your own.
- When taking over work from another agent or folder, verify with your
  own listing before trusting its inventory: spot-check file sizes,
  line counts, and key config values.

## Pro Caption Spec (verified Nov 2026 vs 11 real MrBeast Shorts)

- Font MUST be embedded base64 in the page (`data:font/ttf`), never rely on
  relative font files — headless Chromium silently falls back to a thin
  font and the stroke swallows the fill (hollow-caption bug, Nov 2026).
- Headless Chromium paints `-webkit-text-stroke` OVER the fill. Always set
  `-webkit-text-fill-color` explicitly plus `paint-order: stroke fill markers`,
  and repeat the fill color in every keyword class (`.w-hot`, `.w-money`,
  `.w-risk`) or keywords render white.
- Spec numbers: house style is Luckiest Guy ALL CAPS for BOTH captions
  and hook title (same family — mismatched hook/caption fonts read
  amateur). Every shipped font must still be added to the base64
  embed loop AND the render-room font copy, or headless output
  silently falls back.
  1-3 words per flash, 65-100px at 1080x1920 (96 house), white + ~7-11px black
  stroke over a rounded semi-opaque black pill behind each caption flash
  (`background:rgba(0,0,0,.55);border-radius:20px` on `.capline`) — the pill
  carries contrast on bright footage so the stroke can stay clean.
  captions y950-1240. Hooks are moment-specific, never the campaign
  slogan repeated: `_moment_hook` scans <=6-word windows for
  stakes density, prefers windows that OPEN on a stakes word (money,
  number, win), and trims filler at both edges (leading IN/THE/AND,
  trailing THE/TO/BEING) so hooks read in under a second and never
  trail off mid-phrase. Skips hooks already used (seen-set) and
  penalizes ad-read windows (sponsor/promo/QR copy) so an ad read
  never becomes the hook. Fallback order is moment-first: unseen moment
  windows outrank the campaign slogan — the slogan is the last resort
  before first-6-words, never the first fallback, or every weak moment
  ships the same generic title.
- ffmpeg `amix` normalizes DOWN by default: it divides the mix by the
  input count unless `normalize=0` is set, so voice plus effects ship
  ~10dB quiet even though every meter looked right pre-mix. Always set
  `normalize=0` on voice-over amix stages, and rely on loudnorm
  upstream — never the mixer — for level discipline.
- Hook audio must attack: 0.15s fade-in max on the final mux, whoosh hit
  at frame zero plus a second hit on the cold-open join. A 0.5s fade-in
  dulls the opening and the hook feels quiet even when levels are right.
- One static crop per clip is not subject focus, and slicing into
  tracking chunks IS the fix when done with hysteresis: 2.5s chunk centers, hold unless the face moved >0.08 of frame width, re-center every chunk for huge close-up faces — this holds moving subjects better than any single anchor (verified by frame audit on re-rendered clips). Crop each timeline PART once from its own anchor — cold-open
  seconds on the cold-open face, remainder on the main anchor — then
  concat (details in references/cold-open.md). Video zoom is capped
  in code (join punch <=1.05, keyword/slow push <=1.03 — the old 1.06+
  punches sliced heads at frame edges); word pops (1.1) and caption
  active scale (1.25) are text-only and untouched. Timings kept.
- Ship rule: 7+ posts, below 7 gets fixed or cut. No sentimentality.
- Cold-open frame must contain speech within ~0.8s or captions visibly
  lag the picture (enforced in `_cold_open` via transcript words;
  manual `"co"` overrides bypass it, so verify speech there by eye).
- Hook keyword highlight must land on the stakes (numbers, money, the payoff
  words), never on filler: the longest-word heuristic highlights words like
  TOGETHER while the eye should be forced to 150 LBS and $250,000. Until
  `_highlight_hook` prefers stakes tokens (digits, $, MONEY_RE hits), hand-set
  the hook keyword per campaign via hooks.yaml.
- MrBeast native first frames carry almost NO text overlay — hooks are visual
  (face + gesture + big prop + money). Our burned hook title is agency style,
  correct for clipping reposts; keep it short and never truncate mid-phrase.

## Taste Rubric (Nov 2026 — every clip, every niche, no exceptions)

1. First frame alone explains the video (muted test). Face/proof/prop.
2. Hook line: stakes + reward, <=12 words, unique to THIS clip —
   stamping one slogan on every clip kills suspense; each hook must
   carry its own moment's payoff.
3. Something changes every 2-4s (cut, zoom, pop, B-roll, SFX).
4. Proof (number/screenshot/before-after) inside 8s.
5. One idea per clip; payoff at end (reveal/transformation/twist/loop).
6. Captions readable muted at arm's length over busiest background.
7. Faces: eyes visible, upper third, never under captions/UI.
8. No dead air >0.5s; no greeting/logo/setup opening.
9. Audio: voice clear over bed, no pumping, SFX land on beats.
10. Loop check: end feeds start OR clean payoff; tail trimmed.

## Cold Open

Full pass lives in `references/cold-open.md` — auto pick, join mask,
per-segment crop anchors, hand-pick procedure. Rules from the 10-clip
job already folded in there (early-speech filter, manual `"co"`
override, F AND F+1 verification).

## WhisperX opt-in transcription (Nov 2026, RTX 3070 Ti verified)
- Isolated env `.venv-whisperx` (never install into main venv).
- Per job: wav extract at 16kHz, whisperx CLI (large-v3-turbo,
  int8, batch 4, cuda, NO diarize), then
  `tools/wx_to_transcript.py <json> <transcript.json> [offset]`.
- Schema identical to faster-whisper output; render path unchanged.
- Default stays faster-whisper; use whisperX for noisy audio or
  proper-noun-heavy content (it got "STEP account" right).
- Rollback: delete wav/json, re-run `clip.py moments`.

## Remotion sidecar (Nov 2026, verified solo-free)
- House template at `assets/remotion/house` (pinned 4.0.540).
  Intros, title cards, lower-thirds, overlays only.
- Per job: write props.json (file form, never inline — Windows
  strips quotes), `npx remotion render src/index.ts <CompId>
  out.mp4 --props=./props.json` from the house dir.
- Assets enter clip.py only as plain media files. Rollback =
  delete `assets/remotion/`.
- Solo local renders are $0; recount headcount before any
  collaborator touches the codebase (Company trigger at 4+).

## F-drive rule (Nov 2026, permanent)
- NOTHING of ours on C:. All models/caches/installs live on F:.
- Before any install: check default paths, redirect to F: first.

## VoiceStudio sidecar (Nov 2026, verified commercial-safe)
- App: F:/VoiceStudio/VoiceStudio.exe, data/models: F:/Voice Studio/VoiceStudio
  (per-user install, checksum-verified installer). Engine lives outside
  every venv, so it can never break the caption path.
- Speak to it only while its window is open: local MCP/REST on the
  loopback port. No headless or remote-GPU use on the free tier.
- Two GUI steps belong to Soham (license acceptances an agent must not
  click through): install the local runtime, then install the VoxCPM2
  engine and accept its Apache-2.0 terms in the Model Catalogue. Never
  render sellable audio on the default OmniVoice weights (CC-BY-NC).
- Pin Settings, Performance, Compute device to `cuda` (PUT
  `/api/settings/compute-device` `{"value":"cuda"}`), restart the app,
  then assert `/api/settings/gpu-report` shows every used engine as
  `accelerated` on cuda — auto usually picks GPU, but the pin stops
  silent CPU fallback. Keep one app instance: stale copies pile up
  (each eats RAM and all serve the same port, so the oldest answers
  while the newest setting never applies) — kill all of them first
  with `powershell.exe -NoProfile -Command "Stop-Process -Name
  VoiceStudio -Force"` (bare `taskkill /F` gets its slashes eaten by
  git-bash path conversion; route it through `cmd //c` if powershell
  is unavailable), launch exactly one, then verify.
- Full loopback control recipe (MCP handshake, engine routing, license
  purge) lives in `references/voicestudio-mcp.md` — follow it before
  touching engines or deleting weights.
- Verify `cuda` (not silent CPU fallback) in Settings, Performance on
  first run; do ears-on A/B against Kokoro/Chatterbox before trusting
  it on a real job.
- ONLY green-licence engines. OmniVoice/NLLB/dictation-NC models REMOVED
  from disk; never click Download/Accept on red rows or the app re-fetches.
- VoxCPM2 = Track 2 voice. Engine select: POST /engines/select
  {"family":"tts","backend_id":"voxcpm2"} -> active=voxcpm2 cuda.
- Generate via MCP generate_speech {text, profile_id} -> wav_base64
  (48kHz mono). Verified 3.44s line, 6.7s gen on RTX 3070 Ti.
- Sidecar venv quirk: provisioner uses `uv venv --python 3.11`;
  a beta/RC Python breaks torch (WinError 127). Keep a FINAL 3.11+.
  If Install fails with that error, delete
  data/engines/voxcpm2 and re-run Install in app.

## StykAnimate overlays (Nov 2026, verified end-to-end)
- Author in the user's real browser via desktop control (real GPU):
  scene 1080x1920, bg Alpha 0 checkerboard, pose joints across frames,
  export Transparent PNG sequence. Headless harness browsers CANNOT
  render/export (software-GL ceiling, perpetual "preparing" state) —
  never attempt this in a headless session.
- Do NOT trust Auto key blindly: set CONTRASTING joint values at frame 1
  and at the pose frame, then read the panel value back at EACH frame —
  a single shared value (identical exports) means no keyframe was written.
  An onion-skin ghost behind the figure is the in-app proof frames differ.
- Skip project save (its dialog fights remote input); Export works
  without it. In the export dialog pick the Transparent preset (Frames
  format, PNG sequence, Transparent toggle on) and fire.
- At the native save dialog, accept the DEFAULT name with Return and
  move the file to F: within the same minute — background typing into
  native dialogs never verifies, so never fight the filename field;
  submit-default plus instant terminal move keeps C: clean. Verify the
  C: folder holds no overlay file afterward.
- Composite: -framerate 24 -i overlay/frame-%06d.png,
  format=rgba + overlay format=auto; timed with enable=between().
- Verified: 10 RGBA PNGs, motion (bent vs upright), clean composite over
  real footage, correct timing. Proof: .render_tmp/stykproof/styk_proof.mp4.
- Track 2 inserts and silent gags only; no hero segments, no audio work.
  Animations we make are ours including monetized use.

## Paren-gate lesson (Nov 2026, cost a full batch)
- A single missing ) in render_template word_js killed the ENTIRE caption
  timeline (parse error -> no tl -> hook static, captions opacity 0 forever).
- After ANY template edit: extract the inline <script>, run
  node --check on it BEFORE rendering. 30 seconds saves 9 renders.
- Symptom pattern: hook visible early + gone later (engine clip timing)
  with zero captions throughout = dead timeline, not missing data.
  Verify data first (word counts), then timeline (tl exists?), then syntax.
- v3_visual cache can mask template bugs (old visuals reused) — bump the
  cache key or clear it when the template changes.
