---
name: attio-health-score-sync
description: Write computed health scores and risk classifications to Attio company records
tool: Attio
product: Attio
difficulty: Config
---

# Sync Health Scores to Attio

Write computed account health scores, risk classifications, and dimension breakdowns to Attio company records so the sales and CS team has real-time visibility into account health directly in the CRM.

## Prerequisites

- Attio workspace with Company records populated
- Attio API key or MCP server connected (see `attio-mcp-setup`)
- Health score model producing numeric scores and risk classifications

## Steps

### 1. Create health score attributes on the Company object

Create the required custom attributes before writing scores:

```
POST https://api.attio.com/v2/objects/companies/attributes
Authorization: Bearer {ATTIO_API_KEY}
Content-Type: application/json

{
  "data": {
    "title": "Health Score",
    "api_slug": "health_score",
    "type": "number",
    "is_required": false
  }
}
```

Create additional attributes for the score dimensions and risk level:

```json
// Risk classification
{
  "data": {
    "title": "Health Risk Level",
    "api_slug": "health_risk_level",
    "type": "select",
    "config": {
      "options": [
        {"title": "Healthy", "color": "green"},
        {"title": "Monitor", "color": "yellow"},
        {"title": "At Risk", "color": "orange"},
        {"title": "Critical", "color": "red"}
      ]
    }
  }
}

// Dimension scores (create one for each dimension)
{"data": {"title": "Usage Score", "api_slug": "health_usage_score", "type": "number"}}
{"data": {"title": "Engagement Score", "api_slug": "health_engagement_score", "type": "number"}}
{"data": {"title": "Support Score", "api_slug": "health_support_score", "type": "number"}}
{"data": {"title": "Adoption Score", "api_slug": "health_adoption_score", "type": "number"}}

// Metadata
{"data": {"title": "Health Score Updated At", "api_slug": "health_score_updated_at", "type": "date"}}
{"data": {"title": "Health Score Trend", "api_slug": "health_score_trend", "type": "select", "config": {"options": [{"title": "Improving", "color": "green"}, {"title": "Stable", "color": "blue"}, {"title": "Declining", "color": "red"}]}}}
```

### 2. Write a health score to a company record

```
PATCH https://api.attio.com/v2/objects/companies/records/{record_id}
Authorization: Bearer {ATTIO_API_KEY}
Content-Type: application/json

{
  "data": {
    "values": {
      "health_score": [{"value": 72}],
      "health_risk_level": [{"option": "Monitor"}],
      "health_usage_score": [{"value": 85}],
      "health_engagement_score": [{"value": 60}],
      "health_support_score": [{"value": 90}],
      "health_adoption_score": [{"value": 55}],
      "health_score_updated_at": [{"value": "2026-03-30"}],
      "health_score_trend": [{"option": "Declining"}]
    }
  }
}
```

### 3. Batch update all company health scores

For daily health score refreshes, iterate over all scored companies:

```
for each company in scored_companies:
  PATCH /v2/objects/companies/records/{company.attio_record_id}
  body: {
    data: {
      values: {
        health_score: [{value: company.score}],
        health_risk_level: [{option: company.risk_level}],
        health_usage_score: [{value: company.usage_score}],
        health_engagement_score: [{value: company.engagement_score}],
        health_support_score: [{value: company.support_score}],
        health_adoption_score: [{value: company.adoption_score}],
        health_score_updated_at: [{value: today}],
        health_score_trend: [{option: company.trend}]
      }
    }
  }
```

Rate limit: Attio API allows 100 requests/second. For 500+ accounts, batch in groups of 50 with 1-second pauses.

### 4. Query companies by health score

Pull at-risk accounts for intervention:

```
POST https://api.attio.com/v2/objects/companies/records/query
{
  "filter": {
    "health_risk_level": {"in": ["At Risk", "Critical"]}
  },
  "sorts": [
    {"attribute": "health_score", "direction": "asc"}
  ]
}
```

Pull companies whose health is declining for proactive outreach:

```json
{
  "filter": {
    "health_score_trend": {"eq": "Declining"},
    "health_risk_level": {"not_in": ["Critical"]}
  }
}
```

### 5. Add a health score change note

When a score changes significantly (>10 points), log a note explaining why:

```
POST https://api.attio.com/v2/notes
{
  "data": {
    "parent_object": "companies",
    "parent_record_id": "{record_id}",
    "title": "Health Score Change: 72 → 58",
    "content": "Usage dimension dropped from 85 to 50 (3-week login decline). Engagement stable. Support ticket volume increased. Risk level changed from Monitor to At Risk."
  }
}
```

## Via Attio MCP

```
attio.create_attribute({
  object: "companies",
  title: "Health Score",
  api_slug: "health_score",
  type: "number"
})

attio.update_record({
  object: "companies",
  record_id: "...",
  values: {
    health_score: 72,
    health_risk_level: "Monitor",
    health_score_trend: "Declining"
  }
})

attio.query_records({
  object: "companies",
  filter: {health_risk_level: {in: ["At Risk", "Critical"]}},
  sort: {health_score: "asc"}
})
```

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Attio | REST API / MCP | Custom attributes on Company object |
| HubSpot | Properties API + Scoring | Custom company properties, built-in scoring |
| Salesforce | Custom Fields + Health Score object | Can use formula fields for auto-calculation |
| Pipedrive | Custom Fields API | Simple numeric fields on Organization |
| Clarify | Schema API | Flexible schema, good for custom objects |
| Vitally | Customer Health API | Purpose-built for customer health scoring |
| Gainsight | Health Score API | Enterprise CS platform with native health scores |

## Error Handling

- `404 NOT FOUND`: Company record does not exist in Attio. Match by domain or name first using `POST /v2/objects/companies/records/query`.
- `409 CONFLICT`: Attribute already exists. Use `GET /v2/objects/companies/attributes` to check before creating.
- `422 UNPROCESSABLE`: Invalid option value for select fields. Ensure the option string exactly matches one of the defined options.
