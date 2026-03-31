---
name: stakeholder-mapping-scalable
description: >
  Stakeholder Mapping Framework — Scalable Automation. Scale org chart mapping across all deals
  with auto-population, engagement scoring, multi-threading health views, and A/B testing of
  role-specific outreach to find the 10x multiplier for stakeholder coverage.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Social, Email"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: ">=80% of deals have >=4 stakeholders mapped, multi-threaded deals close >=30% faster, and deal health scoring surfaces at-risk deals 2+ weeks before stall"
kpis: ["Stakeholders mapped per deal", "Multi-threading rate", "Deal health score distribution", "Single-threaded risk detection lead time", "Role-specific engagement rate"]
slug: "stakeholder-mapping"
install: "npx gtm-skills add sales/connected/stakeholder-mapping"
drills:
  - stakeholder-org-mapping
  - ab-test-orchestrator
---

# Stakeholder Mapping Framework — Scalable Automation

> **Stage:** Sales > Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Social, Email

## Outcomes

Scale stakeholder mapping to every active deal with zero manual research. Continuously track engagement depth per stakeholder and compute deal-level health scores. Use A/B testing to optimize role-specific outreach. Achieve 80%+ stakeholder coverage, 30%+ velocity improvement from multi-threading, and early warning detection for at-risk deals.

## Leading Indicators

- Automated org chart refresh detects 5+ org changes per week across all accounts (new hires, departures)
- Deal health score accurately predicts deal stalls 2+ weeks before they happen
- A/B tests on role-specific messaging produce statistically significant winners within 4 weeks
- Single-threaded deal alerts reduce the number of deals stalling from champion loss by 50%

## Instructions

### 1. Scale org chart mapping to all active deals

Run the `stakeholder-org-mapping` drill to:

1. Build a persistent Clay table of all companies with active deals in Attio
2. Configure weekly automated "Find People at Company" enrichment across all accounts
3. Set up delta detection: compare each week's results against existing Attio contacts to find new hires and departures
4. Auto-create new stakeholder records in Attio with role classifications
5. Alert deal owners when new stakeholders are discovered at their accounts

Configure the following Attio list views for pipeline reviews:
- **Under-mapped deals**: Deals with fewer than 3 classified stakeholders
- **Missing Economic Buyer**: Deals with no contact tagged as Economic Buyer
- **Single-threaded risk**: Deals with fewer than 2 contacts at engagement level Active or Warm
- **Stale maps**: Deals where the stakeholder map has not been refreshed in 30+ days

### 2. Deploy engagement scoring

Run the the stakeholder engagement scoring workflow (see instructions below) drill to:

1. Define the engagement event taxonomy in PostHog (email opens, replies, meetings, calls, LinkedIn connections, content shares)
2. Build individual engagement scores per stakeholder (rolling 14-day window, point-based system)
3. Compute deal-level multi-threading health scores incorporating engagement depth AND role coverage
4. Create a daily n8n workflow that recalculates scores and writes them to Attio
5. Set up real-time alerts:
   - Single-threaded alert: Deal has only 1 engaged stakeholder and deal value > $10K
   - Champion cooling alert: Champion drops from Active to Cold
   - Economic Buyer dark alert: Economic Buyer silent for 14+ days
   - Blocker activation alert: Blocker becomes Active (may be mobilizing opposition)

Build a PostHog dashboard showing:
- Deal health score distribution (histogram)
- Deals ranked by health score (worst first)
- Multi-threading rate trend over time
- Engagement by stakeholder role (which roles engage most/least)

### 3. A/B test role-specific outreach

Run the `ab-test-orchestrator` drill to experiment on messaging per stakeholder role:

**Experiment 1: Economic Buyer messaging**
- Control: ROI-focused email with industry benchmarks
- Variant: Competitive risk email highlighting what happens if they do not act
- Success metric: Reply rate from contacts tagged Economic Buyer
- Sample size: 50+ per variant

**Experiment 2: Champion enablement**
- Control: Send a product one-pager for internal sharing
- Variant: Send a customized business case template pre-filled with their company data
- Success metric: Champion shares the asset internally (tracked via unique link)
- Sample size: 30+ per variant

**Experiment 3: Blocker engagement**
- Control: Ignore Blockers until they surface objections
- Variant: Proactively email Blockers with a FAQ addressing their typical concerns (security, integration, compliance)
- Success metric: Blocker sentiment moves from Opposed to Neutral
- Sample size: 20+ per variant

**Experiment 4: Multi-threading cadence timing**
- Control: Contact all stakeholders in week 1
- Variant: Contact Champion in week 1, Influencers in week 2, Economic Buyer in week 3 (staged approach)
- Success metric: Deal progression rate by week 4
- Sample size: 20+ deals per variant

Run experiments sequentially. Each test needs 3-4 weeks minimum. Implement winners immediately. Document what worked and why.

### 4. Build title-to-role prediction model

Analyze classification data across all deals to build deterministic rules that reduce AI classification costs:
- Track which titles map to which roles with what accuracy
- Build a rule set: "VP Engineering" → Influencer (87% accuracy across 40 deals)
- Apply rules as a first pass; only use Claude for titles that do not match any rule
- Store the model in Attio as a reference note; update monthly as data accumulates

### 5. Generate weekly stakeholder coverage reports

Configure n8n to produce a weekly report:
```
## Weekly Stakeholder Coverage — {date}

### Pipeline Overview
- Active deals: {count}
- Deals with >=4 stakeholders: {count} ({%})
- Deals with Economic Buyer identified: {count} ({%})
- Average deal health score: {score}/100

### Multi-Threading Impact
- Multi-threaded deals (3+ engaged): Average days to close = {X}
- Single-threaded deals (1-2 engaged): Average days to close = {Y}
- Velocity improvement: {(Y-X)/Y * 100}%

### A/B Test Results
- Active experiments: {list}
- Completed this week: {list with results}
- Recommended changes: {list}

### Action Items
- Under-mapped deals needing research: {list}
- Single-threaded deals needing expansion: {list}
- Champions at risk of cooling: {list}
```

### 6. Evaluate against threshold

After 2 months, measure:
- **>=80% of active deals** have >=4 stakeholders mapped
- **Multi-threaded deals** close **>=30% faster** than single-threaded
- **Deal health scoring** surfaces at-risk deals **2+ weeks** before they stall (validated by comparing alert timing to actual stall dates)

If PASS, proceed to Durable. If FAIL, diagnose: mapping coverage gap (Clay returning insufficient data → add Apollo), engagement gap (stakeholders found but not engaged → improve role-specific messaging), or scoring gap (scores not predictive → recalibrate the scoring model).

## Time Estimate

- Org mapping automation setup: 8 hours
- Engagement scoring build: 10 hours
- A/B test design and launch (4 experiments): 8 hours
- Dashboard and reporting setup: 6 hours
- Weekly monitoring and A/B test evaluation (8 weeks x 1 hour): 8 hours
- Title-to-role model building: 4 hours
- Threshold evaluation: 6 hours

**Total: ~50 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with stakeholder attributes, scoring fields, and list views | Plus at $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Clay | Scaled org chart research with weekly refresh | Growth at $495/mo (40,000 actions) ([clay.com/pricing](https://clay.com/pricing)) |
| n8n | Orchestration: enrichment, scoring, alerts, reporting | Pro at $60/mo or self-hosted free ([n8n.io/pricing](https://n8n.io/pricing)) |
| PostHog | Engagement event tracking, funnels, dashboards, experiments | Free tier or ~$50-100/mo at volume ([posthog.com/pricing](https://posthog.com/pricing)) |
| Instantly | Role-specific email sequences with A/B testing | Growth at $30/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Anthropic | Claude API for classification and summary generation | ~$15-30/mo at scale ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| LinkedIn Sales Navigator | Supplementary research and warm intro identification | Core at $99.99/mo ([business.linkedin.com/sales-solutions](https://business.linkedin.com/sales-solutions/compare-plans)) |

**Estimated monthly cost for this level: $710-850** (Attio $29 + Clay Growth $495 + n8n Pro $60 + PostHog $50-100 + Instantly $30 + Claude API $15-30 + LinkedIn SN $100)

## Drills Referenced

- `stakeholder-org-mapping` — Continuously map org charts across all active deals with weekly refresh, delta detection, and auto-population of new stakeholders
- the stakeholder engagement scoring workflow (see instructions below) — Compute individual and deal-level engagement scores, surface single-threaded risks, and power the multi-threading dashboard
- `ab-test-orchestrator` — Design, run, and analyze A/B tests on role-specific messaging, cadence timing, and engagement strategies
