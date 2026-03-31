---
name: support-issue-tracking-scalable
description: >
  Support Ticket Churn Signals — Scalable Automation. Scale churn scoring to all accounts,
  add multi-channel interventions, segment by account tier, and integrate product feedback
  loops. Target ≥55% churn save rate on flagged accounts at 500+ active accounts.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥55% save rate on CS-intervened accounts and ≥65% recall at 500+ active accounts"
kpis: ["Churn save rate (target ≥55% of intervened accounts retained)", "Churn prediction recall (target ≥65%)", "Churn prediction precision (target ≥40%)", "Product feedback loop: ≥1 product fix shipped from support data per month"]
slug: "support-issue-tracking"
install: "npx gtm-skills add product/retain/support-issue-tracking"
drills:
  - churn-prevention
  - nps-feedback-loop
  - dashboard-builder
---

# Support Ticket Churn Signals — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Scale the system from reactive alerting to proactive retention. At Baseline, you scored accounts and alerted CS. At Scalable, you add automated interventions (in-app messages, targeted emails, proactive check-ins), segment interventions by account value, and close the feedback loop to product so recurring issues actually get fixed.

Pass: ≥55% of accounts that receive CS intervention are retained (save rate), churn recall ≥65%, and at least 1 product fix per month is shipped based on support data insights.
Fail: Save rate below 40% after 1 month of scaled interventions, or product team is not acting on support signals.

## Leading Indicators

- Automated in-app messages reach at-risk accounts within 1 hour of score exceeding threshold (no human bottleneck)
- CS reps report that alerts include enough context to have productive conversations without additional research
- Product team receives monthly support-signal reports and adds items to their roadmap
- Account segmentation routes enterprise accounts to high-touch CS and SMB accounts to automated flows
- Repeat issue count for top 3 categories trends downward month-over-month (product is fixing root causes)

## Instructions

### 1. Build tiered intervention system

Run the `churn-prevention` drill to add automated interventions layered on top of the existing scoring:

**Tier 1 — Automated (score 26-50, medium risk):**
- In-app message via Intercom acknowledging the issue pattern: "We noticed you've had some friction with [top_category]. Here's how to [workaround/fix]." Link to relevant help article.
- Triggered email via Loops with proactive tips addressing their specific issue category.
- No human action required. Fully automated.

**Tier 2 — CS-assisted (score 51-75, high risk):**
- Everything from Tier 1 plus: CS task created in Attio with full context.
- CS rep sends a personal email referencing the specific issues: "I saw your team ran into [specific problem] a few times this month. I want to make sure this gets resolved — can we hop on a 15-minute call?"
- If the account is on an annual plan approaching renewal, flag for renewal risk.

**Tier 3 — Escalation (score 76+, critical risk):**
- Immediate Slack alert to CS lead.
- CS lead or founder makes a same-day call.
- Prepare a retention offer if appropriate (extended trial, temporary discount, priority support).
- If competitor was mentioned, prepare competitive positioning points.

Segment by account value: Enterprise accounts (MRR > $500) get Tier 2 treatment at score 30+ and Tier 3 at score 60+. SMB accounts use the standard thresholds.

### 2. Close the product feedback loop

Run the `nps-feedback-loop` drill to deploy NPS surveys triggered by support resolution. When a ticket is closed, wait 24 hours, then send a 2-question NPS survey via Intercom. This captures resolution satisfaction separate from the general CSAT.

Aggregate support-driven NPS by issue category. Monthly, generate a product feedback report:
- Top 5 issue categories by ticket volume
- Which categories have the worst NPS
- Which categories correlate most with churn
- Specific feature requests or bug reports that appear 5+ times
- Estimated revenue at risk from each category (sum of MRR for high/critical accounts affected)

**Human action required:** Present this report to the product team monthly. The agent generates the report; a human ensures it reaches the right stakeholders and tracks whether items enter the roadmap. Product fixes driven by support data directly reduce churn risk.

### 3. Build the operational dashboard

Run the `dashboard-builder` drill to create a support-retention operational dashboard:

- **Real-time panel**: Current high/critical risk accounts with scores, intervention status, and days since last CS contact
- **Trend panel**: Weekly ticket volume, category distribution, and churn score distribution — 12-week trend
- **Intervention funnel**: Alerts sent -> CS acted -> Customer responded -> Retained (30 days). Show save rate by tier and by account segment.
- **Product impact**: Repeat issue counts for top categories. Overlay with product fix ship dates to show impact of fixes on ticket volume.
- **Revenue at risk**: Total MRR of accounts at high/critical risk. Trend this weekly. This is the number that gets executive attention.

### 4. Evaluate at scale

After 2 months of scaled operation, evaluate using the `threshold-engine` drill (included in the `churn-prevention` drill's evaluation step):

- **Save rate**: Of all accounts that received intervention (Tier 1, 2, or 3), what % were retained 30 days later? Target ≥55%.
- **Recall**: Of all accounts that churned, what % were flagged? Target ≥65%.
- **Precision**: Of all flagged accounts, what % actually churned? Target ≥40%.
- **Product loop**: Was at least 1 product fix shipped based on support data this month? (Binary: yes/no.)

- **PASS (all targets met):** The system is working at scale. Document: intervention templates, scoring thresholds, and product feedback process. Proceed to Durable.
- **MARGINAL:** If save rate is low but recall is high, the interventions are weak — test different messages and offers. If recall dropped from Baseline, the scoring model drifted — recalibrate with fresh churn data. If product loop is missing, escalate the feedback report.
- **FAIL:** If save rate is below 40% after active optimization, the interventions may not be addressing the real reasons for churn. Conduct exit interviews with 5 churned accounts flagged high-risk to understand what would have kept them.

## Time Estimate

- Tiered intervention system build: 15 hours
- NPS + product feedback loop setup: 10 hours
- Dashboard creation: 8 hours
- Account segmentation and routing rules: 7 hours
- Two months of monitoring and optimization: 12 hours
- Evaluation and documentation: 8 hours
- Total: ~60 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | In-app messaging + NPS surveys + ticket source | Essential $29/seat/mo or Advanced $85/seat/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Anthropic (Claude) | Ticket classification + churn scoring | ~$15-30/mo at scale ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| PostHog | Dashboards + cohorts + funnels | Free tier or Growth $0/mo + usage ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Triggered retention emails | Starter $25/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Workflow orchestration | Free self-hosted or Starter 24 EUR/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM + CS task management | Free up to 3 users or Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated monthly cost for Scalable:** $75-200/mo (Intercom seat + LLM costs + Loops)

## Drills Referenced

- `churn-prevention` — detect churn signals from usage data and trigger tiered interventions
- `nps-feedback-loop` — deploy post-resolution NPS surveys and route feedback to product
- `dashboard-builder` — create the support-retention operational dashboard in PostHog
