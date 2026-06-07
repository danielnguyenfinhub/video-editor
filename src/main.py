#!/usr/bin/env python3
"""
Video Editor CLI

Usage:
  python src/main.py input.mp4 output.mp4
  python src/main.py input.mp4 output.mp4 --config examples/sample_config.yaml
  python src/main.py input.mp4 output.mp4 --no-analysis
  python src/main.py input.mp4 output.mp4 --preset bw
"""
from __future__ import annotations

import argparse
import sys
import os
from pathlib import Path

import yaml

# ── Resolve project root ──────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))


def load_config(preset_path: Path, override_path: str | None) -> dict:
    with open(preset_path) as f:
        config = yaml.safe_load(f) or {}

    if override_path:
        with open(override_path) as f:
            overrides = yaml.safe_load(f) or {}
        _deep_merge(config, overrides)

    return config


def _deep_merge(base: dict, override: dict) -> None:
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


def main() -> None:
    parser = argparse.ArgumentParser(description="AI-powered social media video editor")
    parser.add_argument("input",  help="Input video file")
    parser.add_argument("output", help="Output video file")
    parser.add_argument("--config",      default=None, help="Per-video YAML config override")
    parser.add_argument("--preset",      default=None, choices=["desaturate", "cinematic", "bw"], help="Color grade preset shortcut")
    parser.add_argument("--no-analysis", action="store_true", help="Skip AI content analysis (faster)")
    parser.add_argument("--no-captions", action="store_true", help="Skip caption rendering")
    parser.add_argument("--verbose",     action="store_true", default=True)
    args = parser.parse_args()

    preset_path = ROOT / "config" / "style_presets.yaml"
    config = load_config(preset_path, args.config)

    if args.preset:
        config["color_grade"] = args.preset
    if args.no_analysis:
        config.setdefault("analysis", {})["enabled"] = False
    if args.no_captions:
        config.setdefault("captions", {})["enabled"] = False

    if config.get("analysis", {}).get("enabled", True):
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("⚠️  ANTHROPIC_API_KEY not set — disabling content analysis.")
            print("   Set the env var to enable keyword detection and attention effects.")
            config["analysis"]["enabled"] = False

    from pipeline import run
    run(
        input_path=args.input,
        output_path=args.output,
        config=config,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
