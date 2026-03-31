---
name: instantly-warmup
description: Warm up sending accounts to build sender reputation before campaigns
tool: Instantly
difficulty: Setup
---

# Warm Up Email Accounts in Instantly

## Prerequisites
- Instantly account with connected sending accounts
- DNS records configured (SPF, DKIM, DMARC)

## Steps

1. **Enable warmup immediately via API.** As soon as you connect a new sending account, enable warmup:
   ```
   POST /api/v1/account/<email>/warmup/enable
   { "daily_limit": 5, "increase_per_day": 2, "max_limit": 40, "reply_rate": 35 }
   ```
   Warmup sends automated emails between Instantly users' accounts to build positive sender signals.

2. **Configure warmup settings.** Set daily warmup email limit to start at 5, increasing by 2 per day up to a maximum of 40. Set reply rate to 30-40% (Instantly will auto-reply to that percentage of warmup emails). Choose slow ramp-up speed.

3. **Wait the minimum warmup period.** New domains need at least 14 days of warmup before any cold sending. Established domains (6+ months old with some email history) can start after 7 days. Do not skip this step -- sending cold email from unwarm accounts will land in spam.

4. **Monitor warmup health via API.** Check the warmup status:
   ```
   GET /api/v1/account/<email>/warmup/status
   ```
   Look for: inbox placement rate (target 95%+), warmup emails being opened, no bounces or blocks. If inbox placement drops below 90%, pause and investigate DNS configuration.

5. **Keep warmup running during campaigns.** Never turn off warmup while running campaigns. Warmup emails maintain your sender reputation alongside cold sends. Instantly handles the volume balance automatically.

6. **Rotate accounts showing poor health.** If an account's warmup score drops below 80% (check via API), pause cold sending from that account but keep warmup active. If it does not recover in 7 days, replace the account with a new one.
