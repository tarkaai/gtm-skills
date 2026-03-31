---
name: attio-lead-scoring
description: Configure lead scoring fields, computed attributes, and score-based automations in Attio
tool: Attio
product: Attio
difficulty: Config
---

# Configure Lead Scoring in Attio

Set up the CRM data model for lead scoring: fit score, intent score, composite score, and tier fields on People and Deal records. Enable score-based automations and queries.

## Prerequisites

- Attio workspace with admin access
- Attio API key or MCP server connected (see `attio-mcp-setup`)
- Scoring criteria defined (fit dimensions + intent signals + point values)

## Steps

### 1. Create scoring attributes on People

**Endpoint:** `POST https://api.attio.com/v2/objects/people/attributes`

```json
// Fit score (firmographic match)
{
  "data": {
    "title": "Fit Score",
    "api_slug": "fit_score",
    "type": "number",
    "is_required": false
  }
}

// Intent score (behavioral signals)
{
  "data": {
    "title": "Intent Score",
    "api_slug": "intent_score",
    "type": "number",
    "is_required": false
  }
}

// Composite lead score
{
  "data": {
    "title": "Lead Score",
    "api_slug": "lead_score",
    "type": "number",
    "is_required": false
  }
}

// Score tier
{
  "data": {
    "title": "Lead Tier",
    "api_slug": "lead_tier",
    "type": "select",
    "config": {
      "options": [
        {"title": "Hot", "color": "red"},
        {"title": "Warm", "color": "yellow"},
        {"title": "Cold", "color": "blue"}
      ]
    }
  }
}

// Last scored timestamp
{
  "data": {
    "title": "Last Scored",
    "api_slug": "last_scored",
    "type": "date",
    "is_required": false
  }
}
```

### 2. Write scores to a person record

**Endpoint:** `PATCH https://api.attio.com/v2/objects/people/records/{record_id}`

```json
{
  "data": {
    "values": {
      "fit_score": [{"value": 72}],
      "intent_score": [{"value": 85}],
      "lead_score": [{"value": 79}],
      "lead_tier": [{"option": "Warm"}],
      "last_scored": [{"value": "2026-03-30"}]
    }
  }
}
```

### 3. Query leads by score tier

**Endpoint:** `POST https://api.attio.com/v2/objects/people/records/query`

```json
{
  "filter": {
    "lead_tier": {"is": "Hot"}
  },
  "sorts": [
    {"attribute": "lead_score", "direction": "desc"}
  ]
}
```

To get leads above a score threshold:

```json
{
  "filter": {
    "lead_score": {"gte": 80}
  },
  "sorts": [
    {"attribute": "lead_score", "direction": "desc"}
  ]
}
```

### 4. Batch update scores

When re-scoring all leads (e.g., after model weight changes):

```
for each person in people_records:
  PATCH /v2/objects/people/records/{person.id}
  body: {
    data: {
      values: {
        fit_score: [{ value: new_fit }],
        intent_score: [{ value: new_intent }],
        lead_score: [{ value: new_composite }],
        lead_tier: [{ option: tier_from_score(new_composite) }],
        last_scored: [{ value: today }]
      }
    }
  }
```

Rate limit: 100 requests/second on Attio API. For >1000 leads, batch in groups of 50 with 500ms delays.

### 5. Score decay automation

To implement score decay (reduce intent score for inactive leads), query leads where `last_scored` is older than 14 days and `intent_score` > 0:

```json
{
  "filter": {
    "last_scored": {"before": "2026-03-16"},
    "intent_score": {"gt": 0}
  }
}
```

For each result, update: `intent_score = current_intent_score * 0.5`, recalculate `lead_score` and `lead_tier`.

## Via Attio MCP Server

```
attio.create_attribute({
  object: "people",
  title: "Lead Score",
  api_slug: "lead_score",
  type: "number"
})

attio.update_record({
  object: "people",
  record_id: "...",
  values: { lead_score: 85, lead_tier: "Hot", last_scored: "2026-03-30" }
})

attio.query_records({
  object: "people",
  filter: { lead_tier: { is: "Hot" } },
  sorts: [{ attribute: "lead_score", direction: "desc" }]
})
```

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Attio | REST API / MCP | Native custom attributes + query API |
| HubSpot | Lead Scoring tool | Built-in scoring with Properties API |
| Salesforce | Einstein Lead Scoring | AI-based or rule-based via Process Builder |
| Pipedrive | LeadBooster + Custom Fields | Custom fields with Automations API |
| Clarify | Schema API + computed fields | Flexible object model for custom scoring |

## Error Handling

- `409 CONFLICT`: Attribute already exists. Use `GET /v2/objects/people/attributes` to check first, then update the existing attribute.
- `422 UNPROCESSABLE_ENTITY`: Invalid type or missing config. Verify the type string matches supported types.
- `404 NOT_FOUND`: Record ID does not exist. Re-query the person by email before updating.
- `429 TOO_MANY_REQUESTS`: Rate limited. Back off and retry with exponential delay.
