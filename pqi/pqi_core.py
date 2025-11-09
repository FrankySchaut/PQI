from dataclasses import dataclass
from typing import Callable, Dict, Any

@dataclass(frozen=True)
class PQIWeights:
    alpha: float = 0.3  # salience
    beta: float = 0.4   # grip
    gamma: float = 0.3  # coherence

    def normalized(self) -> "PQIWeights":
        s = self.alpha + self.beta + self.gamma
        if s == 0:
            raise ValueError("Sum of weights cannot be zero.")
        return PQIWeights(self.alpha/s, self.beta/s, self.gamma/s)

    def validate(self, tol: float = 1e-9) -> None:
        s = self.alpha + self.beta + self.gamma
        if abs(s - 1.0) > tol:
            raise ValueError(f"Weights must sum to 1 (got {s}).")

class PQI:
    """Predictive Quality Index (PQI):
    PQI(x) = α*S(x) + β*G(x) + γ*C(x), α+β+γ=1
    where S=salience, G=grip, C=coherence in [0,1].
    """
    def __init__(
        self,
        weights: PQIWeights = PQIWeights(),
        salience_model: Callable[[Any], float] | None = None,
        grip_model: Callable[[Any], float] | None = None,
        coherence_model: Callable[[Any], float] | None = None,
        waffle_threshold: float = 0.6,
    ):
        self.weights = weights.normalized()
        self.weights.validate()
        self.salience_model = salience_model or (lambda x: float(x.get("salience", 0.0)))
        self.grip_model = grip_model or (lambda x: float(x.get("grip", 0.0)))
        self.coherence_model = coherence_model or (lambda x: float(x.get("coherence", 0.0)))
        self.waffle_threshold = waffle_threshold

    def relevance_vector(self, x: Dict[str, Any]) -> Dict[str, float]:
        return {
            "salience": self.salience_model(x),
            "grip": self.grip_model(x),
            "coherence": self.coherence_model(x),
        }

    def score(self, x: Dict[str, Any]) -> float:
        vec = self.relevance_vector(x)
        a, b, c = self.weights.alpha, self.weights.beta, self.weights.gamma
        s = max(0.0, min(1.0, vec["salience"]))
        g = max(0.0, min(1.0, vec["grip"]))
        co = max(0.0, min(1.0, vec["coherence"]))
        return a * s + b * g + c * co

    def relevance_audit(self, x: Dict[str, Any]) -> Dict[str, Any]:
        pqi = self.score(x)
        verdict = "NOT_WAFFLE" if pqi >= self.waffle_threshold else "WAFFLE"
        return {"pqi": pqi, "verdict": verdict}

    def emily_filter(self, x: Dict[str, Any]) -> str:
        return self.relevance_audit(x)["verdict"]
