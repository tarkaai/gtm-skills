---
name: ama-performance-monitoring
description: Track AMA series performance over time, detect format fatigue, and recommend topic/subreddit adjustments
category: Community
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - attio-lists
  - attio-notes
---

# AMA Performance Monitoring

This drill builds the monitoring layer specific to a recurring AMA series. It tracks per-session and cross-session trends, detects format fatigue, and recommends adjustments to topic selection, subreddit targeting, and cadence. Feeds into `autonomous-optimization` at Durable level.

## Input

- Completed AMA sessions with engagement data in PostHog and Attio (from `ama-session-planning` drill)
- At least 3 completed AMAs (minimum data for trend detection)
- PostHog custom events: `ama_session_posted`, `ama_referral_visit`, `ama_signup`, `ama_question_asked`, `ama_answer_posted`

## Steps

### 1. Define AMA-specific tracking events

Using `posthog-custom-events`, fire these events:

```javascript
// When the AMA post goes live
posthog.capture('ama_session_posted', {
    subreddit: 'r/TARGET',
    topic: 'topic-slug',
    host: 'host-name',
    session_number: 4,
    scheduled_duration_hours: 2
});

// When someone clicks through from the AMA to your site
posthog.capture('ama_referral_visit', {
    subreddit: 'r/TARGET',
    session_number: 4,
    source_url: 'https://reddit.com/r/TARGET/comments/...'
});

// When an AMA visitor signs up
posthog.capture('ama_signup', {
    subreddit: 'r/TARGET',
    session_number: 4,
    attribution_url: 'https://reddit.com/r/TARGET/comments/...'
});
```

### 2. Build the AMA series dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

**Panel 1 -- Session comparison (bar chart):**
- X-axis: AMA session number (chronological)
- Y-axis: Total upvotes, questions asked, questions answered
- Enables visual comparison of session engagement over time

**Panel 2 -- Referral traffic per session (bar chart):**
- `ama_referral_visit` events grouped by `session_number`
- Overlay with `ama_signup` events
- Shows which sessions drive the most downstream action

**Panel 3 -- Engagement trend (line chart):**
- Rolling average of questions-per-AMA (3-session window)
- Rolling average of upvotes-per-AMA (3-session window)
- Detects engagement decay across the series

**Panel 4 -- Topic performance (table):**
- Rows: each AMA topic
- Columns: upvotes, questions, referral visits, signups, engagement-per-hour
- Sorted by engagement-per-hour to surface the best-performing topics

**Panel 5 -- Subreddit comparison (table):**
- Rows: each subreddit where an AMA was hosted
- Columns: sessions held, avg upvotes, avg questions, avg referral visits, avg signups
- Identifies which subreddits produce the best AMA results

**Panel 6 -- Conversion funnel (funnel chart):**
- `ama_session_posted` -> `ama_referral_visit` -> pricing/docs page viewed -> `signup_completed`
- Broken down by subreddit

### 3. Configure trend alerts

Using `posthog-anomaly-detection`, set automated alerts:

**Alert 1 -- Engagement decay:**
- If the latest AMA's total questions + upvotes is <60% of the 3-session rolling average
- Diagnosis: topic fatigue, audience saturation, or scheduling conflict
- Action: trigger topic and subreddit review

**Alert 2 -- Referral drop:**
- If `ama_referral_visit` events for the latest session are <50% of the 3-session average
- Diagnosis: answers weren't linking effectively, or topic didn't resonate with your ICP
- Action: review link placement strategy and topic-ICP alignment

**Alert 3 -- Conversion spike:**
- If signup rate from the latest AMA exceeds 2x the series average
- Diagnosis: this topic/subreddit combination is high-value
- Action: schedule a follow-up AMA on a related topic in the same subreddit

### 4. Build the post-AMA analysis workflow

Using `n8n-scheduling`, create a workflow that runs 48 hours after each AMA:

```
Trigger: Webhook (fired manually or by AMA follow-up automation)
  -> Reddit API: Fetch the AMA post data (upvotes, comments, awards)
  -> Reddit API: Fetch all comments on the AMA post
  -> Function Node: Compute metrics:
     - Total questions (top-level comments that are questions)
     - Total answers (host replies)
     - Response rate (answers / questions)
     - Average upvotes per answer
     - Unanswered questions count
     - Top 5 questions by upvotes
  -> PostHog API: Query ama_referral_visit and ama_signup for this session
  -> AI Agent Node (Claude):
     Input: session metrics, comparison to previous sessions, top questions
     Prompt: "Analyze this AMA's performance compared to the series average.
       1. What worked well? (topics, answer style, timing)
       2. What underperformed? Why?
       3. Which unanswered questions should be followed up on?
       4. Recommend the topic and subreddit for the next AMA.
       5. Rate this session: Strong / Average / Weak with reasoning."
  -> Attio Node: Store the session report as a note
  -> Slack Node: Post the session report to #ama-series
```

### 5. Generate the monthly series report

Using `n8n-scheduling`, run a monthly rollup:

```
AMA Series — Month [X] Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SESSIONS THIS MONTH: X
TOTAL QUESTIONS: X (avg X per session)
TOTAL UPVOTES: X (avg X per session)
REFERRAL VISITS: X (avg X per session)
SIGNUPS: X (avg X per session)

ENGAGEMENT TREND: [improving / stable / declining]
BEST SESSION: [topic] in r/[subreddit] — X questions, X upvotes
WEAKEST SESSION: [topic] in r/[subreddit] — X questions, X upvotes

TOPIC RECOMMENDATIONS FOR NEXT MONTH:
  1. [Topic] in r/[subreddit] — rationale
  2. [Topic] in r/[subreddit] — rationale

SERIES HEALTH: [Healthy / Watch / Needs Reset]
```

## Output

- PostHog dashboard with 6 panels tracking AMA series performance
- Automated post-AMA analysis reports (per session)
- Monthly series rollup reports
- Trend alerts for engagement decay and referral drops
- Topic and subreddit recommendations driven by historical data

## Triggers

- Post-AMA analysis: 48 hours after each session
- Monthly series report: 1st of each month
- Trend alerts: continuous (fired by PostHog anomaly detection)
