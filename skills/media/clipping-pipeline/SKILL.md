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
I never edit its code without being asked. I run its commands, read its
outputs, and report back in simple words.

## When to Use

- Soham asks to download, transcribe, render, QC, or track a clip.
- New campaign work: moments, styles, ready_to_post review.
- Daily ops: cleanup old campaigns, learn top performers.

Don't use for: code changes to clip.py. Language: English-first for now.
Hindi and other languages are deferred, not removed.

## Prerequisites

- Working folder is the live Clipping folder, never mine.
- Its own venv: `F:/CD/Projects/Clipping/.venv/Scripts/python.exe`
  (Python 3.12.6). Never my Python. Never the system Python.
- Its own tools: `bin/ffmpeg.exe`, `bin/ffprobe.exe`, `bin/yt-dlp.exe`.
- Node v22 for HyperFrames renders. All free, all local.

## How to Run

All commands run with cwd set to the live folder, using its venv python:

```
cd F:/CD/Projects/Clipping
./.venv/Scripts/python.exe clip.py new <youtube_url> <slug>
./.venv/Scripts/python.exe clip.py moments <slug> --no-docker
./.venv/Scripts/python.exe clip.py render <slug> --style hormozi-clean
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

- Two near-identical project folders can exist (live vs copy). Never trust
  the path alone — run `diff -q` on the entry script across both folders
  before assuming which one is live. Silent diff output means mirror.
- `openai-whisper` is in requirements but NOT installed. Use
  faster-whisper (already in venv). Never pip-install blindly; ask first.
- `ledger.csv` is header-only and `learn.json` is a stub. Real tracking
  starts when real views come in.
- Music defaults to WAIT for approval. Never auto-add music to a campaign
  whose brief says wait.
- openshorts/ is dead weight. Ignore it unless asked to remove it.
- TikTok and Instagram posting is manual from the phone. No API is wired.
  Never claim a video is posted until Soham confirms.

## Verification

- Each command exits 0 and names its output files.
- Rendered MP4s exist under `ready_to_post/` for all three platforms.
- `qc` says pass before anything is called done.
- Dashboard shows the clip cards with pass or fail marks.

## Standing Rules (Soham's standing orders)

- English-only audience for now. Hindi and other languages are parked
  as backup, not removed.
- Two tracks never mix: Track 1 = clipping others' videos for Whop pay.
  Track 2 = own unique content for platform monetization. Separate
  folders, accounts, channels. Clipping output never goes on own channels.
- Music: ALWAYS stop and ask Soham before any music goes on any clip.
  No exceptions, even if a brief says approved.
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
