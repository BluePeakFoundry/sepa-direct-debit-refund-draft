#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED = ["index.html", "app.js", "style.css", "README.md", "LICENSE", "robots.txt", "sitemap.xml"]
FORBIDDEN = ["Sergi", "Rex", r"\bagent\b", r"\bbot\b", "money generated", "money verified", "monetization", "cycle"]
REMOTE_RESOURCE_RE = re.compile(r"<(script|img|iframe)\b[^>]*src=\"https?://|<form\b[^>]*action=", re.I)


def main() -> int:
    missing = [name for name in REQUIRED if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"missing required files: {missing}")
    public_text = "\n".join((ROOT / name).read_text(encoding="utf-8") for name in REQUIRED)
    visible_public_text = "\n".join(
        (ROOT / name).read_text(encoding="utf-8")
        for name in REQUIRED
        if name not in {"robots.txt"}
    )
    found = [term for term in FORBIDDEN if re.search(term, visible_public_text, flags=re.IGNORECASE)]
    if found:
        raise SystemExit(f"public files contain internal language: {found}")
    runtime_text = "\n".join((ROOT / name).read_text(encoding="utf-8") for name in ["index.html", "app.js", "style.css"])
    if REMOTE_RESOURCE_RE.search(runtime_text):
        raise SystemExit("runtime files include remote resources or submission targets")
    required_phrases = [
        "nothing is uploaded",
        "does not verify a real entitlement",
        "not legal or financial advice",
        "no tracking",
        "no external scripts",
        "eight-week",
        "thirteen-month",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase.lower() not in public_text.lower()]
    if missing_phrases:
        raise SystemExit(f"missing expected public safeguards: {missing_phrases}")
    if "money_verified" in public_text or "external_actions" in public_text:
        raise SystemExit("internal accounting fields leaked into public copy")
    print("OK public site files=7 no_remote_runtime_resources privacy_safeguards_present")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
