"""
CapCut-style animated word-highlighting captions.

Features:
  - Word-by-word reveal animation
  - Keyword accent colour from analyze.py
  - Vietnamese / multilingual support via Noto fonts
  - Configurable position, font, size, stroke
"""
from __future__ import annotations

from typing import Any

import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, CompositeVideoClip

from ..utils.fonts import load_font, measure_text


def render_captions(
    clip,
    word_tokens: list[dict[str, Any]],
    config: dict,
    keywords: list = [],
) -> CompositeVideoClip:
    """
    Composite animated captions over *clip*.
    *keywords* is a list of Keyword dataclass instances from analyze.py.
    """
    font_path   = config.get("font",           "fonts/Montserrat-Bold.ttf")
    font_size   = int(config.get("font_size",  68))
    color       = config.get("color",          "white")
    stroke_col  = config.get("stroke_color",   "black")
    stroke_w    = int(config.get("stroke_width", 3))
    hi_color    = config.get("highlight_color", "#FFE000")
    position    = config.get("position",        "bottom")
    wpline      = int(config.get("words_per_line", 4))
    animation   = config.get("animation",       "word_by_word")

    font = load_font(font_path, font_size)

    # Build keyword word lookup
    kw_words: set[str] = set()
    for kw in keywords:
        for w_str in kw.phrase.lower().split():
            kw_words.add(w_str.strip(".,!?:;\"'"))

    groups = _group_words(word_tokens, wpline)
    caption_clips = []

    for group in groups:
        if not group:
            continue
        start = group[0]["start"]
        end   = group[-1]["end"]

        if animation == "word_by_word":
            clips = _word_by_word_clips(
                group, clip.size, font, color,
                stroke_col, stroke_w, hi_color, kw_words, position, start, end,
            )
        else:
            img = _render_line(group, clip.size[0], font, color, stroke_col, stroke_w, hi_color, kw_words, highlight_all=True)
            clips = [_img_to_clip(img, clip.size, position, start, end - start)]

        caption_clips.extend(clips)

    if not caption_clips:
        return clip

    return CompositeVideoClip([clip] + caption_clips)


def _word_by_word_clips(group, video_size, font, color, stroke_col, stroke_w, hi_color, kw_words, position, group_start, group_end):
    clips = []
    for i, token in enumerate(group):
        active_words = {token["word"].lower().strip(".,!?:;\"'")}
        img = _render_line(group, video_size[0], font, color, stroke_col, stroke_w, hi_color, kw_words, active_words=active_words)
        t_start = token["start"]
        t_end   = group[i + 1]["start"] if i + 1 < len(group) else group_end
        dur = max(t_end - t_start, 0.05)
        clips.append(_img_to_clip(img, video_size, position, t_start, dur))
    return clips


def _render_line(tokens, video_w, font, color, stroke_col, stroke_w, hi_color, kw_words, active_words=None, highlight_all=False) -> Image.Image:
    padding = 20
    word_imgs = []
    for t in tokens:
        word = t["word"]
        is_kw     = word.lower().strip(".,!?:;\"'") in kw_words
        is_active = highlight_all or (active_words and word.lower().strip(".,!?:;\"'") in active_words)
        fill = hi_color if (is_kw or is_active) else color
        word_imgs.append((word + " ", fill))

    total_w = sum(measure_text(w, font)[0] for w, _ in word_imgs) + padding * 2
    _, line_h = measure_text("Ay", font)
    total_h = line_h + stroke_w * 2 + padding * 2

    img  = Image.new("RGBA", (max(total_w, 10), total_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    x, y = padding, padding
    for word, fill in word_imgs:
        for dx in range(-stroke_w, stroke_w + 1):
            for dy in range(-stroke_w, stroke_w + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), word, font=font, fill=stroke_col)
        draw.text((x, y), word, font=font, fill=fill)
        x += measure_text(word, font)[0]

    return img


def _img_to_clip(img: Image.Image, video_size: tuple, position: str, start: float, duration: float):
    arr  = np.array(img)
    clip = ImageClip(arr, ismask=False).set_duration(duration).set_start(start)
    vw, vh = video_size
    iw, ih = img.size
    x = (vw - iw) // 2
    if position == "bottom":
        y = vh - ih - int(vh * 0.08)
    elif position == "top":
        y = int(vh * 0.05)
    else:
        y = (vh - ih) // 2
    return clip.set_position((x, y))


def _group_words(tokens: list[dict], words_per_line: int) -> list[list[dict]]:
    return [tokens[i:i + words_per_line] for i in range(0, len(tokens), words_per_line)]
