---
name: chatbot-knowledge-pipeline
description: Continuously identify knowledge gaps from failed chatbot conversations and generate draft articles to fill them
category: Product
tools:
  - Intercom
  - Anthropic
  - n8n
fundamentals:
  - intercom-knowledge-base-sync
  - intercom-conversations-export
  - intercom-help-articles
  - n8n-scheduling
  - n8n-workflow-basics
---

# Chatbot Knowledge Pipeline

This drill creates an always-on workflow that monitors chatbot handoff conversations, identifies recurring knowledge gaps, and generates draft articles to fill them. The goal is to continuously increase the chatbot's resolution rate by expanding its knowledge base.

## Input

- Intercom workspace with Fin AI running and conversation history accumulating
- At least 2 weeks of chatbot conversation data (enough to identify patterns)
- n8n instance for scheduling the pipeline
- Anthropic API key for content generation

## Steps

### 1. Extract handoff conversations

Use the `intercom-conversations-export` fundamental to pull conversations where Fin handed off to a human. Filter to the last 7 days. For each conversation, extract:
- The user's initial question
- Fin's attempted response (if any)
- The handoff reason (low confidence, user request, max replies, topic rule)
- The human agent's resolution (what the correct answer was)

### 2. Classify and cluster knowledge gaps

Pass the extracted questions to Claude Haiku for classification:

```
Prompt: "Classify these support questions into topic clusters.
For each cluster, provide: topic name, question count, example questions (up to 3), and whether this is a knowledge gap (no article exists) or an article quality issue (article exists but Fin couldn't use it).

Questions:
{questions_list}

Respond in JSON: [{"topic": "", "count": 0, "examples": [], "gap_type": "missing_article|article_quality"}]"
```

### 3. Prioritize gaps by impact

Rank topic clusters by:
- **Frequency**: more occurrences = higher priority
- **Resolution cost**: topics that take human agents longer to resolve save more money when automated
- **User satisfaction**: topics where CSAT is lowest during human resolution need better self-serve answers

Focus on the top 3 gaps per week. Do not try to fill every gap at once.

### 4. Generate draft articles

For each prioritized gap, use Claude Sonnet to draft an article:

```
Prompt: "Write a help article for an AI support chatbot knowledge base.

Topic: {topic}
Example user questions: {examples}
How human agents resolved these: {resolution_summaries}

Requirements:
- Title should be the question users ask (e.g., 'How do I export data as CSV?')
- Start with a 1-2 sentence direct answer
- Follow with numbered step-by-step instructions
- Include any prerequisites or permissions needed
- Keep under 400 words
- Write for a user who is frustrated and wants a fast answer
- Do not use marketing language or filler

Output the article title and body in HTML format suitable for Intercom's article API."
```

### 5. Create draft articles in Intercom

Use the `intercom-help-articles` fundamental to create each article as a draft:

```
POST https://api.intercom.io/articles
{
  "title": "{generated_title}",
  "body": "{generated_body_html}",
  "parent_id": "{appropriate_collection_id}",
  "parent_type": "collection",
  "state": "draft",
  "author_id": "{admin_id}"
}
```

**Human action required:** Review and publish draft articles. Verify accuracy, adjust tone, add screenshots if helpful. Fin only indexes published articles.

### 6. Automate as weekly pipeline

Use the `n8n-scheduling` fundamental to schedule this pipeline weekly:

1. Monday 6am: Pull handoff conversations from the past 7 days
2. Classify and cluster questions
3. Identify top 3 knowledge gaps
4. Generate draft articles for each gap
5. Create drafts in Intercom
6. Post Slack summary: "3 knowledge gaps identified. 3 draft articles ready for review: [links]"

Use the `n8n-workflow-basics` fundamental for the workflow structure: HTTP request nodes for Intercom API, code nodes for classification, and Slack node for notification.

### 7. Track pipeline effectiveness

After each weekly run, measure:
- Number of new draft articles created
- Time from gap identification to article publication (depends on human review speed)
- Resolution rate change for topics where articles were added (compare 2 weeks before vs 2 weeks after)

A successful pipeline should increase Fin's resolution rate by 2-5 percentage points per month as knowledge gaps are filled.

## Output

- Weekly identification of top knowledge gaps from chatbot handoff data
- Auto-generated draft articles for each gap
- Slack notifications for human review
- Measurable improvement in chatbot resolution rate over time

## Triggers

- **Weekly**: n8n cron every Monday morning
- **On-demand**: Run manually when resolution rate drops or after a product launch introduces new features
