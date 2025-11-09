#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path

TEMPLATE = """# PQI Relevance Audit Checklist — Operational Form (v1.0)
**Part of The Architecture of Limitation in Code**

### Pre-Audit Header
| Field | Entry |
|-------|-------|
| **Test Cycle** | ☐ I Relevance Stability ☐ II Applied Audit ☐ III Field Integration |
| **Repository Version Tag** | {version} |
| **Tester / Reviewer** | {tester} |
| **Date** | {date} |
| **Data Source** | ☐ Synthetic ☐ Derived ☐ Abstracted ☐ Live |
| **Expected Scope** | |

### 1 · Input Verification
☐ No raw personal identifiers present  
☐ Input reduced to numeric features (S,G,C)  
☐ Values constrained to 0 ≤ x ≤ 1  
☐ Feature extraction documented  
☐ 10 % sample inspected

### 2 · Environmental Controls
☐ Local/offline execution  
☐ No API/telemetry/logging  
☐ Temp files purged  
☐ Weights (α+β+γ=1) validated

### 3 · Output Verification
☐ Output limited to PQI score + verdict  
☐ No intermediate data stored  
☐ Logs anonymised  
☐ Emily Filter threshold validated

### 4 · Ethical Proportion Review
| Question | Y/N | Comment |
|---|---|---|
| Inquiry > surveillance? | | |
| Proportionate to purpose? | | |
| Re-identification risk? | | |
| Reflection recorded? | | |

### 5 · Post-Run Notes

### 6 · Sign-off
| Role | Name | Timestamp |
|---|---|---|
| Tester | | |
| Reviewer | | |
"""

def create_audit_checklist(tester="Franky", version="v0.2"):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = Path("docs/audits"); out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"audit_checklist_{ts}.md"
    path.write_text(TEMPLATE.format(tester=tester, version=version, date=datetime.now().strftime("%Y-%m-%d")), encoding="utf-8")
    print(f"[✓] Created new audit checklist: {path}")
    return path

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--tester", default="Franky")
    ap.add_argument("--version", default="v0.2")
    args = ap.parse_args()
    create_audit_checklist(args.tester, args.version)
