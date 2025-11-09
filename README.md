# PQI v0.2 — Prompt Quality Index
**Measure meaning. Design intention. Build better dialogue.**  
A **privacy-first**, **local**, **modular** tool to score human–AI prompts across six dimensions:

- Clarity • Context • Completeness • Proportion • Fairness • Reflection

> **Note for Readers of the Original PQI Paper**  
> All functionality described in the initial white paper remains fully operational and reproducible.  
> Version **v0.2.1 – The Architecture of Limitation in Code** extends the original implementation with:
> - An auditable test chain (`tools/audit_*`, `docs/audits/`)
> - CI and logging enhancements for reproducible research
> - The restored **legacy radar visualization** for comparative analysis  
> These additions do **not** alter the mathematical core or scoring logic of PQI; they add transparency, version tracking, and usability improvements.

---

### 🧭 Quick Start for Paper Readers
To reproduce the demonstrations from the original PQI paper:

```bash
# clone repository
git clone https://github.com/FrankySchaut/PQI
cd PQI

# install dependencies
python -m pip install -r requirements.txt

# run baseline tests
python -m pytest -q

# optional: generate radar visualization
python -m pqi.legacy.radar
