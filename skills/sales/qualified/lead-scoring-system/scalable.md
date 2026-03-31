---
name: lead-scoring-system-scalable
description: >
  Lead Scoring System — Scalable Automation. Scale to 500+ leads/month with auto-enrichment,
  10+ scoring dimensions, tier-based routing, score decay, and a real-time performance dashboard.
  Target: Hot >=4x Cold conversion over 2 months.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Scalable Automation"
time: "65 hours over 2 months"
outcome: "Hot leads convert at >=4x rate vs Cold leads over 2 months"
kpis: ["Conversion rate by tier", "Score decay impact on pipeline quality", "Time to first contact by tier", "Rep efficiency (meetings per hour of outreach)"]
slug: "lead-scoring-system"
install: "npx gtm-skills add sales/qualified/lead-scoring-system"
drills:
  - lead-routing
  - dashboard-builder
---

# Lead Scoring System — Scalable Automation

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Outcomes

The scoring system processes 500+ leads per month end-to-end without manual intervention. Hot-tier leads convert to meetings at >=4x the rate of Cold-tier leads over 2 months. Tier-based routing ensures Hot leads get contacted within hours and Cold leads are automatically deprioritized. A live dashboard shows scoring model health in real-time.

## Leading Indicators

- New leads scored and routed within 5 minutes of CRM entry
- Hot leads contacted within 4 hours (speed-to-lead metric)
- Score decay correctly removes stale leads from Hot tier (Hot count does not inflate over time)
- Reps report spending >70% of outreach time on Hot/Warm leads (efficiency gain)
- Weekly scoring accuracy remains stable (Hot >=4x Cold conversion)

## Instructions

### 1. Expand the scoring model to 10+ dimensions

Update the lead scoring model built at Baseline. Add new fit and intent dimensions based on Baseline learnings:

**Fit dimensions (max 50 points):**

| Criterion | Condition | Points |
|-----------|-----------|--------|
| Company size | 20-500 employees | +10 |
| Industry | Target industry match | +8 |
| Buyer role | VP+ / Head of / Director | +10 |
| Tech stack | Uses complementary tool | +5 |
| Revenue range | $1M-$50M ARR | +5 |
| Funding stage | Series A-C | +5 |
| Geography | Target market | +3 |
| Hiring velocity | 10%+ headcount growth | +2 |
| Business model | B2B SaaS | +2 |

**Intent dimensions (max 50 points):**

| Signal | Condition | Points |
|--------|-----------|--------|
| Demo form submitted | Any time | +15 |
| Pricing page viewed | Last 14 days (PostHog) | +10 |
| Case study downloaded | Last 14 days (PostHog) | +5 |
| Email replied (positive) | Last 30 days | +8 |
| Repeat website visits | 3+ sessions in 14 days (PostHog) | +4 |
| Funding event | Last 90 days (Clay) | +5 |
| Relevant job postings | 3+ open roles (Clay) | +5 |
| Competitor tool detected | BuiltWith/Wappalyzer (Clay) | +3 |
| Leadership hire | New VP+ in relevant dept (Clay) | +3 |
| Conference engagement | Attended/spoke at relevant event | +2 |

Use the the lead score automation workflow (see instructions below) drill to update the n8n scoring workflows with these expanded criteria.

### 2. Deploy tier-based lead routing

Run the `lead-routing` drill. Build n8n routing workflows based on lead tier:

**Hot leads (score >=80):**
- Auto-assign to the founder or senior rep
- Send immediate Slack alert: "Hot lead: {company} — Score {score}. Fit: {fit_score}/50, Intent: {intent_score}/50."
- Create an Attio task: "Contact {name} at {company} within 4 hours"
- Add to priority outreach queue

**Warm leads (score 50-79):**
- Round-robin assign to available reps
- Add to standard outreach queue with 3-day SLA
- No immediate alert (batched in daily digest)

**Cold leads (score <50):**
- Do not route to reps
- Add to automated nurture sequence (Loops lifecycle email)
- Re-score if they exhibit intent signals later (handled by intent-update workflow from Baseline)

### 3. Implement score decay at scale

Enhance the decay workflow built at Baseline:

- **14-day decay:** If no intent activity for 14 days, reduce intent_score by 50%
- **30-day decay:** If no intent activity for 30 days, reduce intent_score to 0
- **Tier demotion alerts:** When a lead drops from Hot to Warm or Warm to Cold due to decay, fire a `lead_tier_changed` event and update the routing assignment
- **Re-activation:** If a decayed lead shows new intent (website visit, email reply), immediately re-score and potentially promote back to Hot

Run the decay workflow daily at 6 AM via n8n cron.

### 4. Build the scoring performance dashboard

Run the `dashboard-builder` drill. Create a PostHog dashboard named "Lead Scoring — Scalable" with these panels:

**Panel 1: Conversion funnel by tier**
- Funnel: `lead_scored` -> `outreach_sent` -> `meeting_booked` -> `deal_created`
- Breakdown by `lead_tier`
- Time range: last 30 days, compare to previous 30

**Panel 2: Score distribution**
- Histogram of `lead_score` values
- Target: 15-25% Hot, 30-50% Warm, 30-50% Cold

**Panel 3: Speed-to-lead by tier**
- Time from `lead_scored` to `outreach_sent`, broken down by tier
- Target: Hot <4 hours, Warm <3 days

**Panel 4: Score decay impact**
- Count of leads demoted per week due to decay
- Shows whether decay is cleaning stale leads or over-penalizing

**Panel 5: Rep efficiency**
- Meetings booked per hour of outreach, broken down by tier
- Shows whether tier-based routing improves productivity

**Panel 6: Weekly accuracy trend**
- Hot/Cold conversion ratio over time (should stay >=4x)

### 5. Run weekly model calibration

Each week:

1. Query PostHog for meetings booked in the last 7 days, grouped by lead_score at time of scoring
2. Identify which fit and intent criteria contributed most to successful meetings
3. Identify false negatives (Cold leads that converted) and false positives (Hot leads that did not engage)
4. If any single criterion contributes >30% of false positives, reduce its point value
5. If a pattern appears in false negatives that the model does not capture, add a new criterion
6. Re-score all active leads when criteria change (use the model-update workflow from the lead score automation workflow (see instructions below))

### 6. Scale to 500+ leads per month

Increase lead volume:
- Expand Clay enrichment to handle 500+ leads/month (Explorer plan: 120K credits/year)
- Monitor Clay credit usage: ~25 credits per lead for full enrichment = ~12,500 credits/month
- Monitor n8n workflow execution: check for errors, timeouts, and rate limit issues weekly
- Ensure Attio can handle the query volume for routing and scoring (100 req/s API limit)

### 7. Evaluate against threshold

After 2 months, compute:
- Hot tier conversion rate vs Cold tier conversion rate
- **Pass:** Hot >= 4x Cold
- Score decay effectiveness: are stale leads being correctly deprioritized?
- Rep efficiency: has meeting-per-hour improved vs. pre-scoring baseline?

If PASS: proceed to Durable. Document the 10+ dimension model, routing rules, and dashboard configuration.

If FAIL: diagnose whether the issue is model accuracy (wrong criteria), routing latency (Hot leads not contacted fast enough), or volume effects (model that worked at 100 leads breaks at 500). Fix and re-run Scalable for another month.

## Time Estimate

- Model expansion (10+ dimensions): 8 hours
- Routing workflow builds: 10 hours
- Score decay enhancement: 5 hours
- Dashboard build: 8 hours
- Weekly calibration (8 weeks): 16 hours (2 hrs/week)
- Volume scaling and monitoring: 8 hours
- Evaluation: 5 hours
- Buffer for iteration: 5 hours
- Total: ~65 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — scoring fields, routing, task management | Standard stack (excluded) |
| PostHog | Analytics — intent signals, funnels, dashboards | Standard stack (excluded) |
| n8n | Automation — scoring, routing, decay, re-scoring workflows | Standard stack (excluded) |
| Clay | Enrichment — firmographics + intent signals at scale | Explorer: $314/mo for 120K credits/year ([clay.com/pricing](https://www.clay.com/pricing)) |
| Instantly | Cold email — outreach execution at scale | Hypergrowth: $97/mo for 100K emails ([instantly.ai/pricing](https://instantly.ai/pricing)) |

**Play-specific cost: ~$410/mo** (Clay Explorer + Instantly Hypergrowth)

## Drills Referenced

- the lead score automation workflow (see instructions below) — updates scoring workflows for expanded criteria, handles decay and re-scoring at scale
- `lead-routing` — builds tier-based routing with SLAs, auto-assignment, and alerting
- `dashboard-builder` — creates the PostHog dashboard for real-time scoring model health
