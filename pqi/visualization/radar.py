from importlib import import_module


def plot_relevance_radar(*args, **kwargs):
    for mod in ("pqi.radar", "pqi.legacy.radar"):
        try:
            m = import_module(mod)
            if hasattr(m, "plot_relevance_radar"):
                return getattr(m, "plot_relevance_radar")(*args, **kwargs)
        except Exception:
            continue
    raise RuntimeError(
        "No radar implementation found. Ensure pqi/radar.py or pqi/legacy/radar.py exists."
    )
