"""
Audio transcription using faster-whisper.
Returns word-level timestamps for caption and analysis use.
"""
from __future__ import annotations

from typing import Any


def transcribe(
    video_path: str,
    model: str = "base",
    language: str | None = None,
) -> list[dict[str, Any]]:
    """
    Transcribe the audio from *video_path* using faster-whisper.

    Returns a list of segment dicts:
        [
          {
            "text": "...",
            "start": 0.0,
            "end":   2.4,
            "words": [
              {"word": "Hello", "start": 0.0, "end": 0.4},
              ...
            ]
          },
          ...
        ]
    """
    from faster_whisper import WhisperModel

    print(f"  [transcribe] Loading Whisper model '{model}' …")
    wm = WhisperModel(model, device="cpu", compute_type="int8")

    segments_raw, info = wm.transcribe(
        video_path,
        language=language,
        word_timestamps=True,
        vad_filter=True,
    )
    print(f"  [transcribe] Detected language: {info.language} ({info.language_probability:.0%})")

    segments = []
    for seg in segments_raw:
        words = []
        for w in (seg.words or []):
            words.append({
                "word":  w.word,
                "start": round(w.start, 3),
                "end":   round(w.end,   3),
            })
        segments.append({
            "text":  seg.text.strip(),
            "start": round(seg.start, 3),
            "end":   round(seg.end,   3),
            "words": words,
        })

    return segments
