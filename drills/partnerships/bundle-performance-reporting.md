---
name: bundle-performance-reporting
description: Monitor per-partner bundle conversion, surface pricing and promotion optimization levers, and generate weekly bundle performance briefs
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
  - attio-reporting
  - n8n-scheduling
  - hypothesis-generation
---

# Bundle Performance Reporting

This drill builds the monitoring and reporting layer specific to the bundle deals play. It tracks per-partner bundle page visits, tier selection patterns, deal completion rates, and revenue attribution, then generates weekly briefs that feed the `autonomous-optimization` drill at Durable level.

## Input

- Active bundle landing pages with PostHog tracking (UTM parameters firing)
- Attio partner records with bundle deal history
- At least 4 weeks of bundle data (minimum for meaningful trends)

## Steps

### 1. Build the bundle dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a dashboard called "Bundle Deals — Partner Performance" with these panels:

- **Bundle page views by partner** (bar chart): `bundle_page_viewed` events grouped by `partner_slug`, last 30 days
- **Deals completed by partner** (bar chart): `bundle_deal_completed` events grouped by `partner_slug`, last 30 days
- **Page-to-deal conversion rate by partner** (table): deals / page views per partner, sorted descending
- **Tier selection distribution** (pie chart): `bundle_tier_selected` events grouped by `tier_name`, last 30 days — shows which bundle tiers customers prefer
- **Bundle revenue over time** (trend line): sum of `deal_value` from `bundle_deal_completed` events, weekly, last 90 days
- **Bundle funnel** (funnel): `bundle_page_viewed` → `bundle_tier_selected` → `bundle_cta_clicked` → `bundle_checkout_started` → `bundle_deal_completed`
- **Traffic source breakdown** (bar chart): `bundle_page_viewed` events grouped by `utm_source`, to see whether traffic comes from your channels or the partner's
- **Average deal value by partner** (table): mean `deal_value` from `bundle_deal_completed` grouped by `partner_slug`

### 2. Create bundle performance cohorts

Using the `posthog-cohorts` fundamental, create cohorts for:

- **High-converting bundles**: Partners whose page-to-deal CVR exceeds 5%
- **Volume drivers**: Partners driving >100 page views/month but conversion below 3%
- **Declining bundles**: Partners whose deal count dropped >30% month-over-month
- **New bundles**: Partners with bundle launched in the last 30 days (insufficient data for judgment)
- **Tier mismatch bundles**: Partners where >70% of selections go to the lowest tier (pricing may be misaligned)

These cohorts feed the `autonomous-optimization` drill's anomaly detection.

### 3. Build the weekly bundle brief

Using the `n8n-scheduling` fundamental, create a weekly workflow (Friday 3pm):

1. Pull last 7 days of bundle data from PostHog (page views, tier selections, deals completed, revenue per partner)
2. Pull partner pipeline data from Attio (new bundles proposed, bundles launched, deals in progress)
3. Compare this week's metrics to the 4-week rolling average
4. Use the `hypothesis-generation` fundamental to generate insights:
   - Which partners and tiers over/underperformed this week and why?
   - Is there a pricing or positioning issue signaled by tier selection patterns?
   - What should change next week?
5. Compile into a structured brief and post to Slack

Brief format:
```
## Bundle Deals Weekly Brief — {date}

**This week**: {page_views} page views, {deals_completed} deals, ${revenue} revenue
**vs 4-week avg**: {change_pct}% {up/down}
**Active bundles**: {count} | **Avg deal value**: ${avg_deal_value}

### Top partners by revenue
1. {partner_1}: {deals} deals, ${revenue} ({cvr}% CVR)
2. {partner_2}: {deals} deals, ${revenue} ({cvr}% CVR)

### Tier distribution
- Starter: {pct}% | Growth: {pct}% | Scale: {pct}%
- Shift from last week: {direction and magnitude}

### Anomalies detected
- {partner/metric}: {description} — {hypothesis generated}

### Attribution balance
- Traffic from your channels: {pct}%
- Traffic from partner channels: {pct}%
- Imbalanced partners: {list}

### Recommended actions
1. {action_1}
2. {action_2}
```

### 4. Build the per-partner bundle ROI tracker

In Attio, maintain these fields on each partner record (updated weekly by n8n):

- **Total bundle page views**: Cumulative page views for this partner's bundle
- **Total deals completed**: Cumulative closed bundle deals
- **Total bundle revenue**: Cumulative revenue from bundle deals
- **Page-to-deal CVR**: deals / page views
- **Preferred tier**: The tier selected most often by this partner's traffic
- **Revenue split paid**: Total revenue remitted to this partner
- **Traffic attribution**: % of bundle traffic from your channels vs. the partner's
- **Bundle health score**: Composite of conversion rate, deal volume, revenue trend, and promotional effort (calculated by n8n)
- **Last deal date**: When the most recent bundle deal closed

### 5. Set up performance alerts

Using PostHog and n8n, create alerts for:

- Any partner's bundle deals drop to zero for 2 consecutive weeks after having been active → flag in Slack, investigate whether the partner stopped promoting
- A new bundle generates its first deal within 7 days of launch → celebrate in Slack, fast-track promotional support
- Total weekly bundle revenue drops below Scalable baseline for 2 consecutive weeks → trigger `autonomous-optimization` investigation
- Tier distribution shifts >20% toward the lowest tier over 4 weeks → flag potential pricing misalignment
- Traffic attribution becomes >80% from one side → flag promotional imbalance with the partner

## Output

- PostHog dashboard with per-partner and per-tier bundle performance
- Weekly automated bundle brief with insights and recommendations
- Per-partner ROI tracking in Attio
- Alert system for performance anomalies
- Data feed for the `autonomous-optimization` drill at Durable level

## Triggers

Build the dashboard and alerts once at the start of Durable level. The weekly brief runs every Friday. Partner ROI fields update weekly via n8n.
