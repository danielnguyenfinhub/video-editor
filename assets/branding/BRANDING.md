# 🎨 FinHub Branding Assets

This folder contains the official FinHub branding assets used by the video editor.

---

## 📁 Files

| File | Description |
|------|-------------|
| `logo.png` | FinHub logo — desaturated/B&W version recommended for video overlays |
| `banner.mp4` | FinHub branded email/reel banner — use as intro or outro card |

---

## 🎬 Where to Use These Assets

### 1. **Logo — `logo.png`**

Used in `src/effects/text_overlay.py` as a watermark or branded card.

**In `examples/sample_config.yaml`**, reference it under `branding`:
```yaml
branding:
  logo: assets/branding/logo.png
  position: bottom_right   # top_left | top_right | bottom_left | bottom_right
  opacity: 0.8
  scale: 0.15              # 15% of video width
```

**When to show the logo:**
- Bottom-right corner watermark throughout the reel
- On the outro card (last 2–3 seconds)
- On title card overlays (`text_overlay.py`)

To add a logo watermark in your pipeline, in `src/pipeline.py`:
```python
from src.effects.text_overlay import add_logo_watermark

add_logo_watermark(
    video_path="output_graded.mp4",
    logo_path="assets/branding/logo.png",
    position="bottom_right",
    opacity=0.8,
    scale=0.15
)
```

---

### 2. **Video Banner — `banner.mp4`**

Used as a branded intro or outro bumper clip appended to the reel.

**In `examples/sample_config.yaml`**, reference it under `branding`:
```yaml
branding:
  intro_banner: assets/branding/banner.mp4   # plays at start
  outro_banner: assets/branding/banner.mp4   # plays at end
  banner_duration: 3.0                        # seconds to show
```

**When to use the banner:**
- **Intro**: First 2–3 seconds of reel before main content
- **Outro**: Last 2–3 seconds with a call-to-action
- **Transition card**: Between major sections of a long video

To prepend/append the banner in `src/pipeline.py`:
```python
import subprocess

def prepend_banner(banner_path, main_video, output_path):
    """Concatenate banner.mp4 + main video."""
    with open("/tmp/concat_list.txt", "w") as f:
        f.write(f"file '{banner_path}'\n")
        f.write(f"file '{main_video}'\n")
    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", "/tmp/concat_list.txt",
        "-c", "copy", output_path
    ], check=True)
```

---

## 🎨 Style Guide for Overlays

| Setting | Value |
|---------|-------|
| Color grade | Desaturated / B&W |
| Logo opacity | 70–85% |
| Logo position | Bottom-right or bottom-center |
| Banner duration | 2–3 seconds |
| Font | Bold, white, Vietnamese-ready (Noto Sans, Roboto Bold) |

---

## 📌 Quick Reference

```
assets/
└── branding/
    ├── logo.png       ← Watermark / title card / outro card
    ├── banner.mp4     ← Intro bumper / outro bumper
    └── BRANDING.md    ← This file
```
