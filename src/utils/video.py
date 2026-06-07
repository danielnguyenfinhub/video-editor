"""Video I/O helpers."""
from __future__ import annotations

from moviepy.editor import VideoFileClip
import numpy as np


def reframe_clip(clip: VideoFileClip, target_size: tuple[int, int]) -> VideoFileClip:
    """
    Crop and scale *clip* to *target_size* (w, h) while keeping centre frame.
    Adds black bars if the source is narrower than target.
    """
    tw, th = target_size
    sw, sh = clip.size
    target_ratio = tw / th
    source_ratio = sw / sh

    if abs(source_ratio - target_ratio) < 0.01:
        return clip.resize(target_size)

    if source_ratio > target_ratio:
        # Source is wider → crop sides
        new_w = int(sh * target_ratio)
        x1 = (sw - new_w) // 2
        clip = clip.crop(x1=x1, x2=x1 + new_w)
    else:
        # Source is taller → crop top/bottom
        new_h = int(sw / target_ratio)
        y1 = (sh - new_h) // 2
        clip = clip.crop(y1=y1, y2=y1 + new_h)

    return clip.resize(target_size)


def export_clip(clip, output_path: str, export_cfg: dict) -> None:
    """Write *clip* to *output_path* using MoviePy / FFmpeg."""
    clip.write_videofile(
        output_path,
        codec=export_cfg.get("codec", "libx264"),
        audio_codec=export_cfg.get("audio_codec", "aac"),
        bitrate=export_cfg.get("bitrate", "8000k"),
        fps=export_cfg.get("fps", 30),
        preset=export_cfg.get("preset", "slow"),
        threads=4,
        logger="bar",
    )
