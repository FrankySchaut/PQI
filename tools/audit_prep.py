#!/usr/bin/env python3
from os import getenv

from tools.audit_checklist import create_audit_checklist


def main():
    tester = getenv("PQI_TESTER", "Franky")
    version = getenv("PQI_VERSION", "v0.2")
    return create_audit_checklist(tester=tester, version=version)


if __name__ == "__main__":
    main()
