---
name: founder-guest-podcasts-durable
description: >
  Founder Guest Podcast — Durable Intelligence. Autonomous agents monitor podcast performance,
  detect metric anomalies, run experiments on pitch strategy and content repurposing,
  and auto-implement winners to sustain or improve inbound leads from podcast guesting.
stage: "Marketing > Unaware"
motion: "PR & Earned Mentions"
channels: "Content"
level: "Durable Intelligence"
time: "80 hours over 6 months"
outcome: "Sustained or improving podcast-attributed leads over 6 months; successive optimization experiments produce <2% improvement (convergence reached)"
kpis: ["Monthly podcast bookings", "Monthly podcast-attributed leads", "Lead-per-episode ratio", "Content multiplier per episode", "Experiment win rate"]
slug: "founder-guest-podcasts"
install: "npx gtm-skills add marketing/unaware/founder-guest-podcasts"
drills:
  - autonomous-optimization
  - podcast-performance-monitor
  - dashboard-builder
---

# Founder Guest Podcast — Durable Intelligence

> **Stage:** Marketing → Unaware | **Motion:** PR & Earned Mentions | **Channels:** Content

## Outcomes

The podcast guesting channel runs autonomously with agents monitoring performance, diagnosing drops, running experiments, and implementing improvements. The play has reached its local maximum when successive experiments produce <2% improvement for 3 consecutive cycles. Monthly podcast-attributed leads sustain or improve against the Scalable baseline.

## Leading Indicators

- Weekly optimization loop runs without human intervention
- Anomalies (traffic drops, booking rate declines) are detected within 24 hours
- At least 1 experiment runs per month on pitch strategy, CTA, or content format
- Experiment win rate > 30% (at least 1 in 3 experiments produces measurable improvement)
- Weekly optimization brief delivered on schedule

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the podcast guesting play. This is the core loop that makes Durable fundamentally different from Scalable.

**Monitor phase (daily via n8n cron):**
- Use PostHog anomaly detection on these KPIs: podcast referral traffic (weekly), podcast-attributed leads (weekly), pitch reply rate (per campaign), booking rate (per campaign batch), content engagement per episode (per aired episode)
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within ±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected → trigger diagnosis

**Diagnose phase (triggered by anomaly):**
- Pull context from Attio: current pitch angles, target podcast tiers, active campaigns, recent episode performance
- Pull 8-week metric history from PostHog dashboard
- Generate 3 ranked hypotheses. Examples:
  - "Pitch reply rate dropped because the primary pitch angle has saturated — too many similar-topic guests in our target podcasts this quarter"
  - "Referral traffic per episode is declining because CTA script is not resonating — test a new offer"
  - "Booking rate dropped in Tier 2 podcasts — host enrichment data may be stale, re-enrich contacts"
- If top hypothesis risk = "high" (e.g., changes the founder's positioning or targets a completely new audience): send Slack alert for human review, STOP
- If risk = "low" or "medium": proceed to experiment

**Experiment phase:**
- Design the A/B test in PostHog (feature flag splits traffic between control and variant)
- Implement the variant. Experiment types for this play:
  - *Pitch experiments*: new subject line, new angle, different social proof, altered follow-up timing
  - *CTA experiments*: different offer (free consultation vs resource vs extended trial), different vanity URL landing page
  - *Content experiments*: new repurposing format (video clips vs carousels vs threads), different distribution cadence
  - *Targeting experiments*: new podcast tier threshold, new keyword category, geographic expansion
- Run for minimum 7 days or until 50+ data points per variant

**Evaluate phase:**
- Pull experiment results from PostHog
- Decision: Adopt (implement winner), Iterate (build on result), Revert (restore control), Extend (more data needed)
- Log decision, confidence, and reasoning in Attio

**Report phase (weekly via n8n cron):**
- Aggregate: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from adopted changes
- Generate weekly optimization brief:
  - What changed and why
  - Net impact on podcast-attributed leads
  - Current estimated distance from local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 2. Monitor long-tail episode value

Run the `podcast-performance-monitor` drill with Durable-level automation:
- Track lifetime traffic curves for every episode
- Identify evergreen episodes (still driving traffic after 90 days) — these inform which topics to prioritize for future appearances
- Detect episodes that drove zero conversions despite traffic — flag CTA or landing page issues
- Monthly: generate a "Best Performing Episodes" report ranking all appearances by lifetime leads attributed

### 3. Build the strategic podcast dashboard

Run the `dashboard-builder` drill to create an executive-level view:
- Total podcast appearances (cumulative and monthly)
- Podcast-attributed leads (monthly, trailing 6-month trend)
- Lead-per-episode ratio (trending up = optimization working, trending down = investigate)
- Pitch pipeline health: prospects in pipeline, pitches sent this month, booking rate trend
- Content multiplier: average derivative pieces per episode, engagement per derivative
- Experiment log: active experiments, recent results, cumulative impact

### 4. Manage convergence

The `autonomous-optimization` drill detects convergence when 3 consecutive experiments produce <2% improvement. At convergence:
- The podcast guesting channel has reached its local maximum
- Reduce monitoring frequency from daily to weekly
- Shift optimization effort to: (a) maintaining the current run rate, or (b) opening a new channel
- Report to team: "Podcast guesting is optimized at [X leads/month, Y bookings/month]. Further gains require strategic shifts: new podcast categories, a co-hosted podcast, or video podcast appearances."

### 5. Guardrails

- **Rate limit**: Maximum 1 active experiment at a time on this play
- **Revert threshold**: If podcast-attributed leads drop >30% week-over-week during an experiment, auto-revert immediately
- **Human approval required for**: changing the founder's positioning or bio, targeting podcasts outside the established ICP, budget increases >20%
- **Cooldown**: After a failed experiment, wait 7 days before testing the same variable again
- **Maximum experiments per month**: 4. If all 4 fail, pause optimization and flag for human strategic review.

## Time Estimate

- 10 hours: Autonomous optimization loop setup (n8n workflows, PostHog experiments config, hypothesis templates)
- 5 hours/month: Monitoring, experiment review, brief review (largely automated — human reviews weekly brief and approves high-risk hypotheses)
- 5 hours/month: Content repurposing for new episodes (sustained from Scalable)
- Remaining time: Agent-driven with human oversight on weekly briefs

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, dashboards | Free tier or $0+ usage-based ([pricing](https://posthog.com/pricing)) |
| n8n | Cron-triggered optimization loop, reporting | Part of default stack |
| Anthropic (Claude API) | Hypothesis generation and experiment evaluation | ~$10-30/mo at this query volume ([pricing](https://www.anthropic.com/pricing)) |
| Attio | Experiment log, pipeline tracking, performance records | Part of default stack |
| ListenNotes | Ongoing podcast discovery (reduced frequency) | Free tier or $9/mo ([pricing](https://www.listennotes.com/api/pricing/)) |
| Instantly | Pitch campaigns (sustained from Scalable) | $37/mo Growth ([pricing](https://instantly.ai/pricing)) |
| Descript | Content repurposing (sustained from Scalable) | $24/mo Creator ([pricing](https://descript.com/pricing)) |
| Dub.co | Tracking links (sustained from Scalable) | Free or $25/mo Pro ([pricing](https://dub.co/pricing)) |

**Estimated play-specific cost:** $80-200/mo (mostly sustained Scalable tools + Claude API for optimization)

## Drills Referenced

- `autonomous-optimization` — the core monitor → diagnose → experiment → evaluate → implement loop that finds the local maximum for podcast guesting
- `podcast-performance-monitor` — long-tail episode tracking, lifetime ROI analysis, monthly best-performers report
- `dashboard-builder` — executive-level strategic dashboard for podcast channel health
