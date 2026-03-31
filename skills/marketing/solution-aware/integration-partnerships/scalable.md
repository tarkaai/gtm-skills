---
name: integration-partnerships-scalable
description: >
  Integration Partnerships — Scalable Automation. Automate partner pipeline management, build 10+
  integrations with co-marketing, and use Crossbeam for account-level overlap targeting.
stage: "Marketing > SolutionAware"
motion: "PartnershipsWarmIntros"
channels: "Product, Content, Email"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥10 active integrations and ≥60 qualified leads/quarter over 6 months"
kpis: ["Active integration count", "Partner-sourced leads per quarter", "Integration activation rate", "Cost per partner-sourced lead", "Partner pipeline velocity"]
slug: "integration-partnerships"
install: "npx gtm-skills add marketing/solution-aware/integration-partnerships"
drills:
  - partner-pipeline-automation
  - dashboard-builder
---

# Integration Partnerships — Scalable Automation

> **Stage:** Marketing → SolutionAware | **Motion:** PartnershipsWarmIntros | **Channels:** Product, Content, Email

## Outcomes

Ten or more active product integrations with co-marketing in place, generating 60+ qualified leads per quarter sustained over 6 months. Partner pipeline management is automated: outreach sequences, launch coordination, lead attribution, and health monitoring run without manual intervention.

## Leading Indicators

- Partner pipeline always has ≥5 prospects, ≥3 in conversation, and ≥2 building at any time
- Integration activation rate stays within 20% of Baseline benchmark (≥15%)
- Crossbeam overlap data shows ≥500 shared accounts across active partners
- Partner-sourced leads convert to meetings at ≥ the rate of other marketing channels
- Monthly partner-sourced lead volume is growing or stable (not declining)

## Instructions

### 1. Automate the partner pipeline

Run the `partner-pipeline-automation` drill to build n8n workflows that manage the integration partner lifecycle:

- **Partner outreach automation**: When a new partner is added to the "Integration Partners" list in Attio with status "Prospect," auto-send a personalized outreach email via Instantly. Reference the specific integration opportunity identified during discovery. Follow up once after 5 days. Update Attio status on reply.
- **Launch coordination workflow**: When a partner moves to "Building" status in Attio, trigger a checklist: generate co-marketing assets (run the integration launch campaign workflow (see instructions below) drill), set launch date reminder, confirm partner distribution commitment, send partner their tracked URLs.
- **Lead attribution workflow**: When PostHog fires an `integration_lead_captured` event with a partner UTM source, auto-create a lead in Attio linked to the partner deal, increment the partner's lead counter, and notify the team.
- **Partner nurture sequence**: After each integration launch, auto-send the partner a 7-day performance report, a 14-day full retrospective, and a 30-day partnership summary with a proposal for the next co-marketing push.

### 2. Scale with Crossbeam account mapping

If not already configured, set up Crossbeam and connect your Attio CRM data. For each active and prospective integration partner, run account overlap reports. Prioritize:

- Partners with ≥100 overlapping target accounts (their customers are your prospects)
- Partners where overlap accounts are in active deal stages (warm leads who already use the partner product)
- Partners whose overlap is growing (their user base is expanding into your ICP)

Use overlap data to prioritize which integrations to build next. An integration with a partner who shares 500 target accounts is more valuable than one with 50.

### 3. Launch integrations at cadence

Run the the integration launch campaign workflow (see instructions below) drill for each new integration. Target 2-3 new integration launches per month. Standardize the process:

1. Week 1: Build the integration (use existing patterns from Baseline — most integrations should be Light or Medium complexity by now)
2. Week 2: Generate co-marketing assets and coordinate with partner
3. Week 3: Launch (your email + partner email + both blogs + social)
4. Weeks 4-5: Monitor 14-day performance, send partner the retrospective

Create integration templates for common patterns (webhook sync, API pull, n8n connector) to reduce build time from days to hours.

### 4. Monitor portfolio health

Run the `dashboard-builder` drill to build dashboards and weekly briefs covering:

- Per-partner lead attribution and conversion rates
- Integration activation and usage retention
- Partner distribution effectiveness (which partners actually send to their audience)
- Dormant integrations (built but generating zero leads — investigate or sunset)
- Pipeline forecast (based on partner pipeline velocity, how many leads will partners generate next quarter)

Set guardrails: if total partner-sourced leads drop >20% below the Baseline benchmark for 2 consecutive weeks, investigate root causes before continuing to add new partners.

### 5. Evaluate against threshold

Measure against: ≥10 active integrations with co-marketing AND ≥60 qualified leads/quarter sustained over 6 months. If PASS, proceed to Durable. If FAIL, consolidate: focus on the top 5 highest-performing partners, deepen co-marketing with them, and sunset integrations with zero lead generation.

## Time Estimate

- Partner pipeline automation setup: 8 hours (one-time)
- Crossbeam configuration: 4 hours (one-time)
- Integration builds (2-3/month x 3 months): 30 hours
- Co-marketing launches (2-3/month x 3 months): 15 hours
- Monitoring, reporting, optimization: 18 hours (6/month x 3 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Crossbeam | Partner account overlap mapping | Free tier available; Growth: $0-200/mo (https://www.crossbeam.com/pricing) |
| n8n | Partner pipeline automation workflows | Free (self-hosted); Cloud: $24/mo (https://n8n.io/pricing) |
| Attio | CRM for partner pipeline and lead attribution | Plus: $29/user/mo (https://attio.com/pricing) |
| PostHog | Integration tracking, dashboards, alerts | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Loops | Partner co-marketing email sends | Starter: $49/mo (https://loops.so/pricing) |
| Instantly | Partner outreach automation | Growth: $30/mo (https://instantly.ai/pricing) |

## Drills Referenced

- `partner-pipeline-automation` — automate partner outreach, launch coordination, lead attribution, and nurture sequences via n8n
- `dashboard-builder` — dashboards, weekly briefs, per-partner ROI, and performance alerts
- the integration launch campaign workflow (see instructions below) — execute co-marketing launch for each new integration
