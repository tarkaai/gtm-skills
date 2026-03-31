---
name: brand-refresh-redesign-durable
description: >
  Brand Refresh & Redesign — Durable Intelligence. AI agent autonomously optimizes
  website messaging, conversion paths, and brand presentation via the
  detect-diagnose-experiment-evaluate loop. Finds and maintains the local maximum
  of conversion performance as market conditions and competitive landscape evolve.
stage: "Marketing > Unaware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained top-quartile conversion rates over 12 months with autonomous AI-driven messaging and conversion optimization"
kpis: ["Conversion rate (3-month rolling avg)", "AI experiment win rate", "Experiment velocity (tests/month)", "Time to detect regression", "Convergence distance", "Brand search volume trend"]
slug: "brand-refresh-redesign"
install: "npx gtm-skills add marketing/unaware/brand-refresh-redesign"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Brand Refresh & Redesign — Durable Intelligence

> **Stage:** Marketing > Unaware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Outcomes

Deploy the autonomous optimization loop on all website and brand surfaces. The AI agent continuously monitors conversion performance across every page, detects when messaging or conversion paths degrade, generates improvement hypotheses, runs controlled experiments, and auto-implements winners. The goal is to find the local maximum of conversion performance and maintain it as the market, competitive landscape, and audience evolve. Target: sustained top-quartile conversion rates over 12 months.

## Leading Indicators

- Autonomous optimization loop running uninterrupted for 4+ consecutive weeks
- At least 2 experiments launched per month (agent is actively improving the site)
- Experiment win rate >=30% (at least 1 in 3 experiments produces measurable improvement)
- Conversion rate has not declined >5% quarter-over-quarter
- Regressions detected within 48 hours (not waiting for human review)
- Weekly optimization brief delivered on schedule every Monday

## Instructions

### 1. Build the brand intelligence dashboard

Run the `dashboard-builder` drill to create a comprehensive PostHog dashboard:

**Conversion layer:**
- Overall site conversion rate (30-day rolling, with pre-refresh baseline marker)
- Conversion rate by entry page (table: page, visitors, conversion rate, trend arrow)
- Conversion funnel by traffic source (organic vs. paid vs. direct vs. referral)
- Form submission rate by form (which lead capture surfaces are performing?)
- Scroll depth distribution on key pages (are visitors reading your content?)

**Experimentation layer:**
- Active experiments: current hypothesis, variant vs. control metrics, days remaining, statistical significance status
- Experiment history: all past experiments ranked by impact
- Cumulative improvement: total conversion rate gain from all adopted experiments since Durable launch
- Convergence tracker: rolling 3-experiment improvement rate

**Brand health layer:**
- Bounce rate by page (daily trend, 90-day window)
- Session duration trend
- Pages per session
- New vs. returning visitor ratio
- Brand search volume (from Google Search Console API if connected)
- Direct traffic trend (proxy for brand awareness)

### 2. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for brand and conversion optimization:

**Phase 1 — Monitor (daily):**
The n8n cron workflow pulls PostHog web analytics and conversion data. Compares last 2 weeks against the 4-week rolling average. Classifies each metric:

- **Normal**: All page-level metrics within +-10% of average. No action.
- **Plateau**: Conversion rate unchanged >=2% for 3+ weeks on any high-traffic page. Trigger Phase 2 to find improvement.
- **Drop**: Conversion rate decreased >15% or bounce rate increased >15% on any page. Trigger Phase 2 urgently.
- **Spike**: Positive anomaly (conversion rate jumped). Log the conditions (traffic source, time of day, page variant) for replication.

**Phase 2 — Diagnose (triggered by anomaly):**
Agent gathers context:
- Which page(s) are affected?
- Which traffic sources are impacted?
- What changed recently (new content, design update, external link, competitor launch)?
- Session recording analysis: watch 10 recent recordings on the affected page

Pass context to Claude for hypothesis generation:

```
The brand/conversion monitoring detected a {anomaly_type} on {page}.
Current state: {metrics for this page}
Trend: {14-day daily metrics}
Traffic source breakdown: {organic X%, paid Y%, direct Z%}
Recent changes: {any content or design changes in last 14 days}
Session recording observations: {patterns noticed}
Competitor activity: {if detected}

Generate 3 ranked hypotheses for improvement. Each must be:
1. A specific, executable change (e.g., "rewrite homepage H1 from '{current}' to '{proposed}' emphasizing {angle}")
2. Expected impact (e.g., "+10% conversion rate on homepage")
3. Risk level (low = copy change only, medium = layout change, high = navigation or funnel change)
```

High-risk hypotheses require human approval via Slack.

**Phase 3 — Experiment:**
Design and deploy a controlled test:
- Create PostHog feature flag splitting traffic 50/50
- Implement the variant (copy change via Webflow API, layout change via feature flag rendering)
- Minimum duration: 14 days or 500 conversions per variant
- Log experiment in Attio: hypothesis, start date, pages affected, success metric

Types of experiments the agent can run autonomously:
- **Messaging experiments**: Headline rewrites, value proposition variants, CTA copy changes
- **Social proof experiments**: Different testimonials, different metrics, different logo sets
- **Conversion path experiments**: Form placement, CTA button color/size, page structure
- **Content experiments**: Different blog CTAs, different content offers, different lead magnets

Types requiring human approval:
- Navigation changes (affects site architecture)
- Pricing page structure changes
- Brand visual identity changes (colors, logo usage, photography style)

**Phase 4 — Evaluate:**
Pull experiment results from PostHog when the test reaches statistical significance or the maximum duration:
- **Adopt (>=5% improvement, p<0.05)**: Roll out winning variant to 100%. Update Webflow. Log the change.
- **Iterate (inconclusive)**: Generate a refined hypothesis building on this data. Return to Phase 2.
- **Revert (variant loses)**: Restore control. Log the failure. 7-day cooldown before testing the same variable.

**Phase 5 — Report (weekly):**
Every Monday, generate a weekly brand optimization brief:
- Pages monitored and their health status
- Anomalies detected this week
- Experiments run and their outcomes
- Net conversion rate change from all adopted experiments this week
- Current distance from estimated local maximum (based on diminishing experiment returns)
- Recommended focus areas for next week

Post to Slack and store in Attio.

### 3. Configure always-on brand monitoring

Run the `autonomous-optimization` drill at Durable intensity:
- Daily monitoring of every marketing page
- Regression detection within 48 hours
- Weekly brand health reports with page-level breakdowns
- Seasonal pattern recognition (does conversion dip in certain months? If so, don't over-react)
- Competitive monitoring: quarterly re-crawl of competitor websites to detect positioning changes that may require a response

### 4. Define convergence criteria

The optimization loop runs indefinitely, but detects when it has found the local maximum:
- Track the improvement rate of the last 3 adopted experiments
- If all 3 produced <2% improvement: the brand and conversion optimization has converged
- At convergence:
  1. Reduce experiment velocity from 2-3/month to 1/month (maintenance mode)
  2. Shift monitoring from daily to weekly
  3. Report to team: "Website conversion is optimized at [rate]. Further gains require strategic changes (new positioning, new audience, product changes) rather than tactical optimization."
  4. Continue monitoring for regressions — convergence doesn't mean the agent stops watching

### 5. Evaluate sustainability

Measure quarterly:
- **Conversion rate sustained or improving**: 3-month rolling average should not decline >5% from peak
- **Experiment win rate >= 30%**: Indicates the agent is still finding improvements (drops near convergence)
- **Brand search volume trend**: Should be flat or growing (brand awareness is holding)

If metrics sustain over 12 months, the play is durable.
If metrics decay despite optimization, the agent diagnoses strategic causes: market shift, new competitor, product-market fit drift. Recommends a new Smoke-level brand audit to reassess positioning from scratch.

## Time Estimate

- 25 hours: Initial Durable setup (dashboard, optimization loop, monitoring, guardrails)
- 8 hours/month: Experiment review, high-risk approvals, strategy direction
- 5 hours/month: Quarterly competitor re-audit and strategic review

**Total: ~180 hours over 12 months (25 setup + ~13/month ongoing)**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Full-funnel analytics, feature flags, experiments, session recordings | Free tier or ~$50-100/mo at Durable volume |
| Webflow | Website content updates via API | ~$15-40/mo |
| n8n | Optimization loop workflows, monitoring, reporting | Free self-hosted or $20/mo cloud |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly briefs, competitor analysis | ~$30-60/mo |
| Hotjar (optional) | Heatmaps for supplementary UX data | ~$30-100/mo |

## Drills Referenced

- `autonomous-optimization` — The core Durable loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, and generate weekly optimization briefs
- `autonomous-optimization` — Daily monitoring of page-level conversion metrics with regression detection, weekly health reports, and competitive monitoring
- `dashboard-builder` — Creates the PostHog intelligence dashboard with conversion, experimentation, and brand health layers
