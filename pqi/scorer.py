# Thin, typed wrapper for PQI scorer to keep mypy happy and runtime unchanged.

from __future__ import annotations

from typing import TypedDict

# Import the real implementation (lives in _scorer_impl.py)
from ._scorer_impl import score_prompt as _score_prompt_impl  # type: ignore[import-not-found]


class Breakdown(TypedDict):
    clarity: float
    context: float
    completeness: float
    proportion: float
    fairness: float
    reflection: float


class ScoreResult(TypedDict):
    score: int
    breakdown: Breakdown
    feedback: str
    radar_data: list[float]


def score_prompt(prompt: str, weights: dict[str, float] | None = None) -> ScoreResult:
    return _score_prompt_impl(prompt, weights)  # type: ignore[no-any-return]
