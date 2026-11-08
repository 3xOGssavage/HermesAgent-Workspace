"""Rank fresh story blocks from transcript.json, excluding rendered ranges.

Recipe (tested): score density of MONEY/NUM/EMO/question/HOOK cues per
second, merge segs with gap<=2.5s into 15-50s blocks, plus single
15-50s segments (rants hold without merging), skip blocks that
overlap rendered moments by more than half. Print top 12, paste picks
into moments.json as {id, start, end, score, text} (backup first).

Usage: set SLUG below, run with the campaign venv:
  ./.venv/Scripts/python.exe scripts/rank_fresh_blocks.py
  (cwd = F:/CD/Projects/Clipping)
"""
import json
import re
from pathlib import Path

SLUG = "mrbeast-test"  # <-- set per job
CAMP = Path("campaigns") / SLUG

T = json.load(open(CAMP / "transcript.json"))
segs = T.get("segments", T if isinstance(T, list) else [])
M = json.load(open(CAMP / "moments.json"))
used = [(float(x.get("start", 0)), float(x.get("end", 0))) for x in M]

MONEY = re.compile(r"\$|dollar|money|paid|won|prize|cash|buy|bought|cost", re.I)
NUM = re.compile(r"\d")
EMO = re.compile(r"amazing|crazy|insane|love|hate|scared|fear|die|kill|win|lose|shocking|unbelievable|incredible|wow|oh my|no way", re.I)
Q = re.compile(r"\?")
HOOK = re.compile(r"^(watch|look|listen|stop|wait|imagine|what|this is|you guys|three|day \d+)", re.I)


def score(text):
    s = 0.0
    s += 3.0 * len(MONEY.findall(text))
    s += 0.5 * len(NUM.findall(text))
    s += 1.5 * len(EMO.findall(text))
    s += 2.0 * len(Q.findall(text))
    s += 2.0 if HOOK.search(text.strip()) else 0.0
    return s


def overlaps(a, b):
    return not (a[1] <= b[0] or a[0] >= b[1])


blocks, cur, c0, c1 = [], [], None, None
S = sorted(segs, key=lambda s: float(s.get("start", 0)))
for s in S:
    st = float(s.get("start", 0))
    en = float(s.get("end", st + 1))
    tx = s.get("text", "")
    if c0 is None:
        c0, c1, cur = st, en, [(st, en, tx)]
    elif st - c1 <= 2.5 and en - c0 <= 45:
        c1, cur = en, cur + [(st, en, tx)]
    else:
        blocks.append((c0, c1, cur))
        c0, c1, cur = st, en, [(st, en, tx)]
if c0 is not None:
    blocks.append((c0, c1, cur))

out = []
for a, b, parts in blocks:
    dur = b - a
    if not (15 <= dur <= 50):
        continue
    if any(overlaps((a, b), u) and min(b, u[1]) - max(a, u[0]) > 0.5 * dur for u in used):
        continue
    text = " ".join(t for _, _, t in parts)
    out.append((score(text) / dur, a, b, dur, text[:90]))

for s in S:  # single long segments (rants hold without merging)
    a, b = float(s.get("start", 0)), float(s.get("end", 0))
    dur = b - a
    if not (15 <= dur <= 50):
        continue
    if any(overlaps((a, b), u) and min(b, u[1]) - max(a, u[0]) > 0.5 * dur for u in used):
        continue
    if any(abs(round(a, 1) - round(x[1], 1)) < 2 for x in out):
        continue
    out.append((score(s.get("text", "")) / max(dur, 1) + 0.05, a, b, dur, s.get("text", "")[:90])

out.sort(reverse=True)
for sc, a, b, d, t in out[:12]:
    print(f"{sc:5.2f}/s {a:8.1f}-{b:8.1f} ({d:4.1f}s) {t}")
print(f"candidates: {len(out)}")
