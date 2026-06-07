#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
#  Install script for video-editor
# ─────────────────────────────────────────────────────────────────────────────
set -e

echo "📦 Creating virtual environment …"
python3 -m venv .venv
source .venv/bin/activate

echo "📦 Installing Python dependencies …"
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Creating directories …"
mkdir -p fonts input output

echo ""
echo "🎨 Downloading fonts …"
MONTSERRAT_URL="https://github.com/google/fonts/raw/main/ofl/montserrat/static/Montserrat-Bold.ttf"
NOTO_URL="https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Bold.ttf"

curl -sL "$MONTSERRAT_URL" -o fonts/Montserrat-Bold.ttf && echo "  ✅ Montserrat-Bold" || echo "  ⚠️  Montserrat download failed"
curl -sL "$NOTO_URL"       -o fonts/NotoSans-Bold.ttf   && echo "  ✅ NotoSans-Bold"   || echo "  ⚠️  NotoSans download failed"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Set your API key:  export ANTHROPIC_API_KEY=sk-ant-..."
echo "  2. Activate venv:     source .venv/bin/activate"
echo "  3. Run:               python src/main.py input/video.mp4 output/result.mp4"
