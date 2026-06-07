# Video Editor — Claude Code Instructions

This project edits short-form social media videos (Reels / TikTok / Shorts) in the style of high-performing Vietnamese finance content. Claude Code should use this file as the primary guide for every task.

---

## Project layout

```
video-editor/
├── CLAUDE.md                   ← you are here
├── requirements.txt
├── config/
│   └── style_presets.yaml      ← visual style settings
├── examples/
│   ├── README.md
│   └── sample_config.yaml      ← per-video overrides
├── scripts/
│   ├── install.sh
│   └── process.sh
└── src/
    ├── main.py                 ← CLI entry point
    ├── pipeline.py             ← orchestrator
    ├── transcribe.py           ← Whisper transcription
    ├── analyze.py              ← LLM keyword + message analysis  ★
    ├── utils/
    │   ├── video.py
    │   └── fonts.py
    └── effects/
        ├── color_grade.py
        ├── captions.py         ← CapCut-style animated captions
        ├── text_overlay.py     ← static card overlays
        ├── transitions.py
        └── attention.py        ← zoom, flash, shake on keywords  ★
```

---

## Core workflow (pipeline.py)

1. Load raw clip
2. Reframe → target aspect ratio (default 9:16 vertical)
3. Transcribe audio → word-level timestamps (faster-whisper)
4. **Analyse content** → main message + keywords + key moments (Claude API)
5. Color grade (desaturate / cinematic / b&w)
6. **Attention effects** tied to detected keywords (zoom punch, flash, slow zoom, shake)
7. Animated captions with keyword accent highlighting
8. Static text overlay cards
9. Fade in / fade out
10. Export via FFmpeg

---

## Key design decisions

- **Analysis first, effects second.** `analyze.py` runs before any visual effect so all downstream modules can use the keyword/moment data.
- **Config-driven.** Every parameter lives in YAML (`config/style_presets.yaml` + per-video overrides). Never hard-code magic numbers in effect modules.
- **FFmpeg for color grading.** MoviePy is used for compositing; FFmpeg filtergraphs handle color work.
- **Claude API for NLP.** `analyze.py` uses `claude-3-5-haiku-20241022` with structured JSON output. The prompt is in the function — keep it there.
- **Word-level captions.** Each word is rendered as an individual clip and composited over the base. Keywords from `analyze.py` are highlighted in accent colour.

---

## How to run

```bash
# Install
bash scripts/install.sh

# Process a video with defaults
python src/main.py input.mp4 output.mp4

# With a per-video config
python src/main.py input.mp4 output.mp4 --config examples/sample_config.yaml

# Skip analysis (faster, no API call)
python src/main.py input.mp4 output.mp4 --no-analysis
```

---

## Environment variables

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | Claude API — required for keyword analysis |
| `WHISPER_MODEL` | Override Whisper model size (default: `base`) |

---

## Adding a new effect

1. Create `src/effects/my_effect.py` with a function `apply_my_effect(clip, config) -> clip`.
2. Import and call it in `pipeline.py` in the correct order.
3. Add default parameters to `config/style_presets.yaml`.
4. Document usage in `examples/README.md`.

---

## Style guide

- **Format:** vertical 9:16 (1080×1920)
- **Color:** desaturated / cinematic — muted tones, high contrast
- **Captions:** bold white text, accent colour highlights on keywords, word-by-word animation
- **Attention effects:** subtle zoom punches (1.0→1.08 scale) on high-impact keywords; colour flash on the single highest-impact moment; slow zoom on key insight moments
- **Typography:** use `fonts/Montserrat-Bold.ttf` or `fonts/NotoSans-Bold.ttf` for Vietnamese text support
