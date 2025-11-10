#!/usr/bin/env python3
from tools.audit_checklist import create_audit_checklist
from os import getenv


def main():
    tester = getenv("PQI_TESTER", "Franky")
    version = getenv("PQI_VERSION", "v0.2")
    return create_audit_checklist(tester=tester, version=version)


if __name__ == "__main__":
    main()
