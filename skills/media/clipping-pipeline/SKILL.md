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
  I may edit clip.py and render_template.py, but only with a backup
  first, one change at a time, and a render plus qc test after each.
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
5. After render, read the QC verdict. Fix only what QC names.
6. Report back short, in simple words, verdict first: what ran, output
   file names, QC pass or fail, next step. No jargon, no replay.
7. Money truth lives in `ledger.csv` (gitignored). Never post it anywhere.

## Pitfalls

- Old twin copy is gone (deleted Nov 2026 after verifying identical;
  husk removed). Live folder is the only copy. This pitfall is retired.
- `cache/scratch/` is pruned after roughly 24h idle — whole research
  folders can vanish overnight. Promote durable findings into this skill
  or a references/ note before closing the session; never treat scratch
  as an archive.
- `openai-whisper` is in requirements but NOT installed. Use
  faster-whisper (already in venv). Never pip-install blindly; ask first.
- `ledger.csv` is header-only and `learn.json` is a stub. Real tracking
  starts when real views come in.
- Music defaults to WAIT for approval. Never auto-add music to a campaign
  whose brief says wait.
- openshorts/ is dead weight. Ignore it unless asked to remove it.
- TikTok and Instagram posting is manual from the phone. No API is wired.
  Never claim a video is posted until Soham confirms.
- Future-tense talk is not an order — "I will say remove X" announces
  intent, it does not authorize deletion. Hold every removal until the
  exact list is confirmed with an explicit yes, then verify counts
  before and after.

## Verification

- Each command exits 0 and names its output files.
- Rendered MP4s exist under `ready_to_post/` for all three platforms.
- Rendered durations match the pre-render durations (ffprobe before and
  after); a changed duration means the mix chain shortened audio —
  bisect against the backup, do not ship.
- `qc` says pass before anything is called done.
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
