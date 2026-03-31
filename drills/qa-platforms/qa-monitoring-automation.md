---
name: qa-monitoring-automation
description: Automated pipeline that discovers new Q&A questions across platforms and routes high-priority ones for response
category: QA Platforms
tools:
  - n8n
  - Stack Exchange API
  - SerpAPI
  - Slack
fundamentals:
  - qa-question-monitoring
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
---

# Q&A Monitoring Automation

This drill builds an always-on pipeline that monitors Stack Overflow, Quora, and Dev.to for new questions matching your expertise. It filters, scores, prioritizes, and routes questions to a Slack channel (or directly into the answer queue) so you respond within hours of a question being posted.

## Input

- Tag and keyword maps from `qa-question-discovery` drill
- Slack channel for alerts (e.g., `#qa-engagement`)
- n8n instance URL and credentials for Stack Exchange API, SerpAPI

## Steps

### 1. Build the Stack Overflow monitoring workflow

Using `n8n-workflow-basics` and `qa-question-monitoring`, create:

**Workflow: Stack Overflow Question Monitor**

```
Schedule Trigger (every 30 minutes)
  -> HTTP Request Node (Stack Exchange API):
     URL: https://api.stackexchange.com/2.3/search/advanced
     Query params:
       order: desc
       sort: creation
       tagged: {{PRIMARY_TAG_1}};{{PRIMARY_TAG_2}}
       fromdate: {{$now.minus(35, 'minutes').toUnixInteger()}}
       accepted: false
       site: stackoverflow
       key: {{$credentials.stackExchangeApiKey}}
       filter: withbody
       pagesize: 50
  -> Function Node (dedup + filter):
     - Check question_id against stored processed IDs (n8n static data)
     - Remove questions with score < -1 (community-rejected)
     - Remove questions from users with reputation < 5 (often spam)
     - Remove questions older than 6 hours (stale)
  -> Function Node (score):
     For each question:
       unanswered_bonus = (answer_count == 0) ? 30 : (answer_count == 1) ? 15 : 0
       view_bonus = Math.min(view_count / 100, 20)
       recency_bonus = (age_hours < 1) ? 25 : (age_hours < 3) ? 20 : (age_hours < 6) ? 10 : 0
       tag_bonus = primary_tag_match ? 15 : adjacent_tag_match ? 8 : 0
       keyword_bonus = title_contains_keyword ? 10 : 0
       total = unanswered_bonus + view_bonus + recency_bonus + tag_bonus + keyword_bonus
     Classify:
       total >= 60: "high"
       total >= 35: "medium"
       total < 35: "low"
  -> IF Node:
     High/Medium -> Slack alert
     Low -> log only (skip alert)
  -> Slack Node:
     Channel: #qa-engagement
     Message:
       **[{{priority}}]** New SO question
       *{{title}}*
       Tags: {{tags.join(', ')}}
       Score: {{score}} | Views: {{view_count}} | Answers: {{answer_count}}
       {{link}}
       Respond within: {{priority == 'high' ? '2 hours' : '6 hours'}}
```

### 2. Build the Quora monitoring workflow

```
Schedule Trigger (every 6 hours)
  -> HTTP Request Node (SerpAPI):
     URL: https://serpapi.com/search.json
     Params:
       engine: google
       q: site:quora.com {{KEYWORD_1}} OR {{KEYWORD_2}} OR {{KEYWORD_3}}
       tbs: qdr:d
       api_key: {{$credentials.serpApiKey}}
       num: 20
  -> Function Node (parse + dedup):
     - Extract question URLs and titles from organic results
     - Dedup against stored processed URLs
     - Filter out "unanswered" Quora pages (aggregation pages, not real questions)
  -> Function Node (score):
     - Recent (< 24h) + keyword match = high priority
     - Older or weaker match = medium
  -> Slack Node:
     Channel: #qa-engagement
     Message:
       **[{{priority}}]** New Quora question
       *{{title}}*
       {{url}}
       Keywords matched: {{keywords}}
```

### 3. Build the Dev.to monitoring workflow

```
Schedule Trigger (every 2 hours)
  -> HTTP Request Node (Dev.to API):
     URL: https://dev.to/api/articles
     Params:
       tag: help
       top: 1
       per_page: 30
  -> Function Node (filter):
     - Title or tags contain your keywords
     - Published within last 4 hours
     - Comments < 10 (still room to contribute)
     - Dedup against processed IDs
  -> Slack Node:
     Channel: #qa-engagement (same channel)
```

### 4. Add daily summary workflow

```
Schedule Trigger (daily at 9:00 AM)
  -> Function Node:
     Aggregate from n8n static data:
     - Questions discovered yesterday (by platform)
     - Questions alerted (high + medium)
     - Questions responded to (from activity log)
     - Response rate: responded / alerted
  -> Slack Node:
     Channel: #qa-engagement
     Message:
       **Daily Q&A Summary**
       | Platform | Discovered | Alerted | Responded | Rate |
       |----------|-----------|---------|-----------|------|
       | Stack Overflow | {{so_discovered}} | {{so_alerted}} | {{so_responded}} | {{so_rate}}% |
       | Quora | {{quora_discovered}} | {{quora_alerted}} | {{quora_responded}} | {{quora_rate}}% |
       | Dev.to | {{devto_discovered}} | {{devto_alerted}} | {{devto_responded}} | {{devto_rate}}% |

       Unanswered high-priority questions: {{unanswered_high}}
```

### 5. Tune filters after first week

After 7 days of monitoring, evaluate:

- **Alert volume**: Target 5-15 actionable questions per day across all platforms
- **False positive rate**: If > 30% of alerts are irrelevant, tighten tag/keyword filters
- **Response window**: If most questions have 3+ answers by the time you see them, increase polling frequency
- **Platform mix**: If one platform produces 80%+ of leads, concentrate monitoring there

Adjust the n8n workflows:
- Add negative keywords to filter out recurring irrelevant topics
- Adjust score thresholds to reduce noise
- Change polling intervals based on platform activity patterns

## Output

- Three automated monitoring workflows (Stack Overflow, Quora, Dev.to)
- Unified Slack channel receiving prioritized question alerts
- Daily summary workflow with response tracking
- Tuned filters producing 5-15 actionable alerts per day

## Triggers

- Set up once at Baseline level
- Runs continuously (automated)
- Filter tuning: weekly for first month, biweekly thereafter
- Full keyword/tag review: monthly
