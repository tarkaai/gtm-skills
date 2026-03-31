---
name: integration-pipeline-health-monitor
description: Monitor integration partner portfolio health, lead attribution per partner, and surface optimization opportunities
category: Partnerships
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-cohorts
  - posthog-anomaly-detection
  - attio-reporting
  - n8n-scheduling
  - hypothesis-generation
---

# Integration Pipeline Health Monitor

This drill builds the monitoring and reporting layer for the integration partnerships play. It tracks per-partner lead attribution, integration activation rates, partner distribution effectiveness, and overall integration pipeline health. At Durable level, it feeds data into the `autonomous-optimization` drill.

## Input

- Active integration partnerships with PostHog tracking in place (UTM parameters, custom events)
- Attio partner records with integration deal history
- At least 4 weeks of integration data across 3+ partners (minimum for meaningful comparisons)

## Steps

### 1. Build the integration partnerships dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a dashboard called "Integration Partnerships — Pipeline Health" with these panels:

- **Leads by integration partner** (bar chart): `integration_lead_captured` events grouped by `utm_source` (partner slug), last 30 days
- **Integration activations by partner** (bar chart): `integration_activated` events grouped by `integration_partner`, last 30 days
- **Activation-to-first-sync rate by partner** (table): `integration_first_sync` / `integration_activated` per partner, sorted descending
- **Partner-sourced funnel** (funnel): `integration_landing_page_viewed` -> `integration_activated` -> `integration_first_sync` -> `deal_created`, filtered by partner UTM sources
- **Leads over time by partner** (trend line): weekly `integration_lead_captured` events stacked by partner, last 90 days
- **Integration usage retention** (retention chart): users who activated an integration, grouped by activation week, measuring continued usage at weeks 1, 2, 4, 8
- **Top integration use cases** (table): `integration_first_sync` events grouped by `sync_type` or `action_type` to show which integration features drive the most value

### 2. Create partner performance cohorts

Using the `posthog-cohorts` fundamental, create cohorts for:

- **High-value partners**: Partners whose leads convert to paid customers at >5% rate
- **Volume partners**: Partners driving >20 integration activations/month but with lower downstream conversion
- **Growing partners**: Partners whose monthly leads increased >25% month-over-month for 2+ months
- **Declining partners**: Partners whose leads dropped >30% month-over-month
- **New partners**: Partners with first integration launch in the last 30 days (need more data before judging)
- **Dormant integrations**: Integrations with zero activations in the last 30 days despite being live

These cohorts feed the `autonomous-optimization` drill's anomaly detection at Durable level.

### 3. Build the weekly integration partnerships brief

Using the `n8n-scheduling` fundamental, create a weekly workflow (Friday 3pm):

1. Pull last 7 days of integration data from PostHog: landing page views, activations, first syncs, and leads per partner
2. Pull integration pipeline data from Attio: new partners contacted, integrations launched, deals in progress
3. Compare this week's metrics to the 4-week rolling average
4. Use the `hypothesis-generation` fundamental to generate insights:
   - Which partners over/underperformed this week and why?
   - Which integration types (webhook, API sync, native) drive the highest activation rates?
   - Are partner-sourced leads converting to paid at a higher or lower rate than other channels?
   - What should change next week?
5. Compile into a structured brief and post to Slack

Brief format:
```
## Integration Partnerships Weekly Brief — {date}

**This week**: {total_leads} partner-sourced leads, {activations} integration activations
**Activation rate**: {activation_rate}% of landing page visitors activated
**vs 4-week avg**: {change_pct}% {up/down}

### Top partners this week
1. {partner_1}: {leads} leads, {activations} activations ({activation_rate}% rate)
2. {partner_2}: {leads} leads, {activations} activations ({activation_rate}% rate)

### Integration health
- Active integrations: {count} (of {total} launched)
- Integrations with zero activations this week: {dormant_count}
- New integration launched: {new_integration_name} (if any)

### Underperformers
- {partner}: {leads} leads (down {pct}% from last week) — {hypothesis}

### Pipeline impact
- Partner-sourced deals created this week: {count}
- Estimated pipeline value: ${amount}
- Partner-sourced conversion rate vs other channels: {comparison}

### Recommended actions
1. {action_1}
2. {action_2}
```

### 4. Build per-partner ROI tracking in Attio

Using the `attio-reporting` fundamental, maintain these fields on each integration partner record (updated weekly by n8n):

- **Integration name**: The product integration name
- **Launch date**: When the integration went live
- **Total activations**: Cumulative integration activations
- **Total leads captured**: Cumulative leads from this partner's distribution
- **Activation-to-paid rate**: What percentage of integration users became paying customers
- **Cost per lead**: Development cost amortized over lead volume (dev hours x hourly rate / total leads)
- **Best co-marketing format**: Which launch asset (email, blog, social) drove the most leads from this partner
- **Last co-marketing date**: Most recent joint promotion
- **Partner health score**: Composite of recency, lead volume, conversion quality, and integration usage (calculated by n8n)

### 5. Set up performance alerts

Using PostHog and n8n, create alerts for:

- Any partner's weekly leads drop >50% vs prior week -> flag in Slack, investigate (partner changed their product? distribution stopped?)
- A new integration's activations exceed 20 in the first 7 days -> celebrate in Slack, fast-track co-marketing expansion
- Total partner-sourced leads drop below Scalable baseline for 2 consecutive weeks -> trigger `autonomous-optimization` investigation
- An integration's activation-to-first-sync rate drops below 30% -> the integration may be broken or confusing; investigate UX
- A partner's leads convert to paid at >2x the average rate -> flag as "expand" candidate for deeper co-marketing investment

### 6. Monitor integration reliability

Using `posthog-anomaly-detection` (at Durable level), track:

- `integration_error` events by partner: spikes indicate the integration is broken
- `integration_first_sync` completion rate: drops indicate onboarding friction
- `integration_activated` -> `integration_deactivated` within 7 days: high deactivation signals poor integration value

Alert the engineering team if error rates spike >3x baseline for any integration. A broken integration damages both your reputation and the partner relationship.

## Output

- PostHog dashboard with per-partner and per-integration performance
- Weekly automated integration partnerships brief with insights and recommendations
- Per-partner ROI tracking in Attio
- Alert system for performance anomalies and integration reliability
- Data feed for the `autonomous-optimization` drill at Durable level

## Triggers

Build the dashboard and alerts at the start of Scalable level (when you have 3+ active partners). The weekly brief runs every Friday. Partner ROI fields update weekly via n8n. At Durable level, this drill feeds the autonomous optimization loop.
