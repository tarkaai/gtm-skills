---
name: github-project-promotion-durable
description: >
  GitHub Project Promotion — Durable Intelligence. Always-on AI agents monitoring
  repo performance, detecting anomalies, generating improvement hypotheses, running
  A/B experiments on READMEs and promotion, and auto-implementing winners to find
  the local maximum of GitHub-sourced lead generation.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Communities, Social"
level: "Durable Intelligence"
time: "30 hours setup + ongoing autonomous operation over 12 months"
outcome: "Sustained star growth (≥15% QoQ) and ≥40 qualified leads/quarter from GitHub presence over 12 months via autonomous optimization"
kpis: ["Quarter-over-quarter star growth rate", "Qualified leads per quarter", "Experiment win rate", "CTA conversion rate trend", "Time to anomaly resolution"]
slug: "github-project-promotion"
install: "npx gtm-skills add marketing/solution-aware/github-project-promotion"
drills:
  - autonomous-optimization
---

# GitHub Project Promotion — Durable Intelligence

> **Stage:** Marketing → SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Communities, Social

## Outcomes

The agent autonomously monitors the full GitHub repo portfolio, detects when metrics plateau or drop, generates improvement hypotheses, runs experiments, evaluates results, and auto-implements winners. The goal is to find the local maximum — the best possible GitHub-sourced lead generation rate given the current market and competition — and maintain it as conditions change. Pass threshold: sustained star growth (≥15% QoQ) and ≥40 qualified leads/quarter over 12 months.

## Leading Indicators

- Anomaly detection firing within 24 hours of a meaningful metric shift (view drops, star stalls, referrer disappearance)
- At least 1 experiment running per month across the portfolio
- Experiment win rate ≥30% (at least 1 in 3 experiments produces a measurable improvement)
- Weekly optimization briefs generated on schedule without manual prompting
- CTA conversion rate trending upward or holding steady quarter over quarter
- Zero unresolved anomalies older than 14 days

## Instructions

### 1. Deploy the performance monitoring system

Run the `autonomous-optimization` drill to build comprehensive monitoring for the full repo portfolio:

**PostHog dashboard — "GitHub Project Promotion — Durable":**

Traffic panels:
- Line chart: daily views (total + unique) per repo over last 90 days
- Line chart: daily clones per repo over last 90 days
- Line chart: stars gained per week per repo over last 90 days
- Counter: total stars across portfolio

Conversion panels:
- Funnel: `github_repo_views` → `github_readme_cta_clicked` → `github_signup_completed` (or `github_demo_booked`)
- Line chart: weekly CTA click-through rate across portfolio
- Counter: total leads from GitHub this quarter

Referral panels:
- Table: top referral sources by unique visitors per repo (last 30 days)
- Bar chart: referral source traffic over time

Engagement panels:
- Counter: issues opened this month (automated vs manual responses)
- Counter: PRs opened this month
- Counter: releases published this month

**Anomaly detection alerts:**
- Views drop: weekly unique views drops >30% vs 4-week rolling average
- Stars stall: zero new stars for 2 consecutive weeks on any repo
- Clone spike: daily clones >3x the 2-week average (viral moment — capitalize immediately)
- CTA rate drop: weekly CTA click-through rate drops >25% vs 4-week average
- Referrer disappearance: a top-3 referral source drops to zero (broken link or removed mention)

**Weekly digest (n8n cron, every Monday 09:00 UTC):**
1. Query PostHog for 7-day metrics across all repos
2. Compare each metric to prior week and 4-week average
3. Classify: up (>10% above average), stable, down (>10% below average)
4. Format and post to Slack, store in Attio

### 2. Connect the autonomous optimization loop

Run the `autonomous-optimization` drill connected to the GitHub performance monitor:

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check portfolio KPIs: views, stars, clones, CTA clicks, leads
2. Compare last 2 weeks against 4-week rolling average
3. Classify: normal (within ±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
4. If normal: log to Attio, no action
5. If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
1. Pull context: current repo configurations (README version, topics, CTA copy, promotion cadence, recent releases)
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` with anomaly data + context. Example hypotheses:
   - "Star growth stalled because the last 3 releases had no new features — publish a feature update"
   - "CTA click rate dropped because a competitor published a better README — refresh CTA copy"
   - "Views dropped because the top referral blog post was updated and removed our link — reach out to author"
   - "Clone spike from a viral HN post — publish a follow-up post to sustain momentum"
4. Receive 3 ranked hypotheses with expected impact and risk
5. Store in Attio as notes on the campaign record
6. If top hypothesis risk = "high": send Slack alert for human review, STOP
7. If risk = "low" or "medium": proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Design the experiment based on the hypothesis type:
   - **README change:** create a branch with the variant README, swap default branch (A/B test over 2-week period)
   - **CTA copy change:** update the CTA block in the README, measure CTA click rate before vs after over 2 weeks
   - **Promotion change:** adjust posting cadence, channels, or content angle for 4 weeks and compare lead volume
   - **Release strategy change:** publish a feature-focused release vs a maintenance release and compare star/engagement impact
2. Log experiment start in Attio: hypothesis, start date, duration, success criteria
3. Minimum experiment duration: 14 days or 500+ repo views, whichever is longer
4. Use PostHog to track the variant's performance

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation` with control vs variant data
3. Decision:
   - **Adopt:** implement the winning change permanently. Update the live README/config. Log the change.
   - **Iterate:** the experiment showed a directional signal — generate a refined hypothesis. Return to Phase 2.
   - **Revert:** the variant performed worse. Restore the control. Log the failure. Return to Phase 1.
   - **Extend:** results are inconclusive (insufficient sample size). Keep running for another period.
4. Store full evaluation in Attio: decision, confidence interval, reasoning, net metric impact

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from adopted changes
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on stars, leads, CTA conversion rate
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack, store in Attio

### 3. Enforce guardrails

Configure these guardrails in the n8n optimization workflow:

- **Rate limit:** maximum 1 active experiment per repo at a time. Never stack experiments.
- **Revert threshold:** if CTA click rate drops >30% during an experiment, auto-revert immediately
- **Human approval required for:**
  - Changing the product CTA destination URL
  - Archiving or deleting a repo from the portfolio
  - Any change flagged "high risk" by the hypothesis generator
- **Cooldown:** after a failed experiment (revert), wait 7 days before testing a new hypothesis on the same variable
- **Maximum experiments per month:** 4 across the portfolio. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize what is not measured:** if a metric lacks PostHog tracking, fix tracking first before running experiments

### 4. Detect convergence

The optimization loop runs indefinitely. It should detect convergence — when successive experiments produce diminishing returns:

- Track improvement magnitude per experiment over time
- If 3 consecutive experiments produce <2% improvement each, the play has reached its local maximum
- At convergence:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment cadence from monthly to quarterly
  3. Report: "GitHub Project Promotion has reached its local maximum. Current performance: [stars/quarter], [leads/quarter], [CTA rate]. Further gains require strategic changes (new repo concepts, new developer audiences, product changes) rather than tactical optimization."

### 5. Evaluate sustainability

After 12 months, measure:

- Quarter-over-quarter star growth rate (target: ≥15% QoQ sustained)
- Qualified leads per quarter (target: ≥40)
- Total experiments run and win rate
- CTA conversion rate trajectory: improving, stable, or declining
- Time from anomaly detection to resolution (target: <14 days)
- Total leads generated over 12 months and cost per lead

This level runs continuously. Monthly review: which repos are driving leads, which are dead weight, what new repo concepts could expand the portfolio.

## Time Estimate

- 10 hours: PostHog dashboard and anomaly detection setup for full portfolio
- 8 hours: n8n workflow construction (daily monitoring, hypothesis pipeline, experiment management, weekly briefs)
- 4 hours: guardrail configuration and testing
- 3 hours: convergence detection logic
- 5 hours: first month of monitoring, tuning alert thresholds, reviewing initial hypotheses
- Ongoing: ~2 hours/month reviewing optimization briefs and approving high-risk experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Repository hosting, webhooks, traffic APIs | Free for public repos — https://github.com/pricing |
| PostHog | Dashboards, anomaly detection, experiment tracking, funnels | Free up to 1M events/mo — https://posthog.com/pricing |
| n8n | Optimization loop workflows (monitoring, experiments, reporting) | Cloud from $24/mo or free self-hosted — https://n8n.io/pricing |
| Anthropic (Claude) | Hypothesis generation, experiment evaluation, weekly briefs | ~$15-30/mo — https://anthropic.com/pricing |
| Attio | CRM for lead tracking, experiment audit trail, campaign records | Free up to 3 users — https://attio.com/pricing |

**Durable budget: n8n ~$24/mo + Claude API ~$15-30/mo = ~$40-55/mo** (other tools covered by free tiers or standard stack)

## Drills Referenced

- `autonomous-optimization` — the core monitor → diagnose → experiment → evaluate → implement loop that finds the local maximum. Detects metric anomalies, generates improvement hypotheses via Claude, runs A/B experiments, evaluates results, and auto-implements winners. Produces weekly optimization briefs. Converges when successive experiments yield <2% improvement.
- `autonomous-optimization` — comprehensive PostHog dashboard and anomaly detection system for the full repo portfolio: traffic, conversion, referral, and engagement metrics with weekly digests and anomaly-to-optimization pipeline
