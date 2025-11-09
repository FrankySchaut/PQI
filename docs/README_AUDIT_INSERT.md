## Audit & Test Workflow — The Architecture of Limitation in Code
```bash
python tools/audit_prep.py
pytest -q --pqi-autolog --pqi-cycle I --pqi-version v0.2 --pqi-notes "local run"
python tools/audit_sync.py
```
Outputs: docs/audits/run_log.csv, docs/audits/run_log.md, docs/audits/audit_checklist_*.md

## Continuous Integration (GitHub Actions)
See .github/workflows/ci.yml
