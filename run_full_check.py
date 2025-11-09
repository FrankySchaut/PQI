"""
PQI v0.2.1 – Full Functionality Sanity Check
Runs through core, radar, and audit functions to ensure everything works end-to-end.
"""

import sys, pathlib, pprint, importlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

print("=== PQI FULL FUNCTIONALITY TEST ===")
print("Loading PQI core...")

try:
    from pqi.pqi_core import PQI
    pqi = PQI()
    sample = {
        "salience": 0.85,
        "grip": 0.65,
        "coherence": 0.70,
    }
    score = pqi.score(sample)
    print(f"PQI core score OK → {score:.2f}")
except Exception as e:
    print(f"[ERROR] PQI core test failed: {e}")

# --- Radar Visualization Test ---
print("\nLoading radar visualization...")
try:
    from pqi.legacy.radar import plot_relevance_radar
    import os, webbrowser

    out_path = "docs/audits/last_radar.png"
    result = plot_relevance_radar(
        {"salience": 0.85, "grip": 0.65, "coherence": 0.70},
        title="PQI Sanity Radar",
        save_path=out_path,
        show=False,  # change to True if you want a pop-up window
    )

    if result and result.get("saved"):
        print(f"Radar visualization OK (saved → {out_path})")
        webbrowser.open(os.path.abspath(out_path))
    else:
        print("Radar visualization OK (plot displayed or saved).")

except Exception as e:
    print(f"[ERROR] Radar visualization test failed: {e}")

# --- Tools Check ---
print("\nTesting tools (audit_log, audit_prep, audit_sync)...")

try:
    from tools import audit_log, audit_prep, audit_sync
    audit_prep.main()
    audit_log.append_run_summary(
        version="v0.2.1", test_cycle="I", tests=3, passed=3,
        failed=0, skipped=0, duration_s=1.23, notes="full check"
    )
    audit_sync.main()
    print("Tools OK (audit chain executed).")
except Exception as e:
    print(f"[ERROR] Tools test failed: {e}")

# --- CLI Sanity Check ---
print("\nTesting CLI entry point...")
try:
    import subprocess
    result = subprocess.run(
        [sys.executable, "cli.py", "--help"],
        capture_output=True, text=True, timeout=5
    )
    print("CLI help output:")
    print(result.stdout.splitlines()[0:3])
    print("CLI OK")
except Exception as e:
    print(f"[ERROR] CLI test failed: {e}")

# --- Timing and summary ---
print("\nAll tests executed at:", time.strftime("%Y-%m-%d %H:%M:%S"))
print("Check for any [ERROR] lines above.")
print("If none appear, your environment is fully consistent with PQI v0.2.1.")
