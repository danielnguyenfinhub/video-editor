"""
Attention Effects — visual hooks tied to keywords and key moments.

Effects available:
  zoom_punch        — quick scale-up snap on a keyword
  color_flash       — semi-transparent colour overlay burst
  slow_zoom         — gradual zoom in over a longer segment
  shake             — quick horizontal camera shake
  caption_highlight — no visual change here; handled in captions.py
"""
from __future__ import annotations

import numpy as np
from moviepy.editor import CompositeVideoClip, ColorClip

from ..analyze import AnalysisResult, KeyMoment


def apply_attention_effects(clip, analysis: AnalysisResult, config: dict):
    """
    Apply all attention effects derived from *analysis* to *clip*.
    Returns a composited clip of the same duration.
    """
    att_cfg = config.get("attention", {})
    w, h = clip.size
    overlays = []

    for moment in analysis.key_moments:
        effect = moment.effect
        start  = max(0.0, moment.start)
        end    = min(clip.duration, moment.end)
        if end <= start:
            continue

        if effect == "zoom_punch":
            clip = _apply_zoom_punch(clip, start, end, att_cfg.get("zoom_punch", {}))
        elif effect == "color_flash":
            flash = _make_color_flash(start, end, w, h, att_cfg.get("color_flash", {}), moment.intensity)
            if flash:
                overlays.append(flash)
        elif effect == "slow_zoom":
            clip = _apply_slow_zoom(clip, start, end, att_cfg.get("slow_zoom", {}))
        elif effect == "shake":
            clip = _apply_shake(clip, start, end, att_cfg.get("shake", {}))
        # caption_highlight — handled in captions.py

    if overlays:
        clip = CompositeVideoClip([clip] + overlays)

    return clip


def _apply_zoom_punch(clip, start: float, end: float, cfg: dict):
    """Scale the clip up quickly then snap back."""
    if not cfg.get("enabled", True):
        return clip
    peak_scale = float(cfg.get("scale",    1.08))
    duration   = float(cfg.get("duration", 0.25))
    w, h = clip.size

    def make_frame(t):
        frame = clip.get_frame(t)
        if start <= t <= start + duration:
            progress = (t - start) / duration
            scale = 1.0 + (peak_scale - 1.0) * _ease_in_out(progress)
            return _zoom_frame(frame, scale, w, h)
        return frame

    return clip.fl(lambda gf, t: make_frame(t))


def _apply_slow_zoom(clip, start: float, end: float, cfg: dict):
    """Gradually zoom in over [start, end]."""
    if not cfg.get("enabled", True):
        return clip
    peak_scale = float(cfg.get("scale",    1.05))
    duration   = end - start
    w, h = clip.size

    def make_frame(t):
        frame = clip.get_frame(t)
        if start <= t <= end:
            progress = (t - start) / max(duration, 0.001)
            scale = 1.0 + (peak_scale - 1.0) * progress
            return _zoom_frame(frame, scale, w, h)
        return frame

    return clip.fl(lambda gf, t: make_frame(t))


def _apply_shake(clip, start: float, end: float, cfg: dict):
    """Apply a quick horizontal shake."""
    if not cfg.get("enabled", False):
        return clip
    pixels   = int(cfg.get("pixels",   6))
    duration = float(cfg.get("duration", 0.3))

    def make_frame(t):
        frame = clip.get_frame(t)
        if start <= t <= start + duration:
            offset = int(pixels * np.sin(2 * np.pi * 30 * (t - start)))
            if offset > 0:
                return np.roll(frame, offset, axis=1)
        return frame

    return clip.fl(lambda gf, t: make_frame(t))


def _make_color_flash(start, end, w, h, cfg, intensity) -> ColorClip | None:
    """Return a semi-transparent colour overlay clip."""
    if not cfg.get("enabled", True):
        return None
    color   = tuple(cfg.get("color", [255, 220, 0]))
    opacity = float(cfg.get("opacity", 0.18)) * intensity
    dur     = float(cfg.get("duration", 0.15))
    flash = ColorClip(size=(w, h), color=color, duration=dur)
    flash = flash.set_opacity(opacity).set_start(start)
    return flash


def _zoom_frame(frame: np.ndarray, scale: float, w: int, h: int) -> np.ndarray:
    from PIL import Image
    img   = Image.fromarray(frame)
    new_w = int(w / scale)
    new_h = int(h / scale)
    left  = (w - new_w) // 2
    top   = (h - new_h) // 2
    img   = img.crop((left, top, left + new_w, top + new_h))
    img   = img.resize((w, h), Image.LANCZOS)
    return np.array(img)


def _ease_in_out(t: float) -> float:
    return t * t * (3 - 2 * t)
