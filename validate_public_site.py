#!/usr/bin/env python3
from __future__ import annotations

import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED = ["index.html", "app.js", "analytics.js", "style.css", "README.md", "LICENSE", "robots.txt", "sitemap.xml"]
FORBIDDEN = ["Sergi", "Rex", r"\bagent\b", r"\bbot\b", "money generated", "money verified", "monetization", "cycle"]
REMOTE_RESOURCE_RE = re.compile(r"<(script|img|iframe)\b[^>]*src=\"https?://(?!gc\.zgo\.at/count\.js)|<form\b[^>]*action=", re.I)
CANONICAL = "https://bluepeakfoundry.github.io/sepa-direct-debit-refund-draft/"


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
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    if f'<link rel="canonical" href="{CANONICAL}">' not in index:
        raise SystemExit("missing canonical URL")
    for phrase in ['property="og:title"', 'property="og:description"', 'name="twitter:card"', 'FAQPage', 'SoftwareApplication']:
        if phrase not in index:
            raise SystemExit(f"missing SEO/structured data marker: {phrase}")
    json_ld_blocks = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', index, flags=re.S)
    if not json_ld_blocks:
        raise SystemExit("missing JSON-LD block")
    for block in json_ld_blocks:
        json.loads(block)
    for field_id in ["bank", "creditor", "amount", "debitDate", "assessmentDate", "status"]:
        if f'for="{field_id}"' not in index:
            raise SystemExit(f"missing explicit label for {field_id}")
    for marker in ['aria-describedby="form-help"', 'aria-live="polite"', 'aria-atomic="true"', 'class="skip-link"']:
        if marker not in index:
            raise SystemExit(f"missing accessibility marker: {marker}")
    required_phrases = [
        "nothing is uploaded",
        "does not verify a real entitlement",
        "not legal or financial advice",
        "no cookies",
        "eight-week",
        "thirteen-month",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase.lower() not in public_text.lower()]
    if missing_phrases:
        raise SystemExit(f"missing expected public safeguards: {missing_phrases}")
    for marker in ["bluepeakfoundry.goatcounter.com/count", "analytics.js", "data-analytics-event", "data-analytics-submit"]:
        if marker not in public_text:
            raise SystemExit(f"missing analytics marker: {marker}")
    if "money_verified" in public_text or "external_actions" in public_text:
        raise SystemExit("internal accounting fields leaked into public copy")
    print("OK public site files=7 no_remote_runtime_resources privacy_safeguards_present seo_accessibility_present")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
