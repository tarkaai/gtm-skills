---
name: posthog-dashboards
description: Build PostHog dashboards for GTM performance monitoring
tool: PostHog
product: PostHog
difficulty: Intermediate
---

# Build GTM Dashboards in PostHog

## Prerequisites
- PostHog project with events tracked (see `posthog-custom-events`)
- At least 1 week of event data collected

## Steps

1. **Create a GTM overview dashboard via API.** Use the PostHog API to create a dashboard:
   ```
   POST /api/projects/<id>/dashboards/
   { "name": "GTM Overview", "description": "Daily check-in: high-level metrics across all motions" }
   ```
   Alternatively, use the PostHog MCP to create and populate the dashboard.

2. **Add top-of-funnel metrics.** Create insight tiles via the API for: Website visitors (unique users, daily trend), Signups (daily count + conversion rate from visitor), Leads generated (outbound + inbound sources). Use the Trends insight type with daily granularity. Add each insight to the dashboard via `PATCH /api/projects/<id>/dashboards/<dashboard-id>/`.

3. **Add mid-funnel metrics.** Create tiles for: Meetings booked (daily count by source), Trial-to-paid conversion rate (funnel insight from signup to first payment), Email reply rate (trend from outbound metrics). Add comparison to previous period to show trajectory.

4. **Add bottom-funnel metrics.** Create tiles for: Deals closed (weekly count and revenue), Average deal velocity (days from lead to close), Revenue by source (outbound vs inbound vs product-led). Use bar charts for source breakdowns.

5. **Add product engagement tiles.** For product-led motions: Daily Active Users (DAU), Feature adoption rate (% of users who used key feature), Onboarding completion rate (funnel from signup to onboarding complete). These predict future revenue.

6. **Set up dashboard subscriptions via API.** Configure PostHog to email the dashboard weekly:
   ```
   POST /api/projects/<id>/subscriptions/
   { "dashboard": <dashboard-id>, "frequency": "weekly", "target_value": "team@company.com" }
   ```
   Set delivery for Monday morning so the team starts the week with data context.
