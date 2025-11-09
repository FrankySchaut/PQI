# run_audit_chain.ps1
# PQI v0.2.1 – Complete Audit Chain (ASCII-only)

param(
    [string]$Version = "v0.2.1",
    [string]$Cycle   = "I",
    [string]$Notes   = "automated audit chain run"
)

$ErrorActionPreference = "Stop"

Write-Host "=== PQI AUDIT CHAIN START ===`n"
Write-Host "Version: $Version"
Write-Host "Cycle:   $Cycle"
Write-Host "Notes:   $Notes`n"

# 1) Prepare new audit checklist
Write-Host "Step 1: Preparing audit checklist..."
python -m tools.audit_prep
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Step 1 failed - aborting."
    exit $LASTEXITCODE
}

# 2) Run tests with auto-log
Write-Host "`nStep 2: Running tests with auto-log..."
python -m pytest -q --pqi-autolog --pqi-cycle $Cycle --pqi-version $Version --pqi-notes "$Notes"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Step 2 failed - aborting."
    exit $LASTEXITCODE
}

# 3) Sync audit chain
Write-Host "`nStep 3: Syncing audit log..."
python -m tools.audit_sync
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Step 3 failed - aborting."
    exit $LASTEXITCODE
}

Write-Host "`nPQI Audit Chain completed successfully."
Write-Host "Check docs/audits/ for generated files."
Write-Host "=== AUDIT CHAIN END ==="
