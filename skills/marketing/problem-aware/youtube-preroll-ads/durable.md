---
name: youtube-preroll-ads-durable
description: >
  YouTube Pre-roll Ads — Durable Intelligence. AI agent autonomously manages YouTube
  pre-roll campaigns: detects creative fatigue, discovers new placements, generates
  video briefs, rebalances budgets, refreshes audiences, runs optimization experiments,
  and produces weekly performance reports. Sustains ≥ 45 qualified leads/month for
  12 months via AI-optimized creative testing with ≤ 3 hours/week human oversight.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid, Content"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "≥ 45 qualified leads/month for 12 consecutive months with CPqL within 15% of Scalable baseline; agent generates weekly reports and creative briefs with ≤ 3 hours/week human oversight"
kpis: ["Monthly qualified lead volume trend", "CPqL trend (rolling 30-day)", "Lead-to-meeting conversion rate", "Blended ROAS from YouTube-sourced pipeline", "Creative win rate (% of new variants that beat control)", "Placement discovery rate", "Experiment velocity (experiments completed per month)", "Agent intervention count (lower is better)"]
slug: "youtube-preroll-ads"
install: "npx gtm-skills add marketing/problem-aware/youtube-preroll-ads"
drills:
  - autonomous-optimization
  - youtube-preroll-audience-builder
  - dashboard-builder
  - budget-allocation
  - threshold-engine
---

# YouTube Pre-roll Ads — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Content

## Outcomes

The agent manages the entire YouTube pre-roll operation autonomously. Over 12 months, qualified lead volume stays at or above 45/month and CPqL stays within 15% of Scalable-level performance (or improves). The agent detects problems before they become costly (creative fatigue, audience saturation, CPqL spikes, placement quality degradation), generates fixes, implements them, and reports results weekly. A human reviews the weekly report, produces videos from agent-generated briefs, and approves strategic changes (new pain points, budget increases above thresholds, new audience strategies).

This is not "set it and forget it." This is an AI agent actively running the detect-diagnose-experiment-evaluate-implement loop from `autonomous-optimization`, applied specifically to YouTube pre-roll campaigns.

## Leading Indicators

- Weekly report generated on time every Monday (agent is running)
- At least 3 new video creative briefs generated per 2-week cycle (creative pipeline is not stalled)
- Creative win rate above 20% (1 in 5 new variants beats the current control)
- No variant runs for more than 4 weeks without refresh (fatigue prevention is working)
- CPqL does not exceed Scalable baseline by more than 15% for more than 2 consecutive weeks (agent catches and fixes degradation)
- New placements discovered and tested monthly (audience is expanding, not saturating)
- Experiment velocity: 2-4 experiments completed per month (optimization loop is active)

## Instructions

### 1. Build the YouTube pre-roll performance dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard:

**Top row — headline metrics (last 30 days vs. previous 30 days):**
- Total qualified leads from YouTube pre-roll
- Blended CPqL
- Total meetings booked from YouTube pre-roll leads
- Total ad spend
- View rate (VTR)

**Middle row — trend charts (last 90 days, weekly granularity):**
- Qualified leads per week (line chart with Scalable baseline as reference)
- CPqL per week by campaign type (placements vs. custom intent vs. topics)
- VTR per week (creative health indicator)
- Lead-to-meeting conversion rate per week
- Ad spend per week with budget cap overlay

**Bottom row — breakdowns:**
- CPqL by pain point (table, sortable)
- Top 5 performing video variants (by CPqL, with VTR and lead count)
- Bottom 5 performing variants (candidates for pausing)
- Creative age distribution: active variants by age bucket (<1 week, 1-2 weeks, 2-4 weeks, >4 weeks)
- Placement performance: top 10 channels by conversions, bottom 10 by cost/conversion

**Alerts:**
- CPqL exceeds Scalable baseline by 15% for 3 consecutive days
- Any campaign's daily spend exceeds budget by 20%
- Creative refresh overdue: no new variants launched in 14+ days
- Lead routing failure: n8n workflow error count > 0 in last 24 hours
- VTR drops below 12% for any campaign for 3 consecutive days

### 2. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for YouTube pre-roll. This is the core of Durable — the always-on agent loop that finds and maintains the local maximum.

**Configure the optimization targets:**
- Primary KPI: Cost per qualified lead (CPqL)
- Secondary KPIs: View rate (VTR), lead-to-meeting conversion rate
- Anomaly thresholds: within 10% of 4-week rolling average = normal, within 2% for 3+ weeks = plateau, >20% decline = drop

**Configure the experiment types the agent can run:**

1. **Creative experiments:** Test a new video variant against the current best performer. Agent generates the brief, human produces the video, agent configures the experiment.
   - Hypothesis example: "Stat hook with a 2026-specific data point will outperform the current stat hook by 15% on VTR because the existing stat is 6 months old."
   - Implementation: create new ad variant in PAUSED status, activate alongside control, split traffic evenly via ad rotation.

2. **Audience experiments:** Test a new placement set, custom intent segment, or targeting combination against the current best audience.
   - Hypothesis example: "Adding DevOps-focused channels will produce 20% lower CPqL than the current placement mix because our ICP's problem is infrastructure-related."
   - Implementation: create a new ad group with the experimental audience, same creative as control.

3. **Budget experiments:** Test different budget allocations across campaign types.
   - Hypothesis example: "Shifting 20% of topic targeting budget to custom intent will reduce blended CPqL by 10% because custom intent produces higher-quality leads."
   - Implementation: adjust daily budgets via API.

4. **Landing page experiments:** Test different landing page variants (headline, offer, form length).
   - Hypothesis example: "A shorter form (email only) will increase form submission rate by 30% but decrease ICP match rate by 10%, producing a net improvement in CPqL."
   - Implementation: create a variant landing page, split traffic via UTM params.

**Guardrails (from autonomous-optimization):**
- Maximum 1 active experiment per campaign at a time
- If primary KPI drops >30% during an experiment, auto-revert immediately
- Human approval required for: budget changes >20%, new pain points, any experiment the agent flags as "high risk"
- Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.

### 3. Build the autonomous creative management agent

Extend the the youtube preroll creative pipeline workflow (see instructions below) for autonomous operation:

**Creative fatigue detection (from `autonomous-optimization`, runs daily):**
1. For each active variant, compare last 7-day VTR to first-week VTR
2. If VTR declined 30%+ and variant has been running 14+ days: flag as fatigued, pause via API

**Creative generation (runs every 2 weeks, Monday):**
1. Identify the current top 3 performing variants (lowest CPqL with 5,000+ impressions)
2. Extract their pattern: pain point, hook type, video length, CTA type
3. Use the Anthropic API to generate 5 new creative briefs:
   - 3 variations on the winning angle (same pain point, different supporting data or angle)
   - 2 experimental variants (different pain point or hook type to prevent tunnel vision)
4. Output structured briefs: script, on-screen text, companion banner copy, UTM params

**Human action required:** Produce the videos from the briefs every 2 weeks. Review takes 30 minutes (read briefs, flag any that feel off-brand). Production takes 1-2 hours (batch record 5 videos). Total: ~2 hours bi-weekly.

### 4. Build the autonomous audience management agent

Extend the `youtube-preroll-audience-builder` for autonomous operation:

**Placement health check (bi-weekly):**
1. For each placement campaign, pull per-channel performance from Google Ads
2. Identify channels with 1,000+ impressions but zero conversions: add to negative placement list
3. Identify channels with CPqL 50%+ below average: flag as "high value" for budget increase

**Automated placement discovery (weekly):**
1. YouTube Data API search for new videos matching pain point keywords (published last 7 days, 10K+ views)
2. Extract channel IDs, filter by subscriber count and relevance
3. Cross-reference against existing placement list
4. Add new qualifying channels to the placement targeting (auto-add to ad groups)
5. Log discoveries in Attio: `yt_preroll_placement_discovered` with channel name, subscribers, topic

**Custom intent refresh (monthly):**
1. Pull top-performing search terms from Google Ads search term reports (people who saw your ad after searching)
2. Identify new search terms with high VTR and conversion rate
3. Add them to existing custom intent segments
4. Remove terms with 500+ impressions but zero conversions

**Audience saturation check (bi-weekly):**
1. For each campaign type, check frequency (impressions / unique reach)
2. If frequency > 4 and CPqL is rising: flag as saturated
3. For saturated audiences: expand placement list, add new custom intent terms, or shift budget to less-saturated campaign types

### 5. Build the autonomous budget management agent

Create an n8n workflow that runs daily:

**Daily budget check:**
1. Pull yesterday's spend and lead data per campaign from Google Ads
2. Calculate yesterday's CPqL per campaign
3. Compare to the rolling 7-day average CPqL

**Automated actions:**
- Campaign CPqL exceeds 2x target for 3 consecutive days: reduce daily budget by 30%
- Campaign CPqL is below 75% of target for 7 consecutive days: increase daily budget by 15% (up to per-campaign ceiling)
- Total daily spend exceeds monthly budget / 30 by more than 15%: reduce all campaigns proportionally
- Log every adjustment in PostHog: `yt_preroll_budget_auto_adjusted` with reason, campaign, old budget, new budget

**Weekly budget review (Monday workflow):**
1. Calculate last week's blended CPqL vs. target
2. Calculate budget utilization
3. Recommend next week's total budget: increase if CPqL is below target, hold if at target, decrease if above
4. Include the recommendation in the weekly report for human approval

### 6. Generate weekly performance report

Extend the `autonomous-optimization` weekly report for Durable:

```
YOUTUBE PRE-ROLL WEEKLY REPORT — Week of [date]

HEADLINE
- Qualified leads this week: [X] (vs [Y] last week, [Z] Scalable baseline)
- Blended CPqL: $[X] (vs $[Y] last week, $[Z] target)
- Meetings booked from YT preroll leads: [X]
- Total spend: $[X] (vs $[Y] budget)
- VTR: [X]% (vs [Y]% last week)

CREATIVE HEALTH
- Active variants: [X] (of which [Y] are <2 weeks old)
- Top variant: "[name]" — VTR [X]%, CPqL $[Y]
- Fatigued variants paused this week: [X] (list)
- New briefs generated: [X] (awaiting human video production)
- Creative win rate (last 30 days): [X]%

AUDIENCE HEALTH
- Placement campaign: [X] leads at $[Y] CPqL, frequency [Z]
- Custom intent campaign: [X] leads at $[Y] CPqL
- Topic campaign: [X] leads at $[Y] CPqL
- New placements discovered: [X] channels added
- Saturated audiences: [list or "none"]

OPTIMIZATION ACTIVITY
- Active experiment: [description or "none"]
- Experiment results: [if any completed this week]
- Hypotheses in queue: [X]
- Cumulative improvement from optimization: [X]% CPqL reduction since Durable start

PIPELINE IMPACT
- Leads in nurture: [X]
- Meetings booked this week: [X]
- Deals in pipeline from YT preroll (all time): [X] worth $[Y]
- Closed-won revenue attributed to YT preroll: $[X]

RECOMMENDATION
- [One specific recommendation based on this week's data]
```

### 7. Run monthly strategic review

Once per month, the agent generates a deeper analysis:

**Full-funnel attribution:**
- Trace YouTube pre-roll leads through the pipeline: lead to meeting to qualified to deal to closed-won
- Calculate true ROAS: ad spend vs. revenue from YT-preroll-sourced deals
- Compare channel performance: YouTube pre-roll vs. LinkedIn ads vs. organic vs. outreach

**Experiment retrospective:**
- How many experiments were completed this month? How many won?
- Which pain points, hook types, and audience types drove the best results?
- What is the creative "hit rate" trending? (Should improve over time as the agent learns)
- Distance from local maximum: are experiments producing >2% improvement or has the play converged?

**Market adaptation:**
- Is CPV trending up across the market (seasonal/macro) or just for us?
- Are new competitors running YouTube pre-roll in our space?
- Are there new YouTube channels emerging in our ICP's interest areas?
- Should we test new formats (YouTube Shorts ads, in-feed video ads)?

**Human action required:** Review the monthly report. Make strategic decisions: change budget range, approve new pain points for creative, approve new audience strategies, or decide to test new video formats.

### 8. Evaluate sustainability

Run the `threshold-engine` drill monthly. The durable threshold is:

**≥ 45 qualified leads/month for 12 consecutive months with CPqL within 15% of Scalable baseline; agent generates weekly reports and creative briefs with ≤ 3 hours/week human oversight.**

Monthly check:
- Is qualified lead volume ≥ 45/month? (PASS/FAIL)
- Is CPqL within 15% of Scalable CPqL? (PASS/FAIL)
- Did the agent generate a weekly report every week this month? (PASS/FAIL)
- Did the agent produce and test new creative briefs every 2 weeks? (PASS/FAIL)
- Was human oversight ≤ 3 hours/week on average? (PASS/FAIL)

All 5 must pass for the month to count. 12 consecutive passing months = Durable achieved.

If any metric degrades for 2 consecutive months:
1. Agent diagnoses via `autonomous-optimization`: creative fatigue across all variants? Audience saturation? Market shift? Landing page degradation?
2. Agent proposes a recovery plan (e.g., "test 3 entirely new pain points", "expand to YouTube Shorts ads", "rebuild placement list from scratch")
3. Human approves and the agent executes

**Convergence:** When 3 consecutive experiments produce <2% improvement on CPqL, the play has reached its local maximum. The agent:
1. Reduces monitoring frequency from daily to every 3 days
2. Reduces creative refresh from bi-weekly to monthly
3. Reports: "YouTube pre-roll is optimized. Current performance: [metrics]. Further gains require strategic changes (new audience segments, new video formats, product positioning changes) rather than tactical optimization."

## Time Estimate

**One-time setup (month 1): ~40 hours**
- 12 hours: Dashboard build and alert configuration
- 10 hours: Autonomous optimization loop configuration
- 8 hours: Creative management, audience management, and budget management automation
- 6 hours: Weekly report and monthly review templates
- 4 hours: Testing and validation of all workflows

**Ongoing (months 2-12): ~14 hours/month**
- 2 hours bi-weekly: Human reviews creative briefs and produces videos (4 hrs/month)
- 1 hour/week: Human reviews weekly report (4 hrs/month)
- 2 hours/month: Monthly strategic review
- 2 hours/month: Agent maintenance (fix n8n workflow issues, update API integrations)
- 2 hours/month: Agent compute time (automated workflows running)

Total: ~180 hours over 12 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads (YouTube) | Video ad platform | $5,000-20,000/mo ad spend. CPV $0.02-0.10. [Pricing](https://ads.google.com/home/pricing/) |
| YouTube Data API | Automated placement discovery | Free (10,000 units/day). [Pricing](https://developers.google.com/youtube/v3/getting-started#quota) |
| Clay | Lead enrichment and scoring | $349/mo Growth plan (CRM sync at this volume). [Pricing](https://clay.com/pricing) |
| Loops | Nurture sequences at scale | $49-99/mo depending on contact volume. [Pricing](https://loops.so/pricing) |
| PostHog | Dashboards, experiments, events, anomaly detection | Free up to 1M events/mo, then pay-as-you-go. [Pricing](https://posthog.com/pricing) |
| n8n | All automation (creative mgmt, audience discovery, budget mgmt, monitoring, reporting) | Free self-hosted or $20-50/mo cloud. [Pricing](https://n8n.io/pricing) |
| Anthropic API | Creative brief generation, hypothesis generation, experiment evaluation | ~$2-5/month at this usage (Claude Sonnet). [Pricing](https://www.anthropic.com/pricing) |
| Webflow | Landing pages | $23/mo CMS plan. [Pricing](https://webflow.com/pricing) |
| Descript | Video production | $24/mo. [Pricing](https://www.descript.com/pricing) |

**Estimated durable monthly cost:** $5,000-20,000 ad spend + ~$550-800 tooling = $5,550-20,800/mo

## Drills Referenced

- `autonomous-optimization` — the core detect, diagnose, experiment, evaluate, implement loop that finds and maintains the local maximum
- `autonomous-optimization` — daily health checks, fatigue detection, saturation alerts, weekly reports
- the youtube preroll creative pipeline workflow (see instructions below) — autonomous creative brief generation on a bi-weekly cadence
- `youtube-preroll-audience-builder` — automated placement discovery and audience refresh
- `dashboard-builder` — build the YouTube pre-roll performance dashboard with alerts
- `budget-allocation` — automated daily budget adjustments with CPqL guardrails
- `threshold-engine` — monthly sustainability evaluation against Scalable baseline
