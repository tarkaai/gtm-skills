---
name: support-issue-tracking-smoke
description: >
  Support Ticket Churn Signals — Smoke Test. Pull 90 days of support tickets from Intercom,
  classify by category/severity/sentiment, and manually correlate ticket patterns with known
  churned accounts to validate whether support data predicts churn.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Identify at least 1 statistically meaningful ticket pattern that appears in churned accounts at 2x+ the rate of retained accounts"
kpis: ["Churn-signal lift (target: ≥2x for at least 1 signal)", "Ticket classification accuracy (spot-check ≥80% correct)", "Accounts analyzed (≥20 churned + ≥20 retained)"]
slug: "support-issue-tracking"
install: "npx gtm-skills add product/retain/support-issue-tracking"
drills:
  - support-ticket-analysis
  - threshold-engine
---

# Support Ticket Churn Signals — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Prove that support ticket data contains actionable churn signals. You are looking for at least one ticket pattern (high volume, repeat bugs, billing questions, frustrated sentiment) that shows up in churned accounts at 2x+ the rate of retained accounts. If the signal exists, this play has legs. If ticket patterns are random with respect to churn, stop here.

Pass: At least 1 ticket signal with lift >= 2x, validated against ≥20 churned and ≥20 retained accounts.
Fail: No signal exceeds 1.5x lift after analyzing 40+ accounts, or insufficient ticket data to analyze.

## Leading Indicators

- Ticket classification LLM produces consistent, sensible tags when spot-checked against 10 random tickets (≥80% agreement with human judgment)
- Churned accounts have observably higher ticket volume than retained accounts in the raw data before formal analysis
- At least 3 distinct ticket categories appear in the data (the taxonomy is useful, not all tickets lumped into one bucket)
- You can match ticket contacts to CRM records for ≥80% of tickets (data joins work)

## Instructions

### 1. Export and classify historical tickets

Run the `support-ticket-analysis` drill in backfill mode. Pull 90 days of closed conversations from Intercom. Classify each by category, severity, and sentiment using the LLM tagging step. This produces a structured dataset of every support interaction with consistent labels.

Before proceeding, spot-check 10 random classifications against the actual ticket text. If accuracy is below 80%, adjust the classification prompt in the `intercom-ticket-tagging` fundamental (add examples of misclassified tickets to the prompt as few-shot examples) and re-run.

### 2. Build churned vs retained comparison

Manually identify two groups from your CRM (Attio) or billing system:
- **Churned**: ≥20 accounts that cancelled or downgraded in the last 90 days
- **Retained**: ≥20 accounts that remained active throughout the same period, matched by plan tier and tenure (compare similar accounts)

For each account in both groups, pull their ticket summary from Step 1: ticket count, category breakdown, severity breakdown, average CSAT, repeat issues, sentiment trend.

**Human action required:** If your CRM does not have clean churn dates, you need to manually identify churned accounts from billing records or cancellation emails. This is the one piece of data the agent cannot reliably automate at Smoke level.

### 3. Calculate signal lift

For each ticket signal, calculate the lift:
- **Ticket volume**: Median tickets/month for churned vs retained. Lift = churned_median / retained_median.
- **Bug tickets**: % of churned accounts with ≥2 bug tickets vs % of retained. Lift = churned_% / retained_%.
- **Billing tickets**: Same calculation for billing category.
- **Critical/high severity**: % with any critical or high ticket.
- **Low CSAT (≤2)**: % with any CSAT rating ≤2.
- **Repeat issues**: % with the same issue reported twice or more.
- **Frustrated sentiment**: % with ≥1 frustrated-tagged ticket.
- **Competitor mentions**: % mentioning a competitor.

Record all lifts. Rank by lift value descending.

### 4. Evaluate against threshold

Run the `threshold-engine` drill. The pass criteria: at least 1 signal with lift ≥ 2x across the dataset of 40+ accounts.

- **PASS (≥2x lift on at least 1 signal):** Document the top 3 signals by lift. Record their coverage (what % of churned accounts exhibit the signal) and false positive rate (what % of retained accounts also exhibit it). These validated signals become the foundation for the Baseline scoring model. Proceed to Baseline.
- **MARGINAL (1.5-2x lift):** The signal is weak but present. Check: Is your sample size too small? Are your churned/retained groups well-matched? Try increasing to 30+ per group and re-analyzing.
- **FAIL (no signal >1.5x):** Support tickets may not be a meaningful churn predictor for your product. Consider: Do you have enough ticket volume? (If most accounts never file tickets, the signal is too sparse.) Is your product's churn driven by factors invisible in support (pricing, competition, budget cuts)? Pivot to a different retention play.

## Time Estimate

- Intercom API export + LLM classification: 1 hour (agent-automated)
- Churned/retained account identification: 1 hour (human + agent)
- Data joining and signal calculation: 1.5 hours (agent-automated)
- Spot-checking and analysis: 1 hour
- Threshold evaluation and documentation: 30 minutes
- Total: ~5 hours over 1 week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | Source of support ticket data | Existing plan ([intercom.com/pricing](https://intercom.com/pricing)) |
| Anthropic (Claude Haiku) | Ticket classification LLM | ~$0.001/ticket, ~$0.50 for 500 tickets ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| PostHog | Event logging for classified tickets | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | CRM for account matching | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated cost for Smoke:** <$1 (LLM classification of historical tickets)

## Drills Referenced

- `support-ticket-analysis` — export, classify, and aggregate ticket data from Intercom into structured per-account summaries
- `threshold-engine` — evaluate churn signal lift against the ≥2x pass threshold
