---
name: meddic-deal-health-monitor
description: Continuous deal health monitoring that detects MEDDIC element degradation, stalled deals, and risk patterns across the pipeline
category: Qualification
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - attio-deals
  - attio-notes
  - n8n-scheduling
  - n8n-workflow-basics
  - hypothesis-generation
---

# MEDDIC Deal Health Monitor

This drill creates an always-on monitoring system that watches your enterprise deal pipeline for MEDDIC-related risks: element degradation, stalled deals, champion loss, economic buyer disengagement, and pattern-based risk signals. It runs daily via n8n and generates alerts when deals need intervention.

## Input

- Attio CRM with deals flowing through MEDDIC pipeline stages
- PostHog tracking MEDDIC events (from `meddic-scorecard-setup`)
- n8n instance for scheduled monitoring
- At least 2 weeks of MEDDIC scoring data

## Steps

### 1. Build the deal health scoring model

Each deal gets a dynamic "health score" computed from:

- **MEDDIC composite score** (50% weight): The core qualification score
- **Element progression** (20% weight): Are weak elements improving over time, or stagnating?
- **Activity recency** (15% weight): When was the last touchpoint? Stale deals lose health.
- **Stage velocity** (15% weight): Is the deal progressing through stages at expected pace, or stuck?

Create an n8n workflow using `n8n-scheduling` that runs daily at 7am:

1. Query Attio for all active deals (not Disqualified, not Closed)
2. For each deal, compute the health score:
   ```
   health = (meddic_composite * 0.50) +
            (element_progression_score * 0.20) +
            (activity_recency_score * 0.15) +
            (stage_velocity_score * 0.15)
   ```
3. Classify: **Healthy (70+)**, **At Risk (40-69)**, **Critical (<40)**

### 2. Configure element progression tracking

For each deal, track how MEDDIC element scores change over time:

- **Improving:** Element score increased by 10+ points since last assessment. Score: 100.
- **Stable:** Element score within ±10 points. Score: 60.
- **Degrading:** Element score decreased by 10+ points. Score: 20.
- **Stagnant-weak:** Element has been below 40 for 3+ assessments with no change. Score: 0.

Element progression score = average across all 6 elements.

Track changes by comparing `meddic_last_assessed` dates and corresponding scores stored in PostHog event history.

### 3. Configure activity recency scoring

Score based on days since last touchpoint (email, call, meeting) logged in Attio:

- **0-3 days:** 100
- **4-7 days:** 80
- **8-14 days:** 50
- **15-21 days:** 25
- **22+ days:** 0

### 4. Configure stage velocity scoring

Compare actual stage duration against expected duration:

- **New Lead → MEDDIC Pre-Scored:** Expected 1-2 days (auto-scoring)
- **Pre-Scored → Discovery Scheduled:** Expected 3-7 days
- **Discovery → Qualified/Needs Work:** Expected 1-2 days (post-call processing)
- **Needs Work → Qualified:** Expected 7-14 days (element gap closure)
- **Qualified → Champion Engaged:** Expected 7-14 days
- **Champion Engaged → Economic Buyer Meeting:** Expected 14-21 days
- **Economic Buyer Meeting → Decision Criteria Aligned:** Expected 7-14 days

Score: 100 if on pace, decreasing by 10 per day over expected, minimum 0.

### 5. Set up risk detection alerts

Configure the daily n8n workflow to check for specific risk patterns:

**Critical alerts (send immediately via Slack):**
- Champion score dropped below 30 (champion may have been lost)
- Economic buyer score dropped below 30 (budget holder disengaged)
- Deal has been in "Needs Work" stage for 21+ days with no element improvement
- Identify Pain score dropped below 30 (pain may have resolved or been deprioritized)

**Warning alerts (include in daily digest):**
- Any element score decreased by 15+ points since last assessment
- No activity logged for 14+ days on an active deal
- Deal health score dropped from Healthy to At Risk
- 3+ elements still below 50 after discovery call

**Opportunity alerts (include in daily digest):**
- All 6 elements now above 60 (deal approaching full qualification)
- Champion score increased to 80+ (strong internal advocacy detected)
- Economic buyer meeting completed (key milestone)

### 6. Generate daily pipeline health digest

At the end of the daily monitoring run, generate a summary:

```
## MEDDIC Pipeline Health — {date}

### Critical (Action Required)
- {deal_name}: {alert_reason}. Recommended: {action}

### At Risk
- {count} deals at risk. Top concern: {most common weak element}

### Healthy Pipeline
- {count} deals healthy. Total pipeline value: ${value}
- Average MEDDIC composite: {score}
- Deals expected to close this month: {list}

### Element Trends (last 7 days)
- Strongest improving: {element} (+{avg_change} points)
- Most concerning: {element} (-{avg_change} points)

### Stalled Deals (no activity 14+ days)
- {list with deal name, days stalled, last MEDDIC score}
```

Post this to Slack and store in Attio.

### 7. Trigger re-qualification workflows

When the monitor detects specific patterns, automatically trigger follow-up actions:

- **Champion lost (score dropped 30+ points):** Create an Attio task: "Re-engage champion or identify new champion for {deal}. Prepare internal value materials."
- **Economic buyer disengaged:** Create an Attio task: "Request warm intro to economic buyer via champion. Prepare executive business case."
- **Pain fading (score dropped 20+ points):** Create an Attio task: "Re-validate pain with new data or case study. The prospect may have found an alternative."
- **Decision process stalled:** Create an Attio task: "Follow up on procurement status. Offer to provide compliance documentation or technical references to unblock."

## Output

- Daily deal health scores for every active deal
- Real-time risk alerts for critical MEDDIC changes
- Daily pipeline health digest delivered to Slack
- Automatic task creation for deals requiring intervention
- PostHog events tracking health score trends over time

## Triggers

Runs daily at 7am via n8n cron. Critical alerts fire in real-time via Attio webhooks (when element scores are updated below critical thresholds). Weekly summary report aggregates trends for the entire pipeline.
