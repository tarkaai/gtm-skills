---
name: third-party-intent-api
description: Ingest third-party buyer intent data from Bombora, G2, and other intent providers via API
tool: Bombora
product: Intent Data
difficulty: Config
---

# Third-Party Intent Data API

Pull buyer intent signals from third-party platforms that track research behavior across the web. These signals tell you which companies are actively researching topics related to your product category, even if they never visit your site.

## Tool Options

| Tool | Signal Type | Coverage | API | Pricing (2026) |
|------|------------|----------|-----|-----------------|
| Bombora Company Surge | Topic research | 5,000+ B2B sites | REST API | From ~$30K/yr |
| G2 Buyer Intent | Category/competitor research | G2.com traffic | REST API | Included in G2 paid plans |
| 6sense | Multi-source intent | Web + content + G2 | REST API | From ~$50K/yr |
| TrustRadius | Review site research | TrustRadius traffic | Webhooks | Included in vendor plans |
| Demandbase | Account-level intent | Multi-source | REST API | From ~$40K/yr |

## Authentication

### Bombora
1. Contract required — contact sales at bombora.com
2. API credentials issued post-contract: client_id + client_secret
3. OAuth2 token endpoint: `POST https://auth.bombora.com/oauth/token`
4. Exchange credentials for bearer token (expires in 3600s)

### G2 Buyer Intent
1. Requires G2 paid vendor profile
2. Go to my.g2.com > Integrations > API
3. Generate API token
4. Base URL: `https://data.g2.com/api/v1/`

### 6sense
1. Enterprise contract required
2. API key provisioned by account team
3. Base URL: `https://api.6sense.com/v3/`

## Core Operations

### Bombora: Get surging accounts for your topics
```
GET https://api.bombora.com/v1/surge?topic_ids=12345,67890&surge_score_min=70&date_range=last_7_days
Authorization: Bearer YOUR_OAUTH_TOKEN

Response:
{
  "accounts": [
    {
      "domain": "acme.com",
      "company_name": "Acme Corp",
      "surge_score": 82,
      "topics": [
        {"topic_id": 12345, "topic_name": "Sales Automation", "score": 85},
        {"topic_id": 67890, "topic_name": "CRM Software", "score": 78}
      ],
      "surge_start_date": "2026-03-21",
      "industry": "Technology",
      "employee_range": "51-200"
    }
  ]
}
```

### G2: Get buyer intent signals
```
GET https://data.g2.com/api/v1/buyer-intent?start_date=2026-03-01&end_date=2026-03-30
Authorization: Token YOUR_API_TOKEN

Response:
{
  "intent_signals": [
    {
      "company_domain": "acme.com",
      "company_name": "Acme Corp",
      "signal_type": "alternatives",
      "category": "CRM Software",
      "activity_level": "high",
      "buying_stage": "considering",
      "timestamp": "2026-03-27T08:15:00Z",
      "unique_visitors": 4,
      "page_views": 12,
      "geo": "San Francisco, CA"
    }
  ]
}
```

G2 signal types: `profile` (viewed your profile), `pricing` (viewed your pricing), `category` (browsing your category), `alternatives` (comparing alternatives), `compare` (direct comparison page), `sponsored` (clicked your sponsored content), `competitive` (viewed competitor profiles).

### 6sense: Get account intent scores
```
GET https://api.6sense.com/v3/accounts?buying_stage=consideration,decision&min_intent_score=60
Authorization: Bearer YOUR_API_KEY

Response:
{
  "accounts": [
    {
      "domain": "acme.com",
      "buying_stage": "consideration",
      "intent_score": 75,
      "keywords": ["sales automation", "outbound tools"],
      "segments": ["mid-market", "saas"],
      "first_intent_date": "2026-03-10",
      "last_intent_date": "2026-03-28"
    }
  ]
}
```

## Webhook Setup (G2 example)

Configure G2 to push intent signals to your n8n instance in real time:
```
POST https://data.g2.com/api/v1/webhooks
Authorization: Token YOUR_API_TOKEN
Content-Type: application/json

{
  "url": "https://your-n8n-instance.com/webhook/g2-intent",
  "events": ["intent.new_signal"],
  "filters": {
    "signal_types": ["alternatives", "compare", "pricing"],
    "activity_level": ["high"]
  }
}
```

## Error Handling

- **Stale data**: Bombora updates surge scores weekly (Monday). G2 updates nightly. Do not query more frequently than the refresh cycle.
- **Low surge scores**: Scores below 60 are noise. Only act on scores 70+ for outreach triggers.
- **Topic selection**: Bombora has 12,000+ topics. Selecting too many dilutes signal quality. Start with 5-10 topics tightly mapped to your product category and buyer pain points.
- **Rate limits**: Bombora 100 req/hour, G2 1000 req/day. Cache results locally and query incrementally.
- **No data for small companies**: Third-party intent works best for mid-market and enterprise. Companies under 50 employees often lack sufficient web footprint to generate intent signals.
