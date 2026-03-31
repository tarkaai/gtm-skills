---
name: reddit-ama-series-durable
description: >
  Reddit AMA Series — Durable Intelligence. Agent-driven autonomous optimization of
  AMA topic selection, subreddit rotation, format experimentation, and content repurposing.
  Detects engagement decay, runs A/B experiments, and auto-implements winning formats to
  sustain referral traffic at or above the Scalable baseline for 6+ months.
stage: "Marketing > ProblemAware"
motion: "CommunitiesForums"
channels: "Social, Communities"
level: "Durable Intelligence"
time: "160 hours over 6 months"
outcome: "Sustained or improving referral sessions and signups over 6 months; never drops >20% below Scalable baseline (avg referral sessions per AMA) for 2+ consecutive sessions"
kpis: ["Referral sessions per AMA (rolling 4-session avg)", "Signups per AMA (rolling 4-session avg)", "Engagement trend (questions + upvotes per AMA)", "Content repurposing multiplier (total referral sessions / live AMA sessions)", "Optimization experiment win rate"]
slug: "reddit-ama-series"
install: "npx gtm-skills add marketing/problem-aware/reddit-ama-series"
drills:
  - autonomous-optimization
  - community-health-scoring
---

# Reddit AMA Series — Durable Intelligence

> **Stage:** Marketing → ProblemAware | **Motion:** CommunitiesForums | **Channels:** Social, Communities

## Outcomes

Make the AMA series self-sustaining through autonomous optimization. The agent monitors session-over-session performance, detects engagement decay before it becomes a trend, runs controlled experiments on format and topic variables, auto-implements winning changes, and ensures the series never drops significantly below its proven baseline. The human's role narrows to hosting live sessions and approving high-risk changes.

**Pass threshold:** Referral sessions and signups from the AMA series sustained at or above the Scalable baseline for 6 consecutive months. No 2 consecutive AMA sessions drop more than 20% below the rolling 4-session average in referral sessions.

## Leading Indicators

- Rolling 4-session average of referral sessions per AMA is stable or increasing
- Optimization experiments producing measurable improvements (≥ 50% win rate)
- New subreddits being tested and integrated each quarter without overall engagement declining
- Content repurposing multiplier increasing (total attributed referral sessions exceeding 2x the live AMA sessions alone)
- Agent detecting engagement anomalies before the human notices them
- Convergence signal: when successive experiments produce <2% improvement, the play has reached its local maximum

## Instructions

### 1. Build the AMA series performance dashboard

Run the the ama performance monitoring workflow (see instructions below) drill to create a PostHog dashboard with:

**Panel 1 -- Session-over-session engagement (bar chart):**
- X-axis: AMA session number (chronological)
- Y-axis: Total upvotes, total questions, referral sessions
- Overlay the Scalable baseline as a reference line

**Panel 2 -- Referral traffic per session and from repurposed content (stacked bar):**
- For each session: referral sessions from the live AMA + referral sessions from repurposed content (blog, social, newsletter)
- Shows the total reach multiplier per session

**Panel 3 -- Signup attribution by subreddit (bar chart):**
- `ama_signup` events grouped by `subreddit`, cumulative by month
- Identifies which subreddits convert best

**Panel 4 -- Topic performance heatmap (table):**
- Rows: AMA topics (categorized by theme)
- Columns: avg upvotes, avg questions, avg referral sessions, avg signups
- Surfaces which topic categories consistently outperform

**Panel 5 -- Engagement efficiency trend (line chart):**
- Referral sessions per hour of human time, rolling 4-session average
- Should be trending up as automation handles more prep work

**Panel 6 -- Experiment tracker (table):**
- Active experiments: hypothesis, variant, start date, sample size, interim results
- Completed experiments: hypothesis, outcome, impact, decision (adopted/reverted)

### 2. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill, adapted for the AMA series:

**Phase 1 -- Monitor (runs after every AMA session):**

Build an n8n workflow triggered 48 hours after each AMA:

1. Pull session metrics: upvotes, questions, response rate, referral sessions, signups
2. Compare to the rolling 4-session average
3. Classify: **normal** (within +/-15%), **plateau** (within +/-5% for 4+ sessions), **drop** (>20% decline vs. average), **spike** (>50% increase)
4. If normal: log to Attio, generate the standard post-session report
5. If anomaly detected: trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**

1. Gather context: subreddit engagement profile, topic category, AMA format used, day/time of posting, Q&A bank accuracy rate
2. Pull the last 8 sessions of performance data from PostHog
3. Run `hypothesis-generation` with the anomaly data:
   - "Engagement dropped because the topic was too similar to Session N-2" (topic fatigue)
   - "Engagement dropped because this subreddit has AMA fatigue — 3 other AMAs in the past month" (subreddit saturation)
   - "Referral sessions dropped because fewer answers included links" (link strategy regression)
   - "Engagement spiked because the topic aligned with a trending industry event" (timing opportunity)
4. Rank hypotheses by expected impact and risk
5. If top hypothesis is high-risk (e.g., "abandon this subreddit entirely"): send Slack alert for human review
6. If low/medium risk: proceed to Phase 3

**Phase 3 -- Experiment (one active experiment at a time):**

Design controlled experiments using the next 2 AMA sessions as control vs. variant:

- **Control session:** Use the current standard format/topic/subreddit
- **Variant session:** Implement the hypothesized change

Example experiments:
- **Topic freshness:** Control = host's choice of topic. Variant = topic selected from community's most-upvoted recent questions.
- **Post timing:** Control = standard posting time. Variant = post 2 hours earlier/later.
- **AMA duration:** Control = 2 hours. Variant = 4 hours with a "round 2" announcement.
- **Proof-first format:** Control = standard bio intro. Variant = lead with a compelling data point.
- **Guest AMAs:** Control = solo host. Variant = invite a complementary expert as co-host.

Minimum experiment duration: 2 sessions per variant (4 sessions total for a complete test).

**Phase 4 -- Evaluate (after experiment completion):**

1. Compare control vs. variant across all KPIs: upvotes, questions, referral sessions, signups
2. Run `experiment-evaluation`:
   - **Adopt:** Variant outperforms control by ≥ 15% on primary KPI (referral sessions). Make the change the new default.
   - **Iterate:** Results are mixed. Generate a refined hypothesis and test again.
   - **Revert:** Variant underperforms. Restore the previous approach.
   - **Extend:** Not enough data. Run 2 more sessions.
3. Log the full evaluation in Attio with decision rationale

**Phase 5 -- Report (weekly optimization brief):**

Generate a weekly brief posted to Slack:

```
AMA Series — Week [X] Optimization Brief
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SESSIONS THIS WEEK: X
ROLLING AVG REFERRAL SESSIONS/AMA: XXX (target: ≥ [Scalable baseline])
ROLLING AVG SIGNUPS/AMA: XX

STATUS: [On Track / Watch / Action Required]

ACTIVE EXPERIMENT: [name]
  Hypothesis: [what we're testing]
  Interim: [control vs variant so far]
  Sessions remaining: X

LAST EXPERIMENT: [name]
  Result: [Adopted / Reverted / Extended]
  Impact: [+/-X% on referral sessions]

SUBREDDIT HEALTH:
  [subreddit]: [score] [status]
  [subreddit]: [score] [status]

RECOMMENDATIONS:
  1. [action item]
  2. [action item]
```

### 3. Automate subreddit rotation with community health scoring

Run the `community-health-scoring` drill weekly, with AMA-specific scoring adjustments:

**AMA-specific health signals (in addition to standard signals):**
- AMA engagement trend in this subreddit (are our AMAs getting more or fewer questions over time?)
- AMA competition (how many other AMAs were hosted this month? If saturated, engagement drops)
- Moderator relationship quality (are they responsive? Do they help promote our AMAs?)

**Rotation rules the agent enforces:**
- No subreddit hosts more than 2 AMAs per month (prevents community fatigue)
- If a subreddit's AMA engagement drops below 50% of its peak for 2 consecutive sessions, pause for 2 months
- Test 1 new subreddit per month (allocated from the second-tier reconnaissance list)
- Retire subreddits that fail to produce ≥ 5 referral sessions per AMA for 3 consecutive sessions

The agent recommends the subreddit rotation schedule each month. Human approves.

### 4. Evolve the content repurposing engine

Extend the Scalable repurposing pipeline with optimization:

1. Track which repurposed content formats drive the most additional referral sessions (blog vs. social vs. newsletter)
2. Double down on the winning format. If blog posts from AMAs consistently outperform social posts, allocate more effort to expanding blog content.
3. Build a "greatest hits" library: the top 20 AMA answers across all sessions, compiled into an evergreen resource page with UTM tracking
4. Cross-reference repurposed content performance with the original AMA topic. Some topics have longer content tails than others — the agent learns which topic categories to recommend for maximum repurposing ROI.

### 5. Detect convergence

The autonomous optimization loop monitors for convergence — the point where successive experiments produce diminishing returns:

**Convergence criteria:** 3 consecutive experiments produce less than 2% improvement on referral sessions per AMA.

**When convergence is detected:**
1. Reduce optimization experiments from every 4 sessions to every 8 sessions
2. Shift the agent's focus from format experimentation to content quality and community relationship maintenance
3. Report to the team: "The AMA series has reached its local maximum. Current performance: [metrics]. Further gains require strategic changes (new audience segments, product launches creating fresh AMA topics, or expansion to non-Reddit platforms like HN/Discord AMAs) rather than tactical optimization."
4. Continue monitoring for external disruptions (subreddit changes, competitor AMAs, market shifts) that could reset the optimization cycle

### 6. Monthly health check

The agent generates a monthly report:

```
AMA Series — Month [X] Health Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SESSIONS THIS MONTH: X
TOTAL REFERRAL SESSIONS: XXX (target: ≥ [Scalable baseline x sessions])
TOTAL SIGNUPS: XX (target: ≥ [Scalable baseline x sessions])
GUARDRAIL BREACHES: X

SUBREDDIT PORTFOLIO:
  Active: X subreddits
  AMAs hosted: X per subreddit
  New tested this month: X
  Paused/retired this month: X

TOP PERFORMING SESSIONS:
  1. [Topic] in r/[subreddit] — XX referral sessions, XX signups
  2. [Topic] in r/[subreddit] — XX referral sessions, XX signups

REPURPOSING MULTIPLIER: X.Xx (total attributed sessions / live AMA sessions)

EXPERIMENTS:
  Completed this month: X
  Win rate: X%
  Net impact: +/-X% on referral sessions per AMA

CONVERGENCE STATUS: [Optimizing / Approaching / Converged]

RECOMMENDATION FOR NEXT MONTH:
  [Agent's strategic recommendation]
```

## Guardrails

- **Maximum 1 active experiment at a time.** Never stack experiments on the AMA series.
- **Revert threshold:** If an AMA session's referral sessions are <40% of the rolling average, immediately flag for human review before next session.
- **Human approval required for:**
  - Retiring a subreddit that has produced >100 cumulative signups
  - Changing the AMA host or adding co-hosts
  - Any format change the hypothesis generator flags as "high risk"
- **Cooldown:** After a reverted experiment, wait 2 sessions before testing a new hypothesis on the same variable.
- **Maximum experiments per month:** 2. If both fail, pause experimentation and flag for human strategic review.

## Time Estimate

| Activity | Time |
|----------|------|
| Dashboard and monitoring setup | 5 hours |
| Autonomous optimization loop setup | 4 hours |
| AMA review and approval (24 sessions x 30 min) | 12 hours |
| Live AMA sessions (24 sessions x 2.5h) | 60 hours |
| Post-session follow-up (24 sessions x 20 min) | 8 hours |
| Weekly optimization brief review (26 weeks x 15 min) | 6.5 hours |
| Monthly health check review (6 months) | 3 hours |
| Experiment design and analysis (12 experiments) | 6 hours |
| **Total** | **~105 hours human time** |

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Reddit | Platform for AMA hosting | Free (personal account) |
| PostHog | Dashboards, experiments, attribution, anomaly detection | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop, monitoring, repurposing pipeline | Self-hosted: Free / Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Syften | Between-AMA keyword monitoring | Standard: $39.95/mo ([syften.com](https://syften.com)) |
| Claude API | Topic generation, Q&A drafting, hypothesis generation, experiment evaluation | ~$30-50/mo at scale ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Estimated monthly cost:** $95-115/mo (n8n Cloud + Syften Standard + Claude API)

## Drills Referenced

- `autonomous-optimization` — the core detect-diagnose-experiment-evaluate-implement loop that finds the local maximum
- the ama performance monitoring workflow (see instructions below) — AMA-specific dashboard, trend alerts, and per-session analysis
- `community-health-scoring` — weekly subreddit health tracking driving rotation decisions
