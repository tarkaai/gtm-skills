---
name: google-display-network-campaigns-durable
description: >
  Google Display Network — Durable Intelligence. Always-on AI agents autonomously optimize
  display campaigns across GDN and Meta Audience Network. The autonomous-optimization drill
  monitors KPIs, detects placement rot and creative fatigue, generates improvement hypotheses,
  runs A/B experiments, auto-implements winners, and produces weekly optimization briefs.
  Agent finds the local maximum and maintains it as audience behavior shifts.
stage: "Marketing > SolutionAware"
motion: "LightweightPaid"
channels: "Paid"
level: "Durable Intelligence"
time: "140 hours over 6 months"
outcome: ">=50 qualified leads/month for 6 consecutive months with CPA within 115% of Scalable baseline; agent runs autonomously with <=2 hrs/week human oversight"
kpis: ["Monthly qualified leads (>=50/mo sustained)", "CPA trend (rolling 30-day, stable or declining)", "Lead-to-meeting conversion rate", "Blended ROAS across GDN + Meta", "Experiment win rate (% of A/B tests that produce improvement)", "Agent autonomy ratio (automated actions / total actions)", "Creative pipeline depth (variants in staging queue)"]
slug: "google-display-network-campaigns"
install: "npx gtm-skills add marketing/solution-aware/google-display-network-campaigns"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Google Display Network — Durable Intelligence

> **Stage:** Marketing → SolutionAware | **Motion:** LightweightPaid | **Channels:** Paid

## Outcomes

The display ads play runs itself. An AI agent monitors daily metrics across GDN and Meta, detects when performance shifts (CPA rising, CTR dropping, placements degrading, audiences exhausting), generates hypotheses for what to change, designs and runs A/B experiments, evaluates results, and auto-implements winners. The human role reduces to reviewing weekly briefs and approving high-risk changes (budget increases >20%, new platform experiments, audience targeting changes affecting >50% of traffic). The system converges on the local maximum for your market and maintains it as audience behavior, competitor activity, and placement quality evolve.

**Pass threshold:** >=50 qualified leads/month for 6 consecutive months with CPA within 115% of Scalable baseline; agent runs autonomously with <=2 hrs/week human oversight.

## Leading Indicators

- Agent detects anomalies within 24 hours of onset (measured by time-to-detection)
- Experiment cycle time: <14 days from hypothesis to decision
- At least 2 experiments per month running (the system is actively seeking improvement)
- Weekly optimization briefs produced on schedule with actionable content
- Placement exclusion list growing automatically (placement curation continues)
- Creative pipeline never drops below 3 variants in staging queue
- No manual CPA corrections needed (agent handles bid/budget adjustments autonomously)
- CPA variance: week-over-week CPA stays within +/-15% of 30-day average (stability)
- ICP match rate stable at >=50% (quality maintained as the agent optimizes for volume)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for display ads. This is the core of Durable -- the always-on monitor-diagnose-experiment-evaluate-implement cycle.

**Configure the optimization loop with these display-ads-specific parameters:**

**Monitoring (daily via n8n cron):**
- Pull metrics from Google Ads API: CPA by campaign, CTR by creative, impressions by placement, frequency by audience segment, budget utilization
- Pull metrics from Meta Ads API: CPA, CTR, frequency, audience overlap report
- Pull landing page metrics from PostHog: conversion rate, bounce rate, form view rate, scroll depth
- Pull lead quality data from Attio: ICP match rate for display-sourced leads this week
- Compare last 7 days against 30-day rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If anomaly detected on any primary metric (CPA, CTR, conversion rate, ICP match rate), trigger the diagnosis phase

**Diagnosis (triggered by anomaly):**
- Gather context: current audience segments, active creatives with age and CTR trend, placement distribution, bid strategy, budget allocation, frequency data
- Pull 8-week metric history from PostHog
- Pull placement report from Google Ads API (top 50 placements by spend)
- Run `hypothesis-generation` with the anomaly data + display-ads context
- Common display-ads hypotheses the agent should consider:
  - **CPA rising + CTR stable** → landing page conversion decay. Test new landing page variant (headline, form length, CTA).
  - **CPA rising + CTR declining + frequency increasing** → creative fatigue. Trigger the creative pipeline to generate and deploy new variants.
  - **CPA rising + impression volume declining** → audience exhaustion. Expand to new in-market categories, broaden custom intent, or test new geographic markets.
  - **CPA rising on GDN, stable on Meta** → GDN-specific issue. Check placement report for drift. Run a placement audit and exclude junk sites.
  - **CTR dropping on managed placements** → site audience changed or ad position degraded. Test new managed placements from the research pipeline.
  - **ICP match rate dropping + lead volume stable** → targeting is drifting to lower-quality segments. Tighten custom intent audiences. Increase retargeting allocation. Reduce lookalike percentage.
  - **Budget underdelivering on retargeting** → remarketing audience is too small. The cold campaigns are not driving enough traffic. Investigate cold campaign performance first.
- Receive 3 ranked hypotheses with expected impact and risk level
- If risk = "high" (budget changes >20%, audience targeting changes >50% of traffic), send Slack alert for human approval

**Experimentation (triggered by hypothesis acceptance):**
- Take the top-ranked hypothesis
- Design the experiment:
  - For creative tests: generate new variants via the AI pipeline, upload as new ads in a dedicated test ad group, split traffic
  - For landing page tests: use PostHog feature flags to show different page elements to display traffic
  - For audience tests: create a new ad group with the hypothesized targeting, allocate 15% of campaign budget for 2 weeks
  - For placement tests: add/remove managed placements in a test ad group
  - For bid strategy tests: use Google Ads campaign experiments to test Target CPA vs Maximize Conversions at different target levels
- Set minimum experiment duration: 7 days or 50+ conversions per variant (display needs more volume due to lower conversion rates)
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
# Display Ads Optimization Brief — Week of {date}

## Performance Summary
| Metric | This Week | 30-Day Avg | Trend | Status |
|--------|-----------|------------|-------|--------|
| CPA | ${X} | ${Y} | {arrow} | {normal/alert} |
| CTR (GDN) | {X}% | {Y}% | {arrow} | {normal/alert} |
| CTR (Meta) | {X}% | {Y}% | {arrow} | {normal/alert} |
| Qualified Leads | {X} | {Y}/wk avg | {arrow} | {normal/alert} |
| ICP Match Rate | {X}% | {Y}% | {arrow} | {normal/alert} |
| Frequency (GDN) | {X} | {Y} | {arrow} | {normal/alert} |
| Spend | ${X} | ${Y}/wk avg | — | — |

## Anomalies Detected: {count}
{Description of each anomaly and what was done}

## Experiments
| Experiment | Status | Hypothesis | Result |
|-----------|--------|------------|--------|
| {name} | {running/completed/reverted} | {hypothesis} | {outcome} |

## Placement Health
- Placements excluded this week: {count}
- Top 5 converting placements: {list}
- Worst 5 by spend-without-conversion: {list}

## Creative Pipeline
- Active creatives: {count} (GDN), {count} (Meta)
- Staging queue depth: {count} variants
- Creatives rotated this week: {count}
- Estimated days until pipeline runs dry: {days}

## Net Impact This Week
{Net CPA change, net conversion rate change from all adopted experiments}

## Convergence Status
{Distance from estimated local maximum. Successive experiment improvement rate.}

## Recommended Human Actions
{Only items requiring human approval. Empty if agent is handling everything.}
```

### 2. Build the display-ads-specific monitoring layer

Run the `autonomous-optimization` drill to extend the autonomous optimization loop with display-specific monitoring:

- **Automated placement curation (weekly):** Continue the weekly placement audit from Scalable, now fully automated. The agent excludes junk placements, researches new managed placement candidates (using Clay to identify industry publications), and logs every change.
- **Creative fatigue detection and rotation (daily):** Monitor each creative's CTR over time. When CTR declines >25% from peak or creative age exceeds 21 days, auto-pause and promote the next variant from the staging queue. If the staging queue has fewer than 3 variants, trigger the AI creative generation pipeline.
- **Audience exhaustion monitoring (weekly):** Track frequency and impression-per-day trends for each audience segment. Detect when a segment is saturated (frequency >6 on GDN, >4 on Meta, or impressions declining >15% week-over-week). Recommend audience expansion or rotation.
- **Cross-platform arbitrage detection (weekly):** Compare CPA for the same creative concept across GDN and Meta. If one platform delivers >30% better CPA for the same concept, shift 10% of budget to the winning platform. Track platform-level ROAS trends.
- **Lead quality monitoring (weekly):** Pull ICP match rates from Attio for display-sourced leads. If ICP match rate drops below 45%, flag as quality degradation and trigger a diagnosis focused on audience targeting, not creative.

### 3. Build the executive dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard for ongoing visibility:

- **Row 1 (headline metrics):** Monthly qualified leads, CPA (30-day rolling), total monthly spend, blended ROAS
- **Row 2 (trend charts):** Weekly CPA trend (13 weeks), weekly lead volume trend, ICP match rate trend
- **Row 3 (platform split):** GDN vs Meta: spend, qualified leads, CPA, CTR side by side
- **Row 4 (campaign type split):** Managed placements vs custom intent vs retargeting vs lookalike: spend, leads, CPA
- **Row 5 (funnel):** Display click > landing page view > scroll 50% > form view > form submit > lead qualified > meeting booked
- **Row 6 (experiments):** Active experiments, recent experiment results, cumulative improvement from experiments
- **Row 7 (creative health):** Active creative count, average creative age, staging queue depth, creative rotation history
- **Alerts configured:**
  - CPA >140% of 30-day average for 2 consecutive days
  - Weekly qualified lead volume <60% of 4-week average
  - Landing page conversion rate <50% of baseline
  - Monthly spend on pace to exceed budget by >10%
  - Creative staging queue drops below 3 variants
  - ICP match rate drops below 45%

### 4. Implement guardrails

The following guardrails are critical for autonomous operation. Build them into the n8n workflows:

- **Budget guardrail:** Agent cannot increase total monthly display spend by more than 20% without human approval. Cannot exceed hard cap set in campaign settings.
- **Rate limit:** Maximum 1 active experiment per platform at a time. Never stack experiments on the same platform.
- **Revert threshold:** If any experiment causes CPA to spike >40% above 30-day average during the test period, auto-revert immediately and log the failure.
- **Placement guardrail:** Agent can exclude placements freely but cannot add new managed placements without human approval (prevents brand safety risk).
- **Creative guardrail:** Agent can rotate approved creatives from the staging queue but cannot deploy unapproved creative copy (all AI-generated copy must be approved by human before entering the queue).
- **Audience guardrail:** Agent cannot remove an audience segment that is currently producing >30% of qualified leads without human approval.
- **Cooldown:** After a failed experiment (reverted), wait 7 days before testing a new hypothesis on the same variable.
- **Monthly experiment cap:** Maximum 4 experiments per month per platform. If all 4 fail on a platform, pause optimization for that platform and flag for human strategic review.
- **Quality guardrail:** If ICP match rate drops below 40% for 2 consecutive weeks, auto-pause the lowest-quality campaign (by ICP match rate) and alert human.
- **Human approval required for:** Budget increases >20%, adding new managed placements, deploying new creative copy, changes to geographic targeting, removing any audience segment.

### 5. Detect convergence

The autonomous optimization loop should detect when successive experiments produce diminishing returns. Track:
- Improvement magnitude of each adopted experiment (% CPA reduction or % conversion rate increase)
- When 3 consecutive experiments produce <2% improvement, the play has reached its local maximum

At convergence:
1. Reduce monitoring frequency from daily to every-other-day (anomaly detection still runs, but hypothesis generation slows)
2. Reduce experiment frequency from 2-4/month to 1/month (maintenance experiments to ensure the maximum holds)
3. Reduce creative generation frequency from bi-weekly to monthly (maintain the queue but do not over-produce)
4. Report: "Display ads play has converged. Current CPA: ${X}. Monthly qualified leads: {Y}. ICP match rate: {Z}%. Further gains require strategic changes: new audience categories, new platforms (programmatic via DV360/Trade Desk), or product/offer changes."

### 6. Handle seasonal and market shifts

Display ad performance fluctuates with seasons, industry events, and competitive dynamics. Build detection for:
- **Seasonal CPM spikes:** Q4 sees higher display CPMs as e-commerce advertisers flood the GDN. Agent should detect CPM trend upward in October and proactively tighten targeting or reduce budget to maintain CPA.
- **Audience behavior shifts:** If in-market audience sizes change significantly (Google updates audience definitions periodically), detect the change and adapt. If a key in-market category shrinks, expand to adjacent categories.
- **Placement quality drift:** Industry publications change their ad inventory quality over time (more ads, worse positions). If a previously top-performing managed placement degrades, auto-exclude and research replacements.
- **Cross-platform dynamics:** If Meta raises CPMs (common around elections, holidays), the agent should detect and shift budget to GDN if GDN CPAs remain stable.

**Human action required:** Review weekly optimization briefs. Approve high-risk changes flagged by the agent. Conduct monthly strategic reviews: is display still the right allocation of budget vs other plays? Should the play expand to programmatic display (DV360, Trade Desk) for premium inventory access?

## Time Estimate

- 20 hours: Deploy autonomous optimization loop (n8n workflows, PostHog anomaly detection, hypothesis generation pipeline)
- 12 hours: Build display-ads-specific monitoring layer (placement curation, creative fatigue, audience exhaustion, cross-platform arbitrage)
- 8 hours: Build executive dashboard and alert system
- 8 hours: Implement guardrails, convergence detection, and seasonal handling
- 40 hours: Agent operation over 6 months (automated, but requires compute)
- 40 hours: Human oversight over 6 months (~1.5 hrs/week reviewing briefs, approving changes)
- 12 hours: Monthly strategic reviews and agent tuning (3 hrs/mo for 4 months, front-loaded)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads | Display campaigns (GDN) | $6,000-8,000/mo ad spend -- [ads.google.com](https://ads.google.com) |
| Meta Ads | Audience Network display | $2,000-4,000/mo ad spend -- [ads.meta.com](https://ads.meta.com) |
| PostHog | Analytics, experiments, anomaly detection, dashboards | Growth ~$50-200/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Workflow automation (optimization loop, monitoring, creative pipeline) | Pro EUR 60/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API (Claude) | Hypothesis generation, experiment evaluation, creative generation, weekly briefs | ~$40-100/mo -- [anthropic.com](https://console.anthropic.com) |
| Clay | Lead enrichment, placement research | Explorer $149/mo -- [clay.com/pricing](https://clay.com/pricing) |
| Attio | CRM, experiment log, creative rotation audit trail, campaign records | Plus $29/user/mo -- [attio.com/pricing](https://attio.com/pricing) |
| Loops | Email nurture sequences | Starter $49/mo -- [loops.so/pricing](https://loops.so/pricing) |
| Webflow | Landing pages | CMS $23/mo -- [webflow.com/pricing](https://webflow.com/pricing) |

**Estimated play-specific cost:** $8,000-12,000/mo ad spend + ~$400-600/mo tooling + ~$40-100/mo AI compute

## Drills Referenced

- `autonomous-optimization` -- The core always-on optimization loop: monitor metrics, detect anomalies, generate hypotheses, run A/B experiments, evaluate results, auto-implement winners, produce weekly briefs
- `autonomous-optimization` -- Display-specific monitoring: automated placement curation, creative fatigue detection and rotation, audience exhaustion tracking, cross-platform arbitrage, lead quality monitoring
- `dashboard-builder` -- PostHog dashboard with real-time display ads KPIs, platform comparison, campaign type breakdown, creative health, and experiment tracking
