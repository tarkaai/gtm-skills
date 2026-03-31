---
name: field-territory-optimization
description: Analyze field visit performance data to optimize territories, routes, timing, and venue selection
category: Field
tools:
  - PostHog
  - Attio
  - Google Maps
  - Clay
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-cohorts
  - attio-reporting
  - google-maps-place-search
  - clay-scoring
---

# Field Territory Optimization

This drill analyzes accumulated field visit data to find patterns in what locations, times, venue types, and approaches produce the most meetings. It replaces gut-feel territory selection with data-driven optimization.

## Input

- At least 4 weeks of field visit data in Attio and PostHog (from `field-contact-logging` drill)
- At least 20 logged conversations across multiple venues
- PostHog events: `field_visit_completed`, `field_conversation_logged`, `field_meeting_booked`

## Steps

### 1. Build the field performance dashboard

Use the `posthog-dashboards` fundamental to create a "Field Prospecting Performance" dashboard with these panels:

- **Conversations per visit** (bar chart by venue): Which venues produce the most conversations?
- **Meeting conversion rate by venue** (percentage): Which venues convert conversations to meetings?
- **Meeting conversion by day of week** (bar chart): Are Tuesdays better than Thursdays?
- **Meeting conversion by time of day** (bar chart): Morning vs. afternoon?
- **Conversations by interest level** (pie chart): What percentage are hot/warm/cold/not-ICP?
- **Follow-up conversion rate** (funnel): Of follow-ups sent, how many convert to meetings?
- **Pipeline value sourced from field** (trend): Revenue pipeline attributed to field visits

### 2. Analyze venue performance

Use `posthog-funnels` to build a venue-level funnel:

`field_visit_completed` → `field_conversation_logged` → `field_meeting_booked` → `deal_created`

Break down by venue. Identify:

- **High-yield venues**: High conversation count AND high meeting conversion. Visit these more.
- **High-traffic, low-conversion venues**: Many conversations but few meetings. Likely wrong ICP mix. Consider dropping or visiting less frequently.
- **Low-traffic, high-conversion venues**: Few conversations but they convert well. The ICP is there but foot traffic is low. Visit during events or busy times only.
- **Dead zones**: Low traffic AND low conversion. Remove from the route.

### 3. Optimize timing

Use `posthog-cohorts` to segment field visits by:

- Day of week: Create cohorts for each day. Compare meeting booking rates.
- Time of day: Morning (9-12) vs. afternoon (1-5). When are decision makers actually present?
- Season/month: Some venues have seasonal patterns (e.g., coworking spaces emptier in summer).

Output a recommended weekly schedule: which days and times to be in the field.

### 4. Score and rank territories

Use `attio-reporting` to pull deal data sourced from field visits. Map deals back to their originating venue and neighborhood. Calculate per-territory metrics:

- Revenue pipeline per hour in field
- Cost per meeting (travel time + expenses)
- Average deal size by territory

Use `clay-scoring` to build a territory score: revenue potential (40%), ICP density (30%), travel efficiency (20%), conversion rate (10%).

### 5. Discover new venues

Based on patterns from high-performing venues (coworking spaces with tech tenants, business parks with SMBs, etc.), use `google-maps-place-search` to find similar venues in adjacent neighborhoods or underexplored areas. Add these to a "test" route for the next field session.

### 6. Generate territory recommendations

Produce a territory optimization report:

```
## Territory Report — [Date Range]

### Top Performing Venues (visit weekly)
1. [Venue] — [X] meetings from [Y] conversations ([Z]% conversion)
2. ...

### Underperforming Venues (drop or reduce)
1. [Venue] — [X] conversations, [0] meetings. Recommend: remove from rotation.
2. ...

### Optimal Schedule
- Best days: [Tuesday, Thursday]
- Best times: [10am-12pm]
- Recommended sessions per week: [2]

### New Venues to Test
1. [Venue] — Similar profile to [Top Venue], untested
2. ...

### Metrics
- Meetings booked this period: [X]
- Pipeline created: $[X]
- Avg conversations per session: [X]
- Avg meetings per session: [X]
- Cost per meeting: $[X]
```

## Output

- Field performance dashboard in PostHog
- Venue performance rankings with data
- Optimized weekly schedule (best days/times)
- Territory scores for prioritization
- New venue recommendations for expansion
- Written territory report

## Triggers

Run monthly after at least 4 field sessions have been completed. Also run ad hoc when performance declines to diagnose whether the issue is venue selection, timing, or messaging.
