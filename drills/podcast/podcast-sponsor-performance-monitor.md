---
name: podcast-sponsor-performance-monitor
description: Track, compare, and report on ROI across all paid podcast sponsorship placements with multi-signal attribution
category: Podcast
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

# Podcast Sponsor Performance Monitor

This drill builds the ongoing monitoring and reporting system for paid podcast sponsorships. It aggregates multi-signal attribution data (UTM clicks, vanity URL clicks, promo code redemptions, direct traffic uplift) across all placements, identifies top-performing podcasts, and flags underperformers for budget reallocation.

## Input

- Active podcast sponsorship placements tracked in PostHog (from `podcast-sponsor-booking` drill)
- Attio deal records with placement costs and podcast metadata
- Target CPL and CPC benchmarks for this play
- Promo code redemption data from your billing system

## Steps

### 1. Build the podcast sponsorship dashboard in PostHog

Using `posthog-dashboards`, create a dashboard called "Podcast Sponsorships — Performance":

**Panel 1: Click volume by podcast (bar chart)**
- Event: `$pageview` where `utm_medium` = `paid-podcast`
- Breakdown: `utm_source` (podcast name)
- Time range: Last 90 days

**Panel 2: Lead conversion by podcast (funnel)**
- Step 1: `podcast_sponsor_click` (or `$pageview` where `utm_medium` = `paid-podcast`)
- Step 2: `podcast_sponsor_lead`
- Breakdown: `utm_source`
- Conversion window: 14 days (podcast attribution is slower than digital ads)

**Panel 3: Click trend over time (line chart)**
- Event: `$pageview` where `utm_medium` = `paid-podcast`
- Granularity: Daily
- Breakdown: `utm_source`
- Look for traffic spikes on episode air dates, with a long tail of 7-14 days

**Panel 4: Placement ROI table**
- Custom query joining PostHog click/lead data with Attio deal amounts
- Columns: Podcast name, episode date, cost, show-notes clicks, vanity clicks, total clicks, leads, promo redemptions, CPC, CPL
- Sorted by CPL ascending (most efficient placements first)

**Panel 5: Attribution signal breakdown (pie chart)**
- For each placement, show the proportion of leads attributed via: UTM link, vanity URL, promo code
- This reveals which signal to optimize (e.g., if most conversions come from promo codes, invest more in the verbal CTA)

### 2. Set up automated performance collection

Using `n8n-scheduling` and `n8n-workflow-basics`, create an n8n workflow that runs 14 days after each podcast placement:

1. **Trigger**: Scheduled daily. Check Attio for any placement deal where the air date was exactly 14 days ago.
2. **Collect signals**: Query PostHog for UTM click counts and lead counts for that placement's `utm_content` tag. Query Dub.co/Rebrandly for vanity URL click counts. Query Stripe/billing for promo code redemption counts.
3. **Calculate metrics**: CPC, CPL, total attributed leads (UTM leads + promo redemptions), click-to-lead conversion rate.
4. **Update Attio**: Write actual performance metrics to the deal record.
5. **Score the placement**:
   - If CPL < target CPL: flag as **"Rebook"** — this podcast is worth sponsoring again
   - If CPL between target and 1.5x target: flag as **"Test Again"** — try different ad copy or format before deciding
   - If CPL > 1.5x target: flag as **"Do Not Rebook"** — this podcast is not cost-effective
   - If zero leads but strong click volume (20+): flag as **"Landing Page Issue"** — the podcast works but the conversion is broken

### 3. Generate the biweekly sponsorship report

Build an n8n workflow using `n8n-scheduling` that runs every other Monday:

1. Pull all placements from the last 14 days from Attio
2. Query PostHog for aggregate metrics: total spend, total clicks (all signals), total leads, promo redemptions, blended CPC, blended CPL
3. Compare to the previous 14-day period: is efficiency improving or declining?
4. Rank podcasts by CPL: top 3 performers and bottom 3 performers
5. Calculate the attribution signal breakdown: % leads from UTM vs. vanity URL vs. promo code
6. Generate a report:
   - Total spend this period
   - Total clicks, leads, and promo redemptions
   - Blended CPC and CPL (with period-over-period change)
   - Top-performing podcast and what made it effective
   - Bottom-performing podcast and whether to cut or retry
   - Attribution signal health: are listeners using the vanity URL, promo code, or show-notes link?
   - Recommendation: which podcasts to rebook, which to drop, any new podcasts to test

7. Post the report to Slack and store in Attio as a note on the "Podcast Sponsorships" campaign record

### 4. Build the podcast scoring model

After 5+ placements, update scoring based on actual performance data:

- **Actual CTR**: total clicks / estimated episode downloads
- **Actual conversion rate**: leads / total clicks
- **Cost efficiency**: CPL relative to target
- **Consistency**: For repeat placements on the same podcast, is performance consistent or volatile?
- **Long-tail value**: Some podcasts generate clicks for weeks after air date (evergreen episodes). Track the 30-day vs. 14-day attribution ratio.

Create a "Podcast Sponsor Tier" field in Attio:
- **Tier 1**: CPL below target, consistent results — rebook monthly or with every relevant episode
- **Tier 2**: CPL at or slightly above target — rebook quarterly, test different ad copy
- **Tier 3**: CPL above target on first attempt — test once more with different script angle, then decide
- **Drop**: CPL above 1.5x target on two attempts — do not rebook

### 5. Set up anomaly alerts

Using `posthog-custom-events`, create alerts for:

- **Dead placement**: A placement generates zero clicks within 72 hours of the reported air date. Investigate: was the episode published? Was the link included in show notes? Did the host read the ad?
- **Exceptional placement**: A placement's CTR is 3x above average. Investigate: what made it work? Replicate the script angle, podcast audience, and format.
- **Portfolio drift**: Blended CPL across all placements exceeds target by 30% for 2 consecutive reporting periods. Pause new bookings and audit: are costs rising, or are newer podcasts underperforming?
- **Promo code surge**: A promo code redemption rate is 2x above average for a placement. This podcast's audience is highly purchase-intent. Prioritize for rebooking with an upsell offer.

## Output

- PostHog dashboard with real-time visibility into all podcast sponsorship performance
- Multi-signal attribution: UTM + vanity URL + promo code
- Automated 14-day post-placement performance collection
- Biweekly performance report with rebooking recommendations
- Podcast scoring model based on actual performance
- Anomaly alerts for outlier placements

## Triggers

Set up once at Baseline level when you have 3+ completed placements. Run continuously at Scalable and Durable levels. At Durable, this drill feeds into `autonomous-optimization` for automated hypothesis generation and experiment execution.
