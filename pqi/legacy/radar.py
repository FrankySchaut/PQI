# pqi/legacy/radar.py
"""
Minimal PQI radar (S,G,C) for compatibility.
Uses matplotlib if available; otherwise explains how to install it.
"""

from pathlib import Path


def plot_relevance_radar(vec, title="PQI Radar", save_path=None, show=False):
    try:
        import math

        import matplotlib.pyplot as plt
    except Exception as e:
        msg = (
            "Radar plot requires matplotlib. Install with:\n"
            "    python -m pip install matplotlib\n"
            f"(Import error: {e})"
        )
        print(msg)
        return msg

    # Extract and clamp S,G,C
    s = max(0.0, min(1.0, float(vec.get("salience", 0.0))))
    g = max(0.0, min(1.0, float(vec.get("grip", 0.0))))
    c = max(0.0, min(1.0, float(vec.get("coherence", 0.0))))

    labels = ["Salience", "Grip", "Coherence"]
    values = [s, g, c]
    angles = [n / float(len(labels)) * 2 * math.pi for n in range(len(labels))]
    angles += angles[:1]
    values += values[:1]

    fig = plt.figure()
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids([a * 180 / math.pi for a in angles[:-1]], labels)
    ax.set_rlabel_position(0)
    ax.set_ylim(0, 1)

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.15)
    ax.set_title(title, va="bottom")

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)
    return {"saved": bool(save_path), "path": save_path}
