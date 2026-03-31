---
name: usage-limit-sales-upsell-smoke
description: >
  Usage-Based Upsell — Smoke Test. Manually identify accounts hitting usage limits,
  qualify the top 3-5 for sales outreach, and close at least 1 expansion deal within
  1 week to validate that usage-limit signals drive sales-led upsell conversations.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email, Direct"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: ">=1 expansion deal closed from >=3 qualified accounts within 1 week"
kpis: ["Expansion signal detection rate", "Qualification rate (signals to sales-ready)", "Meeting booking rate", "Expansion close rate", "Expansion ARR from closed deals"]
slug: "usage-limit-sales-upsell"
install: "npx gtm-skills add product/upsell/usage-limit-sales-upsell"
drills:
  - usage-threshold-detection
  - threshold-engine
---

# Usage-Based Upsell — Smoke Test

> **Stage:** Product -> Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Direct

## Outcomes

Prove the concept: do usage-limit signals reliably surface accounts that are ready for a sales-led expansion conversation? No automation, no always-on pipeline. Run the detection query once, manually qualify a handful of accounts, personally reach out, and close at least 1 expansion deal. The signal must produce a higher close rate than cold outreach to existing customers.

## Leading Indicators

- Detection query returns at least 10 accounts at 70%+ of a plan limit (sufficient signal volume)
- At least 3 accounts pass qualification gates (the signal produces sales-worthy opportunities, not noise)
- At least 2 of the 3 qualified accounts respond to outreach within 5 business days (the timing and framing resonate)
- At least 1 account books a meeting to discuss expansion (the upsell conversation is welcome, not annoying)

## Instructions

### 1. Verify usage data exists in PostHog

Run the `usage-threshold-detection` drill in manual mode. Confirm your PostHog project tracks per-account resource consumption. Execute this verification query via PostHog API or MCP:

```sql
SELECT
  event,
  count(),
  uniq(properties.account_id)
FROM events
WHERE timestamp > now() - interval 30 day
  AND event IN ('resource_consumed', 'api_call', 'project_created', 'seat_added', 'storage_used')
GROUP BY event
ORDER BY count() DESC
```

You need at least one event type tracking a metered resource against a plan limit. If no usage tracking exists, instrument it first using the `posthog-custom-events` fundamental. At minimum, capture: account_id, resource_type, current_count, and plan_limit.

### 2. Run the threshold detection manually

Execute the detection query once to find accounts at 70%+ of any plan limit:

```sql
SELECT
  properties.account_id AS account_id,
  properties.resource_type AS resource_type,
  properties.current_count AS current_count,
  properties.plan_limit AS plan_limit,
  properties.plan_tier AS plan_tier,
  round(properties.current_count / properties.plan_limit * 100, 1) AS pct_used
FROM events
WHERE event = 'resource_consumed'
  AND timestamp > now() - interval 7 day
  AND properties.plan_limit > 0
  AND properties.current_count / properties.plan_limit >= 0.7
ORDER BY pct_used DESC
```

Export the results. Classify each account by urgency tier: approaching (70-84%), imminent (85-94%), critical (95%+).

### 3. Manually qualify accounts for sales outreach

Run the the expansion signal qualification workflow (see instructions below) drill manually on the detected accounts:

1. Pull account context from Attio: MRR, plan tier, days since signup, account owner, support ticket history
2. Apply the qualification gates: MRR >= $100, active >= 30 days, no active expansion deal, no critical support tickets open
3. Score each qualifying account using the signal-based criteria: usage urgency, multi-resource proximity, billing page visits, team growth
4. Select the top 3-5 accounts scoring 60+ points as sales-ready

**Human action required:** Review the qualified accounts. Verify the usage data is accurate by spot-checking 1-2 accounts in the product admin panel. Remove any accounts where the limit hit is expected behavior (e.g., a known test account, an account on a grandfathered plan that should not be upsold).

### 4. Create expansion deals and reach out

For each of the 3-5 qualified accounts:

1. Create an expansion deal in Attio with the account context, usage numbers, and estimated expansion ARR
2. Craft a personal email referencing their specific usage data. Use this framework:
   - Open: "I noticed your team has used {{pct_used}}% of your {{resource_name}} this month."
   - Frame as growth, not problem: "That level of usage tells me [product] is central to your workflow."
   - Bridge to expansion: "Most teams at your stage move to {{next_tier}} because [specific benefit]. Want me to walk you through it?"
   - CTA: Calendar link for a 15-minute expansion call
3. Send the email personally (from the founder or account owner, not a marketing address)
4. If no response after 3 business days, send a follow-up that adds urgency: projected limit-hit date and what happens when the limit is reached

**Human action required:** Send the outreach emails personally. The founder or account owner must be the sender for Smoke — no automation, no sequences. Personalize each email with the account's actual numbers.

### 5. Run the expansion conversation

For accounts that respond or book meetings:

1. Prepare with the full usage context: which resources are near limits, consumption velocity, team size, feature adoption
2. Lead the conversation with their growth, not with pricing: "Your team is growing fast — here is how {{next_tier}} supports that"
3. Present the upgrade options: next tier, annual discount, custom plan if enterprise
4. Close or capture the objection. If the objection is price-related, note the specific concern for future iteration

### 6. Evaluate against threshold

Run the `threshold-engine` drill to measure: of the 3-5 qualified accounts you reached out to, did at least 1 close an expansion deal within 1 week?

Also evaluate:

- How many accounts did detection find at 70%+? (signal volume)
- Of those, how many passed qualification? (signal quality)
- Of qualified accounts, what was the response rate to outreach? (message-market fit)
- Of responses, what was the meeting booking rate?
- Of meetings, what was the close rate?
- What was the total expansion ARR from closed deals?
- Which resource type drove the strongest expansion signal?
- Were any accounts annoyed by the outreach? (negative signal — important to track)

If PASS (1+ deal closed), proceed to Baseline. If FAIL, examine: were the accounts truly expansion-ready? Was the outreach framed as helpful or pushy? Was the upgrade path too expensive for the value delivered? Fix and re-run.

## Time Estimate

- 1 hour: verify PostHog usage data and run the detection query
- 1.5 hours: qualify accounts (pull CRM context, apply scoring, select top 3-5)
- 1.5 hours: create expansion deals and craft personalized outreach emails
- 1 hour: follow-up emails and monitor responses over the week
- 1 hour: run expansion conversations (meetings)
- 1 hour: evaluate results, document findings, calculate metrics

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage data queries, account identification | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — expansion deals, account context | Free up to 3 seats — [attio.com/pricing](https://attio.com/pricing) |

**Estimated cost for Smoke: Free** (using existing PostHog and Attio instances, manual outreach via personal email)

## Drills Referenced

- `usage-threshold-detection` — identifies accounts approaching plan limits by querying PostHog usage data (run manually for Smoke)
- the expansion signal qualification workflow (see instructions below) — qualifies detected accounts for sales outreach using CRM context and scoring criteria (run manually for Smoke)
- `threshold-engine` — evaluates whether the expansion close rate meets the pass threshold
