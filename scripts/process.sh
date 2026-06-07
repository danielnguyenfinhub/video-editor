#!/usr/bin/env bash
# Quick wrapper: process.sh <input.mp4> [output.mp4] [config.yaml]
set -e
INPUT="${1:?Usage: process.sh <input.mp4> [output.mp4] [config.yaml]}"
OUTPUT="${2:-output/$(basename "$INPUT" .mp4)_edited.mp4}"
CONFIG="${3:-}"

source .venv/bin/activate 2>/dev/null || true

if [ -n "$CONFIG" ]; then
  python src/main.py "$INPUT" "$OUTPUT" --config "$CONFIG"
else
  python src/main.py "$INPUT" "$OUTPUT"
fi
