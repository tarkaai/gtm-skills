---
name: intercom-knowledge-base-sync
description: Sync and maintain knowledge sources that power Intercom Fin AI and Help Center
tool: Intercom
difficulty: Config
---

# Sync Knowledge Base to Intercom

Keep your Intercom Help Center articles and Fin AI knowledge sources up to date with your product. Stale knowledge is the primary cause of low chatbot resolution rates.

## Prerequisites
- Intercom account with Help Center enabled
- Help articles already created (see `intercom-help-articles`)
- Fin AI enabled (see `intercom-fin-ai-setup`)

## Step 1: Audit Current Coverage

List all content sources feeding Fin:

```
GET https://api.intercom.io/ai/content_sources
Authorization: Bearer {access_token}
```

Response includes each source's `type`, `url`, `status`, `last_synced_at`, `article_count`, and `error_count`.

List all Help Center articles:

```
GET https://api.intercom.io/articles
```

For each article, check: `state` (published/draft), `updated_at`, `statistics` (views, helpful_count, unhelpful_count).

## Step 2: Identify Gaps from Support Conversations

Pull recent conversations where Fin failed to resolve (handed off to human):

```
POST https://api.intercom.io/conversations/search
{
  "query": {
    "operator": "AND",
    "value": [
      {"field": "created_at", "operator": ">", "value": {7_days_ago_unix}},
      {"field": "statistics.first_contact_reply_type", "operator": "=", "value": "bot"},
      {"field": "state", "operator": "=", "value": "closed"}
    ]
  }
}
```

For each handoff conversation, extract the user's initial question. Group by topic to identify knowledge gaps. Questions that appear 3+ times in a week need a new help article or custom answer.

## Step 3: Create or Update Articles via API

Create a new article:

```
POST https://api.intercom.io/articles
{
  "title": "How to export your data as CSV",
  "body": "<p>Navigate to Settings > Export. Click 'Export CSV'...</p>",
  "parent_id": "{collection_id}",
  "parent_type": "collection",
  "state": "published",
  "author_id": "{admin_id}"
}
```

Update an existing article:

```
PUT https://api.intercom.io/articles/{article_id}
{
  "body": "<p>Updated instructions for CSV export with new bulk option...</p>"
}
```

## Step 4: Add Custom Answers for Edge Cases

For questions that do not warrant a full article (policy questions, one-off answers):

```
POST https://api.intercom.io/ai/custom_answers
{
  "question": "Can I get a discount for annual billing?",
  "answer": "Yes — annual plans save 20%. Switch to annual billing in Settings > Subscription > Change to annual.",
  "tags": ["billing", "pricing"]
}
```

Review and update custom answers monthly. Remove answers for deprecated features.

## Step 5: Schedule Recurring Sync

Build an n8n workflow on a weekly cron that:

1. Pulls the list of Fin handoff conversations from the past 7 days
2. Groups unanswered questions by topic using Claude Haiku classification
3. For topics with 3+ occurrences, drafts a new help article body using Claude Sonnet
4. Creates the article in Intercom via API (state: "draft" for human review)
5. Posts a Slack summary: "3 knowledge gaps identified this week. 3 draft articles created for review."

**Human action required:** Review and publish draft articles. Fin only indexes published articles.

## Step 6: Monitor Knowledge Health

Track these metrics weekly:
- **Coverage rate**: % of Fin conversations resolved without handoff (target: >50%)
- **Article staleness**: count of articles not updated in >90 days
- **Unhelpful rate**: articles with >30% thumbs-down ratings
- **Search miss rate**: % of Help Center searches returning zero results

If coverage rate drops below 40%, prioritize gap-filling. If unhelpful rate exceeds 30% on any article, rewrite it.

## Error Handling

- If external URL crawl fails (`status: "error"`), check the URL is accessible and not blocked by robots.txt
- If article creation returns 422, verify the parent collection ID exists
- Rate limit: 1000 API calls/minute. Batch article updates in groups of 50.

## Alternative Tools

- **Zendesk Guide** — knowledge base with AI content cues — [zendesk.com/guide](https://www.zendesk.com/guide/)
- **Freshdesk Knowledge Base** — built into Freshdesk plans — [freshdesk.com](https://www.freshdesk.com/pricing)
- **HelpScout Docs** — standalone docs product — [helpscout.com/docs](https://www.helpscout.com/docs/)
- **GitBook** — docs-as-code with AI search — [gitbook.com/pricing](https://www.gitbook.com/pricing)
- **Notion + widget** — internal wiki exposed via chat widget — [notion.so](https://www.notion.so/pricing)
