---
name: technical-intelligence-monitor
description: Monitor technical requirement patterns across deals, track technical win/loss reasons, detect shifts in market technical demands, and report weekly
category: Sales
tools:
  - Attio
  - PostHog
  - Anthropic
  - n8n
fundamentals:
  - attio-reporting
  - attio-deals
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - hypothesis-generation
  - n8n-scheduling
  - n8n-workflow-basics
---

# Technical Intelligence Monitor

This drill creates an always-on monitoring system that tracks technical requirement patterns across your pipeline, identifies which technical factors predict wins and losses, detects shifts in market technical demands, and generates weekly intelligence briefs. It is the play-specific monitoring layer that feeds into the `autonomous-optimization` drill at Durable level.

## Input

- Attio CRM with technical scoring fields populated across multiple deals (minimum 20 deals with scores)
- PostHog tracking technical requirement events
- n8n instance for scheduling
- Anthropic API key for intelligence generation

## Steps

### 1. Build the technical intelligence dashboard in PostHog

Using `posthog-dashboards`, create a dashboard called "Technical Requirements Intelligence" with these panels:

**Panel 1 — Technical Fit Distribution:**
Query all `tech_fit_score_applied` events from the last 90 days. Display a histogram of composite scores. Track the median score over time — is it trending up (you're targeting better-fit prospects) or down (market demands are outpacing your product)?

**Panel 2 — Blocker Frequency:**
Query all `tech_requirements_extraction_completed` events. Break down `certifications_required` and integration system mentions by frequency. Display as a bar chart sorted by count. This shows which certifications and integrations your market demands most.

**Panel 3 — Technical Win/Loss Analysis:**
Query `tech_fit_score_accuracy_check` events. Compare score distributions for won vs. lost deals. Display as overlapping histograms. Calculate: what composite score threshold best predicts wins?

**Panel 4 — Category Score Breakdown:**
For each of the 5 scoring categories, show the average score across all deals in the last 90 days. Highlight the weakest category — this is where your product-market fit is poorest technically.

**Panel 5 — Technical Disqualification Rate:**
Track the percentage of qualified deals that get technically disqualified over time. A rising rate means your technical capabilities are falling behind market demands.

### 2. Set up anomaly detection

Using `posthog-anomaly-detection`, configure alerts for:

- **New certification demand spike:** If a certification that appeared in <10% of deals suddenly appears in >25%, alert. This signals a market shift (e.g., new regulation).
- **Integration demand change:** If a new system appears in the top 5 integration requirements that wasn't there 30 days ago, alert. This signals a platform shift in your market.
- **Technical disqualification rate increase:** If tech DQ rate rises >5 percentage points month-over-month, alert.
- **Composite score decline:** If the 30-day rolling average composite score drops >10 points, alert.

### 3. Build the weekly intelligence brief generator

Create an n8n workflow on a weekly cron schedule (every Monday 8am):

1. Pull the last 7 days of technical events from PostHog
2. Pull all deals with technical scores updated in the last 7 days from Attio
3. Pull any anomaly alerts triggered in the last 7 days
4. Send all data to Claude for analysis:

```
POST https://api.anthropic.com/v1/messages

Prompt: "Generate a weekly Technical Intelligence Brief from this data. Return markdown.

Data:
- Deals scored this week: {count}
- Average composite score: {number}
- Composite score trend (4-week): {up/down/flat} by {amount}
- Top integration demands this week: {list with counts}
- Top certification demands this week: {list with counts}
- Deals technically disqualified: {count} — reasons: {list}
- Deals technically qualified: {count}
- Anomalies detected: {list}
- Won deals this week with technical scores: {list}
- Lost deals this week with technical scores: {list}

Generate:
1. **Executive Summary** (3 sentences): What is the technical landscape telling us this week?
2. **Key Metrics**: Composite score trend, DQ rate, top blockers
3. **Pattern Shifts**: Any new or changing technical demands
4. **Product Gaps**: Requirements we cannot meet that are causing deal losses
5. **Recommendations**: Specific actions for product, engineering, or sales
6. **Competitive Signals**: If technical losses mention competitors, what are they doing that we're not?"
```

5. Post the brief to Slack and store in Attio as a company-level note

### 4. Track technical requirement evolution

Maintain a running dataset of technical requirements across all deals. Every quarter, analyze trends:

- Which integrations are growing/declining in demand?
- Which certifications are becoming table stakes?
- Is the average technical maturity of your prospects increasing (moving upmarket) or decreasing?
- Are certain industries clustering around specific technical requirement profiles?

Log the quarterly analysis as a PostHog event:
```json
{
  "event": "tech_intelligence_quarterly_review",
  "properties": {
    "quarter": "2026-Q1",
    "deals_analyzed": 45,
    "avg_composite_score": 68,
    "top_integration_demand": "Salesforce",
    "top_certification_demand": "SOC2",
    "technical_dq_rate": 0.12,
    "score_trend": "improving"
  }
}
```

## Output

- PostHog dashboard with 5 panels tracking technical intelligence
- Anomaly alerts for significant technical demand shifts
- Weekly technical intelligence briefs posted to Slack and stored in Attio
- Quarterly trend analysis dataset

## Triggers

- Dashboard: always-on, refreshes automatically
- Anomaly detection: runs daily via PostHog
- Weekly brief: n8n cron every Monday 8am
- Quarterly review: n8n cron first Monday of each quarter
