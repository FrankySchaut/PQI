# Prompt Quality Index (PQI) v0.2
# Author: Franky Schaut
# Repository: https://github.com/FrankySchaut/PQI
# License: MIT — Privacy-first, local execution

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from pqi.redactor import redact
from pqi.scorer import score_prompt

st.set_page_config(page_title="PQI v0.2", layout="centered")
st.title("Prompt Quality Index (PQI) v0.2")
st.caption("Privacy-first. Local. Meaningful.")

txt = st.text_area(
    "Enter your prompt",
    height=150,
    placeholder="I wonder: what if every question shaped the soul of the answer?",
)
do_redact = st.checkbox("Redact emails, phones, IDs, URLs (GDPR-safe)", value=True)

if st.button("Measure Meaning"):
    p = redact(txt) if do_redact else txt
    res = score_prompt(p)
    st.json(res, expanded=False)

    # Radar Chart
    dims = list(res["breakdown"].keys())
    vals = list(res["breakdown"].values()) + [list(res["breakdown"].values())[0]]
    angles = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, vals, "o-", linewidth=2)
    ax.fill(angles, vals, alpha=0.15)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dims, fontsize=10)
    ax.set_ylim(0, 100)
    ax.set_yticklabels([])
    ax.grid(True)
    st.pyplot(fig)
