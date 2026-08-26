# SEPA Direct Debit Refund Draft Helper

A static, private browser helper for preparing an editable SEPA Direct Debit refund request draft.

The page can help classify common timing routes:

- authorised Direct Debit inside the common eight-week refund window;
- unauthorised or mandate-missing Direct Debit inside the thirteen-month route;
- outside standard windows;
- missing evidence to check before contacting a bank.

It does not send data anywhere, does not contact a bank, does not verify a real entitlement and is not legal or financial advice. Users should verify deadlines, scheme rules and local bank procedures before sending any request.

The public page includes a canonical URL, basic social metadata, local JSON-LD SoftwareApplication/FAQPage markup, visible FAQ copy and accessible form help text. It remains static and does not load third-party runtime resources.

## Use

Open `index.html` locally or visit the GitHub Pages site:

https://bluepeakfoundry.github.io/sepa-direct-debit-refund-draft/

## Privacy

This is a static page. It has no tracking, no external scripts, no server submission and no payment flow.

## Validation

```bash
python3 validate_public_site.py
```
