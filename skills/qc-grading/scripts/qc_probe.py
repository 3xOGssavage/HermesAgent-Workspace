"""QC probe: extract grade frames + metrics for any video.

Usage (Clipping venv python):
  qc_probe.py --video <mp4> --mode short|long|sweep [--out dir]

short: t=1, dur/2, dur-1. long: hook + end + every 15s.
sweep: hook + end + every 60s (long-form). Writes PNGs +
qc_report.json: {t, faces, sharpness, brightness}.
Sharpness = variance of Laplacian (numpy only). Faces via the
pipeline detector when importable, else [].
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def ffprobe_dur(video):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration", "-of", "csv=p=0", str(video)],
        capture_output=True, text=True)
    return float(r.stdout.strip())


def grab(video, t, out, ffm="ffmpeg", ffp="ffprobe"):
    subprocess.run(
        [ffm, "-y", "-v", "error", "-ss", str(t),
         "-i", str(video), "-frames:v", "1", str(out)],
        capture_output=True, timeout=120)
    return out if Path(out).exists() else None


def sharpness(png):
    try:
        import numpy as np
        from PIL import Image
        g = np.asarray(Image.open(png).convert("L"), dtype=float)
        k = g[2:, 1:-1] + g[:-2, 1:-1] + g[1:-1, 2:] + g[1:-1, :-2] - 4 * g[1:-1, 1:-1]
        return round(float(k.var()), 1)
    except Exception:
        return -1.0


def dark(png):
    try:
        import numpy as np
        from PIL import Image
        g = np.asarray(Image.open(png).convert("L"), dtype=float)
        return round(float(g.mean()), 1)
    except Exception:
        return -1.0


def faces(png):
    try:
        sys.path.insert(0, "F:/CD/Projects/Clipping")
        import clip as C
        import mediapipe as mp
        import numpy as np
        from PIL import Image
        det = C._get_face_detector()
        img = Image.open(png).convert("RGB")
        w, h = img.size
        rgb = np.ascontiguousarray(np.asarray(img))
        res = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
        out = []
        for d in (res.detections or []):
            bb = d.bounding_box
            out.append({"score": round(C._det_score(d), 3),
                        "cx": round((bb.origin_x + bb.width / 2) / w, 3),
                        "cy": round((bb.origin_y + bb.height / 2) / h, 3),
                        "w": round(bb.width / w, 3),
                        "h": round(bb.height / h, 3)})
        return sorted(out, key=lambda b: -b["score"])[:4]
    except Exception:
        return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--mode", default="short",
                    choices=["short", "long", "sweep"])
    ap.add_argument("--out", default="qc_out")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    try:
        dur = ffprobe_dur(a.video)
    except Exception as e:
        print(f"QC-PROBE-FAIL: cannot read duration of {a.video}: {e}")
        raise SystemExit(2)
    if a.mode == "short":
        ts = [1.0, dur / 2, max(dur - 1, 1.5)]
    elif a.mode == "long":
        ts = [1.0] + [float(t) for t in range(15, int(dur), 15)] + [max(dur - 1, 1.5)]
    else:
        ts = [1.0] + [float(t) for t in range(60, int(dur), 60)] + [max(dur - 1, 1.5)]
    rep = []
    for i, t in enumerate(ts):
        f = out / f"qc_{i:03d}_t{t:.1f}.png"
        if grab(a.video, round(t, 1), f):
            rep.append({"t": round(t, 1), "file": str(f),
                        "faces": faces(f), "sharpness": sharpness(f),
                        "brightness": dark(f)})
    (out / "qc_report.json").write_text(json.dumps(
        {"video": str(a.video), "duration": dur, "frames": rep}, indent=1))
    print(f"QC-PROBE-OK: {len(rep)} frames")


if __name__ == "__main__":
    main()
