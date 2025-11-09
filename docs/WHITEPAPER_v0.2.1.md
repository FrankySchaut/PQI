# PQI: From Vervaeke to Vector — The Architecture of Limitation in Code
### Version 0.2.1 – November 2025

## Abstract
The **Predictive Quality Index (PQI)** remains a framework for measuring relevance, proportionality, and ethical salience in AI output — derived from John Vervaeke’s *relevance realization* theory.  
Version 0.2.1 expands the original PQI prototype into an **auditable, reproducible research artifact**. The core algorithm is unchanged; what has evolved is the *architecture of verification*: every function, test, and audit log now exists as a lived enactment of limitation — the principle that integrity in cognition and code arises not from expansion but from proportion.

---

## 1. From Proof of Concept to Lived Architecture
### Then (v0.1 – The Concept)
The first PQI paper established:
- **Theoretical mapping** between Vervaeke’s triad *(Salience, Grip, Coherence)* and a quantifiable PQI vector.  
- **Mathematical expression**  
  \[ PQI(x) = \alpha S(x) + \beta G(x) + \gamma C(x), \quad \alpha + \beta + \gamma = 1 \]
- **Initial implementation** as a lightweight function for evaluating prompt quality.  
- **Philosophical context:** how “relevance realization” can re-ground AI evaluation in lived, embodied cognition rather than policy abstraction.

However, the early release was **conceptual and idealized** — strong on theory, limited in *verifiable practice*. It lacked:
- A formal audit mechanism.  
- Automated reproducibility.  
- Explicit data-privacy boundaries in code.  
- A demonstrable visual diagnostic (radar) integrated with the test chain.

---

## 2. Now (v0.2.1 – The Architecture of Limitation)
### Key Improvements
| Area | v0.1 (Concept) | v0.2.1 (Architecture of Limitation) |
|------|----------------|-------------------------------------|
| **Core Algorithm** | Triadic vector (Salience, Grip, Coherence) | Unchanged — same formula, weights, and semantics |
| **Implementation** | Stand-alone scripts | Modular Python package with `pqi/`, `tools/`, and `docs/audits/` |
| **Verification** | Manual testing | Full **audit chain** (`audit_prep`, `audit_log`, `audit_sync`) with timestamped markdown records |
| **Reproducibility** | Limited to local runs | Automated CI workflow + reproducible `run_audit_chain.ps1` |
| **Visualization** | External/optional | **Legacy radar** reinstated (`pqi/legacy/radar.py`) for interpretability |
| **Privacy Posture** | Implicit (“no data stored”) | Explicit **privacy-first** design — all data remains local, no telemetry |
| **Philosophical Integration** | Theoretical link to Vervaeke | Operational link: “limitation as verification” — philosophy embedded in tooling |
| **Usability** | Research-grade prototype | Developer-ready open-core system (MIT + Relevance Audit license) |

---

## 3. The Philosophy Behind the Upgrade
> *“Limitation is not the end of innovation; it is how truth learns to hold its shape.”*

In **v0.2.1**, PQI’s evolution mirrors its own moral claim:
- Where v0.1 *spoke about relevance*, v0.2.1 *measures it in action*.  
- Where v0.1 theorized about **proportion**, v0.2.1 enforces proportion through auditable constraint.  
- Where v0.1 was a **model of meaning**, v0.2.1 becomes a **system of accountability**.

By embedding philosophy directly in the code structure, PQI no longer needs external validation — it *demonstrates its ethics by design*.

---

## 4. The Audit Chain: Integrity as Process
The audit chain operationalizes the **Architecture of Limitation**:
1. `audit_prep.py` — generates a dated checklist of conditions to verify.  
2. `pytest --pqi-autolog` — runs tests, logs results to `docs/audits/run_log.md`.  
3. `audit_sync.py` — merges logs and checklists into a cumulative record.  
4. `run_audit_chain.ps1` — automates the entire process for consistent replication.

Every run now leaves an immutable trail — a *temporal signature of integrity*.  
No data leaves the local system; no audit depends on external validation.

---

## 5. The Legacy Radar: Visualization as Reflection
The radar chart, re-introduced as `pqi/legacy/radar.py`, translates PQI vectors into a perceptual field.  
It restores the visual diagnostic from the original concept, allowing developers and researchers to *see* the balance between **Salience**, **Grip**, and **Coherence** — a lived embodiment of proportion.

---

## 6. Why This Matters
- **For Researchers:** PQI is now a citable, reproducible artifact (Zenodo DOI pending).  
- **For Developers:** The codebase is modular, auditable, and ready for integration with ethical AI toolchains.  
- **For Philosophers:** PQI demonstrates how metaphysical principles like *limitation, relevance, and proportion* can be expressed in executable form.  
- **For Regulators:** PQI offers a path out of “regulatory panic loops” — measuring not harm itself, but the *relevance of harm* to lived context.

---

## 7. Closing Reflection
> *“In the first version, PQI asked what relevance is.  
> In this one, it learns what relevance does when bound by care.”*

**PQI v0.2.1** completes the first cycle of its design philosophy:  
from concept → implementation → verification.  
What began as an ethical hypothesis is now a reproducible method.  
The next iterations will explore **adaptive weighting** and **meta-auditing** — teaching the architecture to audit itself.
