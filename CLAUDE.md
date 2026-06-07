# 🎬 Claude Code Instructions — FinHub Video Editor

You are helping edit social media videos (Facebook/Instagram Reels, TikTok) in the **FinHub style**:
- **9:16 vertical format** (1080×1920)
- **Desaturated / B&W colour grading**
- **Bold Vietnamese text overlays**
- **CapCut-style animated captions** (word-by-word highlighting)
- **Attention effects** tied to speech keywords (zoom punches, colour pops, shakes)

---

## 🗂 Project Structure

```
video-editor/
├── src/
│   ├── main.py              # CLI entry point
│   ├── transcribe.py        # Whisper transcription (word-level timestamps)
│   ├── analyze.py           # Keyword/moment detection (optional Claude API)
│   ├── pipeline.py          # Full pipeline orchestrator
│   └── effects/
│       ├── attention.py     # Zoom punch, colour pop, shake, slow zoom
│       ├── audio.py         # BG music, normalization, fade, voice enhance
│       ├── captions.py      # CapCut-style animated captions (highlight, typewriter, bounce, wave)
│       ├── color_grade.py   # B&W, desaturate, cinematic, vintage, neon
│       ├── filters.py       # Vignette, grain, glow, blur, LUT, glitch, neon, sharpen
│       ├── overlays.py      # Lower thirds, progress bar, watermark, CTA, countdown
│       ├── speed.py         # Slow-mo, fast-mo, reverse, freeze, boomerang, timelapse
│       ├── text_overlay.py  # Title/quote cards with animations
│       ├── transitions.py   # Fade, wipe, zoom, glitch, spin, slide, blur, whip pan
│       ├── speech_clean.py  # Filler word removal, pause cutting, stutter detection
│       ├── auto_reframe.py  # Face detection → auto 9:16 crop, portrait blur fill
│       ├── beat_sync.py     # Beat detection, beat-synced cuts, flash/zoom on beat
│       └── enhance.py       # Stabilise, denoise, upscale, deblur, skin smooth, HDR
├── config/
│   └── style_presets.yaml   # Named presets: finhub, viral, cinematic, retro, neon, bw, minimalist
├── assets/
│   └── branding/
│       ├── logo.png         # FinHub logo — use as watermark (bottom-right)
│       ├── banner.mp4       # FinHub animated banner — use as intro/outro bumper
│       └── BRANDING.md      # Branding usage instructions
├── examples/
│   └── sample_config.yaml   # Example full config
└── scripts/
    ├── install.sh           # One-shot dependency installer
    └── process.sh           # Quick process wrapper
```

---

## 🚀 Quick Start

```bash
# Install dependencies
bash scripts/install.sh

# Process with default FinHub style
python src/main.py input.mp4 output.mp4

# Use a named preset
python src/main.py input.mp4 output.mp4 --preset viral

# All options
python src/main.py input.mp4 output.mp4 \
  --preset finhub \
  --keywords "tiết kiệm,đầu tư,tài chính" \
  --title "Bí Quyết Tiết Kiệm" \
  --music assets/music/background.mp3 \
  --watermark assets/branding/logo.png \
  --no-api   # skip Claude API, use manual keywords
```

---

## 🎨 Available Effects

### Colour Grading (`color_grade.py`)
| Mode | Description |
|------|-------------|
| `desaturate` | Partially desaturated — FinHub default |
| `bw` | Full black and white |
| `cinematic` | Warm shadows, cool highlights |
| `vintage` | Faded retro look |
| `vivid` | Boosted saturation |
| `dark` | Low brightness, high contrast |

### Filters (`filters.py`)
- `apply_vignette(strength)` — dark edges
- `apply_film_grain(strength)` — film noise
- `apply_glow(intensity)` — soft bloom
- `apply_background_blur(radius)` — blur bg, keep subject sharp
- `apply_lut(lut_path)` — professional .cube LUT files
- `apply_glitch_color(intensity)` — RGB channel split
- `apply_retro_vhs()` — full VHS effect
- `apply_neon_glow(color)` — neon bloom in cyan/magenta/green/orange
- `apply_sharpen(strength)` — crisp output
- `apply_mirror(direction)` — horizontal/vertical flip

### Speed Effects (`speed.py`)
- `apply_slow_motion(factor)` — e.g. 0.5 = half speed
- `apply_fast_motion(factor)` — e.g. 2.0 = double speed
- `apply_reverse()` — play backwards
- `apply_freeze_frame(at, duration)` — hold a frame
- `apply_time_lapse(speed)` — e.g. 10x timelapse
- `apply_boomerang()` — forward + reverse loop
- `trim_clip(start, end)` — cut to a time range

### Audio (`audio.py`)
- `mix_background_music(music_path, volume)` — add BG music
- `normalize_audio(target_lufs)` — -14 LUFS for social media
- `apply_audio_fade(fade_in, fade_out)` — smooth audio edges
- `remove_background_noise()` — reduce room noise
- `apply_voice_enhance()` — EQ + compress for vocal clarity
- `change_pitch(semitones)` — pitch shift
- `add_echo(delay, decay)` — reverb/echo
- `extract_audio(format)` — save audio separately
- `replace_audio(audio_path)` — swap full audio track

### Captions (`captions.py`)
| Style | Effect |
|-------|--------|
| `highlight` | Current word highlights in colour (CapCut default) |
| `typewriter` | Letters appear one at a time |
| `bounce` | Words bounce in from above |
| `wave` | Words wave in sequentially |
| `fade` | Words fade in |
| `karaoke` | Full line shown, current word changes colour |

### Attention Effects (`attention.py`)
- `zoom_punch(timestamp, scale)` — quick push-in zoom
- `color_pop(timestamp, color)` — flash colour highlight
- `slow_zoom(start, end, scale)` — gradual creep zoom
- `camera_shake(start, end, intensity)` — handheld shake
- `caption_highlight(word, timestamp)` — bold + colour on keyword

### Transitions (`transitions.py`)
| Transition | Style |
|------------|-------|
| `fade_in_out` | Classic fade |
| `wipe_transition` | Wipe left/right/up/down |
| `zoom_transition` | Zoom punch between clips |
| `glitch_transition` | Digital glitch snap |
| `spin_transition` | Radial spin |
| `slide_transition` | Slide from any direction |
| `blur_transition` | Dreamy blur dissolve |
| `whip_pan_transition` | Ultra-fast snap cut |
| `cross_dissolve` | Smooth cross-fade |
| `concat_clips` | Simple join with no transition |

### Speech Cleaning (`speech_clean.py`)
- `clean_speech(input, output, words)` — all-in-one: detect and cut all speech issues
- `detect_issues(words)` — analyse transcript for issues (returns full report)
- `print_report(result)` — display speech cleaning report in terminal
- `save_report(result, path)` — save JSON report of all detected issues
- `add_filler_word(word, language)` — add custom filler words (supports `'vi'` and `'en'`)

**Detected issue types:**
| Type | Examples |
|------|----------|
| `filler` | "um", "uh", "ừ", "ờ", "kiểu như", "tức là" |
| `pause` | Silence gaps > 1.0s — shortened or cut |
| `stutter` | Repeated words: "I I want to..." |
| `false_start` | "I wa— I want to..." |

### Auto Reframe (`auto_reframe.py`)
- `auto_reframe_9x16(input, output, method)` — smart crop any video to 9:16
  - `method='face'` — OpenCV face detection, keeps speaker centred
  - `method='motion'` — optical flow, follows movement
  - `method='centre'` — simple centre crop (no detection)
  - `method='thirds'` — rule-of-thirds crop
- `portrait_blur_fill(input, output)` — landscape video on blurred bg (no black bars)

### Beat Sync (`beat_sync.py`)
- `detect_beats(input)` — returns BPM + beat timestamps from audio
- `cut_to_beat(clips, output, music)` — cut multiple clips timed to music beats
- `add_beat_flashes(input, output, beat_times, type)` — white/black flash or zoom on every beat
- `snap_captions_to_beats(words, beat_times)` — snap caption timing to beats
- `find_high_energy_moments(input, top_n)` — detect loudest/most energetic moments

### Enhance (`enhance.py`)
- `stabilise(input, output, smoothing)` — remove camera shake (deshake)
- `upscale(input, output, scale)` — upscale resolution (2x, 4x, lanczos/bicubic)
- `denoise_video(input, output, strength)` — reduce video noise (hqdn3d)
- `auto_correct(input, output)` — auto brightness/contrast/saturation/gamma
- `deblur(input, output, strength)` — sharpen/deblur with unsharp mask
- `smooth_skin(input, output, strength)` — soft skin smoothing (smartblur)
- `tonemap_hdr(input, output)` — convert HDR → SDR
- `deinterlace(input, output)` — remove interlacing (yadif)
- `enhance_all(input, output)` — run full enhancement pipeline in one call

### Overlays (`overlays.py`)
- `add_lower_third(title, subtitle)` — slide-in name banner
- `add_progress_bar(position, color)` — playback progress bar
- `add_watermark(image_path, position)` — logo overlay
- `add_countdown_timer(from, position)` — 5-4-3-2-1 countdown
- `add_cta_card(text)` — call-to-action card
- `add_subscribe_button(channel_name)` — subscribe button animation
- `add_timestamp()` — running time display
- `add_image_overlay(image, x, y)` — any image at any position/time

---

## 🎭 Style Presets

| Preset | Description |
|--------|-------------|
| `finhub` | FinHub brand: desaturated, bold white text, gold highlights |
| `viral` | High-energy: vivid colours, bounce captions, whip-pan cuts |
| `cinematic` | Movie-grade: letterbox, muted tones, typewriter captions |
| `retro` | VHS vintage: grain, scan lines, faded colours |
| `neon` | Night-club: dark, glowing cyan/magenta |
| `minimalist` | Clean & calm: white, black text, subtle fade |
| `blackwhite` | Pure B&W high contrast |

---

## ⚙️ Common Edits

**"Add background music"**
```python
from src.effects.audio import mix_background_music
mix_background_music("input.mp4", "output.mp4", "music.mp3", music_volume=0.12)
```

**"Add FinHub logo watermark"**
```python
from src.effects.overlays import add_watermark
add_watermark("input.mp4", "output.mp4", "assets/branding/logo.png", position="bottom-right")
```

**"Make it slow-mo"**
```python
from src.effects.speed import apply_slow_motion
apply_slow_motion("input.mp4", "output.mp4", factor=0.5)
```

**"Add a progress bar"**
```python
from src.effects.overlays import add_progress_bar
add_progress_bar("input.mp4", "output.mp4", position="bottom", color="0xFF0000")
```

**"Make it B&W with vignette"**
```python
from src.effects.color_grade import apply_color_grade
from src.effects.filters import apply_vignette
apply_color_grade("input.mp4", "tmp.mp4", mode="bw")
apply_vignette("tmp.mp4", "output.mp4", strength=0.5)
```

**"Add a glitch effect"**
```python
from src.effects.filters import apply_glitch_color
apply_glitch_color("input.mp4", "output.mp4", intensity=0.6)
```

**"Remove um/uh filler words and long pauses"**
```python
from src.transcribe import transcribe
from src.effects.speech_clean import clean_speech

words = transcribe("input.mp4")["words"]
clean_speech("input.mp4", "output.mp4", words,
             mode="cut",                  # 'cut' removes, 'mute' silences
             pause_threshold=1.0,         # flag pauses > 1s
             long_pause_threshold=2.0)    # cut pauses > 2s
```

**"Auto-reframe landscape video to 9:16 vertical"**
```python
from src.effects.auto_reframe import auto_reframe_9x16
auto_reframe_9x16("landscape.mp4", "vertical.mp4", method="face")
# or for no black bars:
from src.effects.auto_reframe import portrait_blur_fill
portrait_blur_fill("landscape.mp4", "vertical.mp4")
```

**"Sync cuts to music beat"**
```python
from src.effects.beat_sync import detect_beats, add_beat_flashes
beats = detect_beats("input.mp4")
add_beat_flashes("input.mp4", "output.mp4",
                 beat_times=beats["beat_times"],
                 flash_type="zoom",     # 'white', 'black', or 'zoom'
                 on_every=2)            # every other beat
```

**"Stabilise shaky footage + denoise + sharpen"**
```python
from src.effects.enhance import enhance_all
enhance_all("shaky.mp4", "clean.mp4",
            stabilise_video=True,
            denoise=True,
            sharpen=True)
```

---

## 🔑 API Keys

Only needed if using auto keyword detection via Claude AI:
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

To skip (use manual keywords instead):
```bash
python src/main.py input.mp4 output.mp4 --keywords "từ khóa,quan trọng" --no-api
```

---

## 📐 Output Specs (Social Media)

| Platform | Format | Resolution | FPS |
|----------|--------|------------|-----|
| Facebook Reels | 9:16 vertical | 1080×1920 | 30 |
| Instagram Reels | 9:16 vertical | 1080×1920 | 30 |
| TikTok | 9:16 vertical | 1080×1920 | 30 |
| YouTube Shorts | 9:16 vertical | 1080×1920 | 30 |

All presets output at 1080×1920 by default.

---

## 🏷 Branding

- **Logo**: `assets/branding/logo.png` — always watermark bottom-right at 12% width
- **Banner**: `assets/branding/banner.mp4` — use as intro bumper (first 2–3s) and/or outro
- See `assets/branding/BRANDING.md` for full branding guidelines
