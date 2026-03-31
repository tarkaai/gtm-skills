---
name: best-practices-health-report
description: Generate weekly structured reports on best-practices engagement, content freshness, stalled user detection, and optimization recommendations
category: Product
tools:
  - PostHog
  - Anthropic
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-anomaly-detection
  - hypothesis-generation
  - n8n-scheduling
  - attio-notes
---

# Best Practices Health Report

This drill produces a weekly structured report that tracks every dimension of the best-practices content system: content engagement, delivery health, user progress, stalled users, and content freshness. The report feeds directly into the autonomous optimization loop by surfacing signals that trigger experiments.

## Input

- PostHog tracking from the `best-practices-content-pipeline` drill (card events)
- Delivery automation running from the `best-practices-delivery-automation` drill
- At least 4 weeks of delivery data (needed for trend detection)
- Anthropic API key for report generation

## Steps

### 1. Pull engagement metrics

Using `posthog-dashboards`, query the following metrics for the reporting period (trailing 7 days) and compare to the 4-week rolling average:

**Content Card Performance:**
| Metric | Calculation | Target |
|--------|------------|--------|
| Delivery rate | `best_practice_shown` / eligible users | >60% |
| Click-through rate | `best_practice_clicked` / `best_practice_shown` | >25% |
| Completion rate | `best_practice_completed` / `best_practice_shown` | >15% |
| Dismissal rate | `best_practice_dismissed` / `best_practice_shown` | <30% |

Break down by: card ID, persona, maturity tier, delivery surface (in-app vs. email).

**User Progress:**
| Metric | Calculation | Target |
|--------|------------|--------|
| Tips completed per active user (mean) | Sum of `best_practice_completed` / active users | >1.5/month |
| Users with 0 tips completed (30 days) | Users who saw tips but completed none | <40% |
| Retention lift from tips | 30-day retention of tip-completers vs. non-completers | >5pp |

### 2. Detect stalled users

Using `posthog-cohorts`, identify users who are stalled — they have been shown tips but are not engaging:

- **Tip-resistant:** Shown 3+ tips in the last 30 days, dismissed all of them. These users may find the tips intrusive or irrelevant.
- **Viewed-not-acted:** Clicked 2+ tips in the last 30 days but completed none. The tips may be unclear or the deep links may be broken.
- **Exhausted:** Have seen and completed all available tips for their persona and maturity tier. They need new content.

For each stalled segment, estimate the count and percentage of active users.

### 3. Assess content freshness

For each content card in the library, check:

- **Engagement decay:** Has the card's completion rate dropped >30% compared to its first 30 days? If yes, the card may be stale or the product UI may have changed.
- **Population coverage:** What percentage of eligible users have already been shown this card? If >80%, the card is nearing exhaustion.
- **Age:** How many days since the card was created or last updated? Cards older than 90 days should be reviewed for accuracy.

Flag any card that is decaying, exhausted, or stale.

### 4. Generate the weekly report

Using the `hypothesis-generation` fundamental (adapted for reporting), generate the weekly brief via Claude:

```
System prompt: "You are an AI agent generating a weekly best-practices health report. Analyze the data provided and produce a structured report. Be specific with numbers. Flag problems with severity levels: INFO (no action needed), WATCH (monitor closely), ACT (immediate action required)."

User prompt: "
DATA:
- Card performance: {CARD_PERFORMANCE_TABLE}
- User progress: {USER_PROGRESS_TABLE}
- Stalled users: {STALLED_USER_COUNTS}
- Content freshness: {CONTENT_FRESHNESS_TABLE}
- Week-over-week trends: {TREND_DATA}

Generate:
1. Executive summary (3 sentences: overall health, biggest win, biggest risk)
2. Card performance table with trend arrows
3. Stalled user analysis with recommended interventions
4. Content freshness flags with recommended actions
5. Top 1 experiment recommendation for next week (hypothesis + expected impact)
6. Distance from local maximum estimate (based on successive experiment results)
"
```

### 5. Distribute the report

Using `n8n-scheduling`, automate report generation every Monday at 09:00 UTC:

1. n8n queries PostHog for all metrics from Steps 1-3
2. n8n sends the data to the Anthropic API for report generation
3. The formatted report is posted to Slack
4. The report is stored in Attio using `attio-notes` on the campaign record
5. Any "ACT"-severity signals are automatically converted into hypotheses for the `autonomous-optimization` drill

### 6. Track report accuracy over time

Log each experiment recommendation and its eventual outcome. After 12 weeks, review: what percentage of "ACT" signals resulted in actual problems? What percentage of experiment recommendations produced positive results? If accuracy is below 60%, refine the anomaly detection thresholds and hypothesis generation prompts.

## Output

- Weekly structured health report covering engagement, stalled users, and content freshness
- Automated distribution via Slack and Attio
- "ACT"-severity signals that feed into the autonomous optimization loop
- Experiment recommendation generated from report data

## Triggers

Runs every Monday at 09:00 UTC via n8n cron. Ad-hoc runs can be triggered manually when investigating a metric anomaly.
