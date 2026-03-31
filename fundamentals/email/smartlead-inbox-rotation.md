---
name: smartlead-inbox-rotation
description: Configure inbox rotation to distribute sends across multiple accounts
tool: Smartlead
difficulty: Intermediate
---

# Set Up Inbox Rotation in Smartlead

## Prerequisites
- Smartlead account with 3+ connected and warmed sending accounts
- At least one active campaign

## Steps

1. **Understand inbox rotation.** Inbox rotation distributes your campaign emails across multiple sending accounts. Instead of one account sending 100 emails, four accounts each send 25. This protects individual account reputation and increases total daily capacity.

2. **Connect multiple accounts.** Add at least 3 sending accounts across 2+ domains. Example setup: 2 accounts on acmehq.com, 2 accounts on getacme.com. This provides domain-level diversification in addition to account-level rotation.

3. **Assign accounts to campaigns.** In your campaign settings, select all warmed accounts for the campaign. Smartlead automatically rotates between them using round-robin distribution. Each prospect receives all sequence emails from the same account for conversation threading.

4. **Set per-account limits.** Configure each account with conservative daily limits: 30-50 sends per account for cold outreach. Smartlead respects these limits during rotation and will pause an account once its limit is reached, continuing with other accounts.

5. **Monitor per-account health.** In the Email Accounts dashboard, check deliverability metrics per account. If one account shows higher bounce rates or lower open rates than others, pause it from campaigns and investigate. One bad account can be replaced without stopping the campaign.

6. **Scale strategically.** When you need more volume, add new accounts and warm them for 14 days before including in rotation. A good scaling path: start with 3 accounts (90-150 sends/day), grow to 6 accounts (180-300 sends/day), then 10 accounts (300-500 sends/day) as your pipeline demands increase.
