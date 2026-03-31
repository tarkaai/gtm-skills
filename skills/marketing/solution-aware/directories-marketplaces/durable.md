---
name: directories-marketplaces-durable
description: >
  Directory & Marketplace Listings — Durable Intelligence. Always-on AI agents autonomously optimize
  listings, review responses, PPC bids, and landing pages via the detect-diagnose-experiment-evaluate loop.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Other"
level: "Durable Intelligence"
time: "20 hours setup + 2 hours/week ongoing"
outcome: "Listing views and inquiries sustained at or above Scalable baseline for 6 consecutive months; successive optimization experiments produce <2% improvement (convergence)"
kpis: ["Listing views (trend)", "Inquiry count (trend)", "Cost per inquiry (trend)", "Average rating (trend)", "Experiment win rate", "Convergence score"]
slug: "directories-marketplaces"
install: "npx gtm-skills add marketing/solution-aware/directories-marketplaces"
drills:
  - autonomous-optimization
  - directory-performance-monitor
  - dashboard-builder
---

# Directory & Marketplace Listings — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Other

## Outcomes

Always-on AI agents finding the local maximum. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in directory performance, generate improvement hypotheses, run A/B experiments on listings and landing pages, evaluate results, and auto-implement winners. Weekly optimization briefs. The play converges when successive experiments produce <2% improvement.

**Pass threshold:** Listing views and inquiries sustained at or above Scalable baseline for 6 consecutive months; successive optimization experiments produce <2% improvement (convergence).

## Leading Indicators

- Autonomous optimization loop running daily (monitoring) and weekly (experiment cycle)
- At least 1 experiment active per month
- Weekly optimization briefs delivered automatically
- No manual intervention required for routine listing updates or review responses
- Metric trends stable or improving over 4-week rolling window
- Convergence detected: 3 consecutive experiments produce <2% improvement on any single variable

## Instructions

### 1. Initialize the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play's KPIs:

**Primary KPIs to monitor:**
- Total listing views per week (across all directories)
- Total inquiries per week (from directory-sourced traffic)
- Cost per inquiry (for paid directories)
- Average review rating (across all directories)

**Anomaly detection thresholds:**
- Normal: within +/-10% of 4-week rolling average
- Plateau: +/-2% for 3+ consecutive weeks
- Drop: >20% decline week-over-week
- Spike: >50% increase week-over-week

**Phase 1 -- Monitor (daily via n8n cron):**
1. Pull analytics from all directory APIs using `directory-analytics-scraping` fundamental
2. Pull PostHog data for `directory_listing_view`, `directory_listing_click`, `directory_inquiry_submitted`
3. Compare against 4-week rolling average
4. If anomaly detected -> trigger Phase 2 (Diagnose)
5. If normal -> log metrics, no action

**Phase 2 -- Diagnose (triggered by anomaly):**
1. Gather context: current listing copy for each directory, current landing page variants, PPC bid levels, recent review sentiment
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` with anomaly data + context
4. Receive 3 ranked hypotheses. Examples:
   - "G2 views dropped because a competitor launched a review campaign and pushed us down in category ranking. Hypothesis: refresh listing copy with new feature highlights and request 10 reviews this week."
   - "Capterra CPI increased because our max CPC is too high for the current conversion rate. Hypothesis: reduce max CPC by 20% and test a new landing page headline."
   - "Inquiry rate dropped across all directories. Hypothesis: the landing page CTA changed in a recent site deploy. Revert to previous CTA."
5. If top hypothesis is high-risk (budget change >20% or targeting change >50%) -> alert human and STOP
6. If low/medium risk -> proceed to Phase 3

**Phase 3 -- Experiment:**
1. Take the top hypothesis
2. Design the experiment:
   - For listing copy changes: update the listing on the specific directory and compare 2-week performance before/after
   - For landing page changes: use PostHog feature flags to split directory traffic 50/50
   - For PPC bid changes: adjust bids and measure CPI over 2 weeks
   - For review campaigns: send targeted review asks and measure rating/rank impact
3. Set minimum duration: 14 days or 200+ directory-sourced sessions, whichever is longer
4. Log experiment in Attio: hypothesis, start date, duration, success criteria

**Phase 4 -- Evaluate:**
1. Pull experiment results from PostHog and directory APIs
2. Run `experiment-evaluation`:
   - **Adopt:** Implement the winning variant permanently. Log the change.
   - **Iterate:** Generate a new hypothesis building on the result. Return to Phase 2.
   - **Revert:** Restore the control. Log the failure. Return to Phase 1.
   - **Extend:** Keep running if sample size is insufficient.
3. Store full evaluation in Attio

**Phase 5 -- Report (weekly via n8n cron):**
1. Aggregate: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on views, inquiries, cost per inquiry
   - Current distance from estimated local maximum
   - Convergence status (are gains diminishing?)
4. Post to Slack and store in Attio

### 2. Configure play-specific monitoring

Run the `directory-performance-monitor` drill with Durable-level enhancements:

**Competitive intelligence automation:**
- Weekly Clay scrape of top 5 competitors across all Tier 1 directories
- Alert when a competitor's review count jumps 10+ in a week
- Alert when a competitor moves ahead of you in category ranking
- Feed competitive changes into the hypothesis generator as context

**Review health monitoring:**
- Track review sentiment trend (not just rating, but keyword analysis of review text)
- Detect review fatigue: if review velocity drops below 2/week, trigger a fresh review campaign
- Monitor for review platform policy changes that could affect your listings

**Directory ecosystem monitoring:**
- Track when new directories gain traction in your category
- Alert when an existing directory changes its ranking algorithm or pricing model
- Monitor for new category pages where your product should be listed

### 3. Build the executive dashboard

Run the `dashboard-builder` drill to create the Durable-level directory dashboard:

**Panel 1 -- Health Summary:**
- Traffic light status per directory: green (growing), yellow (stable), red (declining)
- Total views, inquiries, and cost per inquiry (30-day rolling)
- Comparison to Scalable baseline (are we maintaining or exceeding?)

**Panel 2 -- Optimization Activity:**
- Active experiments (count, descriptions)
- Experiments completed this month (win/loss/no-call)
- Cumulative improvement from adopted experiments (% change from Scalable baseline)
- Convergence indicator: moving average of experiment impact (trending toward <2%)

**Panel 3 -- Review Intelligence:**
- Review velocity trend (reviews per week, 12-week rolling)
- Rating trend by directory
- Sentiment analysis: most common positive and negative keywords in recent reviews
- Response time: average hours from review posted to vendor response

**Panel 4 -- Competitive Position:**
- Your rank vs. top 3 competitors on each Tier 1 directory
- Review count gap (how many reviews until you match or exceed competitor)
- Rating comparison

### 4. Guardrails

Follow all guardrails from the `autonomous-optimization` drill, plus these play-specific limits:

- **PPC budget cap:** Never increase PPC spend more than 20% in a single experiment without human approval
- **Listing change rate limit:** Maximum 1 listing copy change per directory per 2-week period. More frequent changes confuse the ranking algorithm.
- **Review ask limit:** Never send more than 1 review ask per customer per quarter, regardless of directory
- **Response tone:** AI-drafted review responses for 3+ star reviews can auto-post. Responses to 1-2 star reviews must be queued for human review before posting.
- **Category changes:** Never change the primary category listing without human approval

### 5. Convergence and steady state

When the optimization loop detects convergence (<2% improvement from 3 consecutive experiments):

1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment cadence from monthly to quarterly
3. Report: "Directory channel optimized. Current performance: {views}/week, {inquiries}/week, ${cost_per_inquiry} CPI, {avg_rating} rating across {directory_count} directories. Further gains require strategic changes (new product features, new category creation, market repositioning)."
4. Continue passive monitoring for external disruptions (competitor moves, platform changes)
5. Re-enter active optimization if any primary KPI drops >15% from the converged baseline

## Time Estimate

- 8 hours: Configure autonomous optimization loop (n8n workflows, PostHog experiments, Attio logging)
- 6 hours: Competitive intelligence and ecosystem monitoring setup
- 4 hours: Executive dashboard build
- 2 hours: Guardrail configuration and testing
- Ongoing: 2 hours/week reviewing optimization briefs and approving high-risk experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| G2 | Directory + sponsored listings | Free listing; sponsored ~$1,000-3,000/quarter ([sell.g2.com/plans](https://sell.g2.com/plans)) |
| Capterra | Directory + PPC | PPC min $500/mo at $2+/click ([capterra.com/vendors](https://www.capterra.com/vendors/)) |
| PostHog | Tracking, experiments, dashboards | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Automation orchestration | Cloud Pro EUR 60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation + evaluation | ~$20-50/mo at optimization cadence ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Clay | Competitive monitoring | Explorer $149/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM + experiment logging | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Loops | Review ask sequences | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost at this level:** $1,000-3,500 (primarily G2 sponsored + Capterra PPC + Anthropic API + Clay)

## Drills Referenced

- `autonomous-optimization` -- the core detect-diagnose-experiment-evaluate loop that finds the local maximum for directory performance
- `directory-performance-monitor` -- enhanced with competitive intelligence, review health tracking, and ecosystem monitoring
- `dashboard-builder` -- executive dashboard with optimization activity, competitive position, and convergence tracking
