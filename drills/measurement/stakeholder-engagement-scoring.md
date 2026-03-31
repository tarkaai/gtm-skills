---
name: stakeholder-engagement-scoring
description: Track and score multi-threaded engagement per deal to identify single-threaded risks and engagement gaps
category: Measurement
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-dashboards
  - attio-deals
  - attio-custom-attributes
  - n8n-workflow-basics
  - n8n-triggers
---

# Stakeholder Engagement Scoring

This drill builds a scoring system that tracks how engaged each stakeholder is across a deal, computes a deal-level multi-threading health score, and surfaces risks when deals become single-threaded or when key stakeholders disengage.

## Input

- Stakeholder maps already populated in Attio (from `stakeholder-research` or `stakeholder-enrichment-automation` drills)
- PostHog tracking configured for sales interactions
- n8n connected to Attio and PostHog

## Steps

### 1. Define the engagement event taxonomy

Using `posthog-custom-events`, define events that represent stakeholder engagement:

| Event | Properties | Source |
|-------|-----------|--------|
| `stakeholder_email_sent` | deal_id, person_id, stakeholder_role | Instantly/Loops webhook |
| `stakeholder_email_opened` | deal_id, person_id, stakeholder_role | Email tracking pixel |
| `stakeholder_email_replied` | deal_id, person_id, stakeholder_role, sentiment | Instantly webhook |
| `stakeholder_meeting_attended` | deal_id, person_id, stakeholder_role, meeting_type | Fireflies/Cal.com |
| `stakeholder_call_completed` | deal_id, person_id, stakeholder_role, duration_min | Fireflies |
| `stakeholder_linkedin_connected` | deal_id, person_id, stakeholder_role | Manual or automation |
| `stakeholder_content_shared` | deal_id, person_id, stakeholder_role, asset_name | Intercom/email |

### 2. Build the individual engagement score

For each stakeholder on a deal, compute a rolling 14-day engagement score:

| Activity | Points |
|----------|--------|
| Email replied (positive) | 10 |
| Meeting attended | 8 |
| Call completed (5+ min) | 6 |
| Email opened | 2 |
| LinkedIn connected | 3 |
| Content viewed/shared | 4 |
| No activity in 14 days | -5 |

Score = sum of all activities in last 14 days. Classify:
- **Active** (15+): Highly engaged, maintain momentum
- **Warm** (5-14): Engaged but could cool off, nurture
- **Cold** (1-4): Minimal engagement, needs re-engagement
- **Dark** (0 or negative): No recent activity, risk of losing this thread

### 3. Compute the deal-level multi-threading score

For each deal, calculate:
- `stakeholder_count`: Total classified stakeholders
- `engaged_count`: Stakeholders with score >= 5 (Warm or Active)
- `multi_thread_ratio`: engaged_count / stakeholder_count
- `role_coverage_score`: 1 point for each role type (Economic Buyer, Champion, Influencer, End User) that has at least one Active or Warm stakeholder. Max 4 points.
- `deal_health_score`: (multi_thread_ratio * 50) + (role_coverage_score * 12.5). Range: 0-100.

### 4. Build the scoring automation in n8n

Using `n8n-workflow-basics` and `n8n-triggers`, create a daily workflow:
1. Query Attio for all active deals
2. For each deal, pull stakeholder engagement events from PostHog (last 14 days)
3. Compute individual and deal-level scores
4. Write scores back to Attio deal records using `attio-custom-attributes`:
   - `deal_health_score` (number)
   - `multi_thread_ratio` (number)
   - `engaged_stakeholder_count` (number)
   - `single_threaded_risk` (checkbox: true if engaged_count < 2)

### 5. Set up alerts

Configure n8n alert branches:
- **Single-threaded alert**: Deal has only 1 engaged stakeholder AND deal value > threshold → Slack alert to deal owner
- **Champion cooling alert**: The contact tagged as Champion drops from Active to Cold → Immediate Slack alert
- **Economic Buyer dark alert**: Economic Buyer has not engaged in 14+ days → Escalation to founder
- **Blocker engagement alert**: A contact tagged as Blocker becomes Active (might be mobilizing opposition) → Alert for strategy review

### 6. Build the multi-threading dashboard

Using `posthog-dashboards`, create a dashboard with:
- **Bar chart**: Distribution of deals by deal_health_score ranges (0-25, 25-50, 50-75, 75-100)
- **Table**: All deals sorted by deal_health_score ascending (worst first), showing stakeholder count, engaged count, missing roles
- **Trend line**: Average multi_thread_ratio over time (should trend upward as the play matures)
- **Funnel**: stakeholder_mapped → stakeholder_contacted → stakeholder_engaged → multi_threaded_deal → deal_advanced

## Output

- Individual engagement score per stakeholder per deal, updated daily
- Deal-level health score incorporating multi-threading depth and role coverage
- Automated alerts for single-threaded risks, Champion disengagement, and Economic Buyer silence
- Multi-threading dashboard showing deal health across the pipeline

## Triggers

- Runs daily via n8n cron (scoring update)
- Alerts fire in real-time when thresholds are breached
- Dashboard is always-on for pipeline reviews
