---
name: clay-email-verification
description: Verify email addresses before outreach to protect sender reputation
tool: Clay
difficulty: Beginner
---

# Verify Emails in Clay

## Prerequisites
- Clay table with enriched email addresses
- Understanding of email deliverability basics

## Steps

1. **Add an email verification column.** In your Clay table, add a "Verify Email" enrichment column. Select a verification provider -- Neverbounce and ZeroBounce are the most reliable options in Clay's provider list.

2. **Understand verification statuses.** Verification returns one of: Valid (safe to send), Invalid (do not send), Catch-all (domain accepts all emails -- risky), Unknown (provider could not determine). Only send to Valid addresses.

3. **Run verification on your list.** Execute the verification column. This costs 1 credit per email checked. For a 200-row table, budget 200 credits for verification.

4. **Filter results.** Create a view that filters to only "Valid" emails. This is your send-ready list. Catch-all emails can be included at Baseline level but should be throttled (send no more than 20% catch-all in any campaign).

5. **Track your verification rate.** A healthy list has 70%+ valid emails. Below 60% indicates your enrichment sources are returning stale data -- consider adjusting your waterfall provider order.

6. **Re-verify before sending.** If your list is more than 2 weeks old, re-run verification before launching a campaign. Email validity decays as people change jobs, and sending to invalid addresses damages your domain reputation.
