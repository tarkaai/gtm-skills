---
name: community-health-scoring
description: Score and rank active communities by engagement ROI, detect declining communities, and recommend reallocation
category: Community
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - attio-lists
---

# Community Health Scoring

This drill maintains a living scorecard for every community in your engagement portfolio. It detects communities losing ROI, surfaces emerging high-potential communities, and recommends how to reallocate engagement effort. Runs on a weekly automated cadence.

## Input

- Community target list in Attio (from `community-reconnaissance` drill)
- PostHog tracking events flowing (from `posthog-gtm-events` drill)
- Activity log of community interactions (from `community-engagement-tracking` fundamental)
- At least 4 weeks of engagement data per community

## Steps

### 1. Define the health score formula

Each community gets a composite score (0-100) computed weekly from five weighted signals:

| Signal | Weight | Measurement | Source |
|--------|--------|-------------|--------|
| Referral volume | 30% | Unique sessions from this community in the last 7 days | PostHog `community_referral_visit` events filtered by `source` property |
| Conversion rate | 25% | Signups / referral sessions for this community | PostHog funnel: `community_referral_visit` -> `signup_completed` filtered by community |
| Engagement efficiency | 20% | (Referral sessions + signups) / hours invested in this community | Activity log hours vs PostHog referral data |
| Engagement trend | 15% | Week-over-week change in referral sessions (positive = growing, negative = declining) | PostHog trend query comparing last 7 days to prior 7 days |
| Pipeline attribution | 10% | Deals in Attio where `lead_source_detail` matches this community | Attio API query filtered by community name |

### 2. Build the scoring n8n workflow

Using the `n8n-scheduling` fundamental, create a workflow that runs every Monday at 6am:

```
Schedule Trigger (weekly, Monday 6am)
  -> PostHog HTTP Request Node:
     Query: community_referral_visit events, last 7 days, grouped by source property
     Return: {community: string, sessions: number}[]
  -> PostHog HTTP Request Node:
     Query: community_signup events, last 7 days, grouped by source property
     Return: {community: string, signups: number}[]
  -> PostHog HTTP Request Node:
     Query: community_referral_visit trend, last 7 days vs prior 7 days, grouped by source
     Return: {community: string, current_week: number, prior_week: number}[]
  -> Attio HTTP Request Node:
     Query: Deals where lead_source_detail matches community names, created in last 30 days
     Return: {community: string, deal_count: number, pipeline_value: number}[]
  -> Function Node (compute scores):
     For each community:
       referral_score = min(sessions / target_sessions * 100, 100) * 0.30
       conversion_score = min(conversion_rate / target_rate * 100, 100) * 0.25
       efficiency_score = min(efficiency / target_efficiency * 100, 100) * 0.20
       trend_score = ((current_week - prior_week) / max(prior_week, 1) + 1) * 50 * 0.15
       pipeline_score = min(deal_count / target_deals * 100, 100) * 0.10
       total = referral_score + conversion_score + efficiency_score + trend_score + pipeline_score
     Classify:
       80-100: "thriving" — increase investment
       60-79: "healthy" — maintain current effort
       40-59: "watch" — investigate, may need strategy change
       20-39: "declining" — reduce effort, reallocate to higher-scoring communities
       0-19: "dormant" — pause engagement, archive from active list
  -> Attio Node: Update each community record with new score, classification, and component scores
  -> Slack Node: Post weekly community health report
```

### 3. Configure anomaly detection

Using the `posthog-anomaly-detection` fundamental, set alerts for:

- **Referral spike:** Any community's weekly referral sessions exceed 3x its 4-week average. Action: investigate what caused the spike and replicate it.
- **Referral collapse:** Any community's weekly referral sessions drop below 30% of its 4-week average. Action: check if the community is still active, if your account was restricted, or if a competitor entered.
- **Conversion rate shift:** Conversion rate for any community changes by more than 50% (up or down) vs 4-week average. Action: review the landing page experience and content quality for that community's traffic.

### 4. Generate the weekly health report

The n8n workflow produces a structured report posted to Slack and stored in Attio:

```markdown
## Community Health Report — Week of {date}

### Portfolio Summary
- Active communities: {count}
- Total referral sessions this week: {total}
- Total signups this week: {total}
- Portfolio health score (weighted avg): {score}/100

### Top Performers
| Community | Score | Sessions | Signups | Trend |
|-----------|-------|----------|---------|-------|
| {name}    | {score} | {sessions} | {signups} | {trend%} |

### Declining Communities (action required)
| Community | Score | Issue | Recommended Action |
|-----------|-------|-------|--------------------|
| {name}    | {score} | {issue} | {action} |

### Emerging Opportunities
{Communities newly added or with rapidly improving scores}

### Reallocation Recommendation
- Increase effort: {list communities}
- Maintain effort: {list communities}
- Decrease effort: {list communities}
- Archive: {list communities}
```

### 5. Feed into autonomous optimization

The health scores and anomaly alerts from this drill feed directly into the `autonomous-optimization` drill at Durable level. When the optimization loop detects a metric anomaly, it uses community health data to generate targeted hypotheses — for example, "Community X's referral volume dropped 40%; hypothesis: our posting frequency decreased. Test: increase to 3 posts/week for 2 weeks."

## Output

- Weekly health score for every active community (0-100 with classification)
- Automated Slack report with portfolio summary and reallocation recommendations
- Anomaly alerts for sudden changes in community performance
- Historical score data in Attio for trend analysis
- Input data for the `autonomous-optimization` drill's hypothesis generation

## Triggers

- Automated: weekly (every Monday)
- Ad-hoc: when evaluating whether to add or drop a community
- Quarterly: full portfolio review with strategic reassessment
