---
name: clay-credits
description: Monitor and optimize Clay credit usage to control enrichment costs
tool: Clay
product: Clay
difficulty: Beginner
---

# Manage Clay Credits

## Prerequisites
- Clay account with a credit balance
- At least one enrichment table set up

## Steps

1. **Understand Clay's credit model.** Each enrichment action (find email, verify email, enrich company, find people) costs credits. Costs vary by provider -- basic lookups cost 1 credit, premium providers like Clearbit cost 2-5 credits per row. Waterfall enrichment charges only for the provider that returns data.

2. **Check your credit balance.** Use the Clay API to check remaining credits and monthly allocation. Set up a low-balance alert at 20% remaining to avoid mid-campaign interruption.

3. **Budget credits per campaign.** Before running enrichment, calculate expected cost: (Number of rows) x (Credits per enrichment column) x (Number of enrichment columns). A typical enrichment workflow (company + person + email + verify) costs 5-8 credits per row.

4. **Use conditional enrichment.** Add "Run if" conditions to expensive enrichment columns. Example: only run Clearbit enrichment if Apollo returned no data. Only verify emails that were successfully found. This can reduce credit usage by 30-40%.

5. **Set table row limits.** Cap your table size before running enrichment. Start with 50 rows for testing, then scale to 200 once you have confirmed your enrichment columns work correctly.

6. **Track ROI on credits.** Calculate cost per qualified lead: (Credits used x Credit cost) / Qualified leads generated. If a campaign costs $50 in credits and produces 10 qualified leads, your cost per lead is $5. Compare this across campaigns to optimize spend.
