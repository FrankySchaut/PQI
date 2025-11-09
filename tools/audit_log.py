#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime

AUDITS = Path("docs/audits"); AUDITS.mkdir(parents=True, exist_ok=True)
CSV = AUDITS / "run_log.csv"
MD  = AUDITS / "run_log.md"
CSV_HEADER = "timestamp,version,test_cycle,tests,passed,failed,skipped,duration_s,notes\n"

def append_run_summary(*, version: str, test_cycle: str, tests: int, passed: int, failed: int, skipped: int, duration_s: float, notes: str = "") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not CSV.exists(): CSV.write_text(CSV_HEADER, encoding="utf-8")
    CSV.open("a", encoding="utf-8").write(f"{ts},{version},{test_cycle},{tests},{passed},{failed},{skipped},{duration_s:.2f},{notes.replace(',',';')}\n")
    if not MD.exists():
        MD.write_text("# PQI Audit Run Log\n\n| Timestamp | Version | Cycle | Tests | Passed | Failed | Skipped | Duration (s) | Notes |\n|---|---|---|---:|---:|---:|---:|---:|---|\n", encoding="utf-8")
    MD.open("a", encoding="utf-8").write(f"| {ts} | {version} | {test_cycle} | {tests} | {passed} | {failed} | {skipped} | {duration_s:.2f} | {notes} |\n")
