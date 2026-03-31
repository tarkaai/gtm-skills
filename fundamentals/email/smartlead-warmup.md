---
name: smartlead-warmup
description: Warm up sending accounts using Smartlead's warmup network
tool: Smartlead
difficulty: Setup
---

# Warm Up Accounts in Smartlead

## Prerequisites
- Smartlead account with connected email accounts
- DNS records configured (SPF, DKIM, DMARC) on all sending domains

## Steps

1. **Enable warmup per account.** In Smartlead, go to Email Accounts, select an account, and enable Warmup. Smartlead's warmup network sends and receives emails between real user accounts to build positive sender reputation.

2. **Configure warmup parameters.** Set the starting volume to 5 emails per day, ramping up by 2 per day to a maximum of 40. Set the reply rate to 35%. Enable "Move from spam to inbox" -- Smartlead warmup recipients will rescue your emails from spam, training providers to inbox your messages.

3. **Monitor warmup score.** Smartlead provides a warmup health score per account. Check it daily for the first week. A healthy score is 90+. If score drops below 80, check your DNS records and pause any cold sending from that account.

4. **Warmup duration.** New domains require a minimum 14-day warmup period. Do not send any cold emails during this window. Older domains (6+ months) can start with a 7-day warmup. Mark your calendar with the "safe to send" date for each account.

5. **Keep warmup running.** Never disable warmup while campaigns are active. Warmup emails maintain your sender reputation alongside cold outreach. Smartlead automatically balances warmup and campaign volume within your daily limits.

6. **Scale with multiple accounts.** For higher volume, add more sending accounts rather than increasing per-account limits. Three accounts sending 40/day (120 total) is safer than one account sending 120/day. Smartlead's inbox rotation handles the distribution.
