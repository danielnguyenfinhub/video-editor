"""
Content Analysis — main message + keyword extraction.

Workflow:
  1. Build a plain-text transcript from word tokens.
  2. Send to Claude with a structured JSON prompt.
  3. Parse the response into typed dataclasses.
  4. Map each keyword back to its timestamp from the word tokens.

Output is consumed by:
  - pipeline.py  (orchestrator)
  - effects/attention.py  (zoom, flash, shake)
  - effects/captions.py   (keyword accent colour)
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field


# ── Data types ───────────────────────────────────────────────────────────────

@dataclass
class WordToken:
    word:  str
    start: float
    end:   float


@dataclass
class Keyword:
    phrase:  str
    start:   float   # timestamp of first occurrence
    end:     float
    impact:  str     # "high" | "medium"
    reason:  str


@dataclass
class KeyMoment:
    start:     float
    end:       float
    effect:    str   # "zoom_punch" | "color_flash" | "slow_zoom" | "shake" | "caption_highlight"
    intensity: float # 0.0 – 1.0


@dataclass
class AnalysisResult:
    main_message: str
    keywords:     list[Keyword]    = field(default_factory=list)
    key_moments:  list[KeyMoment]  = field(default_factory=list)


# ── Main entry point ──────────────────────────────────────────────────

def analyze(
    word_tokens: list[WordToken],
    model: str = "claude-3-5-haiku-20241022",
    max_keywords: int = 8,
    language_hint: str | None = None,
    verbose: bool = False,
) -> AnalysisResult:
    """
    Analyse word_tokens and return an AnalysisResult.

    Requires ANTHROPIC_API_KEY to be set.
    """
    import anthropic

    transcript = _build_transcript(word_tokens)

    lang_note = f"\nThe content is in {language_hint}." if language_hint else ""
    prompt = f"""You are a social media video editor specialising in short-form finance content.{lang_note}

Analyse the transcript below and return a JSON object with EXACTLY this shape:

{{
  "main_message": "<one sentence summarising the core idea viewers should remember>",
  "keywords": [
    {{
      "phrase": "<exact phrase from transcript>",
      "impact": "high" | "medium",
      "reason": "<why this phrase deserves visual emphasis>"
    }}
  ],
  "key_moments": [
    {{
      "start_word": "<first word of the moment>",
      "end_word":   "<last word of the moment>",
      "effect":     "zoom_punch" | "color_flash" | "slow_zoom" | "shake" | "caption_highlight",
      "intensity":  0.0 to 1.0
    }}
  ]
}}

Rules:
- Return at most {max_keywords} keywords. Prefer short punchy phrases (1-3 words).
- Mark a phrase "high" impact only if it is the single most important hook or number.
- key_moments should reference the most emotionally or informationally impactful segments.
- Use "zoom_punch" for single high-impact words/numbers.
- Use "color_flash" for the single most dramatic reveal.
- Use "slow_zoom" for reflective insight moments.
- Use "shake" only for urgent warnings (use sparingly).
- Use "caption_highlight" for important but visually subtle moments.
- Return ONLY valid JSON. No markdown, no explanation.

TRANSCRIPT:
{transcript}
"""

    if verbose:
        print(f"  [analyze] Sending {len(word_tokens)} words to Claude …")

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    if verbose:
        print(f"  [analyze] Response: {raw[:200]} …")

    data = json.loads(raw)
    return _parse(data, word_tokens)


# ── Helpers ───────────────────────────────────────────────────────────────

def _build_transcript(tokens: list[WordToken]) -> str:
    return " ".join(t.word for t in tokens)


def _parse(data: dict, word_tokens: list[WordToken]) -> AnalysisResult:
    keywords: list[Keyword] = []
    for kw in data.get("keywords", []):
        phrase = kw.get("phrase", "").strip()
        start, end = _find_phrase_timestamps(phrase, word_tokens)
        keywords.append(Keyword(
            phrase=phrase,
            start=start,
            end=end,
            impact=kw.get("impact", "medium"),
            reason=kw.get("reason", ""),
        ))

    key_moments: list[KeyMoment] = []
    for km in data.get("key_moments", []):
        start_word = km.get("start_word", "")
        end_word   = km.get("end_word",   start_word)
        start = _find_word_start(start_word, word_tokens)
        end   = _find_word_end(end_word, word_tokens, default=start + 1.0)
        key_moments.append(KeyMoment(
            start=start,
            end=end,
            effect=km.get("effect", "zoom_punch"),
            intensity=float(km.get("intensity", 0.7)),
        ))

    return AnalysisResult(
        main_message=data.get("main_message", ""),
        keywords=keywords,
        key_moments=key_moments,
    )


def _find_phrase_timestamps(
    phrase: str,
    tokens: list[WordToken],
) -> tuple[float, float]:
    """Return (start, end) of the first occurrence of *phrase* in *tokens*."""
    words = phrase.lower().split()
    if not words:
        return 0.0, 0.0

    for i in range(len(tokens) - len(words) + 1):
        window = [t.word.lower().strip(".,!?:;\"'") for t in tokens[i:i + len(words)]]
        if window == words:
            return tokens[i].start, tokens[i + len(words) - 1].end

    # Fuzzy fallback — find best single token
    for t in tokens:
        if words[0] in t.word.lower():
            return t.start, t.end

    return 0.0, 0.0


def _find_word_start(word: str, tokens: list[WordToken]) -> float:
    word_lower = word.lower().strip(".,!?")
    for t in tokens:
        if word_lower in t.word.lower():
            return t.start
    return 0.0


def _find_word_end(word: str, tokens: list[WordToken], default: float = 1.0) -> float:
    word_lower = word.lower().strip(".,!?")
    for t in reversed(tokens):
        if word_lower in t.word.lower():
            return t.end
    return default
