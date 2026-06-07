"""
Full video editing pipeline orchestrator.

Order of operations:
  1.  Load raw clip
  2.  Reframe to target aspect ratio (vertical 9:16 default)
  3.  Transcribe audio → word-level timestamps
  4.  Analyse content  → main message + keywords + key moments
  5.  Color grade
  6.  Attention effects (zoom punch, flash, slow zoom)
  7.  Animated captions (keyword-aware highlighting)
  8.  Static text overlay cards
  9.  Fade in / fade out
  10. Export via FFmpeg
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from moviepy.editor import VideoFileClip

from .transcribe import transcribe
from .analyze import analyze, AnalysisResult, WordToken
from .effects.color_grade import apply_color_grade
from .effects.captions import render_captions
from .effects.text_overlay import apply_text_overlays
from .effects.transitions import apply_fade
from .effects.attention import apply_attention_effects
from .utils.video import reframe_clip, export_clip


def run(
    input_path: str,
    output_path: str,
    config: dict,
    verbose: bool = True,
) -> None:
    def log(msg: str) -> None:
        if verbose:
            print(f"[pipeline] {msg}")

    # ── 1. Load ────────────────────────────────────────────────────────────────────────
    log(f"Loading {input_path} …")
    clip = VideoFileClip(input_path)
    log(f"  Duration: {clip.duration:.1f}s  |  Size: {clip.size}  |  FPS: {clip.fps}")

    # ── 2. Reframe ───────────────────────────────────────────────────────────────────────
    fmt = config.get("format", "vertical")
    target_size = _target_size(fmt)
    log(f"Reframing to {fmt} ({target_size[0]}×{target_size[1]}) …")
    clip = reframe_clip(clip, target_size)

    # ── 3. Transcribe ─────────────────────────────────────────────────────────────────────
    analysis: Optional[AnalysisResult] = None
    word_tokens: list[WordToken] = []

    if config.get("captions", {}).get("enabled", True) or config.get("analysis", {}).get("enabled", True):
        log("Transcribing audio …")
        segments = transcribe(
            input_path,
            model=config.get("whisper_model", "base"),
            language=config.get("language", None),
        )
        for seg in segments:
            for w in seg.get("words", []):
                word_tokens.append(WordToken(word=w["word"], start=w["start"], end=w["end"]))
        log(f"  Transcribed {len(word_tokens)} words.")

    # ── 4. Analyse content ───────────────────────────────────────────────────────────────
    analysis_cfg = config.get("analysis", {})
    if analysis_cfg.get("enabled", True) and word_tokens:
        log("Analysing content for keywords and key moments …")
        analysis = analyze(
            word_tokens,
            model=analysis_cfg.get("model", "claude-3-5-haiku-20241022"),
            max_keywords=analysis_cfg.get("max_keywords", 8),
            language_hint=analysis_cfg.get("language_hint"),
            verbose=verbose,
        )
        log(f"  Main message : {analysis.main_message!r}")
        log(f"  Keywords     : {[k.phrase for k in analysis.keywords]}")
        log(f"  Key moments  : {len(analysis.key_moments)} triggers")
        if analysis_cfg.get("print_summary", True):
            _print_analysis_summary(analysis)

    # ── 5. Color grade ───────────────────────────────────────────────────────────────────
    grade = config.get("color_grade", "desaturate")
    if grade and grade != "none":
        log(f"Color grading ({grade}) …")
        clip = apply_color_grade(clip, grade, config.get("color_grade_options", {}))

    # ── 6. Attention effects ─────────────────────────────────────────────────────────────
    if analysis and analysis_cfg.get("apply_effects", True):
        log("Applying attention effects …")
        clip = apply_attention_effects(clip, analysis, config)

    # ── 7. Animated captions ─────────────────────────────────────────────────────────────
    caption_cfg = config.get("captions", {})
    if caption_cfg.get("enabled", True) and word_tokens:
        log("Rendering captions …")
        clip = render_captions(
            clip,
            word_tokens=[{"word": t.word, "start": t.start, "end": t.end} for t in word_tokens],
            config=caption_cfg,
            keywords=analysis.keywords if analysis else [],
        )

    # ── 8. Text overlay cards ────────────────────────────────────────────────────────────
    overlays = config.get("text_overlays", [])
    if overlays:
        log(f"Applying {len(overlays)} text overlay(s) …")
        clip = apply_text_overlays(clip, overlays, config)

    # ── 9. Fades ───────────────────────────────────────────────────────────────────────
    fade_in  = float(config.get("fade_in",  0.4))
    fade_out = float(config.get("fade_out", 0.4))
    if fade_in > 0 or fade_out > 0:
        log(f"Applying fades (in={fade_in}s, out={fade_out}s) …")
        clip = apply_fade(clip, fade_in=fade_in, fade_out=fade_out)

    # ── 10. Export ───────────────────────────────────────────────────────────────────────
    log(f"Exporting to {output_path} …")
    export_clip(clip, output_path, config.get("export", {}))
    log("✅ Done!")


def _target_size(fmt: str) -> tuple[int, int]:
    return {"vertical": (1080, 1920), "square": (1080, 1080), "landscape": (1920, 1080)}.get(fmt, (1080, 1920))


def _print_analysis_summary(analysis: AnalysisResult) -> None:
    print("\n" + "═" * 60)
    print("📊  CONTENT ANALYSIS SUMMARY")
    print("═" * 60)
    print(f"  Main message : {analysis.main_message}")
    print()
    print("  Keywords:")
    for kw in analysis.keywords:
        bar = "🔴" if kw.impact == "high" else "🟡"
        print(f"    {bar}  {kw.phrase!r:25s}  @ {kw.start:.1f}s  —  {kw.reason}")
    print()
    print("  Key moments:")
    icons = {"zoom_punch": "🔍", "color_flash": "⚡", "slow_zoom": "🎥", "caption_highlight": "✨", "shake": "📳"}
    for m in analysis.key_moments:
        print(f"    {icons.get(m.effect,'🎬')}  {m.effect:20s}  {m.start:.1f}s – {m.end:.1f}s  intensity={m.intensity:.0%}")
    print("═" * 60 + "\n")
