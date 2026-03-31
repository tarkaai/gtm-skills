---
name: review-velocity-monitor
description: Track review submission velocity, rating trends, and review-to-lead attribution across directories with automated weekly reporting
category: Directories
tools:
  - PostHog
  - n8n
  - Attio
  - Loops
fundamentals:
  - directory-review-monitoring
  - directory-analytics-scraping
  - posthog-dashboards
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
  - attio-contacts
---

# Review Velocity Monitor

This drill builds a dedicated monitoring system for review generation campaigns. It tracks how fast reviews are coming in, whether ratings are trending up or down, which ask channels produce the most reviews, and whether new reviews correlate with inbound leads. This is the play-specific monitoring layer that sits on top of `directory-performance-monitor` and feeds data into `autonomous-optimization`.

## Input

- Active review generation campaigns (output from `directory-review-generation` drill)
- Directory listings tracked in Attio (output from `directory-listing-setup` drill)
- PostHog tracking configured for directory events
- At least 4 weeks of review data for trend analysis

## Steps

### 1. Define review velocity events in PostHog

Using the `posthog-custom-events` fundamental, create events specific to the review lifecycle:

- `review_ask_sent`: Fired when a review request email is sent via Loops. Properties: `directory_name`, `ask_channel` (email/in-app/post-support/post-milestone), `customer_tenure_days`, `customer_plan`.
- `review_ask_clicked`: Fired when the recipient clicks the review link. Properties: same as above plus `time_to_click_hours`.
- `review_submitted`: Fired when a new review appears on a directory (detected via `directory-review-monitoring`). Properties: `directory_name`, `rating`, `reviewer_tenure_days`, `ask_channel` (if attributable), `is_incentivized`.
- `review_attributed_lead`: Fired when an inbound lead arrives from a directory within 7 days of a new review being published. Properties: `directory_name`, `review_count_at_time`, `avg_rating_at_time`, `lead_source`.

### 2. Build the review velocity dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a "Review Velocity & Attribution" dashboard:

**Panel 1 -- Review Velocity:**
- Trend: `review_submitted` count per week, stacked by `directory_name`
- Number: total reviews submitted in last 30 days
- Number: cumulative reviews across all directories

**Panel 2 -- Ask-to-Review Funnel:**
- Funnel: `review_ask_sent` -> `review_ask_clicked` -> `review_submitted`
- Break down by `ask_channel`
- Display conversion rates at each step

**Panel 3 -- Rating Trends:**
- Trend: average `rating` per week by `directory_name`
- Number: current average rating across all directories
- Alert threshold: flag if average drops below 4.0

**Panel 4 -- Review-to-Lead Attribution:**
- Trend: `review_attributed_lead` count per week overlaid with `review_submitted` count
- Correlation chart: review count vs inbound leads (scatter)
- Number: estimated leads per review (total attributed leads / total reviews in period)

**Panel 5 -- Ask Channel Effectiveness:**
- Table: `ask_channel`, asks sent, clicks, reviews submitted, conversion rate
- Sorted by conversion rate descending
- Highlight the best-performing channel

### 3. Build the weekly review velocity report workflow

Using `n8n-scheduling` and `n8n-workflow-basics`, create an n8n workflow triggered weekly (Monday 8am):

**Step 1 -- Collect review data:**
For each directory, use `directory-review-monitoring` to fetch reviews from the past 7 days. Count new reviews, calculate average rating of new reviews, and note any 1-2 star reviews.

**Step 2 -- Query PostHog:**
Pull ask-to-review funnel metrics for the past 7 days. Calculate: total asks sent, click-through rate, submission rate, average time from ask to review.

**Step 3 -- Calculate velocity metrics:**
- Current velocity: reviews per week (last 4 weeks rolling average)
- Velocity trend: is velocity increasing, stable, or declining vs prior 4-week average
- Ask efficiency: reviews submitted per 100 asks sent
- Rating trend: is average rating increasing, stable, or declining

**Step 4 -- Generate the report:**

```
# Review Velocity Report -- Week of {date}

## Velocity
- New reviews this week: {count} ({change}% vs 4-week avg)
- Current pace: {velocity} reviews/week
- Trend: {increasing|stable|declining}

## Ratings
- Average rating of new reviews: {avg}
- Overall average across directories: {overall_avg}
- Trend: {increasing|stable|declining}

## Ask Effectiveness
- Review asks sent: {asks}
- Click-through rate: {ctr}%
- Ask-to-review conversion: {conv}%
- Best channel: {channel} ({channel_conv}% conversion)

## Attribution
- Inbound leads from directories this week: {leads}
- Estimated leads per review: {ratio}

## Alerts
- {any negative reviews, rating drops, or velocity stalls}

## Optimization Signals
- {data-driven signals for autonomous-optimization to act on}
```

**Step 5 -- Distribute:**
Post to Slack, store in Attio as a note on the review campaign record.

### 4. Configure anomaly alerts

Using n8n, set up real-time alerts:

- **Velocity stall:** Zero new reviews for 14+ consecutive days on any Tier 1 directory
- **Rating drop:** Average rating drops below 4.0 on any directory
- **Negative review:** Any 1-2 star review published (trigger response within 24 hours)
- **Ask fatigue:** Click-through rate on review asks drops below 5% (signals list is exhausted or messaging is stale)
- **Attribution spike:** 3+ inbound leads from a directory in a single week (signal to double down)

### 5. Maintain review candidate pipeline in Attio

Using `attio-contacts` and `attio-reporting`, keep the review candidate pipeline current:

- Query Attio weekly for new customers who meet review candidate criteria (30+ days active, positive engagement, no existing review)
- Calculate pipeline depth: how many weeks of review candidates remain at current ask rate
- If pipeline depth < 4 weeks, flag for attention (need more customers or need to re-ask lapsed candidates)
- Track: `last_review_asked_date`, `review_ask_count`, `reviewed_on`, `review_rating` per contact

## Output

- Real-time PostHog dashboard tracking review velocity, ratings, and attribution
- Weekly automated report with velocity trends and optimization signals
- Anomaly alerts for velocity stalls, rating drops, and negative reviews
- Review candidate pipeline health tracking in Attio

## Triggers

- Dashboard: always-on, refreshes with live PostHog data
- Weekly report: Monday 8am via n8n cron
- Anomaly alerts: continuous via n8n webhook monitors
- Pipeline health check: weekly, appended to the velocity report
