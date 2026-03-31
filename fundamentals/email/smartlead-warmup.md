---
name: smartlead-warmup
description: Warm up sending accounts using Smartlead's warmup network
tool: Smartlead
product: Smartlead
difficulty: Setup
---

# Warm Up Accounts in Smartlead

## Prerequisites
- Smartlead account with connected email accounts
- DNS records configured (SPF, DKIM, DMARC) on all sending domains

## Steps

1. **Enable warmup per account via API.** Use the Smartlead API or MCP to enable warmup:
   ```
   POST /api/v1/email-accounts/<id>/warmup/enable
   { "daily_limit": 5, "increase_per_day": 2, "max_limit": 40, "reply_rate": 35, "move_from_spam": true }
   ```
   Smartlead's warmup network sends and receives emails between real user accounts to build positive sender reputation.

2. **Configure warmup parameters.** Starting volume: 5 emails/day, ramping by 2/day to max 40. Reply rate: 35%. Enable "move from spam to inbox" -- warmup recipients rescue emails from spam, training providers to inbox your messages.

3. **Monitor warmup score via API.** Check warmup health:
   ```
   GET /api/v1/email-accounts/<id>/warmup/status
   ```
   A healthy score is 90+. Check daily for the first week. If score drops below 80, check DNS records and pause cold sending from that account.

4. **Warmup duration.** New domains require a minimum 14-day warmup period. Do not send cold emails during this window. Older domains (6+ months) can start with a 7-day warmup.

5. **Keep warmup running.** Never disable warmup while campaigns are active. Warmup emails maintain your sender reputation alongside cold outreach. Smartlead automatically balances warmup and campaign volume within daily limits.

6. **Scale with multiple accounts.** For higher volume, add more sending accounts rather than increasing per-account limits. Three accounts sending 40/day (120 total) is safer than one account sending 120/day. Smartlead's inbox rotation handles the distribution.
