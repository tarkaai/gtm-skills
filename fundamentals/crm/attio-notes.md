---
name: attio-notes
description: Create and query structured notes on Attio records for logging interactions
tool: Attio
difficulty: Setup
---

# Attio Notes

Create, read, and query notes on Attio Person, Company, and Deal records. Used for logging in-person conversations, meeting summaries, and field visit observations.

## Prerequisites

- Attio workspace with API access
- Attio MCP server connected (preferred) or API key: `ATTIO_API_KEY`

## Create a Note via API

**Endpoint:** `POST https://api.attio.com/v2/notes`

**Headers:**
```
Authorization: Bearer {ATTIO_API_KEY}
Content-Type: application/json
```

**Request body:**
```json
{
  "data": {
    "parent_object": "people",
    "parent_record_id": "record_id_here",
    "title": "Field Visit — WeWork SoMa — 2024-03-15",
    "content_plaintext": "Met CTO of [Company]. Pain: current tool lacks integrations. Budget cycle starts Q3. Next step: send case study and book demo."
  }
}
```

## Structured Field Visit Note Template

When logging field visits, use a consistent structure so notes are queryable:

```
## Visit Details
- Location: {venue name and address}
- Date: {YYYY-MM-DD}
- Time: {HH:MM}
- Visit type: {drop-in | scheduled | event}

## Conversation
- Person: {name}
- Title: {job title}
- Company: {company name}
- Duration: {minutes}

## Qualification
- Pain identified: {yes/no — description}
- Budget authority: {yes/no/unknown}
- Timeline: {immediate/this quarter/this year/exploring}
- Current solution: {competitor or manual process}

## Outcome
- Result: {meeting booked | follow-up requested | not interested | not ICP}
- Next step: {specific action}
- Follow-up date: {YYYY-MM-DD}
```

## Query Notes via API

**List notes for a record:**
`GET https://api.attio.com/v2/notes?parent_object=people&parent_record_id={id}`

**Search notes (via MCP):**
Use the Attio MCP `search_notes` operation to find notes containing specific keywords. Useful for finding all field visit notes mentioning a competitor or pain point.

## Via Attio MCP Server

If using the Attio MCP server (recommended for agent workflows):

```
attio.create_note({
  parent_object: "people",
  parent_record_id: "...",
  title: "Field Visit — ...",
  content: "..."
})

attio.list_notes({
  parent_object: "people",
  parent_record_id: "..."
})
```

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Attio | API / MCP | Native notes on any record |
| HubSpot | Engagement API | Notes as "engagements" |
| Salesforce | ContentNote API | Notes attached to records |
| Pipedrive | Notes API | Simple note CRUD |
| Clarify | Activity API | Interaction logging |

## Error Handling

- `404 NOT_FOUND`: The parent record ID does not exist. Search for the contact first.
- `422 UNPROCESSABLE_ENTITY`: Missing required fields. Ensure `parent_object` and `parent_record_id` are set.
- `429 RATE_LIMITED`: Back off and retry. Attio allows 100 requests/second.
