# Prompt Quality Index (PQI) v0.2
# Author: Franky Schaut
# Repository: https://github.com/FrankySchaut/PQI
# License: MIT — Privacy-first, local execution


DEFAULT_WEIGHTS: dict[str, float] = {
    "clarity": 0.25,
    "context": 0.15,
    "completeness": 0.15,
    "proportion": 0.15,
    "fairness": 0.15,
    "reflection": 0.15,
}

REFLECTION_MARKERS = [
    "wonder",
    "curious",
    "what if",
    "imagine",
    "reflect",
    "question",
    "doubt",
    "perhaps",
    "maybe",
    "consider",
    "why",
    "how might",
]

BIAS_ABSOLUTES = ["always", "never", "everyone", "nobody", "must", "only", "obviously"]

STRUCTURE_CUES = r"\b(and|but|because|so|then|if|while|therefore|however|although|meanwhile)\b"
