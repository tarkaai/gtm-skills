---
name: github-sample-teaser-durable
description: >
  GitHub Sample Teaser — Durable Intelligence. Always-on AI agents monitor repo
  performance, detect anomalies, generate improvement hypotheses, run A/B
  experiments on README and promotion strategy, auto-implement winners, and
  produce weekly optimization briefs. Converges when successive experiments
  yield less than 2% improvement.
stage: "Marketing > Problem Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving: >=150 stars and >=1,000 unique visitors and >=15 leads per 2-month rolling window for 6 months, via continuous agent-driven optimization. Convergence declared when 3 consecutive experiments produce <2% improvement."
kpis: ["Unique repo visitors (2-month rolling)", "Stars gained (2-month rolling)", "README CTA click-through rate", "Leads attributed to GitHub (2-month rolling)", "Experiments run", "Net metric change from optimization"]
slug: "github-sample-teaser"
install: "npx gtm-skills add marketing/problem-aware/github-sample-teaser"
drills:
  - autonomous-optimization
---

# GitHub Sample Teaser — Durable Intelligence

> **Stage:** Marketing > Problem Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Outcomes

The play runs itself. AI agents continuously monitor GitHub repo performance, diagnose when metrics plateau or drop, generate hypotheses, run experiments, and auto-implement winners. The goal is to find the local maximum -- the best possible traffic, stars, and lead conversion given the current keyword landscape and developer audience -- and maintain it as conditions change. The play is at convergence when 3 consecutive experiments produce less than 2% improvement.

## Leading Indicators

- Autonomous optimization loop running without human intervention for 4+ consecutive weeks
- At least 1 experiment per month producing a measurable improvement
- Weekly optimization briefs generated and posted to Slack on time
- No metric drops >20% that persist for more than 1 week (the agent detects and corrects)
- Anomaly detection fires within 24 hours of a significant metric change

## Instructions

### 1. Build the GitHub performance monitoring dashboard

Run the `autonomous-optimization` drill, Step 1:

Create a PostHog dashboard named "GitHub Sample Teaser - Performance" with:

**Traffic panels:**
- Line chart: daily unique repo visitors over last 90 days
- Line chart: daily clones (total and unique) over last 90 days
- Counter: current total star count
- Line chart: stars gained per week over last 90 days

**Conversion panels:**
- Funnel: `github_repo_views` -> `github_readme_cta_clicked` -> `github_signup_completed`
- Line chart: weekly CTA click-through rate
- Counter: total leads with `first_touch_channel = github`

**Referral panels:**
- Table: top referral sources by unique visitors (last 30 days)
- Bar chart: views by referrer over time

**Engagement panels:**
- Counter: issues opened this month
- Counter: PRs opened this month
- Counter: forks this month

### 2. Configure anomaly detection alerts

Run the `autonomous-optimization` drill, Step 2:

Set PostHog alerts for:
- **Views drop:** Weekly unique views drops >30% vs 4-week rolling average
- **Stars stall:** Zero new stars for 2 consecutive weeks
- **Clone spike:** Daily clones >3x the 2-week average (viral moment -- capitalize immediately)
- **CTA rate drop:** Weekly CTA click-through rate drops >25% vs 4-week average
- **Referrer disappearance:** A top-3 referral source drops to zero (broken link or deindexed page)

### 3. Connect the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on optimization cycle:

**Phase 1 -- Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check the play's primary KPIs: unique visitors, stars gained, CTA click-through rate, leads
2. Compare last 2 weeks against 4-week rolling average
3. Classify: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If normal: log to Attio, no action
5. If anomaly detected: trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**
1. Gather context: current README version, recent releases, referral source data, topic list, competitor repo changes
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` with the anomaly data + context
4. Receive 3 ranked hypotheses. Examples specific to this play:
   - "README CTA conversion dropped because a competitor repo released a similar sample that ranks higher -- update keywords and differentiate the problem statement"
   - "Traffic plateaued because the repo has not had a release in 6 weeks -- publish a release to re-engage stargazers"
   - "Clone spike from Hacker News referral -- post a follow-up comment on the HN thread linking to a deeper tutorial"
5. Store hypotheses in Attio
6. If top hypothesis risk = "high": send Slack alert for human review and STOP
7. If risk = "low" or "medium": proceed to Phase 3

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using `posthog-experiments`:
   - README CTA experiments: create branch with variant README, swap default branch for 50% of the evaluation period
   - Topic/keyword experiments: update topics and measure search ranking changes over 2 weeks
   - Promotion experiments: test different social post formats or channels
2. Set minimum duration: 7 days or 200+ unique visitors per variant, whichever is longer
3. Log experiment start in Attio

**Phase 4 -- Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation`:
   - **Adopt:** primary metric improved by >=5% with 95% confidence. Update the live configuration.
   - **Iterate:** result is directionally positive but not significant. Generate a refined hypothesis. Return to Phase 2.
   - **Revert:** variant performed worse. Restore control. Return to Phase 1.
   - **Extend:** insufficient data. Keep running for another evaluation period.
3. Store the full evaluation in Attio

**Phase 5 -- Report (weekly via n8n cron, Mondays 9am):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate a weekly brief:
   - What changed and why
   - Net impact on visitors, stars, CTA rate, leads
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 4. Guardrails

- **Maximum 1 active experiment at a time.** Never stack experiments.
- **Auto-revert if CTA click-through rate drops >30%** during any experiment.
- **Human approval required for:** changes to the sample code itself, changes to pricing or product CTA URLs, any experiment the hypothesis generator flags as "high risk."
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing the same variable.
- **Maximum 4 experiments per month.** If all 4 fail, pause optimization and flag for human strategic review.

### 5. Detect convergence

When 3 consecutive experiments produce <2% improvement:
1. The play has reached its local maximum
2. Reduce monitoring frequency from daily to weekly
3. Generate a convergence report: "This play is optimized. Current performance: [metrics]. Further gains require strategic changes (new sample repos targeting different keywords, product changes, new channels) rather than tactical optimization of this repo."

## Time Estimate

- 20 hours: dashboard and anomaly detection setup
- 20 hours: autonomous optimization loop development and testing
- 10 hours/month x 6 months: monitoring, reviewing briefs, approving high-risk experiments
- 20 hours: convergence analysis and strategic recommendations

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Repository hosting, traffic API, webhooks | Free for public repos ([github.com/pricing](https://github.com/pricing)) |
| PostHog | Dashboard, anomaly detection, experiments, funnels | Free tier to ~$100/month depending on event volume ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop scheduling and orchestration | Cloud Pro: EUR60/month ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Claude for hypothesis generation, experiment evaluation, weekly briefs | Sonnet 4.6: $3/$15 per M tokens; ~$20-40/month at Durable volume ([claude.com/pricing](https://claude.com/pricing)) |
| Attio | Campaign records, hypothesis storage, audit trail | Included in standard stack |

**Estimated monthly cost at Durable level: $80-200** (PostHog + n8n + Claude API)

## Drills Referenced

- `autonomous-optimization` -- the core monitor > diagnose > experiment > evaluate > implement loop that finds the local maximum
- `autonomous-optimization` -- PostHog dashboard, anomaly alerts, and weekly digest specific to GitHub metrics
