---
name: affiliate-link-generation
description: Generate, manage, and distribute unique affiliate tracking links and referral codes
tool: Rewardful / FirstPromoter / PartnerStack / Tapfiliate
difficulty: Setup
---

# Affiliate Link Generation

## Prerequisites

- Affiliate program configured (see `affiliate-program-setup`)
- Affiliate/partner record created in the platform
- Landing page(s) ready to receive referred traffic

## Steps

### 1. Create an affiliate and generate their link

**Rewardful:**

```
POST https://api.rewardful.com/v1/affiliates
Authorization: Bearer {REWARDFUL_API_KEY}
Content-Type: application/json

{
  "email": "partner@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "campaign_id": "{campaign_id}"
}
```

Response:

```json
{
  "id": "aff_abc123",
  "email": "partner@example.com",
  "link": "https://yourdomain.com?via=janesmith",
  "referral_code": "janesmith",
  "token": "abc123xyz"
}
```

**FirstPromoter:**

```
POST https://firstpromoter.com/api/v1/promoters/create
Authorization: Bearer {FIRSTPROMOTER_API_KEY}

{
  "email": "partner@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "campaign_id": "{campaign_id}",
  "ref_id": "janesmith"
}
```

### 2. Generate custom landing page links

Create links pointing to specific landing pages (not just the homepage):

```
POST https://api.rewardful.com/v1/affiliates/{affiliate_id}/links
{
  "url": "https://yourdomain.com/pricing",
  "utm_source": "affiliate",
  "utm_medium": "partner",
  "utm_campaign": "reseller-program",
  "utm_content": "{affiliate_slug}"
}
```

This generates: `https://yourdomain.com/pricing?via=janesmith&utm_source=affiliate&utm_medium=partner&utm_campaign=reseller-program&utm_content=janesmith`

### 3. Generate coupon-based tracking (alternative to links)

For partners who promote verbally (podcasts, events, word of mouth), create discount codes that double as tracking:

**Stripe coupon + Rewardful attribution:**

```
# Create a Stripe coupon
POST https://api.stripe.com/v1/coupons
Authorization: Bearer {STRIPE_SECRET_KEY}

{
  "percent_off": 10,
  "duration": "once",
  "id": "PARTNER-JANESMITH",
  "metadata": {
    "affiliate_id": "aff_abc123",
    "campaign": "reseller-program"
  }
}
```

Then link the coupon to the affiliate in Rewardful so any redemption triggers commission.

### 4. Bulk-generate links for multiple affiliates

```python
import requests

REWARDFUL_API_KEY = "{REWARDFUL_API_KEY}"
CAMPAIGN_ID = "{campaign_id}"
BASE_URL = "https://api.rewardful.com/v1"

partners = [
    {"email": "partner1@co.com", "first_name": "Alice", "last_name": "Lee"},
    {"email": "partner2@co.com", "first_name": "Bob", "last_name": "Chen"},
    # ... more partners
]

for partner in partners:
    resp = requests.post(
        f"{BASE_URL}/affiliates",
        headers={"Authorization": f"Bearer {REWARDFUL_API_KEY}"},
        json={**partner, "campaign_id": CAMPAIGN_ID}
    )
    data = resp.json()
    print(f"{partner['email']}: {data['link']}")
```

### 5. List all affiliate links

```
GET https://api.rewardful.com/v1/affiliates?campaign_id={campaign_id}&page=1&per_page=50
Authorization: Bearer {REWARDFUL_API_KEY}
```

## Error Handling

- If link not tracking: verify the Rewardful/FirstPromoter JS snippet is loaded on the target page
- If duplicate affiliate error: search existing affiliates by email first before creating
- If coupon not attributing: ensure the Stripe coupon metadata includes the affiliate_id and the platform webhook is listening for `customer.discount.created` events

## Output

- Unique affiliate tracking links for each partner
- UTM-tagged links for PostHog attribution
- Optional coupon codes for verbal/offline promotion
- Bulk generation capability for scaling the program
