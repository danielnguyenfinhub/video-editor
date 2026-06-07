"""Transition effects — fade in / fade out."""
from __future__ import annotations

from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout


def apply_fade(clip, fade_in: float = 0.4, fade_out: float = 0.4):
    """Apply fade-in and fade-out to *clip*."""
    if fade_in > 0:
        clip = clip.fx(fadein, fade_in)
    if fade_out > 0:
        clip = clip.fx(fadeout, fade_out)
    return clip
