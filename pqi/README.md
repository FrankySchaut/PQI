# PQI v0.2 — Prompt Quality Index
**Measure meaning. Design intention. Build better dialogue.**  
A **privacy-first**, **local**, **modular** tool to score human–AI prompts across six dimensions:

- Clarity • Context • Completeness • Proportion • Fairness • Reflection

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](https://www.python.org/)
[![Privacy](https://img.shields.io/badge/privacy-GDPR--Safe%20%7C%20Local-orange.svg)](#privacy--gdpr)
[![Built from Dialogue](https://img.shields.io/badge/origin-Solace%20%26%20Grok-lightgrey.svg)](#)

## Why PQI?
PQI reframes “prompt engineering” as **ethics of articulation**. It evaluates the *form* of a prompt (not identity/content ownership) and returns a composite 0–100 score with diagnostic feedback. Runs locally, no logging, PII redacted by default.

---

## Install

```bash
git clone https://github.com/FrankySchaut/PQI
cd PQI
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"
```

## CLI

```bash
python cli.py -p "How might we redesign hiring prompts to reduce bias while preserving intent?"
```

**Stdin supported:**
```bash
echo "I wonder: what if every prompt shaped shared cognition?" | python cli.py
```

**Skip redaction (not recommended):**
```bash
python cli.py -p "Email me at jane@acme.com" --no-redact
```

## Streamlit Demo (optional)

```bash
streamlit run app.py
```

You’ll get:
- JSON breakdown of the six dimensions
- A radar chart visualising scores (0–100)

---

## How It Works (v0.2)
- **Clarity**: Flesch Reading Ease → 0–100 (clipped)  
- **Context**: content-word count → 0–100  
- **Completeness**: question cues + connective structure → 40–100  
- **Proportion**: density sweet spot (~0.625) + length guard (>120 tokens penalised)  
- **Fairness**: VADER neutrality + penalties for absolutist terms  
- **Reflection**: presence of reflective markers (“wonder”, “consider”, “what if”, etc.)

Weights are in `pqi/config.py`.

---

## Privacy & GDPR
- **Local** analysis only.  
- **No logging**; no network calls required.  
- **PII redaction by default** (emails, phones, IDs, URLs).  
- PQI evaluates **form** (linguistic structure), not identity.  
- If you deploy the Streamlit app to the web, **your hosting** must meet your org’s privacy policy.

---

## Configuration (optional)
- Tune weights or markers in `pqi/config.py`.
- (Advanced) You can pass custom weights in code via `score_prompt(prompt, weights={...})`.

---

## Limitations
- **Language**: v0.2 is calibrated for English. Multilingual support would require language detection and per-language analyzers.  
- **Short prompts**: very short prompts can yield extreme clarity; use judgment or add a minimum-length policy in your workflow.  
- **Determinism**: VADER-based fairness is deterministic; results are reproducible.

---

## Dev & Tests

```bash
pytest -q
```

---

## License
MIT © 2025 François Schaut


---

## Release Notes — v0.2 (November 2025)
**Title:** The Architecture of Limitation in Code  
**Author:** Franky Schaut  
**Repository:** [https://github.com/FrankySchaut/PQI](https://github.com/FrankySchaut/PQI)  

### Highlights:
- Full refactor from v0.1 → modular package structure (`pqi/`)
- GDPR-safe PII redaction layer (emails, phones, URLs, IDs)
- Configurable weights + calibration deck
- Streamlit visualization app (local use)
- Deterministic scoring model (no API dependency)
- Tested with pytest; 100% local; zero data retention

> “A question is not harmless—it architects cognition.” — *Franky Schaut, 2025*
