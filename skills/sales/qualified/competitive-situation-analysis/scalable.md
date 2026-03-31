---
name: competitive-situation-analysis-scalable
description: >
  Competitive Situation Assessment — Scalable Automation. Automated competitor monitoring,
  real-time battlecard delivery triggered by deal events, web behavior competitive triggers,
  and A/B testing of competitive positioning frameworks to maximize win rates.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Scalable Automation"
time: "54 hours over 2 months"
outcome: "Competitive situation assessed on ≥75% of opportunities at scale over 2 months with win rate improvement against top 3 competitors"
kpis: ["Competitive discovery rate at scale", "Win rate by competitor (trending up)", "Positioning framework win rate by competitor", "Battlecard delivery latency (<30 min)", "Competitor change detection rate"]
slug: "competitive-situation-analysis"
install: "npx gtm-skills add sales/qualified/competitive-situation-analysis"
drills:
  - ab-test-orchestrator
  - dashboard-builder
---

# Competitive Situation Assessment — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Competitive intelligence operates as a fully automated system: competitor changes are detected before they appear in deals, battlecards are delivered within 30 minutes of competitor identification, web behavior triggers surface competitive intent, and A/B testing identifies which positioning frameworks produce the highest win rates against each competitor. Win rate against top 3 competitors improves versus the Baseline period.

## Leading Indicators

- Competitor change monitoring detecting real product/pricing changes weekly
- Battlecard delivery latency dropping below 30 minutes consistently
- Web behavior triggers surfacing competitive prospects before the first call
- A/B test sample sizes reaching statistical significance (100+ deals per variant per competitor)
- Positioning framework win rates diverging (some frameworks clearly outperform others)
- Competitive discovery rate holding above 75% at higher deal volume

## Instructions

### 1. Deploy the competitive intelligence automation stack

Run the the competitive intelligence automation workflow (see instructions below) drill to build three automated loops:

**Loop 1 — Competitor change monitoring (n8n weekly cron):**
1. Fetch all tracked competitors from Attio Competitors object
2. Scrape changelog URLs, pricing pages, and feature pages via Clay Claygent
3. Compare content hashes against stored values — detect changes
4. Classify changes via Claude: `change_type`, `competitive_impact` (1-5), `positioning_affected`
5. Route by impact: low → log silently, medium → Slack alert + battlecard update, high → urgent strategy review task
6. Fire `competitor_change_detected` event in PostHog

**Loop 2 — Real-time battlecard delivery (Attio webhook trigger):**
1. When `competitors_evaluated` field is updated on any deal, trigger the workflow
2. Fetch battlecards for each named competitor
3. Generate tailored positioning via `competitive-positioning-generation` using deal-specific context (pains, criteria, champion, industry)
4. Deliver to deal owner via Slack DM with summary, positioning response, trap questions, and relevant won case studies
5. Fire `battlecard_delivered` event

**Loop 3 — Web behavior competitive trigger (PostHog webhook):**
1. When a known prospect visits a competitor comparison page or pricing page, trigger the workflow
2. Match the visitor to an Attio contact/deal
3. Generate contextual positioning content (does not reveal page visit knowledge)
4. Alert the deal owner with context and suggested response
5. Fire `competitive_page_trigger` event

### 2. Launch competitive positioning A/B tests

Run the `ab-test-orchestrator` drill to test positioning effectiveness against each top competitor:

**What to test:**
- Positioning framework variants: `pain_alignment` vs `capability_gap` vs `tco_comparison` vs `customer_proof` against Competitor A
- Trap question sets: which questions best surface competitive gaps
- Follow-up email variants: different competitive positioning angles
- Battlecard format: detailed vs summary — which format produces higher win rates

**How to test:**
1. Use PostHog feature flags to randomly assign deals to positioning variants when a specific competitor is detected
2. The `competitive-positioning-generation` fundamental accepts a `positioning_framework` parameter — set it based on the assigned variant
3. Track the funnel: `competitive_positioning_generated` (variant A or B) → `deal_won` or `deal_lost`
4. Minimum sample: 50 deals per variant per competitor before declaring a winner (or 100 for high confidence)
5. When a winner is declared, promote it as the default framework for that competitor and start the next test

### 3. Build the competitive intelligence dashboard

Create a PostHog dashboard with these panels (as defined in the the competitive intelligence automation workflow (see instructions below) drill):

| Panel | Query | Purpose |
|-------|-------|---------|
| Competitor frequency (30d) | Count `competitor_named` by `competitor_name` | Which competitors appear most |
| Win rate by competitor | `deal_won` / total closed where `competitor_name` = X | Competitive health scorecard |
| Competitive risk distribution | Count open deals grouped by `competitive_risk` | Pipeline risk at a glance |
| Battlecard delivery rate | `battlecard_delivered` / `competitive_situation_extracted` | Intel adoption metric |
| Battlecard delivery latency | P50 and P90 time between extraction and delivery | Speed metric |
| Positioning framework win rates | Win rate grouped by `positioning_framework` per competitor | A/B test results |
| Competitor change velocity | Count `competitor_change_detected` by week | Market movement speed |
| Discovery quality trend | Average `seller_discovery_quality` by week | Team skill improvement |

### 4. Generate monthly competitive reports

Run the `dashboard-builder` drill on a monthly cron (first Monday of each month):

1. Aggregate all competitive deal outcomes from the past 30 days
2. Calculate per-competitor metrics: win rate, deal count, avg deal value, velocity, battlecard lift
3. Run pattern analysis: when do we win? when do we lose? which positioning works?
4. Identify emerging threats: new competitors appearing, existing competitors improving
5. Generate actionable recommendations grounded in data
6. Distribute to Slack and store in Attio

### 5. Set guardrails and evaluate

Configure guardrail alerts (from the the competitive intelligence automation workflow (see instructions below) drill):
- **New competitor spike:** 3+ mentions in one week without a battlecard → alert to build one
- **Win rate drop:** Win rate against any competitor drops below 35% over 4 weeks → strategy review
- **Discovery gap:** Competitive discovery rate drops below 60% for 2 weeks → process alert
- **Stale battlecard:** Competitor record not updated in 30+ days with 5+ mentions → refresh

**Evaluate against threshold after 2 months:**
- Competitive situation assessed on ≥75% of opportunities at scale
- Win rate against top 3 competitors improved vs Baseline period
- Battlecard delivery latency ≤30 minutes (P90)
- At least 1 A/B test completed with statistically significant winner

If PASS: the competitive intelligence system operates at scale and demonstrably improves win rates. Proceed to Durable.

If FAIL: diagnose:
- Discovery rate dropping at scale: automation missing calls (check n8n webhook reliability) or new reps not asking competitive questions (training gap)
- Win rate not improving: positioning frameworks may need different approaches. Run more A/B tests targeting the lowest-performing competitor matchup.
- Battlecard delivery slow: API rate limits or n8n queue depth. Scale n8n workers or batch less aggressively.

## Time Estimate

- 12 hours: Build and test 3 automation loops (4 hours each)
- 6 hours: Configure A/B testing framework and first round of experiments
- 4 hours: Build PostHog dashboard
- 4 hours: Set up monthly reporting and guardrail alerts
- 20 hours: Monitor, iterate, and run A/B tests over 2 months (2.5 hours/week)
- 8 hours: Analyze results, compile learnings, threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies | Call transcription (always-on) | Pro $10/user/mo annual — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Anthropic Claude API | Extraction + positioning + change analysis | ~$50-100/mo at scale — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Attio | CRM: deals + Competitors object + automation webhooks | Included in standard stack — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Events + funnels + feature flags + dashboards | Free tier or Growth $0.00045/event — [posthog.com/pricing](https://posthog.com/pricing) |
| Clay | Competitor enrichment + changelog scraping | Launch $185/mo or Growth $495/mo — [clay.com/pricing](https://www.clay.com/pricing) |
| n8n | Workflow automation (3 loops + crons) | Self-hosted free or Cloud from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost:** ~$200-500/mo (Clay enrichment + Claude API at scale are the main drivers)

## Drills Referenced

- the competitive intelligence automation workflow (see instructions below) — the three automated loops: competitor monitoring, battlecard delivery, web behavior triggers
- `ab-test-orchestrator` — A/B testing competitive positioning frameworks
- `dashboard-builder` — monthly competitive reports with per-competitor scorecards
