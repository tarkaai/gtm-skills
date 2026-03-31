---
name: newsletter-sponsor-performance-monitor
description: Track, compare, and report on ROI across all paid newsletter sponsorship placements
category: Paid
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-funnels
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Newsletter Sponsor Performance Monitor

This drill builds the ongoing monitoring and reporting system for paid newsletter sponsorships. It aggregates performance data across all placements, identifies top-performing newsletters, and flags underperformers for budget reallocation.

## Input

- Active newsletter sponsorship placements tracked in PostHog (from `newsletter-sponsor-booking` drill)
- Attio deal records with placement costs and newsletter metadata
- Target CPC and CPL benchmarks for this play

## Steps

### 1. Build the newsletter sponsorship dashboard in PostHog

Using `posthog-dashboards`, create a dashboard called "Newsletter Sponsorships — Performance":

**Panel 1: Click volume by newsletter (bar chart)**
- Event: `$pageview` where `utm_medium` = `paid-newsletter`
- Breakdown: `utm_source` (newsletter name)
- Time range: Last 30 days

**Panel 2: Lead conversion by newsletter (funnel)**
- Step 1: `$pageview` where `utm_medium` = `paid-newsletter`
- Step 2: `newsletter_sponsor_lead`
- Breakdown: `utm_source`
- Shows click-to-lead conversion rate per newsletter

**Panel 3: Click trend over time (line chart)**
- Event: `$pageview` where `utm_medium` = `paid-newsletter`
- Granularity: Daily
- Breakdown: `utm_source`
- Shows when each placement generated traffic (expect spikes on send days)

**Panel 4: Placement ROI table**
- Custom query joining PostHog click/lead data with Attio deal amounts
- Columns: Newsletter name, placement date, cost, clicks, leads, CPC, CPL, CTR
- Sorted by CPL ascending (most efficient placements first)

### 2. Set up automated performance collection

Using `n8n-scheduling` and `n8n-workflow-basics`, create an n8n workflow that runs 7 days after each newsletter placement:

1. Trigger: Scheduled — runs daily, checks if any placement is 7 days old today
2. Query PostHog API for click and lead counts for that placement's UTM content tag
3. Calculate CPC, CPL, and CTR
4. Update the Attio deal record with actual performance metrics
5. Compare actual vs. target metrics
6. If CPL is below target: flag as "Rebook" — this newsletter is worth rebooking
7. If CPL is above 2x target: flag as "Do Not Rebook" — this newsletter is not cost-effective

### 3. Generate the weekly sponsorship report

Build an n8n workflow using `n8n-scheduling` that runs every Monday:

1. Pull all placements from the last 7 days from Attio
2. Query PostHog for aggregate metrics: total spend, total clicks, total leads, blended CPC, blended CPL
3. Compare to previous week: is efficiency improving or declining?
4. Rank newsletters by CPL: top 3 performers and bottom 3 performers
5. Generate a report summary:
   - Total spend this week
   - Total clicks and leads
   - Blended CPC and CPL (with week-over-week change)
   - Top-performing newsletter and why
   - Recommendation: which newsletters to rebook, which to drop, and any new newsletters to test

6. Post the report to Slack (or email) and store in Attio as a note on the "Newsletter Sponsorships" campaign record

### 4. Build the newsletter scoring model

After 5+ placements, you have enough data to score newsletters on actual performance, not just estimates. Update the scoring:

- **Actual CTR** (replaces estimated): clicks / estimated newsletter audience
- **Actual conversion rate**: leads / clicks
- **Cost efficiency**: CPL relative to your target
- **Consistency**: If you have multiple placements with the same newsletter, is performance consistent or volatile?

Use this data to create a "Newsletter Sponsor Tier" field in Attio:
- **Tier 1**: CPL below target, consistent results — rebook monthly
- **Tier 2**: CPL at target, moderate results — rebook quarterly
- **Tier 3**: CPL above target — test once more with different copy, then drop if still underperforming
- **Drop**: CPL above 2x target on two attempts — do not rebook

### 5. Set up anomaly alerts

Using `posthog-custom-events`, create alerts for:
- A placement generates zero clicks within 48 hours of the reported send date (investigate: was the link included correctly?)
- A placement's CTR is 3x above average (investigate: what made this placement exceptional? Replicate.)
- Blended CPL across all placements exceeds target by 30% for 2 consecutive weeks (investigate: pause new bookings and audit the portfolio)

## Output

- PostHog dashboard with real-time visibility into all newsletter sponsorship performance
- Automated 7-day post-placement performance collection
- Weekly performance report with rebooking recommendations
- Newsletter scoring model based on actual performance data
- Anomaly alerts for outlier placements

## Triggers

Set up once at Baseline level when you have 3+ active placements. Run continuously at Scalable and Durable levels.
