---
name: smartlead-inbox-rotation
description: Configure inbox rotation to distribute sends across multiple accounts
tool: Smartlead
product: Smartlead
difficulty: Intermediate
---

# Set Up Inbox Rotation in Smartlead

## Prerequisites
- Smartlead account with 3+ connected and warmed sending accounts
- At least one active campaign

## Steps

1. **Understand inbox rotation.** Inbox rotation distributes campaign emails across multiple sending accounts. Instead of one account sending 100 emails, four accounts each send 25. This protects individual account reputation and increases total daily capacity.

2. **Connect multiple accounts via API.** Add at least 3 sending accounts across 2+ domains using the Smartlead API:
   ```
   POST /api/v1/email-accounts/add
   { "email": "dan@acmehq.com", "provider": "google" }
   ```
   Example setup: 2 accounts on acmehq.com, 2 on getacme.com for domain-level diversification.

3. **Assign accounts to campaigns.** In your campaign configuration, assign all warmed accounts. Smartlead automatically rotates using round-robin distribution. Each prospect receives all sequence emails from the same account for conversation threading.

4. **Set per-account limits via API.** Configure conservative daily limits:
   ```
   PATCH /api/v1/email-accounts/<id>/settings
   { "daily_limit": 40 }
   ```
   30-50 sends per account for cold outreach. Smartlead pauses an account at its limit and continues with other accounts.

5. **Monitor per-account health.** Use the API to check per-account deliverability metrics: `GET /api/v1/email-accounts/<id>/stats`. If one account shows higher bounce rates or lower open rates, pause it from campaigns and investigate. One bad account can be replaced without stopping the campaign.

6. **Scale strategically.** When you need more volume, add new accounts and warm them for 14 days before including in rotation. Scaling path: 3 accounts (90-150 sends/day) -> 6 accounts (180-300 sends/day) -> 10 accounts (300-500 sends/day).
