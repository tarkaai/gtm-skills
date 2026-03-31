---
name: ai-support-chatbot-scalable
description: >
  AI In-App Support — Scalable Automation. Find the 10x multiplier: segment-specific
  chatbot personas, proactive support triggers, churn-correlated support intervention,
  and multi-language scaling without proportional human headcount.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥60% AI resolution rate at 500+ users/mo; human ticket volume down ≥40%; churn-risk accounts get intervention within 48h"
kpis: ["AI resolution rate at scale", "Human ticket volume reduction", "Churn intervention coverage", "Resolution rate by segment", "Cost per resolution"]
slug: "ai-support-chatbot"
install: "npx gtm-skills add product/retain/ai-support-chatbot"
drills:
  - support-ticket-analysis
  - support-churn-correlation
---

# AI In-App Support — Scalable Automation

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Find the 10x multiplier. At Baseline, the chatbot resolves 50% of conversations for your current user base. At Scalable, it handles 500+ support-seeking users per month at 60%+ resolution rate without adding human agents. The chatbot becomes a retention engine: support ticket patterns feed churn prediction, at-risk accounts get proactive intervention, and knowledge gaps are filled faster than they appear. Human agents focus exclusively on complex, high-value conversations.

## Leading Indicators

- Support ticket analysis classifies 90%+ of historical conversations with valid category/severity/sentiment tags (data quality is sufficient for churn correlation)
- Churn correlation identifies at least 3 ticket patterns with >2x lift for churn prediction (signals are actionable)
- Cost per AI resolution stays below $1.50 even as volume grows (unit economics work at scale)
- Knowledge pipeline gap closure rate exceeds 70% within 2 weeks of identification (flywheel is fast enough)

## Instructions

### 1. Build the support-churn intelligence layer

Run the `support-ticket-analysis` drill to classify and analyze all historical support data:
- Export the last 90 days of Intercom conversations
- Classify each by category, severity, sentiment, and churn signals using LLM auto-tagging
- Aggregate by account: ticket velocity, category distribution, severity trend, CSAT, repeat issues, sentiment trajectory
- Log events to PostHog (`support_ticket_classified`, `support_account_summary_updated`)
- Enrich Attio company records with support health attributes

Set this to run daily via n8n to keep classifications current.

### 2. Correlate support patterns with churn

Run the `support-churn-correlation` drill to identify which ticket patterns actually predict churn:
- Build churned-vs-retained cohorts in PostHog
- Compare ticket patterns between cohorts: volume, categories, severity, resolution time, CSAT, repeat issues
- Rank signals by lift, coverage, and false positive rate
- Score all active accounts for churn risk based on their support history
- Route high-risk and critical-risk accounts to CS via automated n8n alerts

This creates a feedback loop: the chatbot generates structured support data, which feeds churn prediction, which triggers retention interventions before the user cancels.

### 3. Scale the knowledge pipeline

Upgrade the the chatbot knowledge pipeline workflow (see instructions below) drill from weekly to twice-weekly runs:
- Monday and Thursday at 6am
- Reduce the gap threshold from 3 occurrences to 2 (catch gaps faster)
- Add a "product launch" trigger: when a new feature ships, proactively generate help articles from the feature's documentation before users start asking questions
- Track gap closure rate: from identification to published article, target <5 business days

**Human action required:** Continue reviewing and publishing draft articles. Consider delegating review to a support team member or CS lead rather than founder/PM.

### 4. Segment chatbot behavior by user type

Configure Fin AI to adjust its behavior based on user properties in Intercom:

- **New users (signup <14 days)**: More proactive article suggestions. Offer guided walkthroughs. Lower escalation threshold (hand off faster if confused).
- **Power users**: More technical responses. Link to API docs and advanced articles. Higher escalation threshold (they can handle more bot interaction).
- **Enterprise accounts**: Human-first for complex issues. Fin handles only simple how-to questions. Escalation includes account context and CS owner name.
- **Churn-risk accounts (score >50)**: Human-first routing. Fin can answer simple questions but any sign of frustration triggers immediate escalation with churn context.

Implement via Intercom user properties (set from PostHog cohorts and Attio churn scores) and Fin targeting rules.

### 5. Launch proactive support triggers

Instead of waiting for users to ask for help, detect struggle signals and offer help proactively:

- **Error page visits**: If a user hits an error page 2+ times in a session, trigger an Intercom message: "Having trouble? Our support bot can help — [open chat]"
- **Feature abandonment**: If a user starts a workflow but does not complete it within the expected time, offer contextual help via tooltip or in-app message
- **Usage decline**: If a user's weekly activity drops >50% vs their average, send an Intercom message: "We noticed you have been less active. Anything we can help with?"

Wire these triggers via PostHog events → n8n webhook → Intercom in-app message API.

### 6. Measure scale metrics

After 2 months, evaluate:
- **AI resolution rate at scale**: ≥60% with 500+ support-seeking users/month. Pass/fail.
- **Human ticket volume**: ≥40% reduction vs pre-chatbot baseline. Pass/fail.
- **Churn intervention coverage**: ≥80% of accounts scored high/critical risk received a human touchpoint within 48 hours. Pass/fail.
- **Cost per resolution**: AI resolutions cost <$1.50 each including Fin fees + knowledge pipeline costs. Pass/fail.
- **Segment resolution rates**: No user segment has a resolution rate below 40% (no segment is being left behind). Pass/fail.

If all PASS, proceed to Durable. If resolution rate plateaus, run a deep analysis on top escalation topics — the knowledge pipeline may need product documentation updates, not just article generation. If human volume has not dropped enough, check whether the chatbot is handling the right conversations (are easy questions reaching humans anyway?).

## Time Estimate

- 12 hours: support ticket analysis setup, historical backfill, classification validation
- 10 hours: churn correlation analysis, scoring model setup, alert routing
- 8 hours: knowledge pipeline upgrade (twice-weekly, product launch trigger)
- 10 hours: user segment configuration, Fin targeting rules, proactive support triggers
- 12 hours: monitoring, weekly reviews, article review cycles (spread over 2 months)
- 8 hours: scale testing, metric evaluation, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom (Advanced) | Fin AI + advanced routing + team inboxes | $85/seat/mo + $0.99/resolution — [intercom.com/pricing](https://www.intercom.com/pricing) |
| PostHog | Analytics, cohorts, experiments, feature flags | Free up to 1M events/mo; ~$50-100/mo at scale — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API | Ticket classification, article generation, churn scoring, reports | ~$40-80/mo at 500+ users — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Estimated cost for Scalable: ~$250–500/mo** (Intercom $85 base + $200-300 Fin resolutions at volume + $40-80 Anthropic + PostHog usage)

## Drills Referenced

- `support-ticket-analysis` — classifies all support tickets by category/severity/sentiment, aggregates by account for churn analysis
- `support-churn-correlation` — identifies which ticket patterns predict churn, scores accounts, routes alerts to CS
- the chatbot knowledge pipeline workflow (see instructions below) — twice-weekly gap detection and article generation, now with proactive coverage for product launches
