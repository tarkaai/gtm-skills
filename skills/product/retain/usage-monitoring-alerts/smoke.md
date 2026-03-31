---
name: usage-monitoring-alerts-smoke
description: >
  Usage Drop Alerting — Smoke Test. Run a one-time engagement drop scan on your existing user
  base, identify the top at-risk accounts, and manually intervene to test whether early
  detection produces re-engagement.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "Identify 10+ accounts with engagement drops and re-engage at least 3 through manual outreach"
kpis: ["Accounts flagged with engagement drop", "Manual intervention count", "Re-engagement rate within 14 days"]
slug: "usage-monitoring-alerts"
install: "npx gtm-skills add product/retain/usage-monitoring-alerts"
drills:
  - usage-drop-detection
  - threshold-engine
---

# Usage Drop Alerting — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Prove that you can detect meaningful engagement drops from your product data and that reaching out to flagged accounts produces re-engagement. This is a one-time manual run — no automation, no always-on monitoring. You are testing whether the signal is real.

## Leading Indicators

- PostHog query returns a non-trivial number of accounts with 30%+ engagement drops
- At least some flagged accounts are genuinely at risk (not on vacation, not seasonal)
- Manual outreach to flagged accounts gets responses or produces re-engagement within 14 days

## Instructions

### 1. Define your core engagement signal

Before running any queries, decide what "engagement" means for your product. Pick 2-3 events that represent real value delivery — not page views or passive logins.

Examples by product type:
- **SaaS tool:** `document_created`, `workflow_completed`, `data_exported`
- **Platform:** `api_call_made`, `integration_used`, `query_executed`
- **Collaboration:** `message_sent`, `comment_posted`, `file_shared`

Write these down. They become the events in every query going forward.

### 2. Run the initial drop detection scan

Run the `usage-drop-detection` drill — but only the manual query steps (Steps 1 and 2). Do not set up the n8n automation yet. Execute the HogQL queries directly against PostHog via the API or MCP:

- Compute each account's 30-day weekly engagement baseline
- Compare their last 7 days against that baseline
- Filter for accounts with 30%+ drops

Export the results as a list: account name, email, baseline weekly activity, current weekly activity, percentage drop.

### 3. Classify and prioritize the flagged accounts

Review the list manually. For each flagged account:
- Check if the drop is real (not a vacation, holiday, or known product outage)
- Note their plan tier and MRR from Attio
- Sort by: highest-value accounts with the steepest drops first

Pick the top 10 accounts for manual intervention.

### 4. Manually intervene with the top 10

For each of the 10 accounts, send a personal email from the account owner (or founder if no account owner exists). The email should:
- Reference their specific usage pattern ("You were using [feature] regularly until recently")
- Ask a direct question ("Is something blocking you?" or "Did something change on your end?")
- Offer concrete help (a call, a walkthrough, a specific resource)
- Include a calendar booking link

**Human action required:** Write and send each email personally. Do not use a template blast. The goal is to learn what is actually happening with these accounts.

### 5. Track responses and re-engagement

For each of the 10 accounts, track over 14 days:
- Did they respond to the email? What did they say?
- Did they return to the product? (Check PostHog for activity after intervention)
- If they re-engaged, did their usage stabilize or drop again?

Log outcomes in a simple table: account, drop %, intervention date, response (Y/N), re-engaged (Y/N), feedback notes.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to measure against the pass threshold: **re-engage at least 3 of the 10 flagged accounts within 14 days.**

If PASS: The signal is real — engagement drops predict churn risk and early intervention works. Move to Baseline.

If FAIL: Investigate why. Possible causes:
- The engagement signal was wrong (tracking vanity metrics, not real engagement)
- The drop thresholds were too sensitive (flagging normal variation)
- The intervention was too late (accounts had already mentally churned)

Adjust and re-run before moving to Baseline.

## Time Estimate

- 1 hour: Define engagement signals, write PostHog queries
- 1 hour: Run detection scan, export and review results
- 2 hours: Write and send 10 personal intervention emails
- 2 hours: Monitor responses and re-engagement over 14 days, compile results

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Query engagement data, identify drops | Free up to 1M events/mo; https://posthog.com/pricing |
| Attio | Look up account value and owner | Free for small teams; https://attio.com/pricing |

## Drills Referenced

- `usage-drop-detection` — Run the manual query portion to identify accounts with engagement drops
- `threshold-engine` — Evaluate pass/fail against the re-engagement threshold
