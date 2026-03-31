---
name: qa-authority-performance-monitor
description: Track answer performance, reputation growth, profile clicks, and lead attribution across Q&A platforms
category: QA Platforms
tools:
  - Stack Exchange API
  - PostHog
  - n8n
  - Attio
fundamentals:
  - qa-platform-api-read
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - n8n-scheduling
  - attio-lists
---

# Q&A Authority Performance Monitor

This drill tracks the full funnel from Q&A answers to pipeline: answer performance metrics (upvotes, accepted answers), reputation growth, profile click-through, referral traffic, and lead attribution. It produces a weekly report and feeds data to the `autonomous-optimization` drill at Durable level.

## Input

- Activity log of posted answers (from `qa-answer-crafting` drill)
- PostHog tracking configured with UTM parameters (from `posthog-gtm-events` drill)
- Stack Exchange API credentials for reading user stats
- Attio with contact records that include `lead_source` field

## Steps

### 1. Set up PostHog event tracking for Q&A traffic

Using `posthog-custom-events`, define these events:

```javascript
// Fired when a visitor arrives from a Q&A platform (detected via UTM or referrer)
posthog.capture('qa_referral_visit', {
    source_platform: 'stackoverflow',  // stackoverflow, quora, devto
    source_url: document.referrer,
    landing_page: window.location.pathname,
    campaign: 'q-a-sites-stackoverflow-etc'
});

// Fired when a Q&A referral visitor signs up
posthog.capture('qa_signup', {
    source_platform: 'stackoverflow',
    attribution_answer_url: 'stored from session',
    campaign: 'q-a-sites-stackoverflow-etc'
});

// Fired when a Q&A referral visitor books a meeting
posthog.capture('qa_meeting_booked', {
    source_platform: 'stackoverflow',
    campaign: 'q-a-sites-stackoverflow-etc'
});
```

Configure PostHog to detect Q&A referrals automatically:
- `$initial_referrer` contains `stackoverflow.com` -> fire `qa_referral_visit` with `source_platform: 'stackoverflow'`
- `$initial_referrer` contains `quora.com` -> fire with `source_platform: 'quora'`
- `$initial_referrer` contains `dev.to` -> fire with `source_platform: 'devto'`
- UTM params: `utm_source=stackoverflow&utm_medium=qa&utm_campaign=q-a-sites-stackoverflow-etc`

### 2. Build the answer performance tracking workflow

Using `n8n-scheduling`, create a workflow that runs daily:

**Workflow: Q&A Answer Performance Tracker**

```
Schedule Trigger (daily at 7:00 AM)
  -> Function Node: Load list of answer IDs from Attio (posted in last 90 days)
  -> HTTP Request Node (Stack Exchange API - batch):
     URL: https://api.stackexchange.com/2.3/answers/{{ANSWER_IDS_SEMICOLON_SEPARATED}}
     Params:
       site: stackoverflow
       key: API_KEY
       filter: withbody
     (Stack Exchange supports up to 100 IDs per request)
  -> Function Node (extract metrics per answer):
     For each answer:
       - score (upvotes - downvotes)
       - is_accepted (boolean)
       - last_activity_date
       - comment_count
       - delta_score (today's score minus yesterday's stored score)
  -> Attio Node: Update each answer record in the "Q&A Answer Queue" list
  -> Function Node (aggregate):
     - Total answers posted (lifetime, last 7 days, last 30 days)
     - Total upvotes earned (lifetime, last 7 days)
     - Accepted answer count and rate
     - Average score per answer
     - Top 5 answers by score
     - Answers with negative scores (quality issues)
```

### 3. Track reputation growth

Using `qa-platform-api-read`:

```
Schedule Trigger (daily)
  -> HTTP Request Node:
     GET /users/YOUR_USER_ID?site=stackoverflow&key=API_KEY
  -> Function Node:
     Extract:
       - reputation (current)
       - reputation_change_day
       - reputation_change_week
       - reputation_change_month
       - badge_counts (gold, silver, bronze)
     Log to Attio as a daily snapshot
```

Reputation milestones matter because they unlock capabilities:
- 15 rep: upvote privilege (can upvote others' content to build community)
- 50 rep: comment privilege (can engage in conversations on others' posts)
- 125 rep: downvote privilege
- 200 rep: reduced advertising (signals active user)
- 1000 rep: established user (show up in tag top users)
- 2000 rep: edit privilege (can improve others' posts, building visibility)

Track these milestones and alert when reached -- each unlocks new engagement strategies.

### 4. Build the PostHog Q&A dashboard

Using `posthog-dashboards`, create a dashboard named "Q&A Site Authority":

**Panel 1: Referral Traffic Trend**
- Line chart: `qa_referral_visit` events over time, broken down by `source_platform`
- Comparison: current week vs previous week

**Panel 2: Conversion Funnel**
- Funnel: `qa_referral_visit` -> `page_viewed` (any page beyond landing) -> `qa_signup` -> `qa_meeting_booked`
- Breakdown by `source_platform`

**Panel 3: Top Referral Sources**
- Table: referral sessions grouped by `source_url`, sorted by count
- Shows which specific answers drive the most traffic

**Panel 4: Profile Click Rate**
- Metric: (qa_referral_visit where landing_page = /about or /profile) / total_qa_referral_visit
- This approximates how often Q&A viewers click through to learn about you

**Panel 5: Lead Attribution**
- Bar chart: `qa_signup` events per week, stacked by `source_platform`

**Panel 6: Answer Performance**
- Metric tiles: total answers posted, avg score, accepted rate, total upvotes this week

### 5. Configure anomaly detection

Using `posthog-anomaly-detection`, set alerts for:

- **Referral traffic drop**: `qa_referral_visit` events fall >40% vs 4-week average. Investigate: did a high-traffic answer get deleted or downvoted? Did a competitor post a better answer?
- **Conversion rate shift**: `qa_signup / qa_referral_visit` changes >50% vs 4-week average. Check landing page or signup flow for issues.
- **Profile click spike**: Sudden increase may indicate a viral answer. Identify and replicate the pattern.
- **Reputation stall**: Reputation growth rate drops to near zero for 2+ weeks. Answers may be lower quality or targeting wrong tags.

### 6. Generate the weekly Q&A performance report

```
Schedule Trigger (weekly, Monday 8:00 AM)
  -> [Pull all data from steps 2-4]
  -> Function Node (compile report):

## Q&A Authority Report -- Week of {{date}}

### Answer Activity
- Answers posted this week: {{posted}}
- Total upvotes earned: {{upvotes}}
- Accepted answers: {{accepted}} ({{accepted_rate}}%)
- Current reputation: {{reputation}} (+{{rep_change_week}} this week)

### Traffic & Conversions
- Referral sessions: {{sessions}} ({{sessions_delta}} vs last week)
- Signups from Q&A: {{signups}}
- Meetings booked: {{meetings}}
- Conversion rate: {{conversion_rate}}%

### Platform Breakdown
| Platform | Answers | Upvotes | Sessions | Signups |
|----------|---------|---------|----------|---------|
| Stack Overflow | {{so_answers}} | {{so_upvotes}} | {{so_sessions}} | {{so_signups}} |
| Quora | {{quora_answers}} | {{quora_upvotes}} | {{quora_sessions}} | {{quora_signups}} |
| Dev.to | {{devto_answers}} | {{devto_upvotes}} | {{devto_sessions}} | {{devto_signups}} |

### Top Performing Answers
{{top_5_answers_by_upvotes_this_week}}

### Issues & Actions
{{anomaly_alerts_summary}}
{{reputation_milestone_progress}}

  -> Slack Node: Post to #qa-engagement
  -> Attio Node: Store report as note on campaign record
```

## Output

- Daily answer performance tracking (upvotes, accepted answers, reputation)
- PostHog dashboard with referral traffic, conversion funnel, and attribution
- Anomaly detection alerts for significant changes
- Weekly performance report posted to Slack and stored in Attio
- Historical data for `autonomous-optimization` drill at Durable level

## Triggers

- Daily: answer performance update, reputation tracking
- Weekly: comprehensive performance report
- Real-time: anomaly alerts via PostHog
