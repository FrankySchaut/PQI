#!/usr/bin/env python3
from pathlib import Path
import csv

AUDITS = Path("docs/audits")
CSV = AUDITS / "run_log.csv"
MD  = AUDITS / "run_log.md"

HEADER = """# PQI Audit Run Log

| Timestamp | Version | Cycle | Tests | Passed | Failed | Skipped | Duration (s) | Notes |
|---|---|---|---:|---:|---:|---:|---:|---|
"""

def main():
    if not CSV.exists():
        print(f"[!] CSV not found: {CSV}. Nothing to sync."); return
    rows=[]
    with CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            notes = (r.get("notes") or "").replace("\n"," ").strip()
            rows.append(f"| {r['timestamp']} | {r['version']} | {r['test_cycle']} | {r['tests']} | {r['passed']} | {r['failed']} | {r['skipped']} | {float(r['duration_s']):.2f} | {notes} |")
    MD.write_text(HEADER + ("\n".join(rows)+"\n" if rows else ""), encoding="utf-8")
    print(f"[✓] Synced {len(rows)} rows → {MD}")

if __name__ == "__main__":
    main()
