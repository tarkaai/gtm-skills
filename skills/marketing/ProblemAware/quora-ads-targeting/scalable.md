---
name: quora-ads-targeting-scalable
description: >
  Quora Ads — Scalable. Automated creative rotation, systematic A/B testing of targeting and
  creative, dynamic budget allocation across targeting types, audience expansion with lookalikes,
  and integrated performance dashboards. Target 5x Baseline lead volume without proportional effort.
stage: "Marketing > ProblemAware"
motion: "LightweightPaid"
channels: "Paid, Communities"
level: "Scalable"
time: "60 hours over 3 months"
outcome: ">=200,000 impressions and >=50 qualified leads/month from $4,000-8,000/month budget, with cost per qualified lead below $150 and automated creative rotation running weekly"
kpis: ["Monthly impressions", "Monthly qualified leads", "Cost per qualified lead", "Creative rotation cadence", "Targeting type CPA", "Audience expansion reach", "Budget efficiency trend"]
slug: "quora-ads-targeting"
install: "npx gtm-skills add Marketing/ProblemAware/quora-ads-targeting"
drills:
  - ab-test-orchestrator
  - budget-allocation
  - dashboard-builder
---

# Quora Ads — Scalable

> **Stage:** Marketing > ProblemAware | **Motion:** LightweightPaid | **Channels:** Paid, Communities

## Outcomes

Find the 5-10x multiplier. The agent automates creative rotation, runs systematic A/B tests on targeting and creative, manages budget allocation across targeting types based on performance data, and expands audiences with lookalikes and new topic clusters. The system produces 50+ qualified leads per month from Quora without proportional increase in human time. Quora-specific advantages at scale: question targeting enables hyper-specific placement, topic targeting provides broad reach, and the combination creates a multi-layer funnel within a single platform.

**Pass threshold:** >=200,000 impressions and >=50 qualified leads/month from $4,000-8,000/month budget, with cost per qualified lead below $150, sustained for 3 months.

## Leading Indicators

- Automated creative rotation produces 8+ new ad variants per month
- At least 2 A/B experiments running per month (targeting, creative, bidding, or audience)
- Budget reallocation happens weekly based on targeting type CPA data
- Lookalike audience reaches 50,000+ matched users
- Question targeting inventory expands to 200+ questions across 5+ theme clusters
- Cost per qualified lead is stable or improving month over month
- Creative fatigue detected and resolved automatically (no ad runs for >3 weeks without refresh)

## Instructions

### 1. Scale Creative Production and Rotation

Build an automated creative rotation pipeline:

1. **Analyze Baseline creative data**: Which hook types produced the best CTR? Which ad formats (Image vs Text) converted better? What pain points resonated most?
2. **Build a creative playbook**: Document the 3-5 winning creative templates from Baseline:
   - Template A: "[Statistic] — [Outcome]. Free [asset type]." (Data hook)
   - Template B: "Still [problem]? [Solution approach] in [timeframe]." (Question hook)
   - Template C: "How [X] teams [achieved result]." (Social proof hook)
   - Add new templates based on Baseline learnings
3. **Deploy AI-assisted batch creative production**:
   - Agent generates 5-8 new ad variants every 2 weeks using the creative playbook + rotating ICP pain points
   - Each variant gets both Image Ad and Text Ad versions
   - Headline, body, and image assets are generated programmatically
   - Output as a structured JSON brief for human upload to Ads Manager
4. **Automate the rotation cycle** via n8n workflow (runs every Monday):
   - Pull per-ad CTR and CPC from Quora Ads Manager export
   - Flag ads with CTR declining for 5+ days as fatigued
   - Recommend specific ads for replacement from the new variant queue
   - Send Slack notification with rotation recommendations for human execution
   - No ad should run for more than 3 weeks without refresh

### 2. Deploy Systematic A/B Testing

Run the `ab-test-orchestrator` drill adapted for Quora Ads:

Test one variable at a time with controlled experiments:

**Creative experiments:**
- Test hook types: data vs question vs outcome vs social proof (duplicate ad set, change only the ads)
- Test formats: Image Ad vs Text Ad (same copy, different format)
- Test CTAs: Learn More vs Sign Up vs Download (same ad, different CTA)
- Test offer types: guide vs checklist vs template vs free tool

**Targeting experiments:**
- Test topic breadth: Tier 1 only vs Tier 1+2 (measure CPA difference)
- Test question volume: 50 questions vs 100 questions vs 200 questions per ad set
- Test keyword match: specific keywords vs broad keywords
- Test audience layering: contextual only vs contextual + retargeting combo

**Bidding experiments:**
- Test CPC bid levels: current bid vs +30% vs -30%
- Test Conversion Optimized bidding vs manual CPC (requires 30+ conversions for Quora's algorithm to optimize)
- Test daily budget caps: current vs 2x (measure if scale degrades CPA)

For each experiment:
1. Form hypothesis using the `ab-test-orchestrator` drill framework
2. Calculate sample size (minimum 200 clicks per variant for Quora)
3. Run for 7-14 days
4. Evaluate: adopt winner, iterate, or revert
5. Document results in Attio

Run 2-4 experiments per month. Never stack experiments on the same variable.

### 3. Expand Audiences

**Lookalike audiences:**
1. Export Quora-sourced qualified leads from Attio (minimum 300 emails)
2. Upload as List Match Audience in Quora Ads Manager
3. Create a Lookalike Audience from this list (start with 1-3% similarity)
4. Test lookalike in a new ad set with proven creative
5. Compare lookalike CPA to contextual targeting CPA

**Expand question inventory:**
1. For every high-performing topic, mine 20-50 additional questions
2. Sort by monthly views and commercial intent
3. Create new ad sets for each question theme cluster
4. Test 5 new question clusters per month

**Expand topic coverage:**
1. Add Tier 2 topics (adjacent problems) to new ad sets
2. Add Tier 3 topics (industry-level) if Tier 1+2 are saturated
3. Track CPA at the topic level to determine which tier delivers best results

**Cross-targeting audiences:**
- Create retargeting audiences from Quora engagement (users who clicked but did not convert)
- Layer these on top of new contextual targeting for warmer impressions
- Target users who visited your website from any source with Quora-specific messaging

### 4. Deploy Data-Driven Budget Allocation

Run the `budget-allocation` drill adapted for Quora:

1. **Weekly budget rebalancing** via n8n workflow (runs every Monday):
   - Pull per-ad-set CPA from Quora + PostHog
   - Apply the 70/20/10 framework:
     - 70% to proven targeting types and ad sets (CPA below target)
     - 20% to optimization experiments (A/B tests running)
     - 10% to new audience/targeting tests (lookalikes, new topic clusters)
   - Generate a budget reallocation recommendation
   - Send to Slack for approval

2. **Set automated rebalancing triggers:**
   - If an ad set's CPA exceeds 150% of target for 7 days: reduce budget 30%
   - If an ad set's CPA is below 75% of target for 7 days: increase budget 20%
   - If a new experiment ad set hits target CPA within 14 days: promote to the 70% bucket
   - If daily total spend exceeds 120% of daily budget target: Slack alert

3. **Monthly budget escalation:**
   - If blended CPA is below target, increase monthly budget by 20-30%
   - If blended CPA is at target, maintain current budget
   - If blended CPA exceeds target, reduce budget 10% and consolidate to best-performing ad sets

### 5. Deploy Performance Monitoring

Run the `dashboard-builder` drill:

1. Build the PostHog dashboard (8 panels: spend/reach, click performance, conversion funnel, CPA trend, creative performance, targeting comparison, lead quality, full-funnel attribution)
2. Build Attio saved views (Quora-sourced contacts, Quora pipeline, Quora ROI by targeting type)
3. Deploy the weekly automated report (n8n workflow every Monday)
4. Configure 5 real-time anomaly alerts (CPC spike, conversion rate drop, zero conversions, budget runaway, creative fatigue)
5. Implement question/topic performance tracking log

### 6. Monthly Strategic Review

At the end of each month:

1. Compare actual vs target on all KPIs
2. Review A/B test results: what won, what lost, what was inconclusive
3. Calculate blended CPA across all targeting types and audiences
4. Compare Quora channel CPA to other paid channels (LinkedIn, Google, Reddit)
5. Identify the single biggest lever for next month (audience expansion, creative refresh, budget shift, or new experiment focus)
6. Decide: if metrics are stable and repeatable at volume for 3 consecutive months, proceed to Durable

## Time Estimate

- 12 hours: Creative production system setup (playbook, batch generation, rotation workflow)
- 8 hours: A/B testing framework and first experiments
- 8 hours: Audience expansion (lookalikes, question mining, topic expansion)
- 5 hours: Budget allocation automation
- 5 hours: Performance monitoring dashboard and alerts
- 15 hours: Ongoing management over 3 months (~1.25 hours/week)
- 7 hours: Monthly strategic reviews and creative refresh (3 reviews + ongoing)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Quora Ads | Campaign management and ad delivery | Ad spend ($4,000-8,000/mo) |
| PostHog | Analytics — dashboards, funnels, experiments, anomaly detection | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — lead and deal management, experiment logging | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — lead scoring at scale | $349/mo (Explorer) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Email — nurture sequences at scale | $99/mo (Growth) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Automation — creative rotation, budget allocation, reporting, alerts | $60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | AI — creative generation and experiment evaluation | Usage-based, ~$30-60/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** $4,000-8,000/mo ad spend + ~$600-900/mo tools. Total: $4,600-8,900/mo.

## Drills Referenced

- `ab-test-orchestrator` — systematic A/B testing framework for Quora creative, targeting, bidding, and audience experiments with hypothesis-driven methodology and statistical rigor
- `budget-allocation` — data-driven weekly budget rebalancing across targeting types (topic, question, keyword, retargeting, lookalike) using the 70/20/10 framework
- `dashboard-builder` — PostHog dashboards, Attio views, weekly reports, anomaly alerts, and question/topic performance tracking for continuous campaign visibility
