---
name: ugc-submission-webhook
description: Receive and process user-generated content submissions via webhook endpoint
tool: n8n
product: n8n
difficulty: Config
---

# UGC Submission Webhook

Receive user-generated content submissions (tutorials, reviews, templates, use cases) from in-product forms, email replies, or third-party platforms and route them into a processing pipeline.

## n8n Webhook Setup

Create an n8n webhook node that accepts POST requests with content submissions.

**Endpoint:** `POST /webhook/ugc-submission`

**Expected payload:**

```json
{
  "submitter_email": "user@example.com",
  "submitter_name": "Jane Doe",
  "content_type": "tutorial|review|template|use_case|video|blog_post",
  "title": "How I automated my weekly reports with [Product]",
  "content_url": "https://...",
  "content_body": "Full text if inline submission",
  "platform": "in_product|email|twitter|linkedin|blog|youtube|github",
  "tags": ["automation", "reporting"],
  "submitted_at": "2026-03-30T12:00:00Z"
}
```

**n8n workflow steps:**

1. **Webhook trigger** — receives the submission
2. **Validation node** — check required fields: `submitter_email`, `content_type`, at least one of `content_url` or `content_body`. Reject with 400 if missing.
3. **Deduplication node** — query Attio or a storage table to check if this URL or content body hash was already submitted. Skip duplicates.
4. **Enrichment node** — look up the submitter in Attio CRM to get their account, plan tier, power user score, and advocacy tier. Attach as metadata.
5. **PostHog event node** — fire `ugc_submitted` event with properties:
   ```json
   {
     "content_type": "tutorial",
     "platform": "blog",
     "submitter_tier": "pro",
     "power_user_score": 72,
     "advocacy_tier": "insider"
   }
   ```
6. **Storage node** — create an Attio note or record with the submission details, status `pending_review`, and a link to the content.
7. **Response** — return 200 with `{ "status": "received", "submission_id": "..." }`

## Integration Points

**In-product submission form:** Build a simple form (Intercom custom bot or in-app modal) that POSTs to this webhook. Fields: content type dropdown, title, URL or text body, optional tags.

**Email-based submissions:** Configure an n8n email trigger on a dedicated address (e.g., ugc@yourproduct.com) that parses the email body and POSTs to this webhook.

**Social monitoring:** When the `community-monitoring-automation` drill or `slack-discord-monitoring-automation` drill detects a user sharing product content, it POSTs the discovered content to this webhook with `platform` set to the source.

## Authentication

Use a shared secret header (`X-UGC-Webhook-Secret`) for requests from external sources. In-product submissions authenticate via the user's session. n8n validates the secret before processing.

## Error Handling

- Invalid payload: return 400 with specific field errors
- Duplicate submission: return 200 with `{ "status": "duplicate", "original_id": "..." }`
- Attio lookup failure: proceed without enrichment, flag for manual enrichment later
- PostHog event failure: log the error, do not block the submission pipeline

## Tool Alternatives

| Tool | Purpose | Notes |
|------|---------|-------|
| n8n | Primary webhook + workflow | Self-hosted or cloud |
| Zapier | Alternative webhook handler | Webhook trigger on paid plans |
| Make (Integromat) | Alternative workflow | HTTP module for webhooks |
| Pipedream | Alternative webhook | Built-in webhook triggers, code steps |
| Tray.io | Enterprise alternative | For larger-scale UGC processing |
