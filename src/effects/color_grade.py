"""Color grading effects applied via FFmpeg filtergraph."""
from __future__ import annotations

import subprocess
import tempfile
import os

from moviepy.editor import VideoFileClip


def apply_color_grade(clip, preset: str, options: dict):
    """
    Apply a color grade to *clip* using FFmpeg.

    Presets:
      desaturate  — muted saturation, slight contrast boost
      cinematic   — low sat + lifted blacks + slight vignette
      bw          — full black & white
    """
    filtergraph = _build_filtergraph(preset, options)
    if not filtergraph:
        return clip

    with tempfile.TemporaryDirectory() as tmp:
        in_path  = os.path.join(tmp, "in.mp4")
        out_path = os.path.join(tmp, "out.mp4")

        clip.write_videofile(in_path, codec="libx264", audio_codec="aac",
                             logger=None, verbose=False)

        cmd = ["ffmpeg", "-y", "-i", in_path, "-vf", filtergraph, "-c:a", "copy", out_path]
        subprocess.run(cmd, check=True, capture_output=True)

        graded = VideoFileClip(out_path)
        graded = graded.set_audio(clip.audio)
        return graded


def _build_filtergraph(preset: str, options: dict) -> str:
    sat      = options.get("saturation",  0.35)
    contrast = options.get("contrast",    1.15)
    bright   = options.get("brightness",  0.0)

    if preset == "bw":
        return "hue=s=0,eq=contrast=1.2:brightness=-0.05"

    if preset == "cinematic":
        return (
            f"hue=s={sat},"
            f"eq=contrast={contrast}:brightness={bright - 0.05},"
            "curves=all='0/0.05 1/0.95',"
            "vignette=PI/4"
        )

    # default: desaturate
    return f"hue=s={sat},eq=contrast={contrast}:brightness={bright}"
