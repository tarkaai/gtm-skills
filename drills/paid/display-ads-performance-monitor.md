---
name: display-ads-performance-monitor
description: Continuously monitor GDN and Meta display campaign KPIs, detect placement rot, creative fatigue, audience exhaustion, and CPA drift
category: Paid
tools:
  - Google Ads
  - Meta Ads
  - PostHog
  - n8n
  - Anthropic
fundamentals:
  - google-ads-display-campaign
  - google-ads-display-audiences
  - meta-ads-creative-optimization
  - posthog-anomaly-detection
  - posthog-dashboards
  - cross-platform-retargeting-sync
  - n8n-workflow-basics
  - n8n-scheduling
  - hypothesis-generation
---

# Display Ads Performance Monitor

This drill creates an always-on monitoring system for display advertising campaigns on GDN and Meta Audience Network. Display campaigns degrade differently than search -- the primary failure modes are placement rot (ads appearing on increasingly low-quality sites), creative fatigue (audience sees the same banners repeatedly), audience exhaustion (in-market segments saturated), and CPA drift. This drill detects each failure mode and generates agent-executable remediation actions.

## Prerequisites

- Active display campaigns on GDN and/or Meta with at least 4 weeks of performance data
- PostHog receiving display ad events with properties: `platform`, `campaign_id`, `ad_group_id`, `creative_id`, `placement`, `audience_segment`
- n8n instance for scheduled workflows
- Anthropic API key for hypothesis generation

## Input

- PostHog events: `display_impression`, `display_click`, `display_conversion`, `display_spend`
- Each event carries: `platform` (google/meta), `campaign_id`, `ad_group_id`, `creative_id`, `placement_url` (GDN only), `audience_segment`, `pain_point`

## Steps

### 1. Build the display health dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

**Panel 1 -- Cross-platform CPA trend (line chart, 90 days)**
- Y-axis: cost per conversion, grouped by platform and campaign type (managed placements vs custom intent vs retargeting)
- Alert threshold: CPA > 140% of 4-week rolling average for any campaign

**Panel 2 -- Placement quality distribution (table, weekly, GDN only)**
- Columns: placement_url, impressions, clicks, CTR, conversions, CPA
- Rank by impressions descending
- Alert threshold: top-10 placements by spend have zero conversions for 7+ days

**Panel 3 -- Creative performance decay (line chart per creative_id, 30 days)**
- Y-axis: CTR per creative_id, grouped by pain_point
- Alert threshold: CTR decline > 25% from first-week average for any creative

**Panel 4 -- Audience saturation (bar chart, weekly)**
- Y-axis: frequency (impressions / estimated unique reach) per audience_segment
- Alert threshold: frequency > 6 on GDN, > 4 on Meta

**Panel 5 -- Conversion funnel by campaign type (funnel)**
- Steps: display_impression > display_click > page_view > form_view > form_submit > demo_booked
- Compare week-over-week drop-off rates by campaign type

**Panel 6 -- Budget utilization and ROAS (table, daily)**
- Columns: platform, campaign, daily_budget, actual_spend, spend_rate, conversions, CPA, ROAS (if revenue attributed)
- Alert: underspend < 70% utilization signals audience exhaustion or bid too low

### 2. Configure automated health checks

Build an n8n workflow triggered by daily cron at 07:00 UTC:

**Check 1 -- Placement rot detection (GDN only):**
1. Pull the placement report from Google Ads API for the last 7 days
2. Identify placements that received > 100 impressions with zero conversions
3. Identify placements with CTR < 0.05% (likely bot traffic or irrelevant sites)
4. Compare current placement distribution against baseline: if > 30% of impressions are going to placements not in the original managed list, placement expansion has drifted
5. Output: list of placements to exclude with reasoning

**Check 2 -- Creative fatigue detection:**
1. Query PostHog for each active creative_id: CTR over last 7 days vs first-week CTR
2. Flag creatives where CTR declined > 25%
3. Cross-reference with frequency data: if creative is flagged AND frequency > 5, it is fatigued
4. Check creative age: creatives older than 21 days should be flagged for proactive refresh even if CTR has not declined yet
5. Output: list of fatigued creatives, recommended replacements from staging queue

**Check 3 -- Audience exhaustion detection:**
1. Query impression frequency per audience_segment per platform
2. Flag segments where weekly frequency > 6 (GDN) or > 4 (Meta)
3. Check if impressions-per-day is declining for the segment (Google is running out of people to show to)
4. For custom intent audiences: check if any seed keywords or URLs have been flagged as low-volume
5. Output: exhausted audiences with recommended action (broaden targeting, swap in new custom audiences, shift budget)

**Check 4 -- CPA drift detection:**
1. Query PostHog for CPA by campaign over last 14 days vs 4-week baseline
2. Flag campaigns where CPA increased > 25%
3. Correlate with the three checks above: CPA drift is usually a symptom of placement rot, creative fatigue, or audience exhaustion
4. Output: CPA drift alert with diagnosed root cause

### 3. Generate automated diagnoses

When any health check flags an issue, use `hypothesis-generation` via the Anthropic API:

Input to Claude:
```
Platform: {platform}
Campaign type: {managed_placements | custom_intent | retargeting}
Issue: {placement_rot | creative_fatigue | audience_exhaustion | cpa_drift}
Current metrics: {metrics snapshot for last 7 days}
Baseline metrics: {4-week averages}
Active creatives: {list with age_days, CTR_current, CTR_baseline}
Audience segments: {list with frequency, estimated_reach, impressions_trend}
Placement distribution: {top 20 placements by spend with CTR and conversion data}

Generate 3 ranked hypotheses for why {issue} is occurring.
For each hypothesis, recommend a specific agent-executable action.
Rate each hypothesis: low/medium/high confidence.
Flag actions that require human approval.
```

Store the diagnosis in Attio as a note on the campaign record.

### 4. Define automation boundaries

**Agent handles automatically:**
- Excluding GDN placements with 100+ impressions and zero conversions (batch exclusion via API)
- Pausing creatives older than 21 days with CTR below 50% of campaign average
- Refreshing exclusion lists via `cross-platform-retargeting-sync`
- Shifting up to 15% of budget between ad groups within a campaign
- Promoting staging queue creatives to replace fatigued ones

**Requires human approval (Slack alert):**
- Pausing an entire audience segment or campaign
- Budget reallocation > 20% between campaigns
- Launching new creative concepts (agent generates the brief, human approves)
- Adding new managed placements (agent researches candidates, human approves)
- Any change when total monthly display spend > $10,000

### 5. Generate weekly display performance brief

Every Monday at 08:00 UTC, an n8n workflow generates a brief:

1. Pull 7-day performance data from PostHog across all display campaigns
2. Compare to previous week and 4-week rolling average
3. Report by campaign type: managed placements, custom intent, retargeting
4. List: creatives launched/paused, placements added/excluded, audience changes, budget shifts
5. Calculate: blended CPA by campaign type, total conversions, total spend, ROAS if available
6. Placement health: number of placements excluded this week, top 5 converting placements, worst 5 by spend-without-conversion
7. Creative pipeline: variants in staging queue, estimated days until pipeline runs dry
8. Forecast: projected monthly conversions and CPA at current trajectory
9. Post to Slack and store in Attio

## Output

- PostHog dashboard with 6 panels monitoring display campaign health
- Daily automated checks for placement rot, creative fatigue, audience exhaustion, and CPA drift
- AI-generated diagnoses with ranked hypotheses and recommended actions
- Weekly display performance brief posted to Slack
- Audit trail: every automated action (placement exclusion, creative rotation, budget shift) logged in Attio with reasoning

## Triggers

- Daily health checks: n8n cron, 07:00 UTC
- Weekly brief: n8n cron, Monday 08:00 UTC
- Emergency alert: CPA spikes > 200% of baseline (real-time PostHog webhook)
- Creative pipeline trigger: fewer than 3 creatives in staging queue (triggers AI generation)
