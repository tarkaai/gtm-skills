---
name: lob-address-verify
description: Verify and standardize a US mailing address via the Lob Address Verification API
tool: Lob
difficulty: Setup
---

# Lob Address Verify

Verify that a physical mailing address is deliverable before sending postcards. This avoids wasted print-and-postage costs on undeliverable addresses. Lob uses USPS CASS-certified validation.

## Authentication

Same as all Lob endpoints — HTTP Basic Auth with your API key as username, empty password.

## API Endpoint

```
POST https://api.lob.com/v1/us_verifications
```

## Request Format

```bash
curl https://api.lob.com/v1/us_verifications \
  -u "$LOB_API_KEY:" \
  -d "primary_line={{address_line1}}" \
  -d "secondary_line={{address_line2}}" \
  -d "city={{city}}" \
  -d "state={{state}}" \
  -d "zip_code={{zip}}"
```

Or verify with a single freeform string:

```bash
curl https://api.lob.com/v1/us_verifications \
  -u "$LOB_API_KEY:" \
  -d "address=123 Main St, San Francisco CA 94107"
```

## Response

```json
{
  "id": "us_ver_abc123",
  "primary_line": "123 MAIN ST",
  "secondary_line": "",
  "city": "SAN FRANCISCO",
  "state": "CA",
  "zip_code": "94107",
  "deliverability": "deliverable",
  "deliverability_analysis": {
    "dpv_confirmation": "Y",
    "dpv_cmra": "N",
    "dpv_vacant": "N",
    "dpv_active": "Y"
  },
  "components": {
    "primary_number": "123",
    "street_predirection": "",
    "street_name": "MAIN",
    "street_suffix": "ST",
    "city": "SAN FRANCISCO",
    "state": "CA",
    "zip_code": "94107",
    "zip_code_plus_4": "1234"
  }
}
```

## Deliverability Values

- `deliverable` — Address exists and can receive mail. Safe to send.
- `deliverable_unnecessary_unit` — Deliverable, but the secondary line (apt/suite) is unnecessary.
- `deliverable_incorrect_unit` — Address is real but the unit number is wrong. Fix before sending.
- `deliverable_missing_unit` — Multi-unit building but no unit specified. May reach the building but not the right person.
- `undeliverable` — Address does not exist or cannot receive mail. Do NOT send.

## Decision Logic

```
IF deliverability == "deliverable" OR deliverability == "deliverable_unnecessary_unit":
    Use the standardized address from the response (it may correct typos)
    Proceed to lob-postcard-send
ELIF deliverability == "deliverable_missing_unit":
    Flag for manual review — may need a suite/apt number
ELSE:
    Mark contact as "bad address" in CRM, skip this recipient
```

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 200 | Verification complete | Check `deliverability` field |
| 401 | Invalid API key | Check credentials |
| 422 | Could not parse the address | Address is too malformed to verify — skip |

## Pricing

- Address verification is included in all Lob plans
- Free tier: 300 verifications/month
- Paid plans: volume-based pricing
- Pricing page: https://www.lob.com/pricing

## Notes

- Always use the standardized address from the response (uppercased, formatted) when sending postcards — it improves deliverability
- Run verification in batch before a campaign, not at send time, to catch issues early
- Store the `deliverability` status on the contact record in your CRM
- For international addresses, use `POST /intl_verifications` instead
