---
name: paid-search-ads-durable
description: >
  Paid Search Ads — Durable Intelligence. Always-on AI agents autonomously optimize search
  ad campaigns across Google and Microsoft Ads. The autonomous-optimization drill monitors
  KPIs, generates hypotheses when metrics change, runs A/B experiments, auto-implements
  winners, and produces weekly optimization briefs. Agent finds the local maximum and
  maintains it as market conditions shift.
stage: "Marketing > SolutionAware"
motion: "LightweightPaid"
channels: "Paid"
level: "Durable Intelligence"
time: "160 hours over 6 months"
outcome: ">=15 leads/month for 6 consecutive months with CPA within 115% of Scalable baseline; agent runs autonomously with <=2 hrs/week human oversight"
kpis: ["Monthly lead volume (>=15/mo sustained)", "CPA trend (rolling 30-day, stable or declining)", "Lead-to-meeting conversion rate", "Blended ROAS across Google + Microsoft", "Experiment win rate (% of A/B tests that produce improvement)", "Agent autonomy ratio (automated actions / total actions)"]
slug: "paid-search-ads"
install: "npx gtm-skills add marketing/solution-aware/paid-search-ads"
drills:
  - autonomous-optimization
  - search-ads-performance-monitor
  - dashboard-builder
---

# Paid Search Ads — Durable Intelligence

> **Stage:** Marketing → SolutionAware | **Motion:** LightweightPaid | **Channels:** Paid

## Outcomes

The search ads play runs itself. An AI agent monitors daily metrics, detects when performance shifts (CPA rising, CTR dropping, impression share declining), generates hypotheses for what to change, designs and runs A/B experiments, evaluates results, and auto-implements winners. The human role reduces to reviewing weekly briefs and approving high-risk changes (budget increases >20%, new platform experiments, targeting changes affecting >50% of traffic). The system converges on the local maximum for your market and maintains it as competitors, seasonality, and search behavior evolve.

**Pass threshold:** >=15 leads/month for 6 consecutive months with CPA within 115% of Scalable baseline; agent runs autonomously with <=2 hrs/week human oversight.

## Leading Indicators

- Agent detects anomalies within 24 hours of onset (measured by time-to-detection)
- Experiment cycle time: <14 days from hypothesis to decision
- At least 2 experiments per month running (the system is actively seeking improvement)
- Weekly optimization briefs produced on schedule with actionable content
- Negative keyword list growing automatically (search query mining continues)
- No manual CPA corrections needed (agent handles bid/budget adjustments autonomously)
- CPA variance: week-over-week CPA stays within +/-15% of 30-day average (stability)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for search ads. This is the core of Durable -- the always-on monitor-diagnose-experiment-evaluate-implement cycle.

**Configure the optimization loop with these search-ads-specific parameters:**

**Monitoring (daily via n8n cron):**
- Pull metrics from Google Ads API and Microsoft Ads API: CPA, CTR, conversion rate, impression share, quality score, cost per click, budget utilization
- Pull landing page metrics from PostHog: conversion rate, bounce rate, form view rate
- Compare last 7 days against 30-day rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If anomaly detected on any primary metric (CPA, CTR, conversion rate), trigger the diagnosis phase

**Diagnosis (triggered by anomaly):**
- Gather context: current keyword list, active ad variants, landing page version, bid strategy, budget allocation, competitor auction insights
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data + search-ads context
- Common search-ads hypotheses the agent should consider:
  - **CPA rising + impression share stable** → ad fatigue or landing page decay. Test new ad copy or landing page variant.
  - **CPA rising + impression share declining** → competitor bid pressure. Test bid increases on top keywords or shift budget to Microsoft Ads where competition may be lower.
  - **CTR dropping + impressions stable** → ad fatigue. Refresh headlines and descriptions.
  - **Conversion rate dropping + CTR stable** → landing page issue. Test new headline, shorter form, or different CTA.
  - **Quality score dropping** → relevance drift. Tighten keyword-to-ad-to-landing-page alignment.
- Receive 3 ranked hypotheses with expected impact and risk level
- If risk = "high" (budget changes >20%, targeting changes >50% of traffic), send Slack alert for human approval

**Experimentation (triggered by hypothesis acceptance):**
- Take the top-ranked hypothesis
- Design the experiment using PostHog feature flags:
  - For ad copy tests: create a new RSA variant in Google/Microsoft Ads, split traffic via campaign experiments
  - For landing page tests: use PostHog feature flags to show different page elements
  - For bid strategy tests: use Google Ads experiments to test Target CPA vs Target ROAS
  - For budget allocation tests: shift 20% of budget to the hypothesized better allocation for 2 weeks
- Set minimum experiment duration: 7 days or 100+ conversions per variant
- Log experiment start in Attio: hypothesis, start date, variants, success criteria

**Evaluation (triggered by experiment completion):**
- Pull experiment results from PostHog and ad platform APIs
- Run `experiment-evaluation`: is the improvement statistically significant at 95% confidence?
- Decision matrix:
  - **Adopt**: Primary metric improved >=5% with statistical significance. Update live configuration. Log the change.
  - **Iterate**: Direction is promising but not significant. Generate a refined hypothesis. Return to diagnosis.
  - **Revert**: Variant performed worse. Restore control. Log the failure. Return to monitoring.
  - **Extend**: Results trending positive but sample size insufficient. Run 7 more days.
- Store full evaluation in Attio with decision, confidence interval, and reasoning

**Reporting (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from adopted changes
- Generate weekly optimization brief:

```markdown
# Search Ads Optimization Brief — Week of {date}

## Performance Summary
| Metric | This Week | 30-Day Avg | Trend | Status |
|--------|-----------|------------|-------|--------|
| CPA | ${X} | ${Y} | {arrow} | {normal/alert} |
| CTR | {X}% | {Y}% | {arrow} | {normal/alert} |
| Conv Rate | {X}% | {Y}% | {arrow} | {normal/alert} |
| Leads | {X} | {Y}/wk avg | {arrow} | {normal/alert} |
| Imp Share | {X}% | {Y}% | {arrow} | {normal/alert} |
| Spend | ${X} | ${Y}/wk avg | — | — |

## Anomalies Detected: {count}
{Description of each anomaly and what was done}

## Experiments
| Experiment | Status | Hypothesis | Result |
|-----------|--------|------------|--------|
| {name} | {running/completed/reverted} | {hypothesis} | {outcome} |

## Net Impact This Week
{Net CPA change, net conversion rate change from all adopted experiments}

## Convergence Status
{Distance from estimated local maximum. Successive experiment improvement rate.}

## Recommended Human Actions
{Only items requiring human approval. Empty if agent is handling everything.}
```

### 2. Build the search-ads-specific monitoring layer

Run the `search-ads-performance-monitor` drill to extend the autonomous optimization loop with search-specific monitoring:

- **Automated search query mining (weekly):** Continue the weekly search terms analysis from Scalable, now fully automated. The agent adds negative keywords, promotes converting queries, and logs every change.
- **Creative fatigue detection (weekly):** Monitor each RSA variant's CTR over time. When CTR declines >30% from peak, auto-generate 3 new headline variants using Claude and create new RSA experiments.
- **Competitive auction monitoring (weekly):** Track auction insights data from Google Ads API. Detect when new competitors enter your keyword space or existing competitors increase bids. Alert if impression share drops below 50% on any top-5 keyword.
- **Quality score tracking (daily):** Monitor quality score trends. If any ad group's average QS drops below 6, diagnose the cause (ad relevance, landing page experience, or expected CTR) and generate specific improvement actions.

### 3. Build the executive dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard for ongoing visibility:

- **Row 1 (headline metrics):** Monthly leads, CPA (30-day rolling), total monthly spend, ROAS
- **Row 2 (trend charts):** Weekly CPA trend (13 weeks), weekly lead volume trend, CTR trend
- **Row 3 (platform split):** Google vs Microsoft Ads: spend, leads, CPA side by side
- **Row 4 (funnel):** Ad click → landing page view → form view → form submit → meeting booked → meeting held
- **Row 5 (experiments):** Active experiments, recent experiment results, cumulative improvement from experiments
- **Alerts configured:**
  - CPA >150% of 30-day average for 2 consecutive days
  - Weekly lead volume <50% of 4-week average
  - Landing page conversion rate <50% of baseline
  - Monthly spend on pace to exceed budget by >10%

### 4. Implement guardrails

The following guardrails are critical for autonomous operation. Build them into the n8n workflows:

- **Budget guardrail:** Agent cannot increase total monthly ad spend by more than 20% without human approval. Cannot exceed hard cap set in campaign settings.
- **Rate limit:** Maximum 1 active experiment per platform at a time. Never stack experiments.
- **Revert threshold:** If any experiment causes CPA to spike >40% above 30-day average during the test period, auto-revert immediately and log the failure.
- **Negative keyword guardrail:** Agent cannot add negative keywords that match any currently-converting search query. Verify against conversion data before adding.
- **Bid guardrail:** Agent cannot increase max CPC bids by more than 50% in a single change. Ratchet up in 20% increments.
- **Cooldown:** After a failed experiment (reverted), wait 7 days before testing a new hypothesis on the same variable (e.g., if a headline test failed, do not test another headline change for 7 days -- test something else).
- **Monthly experiment cap:** Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review (the play may need a fundamental strategy change, not tactical tweaks).
- **Human approval required for:** Budget increases >20%, adding or removing entire ad groups, changes to geographic targeting, changes to bid strategy type.

### 5. Detect convergence

The autonomous optimization loop should detect when successive experiments produce diminishing returns. Track:
- Improvement magnitude of each adopted experiment (% CPA reduction or % conversion rate increase)
- When 3 consecutive experiments produce <2% improvement, the play has reached its local maximum

At convergence:
1. Reduce monitoring frequency from daily to every-other-day (anomaly detection still runs, but hypothesis generation slows)
2. Reduce experiment frequency from 2-4/month to 1/month (maintenance experiments to ensure the maximum holds)
3. Report: "Search ads play has converged. Current CPA: ${X}. Monthly leads: {Y}. Further gains require strategic changes: new keyword categories, new platforms, or product/offer changes."

### 6. Handle seasonal and market shifts

Search behavior changes with seasons, industry events, and competitive dynamics. Build detection for:
- **Seasonal CPC spikes:** Q4 in B2B sees higher CPCs. Agent should detect CPC trend upward in October and proactively reduce budget or tighten targeting to maintain CPA.
- **New competitor entry:** If a new domain appears in auction insights at >10% impression share, alert the human and draft a competitive response (new ad copy addressing the competitor's positioning).
- **Search volume shifts:** If impression volume drops >30% month-over-month on core keywords, investigate: is the category shrinking, or did Google change how it matches queries? Adjust keyword strategy accordingly.

**Human action required:** Review weekly optimization briefs. Approve high-risk changes flagged by the agent. Conduct monthly strategic reviews: is the search ads channel still the right allocation of budget vs other plays?

## Time Estimate

- 20 hours: Deploy autonomous optimization loop (n8n workflows, PostHog anomaly detection, hypothesis generation pipeline)
- 12 hours: Build search-ads-specific monitoring layer (query mining automation, creative fatigue, competitive monitoring)
- 8 hours: Build executive dashboard and alert system
- 8 hours: Implement guardrails, convergence detection, and seasonal handling
- 48 hours: Agent operation over 6 months (automated, but requires compute)
- 48 hours: Human oversight over 6 months (~2 hrs/week reviewing briefs, approving changes)
- 16 hours: Monthly strategic reviews and agent tuning (4 hrs/mo x 4 months, front-loaded)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads | Search campaigns | $3,000-12,000/mo budget — [ads.google.com](https://ads.google.com) |
| Microsoft Advertising | Bing search campaigns | $1,000-4,000/mo budget — [ads.microsoft.com](https://ads.microsoft.com) |
| PostHog | Analytics, experiments, anomaly detection, dashboards | Growth ~$50-200/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Workflow automation (optimization loop, monitoring, syncs) | Pro EUR60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API (Claude) | Hypothesis generation, experiment evaluation, weekly briefs | ~$30-80/mo — [anthropic.com](https://console.anthropic.com) |
| Attio | CRM, experiment log, campaign records | Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Webflow | Landing pages | CMS $23/mo — [webflow.com/pricing](https://webflow.com/pricing) |

**Estimated play-specific cost:** $5,000-20,000/mo ad spend + ~$200-400/mo tooling + ~$30-80/mo AI compute

## Drills Referenced

- `autonomous-optimization` — The core always-on optimization loop: monitor metrics, detect anomalies, generate hypotheses, run A/B experiments, evaluate results, auto-implement winners, produce weekly briefs
- `search-ads-performance-monitor` — Search-specific monitoring: automated query mining, creative fatigue detection, competitive auction tracking, quality score monitoring
- `dashboard-builder` — PostHog dashboard with real-time search ads KPIs, trends, platform comparison, and experiment tracking
