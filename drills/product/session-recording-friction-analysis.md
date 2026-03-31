---
name: session-recording-friction-analysis
description: Systematically review PostHog session recordings to identify UX friction points and quantify their retention impact
category: Product
tools:
  - PostHog
  - Attio
fundamentals:
  - posthog-session-recording
  - posthog-funnels
  - posthog-user-path-analysis
  - attio-notes
---

# Session Recording Friction Analysis

This drill turns qualitative session recording data into structured friction reports that drive layout and UX experiments. Instead of watching random recordings, it targets recordings of users who dropped off at specific funnel steps, catalogs friction patterns, and quantifies their impact on retention.

## Prerequisites

- PostHog session recordings enabled with at least 2 weeks of data
- PostHog funnels defined for the pages/flows being analyzed
- At least 50 recordings available for the target flow
- Attio configured for storing analysis results

## Input

- **Target flow:** The funnel or page flow to analyze (e.g., "pricing page to signup", "dashboard first visit", "settings configuration")
- **Drop-off step:** The specific funnel step where users are lost (identified from PostHog funnel data)
- **Sample size:** Minimum 15 recordings per segment (drop-off users vs. completed users)

## Steps

### 1. Pull the funnel data

Using `posthog-funnels`, identify the exact drop-off points:

```
GET /api/projects/<id>/insights/funnel/
{
  "events": [
    {"id": "page_viewed", "properties": {"path": "/pricing"}},
    {"id": "signup_started"},
    {"id": "signup_completed"}
  ],
  "date_from": "-30d"
}
```

Rank the drop-off steps by volume. The step with the highest absolute drop-off count is where friction analysis has the most leverage.

### 2. Sample recordings at the drop-off step

Using `posthog-session-recording`, query recordings of users who reached the drop-off step but did NOT complete the next step:

```
GET /api/projects/<id>/session_recordings/
?events=[{"id":"<drop-off-event>"}]
&date_from=-14d
&limit=30
```

Also query recordings of users who DID complete the next step (control group):

```
GET /api/projects/<id>/session_recordings/
?events=[{"id":"<drop-off-event>"},{"id":"<next-step-event>"}]
&date_from=-14d
&limit=15
```

### 3. Review recordings with a friction taxonomy

Watch each recording and classify friction into categories. For every friction instance, log:

- **Friction type:** One of: Confusion (user pauses, scrolls up/down repeatedly), Hesitation (hovers over element but does not click), Rage-click (repeated clicks on non-interactive element), Dead-end (user reaches a point with no clear next action), Load-failure (page element fails to render or loads slowly), Scroll-past (user scrolls past the target element without stopping)
- **Element:** The specific UI element involved (e.g., "pricing toggle", "CTA button", "feature comparison table")
- **Timestamp:** When in the session it occurred
- **Device:** Desktop, tablet, or mobile
- **Outcome:** Did the user eventually complete the step or abandon?

### 4. Aggregate friction patterns

After reviewing all recordings, aggregate:

- **Frequency:** How many recordings showed each friction type at each element?
- **Severity:** What percentage of users who experienced this friction abandoned vs. continued?
- **Device skew:** Is the friction concentrated on mobile, desktop, or both?

Rank friction patterns by: `frequency x severity`. The highest-ranked pattern is the top candidate for a layout experiment.

### 5. Generate the friction report

Produce a structured report for each top friction pattern:

```
## Friction: [Type] at [Element]
- Observed in: X of Y recordings (Z%)
- Abandonment rate when friction occurs: A%
- Device distribution: Desktop B%, Mobile C%
- Hypothesis: If we [proposed change], [metric] will improve by [estimate]
- Supporting recordings: [list of recording IDs]
- Recommended experiment: [brief description of A/B test]
```

### 6. Store findings and create experiment backlog

Using `attio-notes`, log the friction report on the relevant campaign or product record in Attio. Create one note per friction pattern with:

- The friction description, frequency, and severity
- The proposed layout experiment
- Links to supporting PostHog recordings
- Priority ranking

Using `posthog-user-path-analysis`, validate that the friction pattern aligns with the broader user path data — confirm that the drop-off is real and not an artifact of the recording sample.

## Output

- A ranked list of friction patterns with frequency, severity, and device distribution
- A hypothesis and proposed experiment for each top-3 friction pattern
- Supporting recording IDs for team review
- Friction report stored in Attio for experiment planning

## Triggers

Run this drill:
- Before launching a layout experiment (to identify what to test)
- After a layout experiment shows unexpected results (to understand why)
- Monthly as part of the retention review cadence
