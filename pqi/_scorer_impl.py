# Prompt Quality Index (PQI) v0.2
# Author: Franky Schaut
# Repository: https://github.com/FrankySchaut/PQI
# License: MIT — Privacy-first, local execution

from __future__ import annotations

import os
import re
from typing import Any

import numpy as np
import textstat

from .config import BIAS_ABSOLUTES, DEFAULT_WEIGHTS, REFLECTION_MARKERS, STRUCTURE_CUES

# --------- NLTK helpers (lazy, resilient) ------------------------------------

# Minimal fallback stopwords if NLTK's corpus isn't available
_FALLBACK_STOPWORDS = {
    "the",
    "and",
    "is",
    "are",
    "was",
    "were",
    "be",
    "to",
    "of",
    "in",
    "a",
    "an",
    "it",
    "that",
    "this",
    "for",
    "on",
    "with",
    "as",
    "by",
    "at",
    "from",
    "or",
    "but",
    "not",
    "into",
    "about",
    "over",
    "after",
    "before",
    "between",
    "out",
    "up",
    "down",
    "off",
    "so",
    "than",
    "too",
    "very",
}

_SIA: Any | None = None  # cached SentimentIntensityAnalyzer or None
_STOP_WORDS: set[str] | None = None  # cached set of stopwords


def _ensure_nltk() -> Any | None:
    """
    Try to import nltk. Return the module (typed as Any) or None if unavailable.
    Using Any avoids mypy attr errors when calling nltk APIs.
    """
    try:
        import nltk  # type: ignore

        return nltk  # type: Any
    except Exception:
        return None


def _ensure_nltk_resource(nltk_mod: Any, resource: str) -> bool:
    """
    Ensure an NLTK resource exists; try to find, otherwise quietly download.
    Returns True if available, False if not.
    """
    try:
        nltk_mod.data.find(resource)
        return True
    except Exception:
        try:
            # resource like "tokenizers/punkt_tab/english" -> last part "english"
            nltk_mod.download(resource.split("/")[-1], quiet=True)
            nltk_mod.data.find(resource)
            return True
        except Exception:
            return False


def _word_tokenize_safe(text: str) -> list[str]:
    """
    Try NLTK word_tokenize; if resources are missing or NLTK isn't installed,
    fall back to a simple regex tokenizer. You can force the fallback with
    PQI_USE_SIMPLE_TOKENIZER=1.
    """
    if os.getenv("PQI_USE_SIMPLE_TOKENIZER") == "1":
        return re.findall(r"\b\w+(?:'\w+)?\b", text.lower())

    nltk_mod = _ensure_nltk()
    if nltk_mod is not None:
        # Newer NLTK uses punkt_tab; older uses punkt. Try both.
        have_tab = _ensure_nltk_resource(nltk_mod, "tokenizers/punkt_tab/english")
        have_punkt = have_tab or _ensure_nltk_resource(nltk_mod, "tokenizers/punkt")
        if have_tab or have_punkt:
            try:
                return nltk_mod.word_tokenize(text)
            except Exception:
                pass

    # Regex fallback (good enough for scoring)
    return re.findall(r"\b\w+(?:'\w+)?\b", text.lower())


def _get_stop_words() -> set[str]:
    global _STOP_WORDS
    if _STOP_WORDS is not None:
        return _STOP_WORDS

    nltk_mod = _ensure_nltk()
    if nltk_mod is not None:
        # Ensure stopwords resource
        have_sw = _ensure_nltk_resource(nltk_mod, "corpora/stopwords")
        if have_sw:
            try:
                _STOP_WORDS = set(nltk_mod.corpus.stopwords.words("english"))
                return _STOP_WORDS
            except Exception:
                pass

    _STOP_WORDS = set(_FALLBACK_STOPWORDS)
    return _STOP_WORDS


def _get_sia() -> Any:
    """
    Lazy-init SentimentIntensityAnalyzer. Return a shim if unavailable.
    Returns Any to avoid mypy attr errors.
    """
    global _SIA
    if _SIA is not None:
        return _SIA

    nltk_mod = _ensure_nltk()
    if nltk_mod is not None:
        # Ensure VADER lexicon
        have_vader = _ensure_nltk_resource(nltk_mod, "sentiment/vader_lexicon")
        if have_vader:
            try:
                from nltk.sentiment import SentimentIntensityAnalyzer  # type: ignore

                _SIA = SentimentIntensityAnalyzer()
                return _SIA
            except Exception:
                pass

    # Fallback shim: always neutral
    class _NeutralSIA:
        def polarity_scores(self, _: str) -> dict[str, float]:
            return {"neg": 0.0, "neu": 1.0, "pos": 0.0, "compound": 0.0}

    _SIA = _NeutralSIA()
    return _SIA


# --------- Core scoring utilities --------------------------------------------


def _tokenize(text: str) -> tuple[list[str], list[str]]:
    words = _word_tokenize_safe(text)
    stop = _get_stop_words()
    content = [w.lower() for w in words if w.isalpha() and w.lower() not in stop]
    return words, content


def _clarity(prompt: str) -> float:
    fre = textstat.flesch_reading_ease(prompt)
    return float(np.clip((fre - 30) * (100 / 60), 0, 100))


def _context(content_words: list[str]) -> float:
    return float(np.clip(len(content_words) * 5, 0, 100))


def _completeness(prompt: str) -> float:
    q_starters = (
        "what",
        "how",
        "why",
        "when",
        "where",
        "who",
        "explain",
        "describe",
        "analyze",
        "compare",
        "analyse",
    )
    has_q = any(prompt.lower().strip().startswith(q) for q in q_starters) or ("?" in prompt)
    has_struct = bool(re.search(STRUCTURE_CUES, prompt, re.I))
    score = 40 + (35 if has_q else 0) + (25 if has_struct else 0)
    return float(min(100, score))


def _proportion(words: list[str], content_words: list[str]) -> float:
    if not words:
        return 0.0
    density = len(content_words) / max(1, len(words))
    dens_penalty = abs(density - 0.625) * 120
    length_penalty = max(0, (len(words) - 120) * 0.25)
    return float(np.clip(100 - dens_penalty - length_penalty, 0, 100))


def _fairness(prompt: str) -> float:
    sia = _get_sia()
    vs = sia.polarity_scores(prompt)
    neutrality = 1.0 - min(1.0, vs.get("pos", 0.0) + vs.get("neg", 0.0))
    base = 100 * neutrality
    bias_hits = sum(1 for k in BIAS_ABSOLUTES if k in prompt.lower())
    return float(np.clip(base - 8 * bias_hits, 0, 100))


def _reflection(prompt: str) -> float:
    count = sum(1 for m in REFLECTION_MARKERS if m in prompt.lower())
    return float(min(100, count * 20))


# --------- Public API ---------------------------------------------------------


def score_prompt(prompt: str, weights: dict[str, float] | None = None) -> dict:
    p = prompt.strip()
    if not p:
        return {"score": 0, "breakdown": {}, "feedback": "Empty prompt. Begin with intention."}

    words, content = _tokenize(p)
    breakdown = {
        "clarity": round(_clarity(p), 1),
        "context": round(_context(content), 1),
        "completeness": round(_completeness(p), 1),
        "proportion": round(_proportion(words, content), 1),
        "fairness": round(_fairness(p), 1),
        "reflection": round(_reflection(p), 1),
    }

    w = weights or DEFAULT_WEIGHTS
    pqi = round(sum(breakdown[k] * w[k] for k in breakdown), 1)

    weak = [k for k, v in breakdown.items() if v < 60]
    if pqi >= 85:
        fb = f"PQI = {pqi}. Transcendent. You ask with proportion and care."
    elif pqi >= 70:
        fb = f"PQI = {pqi}. Strong. Polish {', '.join(weak) or 'reflection'} for depth."
    else:
        fb = f"PQI = {pqi}. Refine {', '.join(weak)}. Ask with clearer intention."

    return {
        "score": int(pqi),
        "breakdown": breakdown,
        "feedback": fb,
        "radar_data": list(breakdown.values()),
    }
