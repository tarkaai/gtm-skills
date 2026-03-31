---
name: open-source-content-release-durable
description: >
  Open Source Content Release — Durable Intelligence. Autonomous agents monitor repo performance,
  detect anomalies, generate improvement hypotheses, run experiments on README copy, release
  timing, and community engagement strategies, then auto-implement winners. The optimization loop
  converges when successive experiments produce <2% improvement.
stage: "Marketing > Solution Aware"
motion: "Content"
channels: "Communities, Social, Content"
level: "Durable Intelligence"
time: "8 hours setup + autonomous ongoing"
outcome: "Sustained star growth (>=10% QoQ), >=5% OSS-to-signup conversion rate, and convergence of the optimization loop (successive experiments <2% improvement) over 12 months"
kpis: ["Quarter-over-quarter star growth rate", "OSS-to-signup conversion rate", "Experiment win rate", "Autonomous optimization cycle time", "Lead quality score"]
slug: "open-source-content-release"
install: "npx gtm-skills add marketing/solution-aware/open-source-content-release"
drills:
  - autonomous-optimization
---

# Open Source Content Release — Durable Intelligence

> **Stage:** Marketing > Solution Aware | **Motion:** Content | **Channels:** Communities, Social, Content

## Outcomes

An always-on agent loop monitors all OSS repo metrics, detects when performance plateaus or drops, generates hypotheses for improvement, runs A/B experiments, evaluates results, and auto-implements winners. The play sustains >=10% quarter-over-quarter star growth and achieves >=5% OSS-to-signup conversion. The loop converges to the local maximum -- the best possible performance given the current market, audience, and competitive landscape.

## Leading Indicators

- Anomaly detection firing within 24 hours of any significant metric change
- At least 1 experiment running per month across the repo portfolio
- Weekly optimization briefs generating without manual intervention
- Experiment win rate >=30% (at least 1 in 3 hypotheses produces measurable improvement)
- Time-to-convergence: successive experiments producing diminishing returns signals the play is near its local maximum

## Instructions

### 1. Deploy the performance monitoring system

Run the `autonomous-optimization` drill to build a comprehensive monitoring layer for all OSS repos. This produces:

**PostHog dashboard ("OSS Content Release - Performance"):**
- Line chart: daily repo views (total + unique) per repo, last 90 days
- Line chart: daily clones (total + unique) per repo, last 90 days
- Counter: total star count per repo + portfolio total
- Line chart: stars gained per week per repo, last 90 days
- Funnel: `oss_repo_viewed` -> `oss_readme_cta_clicked` -> `oss_signup_completed`
- Line chart: weekly CTA click-through rate per repo
- Table: top referral sources by unique visitors, last 30 days
- Counter: issues opened, PRs opened, forks this month per repo

**Anomaly detection alerts:**
- Weekly unique views drops >30% vs 4-week rolling average
- Zero new stars for 2 consecutive weeks
- Daily clones spike >3x the 2-week average (possible viral moment -- capitalize immediately)
- Weekly CTA click-through rate drops >25% vs 4-week average
- A top-3 referral source drops to zero (broken link or deindexed content)

**Weekly digest workflow (n8n, Monday 9am):**
- Query PostHog for last 7 days of all OSS metrics
- Compare each metric to prior week and 4-week average
- Classify each metric: UP (>10% above average), STABLE (within 10%), DOWN (>10% below average)
- Format and post to Slack, store in Attio

When an anomaly fires, the performance monitor packages the anomaly data (metric, current value, expected value, deviation %) along with recent context (last 4 weeks of data, recent repo changes, recent releases) and passes this bundle to the autonomous optimization drill.

### 2. Connect the autonomous optimization loop

Run the `autonomous-optimization` drill. This is the core loop that makes Durable fundamentally different. It operates in 5 phases:

**Phase 1 -- Monitor (daily via n8n cron):**
Check all OSS play KPIs via PostHog anomaly detection. Compare last 2 weeks against 4-week rolling average. Classify: normal, plateau (within ±2% for 3+ weeks), drop (>20% decline), spike (>50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**
Gather the repo's current configuration from Attio (README version, CTA copy, release frequency, active promotion channels). Pull 8-week metric history from PostHog. Run `hypothesis-generation` with anomaly data + context. Receive 3 ranked hypotheses with expected impact and risk.

Example hypotheses the agent generates for this play:
- "README CTA conversion dropped because the Quick Start section got longer after v1.3 release, pushing the CTA below the fold. Shorten Quick Start by 40%."
- "Star growth plateaued because the monthly release cadence shipped only patch fixes. Ship a minor feature release to generate social buzz."
- "Referral traffic from dev.to dropped to zero. The companion article may have been deindexed. Republish with updated content."

If top hypothesis risk = high, send Slack alert for human review and stop. If risk = low or medium, proceed to Phase 3.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
Implement the top hypothesis as an A/B experiment. For README changes, use branch-swapping with PostHog tracking. For release timing changes, compare star bumps between release schedules. For community promotion changes, alternate strategies bi-weekly and compare referral traffic.

Minimum experiment duration: 7 days or 100+ samples per variant, whichever is longer. Log experiment start in Attio.

**Phase 4 -- Evaluate (triggered by experiment completion):**
Pull experiment results from PostHog. Run `experiment-evaluation` with control vs variant data. Decision:
- **Adopt:** Implement the winning variant permanently. Log the change.
- **Iterate:** Generate a new hypothesis building on this result. Return to Phase 2.
- **Revert:** Restore control. Log the failure. Return to Phase 1.
- **Extend:** Keep the experiment running for another period if inconclusive.

**Phase 5 -- Report (weekly via n8n cron):**
Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made. Calculate net metric change from adopted changes. Generate a weekly optimization brief:
- What changed and why
- Net impact on star growth, CTA conversion, and lead generation
- Current distance from estimated local maximum
- Recommended focus for next week

Post to Slack. Store in Attio.

### 3. Configure guardrails

Apply these safety limits to the autonomous loop:

- **Rate limit:** Maximum 1 active experiment per repo at a time. Never stack experiments.
- **Revert threshold:** If CTA conversion drops >30% at any point during an experiment, auto-revert immediately.
- **Human approval required for:** Changes to the repo's core code or functionality (not just README/docs), any experiment that would modify the Quick Start instructions, budget changes >20%.
- **Cooldown:** After a failed experiment, wait 7 days before testing a new hypothesis on the same variable.
- **Maximum experiments per month:** 4 per repo. If all 4 fail, pause and flag for human strategic review.
- **Never optimize unmeasured metrics:** If a KPI lacks PostHog tracking, fix tracking first before running experiments.

### 4. Detect convergence

The optimization loop runs indefinitely. However, it detects convergence -- when successive experiments produce diminishing returns:

- If 3 consecutive experiments produce <2% improvement, the repo has reached its local maximum
- Reduce monitoring frequency from daily to weekly
- Generate a convergence report: "This repo is optimized. Current performance: [stars/week], [CTA conversion %], [leads/month]. Further gains require strategic changes (new repo targeting different keywords, product changes that unlock new OSS assets, or expansion to new developer communities) rather than tactical optimization."

When convergence is reached, shift optimization effort to other repos in the portfolio or re-run the oss content selection workflow (see instructions below) to identify the next asset to release.

### 5. Sustain and compound

While the optimization loop runs, maintain these ongoing activities:
- Monthly releases continue automatically via the Scalable-level automation
- Issue triage continues via the automated workflow
- Community content continues on the bi-weekly cadence
- New repos launched quarterly extend the portfolio and the search surface

The compounding effect: each new repo benefits from the existing automation infrastructure (issue triage, release cadence, cross-posting) and the optimization learnings from previous repos.

## Time Estimate

- Performance monitor setup: 3 hours
- Autonomous optimization loop configuration: 3 hours
- Guardrail configuration: 1 hour
- Ongoing: 1 hour/month reviewing weekly briefs and approving high-risk experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Host repos, webhooks, releases, Traffic API | Free for public repos |
| PostHog | Dashboards, anomaly detection, experiments, funnels | Free up to 1M events/mo (https://posthog.com/pricing) |
| n8n | Monitoring cron, optimization loop workflows, cross-posting | Free self-hosted or from EUR 20/mo cloud (https://n8n.io/pricing) |
| Anthropic | Claude API for hypothesis generation, issue triage, experiment evaluation | Pay-per-use, ~$3/1M input tokens (https://www.anthropic.com/pricing) |
| Attio | Campaign records, experiment audit trail, lead attribution | From $0/user/mo free tier (https://attio.com/pricing) |

**Play-specific cost:** ~$50-150/mo (n8n cloud + Anthropic API for optimization loop + issue triage)

_Your CRM, PostHog, and automation platform are not included -- standard stack paid once._

## Drills Referenced

- `autonomous-optimization` -- the core always-on loop: detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `autonomous-optimization` -- comprehensive monitoring dashboard, anomaly detection alerts, and weekly digest that feeds anomalies into the optimization loop
