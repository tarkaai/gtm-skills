---
name: champion-identification-scalable
description: >
  Champion Identification & Development — Scalable Automation. Scale champion identification across
  all active deals with automated multi-threading, health monitoring, and A/B testing of recruitment
  and enablement approaches. The 10x multiplier is using champions to expand into buying committees,
  turning each champion into 3-5 additional stakeholder relationships.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Scalable Automation"
time: "65 hours over 2 months"
outcome: ">=60% of deals with active champions, >=40% higher win rate for champion deals, and >=3 stakeholders per champion deal over 2 months"
kpis: ["Champion rate across all deals", "Win rate lift (champion vs non-champion)", "Stakeholders per champion deal", "Champion health score trend", "Enablement forward rate"]
slug: "champion-identification"
install: "npx gtm-skills add sales/connected/champion-identification"
drills:
  - champion-health-monitoring
  - champion-multi-thread-expansion
  - ab-test-orchestrator
---

# Champion Identification & Development — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Find the 10x multiplier. At Baseline, each champion is a single contact who might advocate. At Scalable, each champion becomes a bridge into the entire buying committee. Automated health monitoring catches disengagement before deals stall. A/B testing optimizes every touchpoint — recruitment messaging, enablement format, multi-threading approach.

**Pass threshold:** >=60% of deals with active champions, >=40% higher win rate for champion deals, and >=3 stakeholders per champion deal over 2 months.

## Leading Indicators

- Champion health monitoring catches at-risk champions within 48 hours of disengagement
- Multi-thread expansion produces >=3 new stakeholder contacts per champion deal
- A/B tests on recruitment messaging produce a statistically significant winner within 4 weeks
- Champion-introduced stakeholders have >=2x higher meeting acceptance rate than cold outreach
- Deals with multi-threaded champion coverage show >=50% less single-thread risk

## Instructions

### 1. Deploy Champion Health Monitoring

Run the `champion-health-monitoring` drill:
- Build the daily health check n8n workflow that scores all active champions using AI engagement scoring
- Configure alert routing: at-risk alerts to Slack, dark alerts trigger replacement profiling
- Build the PostHog champion health dashboard (6 panels: health distribution, score trend, deals without champions, recruitment funnel, at-risk volume, enablement effectiveness)
- Set up the weekly champion digest

This creates the always-on monitoring layer. Every champion is scored daily, and the founder is alerted the moment engagement drops.

### 2. Launch Multi-Thread Expansion

Run the `champion-multi-thread-expansion` drill for all deals with active champions (score >= 60):

- Map the buying committee for each deal (Economic Buyer, Technical Evaluator, End Users, Legal/Procurement, Executive Sponsor)
- Use Clay to find contacts matching each role at the champion's company
- Generate stakeholder mapping requests for champions to confirm the org chart
- Build role-specific messaging for each stakeholder type
- Execute champion-assisted introductions (preferred) or direct outreach with champion reference (fallback)

Configure the n8n workflow to auto-trigger multi-thread expansion when:
- A champion reaches "Active" status with score >= 60
- A deal moves from Connected to Qualified (ensure multi-threading before deeper engagement)

### 3. A/B Test Everything

Run the `ab-test-orchestrator` drill to set up experiments on the champion program:

**Experiment 1 — Recruitment Messaging (weeks 1-4):**
- Control: Current recruitment email sequence (signal-led)
- Variant A: Lead with peer social proof ("Other {title}s at {industry} companies told us...")
- Variant B: Lead with a provocative question about their pain point
- Measure: Positive reply rate. Minimum 50 sends per variant before declaring winner.

**Experiment 2 — Enablement Format (weeks 3-6):**
- Control: Full kit (email draft + business case + objection responses + talking points)
- Variant A: Loom video only (no documents)
- Variant B: One-page business case only (no video)
- Measure: Forward rate (champion shares materials internally). Minimum 20 champions per variant.

**Experiment 3 — Multi-Thread Approach (weeks 5-8):**
- Control: Champion-assisted introductions (ask champion to forward)
- Variant: Direct outreach with champion reference (don't ask champion, just name-drop)
- Measure: Meeting acceptance rate with new stakeholders. Minimum 30 outreach attempts per variant.

Log all experiment results in PostHog using feature flags. Use the `ab-test-orchestrator` to auto-promote winners and start new experiments.

### 4. Scale Volume

With health monitoring and multi-threading automated, increase throughput:
- Run champion profiling for ALL Connected+ deals, not just new ones
- Backfill champion candidates for deals that have been in pipeline without champions
- Set a target: zero deals should sit in Qualified or Proposed stage with `champion_count` = 0

Increase Instantly sending volume to handle the higher outreach load. Monitor deliverability weekly.

### 5. Build the Feedback Loop

Connect multi-threading outcomes back to champion scoring:
- Champions who successfully introduce >=2 stakeholders: boost score by +20 and set `champion_deal_role` = "Internal Coach"
- Champions who don't respond to multi-threading requests: reduce score by -10 and flag for re-engagement
- Track which champion profiles (title, seniority, department) produce the best multi-thread expansion — feed this back into the profiling scoring model

### 6. Evaluate Against Threshold

After 2 months, measure:
- Champion rate: % of active deals with at least 1 active champion (target >=60%)
- Win rate lift: close rate of champion deals vs non-champion deals (target >=40% improvement)
- Multi-threading depth: average stakeholders per champion deal (target >=3)
- Champion health trend: are average health scores stable or improving?

If all pass: proceed to Durable.
If champion rate or win rate regresses: check if health monitoring is catching problems early enough. Review at-risk alert response times.
If multi-threading depth is low: champions may not be comfortable making introductions. Test the champion-assisted vs direct outreach experiment more aggressively.

## Time Estimate

- 8 hours: Health monitoring setup (n8n workflows, PostHog dashboard, alert routing)
- 10 hours: Multi-thread expansion for initial batch of champion deals
- 8 hours: A/B test design and orchestrator configuration
- 15 hours: Ongoing multi-thread execution (outreach, introductions, follow-ups) over 2 months
- 8 hours: Volume scaling and backfill profiling
- 6 hours: Experiment analysis and scoring model refinement
- 10 hours: Daily monitoring and weekly digest review (30 min/day x 60 days)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — champion tracking, automations, reporting | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — champion profiling + stakeholder search | $185/mo (Launch) or $495/mo (Growth for higher volume) — [clay.com/pricing](https://www.clay.com/pricing) |
| Instantly | Cold email — recruitment + stakeholder outreach | $97/mo (Hypergrowth, 100K emails) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Loom | Video — personalized champion walkthroughs | $12.50/mo (Business) — [loom.com/pricing](https://www.loom.com/pricing) |
| Loops | Email — enablement sequences | Paid tier for higher volume — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Analytics — champion dashboards, A/B testing | Free up to 1M events, then $0.00005/event — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation — health monitoring, multi-thread triggers | $24/mo (Starter) or $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| LinkedIn Sales Navigator | Prospecting — stakeholder identification | $99.99/mo (Core) — [business.linkedin.com/sales-solutions](https://business.linkedin.com/sales-solutions/compare-plans) |

**Estimated play-specific cost this level:** ~$200-500/mo. Primary cost drivers: Clay ($185-495), Instantly ($97), LinkedIn Sales Navigator ($100).

## Drills Referenced

- `champion-health-monitoring` — daily automated health checks with AI engagement scoring, disengagement alerts, and weekly digests
- `champion-multi-thread-expansion` — leverage champions to map buying committees and create multi-threaded deal engagement
- `ab-test-orchestrator` — run controlled experiments on recruitment messaging, enablement format, and multi-threading approach
