# Prompt Quality Index (PQI) v0.2
# Author: Franky Schaut
# Repository: https://github.com/FrankySchaut/PQI
# License: MIT — Privacy-first, local execution

import re
import numpy as np
import nltk
import textstat
from typing import Dict, Optional, List
from .config import DEFAULT_WEIGHTS, REFLECTION_MARKERS, BIAS_ABSOLUTES, STRUCTURE_CUES
from nltk.sentiment import SentimentIntensityAnalyzer

# One-time safe downloads
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('vader_lexicon', quiet=True)

SIA = SentimentIntensityAnalyzer()
STOP_WORDS = set(nltk.corpus.stopwords.words("english"))

def _tokenize(text: str) -> tuple[List[str], List[str]]:
    words = nltk.word_tokenize(text)
    content = [w.lower() for w in words if w.isalpha() and w.lower() not in STOP_WORDS]
    return words, content

def _clarity(prompt: str) -> float:
    fre = textstat.flesch_reading_ease(prompt)
    return float(np.clip((fre - 30) * (100 / 60), 0, 100))

def _context(content_words: List[str]) -> float:
    return float(np.clip(len(content_words) * 5, 0, 100))

def _completeness(prompt: str) -> float:
    q_starters = ('what','how','why','when','where','who','explain','describe','analyze','compare','analyse')
    has_q = any(prompt.lower().strip().startswith(q) for q in q_starters) or ("?" in prompt)
    has_struct = bool(re.search(STRUCTURE_CUES, prompt, re.I))
    score = 40 + (35 if has_q else 0) + (25 if has_struct else 0)
    return float(min(100, score))

def _proportion(words: List[str], content_words: List[str]) -> float:
    if not words:
        return 0.0
    density = len(content_words) / max(1, len(words))
    dens_penalty = abs(density - 0.625) * 120
    length_penalty = max(0, (len(words) - 120) * 0.25)
    return float(np.clip(100 - dens_penalty - length_penalty, 0, 100))

def _fairness(prompt: str) -> float:
    vs = SIA.polarity_scores(prompt)
    neutrality = 1.0 - min(1.0, vs["pos"] + vs["neg"])
    base = 100 * neutrality
    bias_hits = sum(1 for k in BIAS_ABSOLUTES if k in prompt.lower())
    return float(np.clip(base - 8 * bias_hits, 0, 100))

def _reflection(prompt: str) -> float:
    count = sum(1 for m in REFLECTION_MARKERS if m in prompt.lower())
    return float(min(100, count * 20))

def score_prompt(prompt: str, weights: Optional[Dict[str, float]] = None) -> Dict:
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
        "radar_data": list(breakdown.values())
    }
