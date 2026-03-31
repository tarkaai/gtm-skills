---
name: pain-intelligence-reporting
description: Continuous monitoring of pain discovery effectiveness with automated dashboards, trend analysis, and market-level pain intelligence
category: Deal Management
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
  - hypothesis-generation
---

# Pain Intelligence Reporting

This drill builds the continuous monitoring layer for the pain discovery framework at Durable level. It tracks pain discovery effectiveness over time, detects when metrics degrade, identifies emerging pain patterns in the market, and generates weekly intelligence briefs that feed the autonomous optimization loop.

## Input

- At least 4 weeks of pain discovery data in PostHog and Attio
- Active n8n instance for scheduled workflows
- PostHog dashboard from the Scalable level

## Steps

### 1. Build the pain intelligence dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

**Discovery Effectiveness (top row)**
- Avg pain-to-price ratio per week (line chart, 12-week trend)
- Avg quantification rate per week (line chart, target line at 70%)
- Discovery calls completed per week (bar chart)
- Business cases generated vs sent vs progressed (funnel)

**Pain Landscape (middle row)**
- Pain category distribution over time (stacked area chart)
- Top 10 pains by frequency this month (horizontal bar)
- Average dollar impact per pain by category (grouped bar)
- New pains detected this month (count + list)

**Pipeline Impact (bottom row)**
- Win rate: deals with business case vs without (comparison bar)
- Average deal velocity: pain-discovered vs cold pipeline (comparison)
- Total pipeline value sourced from pain discovery (cumulative line)
- Pain-to-price ratio vs win probability (scatter plot)

### 2. Set up anomaly detection

Using `posthog-anomaly-detection`, configure alerts for:

- **Pain-to-price ratio drops below 8x** for 2 consecutive weeks (discovery quality declining)
- **Quantification rate drops below 50%** (questions not probing deep enough)
- **Business case conversion drops 20%** vs 4-week average (business cases not landing)
- **New pain categories emerge** with frequency > 3 in one week (market shift detected)
- **Win correlation for a pain type drops below 0.3** (pain no longer predicts wins)

Route alerts to Slack and create Attio tasks for investigation.

### 3. Build the weekly pain intelligence brief

Create an n8n workflow that runs every Monday at 8am using `n8n-scheduling`:

1. Query PostHog for last 7 days of pain discovery metrics
2. Query Attio for all deals with pain data updated in last 7 days
3. Compare current week metrics against 4-week rolling average
4. Send the data to Claude via `hypothesis-generation` with this prompt:

```
Analyze this week's pain discovery data and generate a weekly intelligence brief.

This week's metrics: {metrics}
4-week rolling average: {rolling_avg}
New pains detected: {new_pains}
Question bank hit rates: {question_performance}

Generate:
1. Executive summary (3 sentences: what happened, what changed, what to do)
2. Key metric changes with explanations
3. Emerging pain patterns (new pains or shifting severity)
4. Question bank recommendations (what to add, retire, or modify)
5. ICP implications (any segment shifts based on pain data)
6. Recommended experiments for autonomous optimization to test next
```

### 4. Track question bank decay

Over time, discovery questions lose effectiveness as markets shift. Monitor:

- **Question surface rate trend:** Plot each question's surface rate over 8 weeks
- **Decay detection:** If a question's surface rate drops 50% from its peak, flag it for retirement
- **Gap detection:** If a pain category has no associated high-performing questions, generate new ones

Update the question bank weekly:
- Retire questions with surface_rate < 0.1 for 3 consecutive weeks
- Promote experimental questions with surface_rate > 0.3 to the standard bank
- Generate 2-3 new experimental questions per week targeting detected gaps

### 5. Market-level pain intelligence

Aggregate pain data across all prospects to build a market-level view:

- **Pain heat map:** Which pains are growing in severity across your market?
- **Segment migration:** Are certain segments developing new pains?
- **Competitive signals:** Are prospects mentioning competitors more or less?
- **Timing patterns:** Do certain pains peak in specific quarters?

This market intelligence feeds into broader GTM strategy — which segments to target, what content to create, and how to position against competitors.

### 6. Feed the autonomous optimization loop

The weekly brief includes specific experiment recommendations that the `autonomous-optimization` drill can act on:

- "Test adding question X to the standard bank — predicted to surface high-value operational pains"
- "Test removing the compliance question block for SMB prospects — it has zero surface rate for companies < 50 employees"
- "Test a shorter discovery call format (30 min vs 45 min) — quantification rates are flat after minute 35"

Each recommendation includes: hypothesis, expected impact, measurement criteria, and risk level.

## Output

- Real-time PostHog dashboard for pain discovery effectiveness
- Automated anomaly alerts when metrics degrade
- Weekly pain intelligence brief delivered to Slack and stored in Attio
- Question bank updates (retirements, promotions, new experiments)
- Market-level pain intelligence for GTM strategy
- Experiment recommendations for autonomous optimization

## Triggers

- Dashboard: always-on, refreshes every hour
- Anomaly detection: runs daily via PostHog
- Weekly brief: every Monday at 8am via n8n cron
- Question bank review: every 2 weeks (aligned with `pain-pattern-analysis` drill)
