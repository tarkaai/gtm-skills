---
name: attio-champion-tracking
description: Create champion-specific custom attributes, lists, and automations in Attio for tracking champion status across deals
tool: Attio
difficulty: Config
---

# Attio Champion Tracking

Set up Attio CRM to track champion identification, engagement, and health across all active deals. This creates the data layer that champion drills read from and write to.

## Prerequisites

- Attio workspace with admin access
- Attio API key or MCP server connected (see `attio-mcp-setup`)
- Deals pipeline configured (see `attio-pipeline-config`)

## Steps

### 1. Create Champion Custom Attributes on People

Using the `attio-custom-attributes` fundamental, create these attributes on the People object:

```
POST https://api.attio.com/v2/objects/people/attributes

1. Champion Status (select)
   api_slug: champion_status
   options: ["Candidate", "Recruited", "Active", "Disengaged", "Lost"]
   colors: ["blue", "yellow", "green", "orange", "red"]

2. Champion Score (number)
   api_slug: champion_score
   description: "0-100 score from champion signal analysis"

3. Champion Signals (text)
   api_slug: champion_signals
   description: "JSON array of detected champion signals"

4. Champion Recruited Date (date)
   api_slug: champion_recruited_date

5. Champion Last Engaged (date)
   api_slug: champion_last_engaged

6. Champion Role in Deal (select)
   api_slug: champion_deal_role
   options: ["Technical Champion", "Business Champion", "Executive Sponsor", "Internal Coach"]
   colors: ["blue", "green", "purple", "yellow"]
```

### 2. Create Champion Attributes on Deals

Using the same fundamental, create on the Deals object:

```
1. Champion Count (number)
   api_slug: champion_count
   description: "Number of active champions in this deal"

2. Champion Health (select)
   api_slug: champion_health
   options: ["Strong", "Healthy", "At Risk", "No Champion"]
   colors: ["green", "blue", "orange", "red"]

3. Primary Champion (person_reference)
   api_slug: primary_champion
   description: "Link to the primary champion contact"

4. Champion Win Correlation (checkbox)
   api_slug: champion_win_correlation
   description: "True if deal had active champion at close"
```

### 3. Create Champion Lists

Using the `attio-lists` fundamental, create three dynamic lists:

**Champion Candidates:**
```json
POST https://api.attio.com/v2/lists
{
  "data": {
    "name": "Champion Candidates",
    "object": "people",
    "filter": {
      "champion_status": {"eq": "Candidate"}
    },
    "sorts": [{"attribute": "champion_score", "direction": "desc"}]
  }
}
```

**Active Champions:**
```json
{
  "data": {
    "name": "Active Champions",
    "object": "people",
    "filter": {
      "champion_status": {"eq": "Active"}
    }
  }
}
```

**At-Risk Champions (last engaged >14 days ago):**
```json
{
  "data": {
    "name": "At-Risk Champions",
    "object": "people",
    "filter": {
      "and": [
        {"champion_status": {"eq": "Active"}},
        {"champion_last_engaged": {"lt": "{{14_days_ago}}"}}
      ]
    }
  }
}
```

### 4. Set Up Champion Automations

Using the `attio-automation` fundamental, create two automations:

**Auto-update deal champion health:**
- Trigger: When `champion_last_engaged` on any linked Person changes
- Condition: Person has `champion_status` = "Active"
- Action: If `champion_last_engaged` > 14 days ago, set the linked Deal's `champion_health` to "At Risk"
- Action: If `champion_last_engaged` <= 7 days, set the linked Deal's `champion_health` to "Strong"
- Action: Otherwise, set to "Healthy"

**Auto-count champions per deal:**
- Trigger: When `champion_status` on any Person linked to a Deal changes
- Action: Count People linked to this Deal where `champion_status` = "Active". Write count to Deal's `champion_count`.
- Action: If count = 0, set Deal's `champion_health` to "No Champion"

### 5. Via Attio MCP Server

```
attio.create_attribute({
  object: "people",
  title: "Champion Status",
  api_slug: "champion_status",
  type: "select",
  config: {
    options: [
      {title: "Candidate", color: "blue"},
      {title: "Recruited", color: "yellow"},
      {title: "Active", color: "green"},
      {title: "Disengaged", color: "orange"},
      {title: "Lost", color: "red"}
    ]
  }
})

attio.update_record({
  object: "people",
  record_id: "...",
  values: {
    champion_status: "Active",
    champion_score: 85,
    champion_last_engaged: "2026-03-30"
  }
})
```

## Error Handling

- `409 CONFLICT`: Attribute already exists. Use `GET /v2/objects/{object}/attributes` to check, then skip creation.
- `422 UNPROCESSABLE_ENTITY`: Invalid option in select field. Verify option titles match exactly.
- `403 FORBIDDEN`: Requires workspace admin role for attribute creation.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Attio | REST API / MCP | Native custom attributes and automations |
| HubSpot | Properties API + Workflows | Custom properties + automation workflows |
| Salesforce | Custom Fields + Process Builder | Most mature, most complex setup |
| Pipedrive | Custom Fields API | Simple field CRUD, limited automation |
| Clarify | Schema API + Triggers | Flexible object model |
