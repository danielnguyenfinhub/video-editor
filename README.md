# 🎬 Video Editor

> Claude Code–friendly Python video editor for social media Reels, TikTok & YouTube Shorts.  
> Auto-detects keywords, applies attention effects, and renders CapCut-style captions.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎙️ **Auto-transcription** | faster-whisper with word-level timestamps |
| 🧠 **AI content analysis** | Claude detects main message, keywords & key moments |
| 🔍 **Zoom punch** | Quick scale-up on high-impact keywords |
| ⚡ **Colour flash** | Dramatic overlay burst on peak moments |
| 🎥 **Slow zoom** | Gradual pull-in on insight moments |
| ✨ **Animated captions** | Word-by-word reveal with keyword accent colour |
| 🎨 **Color grading** | Desaturate / cinematic / B&W via FFmpeg |
| 📝 **Text overlays** | Animated card overlays with slide/fade animations |
| 📱 **9:16 vertical** | Auto-reframes landscape footage for Reels |

---

## 🚀 Quick start

```bash
# 1. Clone
git clone https://github.com/danielnguyenfinhub/video-editor.git
cd video-editor

# 2. Install (creates .venv, downloads fonts)
bash scripts/install.sh

# 3. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...

# 4. Edit a video
source .venv/bin/activate
python src/main.py input/my_video.mp4 output/result.mp4
```

---

## 📖 Usage

```bash
# Basic (uses default style_presets.yaml)
python src/main.py input.mp4 output.mp4

# With per-video config override
python src/main.py input.mp4 output.mp4 --config examples/sample_config.yaml

# Skip AI analysis (faster, no API call)
python src/main.py input.mp4 output.mp4 --no-analysis

# Quick color preset shortcut
python src/main.py input.mp4 output.mp4 --preset bw

# Wrapper script
bash scripts/process.sh input/my_video.mp4
```

---

## 🧠 How AI analysis works

1. The video is transcribed word-by-word with Whisper
2. The transcript is sent to **Claude** (`claude-3-5-haiku`) with a prompt asking for:
   - **Main message** — one-sentence summary of the core idea
   - **Keywords** — impactful phrases (rated high / medium) with timestamps
   - **Key moments** — segments mapped to specific visual effects
3. Each keyword triggers a visual effect at its exact timestamp:
   - `zoom_punch` → scale snap (default 1.08×)
   - `color_flash` → yellow overlay burst
   - `slow_zoom` → gradual pull-in
   - `shake` → horizontal camera shake (use sparingly)
   - `caption_highlight` → accent colour in captions only

The analysis summary is printed to console so you can review it before the video renders.

---

## ⚙️ Configuration

Edit `config/style_presets.yaml` for global defaults, or pass a per-video YAML:

```yaml
# examples/sample_config.yaml
format: vertical
whisper_model: small      # better accuracy for Vietnamese
language: vi

analysis:
  enabled: true
  language_hint: "Vietnamese finance content about home loans"
  max_keywords: 6

color_grade: cinematic
captions:
  font_size: 72
  highlight_color: "#FFE000"
  words_per_line: 3
```

---

## 📁 Project structure

```
video-editor/
├── CLAUDE.md                    ← instructions for Claude Code
├── requirements.txt
├── config/style_presets.yaml    ← global defaults
├── examples/sample_config.yaml  ← per-video override example
├── scripts/
│   ├── install.sh
│   └── process.sh
└── src/
    ├── main.py                  ← CLI
    ├── pipeline.py              ← orchestrator
    ├── transcribe.py            ← Whisper
    ├── analyze.py               ← Claude keyword extraction ★
    ├── utils/
    │   ├── video.py
    │   └── fonts.py
    └── effects/
        ├── color_grade.py
        ├── captions.py          ← animated captions ★
        ├── text_overlay.py
        ├── transitions.py
        └── attention.py         ← zoom, flash, shake ★
```

---

## 🔑 Environment variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | For AI analysis | Claude API key |
| `WHISPER_MODEL` | No | Override model size (tiny/base/small/medium/large) |

---

## 📦 Dependencies

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — transcription
- [moviepy](https://github.com/Zulko/moviepy) — video compositing
- [Pillow](https://pillow.readthedocs.io/) — image rendering
- [anthropic](https://github.com/anthropics/anthropic-sdk-python) — Claude API
- FFmpeg (system) — color grading & export

---

## 🤝 Working with Claude Code

This repo ships with `CLAUDE.md` at the root. When you open it in Claude Code:
- Claude understands the full pipeline and file layout
- Ask Claude to add a new effect, tweak caption style, or adjust keyword sensitivity
- Claude knows to update `style_presets.yaml` for config changes, not hard-code values

---

*Built for FinHub — Vietnamese mortgage & finance short-form content.*
