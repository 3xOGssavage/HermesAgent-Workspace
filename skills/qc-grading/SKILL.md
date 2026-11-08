---
name: qc-grading
description: Use when grading video quality — hooks, mids, audits.
version: 1.0.0
author: Neohelper
license: MIT
---

# QC Grading (any video, any duration, any subject)

## When to Use

Grade a clip or long video before shipping: hook frame, mid frame,
end frame, or dense per-N-second sweeps. Works for Shorts, long-form,
any subject (people, product, gameplay, montage).

## Procedure

1. Pick the mode by duration: under 90s → hook (t=1) + mid (dur/2)
   + end (dur-1). Over 90s → hook + end + one frame per 15s.
   Over 10min → hook + end + one frame per 60s plus any flagged
   chapter boundaries.
2. Run `scripts/qc_probe.py --video <path> --mode <short|long|sweep>`.
   It writes frames + `qc_report.json` (face boxes/scores,
   sharpness, brightness). Unreadable input exits non-zero with a
   `QC-PROBE-FAIL` line instead of a traceback.
3. Grade each frame against the owner bar: whole faces (or whole
   subject for non-people: product readable, gameplay HUD intact),
   whole burned-in text, no blur below threshold, no empty frame,
   no backs unless the action reads, no edge slivers of people.
4. For stitched pairs: ALWAYS instruct the grader to ignore the
   center seam and judge outer edges only.
5. Verdict per clip: PASS only if hook AND mid pass. Fails get a
   defect class (face-cut, text-cut, empty, blur, backs, sliver,
   baked-subs, graphic) + the fix pattern it maps to.
6. Log verdicts append-only to the campaign grade file; never
   overwrite — history is the audit trail.

## Pitfalls

- Vision models flag stitching seams as cuts — the seam disclaimer
  in step 4 is mandatory, not optional.
- A still mid-phrase caption is not a defect (video moves on);
  fail only text cut by frame edges.
- Blinking eyes in one frame are motion, not a defect — fail only
  persistent blur/softness across seconds.
- Face gates: 0.5 for crop decisions (load-bearing), 0.3 minimum
  for text-placement probes with crowd veto kept. Never lower the
  crop gate to pass a grade.
- Empty frames at fades/transitions (first/last 0.5s) don't fail
  content frames — grade t=1 and dur-1, not t=0.
- Probe frames are evidence, not verdicts: metrics filter, the bar
  decides. Borderline frames always get an owner-bar read.

## Verification

- Every PASS clip's file must exist on disk, exceed 1MB, and probe
  a sane duration before it counts.
- Re-grade after ANY render (new visual, new composition, new text
  positions) — caches strand old frames.
