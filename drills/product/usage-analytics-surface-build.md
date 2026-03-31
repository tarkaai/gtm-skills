---
name: usage-analytics-surface-build
description: Build a user-facing analytics dashboard that surfaces personal usage data, trends, and actionable insights inside the product
category: Product
tools:
  - PostHog
  - Intercom
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-dashboards
  - intercom-in-app-messages
  - n8n-workflow-basics
---

# Usage Analytics Surface Build

This drill builds the in-product analytics surface that shows each user their own usage data, trends, and actionable insights. The surface must answer: "How much value am I getting from this product?" If the answer is clear and positive, retention follows.

## Input

- PostHog project with at least 14 days of product usage events flowing
- A list of 3-5 core user actions you want to reflect back (e.g., projects created, automations run, queries executed, time saved)
- Intercom configured for contextual messaging
- n8n instance for data aggregation workflows

## Steps

### 1. Select the metrics to surface

Query PostHog for the top user actions by volume and frequency. From those, select 3-5 metrics that meet ALL of these criteria:

- **Meaningful to the user** -- the user understands what this number means without explanation
- **Grows with usage** -- the number goes up the more the user uses the product
- **Implies value** -- a higher number means the user got more value (e.g., "hours saved" not "API calls made")

Typical choices:
- Total [core objects] created (cumulative, feels like investment)
- [Core actions] completed this week vs. last week (momentum signal)
- Time/money/effort saved (derived metric, requires a formula -- e.g., 2 minutes saved per automation run)
- Streak or consistency metric (days active this month)
- Percentile rank vs. similar users (social proof, optional)

Store the metric definitions as PostHog custom events using `posthog-custom-events`. Each metric needs: event name, aggregation method (count, sum, unique), time window (daily, weekly, monthly), and display format (number, percentage, chart).

### 2. Build the data aggregation pipeline

Using `n8n-workflow-basics`, create a scheduled workflow that runs daily:

1. Query PostHog API for each user's metric values over the last 7 and 30 days
2. Calculate derived metrics (e.g., time saved = automation_runs * avg_time_per_run)
3. Calculate week-over-week and month-over-month trends for each metric
4. Generate a "top insight" per user -- the most notable change in their usage (biggest positive trend, new milestone reached, or streak maintained)
5. Write the aggregated data to a cache/storage layer your product frontend can read (database table, Redis, or API endpoint)

The n8n workflow should handle:
- Users with zero activity (show "Get started" messaging, not empty charts)
- New users with less than 7 days of data (show cumulative totals, skip trend comparisons)
- Error states (PostHog API timeout -- use cached data from previous run)

### 3. Design the analytics surface layout

The analytics surface appears as a dedicated page or panel in the product. Structure:

**Header section:**
- Greeting with the user's name
- One-sentence summary of their top insight: "You ran 34% more automations this week than last week"

**Metrics cards (3-5 cards):**
- Each card: metric name, current value, trend indicator (up/down arrow with percentage), sparkline chart (last 30 days)
- Cards sorted by most positive trend first (reinforce good behavior)

**Activity timeline:**
- Last 10 significant actions with timestamps
- Highlights milestones: "You hit 100 projects created" or "5-day streak"

**Call to action:**
- If usage is high: "You're a power user. Have you tried [underused feature]?"
- If usage is declining: "Pick up where you left off: [link to last active workflow]"
- If new milestone approaching: "3 more [actions] until you hit [milestone]"

### 4. Implement the frontend integration

The product frontend reads from the cache populated in Step 2. Instrument PostHog tracking on the analytics surface itself using `posthog-custom-events`:

```
usage_analytics_page_viewed -- user opened the analytics surface
usage_analytics_metric_clicked -- user clicked a specific metric card (property: metric_name)
usage_analytics_cta_clicked -- user clicked the call-to-action (property: cta_type)
usage_analytics_time_spent -- time on the analytics surface in seconds
```

**Human action required:** A developer must implement the frontend component that reads the aggregated data and renders the analytics surface. Provide them with: the data schema from Step 2, the layout spec from Step 3, and the PostHog event names from this step.

### 5. Set up discovery prompts

Using `intercom-in-app-messages`, create messages that drive users to the analytics surface:

- **First visit prompt** (trigger: user has never viewed the analytics page, has 7+ days of activity): "See how you're using [Product] -- check your personal stats"
- **Milestone prompt** (trigger: n8n detects user hit a new milestone): "You just hit [milestone]! See your full usage breakdown"
- **Weekly digest prompt** (trigger: every Monday for users active in the last 7 days): "Your weekly stats are ready"

Each prompt links directly to the analytics surface.

### 6. Build the email digest (optional, for Baseline+)

Using `n8n-workflow-basics`, create a weekly workflow that generates a personal usage email per user:

1. Query the aggregated data from Step 2
2. Select the top 3 metrics and the top insight
3. Format as a simple email: subject line includes a personal stat ("You saved 4.2 hours this week")
4. Send via your email platform (Loops, Intercom, or transactional email)

Only send to users who have been active in the last 14 days. Include an unsubscribe link.

## Output

- 3-5 user-facing metrics defined and tracked in PostHog
- Daily n8n aggregation workflow populating a data cache
- Analytics surface layout spec for frontend implementation
- PostHog event tracking on the analytics surface itself
- Intercom discovery prompts driving traffic to the surface
- Optional weekly email digest

## Triggers

The n8n aggregation workflow runs daily at a low-traffic hour. Intercom prompts fire based on user cohort membership in PostHog. The email digest runs weekly on Monday morning.
