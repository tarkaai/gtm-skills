---
name: paid-social-ads-durable
description: >
  Paid Social Ads — Durable Intelligence. AI agent autonomously manages paid social campaigns:
  detects creative fatigue, generates new variants, rebalances budgets, refreshes audiences,
  and produces weekly performance reports. Sustains or improves on Scalable-level lead volume
  for 6+ months without increasing manual effort.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "≥ 15 leads/month for 6 consecutive months with CPL within 15% of Scalable baseline; agent generates weekly reports and creative variants with ≤ 2 hours/week human oversight"
kpis: ["Monthly lead volume trend", "CPL trend (rolling 30-day)", "Lead-to-meeting conversion rate", "Blended ROAS", "Creative win rate (% of new variants that beat control)", "Audience refresh frequency", "Agent intervention count (lower is better)"]
slug: "paid-social-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-social-ads"
drills:
  - autonomous-optimization
  - dashboard-builder
  - ab-test-orchestrator
  - paid-social-audience-builder
  - budget-allocation
  - threshold-engine
---

# Paid Social Ads — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Outcomes

The agent manages the entire paid social operation autonomously. Over 6 months, lead volume and CPL stay within 15% of Scalable-level performance (or improve). The agent detects problems before they become crises (creative fatigue, audience saturation, CPL spikes), generates fixes, implements them, and reports results weekly. A human reviews the weekly report and approves any strategic changes (new audiences, budget increases above thresholds, new pain point messaging).

This is not "set it and forget it." This is an AI agent actively running experiments, learning what works, and adapting — the equivalent of a junior paid media manager who never sleeps, never forgets to check metrics, and documents every decision.

## Leading Indicators

- Weekly report generated on time every Monday (agent is running)
- At least 3 new creative variants tested per 2-week cycle (creative pipeline is not stalled)
- Creative win rate above 20% (1 in 5 new variants beats the current control — proves the agent is generating useful variations, not random noise)
- No campaign runs for more than 4 weeks without creative refresh (fatigue prevention is working)
- CPL does not exceed Scalable baseline by more than 15% for more than 2 consecutive weeks (agent catches and fixes degradation)
- Audience overlap between active segments stays below 30% (audiences are distinct)

## Instructions

### 1. Build the paid social performance dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard with these panels:

**Top row — headline metrics (last 30 days vs. previous 30 days):**
- Total leads from paid social
- Blended CPL
- Total meetings booked from paid social leads
- Total ad spend

**Middle row — trend charts (last 90 days, weekly granularity):**
- Leads per week (line chart with Scalable baseline as a reference line)
- CPL per week by platform (LinkedIn vs. Meta)
- Lead-to-meeting conversion rate per week
- Ad spend per week with budget cap overlay

**Bottom row — breakdowns:**
- CPL by audience segment (table, sortable)
- Top 5 performing ad variants (by CPL, with CTR and lead count)
- Bottom 5 performing ad variants (candidates for pausing)
- Creative age distribution: how many active variants are <1 week, 1-2 weeks, 2-4 weeks, >4 weeks old

**Alerts:**
- CPL exceeds Scalable baseline by 15% for 3 consecutive days
- Any campaign's daily spend exceeds budget by 20%
- Creative refresh overdue: no new variants launched in 14+ days
- Lead routing failure: n8n workflow error count > 0 in last 24 hours

### 2. Build the autonomous creative management agent

Create an n8n workflow that runs every Monday:

**Creative fatigue detection:**
1. For each active variant, pull last 7 days of impressions and CTR from the ad platform API
2. Compare to that variant's first-week CTR
3. If CTR has declined 30%+ from first-week average AND the variant has been running 10+ days, flag it as "fatigued"
4. Pause fatigued variants via the platform API

**Creative generation:**
1. Identify the current top 3 performing variants (lowest CPL with 500+ impressions)
2. Extract their pattern: which pain point, hook type, and offer format are they using
3. Use the Anthropic API to generate 5 new variants inspired by the winning pattern:
   - 3 variations on the winning angle (same pain point, different specific stats/questions/proof)
   - 2 experimental variants (different pain point or hook type to prevent tunnel vision)
4. Output the new variant copy as a structured payload: headline, body, CTA, target platform

**Human action required:** Review the 5 generated variants weekly. Approve, edit, or reject each. The agent creates the ads in draft/paused status; a human activates them after review. Over time, as the agent's creative quality proves reliable, the human can batch-approve without detailed review.

### 3. Build the autonomous budget management agent

Create an n8n workflow that runs daily:

**Daily budget check:**
1. Pull yesterday's spend and lead count per campaign from LinkedIn and Meta APIs
2. Calculate yesterday's CPL per campaign
3. Compare to the rolling 7-day average CPL

**Automated actions:**
- If a campaign's CPL exceeds 2x target for 3 consecutive days: reduce daily budget by 30%
- If a campaign's CPL is below 75% of target for 7 consecutive days: increase daily budget by 15% (up to the per-campaign ceiling)
- If total daily spend across all campaigns exceeds the monthly budget / 30 by more than 15%: reduce all campaigns proportionally to get back on pace
- Log every adjustment in PostHog: `paid_social_budget_auto_adjusted` with reason, campaign, old budget, new budget

**Weekly budget review (Monday workflow):**
1. Calculate last week's blended CPL vs. target
2. Calculate budget utilization (actual spend vs. planned)
3. Recommend next week's total budget: increase if CPL is below target, hold if at target, decrease if above target
4. Include the recommendation in the weekly report for human approval

### 4. Build the autonomous audience management agent

Create an n8n workflow that runs every 2 weeks:

**Audience health check:**
1. For each active audience segment, pull: reach (% of audience shown ads), frequency (average impressions per person), and CPL trend
2. If frequency > 4 and CPL is rising: flag as "saturated"
3. If reach > 80% of estimated audience size: flag as "exhausted"

**Audience refresh:**
1. For saturated audiences: create a variant of the audience with tighter or shifted criteria (e.g., if "VP Engineering at 20-200 person SaaS companies" is saturated, try "Director Engineering at 50-500 person SaaS companies")
2. For exhausted audiences: retire and replace with a new segment from the `paid-social-audience-builder` drill
3. Refresh exclusion lists: re-export current customers and recent converters from Attio, upload to both platforms

**Lookalike refresh (monthly):**
1. Re-export your best customers (closed-won in the last 90 days) from Attio
2. Upload to Meta as a new source audience
3. Create fresh 1% and 3% lookalikes
4. The newest lookalike should reflect your most recent customer profile, which may have shifted

### 5. Generate weekly performance report

Create an n8n workflow that runs every Monday at 8am and sends a structured report:

```
PAID SOCIAL WEEKLY REPORT — Week of [date]

HEADLINE
- Leads this week: [X] (vs. [Y] last week, [Z] Scalable baseline)
- Blended CPL: $[X] (vs. $[Y] last week, $[Z] target)
- Meetings booked from paid social leads: [X]
- Total spend: $[X] (vs. $[Y] budget)

WHAT WORKED
- Top variant: "[headline]" on [platform] — [X] leads at $[Y] CPL
- Best audience: [segment name] — [X] leads at $[Y] CPL

WHAT DIDN'T
- Paused [X] fatigued variants (list them)
- Audience [name] flagged as saturated (frequency [X])

CHANGES MADE
- Budget adjustments: [list any automated budget changes]
- New variants drafted: [list 5 new variants pending approval]
- Audience changes: [any segments retired or created]

RECOMMENDATION
- [One specific recommendation: e.g., "Increase budget by 15% — CPL has been 20% below target for 3 weeks"]
```

Send to Slack and/or email. The human reviews weekly and acts on recommendations.

### 6. Run monthly strategic review

Once per month, the agent generates a deeper analysis:

**Full-funnel attribution:**
- Trace paid social leads through the entire pipeline: lead -> meeting -> qualified -> deal -> closed-won
- Calculate true ROAS: ad spend vs. revenue from paid-social-sourced deals
- Compare channel performance: paid social vs. organic vs. outreach vs. referral

**Experiment retrospective:**
- How many creative variants were tested this month? How many won?
- Which pain points and hook types drove the best results?
- What is the creative "hit rate" trending? (Should improve over time as the agent learns)

**Market adaptation:**
- Is CPL trending up across the market (seasonal/macro) or just for us?
- Are new competitors bidding on the same audiences?
- Should we test a new platform, offer format, or audience angle?

**Human action required:** Review the monthly report. Make strategic decisions: change budget range, approve new pain points for creative, approve new audience segments, or decide to add/remove a platform.

### 7. Evaluate sustainability

Run the `threshold-engine` drill monthly. The durable threshold is:

**≥ 15 leads/month for 6 consecutive months with CPL within 15% of Scalable baseline; agent generates weekly reports and creative variants with ≤ 2 hours/week human oversight.**

Monthly check:
- Is lead volume ≥ 15/month? (PASS/FAIL)
- Is CPL within 15% of Scalable CPL? (PASS/FAIL)
- Did the agent generate a weekly report every week this month? (PASS/FAIL)
- Did the agent produce and test new creative variants every 2 weeks? (PASS/FAIL)
- Was human oversight ≤ 2 hours/week on average? (PASS/FAIL)

All 5 must pass for the month to count. 6 consecutive passing months = Durable achieved.

If any metric degrades for 2 consecutive months:
1. Agent diagnoses: is it creative fatigue, audience saturation, market shift, or budget constraint?
2. Agent proposes a recovery plan (e.g., "test 3 entirely new pain points", "expand to TikTok Ads", "increase budget to reach new audience segments")
3. Human approves and the agent executes

## Time Estimate

**One-time setup (month 1): ~40 hours**
- 12 hours: Dashboard build and alert configuration
- 10 hours: Autonomous creative management workflow
- 8 hours: Autonomous budget management workflow
- 6 hours: Autonomous audience management workflow
- 4 hours: Weekly report template and workflow

**Ongoing (months 2-6): ~32 hours/month**
- 2 hours/week: Human review of weekly report and creative approval (8 hrs/month)
- 4 hours/month: Monthly strategic review
- 4 hours/month: Agent maintenance (fix n8n workflow issues, update API integrations)
- 16 hours/month: Agent compute time (automated workflows running)

Total: ~200 hours over 6 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Ads | B2B targeting and lead gen | $5,000-20,000/mo ad spend. [Pricing](https://business.linkedin.com/marketing-solutions/ads/pricing) |
| Meta Ads | Retargeting, lookalikes | Included in above budget. [Pricing](https://www.facebook.com/business/ads/pricing) |
| Clay | Lead enrichment and scoring | $495/mo Growth plan (CRM sync needed at this volume). [Pricing](https://clay.com/pricing) |
| Loops | Nurture sequences at scale | $49-99/mo depending on contact volume. [Pricing](https://loops.so/pricing) |
| PostHog | Dashboards, experiments, events | Free up to 1M events/mo, then pay-as-you-go. [Pricing](https://posthog.com/pricing) |
| n8n | All automation (creative management, budget, audience, reporting) | Free self-hosted or $20-50/mo cloud. [Pricing](https://n8n.io/pricing) |
| Anthropic API | Creative variant generation | ~$0.50-2.00 per batch of 5 variants (Claude Sonnet). [Pricing](https://www.anthropic.com/pricing) |
| Webflow | Landing pages | $23/mo CMS plan. [Pricing](https://webflow.com/pricing) |

**Estimated durable monthly cost:** $5,000-20,000 ad spend + ~$600-900 tooling = $5,600-20,900/mo

## Drills Referenced

- `dashboard-builder` — build the paid social performance dashboard with alerts
- `ab-test-orchestrator` — structured creative testing integrated into the autonomous workflow
- the paid social creative pipeline workflow (see instructions below) — AI-assisted creative generation on a bi-weekly cadence
- `paid-social-audience-builder` — audience refresh and expansion managed by the agent
- `budget-allocation` — automated daily budget adjustments with guardrails
- `threshold-engine` — monthly sustainability evaluation against Scalable baseline
