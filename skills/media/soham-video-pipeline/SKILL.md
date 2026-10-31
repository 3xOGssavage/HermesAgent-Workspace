---
name: soham-video-pipeline
description: Free Windows short-video pipeline for Soham.
version: 0.2.0
author: Soham, Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [video, ffmpeg, whisper, edge-tts, shorts]
    related_skills: [youtube-content, manim-video, p5js]
---

# Soham Video Pipeline

Owner: Soham | Windows, partial coder | Free-only | 2h setup goal.
Scope: no installs, no paid services, no uploads without asking. Research verified 30 Oct 2026 (rounds 1-16 + blueprint + closeout).

## When to Use

- Soham asks for: short/reel/shorts video, Hindi voiceover, captions/subtitles, stock clip assembly, autopost queue.
- Route here first for any 9:16 vertical short (15-60s) before touching other video skills.
- Don't use for: pro 4K feature edits (defer to Resolve Free), paid AI generation (Kling/LTX Studio/ElevenLabs free tiers are personal-only), CapCut scripted automation (ToS s6 bans scripts).

## Procedure (free-only, Windows, ~2h setup order)

1. Base — ffmpeg on PATH (15m). Done when: `ffmpeg -version` prints.
   - `winget install ffmpeg`, new terminal, verify. Everything below wraps ffmpeg (FableCut/OpenEdit/HyperFrames all require it).
2. Edit — FableCut Studio in Chrome, zero-install (20m). Done when: `project.json` opens and exports a test MP4.
   - Timeline is one `project.json`; ~25 MCP tools (patch/undo/versions). Local `npx -y fablecut` only if denoise/ProRes/reference analysis needed.
   - 9:16 comp: 1080x1920; safe zones universal 380 top / 480-672 bottom / 120 sides (R10).
3. Motion (optional) — HyperFrames core skills (20m). Done when: `npx hyperframes skills update` succeeds and a sample renders.
   - `npx hyperframes skills update` (core; `--all` = full 21). Revideo (MIT) is runner-up for typed scenes. Onda (MIT, 70+18) is the runner-up Remotion library. Remotion itself is solo-free even for commercial/automated pipelines — paid company license only at 4+ headcount. Skip Manim on Windows unless math explainers are the point (pip-only, 0.22.x).
4. Voice draft — Edge-TTS hi-IN (15m). Publish — Azure F0 Swara/Madhur OR Kokoro offline. Done when: one Hindi WAV plays clean.
   - Draft: Edge-TTS `hi-IN-SwaraNeural` free unlimited, best quality — LICENSE-GREY for money, never publish for revenue.
   - Publish: Azure F0 500K chars/mo free (card required; 900 chars = 1x60s short = ~555 shorts/mo single-target); Kokoro Apache-2.0 offline (4 Hindi voices hf_alpha/hf_beta/hm_omega/hm_psi grade C, needs espeak-ng MSI, Python 3.10-3.11).
   - Skip: ElevenLabs free (10K credits NON-COMMERCIAL + attribution), Piper (GPL + per-voice caution), Chatterbox watermark (PerTh embedded, try HF Space first).
5. Captions — VEED hosted first, WhisperX local fallback (15m). Done when: `transcript.json` with word timings exists.
   - VEED: 10-min free, best Hindi quality. Fallback: WhisperX local offline (word-times + hi aligner, needs HF token; medium model = sweet spot, small collapses 42% WER, large-v3 best 15.7%).
   - Render: ffmpeg libass burn-in (watch Windows colon escaping); karaoke ASS = small custom script grouping 4-7 words. faster-whisper has NO upstream CLI; stable-ts is archived — don't build on them.
   - Whisper tuning: `vad_filter` + `condition_on_previous_text False` kills ghosts; never force `en` on Hinglish; prompt script controls output script.
6. Stock+Music+SFX (10m). Done when: one clip + one bed downloaded with license logged per asset.
   - Stock: Pixabay API key (instant, 100/min, cache 24h, no hotlink; music = Content-ID trap). Pexels new keys PAUSED; Coverr demo 50/hr + attribution.
   - Music: YouTube Audio Library first (no Content-ID); SFX: Mixkit / Freesound-per-sample (check each license) / Adobe Firefly SFX. BBC RemArc is personal/research/education only — never list it as commercial-safe. Rule: transform every clip, log license. yt-dlp grants NO rights.
7. Autopost queue (15m). Done when: one cron job renders and one upload succeeds to YT or FB.
   - Hermes cron (durable + retries) + Kanban SQLite queue + webhook->cron bridge (no native file watcher — poll via cron). YT API (100 uploads/day bucket) + FB Page (easiest) = auto; IG gated App Review; TikTok SELF_ONLY until audit (hand file+caption to human).
8. QC (10m). Done when: loudness check passes and safe-zone check passes.
   - Audio: target -16 LUFS, ceiling -1.5, tolerance 0.5; highpass 80Hz; BGM bed -18dB. TwelveLabs MCP (10h cumulative fuse) for scene-detect only if needed — dedupe before indexing ($2.50/video-hr PAYG).
   - YPP safety: 70% original input, commentary primary, human presence; AI voice reading wiki over stock = demonetized (July-2025 tightening).

## Pitfalls

- Edge-TTS for money = grey; Piper = GPL; espeak = robotic fallback only.
- Windows ffmpeg ASS colon escaping; props via file on Windows (no inline JSON with quotes).
- Kimo: CI-only Windows, deletes-only transcript, 1 undo step, no autosave — deferred.
- OpenEdit: transcribe first; `transcript.json` is the seam; EDL apply + retime.
- NLLB-600M-int8 is CC-BY-NC research-only; Google 500K free wins fluency.
- Never commit renders to git; checkpoints every 25 min; external copy of project file + selects + final.

## Verification

- `ffmpeg -version` prints; FableCut Studio exports test MP4; HyperFrames sample renders.
- One Hindi WAV (Edge draft + Azure/Kokoro publish) plays clean.
- `transcript.json` has word timings; burned-in MP4 shows captions inside safe zones.
- License log row per asset; unlisted pre-check upload passes.

## Local skill links (this repo)

- `skills/creative/ascii-video/SKILL.md` — ASCII/video conversion effects.
- `skills/creative/manim-video/SKILL.md` — math/algo animation (defer on Windows).
- `skills/creative/p5js/SKILL.md` — generative backgrounds/fillers.
- `skills/media/youtube-content/SKILL.md` — transcripts to summaries/threads.
- `skills/media/songsee/SKILL.md` — audio spectrograms/features.
- `skills/productivity/teams-meeting-pipeline/SKILL.md` — meeting pipeline pattern (cron+queue reference).
- `skills/simple-terminal-formatting/SKILL.md` — reply formatting for Soham (plain terminal, wide tables).
- Source research: `cache/scratch/agent-video-house/round1.md` … `round16.md`, `round5-final-blueprint.md`, `round14.md` (3-day starter), `closeout-report.md`.
