---
name: video-tutorial-health-monitor
description: Continuous monitoring of video tutorial library performance with per-video health scores, content freshness tracking, and automated reporting
category: Enablement
tools:
  - PostHog
  - Loom
  - n8n
  - Attio
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-cohorts
  - posthog-custom-events
  - loom-analytics
  - loom-workspace-management
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Video Tutorial Health Monitor

This drill creates a continuous monitoring system for the video tutorial library. It tracks per-video performance, detects content that is underperforming or stale, identifies gaps in tutorial coverage, and generates weekly reports. This drill feeds anomaly data into the `autonomous-optimization` drill for automated experimentation.

## Input

- Video tutorial engagement tracking configured (from `video-tutorial-engagement-tracking` drill)
- At least 15 published tutorials with 4+ weeks of engagement data
- PostHog with video event taxonomy implemented
- n8n instance for scheduled monitoring
- Attio configured for logging observations

## Steps

### 1. Build the video library health dashboard

Using `posthog-dashboards`, create a dashboard titled "Video Tutorial Library Health" with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Library-wide play rate (weekly trend) | Line chart | Are users starting videos more or less over time |
| Library-wide completion rate (weekly trend) | Line chart | Are videos holding attention |
| Post-video activation rate (weekly trend) | Line chart | Are tutorials driving action |
| Per-video play rate (ranked table) | Table sorted by play rate | Which videos attract clicks |
| Per-video completion rate (ranked table) | Table sorted by completion | Which videos hold attention |
| Per-video activation rate (ranked table) | Table sorted by activation | Which videos drive action |
| Surface effectiveness (bar chart) | Grouped bar | Compare in-app vs email vs help center |
| Persona engagement (stacked bar) | Stacked weekly | Which personas engage with tutorials |
| New vs returning video watchers | Area chart | Is the audience growing or recycling |
| Content freshness (table) | Table with last-updated dates | Which tutorials are stale |

### 2. Define per-video health scores

Score each video on a 0-100 scale using three metrics:

- **Engagement score (0-40):** play rate relative to impressions. Top quartile = 40, bottom quartile = 10.
- **Retention score (0-30):** completion rate. 80%+ = 30, 60-80% = 20, 40-60% = 10, <40% = 0.
- **Impact score (0-30):** post-video activation rate. Top quartile = 30, bottom quartile = 5.

Health classification:
- 70-100: **Healthy** -- performing well, no action needed
- 40-69: **Watch** -- underperforming on one dimension, investigate
- 0-39: **Critical** -- underperforming on multiple dimensions, rewrite or retire

### 3. Build the daily monitoring workflow

Using `n8n-scheduling` and `n8n-workflow-basics`, create a workflow that runs daily at 07:00 UTC:

1. Query PostHog for each video's metrics from the last 7 days
2. Query Loom API via `loom-analytics` for view counts and watch percentages
3. Calculate health scores for each video
4. Compare each video's current health score against its 4-week rolling average
5. Classify: **stable** (within 10%), **declining** (>15% drop), **improving** (>15% increase)

If any video moves to Critical status:
- Send alert: "VIDEO ALERT: '{video_title}' health dropped to {score} (was {previous}). Play rate: {X}%, Completion: {Y}%, Activation: {Z}%. Suggested action: {rewrite hook | shorten duration | update CTA | retire and replace}."
- Log to Attio using `attio-notes`

If any video has 0 impressions in 14 days:
- Flag as "orphaned" -- the video exists but is not being surfaced to users
- Suggested action: add to an Intercom message, include in an email sequence, or archive

### 4. Track content freshness

Using `loom-workspace-management`, maintain a content registry:

For each tutorial, track:
- `video_id`: Loom video ID
- `created_date`: when the video was first published
- `last_updated_date`: when the video was last re-recorded
- `product_version_at_recording`: the product version when the video was made
- `current_product_version`: the current product version

Flag videos where `current_product_version` differs from `product_version_at_recording` by a major version as "potentially stale." The UI may have changed, making the tutorial confusing.

Using `n8n-scheduling`, run a weekly check:
1. Compare each video's `product_version_at_recording` against the current product version
2. If stale, add to the "Needs Re-recording" list
3. Priority-rank by health score (re-record high-impact stale videos first)

### 5. Detect tutorial coverage gaps

Using `posthog-cohorts`, identify users who:
- Activated without watching any tutorial (they found their own way -- study what they did)
- Watched tutorials but did not activate (tutorials are not effective for this path)
- Searched help center for topics with no matching tutorial (unmet demand)

Using `posthog-custom-events`, track help center searches and in-app search queries. Group by topic. Topics with high search volume but no matching tutorial are gaps in your library.

Generate a monthly "Coverage Gap Report":
```
# Tutorial Coverage Gap Report -- {month}

## Topics with user demand but no tutorial
1. {topic} -- {N} searches, {M} support tickets
2. ...

## Activation paths with no tutorial coverage
1. {path description} -- {N} users took this path, {X}% activated

## Tutorials with declining relevance
1. {video_title} -- health score dropped {X} points in 4 weeks
```

### 6. Generate the weekly health report

Using `n8n-scheduling`, create a workflow that runs every Monday at 09:00 UTC:

```
# Video Tutorial Library Health -- Week of {date}

## Summary
- Total tutorials: {N}
- Healthy: {N} | Watch: {N} | Critical: {N}
- Library-wide play rate: {X}% (prev: {Y}%)
- Library-wide completion rate: {X}% (prev: {Y}%)
- Post-video activation rate: {X}% (prev: {Y}%)

## Top Performers (highest impact score)
| Video | Play Rate | Completion | Activation | Health |
|-------|-----------|------------|------------|--------|
| ...   | ...       | ...        | ...        | ...    |

## Underperformers (needs attention)
| Video | Issue | Suggested Action |
|-------|-------|-----------------|
| ...   | Low completion (22%) | Shorten from 5min to 2min, rewrite hook |
| ...   | Zero impressions | Add to onboarding email sequence |

## Content Freshness
- Videos needing re-recording: {N}
- Highest-priority re-record: {video_title} (health: {score}, stale since {date})

## Experiments in Flight
- {List any active A/B tests from autonomous-optimization}

## Recommended Actions
1. {Highest-impact recommendation based on data}
2. {Second recommendation}
```

Post to Slack and store in Attio as a note.

### 7. Connect to autonomous optimization

This drill's output feeds directly into the `autonomous-optimization` drill:

- **Video health decline** triggers the Diagnose phase
- **Health score components** determine hypothesis space: low play rate leads to testing thumbnails/placement, low completion leads to testing video length/structure, low activation leads to testing CTAs
- **Weekly health report** provides context for hypothesis generation
- **Coverage gap data** informs which new tutorials to prioritize

## Output

- Video library health dashboard with 10 panels
- Per-video health scoring (0-100, three components)
- Daily monitoring workflow with Critical alerts
- Content freshness tracking with re-recording priority list
- Coverage gap detection and monthly reporting
- Weekly structured health report
- Integration with autonomous-optimization for automated response

## Triggers

Daily health check runs at 07:00 UTC. Weekly report generates every Monday at 09:00 UTC. Content freshness check runs weekly. Coverage gap report generates monthly. Re-run the full setup when adding new video categories or changing the health scoring formula.
