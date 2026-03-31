---
name: so-authority-monitoring
description: Track Stack Overflow reputation, badge progress, answer performance, and referral attribution for continuous authority measurement
category: QA Platforms
tools:
  - Stack Exchange API
  - PostHog
  - n8n
  - Attio
fundamentals:
  - qa-platform-api-read
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - attio-notes
---

# Stack Overflow Authority Monitoring

This drill maintains a live scorecard of your Stack Overflow authority metrics: reputation growth, tag-level expertise ranking, answer performance trends, and downstream lead attribution. It feeds data into the `autonomous-optimization` drill for Durable-level experimentation.

## Input

- Stack Overflow user ID for the answering account
- PostHog tracking configured for community referral events
- At least 4 weeks of answering data
- Target tag list from `so-tag-reconnaissance`

## Steps

### 1. Build the weekly authority snapshot workflow

Using the `n8n-scheduling` fundamental, create a workflow that runs every Monday at 7am:

```
Schedule Trigger (weekly, Monday 7am)
  -> HTTP Request Node (Stack Exchange API):
     GET /users/{USER_ID}?site=stackoverflow&key=YOUR_API_KEY
     Extract: reputation, badge_counts (gold, silver, bronze), answer_count, accept_rate
  -> HTTP Request Node (Stack Exchange API):
     GET /users/{USER_ID}/top-tags?site=stackoverflow&key=YOUR_API_KEY&pagesize=25
     Extract: per-tag answer count, score, and rank
  -> HTTP Request Node (Stack Exchange API):
     GET /users/{USER_ID}/answers?order=desc&sort=creation&site=stackoverflow&key=YOUR_API_KEY&fromdate={7_days_ago}&filter=withbody&pagesize=100
     Extract: answers posted this week with scores, views, acceptance
  -> PostHog HTTP Request Node:
     Query: community_referral_visit events where source='stackoverflow', last 7 days
     Return: total sessions, signups, grouped by utm_content (tag or question)
  -> Attio HTTP Request Node:
     Query: Deals where lead_source_detail contains 'stackoverflow', created in last 30 days
     Return: deal count, pipeline value
  -> Function Node (compute authority metrics):
     - reputation_growth: current_rep - last_week_rep
     - answers_this_week: count of answers posted
     - avg_score_this_week: mean upvote score of answers posted this week
     - acceptance_rate_this_week: accepted / total answers this week
     - top_tag_rank_changes: compare this week's per-tag scores to last week
     - referral_sessions: from PostHog
     - signups_attributed: from PostHog
     - deals_attributed: from Attio
     - authority_score: weighted composite (see formula below)
  -> Attio Node: Store weekly snapshot as note on "SO Authority" record
  -> Slack Node: Post weekly authority report
```

### 2. Define the authority score formula

Composite score (0-100) computed weekly:

| Signal | Weight | Calculation |
|--------|--------|-------------|
| Reputation growth rate | 20% | `min(rep_growth_this_week / 100 * 100, 100) * 0.20` |
| Answer volume | 15% | `min(answers_this_week / 15 * 100, 100) * 0.15` |
| Answer quality | 25% | `min(avg_score_this_week / 5 * 100, 100) * 0.25` |
| Acceptance rate | 15% | `min(acceptance_rate / 0.30 * 100, 100) * 0.15` |
| Referral traffic | 15% | `min(referral_sessions / 50 * 100, 100) * 0.15` |
| Pipeline attribution | 10% | `min(deals_attributed / 3 * 100, 100) * 0.10` |

### 3. Configure anomaly detection

Using the `posthog-anomaly-detection` fundamental, set alerts for:

- **Reputation stall**: Weekly reputation growth drops below 50% of 4-week average for 2 consecutive weeks. Investigate: are we answering fewer questions, or are answers getting fewer upvotes?
- **Quality drop**: Average answer score drops below 1.0 for a week. Investigate: are we answering outside our expertise, or are answer quality standards slipping?
- **Referral spike**: SO referral sessions exceed 3x weekly average. Investigate: which answer drove it? Can we replicate the pattern?
- **Downvote surge**: More than 3 answers receive downvotes in a week. Action: pause AI-assisted posting, review recent answers, tighten quality gates.

### 4. Generate the weekly authority report

```markdown
## SO Authority Report -- Week of {date}

### Account Summary
- Reputation: {current} (+{growth} this week)
- Total answers: {total} ({this_week} this week)
- Badges: {gold}G {silver}S {bronze}B
- Authority score: {score}/100 ({trend} from last week)

### This Week's Performance
| Metric | This Week | 4-Week Avg | Trend |
|--------|-----------|------------|-------|
| Answers posted | {n} | {avg} | {+/-}% |
| Avg upvote score | {n} | {avg} | {+/-}% |
| Acceptance rate | {n}% | {avg}% | {+/-}pp |
| Referral sessions | {n} | {avg} | {+/-}% |
| Signups attributed | {n} | {avg} | {+/-}% |

### Tag Performance
| Tag | Answers | Avg Score | Rank | Referrals |
|-----|---------|-----------|------|-----------|
| {tag} | {n} | {avg} | #{rank} | {n} |

### Top Performing Answers
1. [{title}]({url}) -- Score: {score}, Views: {views}, Accepted: {y/n}
2. ...

### Anomalies & Actions
{Any anomalies detected and recommended actions}

### Recommendations
{What to focus on next week: specific tags, question types, answer formats}
```

### 5. Feed into autonomous optimization

The authority metrics and anomaly alerts from this drill serve as input to the `autonomous-optimization` drill. When the optimization loop detects a metric anomaly, it uses authority data to generate targeted hypotheses:

- "Answer quality dropped in the `python-api` tag; hypothesis: recent answers focused on outdated library versions. Test: prioritize questions about current versions."
- "Referral traffic spiked from an answer about [topic]; hypothesis: this topic has high search volume. Test: proactively answer 5 more questions in this area."

## Output

- Weekly authority snapshot with composite score
- Anomaly alerts for reputation, quality, and referral changes
- Per-tag performance breakdown
- Historical authority data in Attio for trend analysis
- Input data for the `autonomous-optimization` drill

## Triggers

- Automated: weekly (every Monday)
- Ad-hoc: when investigating a performance change
- On-demand: before quarterly planning or strategy reviews
