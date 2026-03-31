---
name: story-intelligence-reporting
description: Track which customer stories and narrative structures drive highest demo engagement and conversion, surfacing insights to improve story selection and delivery
category: Sales
tools:
  - PostHog
  - n8n
  - Attio
  - Gong
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - attio-deals
  - attio-reporting
  - gong-engagement-analysis
---

# Story Intelligence Reporting

This drill creates the monitoring and reporting layer for the demo storytelling program. It tracks which stories are used, how prospects engage with them, which narrative structures drive conversion, and where the story library has gaps. Produces weekly intelligence reports and alerts on degradation.

## Input

- PostHog events flowing from `story-matched-demo-prep` drill (`story_demo_prep_generated`, `story_demo_completed`)
- Attio deal records with story usage and demo outcomes
- Gong recordings for demo calls (optional but recommended)
- At least 2 weeks of storytelling demo data (minimum 8-10 demos)

## Steps

### 1. Define the storytelling funnel

Ensure these PostHog events are captured (from the demo prep and delivery flow):

| Event | Trigger | Key Properties |
|-------|---------|----------------|
| `story_match_scored` | Story selected for demo | `deal_id`, `story_id`, `match_score`, `pain_overlap_score` |
| `story_narrative_generated` | Narrative built | `deal_id`, `story_id`, `features_mapped`, `adaptation_depth` |
| `story_demo_prep_generated` | Full prep doc created | `deal_id`, `story_id`, `story_match_score`, `story_gap_flagged` |
| `story_demo_completed` | Demo delivered | `deal_id`, `story_id`, `outcome`, `prospect_related_to_story`, `emotional_connection_observed` |
| `demo_engagement_scored` | Gong analysis complete | `deal_id`, `story_id`, `engagement_score`, `story_connection_count` |
| `proposal_sent` | Proposal sent post-demo | `deal_id`, `story_id` |
| `deal_closed_won` | Deal won | `deal_id`, `story_id`, `deal_value` |

### 2. Build the story performance dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

1. **Story Usage Distribution**: bar chart showing how often each story is used in demos. Flag overused stories (>30% of all demos) and underused stories.
2. **Story-to-Conversion Funnel**: funnel from `story_demo_completed` -> `proposal_sent` -> `deal_closed_won`, broken down by `story_id`. Which stories have the highest conversion path.
3. **Engagement Score by Story**: average `engagement_score` per `story_id`. Which stories hold attention best.
4. **Story Connection Rate**: % of demos where `prospect_related_to_story = true`, broken down by story. Which stories make prospects see themselves.
5. **Emotional Connection Rate**: % of demos where `emotional_connection_observed = true`, by story.
6. **Match Score vs Outcome**: scatter plot of `story_match_score` vs `outcome`. Does a higher match score predict better outcomes.
7. **Story Gap Tracker**: count of demos where `story_gap_flagged = true`, broken down by prospect industry. Where do you need new stories.
8. **Weekly Demo Volume**: count of storytelling demos per week with conversion overlay.

### 3. Build the story effectiveness ranking

Create a weekly n8n workflow using `n8n-scheduling`:

1. Pull all `story_demo_completed` events from the last 30 days
2. Group by `story_id`
3. For each story, calculate:
   - Usage count (how many times used)
   - Demo-to-proposal rate (% of demos that led to a proposal)
   - Demo-to-close rate (% of demos that led to a closed deal)
   - Average engagement score (from Gong analysis)
   - Story connection rate (% where prospect related to story)
   - Emotional connection rate
4. Rank stories by a composite effectiveness score: `(demo_to_proposal_rate * 0.4) + (engagement_score_normalized * 0.3) + (story_connection_rate * 0.2) + (emotional_connection_rate * 0.1)`
5. Identify:
   - **Top 3 stories**: highest composite effectiveness. Recommend using these more.
   - **Bottom 3 stories**: lowest effectiveness. Investigate: is the story stale, poorly matched, or poorly delivered?
   - **Rising stories**: stories with improving trend over last 4 weeks
   - **Declining stories**: stories with worsening trend (may need refresh or retirement)
6. Store the ranking report in Attio as a campaign note

### 4. Build narrative structure analysis

Beyond which story is told, track HOW stories are told:

Using `gong-engagement-analysis` on each recorded demo:
- Track which story phases (problem, turning point, solution, results) correlate with highest engagement moments
- Identify if shorter or longer story arcs perform better
- Measure whether demos that start with the customer quote vs start with the customer's challenge have different outcomes
- Track whether the closing bridge question produces verbal commitment

Aggregate across demos to identify the optimal narrative structure:
- Best opening pattern (quote-first vs challenge-first vs result-first)
- Optimal story length (phases and minutes)
- Best closing technique (question type that drives next step commitment)

### 5. Set up degradation alerts

Using `n8n-triggers`, create automated alerts:

- **Story fatigue**: If any single story is used in >40% of demos for 2+ consecutive weeks, alert to diversify
- **Conversion drop**: If demo-to-proposal rate drops >20% below 4-week rolling average, alert with story-level breakdown
- **Engagement decline**: If average engagement score drops >15% for 2+ weeks, alert to investigate demo delivery quality
- **Gap expansion**: If `story_gap_flagged` events exceed 30% of demos in a week, alert to prioritize new story creation

### 6. Generate weekly intelligence brief

Weekly n8n workflow (Monday 8 AM):

1. Aggregate last 7 days of storytelling data
2. Generate a structured brief via Claude:
   ```
   ## Story Intelligence Brief — Week of {date}

   ### Performance Summary
   - Demos delivered: {count}
   - Demo-to-proposal rate: {rate} ({trend vs prior week})
   - Average engagement score: {score} ({trend})

   ### Top Performing Story
   {story_title} — used {count} times, {conversion_rate} proposal rate

   ### Story Needing Attention
   {story_title} — {reason: declining engagement / low conversion / overused}

   ### Story Gaps
   {list of industries/segments with no matching story}

   ### Narrative Insight
   {one finding about story structure that correlates with better outcomes}

   ### Recommended Actions
   1. {action_1}
   2. {action_2}
   ```
3. Post to Slack and store in Attio

## Output

- Real-time story performance dashboard in PostHog
- Weekly story effectiveness ranking
- Narrative structure analysis showing optimal demo patterns
- Degradation alerts for story fatigue, conversion drops, and engagement decline
- Weekly intelligence brief with actionable recommendations

## Triggers

- Dashboard: always-on, real-time
- Story effectiveness ranking: weekly (Monday 8 AM via n8n cron)
- Degradation alerts: daily check (9 AM via n8n cron)
- Intelligence brief: weekly (Monday 8 AM via n8n cron)
- Narrative structure analysis: monthly deep-dive (1st of month via n8n cron)
