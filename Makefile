.PHONY: audit-sync test audit fmt lint typecheck qa
audit-sync:
	python tools/audit_sync.py
test:
	pytest -q
audit:
	python tools/audit_prep.py
	pytest -q --pqi-autolog --pqi-cycle I --pqi-version v0.2 --pqi-notes "local run"
	python tools/audit_sync.py
fmt:
	black .
lint:
	ruff check .
typecheck:
	mypy pqi tools
qa: fmt lint typecheck
