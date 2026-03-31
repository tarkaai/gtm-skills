---
name: chatbot-resolution-monitor
description: Monitor AI chatbot resolution rate, CSAT, escalation patterns, and support load impact
category: Enablement
tools:
  - PostHog
  - Intercom
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - posthog-funnels
  - n8n-scheduling
  - attio-reporting
---

# Chatbot Resolution Monitor

This drill creates the monitoring layer for an AI support chatbot. It tracks resolution rate, user satisfaction, escalation patterns, and the chatbot's impact on support load. It provides the data that the `autonomous-optimization` drill uses at Durable level.

## Input

- PostHog events flowing from chatbot interactions (`chatbot_conversation_started`, `chatbot_resolved_by_ai`, `chatbot_escalated_to_human`, `chatbot_csat_submitted`, `chatbot_article_suggested`)
- Intercom workspace with Fin AI metrics
- n8n instance for scheduled reporting
- At least 2 weeks of chatbot data for meaningful baselines

## Steps

### 1. Build the chatbot performance dashboard

Use `posthog-dashboards` to create a dedicated "AI Support Chatbot" dashboard with these panels:

- **Resolution rate trend**: Daily % of conversations resolved by AI vs escalated to human. 30-day rolling window. Target line at 50%.
- **CSAT by resolver**: Average satisfaction score for AI-resolved vs human-resolved conversations. Side-by-side comparison.
- **Escalation reasons breakdown**: Pie chart of handoff reasons (low_confidence, user_request, max_replies, topic_rule). Shows where the bot fails.
- **Top unresolved topics**: Bar chart of most frequent topics in escalated conversations. Identifies knowledge gaps.
- **Article suggestion click-through**: % of suggested articles that users clicked. Low click-through suggests articles are not matching user intent.
- **Conversation volume trend**: Total daily conversations (AI + human). Watch for whether AI support increases total conversation volume (users engage more because the barrier is lower).
- **Time to resolution**: Median time from first message to resolution, split by AI vs human. AI should be significantly faster.
- **Support load impact**: Human agent ticket volume before and after chatbot launch. The key business metric.

### 2. Configure anomaly alerts

Use `posthog-anomaly-detection` to set alerts:

- Resolution rate drops >10 percentage points below 4-week average for 3 consecutive days → knowledge base degradation or product change broke answers
- CSAT drops below 3.0 for AI-resolved conversations for 5 consecutive days → chatbot giving wrong answers
- Escalation rate exceeds 70% for 3 consecutive days → chatbot unable to help most users
- A single topic accounts for >30% of all escalations in a day → specific product issue or outage generating support load

### 3. Build escalation analysis funnel

Use `posthog-funnels` to track the full conversation journey:

1. `chatbot_conversation_started`
2. `chatbot_article_suggested` (optional step — not all conversations get article suggestions)
3. `chatbot_resolved_by_ai` OR `chatbot_escalated_to_human`
4. `chatbot_csat_submitted`

Break down by: user plan, user tenure (days since signup), time of day, topic. Identify which user segments get the most value from the chatbot.

### 4. Create user cohorts for analysis

Use `posthog-cohorts` to create:

- **Chatbot promoters**: Users who rated AI-resolved conversations 4-5 stars
- **Chatbot detractors**: Users who rated AI-resolved conversations 1-2 stars
- **Repeat escalators**: Users who triggered 3+ handoffs in 30 days (frustrated, need better self-serve resources or human attention)
- **AI-only users**: Users whose last 5 conversations were all AI-resolved (fully self-serve, low support cost)

### 5. Generate weekly chatbot health report

Use `n8n-scheduling` to run weekly:

1. Pull chatbot metrics from PostHog for the past 7 days
2. Pull Fin AI metrics from Intercom API: `GET /ai/agent/metrics?period=7d`
3. Compare to previous week and 4-week baseline
4. Generate report with Claude:

```
Prompt: "Generate a weekly AI support chatbot health report.

This week:
{metrics_json}

Previous week:
{prev_metrics_json}

4-week average:
{avg_metrics_json}

Include:
1. Headline: one-sentence verdict (improving/stable/declining)
2. Resolution rate: current vs target (50%), trend direction
3. CSAT comparison: AI-resolved vs human-resolved conversations
4. Top 3 knowledge gaps: most escalated topics this week
5. Support load impact: change in human agent ticket volume
6. Recommendation: one specific action for this week

Keep under 250 words. Write for a support team lead."
```

5. Post to Slack and store in Attio using `attio-reporting`.

### 6. Track knowledge gap closure

Maintain a running list of identified knowledge gaps and their status:
- Gap identified (topic + frequency)
- Article drafted
- Article published
- Resolution rate for that topic (before vs after article)

Report the gap closure rate: how many gaps identified in the last 30 days have been resolved?

## Output

- Live PostHog dashboard with chatbot performance metrics
- Automated anomaly alerts for resolution rate and CSAT degradation
- Weekly health reports delivered to Slack
- User cohorts for segmented analysis
- Knowledge gap tracking with closure metrics

## Triggers

- **Dashboard**: Always-on, real-time updates as PostHog events flow
- **Anomaly alerts**: Checked daily via n8n cron
- **Weekly report**: Every Monday morning via n8n cron
