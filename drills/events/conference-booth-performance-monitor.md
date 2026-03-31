---
name: conference-booth-performance-monitor
description: Continuous monitoring and cross-conference analysis of booth sponsorship ROI, lead quality trends, and follow-up effectiveness
category: Events
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Conference Booth Performance Monitor

This drill builds the always-on monitoring layer for the conference booth sponsorship play. Unlike webinars (which run weekly), conferences happen quarterly, so this monitor operates on event-cycle cadence: post-event health checks, cross-conference trend analysis, and forward-looking sponsorship ROI predictions.

## Input

- PostHog events from `booth-lead-capture` and `booth-follow-up-nurture` drills (at least 2 conferences of data for trend analysis)
- Attio conference records with sponsorship costs and lead data
- Target benchmarks from Baseline/Scalable levels

## Steps

### 1. Build the conference booth dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

**Per-conference breakdown:**
- Total badge scans vs qualified leads (Tier 1+2) — bar chart by conference
- Conversion funnel: badge_scanned → demo_given → meeting_booked → deal_created — funnel chart
- Lead tier distribution — pie chart per conference
- Cost per qualified lead and cost per meeting — trend line across conferences

**Cross-conference trends:**
- Qualified lead rate (Tier 1+2 / total scans) — trend line across conferences
- Meeting book rate (meetings / qualified leads) — trend line
- Follow-up reply rate by tier — grouped bar chart
- Pipeline generated vs sponsorship cost — ROI ratio trend line
- Days from conference to deal creation — histogram

**Forward indicators:**
- Pre-event outreach response rate per conference — trend
- Booth demo-to-meeting conversion rate — trend
- Follow-up sequence completion rate by tier — trend

### 2. Configure post-event automated health checks

Using `n8n-scheduling`, create a workflow that triggers 14 days after each conference (when the follow-up window closes):

1. Pull all PostHog events for this conference (filter by conference_name property)
2. Calculate core metrics:
   - Total scans, qualified leads, demos given, meetings booked, deals created
   - Cost per qualified lead: sponsorship cost / (Tier 1 + Tier 2 count)
   - Cost per meeting: sponsorship cost / meetings booked
   - Follow-up reply rate by tier
   - Pipeline value generated (from Attio deals)
3. Compare against benchmarks:
   - If cost per qualified lead > 2x target: flag RED
   - If meetings booked < 50% of target: flag RED
   - If qualified lead rate < 15% of total scans: flag YELLOW
   - If follow-up reply rate drops >30% vs previous conference: flag YELLOW
4. Generate a structured post-conference report:
   - Metrics vs targets (table)
   - What worked (which demo track, which talking points, which follow-up tier performed best)
   - What needs attention (flags from step 3)
   - Recommendation: continue with this conference next year? adjust tier? change approach?
5. Post to Slack and log in Attio as a note on the conference record

### 3. Build cross-conference comparison reports

Using `n8n-workflow-basics`, create a quarterly workflow that aggregates all conferences in the period:

1. Pull metrics from every conference in the quarter from PostHog
2. Rank conferences by ROI: (pipeline generated - sponsorship cost) / sponsorship cost
3. Rank conferences by lead quality: average deal conversion rate from booth leads
4. Identify patterns:
   - Which conference type (industry vertical, size, region) produces the best ROI?
   - Which sponsorship tier provides the best value per dollar?
   - Which demo track converts best across conferences?
   - Which follow-up approach (Loom vs text-only, timing, number of touches) works best?
5. Generate a quarterly conference program report with recommendations:
   - Conferences to re-sponsor (top 3 by ROI)
   - Conferences to drop (negative ROI or below-threshold quality)
   - Conferences to try next quarter (new events matching the profile of your winners)
   - Budget reallocation recommendations

### 4. Set up degradation alerts

Using `posthog-anomaly-detection` and `n8n-scheduling`:

- If two consecutive conferences have cost-per-meeting above 2x the rolling average, alert for investigation
- If qualified lead rate drops below 15% for 2 consecutive events, alert for investigation
- If follow-up reply rates decline 3 conferences in a row, alert for messaging refresh
- If meeting-to-deal conversion drops below 20%, alert for lead quality investigation

Route all alerts to the conference program owner.

### 5. Track long-term ROI attribution

Some conference leads take 3-6 months to convert. Build a lagging indicator dashboard:

- Deals closed-won that originated from conference booth leads (by conference)
- Revenue attributed to conference program (total and per conference)
- Average time from booth scan to closed-won deal
- Customer lifetime value of conference-sourced customers vs other channels

This data feeds back into the `autonomous-optimization` loop at the Durable level, informing which conferences to invest in and which variables to experiment on.

## Output

- PostHog dashboard with per-conference and cross-conference metrics
- Automated post-event health check reports (14 days after each conference)
- Quarterly conference program comparison reports
- Degradation alerts for quality and ROI declines
- Long-term revenue attribution tracking

## Triggers

- Post-event health check: 14 days after each conference
- Quarterly comparison: at the end of each quarter
- Degradation alerts: run weekly (checking if new data from recent conferences triggers thresholds)
- Revenue attribution: update monthly (lagging data needs time to accumulate)
