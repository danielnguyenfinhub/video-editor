"""
Static text overlay cards with animations.
Supports: fade_slide_down, fade, none.
"""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, CompositeVideoClip

from ..utils.fonts import load_font, measure_text


def apply_text_overlays(clip, overlays: list[dict], config: dict):
    """Composite all text overlay cards over *clip*."""
    extra = []
    for ov in overlays:
        ov_clip = _make_overlay_clip(ov, clip.size, config)
        if ov_clip:
            extra.append(ov_clip)
    if not extra:
        return clip
    return CompositeVideoClip([clip] + extra)


def _make_overlay_clip(ov: dict, video_size: tuple, config: dict):
    text      = ov.get("text", "")
    pos_key   = ov.get("position",  "top_center")
    font_path = ov.get("font", config.get("captions", {}).get("font", "fonts/Montserrat-Bold.ttf"))
    font_size = int(ov.get("font_size", 64))
    color     = ov.get("color",    "white")
    bg        = ov.get("bg",       None)
    start     = float(ov.get("start",    0.0))
    duration  = float(ov.get("duration", 3.0))
    animation = ov.get("animation", "fade_slide_down")

    font = load_font(font_path, font_size)
    tw, th = measure_text(text, font)
    pad  = 24
    img  = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    if bg:
        ImageDraw.Draw(img).rectangle([0, 0, img.width, img.height], fill=bg)
    ImageDraw.Draw(img).text((pad, pad), text, font=font, fill=color)

    arr  = np.array(img)
    base = ImageClip(arr, ismask=False).set_duration(duration).set_start(start)

    vw, vh = video_size
    x, y = _position_xy(pos_key, vw, vh, img.width, img.height)

    if animation == "fade_slide_down":
        base = (
            base
            .set_position(lambda t: (x, y - int((1 - min(t / 0.4, 1.0)) * 40)))
            .crossfadein(0.4)
        )
    elif animation == "fade":
        base = base.crossfadein(0.3).set_position((x, y))
    else:
        base = base.set_position((x, y))

    return base


def _position_xy(pos_key: str, vw: int, vh: int, iw: int, ih: int) -> tuple[int, int]:
    mapping = {
        "top_center":    ((vw - iw) // 2,          int(vh * 0.05)),
        "top_left":      (int(vw * 0.05),           int(vh * 0.05)),
        "top_right":     (vw - iw - int(vw * 0.05), int(vh * 0.05)),
        "center":        ((vw - iw) // 2,           (vh - ih) // 2),
        "bottom_center": ((vw - iw) // 2,           vh - ih - int(vh * 0.08)),
        "bottom_left":   (int(vw * 0.05),           vh - ih - int(vh * 0.08)),
        "bottom_right":  (vw - iw - int(vw * 0.05), vh - ih - int(vh * 0.08)),
    }
    return mapping.get(pos_key, ((vw - iw) // 2, int(vh * 0.05)))
