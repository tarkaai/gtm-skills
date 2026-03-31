---
name: adoption-campaign-health-report
description: Generate weekly adoption campaign health reports covering per-segment performance, experiment outcomes, and optimization recommendations
category: Experimentation
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-custom-events
  - attio-notes
  - n8n-scheduling
  - n8n-workflow-basics
  - hypothesis-generation
---

# Adoption Campaign Health Report

This drill generates a weekly health report specific to feature adoption campaigns. It aggregates per-segment adoption rates, experiment outcomes, channel effectiveness, and user feedback into a structured report that feeds into the `autonomous-optimization` drill's decision-making loop. This is the play-specific monitoring that complements the generic optimization loop.

## Input

- Feature adoption campaign running at Durable level with at least 4 weeks of per-segment data
- PostHog tracking all campaign events with segment and channel properties
- Attio storing campaign records and experiment history
- n8n instance for scheduled report generation

## Steps

### 1. Pull per-segment adoption metrics

Using `posthog-dashboards`, query the last 7 days for each active segment:

| Metric | How to Calculate |
|--------|-----------------|
| Segment reach | Count of unique users who received a campaign impression this week |
| Engagement rate | Users who interacted with a campaign message / users who received one |
| Conversion rate | Users who adopted the feature within 7 days of first impression / users reached |
| Retention rate | Users still using the feature 14+ days after adoption / total adopters |
| Dismissal rate | Users who dismissed the campaign message / users who received one |
| Channel effectiveness | Conversion rate broken down by channel (in-app, email, product tour) |

Compare each metric to the previous 4-week rolling average. Flag any metric that changed by more than 15% in either direction.

### 2. Summarize experiment outcomes

Using `posthog-custom-events` and Attio records, pull all experiments that completed or started this week:

For each experiment, report:
- Hypothesis tested
- Segment and channel affected
- Duration and sample size achieved
- Result: variant adoption rate vs. control adoption rate
- Decision: adopted, reverted, extended, or iterated
- Net impact on overall adoption rate

If no experiments ran this week, flag this as a gap — Durable level should always have one active experiment.

### 3. Identify stagnation and decay signals

Using `posthog-cohorts`, check for:

- **Campaign fatigue**: Engagement rate declining for 3+ consecutive weeks in any segment. Users are ignoring the messages.
- **Adoption plateau**: Overall adoption rate flat (less than 1% change) for 3+ weeks. The current approach has found its ceiling.
- **Retention decay**: Users who adopted the feature are dropping off at an increasing rate. The feature itself may need improvement, not the campaign.
- **Segment exhaustion**: A segment's addressable population (non-adopters) has shrunk below 50 users. The campaign has reached most targetable users in this segment.

Each signal gets a severity rating: **watch** (1 week of signal), **warn** (2 weeks), **act** (3+ weeks). Only "act" signals trigger automatic response from the `autonomous-optimization` drill.

### 4. Generate the weekly brief

Using `n8n-scheduling` and `n8n-workflow-basics`, build a workflow that runs every Monday at 09:00:

1. Execute Steps 1-3 above via PostHog API queries
2. Pass the aggregated data to Claude via `hypothesis-generation` with the prompt: "Given this week's adoption campaign performance data, generate a 1-paragraph executive summary, identify the top risk and top opportunity, and recommend 1 specific experiment to run next week."
3. Format the report:

```
## Feature Adoption Campaign — Weekly Health Report
Week of {date}

### Executive Summary
{AI-generated 1-paragraph summary}

### Segment Performance
| Segment | Reached | Engaged | Converted | Retained | vs. 4wk avg |
{table rows}

### Experiments This Week
{experiment summaries}

### Signals
- {signal type}: {description} — Severity: {watch|warn|act}

### Recommended Next Experiment
{AI recommendation with hypothesis, expected impact, and segment}

### Distance from Local Maximum
Current overall adoption rate: {X}%
Estimated ceiling (based on diminishing returns): {Y}%
Gap: {Z percentage points}
```

4. Post the report to Slack and store as an Attio note on the campaign record

### 5. Feed signals into autonomous optimization

When the report identifies "act"-severity signals:
- Campaign fatigue: the `autonomous-optimization` drill should test new messaging copy or a different channel for the affected segment
- Adoption plateau: the drill should test expanding to a new segment or testing a fundamentally different value proposition
- Retention decay: flag for human review — this likely requires product changes, not campaign changes
- Segment exhaustion: retire the segment and reallocate effort to underserved segments

## Output

- Weekly health report posted to Slack and stored in Attio
- Per-segment performance comparison with trend analysis
- Experiment outcome summaries
- Stagnation and decay signal detection with severity ratings
- AI-generated recommendations feeding into the optimization loop

## Triggers

Runs weekly via n8n cron (Monday 09:00). The stagnation detection also runs as part of the daily monitoring in the `autonomous-optimization` drill, but the weekly report provides the comprehensive view.
