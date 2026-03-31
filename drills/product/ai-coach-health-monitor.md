---
name: ai-coach-health-monitor
description: Continuous monitoring of AI onboarding coach effectiveness — engagement rates, resolution quality, activation lift, and content gap detection
category: Product
tools:
  - PostHog
  - Intercom
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - posthog-custom-events
  - intercom-conversations-export
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# AI Coach Health Monitor

This drill creates a continuous monitoring system for the AI onboarding coach. It tracks whether the coach is actually helping users activate, detects degradation in coach quality (wrong answers, low engagement, content gaps), and feeds anomaly data into the `autonomous-optimization` drill for automated experimentation.

This is the play-specific monitoring that supplements `autonomous-optimization`. While autonomous-optimization handles the generic experiment loop, this drill monitors metrics unique to an AI coaching surface.

## Prerequisites

- AI coach deployed and running at Scalable level for at least 4 weeks
- Coach analytics instrumented (`ai_coach_impression`, `ai_coach_engaged`, `ai_coach_resolved`, `ai_coach_to_activation` events in PostHog)
- Intercom Fin analytics accessible
- n8n instance for scheduled monitoring

## Steps

### 1. Build the coach health dashboard

Using `posthog-dashboards`, create a dashboard "AI Coach Health" with these panels:

- **Coach engagement rate (weekly trend)**: % of onboarding users who interact with the coach. Target: >= play threshold. 12-week rolling view.
- **Coach resolution rate (weekly)**: % of coach conversations resolved by Fin without human handoff. Target: >= 65%. Declining = content gaps or quality degradation.
- **Activation lift (coach vs no-coach, weekly cohort)**: Side-by-side activation rates for coach-engaged vs coach-ignored users. The gap should be stable or growing.
- **Proactive suggestion CTR (weekly)**: Click-through rate on proactive coach nudges. Declining = suggestion fatigue or poor relevance.
- **Top unanswered queries (last 7 days)**: Fin questions that resulted in handoff or "I don't know" responses. These are content gaps to fill.
- **Coach interactions by onboarding step**: Heatmap showing where in the funnel users engage the coach. Shifts indicate new friction points.
- **Time to first coach interaction**: Distribution of how quickly new users engage the coach. Getting slower = greeting or trigger issues.
- **Coach-attributed activations**: Count of users who both engaged the coach AND activated within 7 days.

### 2. Define coach-specific anomaly thresholds

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Coach engagement rate | Within 10% of 4-week avg | 10-20% below for 1 week | >20% below OR below play threshold for 2 weeks |
| Resolution rate | >= 60% | 50-60% | < 50% |
| Activation lift (coach vs no-coach) | >= 5pp gap | 2-5pp gap | < 2pp gap OR coach users activate LOWER |
| Proactive suggestion CTR | Within 20% of avg | 20-40% below for 1 week | > 40% below OR < 3% absolute |
| Unanswered query volume | Stable week-over-week | 25%+ increase in new unanswered | Any single query appearing 10+ times unanswered |
| Human handoff rate | <= 35% | 35-50% | > 50% |

### 3. Build the daily coach monitoring workflow

Using `n8n-scheduling`, create a workflow that runs daily at 09:00 UTC:

1. Query PostHog for coach metrics from the last 24 hours
2. Compare against 4-week rolling averages using `posthog-anomaly-detection`
3. Query Intercom Fin analytics for: unanswered queries, low-confidence responses, handoff reasons
4. Classify each metric: normal, warning, critical

If critical anomaly detected:
```
COACH ALERT: [metric] at [value] (expected [expected_value])
Possible causes:
- Resolution rate dropped: Check Intercom for new unanswered question patterns. Content may be stale or missing.
- Engagement dropped: Check if Messenger widget is loading. Verify proactive triggers still firing.
- Activation lift collapsed: Coach may be giving correct answers that do not lead to action. Check if coach responses include deep links and next-step CTAs.
- Suggestion CTR collapsed: Users may have suggestion fatigue. Reduce frequency or refresh suggestion copy.
```

### 4. Build the weekly content gap report

Using `n8n-scheduling`, create a workflow that runs every Monday:

1. Export Fin conversations from the last 7 days using `intercom-conversations-export`
2. Filter to: unanswered queries, low-confidence responses (< 60%), and conversations that resulted in human handoff
3. Cluster the queries by topic (use regex patterns or Claude API for semantic clustering)
4. For each cluster with 3+ occurrences:
   - Identify whether a help article exists for this topic
   - If yes: the article may need improvement (Fin could not extract the answer)
   - If no: flag as a content gap requiring a new article or custom Fin answer
5. Generate a prioritized content gap report:

```
# Coach Content Gap Report — Week of [date]

## New gaps (no article exists)
1. "[query pattern]" — [count] occurrences — Recommended: Create article on [topic]
2. ...

## Article quality issues (article exists but Fin could not resolve)
1. "[query pattern]" → Article: [article_title] — [count] failures — Recommended: Rewrite [section]
2. ...

## Top performing content (highest resolution rate)
1. "[query pattern]" → [resolution_rate]% resolved by Fin
2. ...
```

6. Store the report in Attio using `attio-notes` and post to Slack

### 5. Build the coach effectiveness regression detector

Using `posthog-cohorts`, run a weekly regression analysis:

1. For each signup week cohort (last 8 weeks), compute: activation rate for coach-engaged users vs coach-ignored users
2. Plot the lift (coach-engaged minus coach-ignored) over time
3. If the lift is declining across consecutive cohorts:
   - The coach may be giving outdated or unhelpful advice
   - The product may have changed but the coach knowledge base was not updated
   - New user personas may not be covered by the existing coach content
4. Flag regression and recommend: knowledge base audit, trigger rule review, or persona expansion

### 6. Feed anomalies to autonomous optimization

This drill's outputs connect directly to `autonomous-optimization`:

- **Engagement drop** -> hypothesis space: test new greeting copy, adjust proactive trigger timing, A/B test suggestion formats
- **Resolution rate drop** -> content action: update articles, add custom Fin answers (this is a content fix, not an A/B test)
- **Activation lift drop** -> hypothesis space: test different post-resolution CTAs, test coach response formats, A/B test deep link placement
- **Suggestion CTR drop** -> hypothesis space: test new suggestion copy, adjust frequency/timing, test different trigger thresholds

The weekly health report provides the context data that `autonomous-optimization`'s hypothesis generation needs to propose relevant experiments.

## Output

- Daily automated coach health checks with critical anomaly alerts
- Weekly content gap report identifying unanswered queries and article quality issues
- Weekly regression analysis comparing coach effectiveness across cohorts
- Integration hooks feeding anomaly data to the autonomous optimization loop
- Full dashboard showing coach health trends over time

## Triggers

Daily monitoring runs at 09:00 UTC. Weekly content gap report runs Mondays at 10:00 UTC. Weekly regression analysis runs Mondays at 11:00 UTC. Recalibrate anomaly thresholds monthly.
