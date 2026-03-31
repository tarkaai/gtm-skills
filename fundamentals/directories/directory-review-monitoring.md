---
name: directory-review-monitoring
description: Monitor, fetch, and respond to product reviews across software directories via APIs and webhooks
tool: G2 / Capterra / Product Hunt / TrustRadius / n8n
difficulty: Config
---

# Directory Review Monitoring

Programmatically monitor incoming reviews, detect sentiment, and post responses across software review directories. This fundamental covers the read/write operations for review management.

## G2 Review API

### Fetch recent reviews

**Endpoint:** `GET https://seller.g2.com/api/v1/products/{product_id}/reviews`

```
Headers:
  Authorization: Bearer {G2_API_TOKEN}

Query parameters:
  since: "2026-03-01T00:00:00Z"
  sort: "created_at_desc"
  per_page: 25
  page: 1
```

**Response schema:**
```json
{
  "reviews": [
    {
      "id": "review-123",
      "title": "Great tool for our team",
      "rating": 4.5,
      "pros": "Easy to set up, great support",
      "cons": "Could use more integrations",
      "reviewer": {
        "name": "Jane D.",
        "title": "VP Marketing",
        "company_size": "51-200",
        "industry": "SaaS"
      },
      "created_at": "2026-03-15T10:30:00Z",
      "verified": true,
      "vendor_response": null
    }
  ],
  "meta": { "total": 45, "page": 1, "per_page": 25 }
}
```

### Respond to a review

**Endpoint:** `POST https://seller.g2.com/api/v1/reviews/{review_id}/responses`

```
Headers:
  Authorization: Bearer {G2_API_TOKEN}
  Content-Type: application/json

Body:
{
  "body": "Thank you for the detailed review, Jane. We appreciate the feedback on integrations -- we're shipping 5 new integrations this quarter. Happy to hear setup was smooth for your team."
}
```

**Response guidelines:**
- Respond within 48 hours of review posting
- Thank the reviewer by name
- Address specific feedback (both positive and negative)
- Never be defensive about criticism
- Mention relevant upcoming features for negative points
- Keep responses under 200 words

### Set up review webhooks

**Endpoint:** `POST https://seller.g2.com/api/v1/webhooks`

```
Body:
{
  "url": "https://your-n8n-instance.com/webhook/g2-reviews",
  "events": ["review.created", "review.updated"],
  "secret": "{WEBHOOK_SECRET}"
}
```

The webhook payload includes the full review object. Verify the webhook signature using HMAC-SHA256 with your secret.

## Capterra Review API (Gartner Digital Markets)

### Fetch reviews

**Endpoint:** `GET https://api.gartnerdigitalmarkets.com/v1/products/{product_id}/reviews`

```
Headers:
  Authorization: Bearer {CAPTERRA_API_TOKEN}

Query parameters:
  date_from: "2026-03-01"
  date_to: "2026-03-31"
  sort_by: "date_desc"
  limit: 50
```

### Respond to reviews

**Endpoint:** `POST https://api.gartnerdigitalmarkets.com/v1/reviews/{review_id}/response`

```
Body:
{
  "response_text": "Your response here. Same guidelines as G2."
}
```

## Product Hunt

### Fetch comments (reviews equivalent)

```graphql
{
  post(slug: "your-product") {
    comments(first: 20) {
      edges {
        node {
          id
          body
          createdAt
          user { name headline }
          replies { edges { node { body } } }
        }
      }
    }
  }
}
```

### Reply to a comment

```graphql
mutation {
  createComment(input: {
    postId: "post-id",
    parentCommentId: "comment-id",
    body: "Your reply here."
  }) {
    id
  }
}
```

## TrustRadius

### Fetch reviews

**Endpoint:** `GET https://api.trustradius.com/v1/products/{product_id}/reviews`

```
Headers:
  Authorization: Bearer {TR_API_TOKEN}

Query parameters:
  created_after: "2026-03-01"
  limit: 25
```

### Respond to reviews

**Endpoint:** `POST https://api.trustradius.com/v1/reviews/{review_id}/vendor-response`

```
Body:
{
  "response": "Your response text."
}
```

## Review Sentiment Classification

When processing reviews, classify each into an action bucket:

| Rating | Sentiment | Action |
|--------|-----------|--------|
| 4.5-5.0 | Promoter | Thank, ask if they would be a case study candidate. Log in CRM. |
| 3.5-4.4 | Satisfied | Thank, address any specific feedback points. |
| 2.5-3.4 | Mixed | Acknowledge positives, address concerns with specifics. Flag for follow-up. |
| 1.0-2.4 | Detractor | Acknowledge, apologize for specific issues, offer direct support contact. Alert CS team. |

## Error Handling

- **404 Review Not Found**: Review may have been removed by the platform or reviewer. Log and skip.
- **403 Response Not Allowed**: Some platforms restrict responses until profile is verified. Complete verification first.
- **429 Rate Limited**: Review APIs typically allow 30-60 requests/minute. Queue responses and batch.
- **Duplicate Response**: Most platforms allow only one vendor response per review. Check for existing response before posting.
