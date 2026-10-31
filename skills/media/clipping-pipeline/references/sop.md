# Clipping SOP — daily and weekly operating rules

Source: the pipeline builder's own runbook. Read-only mirror; the code
stays the authority when this note and `clip.py` disagree.

## Daily order

1. `git pull --ff-only`, `git status --short` — report dirt, never commit unasked.
2. Pick campaign: Whop Discover ≥ $1/1K, budget ≥ $3K and ≥ 60% left.
   Skip anything > 80% spent. Note rate, min, max, end date.
3. `new <url> <slug>` → source lands in `library/<slug>/`.
4. `moments <slug> --no-docker` → transcript + moments + hooks.
5. `render <slug> --style <preset>` → one MP4 per platform + posters.
6. `qc <slug>` — must pass every gate before review.
7. Open `dashboard/index.html` → accept or reject each clip.
8. Post accepted clips only, paste caption exactly, submit to Whop
   within 30 minutes, log the date.

## Weekly order

1. `track <slug> <platform> <views> <earnings>` per post → `ledger.csv`.
2. `learn` → top 5 by views and $/1K; copy the winners' style next week.
3. `cleanup --days 30` → archive old campaigns.
4. Weekly push script → code and config only; videos stay local.

## Never-break rules

- License first: CC or permission letter only. No permission = stop.
- Music WAIT: never auto-strip or auto-add music; check transcript + brief.
  Game clips stay original-audio only.
- QC gates stop the line: bad license, no permission, out-of-range
  duration, unapproved music, missing tag or credit, blurry, duplicate.
- One source file becomes at most one clip times three platform posts,
  and only when the campaign allows it. Never the same video on 5+ pages.

## Dashboard review bar

- Reject: weak 2-second hook, unreadable or blocked text, black bars,
  tearing or freezes, wrong or missing logo, bad sound, no kill/feed/action.
- Accept: sharp 9:16, readable title, synced captions, clean sound,
  clear action.

## Posting discipline

- Post mornings, midday, evenings in the audience timezone; 1–2 per day
  on new pages; public; likes on; original sound.
- Screenshot analytics at 24h, 72h, 7d. Keep clips live per brief.

## When broken

- Docker down → `--no-docker` CPU fallback is the normal path, not a hack.
- yt-dlp 403 → upgrade the exe, fall back to search-based fetch.
- Render fail → CPU libx264 fallback, then check ffprobe duration ± 0.1s.
- Ban signs (captcha, logout, zero-view run) → stop posting 1–2 weeks;
  one profile plus one VPN endpoint forever, never switch fast.

## Nobody touches unasked

`.env`, `ledger.csv`, `accounts.json`, `bin/*.exe`, `library/`,
`ready_to_post/` videos, `.venv/`, the git remote, the house style
without a 30-day test.
