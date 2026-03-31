---
name: intercom-ticket-tagging
description: Auto-tag and categorize Intercom conversations by topic, severity, and sentiment
tool: Intercom
product: Intercom
difficulty: Config
---

# Auto-Tag Intercom Tickets

Programmatically classify and tag Intercom conversations by category, severity, and sentiment so downstream analysis drills can aggregate patterns.

## Prerequisites
- Intercom account with API access (scopes: `read conversations`, `write conversations`, `write tags`)
- Tags pre-created in Intercom for your taxonomy
- Conversation data accessible via `intercom-conversations-export` fundamental

## Step 1: Create your tag taxonomy

Use the Intercom Tags API to create a consistent set of tags:

```
POST https://api.intercom.io/tags
{
  "name": "category:bug"
}
```

Recommended taxonomy:
- **Category tags**: `category:bug`, `category:feature-request`, `category:billing`, `category:how-to`, `category:integration`, `category:performance`, `category:access`, `category:data-loss`
- **Severity tags**: `severity:critical`, `severity:high`, `severity:medium`, `severity:low`
- **Sentiment tags**: `sentiment:frustrated`, `sentiment:neutral`, `sentiment:positive`
- **Churn signal tags**: `signal:churn-risk`, `signal:escalation`, `signal:repeat-issue`

List existing tags to avoid duplicates:

```
GET https://api.intercom.io/tags
```

## Step 2: Classify conversations with LLM

For each conversation, extract the first customer message body and pass it to an LLM for classification:

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-haiku-4-20250414",
  "max_tokens": 500,
  "messages": [{
    "role": "user",
    "content": "Classify this support ticket. Return JSON only.\n\nTicket text: \"{first_message_body}\"\n\nClassify:\n- category: one of [bug, feature-request, billing, how-to, integration, performance, access, data-loss]\n- severity: one of [critical, high, medium, low]. Critical = data loss or complete outage. High = major feature broken. Medium = workaround exists. Low = cosmetic or question.\n- sentiment: one of [frustrated, neutral, positive]\n- churn_signals: array of any that apply: [churn-risk, escalation, repeat-issue, competitor-mention, cancellation-intent]\n\nRespond: {\"category\": \"\", \"severity\": \"\", \"sentiment\": \"\", \"churn_signals\": []}"
  }]
}
```

Use claude-haiku-4-20250414 for cost efficiency at volume. Estimated cost: ~$0.001 per ticket classification.

## Step 3: Apply tags via API

```
POST https://api.intercom.io/tags
{
  "name": "category:bug",
  "conversations": [{"id": "{conversation_id}"}]
}
```

Apply each relevant tag from the classification. A single conversation may receive multiple tags (e.g., `category:bug` + `severity:high` + `sentiment:frustrated` + `signal:churn-risk`).

## Step 4: Batch processing

For historical backfill, iterate over all conversations from the past 90 days:

1. Use `intercom-conversations-export` to pull conversations
2. Filter to those without category tags (avoid re-tagging)
3. Classify each with the LLM
4. Apply tags in batch

Rate limit: process ~100 conversations per minute to stay within Intercom API limits.

## Step 5: Real-time tagging via webhook

For ongoing classification, set up an Intercom webhook for `conversation.created` events:

```
POST https://api.intercom.io/subscriptions
{
  "service_type": "web",
  "url": "https://your-n8n-instance.com/webhook/intercom-ticket-tag",
  "topics": ["conversation.created"]
}
```

The webhook payload contains the conversation ID. Your n8n workflow fetches the full conversation, classifies it, and applies tags within seconds of ticket creation.

## Error Handling

- If LLM classification fails, tag as `category:unclassified` and queue for retry
- If Intercom tag API fails with 404, the tag was deleted; recreate it first
- Log all classifications for audit: conversation_id, classification result, confidence
