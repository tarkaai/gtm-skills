---
name: posthog-dashboards
description: Build PostHog dashboards for GTM performance monitoring
tool: PostHog
difficulty: Intermediate
---

# Build GTM Dashboards in PostHog

## Prerequisites
- PostHog project with events tracked (see `fundamentals/analytics/posthog-custom-events`)
- At least 1 week of event data collected

## Steps

1. **Create a GTM overview dashboard.** In PostHog, go to Dashboards > New Dashboard. Name it "GTM Overview". This is your daily check-in dashboard showing high-level metrics across all motions.

2. **Add top-of-funnel metrics.** Create insight tiles for: Website visitors (unique users, daily trend), Signups (daily count + conversion rate from visitor), Leads generated (from outbound + inbound sources). Use the Trends insight type with daily granularity.

3. **Add mid-funnel metrics.** Create tiles for: Meetings booked (daily count by source), Trial-to-paid conversion rate (funnel insight from signup to first payment), Email reply rate (trend from your outbound metrics). Add comparison to previous period to show trajectory.

4. **Add bottom-funnel metrics.** Create tiles for: Deals closed (weekly count and revenue), Average deal velocity (days from lead to close), Revenue by source (outbound vs inbound vs product-led). Use bar charts for source breakdowns.

5. **Add product engagement tiles.** For product-led motions: Daily Active Users (DAU), Feature adoption rate (% of users who used key feature), Onboarding completion rate (funnel from signup to onboarding complete). These predict future revenue.

6. **Set up dashboard subscriptions.** Configure PostHog to email the dashboard as a PDF to your team weekly. Go to Dashboard > Subscribe and add team email addresses. Set delivery for Monday morning so the team starts the week with data context.
