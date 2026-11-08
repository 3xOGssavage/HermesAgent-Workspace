# Cold Open (Hook V2 lite)

Peak-first opening: the best-face 2 seconds of the moment play under the
hook title before the story starts. Standard agency practice — the scroller
meets a face, not a torso, wall, or blink.

## When it fires

`_cold_open` scans the whole moment from second 2 to `end - 2.5s` (1s steps, MediaPipe face
area) and returns the best stable face frame time, or None. Restricting the scan to the first 15s misses the peak face in 40s moments — the best reaction often lives mid-moment, and the replay makes it the opener. Bar: face area >= 0.025
of frame — background faces don't qualify, and a weak cold open is worse
than none. Candidates must also speak within ~0.8s (a transcript word
starting inside that window): a great face with no early words opens
dead — the eye sees motion but reads nothing, and captions visibly lag
the picture. Two anti-hallucination guards, both required: frames with more
than 2 detections are vetoed outright (confetti/bokeh sprays overlapping
boxes with confidence up to 0.67, outscoring real faces — confidence does
NOT discriminate, count does), and the winning face must still be present
in neighboring seconds (stability check kills whip-pans, flash frames,
and phone-screen avatars). When None, the clip renders straight with no
cold open.

## What changes when it fires

- Visual: `[F, F+2s]` concatenated in FRONT of `[start, end]` (ffmpeg
  concat filter, then the normal crop chain runs on the joined master).
- Audio: same concat on the voice track, THEN the denoise/duck/loudnorm
  chain — silence removal after concat also cleans the join.
- Captions: cold-open words at 0-2s, main-moment words shifted +2s
  (`_shift_chunks` shifts chunk AND inner word times — shift one without
  the other and the highlight drifts off the voice).
- Hook title cap is 3s so the premise survives into the main content.
- Join mask: white flash div (`#coflash`) fired at exactly the join timestamp, passed as `coldopen_at`. A hard cut from close-up to wide without a mask reads as a glitch; the flash makes it feel intentional. Build it as `tl.set` (opacity up at the join) followed by `tl.to` (fade out) — never `tl.fromTo` with a position: in headless capture the from-state paints from frame zero no matter what flags are set, so the whole cold open renders under a white veil. `set` plus `to` cannot fire early by construction.

## Pitfalls

- In ffmpeg filter_complex, a stream label that is consumed cannot be
  reused: `[0:v][1:v]concat` eats both inputs, so continue the chain from
  a fresh label (`[vc]`), never restate `[0:v]` downstream. Same for the
  output-seek retry path, which needs absolute-timeline trims plus
  setpts on each leg before concat.
- The retry/output-seek path must mirror the primary path's branch:
  a retry that assumes a single input silently renders the wrong range
  when the primary used two.
- Cache keys must include the cold-open frame: a re-render with different
  cold-open state but the same moment ID reuses a stale visual.
- Caption typo class: a tiny whole-word ASR fix-map (STEPPE/SEPERATE/
  DEFINATELY/RECIEVE/UNTILL/THIER, plus branded terms the ASR mangles
  like STEP-A-KILL for the Step banking app's Step account) applied at
  caption build time and mirrored in hook text.
  Whole-word only, never rewrite speech — it fixes transcription, not copy.
- Crop each timeline part from its own anchor: the 9:16 crop position is
  computed once per clip, but a cold open shows a different second of
  video than the main moment — cut and crop the cold-open seconds with
  the cold-open face frame, crop the rest with the main anchor, then
  concat. One anchor for a two-part timeline crops the wrong heads.
- Branch filter graphs under ONE if: two sequential `if` blocks sharing an
  `elif` chain let the trailing `else` overwrite the first branch's
  command. Nest alternatives as if/else inside a single branch.
- Distant-face moments get a per-moment punch-in: `moments.json` accepts
  `"zoom": 1.25`, honored in `_crop_expr` as a divisor on the crop-window
  width for both main and cold-open crops. Faces under ~3% of frame read
  as blobs on phones; a 1.2-1.3x punch on verified face-rich moments
  restores eye contact without re-picking. Never apply globally — it
  crops edge graphics (day counters, prize stickers) that wider moments
  need.
- When every first frame comes out washed white but mid-clip frames and the
  raw visual are clean, suspect a headless overlay, not the encode: load
  the render-room page live and read computed opacity of each overlay div.
  Video clean plus one overlay opaque equals overlay bug — fix the timeline,
  never re-encode blind.

## Hand-picking the cold open (when auto fails)

Use when auto returns None twice, or its picks score under 7 twice: eyes
beat the detector on footage with patterns, crowds, or fast cuts.

1. Sweep the moment's source range: extract one frame every 2-4s
   (`-ss <t>` per timestamp, absolute output paths), one PIL contact
   sheet per moment (480x270 thumbs, 4 across), vision-pick the best
   eyes-to-camera frame. Record its source timestamp F.
2. Verify F AND F+1 as stills before pinning: scene cuts hide inside
   the 2s window, and a hero frame at F with a cut at F+0.5 plays as
   the wrong shot. Both seconds must hold the face.
3. Pin it: set `"co": F` (source seconds, float) on that moment in
   moments.json, plus `"zoom": 1.1-1.25` only if the verified face is
   under ~3% of frame. Re-render just that moment (`--only mN`).
4. Confirm the override took: the fresh visual filename in .render_tmp
   must carry the new co-tag, and clip t=0.5 must match source F+0.5.
   A matching filename with mismatched content means the cache key
   lied — bust that visual and re-render, never grade the stale file.
