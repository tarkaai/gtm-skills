---
name: paid-reddit-ads-durable
description: >
  Paid Reddit Ads — Durable Intelligence. Always-on AI agents run the autonomous optimization
  loop: detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate
  results, and auto-implement winners. Converges when experiments produce <2% improvement.
stage: "Marketing > Problem Aware"
motion: "LightweightPaid"
channels: "Paid, Social"
level: "Durable Intelligence"
time: "12 hours setup + continuous (6+ months)"
outcome: "Sustained or improving leads/meetings over 6 months with CPA trending flat or down; convergence detected when 3 consecutive experiments produce <2% improvement"
kpis: ["Cost per acquisition trend (4-week rolling)", "Return on ad spend", "Experiment win rate", "Weeks since last CPA improvement", "Autonomous optimization loop health"]
slug: "paid-reddit-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-reddit-ads"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Paid Reddit Ads — Durable Intelligence

> **Stage:** Marketing -> Problem Aware | **Motion:** LightweightPaid | **Channels:** Paid, Social

## Outcomes

The campaign runs itself. AI agents continuously monitor Reddit Ads performance, detect when metrics plateau or decline, generate hypotheses for improvement, run controlled experiments, and auto-implement winners. The goal is to find the local maximum — the best possible CPA and lead volume given your audience, creative approach, and competitive landscape — and maintain it as conditions change.

Success is not a fixed number. Success is: CPA stays flat or improves over 6 months without human intervention, and the system detects convergence (3 consecutive experiments produce <2% improvement), signaling the local maximum has been reached.

## Leading Indicators

- Autonomous optimization loop runs without errors for 7+ consecutive days
- At least 1 experiment launched per month (system is actively optimizing)
- Weekly optimization briefs generated and posted to Slack on schedule
- Anomaly detection catches CPA spikes within 24 hours
- No human intervention required for routine optimizations for 30+ consecutive days

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. This is the core of Durable. Configure it specifically for the paid-reddit-ads play:

**Monitor phase (daily via n8n cron):**
- Pull Reddit Ads metrics using the `reddit-ads-reporting` fundamental
- Pull PostHog conversion data for cross-reference
- Compare last 2 weeks against 4-week rolling average
- Classify: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- Variables to monitor: CPA, CTR, conversion rate, ROAS, lead quality (ICP match rate from Attio)
- If normal: log to Attio, no action
- If anomaly detected: trigger Diagnose phase

**Diagnose phase (triggered by anomaly):**
- Gather context: current subreddit targeting, active ad creative, bid levels, budget allocation, recent changes
- Pull 8-week metric history from PostHog
- Use Claude to generate 3 ranked hypotheses for the anomaly
- Example hypotheses for a CPA spike:
  - "Subreddit r/SaaS audience is saturated. Test replacing with r/indiehackers." (risk: medium)
  - "Top creative variant has fatigued after 4 weeks. Generate 3 new variants with a different hook." (risk: low)
  - "Competitor entered the same subreddits with lower-priced offer. Test new value proposition angle." (risk: medium)
- Store hypotheses in Attio as notes on the campaign record
- If top hypothesis is "high risk" (e.g., requires >20% budget change or complete targeting overhaul): send Slack alert for human review and STOP
- If "low" or "medium" risk: proceed to Experiment phase

**Experiment phase (triggered by hypothesis acceptance):**
- Design the experiment using PostHog feature flags:
  - Split traffic: 50% control (current configuration), 50% variant (hypothesis change)
  - For creative experiments: create new ad variants, run alongside current winners
  - For targeting experiments: create a new ad group with the proposed subreddit changes
  - For bid experiments: adjust bids in a test ad group
- Set experiment duration: minimum 7 days or 100+ samples per variant
- Log experiment start in Attio: hypothesis, start date, expected duration, success metric

**Evaluate phase (triggered by experiment completion):**
- Pull experiment results from PostHog and Reddit Ads
- Use Claude to evaluate: was the hypothesis correct? Is the improvement statistically significant?
- Decision:
  - **Adopt**: Variant CPA is >5% better than control with 95% confidence. Update the live campaign.
  - **Iterate**: Result is inconclusive or mixed. Generate a refined hypothesis and return to Diagnose.
  - **Revert**: Variant performed worse. Restore control configuration. Log the failure.
  - **Extend**: Not enough data yet. Continue for another 7 days.
- Store the full evaluation in Attio

**Report phase (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes this week
- Generate a weekly optimization brief:
  - What changed and why
  - Net impact on CPA, CTR, lead volume
  - Current distance from estimated local maximum (based on improvement trend)
  - Recommended focus for next week
- Post to Slack and store in Attio

### 2. Build the Durable performance dashboard

Run the `dashboard-builder` drill to create a Durable-level PostHog dashboard:

- **CPA trend (12-week rolling):** Shows convergence toward local maximum
- **Experiment tracker:** Active experiment, control vs. variant performance, days remaining
- **Experiment history:** All past experiments with outcomes (adopted/reverted/iterated)
- **ROAS by subreddit:** Which communities produce revenue, not just leads
- **Creative performance decay:** CTR curve for each active ad variant (detect fatigue before it impacts CPA)
- **Autonomous loop health:** Last run time, error count, days since last human intervention
- **Budget efficiency:** Spend vs. qualified leads vs. meetings vs. deals (full funnel)

### 3. Configure the Reddit Ads performance monitor for Durable

Run the `autonomous-optimization` drill with Durable-level settings:

- Reduce daily health check to a lightweight status check (is the loop running? any critical errors?)
- The autonomous-optimization loop handles the heavy analysis now
- Keep the weekly Attio logging for audit trail
- Add a monthly full-funnel attribution review: which Reddit-sourced leads became customers? What was the true ROAS including sales cycle?

### 4. Set Durable guardrails

These are non-negotiable safety limits for the autonomous loop:

- **Maximum 1 active experiment per ad group at a time.** Never stack experiments.
- **Revert threshold:** If CPA increases >30% during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Budget changes >20% in a single adjustment
  - Removing or adding more than 3 subreddits at once
  - Any change flagged "high risk" by the hypothesis generator
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing the same variable.
- **Maximum experiments per month:** 4 per play. If all 4 fail, pause optimization and flag for human strategic review.
- **Budget floor:** Never reduce total daily budget below 50% of the Scalable level average.

### 5. Detect convergence and adjust

The optimization loop runs indefinitely but should detect convergence:

- Track the improvement magnitude of each adopted experiment
- When 3 consecutive experiments produce <2% CPA improvement: the play has reached its local maximum
- At convergence:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment frequency from weekly to monthly (maintenance mode)
  3. Generate a convergence report: "Reddit Ads optimized. Current CPA: $X. ROAS: Y. Further gains require strategic changes (new channels, new product positioning, new market segments) rather than tactical optimization."
  4. Post the report to Slack and the Attio campaign record

### 6. Ongoing maintenance

Even after convergence, the system continues monitoring for:
- External shocks (competitor enters your subreddits, Reddit policy changes, market shifts)
- Seasonal patterns (budget adjustments for Q4, summer slowdowns)
- New subreddit opportunities (monthly scan for emerging communities)
- Platform changes (new Reddit ad formats, API updates, targeting options)

If an external shock causes CPA to spike >20% from the converged baseline, the system exits maintenance mode and resumes active optimization.

## Time Estimate

- Autonomous optimization loop setup: 6 hours
- Durable dashboard build: 2 hours
- Performance monitor Durable configuration: 1 hour
- Guardrail configuration: 1 hour
- Convergence detection setup: 1 hour
- Monthly maintenance review: 1 hour/month

**Total setup time: ~12 hours. Ongoing: 1 hour/month for human review of optimization briefs.**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Reddit Ads | Ad platform | $5,000-20,000/mo ad spend (agent-optimized). https://ads.reddit.com |
| PostHog | Analytics, experiments, feature flags, dashboards | Free up to 1M events, then $0.00031/event. https://posthog.com/pricing |
| n8n | Automation (optimization loop, monitoring, syncs) | Free self-hosted or $20/mo cloud. https://n8n.io/pricing |
| Anthropic API | Hypothesis generation and experiment evaluation | ~$30-50/mo at Durable frequency. https://www.anthropic.com/pricing |
| Attio | CRM for campaign records and audit trail | $29/user/mo Pro. https://attio.com/pricing |
| Clay | Lead enrichment for quality scoring | From $149/mo. https://clay.com/pricing |

**Estimated monthly cost: $5,230-20,300 (primarily ad spend). Agent compute: ~$50-70/mo.**

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor -> diagnose -> experiment -> evaluate -> implement
- `autonomous-optimization` — lightweight health checks and audit trail at Durable level
- `dashboard-builder` — Durable-level PostHog dashboard with experiment tracking and convergence visualization
