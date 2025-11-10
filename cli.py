# Prompt Quality Index (PQI) v0.2
# Author: Franky Schaut
# Repository: https://github.com/FrankySchaut/PQI
# License: MIT — Privacy-first, local execution

import argparse
import json
import sys
from pqi.redactor import redact
from pqi.scorer import score_prompt


def main():
    parser = argparse.ArgumentParser(description="PQI v0.2 — Privacy-First Prompt Quality Index")
    parser.add_argument("--prompt", "-p", type=str, help="Prompt text")
    parser.add_argument("--no-redact", action="store_true", help="Skip PII redaction")
    args = parser.parse_args()

    text = args.prompt or sys.stdin.read().strip()
    if not args.no_redact:
        text = redact(text)

    result = score_prompt(text)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
