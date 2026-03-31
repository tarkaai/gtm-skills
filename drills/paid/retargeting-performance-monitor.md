---
name: retargeting-performance-monitor
description: Monitor retargeting campaign health across Meta, LinkedIn, and Google — detect creative fatigue, audience exhaustion, and CPA drift
category: Paid
tools:
  - PostHog
  - Meta Ads
  - LinkedIn Ads
  - Google Ads
  - n8n
  - Anthropic
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - meta-ads-campaign-setup
  - linkedin-ads-measurement
  - google-ads-campaign-setup
  - cross-platform-retargeting-sync
  - n8n-scheduling
  - hypothesis-generation
---

# Retargeting Performance Monitor

This drill provides always-on monitoring of multi-platform retargeting campaigns. It detects three failure modes that kill retargeting ROI: creative fatigue, audience exhaustion, and CPA drift. When it detects a problem, it generates a diagnosis and recommended action.

## Prerequisites

- Retargeting campaigns running on at least 2 of: Meta, LinkedIn, Google Display
- PostHog receiving ad performance data via n8n sync workflows
- At least 4 weeks of baseline performance data
- n8n instance with scheduled workflows

## Input

- PostHog project with retargeting events: `retargeting_impression`, `retargeting_click`, `retargeting_conversion`, `retargeting_spend`
- Each event carries properties: `platform` (meta/linkedin/google), `campaign_id`, `ad_set_id`, `creative_id`, `audience_segment` (high_intent/medium_intent/low_intent)

## Steps

### 1. Build the retargeting health dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

**Panel 1 — Cross-platform CPA trend (line chart, 90 days)**
- Y-axis: cost per conversion, grouped by platform
- Alert threshold: CPA > 150% of 4-week rolling average

**Panel 2 — Creative performance decay (line chart per creative, 30 days)**
- Y-axis: CTR per creative_id
- Alert threshold: CTR decline > 30% from first-week average for any creative

**Panel 3 — Audience saturation (bar chart, weekly)**
- Y-axis: frequency (impressions / unique reach) per audience_segment per platform
- Alert threshold: frequency > 5 on display, > 3 on LinkedIn

**Panel 4 — Conversion funnel by platform (funnel)**
- Steps: impression -> click -> landing_page_view -> conversion
- Compare week-over-week drop-off rates

**Panel 5 — Budget utilization (table, daily)**
- Columns: platform, daily_budget, actual_spend, spend_rate, conversions, CPA
- Highlight: underspend (< 80% utilization signals audience exhaustion)

**Panel 6 — Lead quality score (trend, 30 days)**
- Y-axis: percentage of retargeting conversions that become qualified leads in Attio
- Alert threshold: quality rate drops below 40%

### 2. Configure automated health checks

Build an n8n workflow triggered by daily cron at 08:00 UTC:

**Check 1 — Creative fatigue detection:**
1. Query PostHog for each active creative_id: CTR over last 7 days vs. first-week CTR
2. Flag creatives where CTR has declined > 30%
3. For flagged creatives, check frequency — if frequency > 4, the audience has seen this ad too many times
4. Output: list of fatigued creatives with recommended action (pause and replace)

**Check 2 — Audience exhaustion detection:**
1. Query PostHog for impression frequency per audience_segment per platform
2. Flag segments where weekly frequency > 5 (display/Meta) or > 3 (LinkedIn)
3. Check if the audience size has shrunk (via platform APIs) — if below 1,000, the segment is too small to retarget effectively
4. Output: list of exhausted audiences with recommended action (refresh exclusion lists, broaden window, or rotate to new segment)

**Check 3 — CPA drift detection:**
1. Query PostHog for CPA by platform over last 14 days vs. 4-week baseline
2. Flag platforms where CPA has increased > 25%
3. Correlate with creative fatigue and audience exhaustion — CPA often drifts because of one of those root causes
4. Output: CPA drift alert with root cause diagnosis

### 3. Generate automated diagnoses

When any health check flags an issue, use `hypothesis-generation` via the Anthropic API to generate a diagnosis:

Input to Claude:
```
Platform: {platform}
Issue: {creative_fatigue | audience_exhaustion | cpa_drift}
Current metrics: {metrics snapshot}
Baseline metrics: {4-week averages}
Active creatives: {list with age and CTR trend}
Audience segments: {list with frequency and size}

Generate 3 ranked hypotheses for why {issue} is occurring.
For each hypothesis, recommend a specific action the agent can take.
Rate each hypothesis: low/medium/high confidence.
```

Store the diagnosis in Attio as a note on the campaign record.

### 4. Set up escalation rules

Not every issue needs human intervention. Define the automation boundary:

**Agent handles automatically:**
- Pausing a creative that has been running > 14 days with CTR below platform baseline
- Refreshing exclusion lists via `cross-platform-retargeting-sync`
- Shifting 10% of budget from underperforming platform to overperforming platform

**Requires human approval (Slack alert):**
- Pausing an entire audience segment
- Budget reallocation > 20%
- Launching new creative (agent generates the brief, human approves)
- Any change when total monthly spend > $10,000

### 5. Generate weekly retargeting brief

Every Monday at 09:00 UTC, an n8n workflow generates a weekly brief:

1. Pull 7-day performance data from PostHog across all platforms
2. Compare to previous week and 4-week rolling average
3. List: creatives launched, creatives paused, audience changes, budget changes
4. Calculate: blended CPA, total conversions, total spend, ROAS if revenue data available
5. Highlight: top-performing creative + audience combo, worst-performing combo
6. Forecast: projected monthly conversions and CPA at current trajectory
7. Post to Slack channel and store in Attio

## Output

- Real-time PostHog dashboard with 6 panels monitoring retargeting health
- Daily automated health checks detecting creative fatigue, audience exhaustion, and CPA drift
- AI-generated diagnoses with ranked hypotheses and recommended actions
- Weekly retargeting performance brief posted to Slack
- Audit trail: every automated action logged in Attio with reasoning

## Triggers

- Daily health checks: n8n cron, 08:00 UTC
- Weekly brief: n8n cron, Monday 09:00 UTC
- Emergency alert: any time CPA spikes > 200% of baseline (real-time PostHog webhook)
