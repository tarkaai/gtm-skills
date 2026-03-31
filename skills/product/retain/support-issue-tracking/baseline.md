---
name: support-issue-tracking-baseline
description: >
  Support Ticket Churn Signals — Baseline Run. Deploy always-on ticket classification, account-level
  churn scoring, and automated CS alert routing. Validate that scoring identifies ≥60% of accounts
  that actually churn within 30 days.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "Churn prediction recall ≥60% — of accounts that churn, ≥60% were flagged high/critical risk beforehand"
kpis: ["Churn prediction recall (target ≥60%)", "Churn prediction precision (target ≥35%)", "CS alert-to-action rate (target ≥80%)", "Mean time from alert to CS outreach (target <48 hours)"]
slug: "support-issue-tracking"
install: "npx gtm-skills add product/retain/support-issue-tracking"
drills:
  - support-churn-correlation
  - posthog-gtm-events
  - threshold-engine
---

# Support Ticket Churn Signals — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Turn the validated churn signals from Smoke into an always-on system. Tickets are classified in real-time as they arrive. Every active account gets a weekly churn risk score based on their ticket history. High/critical risk accounts trigger automated CS alerts with context and talking points.

Pass: Of all accounts that churn in the evaluation period, ≥60% were flagged high or critical risk at least 7 days before cancellation (recall ≥60%). Precision ≥35% (at least 35% of flagged accounts actually churn, so CS time is not wasted on false alarms).
Fail: Recall below 50% after 2 weeks of scoring, or CS team ignores >50% of alerts.

## Leading Indicators

- Real-time ticket classification runs within 60 seconds of ticket creation (the webhook + n8n pipeline works end-to-end)
- Account churn scores update weekly without manual intervention
- CS reps acknowledge ≥80% of high/critical alerts within 24 hours (alerts are reaching the right people and are actionable)
- At least 3 accounts are flagged high/critical risk in the first week (the scoring threshold is calibrated — not too sensitive, not too lenient)
- Spot-check 5 flagged accounts: do the risk signals match reality when a human reviews the ticket history?

## Instructions

### 1. Set up real-time ticket classification pipeline

Run the `posthog-gtm-events` drill to establish the event taxonomy for support tracking. Define these events:
- `support_ticket_created`: fired when a new Intercom conversation is created
- `support_ticket_classified`: fired after LLM classification, properties include category, severity, sentiment, churn_signals
- `support_churn_score_calculated`: fired after weekly account scoring
- `support_cs_alert_sent`: fired when a CS alert is routed
- `support_intervention_logged`: fired when CS acts on an alert

Then configure the real-time pipeline: Intercom webhook on `conversation.created` triggers an n8n workflow that fetches the conversation, classifies it with the LLM, applies tags to Intercom, and fires PostHog events. This replaces the batch backfill from Smoke with continuous processing.

### 2. Deploy account-level churn scoring

Run the `support-churn-correlation` drill. This builds the weekly scoring pipeline:

1. Every Sunday night, n8n triggers a workflow that pulls all accounts with ticket activity in the last 30 days
2. For each account, aggregates their ticket history (volume, categories, severities, CSAT, repeats, sentiment trend)
3. Passes the account summary to the `ticket-churn-signal-scoring` fundamental
4. Stores the score, risk level, and recommended action in Attio
5. Routes high/critical scores to CS via Slack alert and Attio task

Use the signal weights validated in Smoke as the scoring model's starting point. If Smoke found that "≥3 tickets in 30 days" had 3x lift and "frustrated sentiment" had 2.5x lift, those signals get the highest weights.

### 3. Build CS alert workflow

The alert must be actionable without CS needing to research the account. Each alert includes:
- Account name, plan, MRR, tenure
- Current churn risk score and risk level
- Top 3 risk signals (e.g., "4 bug tickets in 2 weeks, CSAT 2.0, competitor mention")
- Specific talking points (e.g., "Address the recurring CSV export failure. Acknowledge the wait time on their last critical ticket.")
- Link to the Intercom conversation history for the account
- Recommended intervention type (call, email, in-app message)

Route to the account's CS owner in Attio. If no owner assigned, route to the CS team Slack channel.

### 4. Track and evaluate

After 2 full weeks of scoring, evaluate against the threshold using the `threshold-engine` drill:

- Pull all accounts that churned during the evaluation period
- Check: what % were scored high/critical at least 7 days before cancellation? (This is recall.)
- Pull all accounts that were scored high/critical during the evaluation period
- Check: what % actually churned within 30 days? (This is precision.)
- Check: what % of CS alerts were acted on within 48 hours? (This is the alert-to-action rate.)

- **PASS (recall ≥60%, precision ≥35%, alert-to-action ≥80%):** The scoring model catches most churn risk and CS is using the alerts. Document the current signal weights and thresholds. Proceed to Scalable.
- **MARGINAL (recall 50-60% or precision 25-35%):** Adjust scoring weights. If recall is low, lower the threshold for high risk (catch more accounts). If precision is low, raise the threshold (fewer false alarms). Re-evaluate after 1 more week.
- **FAIL (recall <50% or alert-to-action <50%):** If recall is low, the ticket signals may not be sufficient predictors on their own — consider combining with usage data from the `churn-prevention` drill. If CS is ignoring alerts, the alerts are either too noisy or not reaching the right channel. Talk to CS and fix the routing.

## Time Estimate

- Real-time pipeline setup (webhook + n8n + PostHog events): 4 hours
- Churn scoring pipeline configuration: 4 hours
- CS alert workflow build and testing: 3 hours
- Two weeks of monitoring: 2 hours (periodic checks)
- Evaluation and threshold analysis: 3 hours
- Total: ~16 hours over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | Ticket source + webhook events | Existing plan ([intercom.com/pricing](https://intercom.com/pricing)) |
| Anthropic (Claude Haiku) | Real-time ticket classification | ~$5-15/mo at 5K-15K tickets/mo ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Anthropic (Claude Sonnet) | Weekly churn scoring | ~$4-8/mo for 100-200 accounts ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| PostHog | Event tracking and cohort analysis | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Webhook processing + scheduled workflows | Free self-hosted or Starter at 24 EUR/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM for score storage and CS routing | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated monthly cost for Baseline:** $10-25/mo (LLM classification + scoring)

## Drills Referenced

- `support-churn-correlation` — validate churn signals, score accounts, and route CS alerts
- `posthog-gtm-events` — establish the support event taxonomy for real-time tracking
- `threshold-engine` — evaluate recall, precision, and alert-to-action metrics against pass thresholds
