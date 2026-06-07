"""Font loading and text measurement helpers."""
from __future__ import annotations

from pathlib import Path
from PIL import ImageFont

_FALLBACK_FONTS = [
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "C:/Windows/Fonts/arialbd.ttf",
]


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a TrueType font, falling back to system fonts if *path* doesn't exist."""
    if Path(path).exists():
        return ImageFont.truetype(path, size)
    for fp in _FALLBACK_FONTS:
        if Path(fp).exists():
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def measure_text(text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    """Return (width, height) of *text* rendered in *font*."""
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]
