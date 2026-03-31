---
name: attio-custom-attributes
description: Create and manage custom attributes on Attio objects for structured data like BANT scores
tool: Attio
difficulty: Config
---

# Create Custom Attributes in Attio

Add custom fields to People, Companies, and Deal records for storing structured qualification data, scores, and metadata.

## Prerequisites

- Attio workspace with admin access
- Attio API key or MCP server connected (see `attio-mcp-setup`)

## Steps

### 1. Create a custom attribute via API

**Endpoint:** `POST https://api.attio.com/v2/objects/{object_slug}/attributes`

**Headers:**
```
Authorization: Bearer {ATTIO_API_KEY}
Content-Type: application/json
```

**Example — create a numeric score field on Deals:**
```json
{
  "data": {
    "title": "BANT Budget Score",
    "api_slug": "bant_budget_score",
    "type": "number",
    "is_required": false
  }
}
```

**Supported types:** `text`, `number`, `checkbox`, `date`, `select`, `multi_select`, `currency`, `rating`, `email`, `phone`, `url`, `person_reference`, `company_reference`.

### 2. Create select-type attributes for categorical data

For fields with predefined options (e.g., qualification verdict):

```json
{
  "data": {
    "title": "BANT Verdict",
    "api_slug": "bant_verdict",
    "type": "select",
    "config": {
      "options": [
        {"title": "Qualified", "color": "green"},
        {"title": "Needs Work", "color": "yellow"},
        {"title": "Disqualified", "color": "red"}
      ]
    }
  }
}
```

### 3. Write values to custom attributes

**Endpoint:** `PATCH https://api.attio.com/v2/objects/deals/records/{record_id}`

```json
{
  "data": {
    "values": {
      "bant_budget_score": [{"value": 75}],
      "bant_verdict": [{"option": "Qualified"}]
    }
  }
}
```

### 4. Query records by custom attribute

**Filter deals by BANT score range:**
```json
POST https://api.attio.com/v2/objects/deals/records/query
{
  "filter": {
    "bant_composite_score": {
      "gte": 70
    }
  },
  "sorts": [
    {"attribute": "bant_composite_score", "direction": "desc"}
  ]
}
```

### 5. Batch update attributes

For bulk BANT score updates (e.g., after re-scoring), iterate over records:

```
for each deal in deals:
  PATCH /v2/objects/deals/records/{deal.id}
  body: { data: { values: { bant_composite_score: [{ value: new_score }] } } }
```

Rate limit: 100 requests/second on Attio API.

## Via Attio MCP Server

```
attio.create_attribute({
  object: "deals",
  title: "BANT Budget Score",
  api_slug: "bant_budget_score",
  type: "number"
})

attio.update_record({
  object: "deals",
  record_id: "...",
  values: { bant_budget_score: 75 }
})
```

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Attio | REST API / MCP | Native custom fields |
| HubSpot | Properties API | Custom properties on any object |
| Salesforce | Metadata API | Custom fields via Tooling API |
| Pipedrive | Custom Fields API | Simple field CRUD |
| Clarify | Schema API | Flexible object model |

## Error Handling

- `409 CONFLICT`: Attribute with that slug already exists. Use `GET /v2/objects/{object}/attributes` to check first.
- `422 UNPROCESSABLE_ENTITY`: Invalid type or missing required config. Verify the type string matches supported types.
- `403 FORBIDDEN`: API key lacks admin permissions. Custom attribute creation requires workspace admin role.
