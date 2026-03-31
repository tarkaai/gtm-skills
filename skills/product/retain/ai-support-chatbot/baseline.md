---
name: ai-support-chatbot-baseline
description: >
  AI In-App Support — Baseline Run. Scale the AI chatbot to all users, launch
  the knowledge gap pipeline, and configure intelligent escalation routing.
  First always-on automation.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥50% AI resolution rate; ≥4.0 CSAT for AI-resolved; human ticket volume down ≥20%"
kpis: ["AI resolution rate", "CSAT (AI-resolved)", "Human ticket volume reduction", "Escalation routing accuracy"]
slug: "ai-support-chatbot"
install: "npx gtm-skills add product/retain/ai-support-chatbot"
drills:
  - chatbot-knowledge-pipeline
  - chatbot-resolution-monitor
---

# AI In-App Support — Baseline Run

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Roll the chatbot out to 100% of users, turn on always-on knowledge gap detection, and configure intelligent escalation routing. By the end of 2 weeks, the AI chatbot should resolve at least half of all support conversations without human help, maintain high satisfaction, and measurably reduce human agent workload. This is the first always-on automation — the chatbot runs continuously, the knowledge pipeline fills gaps weekly, and escalation routing operates in real-time.

## Leading Indicators

- Knowledge pipeline identifies 3+ gaps in its first weekly run and generates draft articles (the pipeline is working)
- Escalation routing correctly assigns priority tiers for 85%+ of sampled conversations (routing logic is sound)
- Resolution rate trends upward week-over-week as knowledge gaps are filled (the flywheel is turning)
- Human agent first-response time improves as lower-priority tickets are properly queued (load is being managed)

## Instructions

### 1. Roll out to 100%

Remove the PostHog feature flag gate (or set it to 100% rollout). All users now interact with the AI chatbot as their first point of contact. Monitor the first 48 hours closely for any spike in escalations or negative CSAT.

### 2. Launch the knowledge gap pipeline

Run the `chatbot-knowledge-pipeline` drill to set up the always-on knowledge improvement loop:
- Configure an n8n workflow that runs every Monday at 6am
- The workflow pulls all chatbot escalation conversations from the past 7 days
- Classifies questions by topic using Claude Haiku
- Identifies the top 3 knowledge gaps (topics with 3+ unanswered questions)
- Generates draft Intercom help articles using Claude Sonnet
- Posts a Slack summary with links to draft articles for human review

**Human action required:** Review and publish draft articles within 48 hours of each weekly pipeline run. Fin only indexes published articles. Verify accuracy, adjust tone, and add screenshots where helpful.

### 3. Configure intelligent escalation routing

Run the the chatbot escalation routing workflow (see instructions below) drill to replace the generic escalation queue with priority-based routing:
- P0 (immediate): security, data loss, billing disputes, cancellation intent → senior support / CS lead
- P1 (high): enterprise accounts, churn-risk-critical, production blockers → dedicated support / CS owner
- P2 (standard): general technical issues, how-to questions → general support queue
- P3 (low): feedback, minor issues, general questions → general queue, lowest priority

The drill builds an n8n workflow triggered by every Fin escalation that classifies the conversation, enriches with CRM data from Attio, computes priority, routes to the correct team inbox, and adds context notes for the human agent.

### 4. Build the monitoring layer

Run the `chatbot-resolution-monitor` drill to create:
- A PostHog dashboard tracking resolution rate, CSAT, escalation patterns, top unresolved topics, and support load impact
- Anomaly alerts: resolution rate drop >10 points, CSAT below 3.0, escalation rate above 70%, single topic >30% of escalations
- Weekly health report delivered to Slack every Monday

### 5. Evaluate against threshold

After 2 weeks of always-on operation, measure:
- **AI resolution rate**: ≥50% of conversations resolved without human handoff. Pass/fail.
- **CSAT for AI-resolved**: ≥4.0 average rating. Pass/fail.
- **Human ticket volume**: ≥20% reduction compared to pre-chatbot baseline. Pass/fail.
- **Escalation routing accuracy**: Sample 20 routed conversations, verify ≥85% correct tier assignment. Pass/fail.

If all PASS, proceed to Scalable. If resolution rate is low, check knowledge pipeline output — are gaps being identified and filled? If CSAT is low, review AI-resolved conversations for incorrect answers. If human volume has not dropped, check whether users are bypassing the chatbot (Messenger placement issue) or the chatbot is escalating too aggressively (adjust confidence thresholds).

## Time Estimate

- 2 hours: remove feature flag, monitor initial 100% rollout
- 4 hours: set up knowledge pipeline n8n workflow, test end-to-end
- 4 hours: build escalation routing workflow with CRM enrichment
- 3 hours: build PostHog dashboard and configure anomaly alerts
- 2 hours: review weekly pipeline output, publish articles
- 1 hour: final evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom (Essential) | Fin AI chatbot + Messenger + team inboxes | $29/seat/mo + $0.99/resolution — [intercom.com/pricing](https://www.intercom.com/pricing) |
| PostHog | Dashboards, funnels, feature flags, anomaly detection | Free up to 1M events/mo; $0.00005/event after — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Haiku) | Knowledge gap classification | ~$1/MTok input, $5/MTok output; ~$5-10/mo for weekly pipeline — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Anthropic API (Sonnet) | Article draft generation + reports | ~$3/MTok input, $15/MTok output; ~$10-20/mo — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Estimated cost for Baseline: ~$100–250/mo** (Intercom $29 base + $100-150 Fin resolutions + $15-30 Anthropic API + PostHog free tier)

## Drills Referenced

- `chatbot-knowledge-pipeline` — weekly detection of knowledge gaps from escalation data, auto-generates draft articles
- the chatbot escalation routing workflow (see instructions below) — priority-based routing with CRM enrichment and context notes for human agents
- `chatbot-resolution-monitor` — PostHog dashboard, anomaly alerts, and weekly health reports
