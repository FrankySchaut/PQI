# Prompt Quality Index (PQI) v0.2
# Author: Franky Schaut
# Repository: https://github.com/FrankySchaut/PQI
# License: MIT — Privacy-first, local execution

import re

EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE = re.compile(r"\b(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}\b")
IDLIKE = re.compile(r"\b[A-Z]{2,3}\d{4,}\b")
URL = re.compile(r"https?://\S+")

def redact(text: str) -> str:
    t = EMAIL.sub("[EMAIL]", text)
    t = PHONE.sub("[PHONE]", text)
    t = IDLIKE.sub("[ID]", t)
    t = URL.sub("[URL]", t)
    return t
