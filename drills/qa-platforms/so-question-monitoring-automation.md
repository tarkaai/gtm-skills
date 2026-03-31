---
name: so-question-monitoring-automation
description: Automated pipeline that discovers high-opportunity Stack Overflow questions and routes them for answering
category: QA Platforms
tools:
  - Stack Exchange API
  - n8n
  - Slack
fundamentals:
  - qa-question-monitoring
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
---

# Stack Overflow Question Monitoring Automation

This drill builds an automated pipeline that discovers new Stack Overflow questions matching your target tags, scores them by opportunity, and routes the best ones for answering. The pipeline runs continuously and replaces manual SO browsing.

## Input

- Target tag list from the `so-tag-reconnaissance` drill (primary, secondary, watch list)
- Slack channel for engagement alerts (or email if Slack not available)
- Stack Exchange API key (10,000 requests/day)

## Steps

### 1. Build the n8n polling workflow

Using the `n8n-workflow-basics` and `n8n-triggers` fundamentals, create:

**Workflow: Stack Overflow Question Monitor**

```
Schedule Trigger (every 30 minutes)
  -> HTTP Request Node (Stack Exchange API):
     URL: https://api.stackexchange.com/2.3/search/advanced
     Params:
       order: desc
       sort: creation
       tagged: {primary_tags, semicolon-separated}
       fromdate: {{$now.minus(30, 'minutes').toUnixInteger()}}
       accepted: false
       site: stackoverflow
       key: YOUR_API_KEY
       filter: withbody
       pagesize: 100
  -> Function Node (deduplicate):
     Check question_id against static data store.
     Remove already-seen questions.
     Store new question_ids (keep last 2000).
  -> Function Node (score):
     For each question, compute opportunity_score:
       +3 if answer_count == 0 (unanswered)
       +2 if answer_count <= 2 AND no accepted answer
       +1 if view_count > 100
       +2 if question score >= 3 (community validated)
       +1 if asker reputation >= 100 (serious user, likely to accept)
       -2 if question score < 0 (likely to be closed)
       -1 if answer_count >= 5 (crowded)
  -> IF Node (filter):
     Pass only questions with opportunity_score >= 3
  -> Switch Node (prioritize):
     High: opportunity_score >= 5 AND answer_count == 0
     Medium: opportunity_score >= 3 AND answer_count <= 2
     Low: everything else that passed the filter
  -> Slack Node:
     Channel: #so-engagement
     Message:
       [{PRIORITY}] New SO question
       Title: {title}
       Tags: {tags}
       Score: {score} | Views: {view_count} | Answers: {answer_count}
       Opportunity: {opportunity_score}
       URL: {link}
       Action: Answer within {2h for high / 6h for medium / 24h for low}
```

### 2. Add secondary tag monitoring

Create a parallel branch in the same workflow or a separate workflow for secondary tags. Run every 2 hours instead of 30 minutes. Apply the same scoring but raise the opportunity_score threshold to 5 (only alert on high-value questions in secondary tags).

### 3. Add "golden question" detection

High-value patterns to detect and flag as top priority:

- **"How to [action] with [your-technology-area]?"** with 0 answers and 5+ views in first hour
- **Competitor comparison questions**: Title contains "vs" or "alternative to" plus a competitor name
- **Error questions about tools you integrate with**: Title contains a known error message your product solves
- **Bounty questions in your tags**: Use `GET /questions/featured?tagged={TAG}` to find questions with active bounties

Add these as separate detection branches in the n8n workflow, triggering with the highest priority.

### 4. Build the daily digest workflow

Using the `n8n-scheduling` fundamental:

```
Schedule Trigger (daily at 9am)
  -> Function Node: Aggregate yesterday's data from static data:
     - Questions alerted: count
     - Questions answered: count (from activity log)
     - Total upvotes earned: sum
     - Acceptance rate: accepted / answered
     - Top performing answer: highest score
  -> Slack Node:
     Channel: #so-engagement
     Message:
       SO Engagement Daily Digest
       Questions surfaced: {alerted}
       Questions answered: {answered}
       Answer rate: {answered/alerted}%
       Upvotes earned: {upvotes}
       Acceptance rate: {acceptance_rate}%
       Unanswered high-priority: {list URLs}
```

### 5. Tune the pipeline

After 1 week of monitoring, adjust:
- **Too many alerts (>20/day)**: Narrow to primary tags only, raise opportunity_score threshold
- **Too few alerts (<3/day)**: Add secondary tags to primary monitoring, lower threshold
- **Low quality alerts**: Increase minimum question score to 1, increase minimum asker reputation to 50
- **Target**: 5-15 actionable questions per day

## Output

- Automated monitoring pipeline (n8n + Stack Exchange API)
- Slack channel receiving scored, prioritized question alerts
- Daily engagement digest workflow
- Tuned tag filters producing 5-15 actionable questions/day

## Triggers

- Set up once during Baseline level
- Runs continuously (automated)
- Tag and filter review: weekly for first month, monthly thereafter
