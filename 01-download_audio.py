"""
01-download_audio.py
Step 1: download the audio of one "Befarmaeed Sham" episode from YouTube.

Outputs:
    data/audio/episode01.wav        local only (git-ignored), input for step 02 (Whisper)
    outputs/01-download_info.txt    commit & push this one

Requirements (install once):
    pip install yt-dlp
    ffmpeg must be installed and on PATH
        Windows:  winget install ffmpeg   (then restart PyCharm)
"""
from datetime import datetime
from pathlib import Path
import traceback

import yt_dlp
from yt_dlp.utils import download_range_func

# ---------------- settings ----------------
URL = "https://www.youtube.com/watch?v=3K3rDlrreHU"
ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / "data" / "audio"
OUT_DIR = ROOT / "outputs"
OUT_NAME = "episode01"

# Whole episode: leave both as None.
# Only from minute 28 to the end:  START = "00:28:00", END = None
START = None
END = None
# ------------------------------------------


def to_seconds(t: str) -> int:
    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s


AUDIO_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)
log_path = OUT_DIR / "01-download_info.txt"
wav_path = AUDIO_DIR / f"{OUT_NAME}.wav"

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": str(AUDIO_DIR / f"{OUT_NAME}.%(ext)s"),
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "wav",
    }],
}

if START or END:
    start_s = to_seconds(START) if START else 0
    end_s = to_seconds(END) if END else float("inf")
    ydl_opts["download_ranges"] = download_range_func(None, [(start_s, end_s)])
    ydl_opts["force_keyframes_at_cuts"] = True

lines = [
    "01-download_audio",
    f"Run at   : {datetime.now():%Y-%m-%d %H:%M}",
    f"URL      : {URL}",
    f"Range    : {START or 'start'} -> {END or 'end'}",
]

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=True)
    size_mb = wav_path.stat().st_size / 1e6 if wav_path.exists() else 0
    lines += [
        "Status   : OK",
        f"Title    : {info.get('title')}",
        f"Channel  : {info.get('channel') or info.get('uploader')}",
        f"Upload   : {info.get('upload_date')}",
        f"Duration : {round((info.get('duration') or 0) / 60, 1)} minutes",
        f"WAV file : {wav_path.relative_to(ROOT)} ({size_mb:.1f} MB, local only)",
    ]
except Exception:
    lines += ["Status   : ERROR", "", traceback.format_exc()]

report = "\n".join(lines)
log_path.write_text(report, encoding="utf-8")
print(report)
print(f"\nSaved report to {log_path.relative_to(ROOT)} -> commit & push it.")
