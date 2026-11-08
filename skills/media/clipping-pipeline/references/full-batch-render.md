# Full-batch re-render (whole catalog, all moments)

Use when every code slice is proven on single clips and the whole
catalog must be re-rendered with the fixes inside.

## Preconditions

- `git status --short` recorded. Report dirt, commit nothing.
- Back up `campaigns/<slug>/moments.json` (dated `.bak-*`) before any
  moment-field edits; it is the only non-regenerable batch input.
- Fixes verified: all unit suites green, py_compile clean on both files.
- User confirmed timing (multi-hour foreground job, fan noise).

## Steps

1. Back up outputs: copy `campaigns/<slug>/renders/*.mp4` plus each
   `ready_to_post/<tiktok,instagram,youtube>/*.mp4` to a scratch dir.
   Verify counts per folder before proceeding.
2. Clear ONLY the render cache: delete `<slug>_m*_*_v5_visual.mp4`
   (count before and after; 44 means 44). Keep older cache
   generations. Deletion needs the user's explicit yes.
3. Run the batch in BACKGROUND with notify (foreground tool calls
   time out around 7-10 minutes; the batch runs hours):
   `./.venv/Scripts/python.exe clip.py render <slug>`, log to file.
   One flaked moment does not kill the batch; the built-in retry
   covers single preflight flakes (see SKILL.md retry rule).
4. Collect failures: grep the log for `failed`, `Traceback`,
   `BATCH-EXIT`. Re-run each failed moment with `--only <mid>`
   until the log shows `done 1 clips` for it. If a moment flakes
   twice in a row (retry exhausted), wait for load to drop and
   retry solo — burst flakes are contention, not broken installs;
   never touch ffmpeg installs or PATH for them.
5. Verify mechanically per moment: render exists (>100KB),
   duration >= 10s via ffprobe, all three platform copies exist,
   dashboard entry exists. Report `verified X / problems Y`.
6. Grade on video: hook @1s + mid @dur/2 frames per clip, PIL
   contact-sheet grids (~1920px wide), harsh postable / reworkable /
   cut verdicts with one-line reasons. Save the verdict sheet.
7. Rework loop to the user's count bar: reworkable gets fixed and
   re-rendered, cut gets replaced with a fresh ranked block, never
   re-ship the same file. Repeat until the postable count is met
   or the ranked list is honestly exhausted.

## Rollback

- Outputs: copy the backup folders back over renders + ready_to_post.
- Code: `git diff` hunks or the dated `.bak-*` files (clip.py has
  dated backups; render_template.py reverts via git diff only).
