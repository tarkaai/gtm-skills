---
name: q-a-sites-stackoverflow-etc-durable
description: >
  Q&A Site Authority -- Durable Intelligence. Autonomous agents monitor answer performance,
  detect metric anomalies, generate improvement hypotheses, run experiments, and auto-implement
  winners. Converges on the local maximum for Q&A-driven pipeline.
stage: "Marketing > Problem Aware"
motion: "CommunitiesForums"
channels: "Other"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving profile clicks and leads over 6 months; successive optimization experiments produce <2% improvement (convergence reached)"
kpis: ["Profile views", "Profile click rate"]
slug: "q-a-sites-stackoverflow-etc"
install: "npx gtm-skills add marketing/problem-aware/q-a-sites-stackoverflow-etc"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Q&A Site Authority -- Durable Intelligence

> **Stage:** Marketing > Problem Aware | **Motion:** CommunitiesForums | **Channels:** Other

## Outcomes

Pass threshold: Sustained or improving profile clicks and leads over 6 months. The play has converged when 3 consecutive optimization experiments produce <2% improvement -- the local maximum has been found.

This is the always-on, self-optimizing level. The agent runs the full monitor-diagnose-experiment-evaluate-implement loop autonomously. Human involvement drops to reviewing weekly optimization briefs and approving high-risk changes. The system continuously adapts to shifting platform dynamics (new tags trending, competitor answers, algorithm changes) without manual intervention.

## Leading Indicators

- Optimization loop running without human intervention for 2+ consecutive weeks
- Experiment win rate >= 40% (4 out of 10 experiments produce measurable improvement)
- Stack Overflow reputation growing at >= 50 points/week on autopilot
- Referral sessions stable or growing month-over-month
- No platform bans, rate-limit warnings, or quality flags
- Weekly optimization brief delivered on time with actionable insights

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play:

**Phase 1 -- Monitor (daily via n8n cron):**
The agent checks the play's primary KPIs using `posthog-anomaly-detection`:
- Referral sessions from Q&A platforms (7-day rolling vs 4-week average)
- Profile click rate (profile views / answer impressions)
- Lead conversion rate (signups / referral sessions)
- Answer quality score (average upvotes per answer, acceptance rate)
- Reputation growth rate

Classify each metric: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase).

If all normal: log to Attio, no action.
If anomaly detected: trigger Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**
The agent gathers context:
1. Pulls 8-week metric history from PostHog.
2. Reviews current answer strategy: tags targeted, platforms, answer frequency, format distribution, link strategy.
3. Checks for external factors: Did Stack Overflow change ranking algorithm? Did a competitor start answering in your tags? Did question volume in your tags change?
4. Runs `hypothesis-generation` with the anomaly data and context.
5. Receives 3 ranked hypotheses. Examples:
   - "Profile clicks dropped 25% because answer format shifted too code-heavy; hypothesis: add more explanatory context to increase time-on-answer and profile curiosity."
   - "Referral traffic plateaued; hypothesis: expand to 3 new Stack Exchange sites where our tags have high question volume but low competition."
   - "Lead conversion dropped; hypothesis: the landing page visitors reach from Q&A profiles does not match their intent. Test a dedicated Q&A-sourced landing page."
6. If top hypothesis is high-risk (e.g., changes affecting >50% of answer strategy): send Slack alert for human review. Stop.
7. If low/medium risk: proceed to Phase 3.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
The agent designs and runs the experiment:
1. Creates a PostHog feature flag or experiment to split traffic between control and variant.
2. Implements the variant. Examples:
   - Change answer format for the next 20 answers (variant) while maintaining current format for another 20 (control).
   - Expand to 3 new Stack Exchange sites (variant) while maintaining current sites (control).
   - Deploy a dedicated Q&A landing page for variant traffic.
3. Sets experiment duration: minimum 7 days or until 50+ answers per variant.
4. Logs experiment details in Attio: hypothesis, start date, success criteria.

**Phase 4 -- Evaluate (triggered by experiment completion):**
The agent runs `experiment-evaluation`:
- **Adopt**: Variant outperforms control with statistical significance. Update live strategy. Log the change.
- **Iterate**: Results inconclusive or partially positive. Generate a refined hypothesis. Return to Phase 2.
- **Revert**: Variant underperforms. Restore control. Log the failure. Return to Phase 1.
- **Extend**: Not enough data. Run for another period.

All evaluation data stored in Attio with full reasoning.

**Phase 5 -- Report (weekly via n8n cron):**
The agent generates a weekly optimization brief:
- Anomalies detected this week
- Experiments running, completed, or planned
- Net impact on KPIs from adopted changes
- Current performance vs Scalable baseline
- Estimated distance from local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Deploy comprehensive dashboards

Run the `dashboard-builder` drill to create the Durable-level PostHog dashboard:

**Panel 1: Q&A Pipeline Attribution**
- Full funnel: `qa_referral_visit` -> `page_viewed` -> `qa_signup` -> `qa_meeting_booked` -> `deal_created`
- Breakdown by platform and tag

**Panel 2: Answer Quality Trends**
- Line chart: average upvotes per answer (7-day rolling)
- Line chart: acceptance rate (7-day rolling)
- Comparison to 4-week baseline

**Panel 3: Platform Performance Matrix**
- Table: each platform x (answers posted, upvotes earned, referral sessions, signups, cost)
- Sorted by efficiency (leads per hour invested)

**Panel 4: Experiment History**
- Table: all experiments with hypothesis, variant, result, and net impact
- Running tally of cumulative improvement from adopted experiments

**Panel 5: Convergence Tracker**
- Line chart: improvement percentage from each successive experiment
- Horizontal line at 2% threshold (convergence boundary)
- When 3 consecutive experiments fall below this line, the play has reached its local maximum

### 3. Run the Q&A authority performance monitor

Run the `autonomous-optimization` drill in always-on mode:

1. Daily: track answer performance, reputation growth, profile click metrics.
2. Weekly: generate comprehensive report with platform breakdown.
3. Feed all performance data into the `autonomous-optimization` loop as input for anomaly detection and hypothesis generation.

### 4. Manage convergence

When the optimization loop detects convergence (<2% improvement for 3 consecutive experiments):

1. The agent reduces monitoring frequency from daily to weekly.
2. Generates a convergence report: "Q&A Site Authority has reached its local maximum. Current steady-state: X profile clicks/week, Y leads/month, Z reputation growth/month."
3. Recommends strategic pivots for further growth (outside the scope of tactical optimization): new product domains to answer about, partnerships with other answerers, creating canonical reference answers, or launching a dedicated Q&A community.
4. The play shifts to maintenance mode: weekly monitoring, answer existing questions at steady cadence, respond to anomalies only.

## Time Estimate

- Autonomous optimization setup (n8n workflows, PostHog experiments): 8 hours
- Dashboard build: 3 hours
- Weekly brief review (15 min/week x 26 weeks): 6.5 hours
- Experiment approval for high-risk changes: ~2 hours total
- Ongoing answer operations (agent-automated, human spot-checks): 50 hours over 6 months
- Performance monitoring setup and tuning: 4 hours
- Total: ~73 hours of human time; remainder is agent compute time

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Stack Exchange API | Read/write across SE sites | Free (10,000 req/day) |
| Dev.to API | Read and publish articles | Free |
| SerpAPI | Quora monitoring | ~$50-75/mo ([serpapi.com/pricing](https://serpapi.com/pricing)) |
| Syften | Real-time keyword monitoring across platforms | $40-100/mo ([syften.com](https://syften.com)) |
| Common Room | Community intelligence, signal aggregation (optional) | From $1,000/mo ([commonroom.io/pricing](https://www.commonroom.io/pricing/)) |
| PostHog | Attribution, experiments, anomaly detection, dashboards | Free tier or ~$0 at this volume ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop automation, scheduling | Free self-hosted or from $20/mo cloud ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM, experiment log, performance tracking | Included in standard stack |
| Anthropic API | Hypothesis generation, answer drafting, experiment evaluation | ~$20-50/mo ([anthropic.com/pricing](https://anthropic.com/pricing)) |

Estimated play-specific cost: $110-265/mo (without Common Room); $1,110-1,265/mo (with Common Room)

Common Room is optional at Durable level. It aggregates signals across Q&A platforms, GitHub, Slack, and social into a unified view, which can accelerate hypothesis generation. For most teams, PostHog + Syften + n8n is sufficient.

## Drills Referenced

- `autonomous-optimization` -- the core monitor-diagnose-experiment-evaluate-implement loop that finds the local maximum
- `autonomous-optimization` -- daily answer tracking, reputation growth, and attribution reporting
- `dashboard-builder` -- Durable-level PostHog dashboards with convergence tracking
