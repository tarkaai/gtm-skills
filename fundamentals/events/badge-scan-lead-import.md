---
name: badge-scan-lead-import
description: Import badge scan and lead retrieval data from conference platforms into CRM
tool: Attio
difficulty: Config
---

# Badge Scan Lead Import

Import lead data captured via conference badge scanners and lead retrieval apps into your CRM. Most conferences provide lead retrieval through dedicated apps or badge scanner hardware that export CSV/JSON contact data.

## Authentication

- Attio API key: Settings → Developers → API Keys → `Authorization: Bearer {ATTIO_API_KEY}`
- Conference lead retrieval platform credentials (varies by provider)

## Method 1: CSV Export + n8n Import (Universal)

Most conference lead retrieval systems (Bizzabo, Swapcard, Eventbrite Exhibitor, Cvent LeadCapture, Expo Logic) export to CSV. This method works with all of them.

1. **Export leads from the conference platform** as CSV. Standard fields: first_name, last_name, email, company, title, phone, notes, scan_timestamp.

2. **Create an n8n workflow** triggered by file upload (or cron to check a shared folder):

   - Read CSV node → parse each row into a JSON object
   - For each contact, call Attio API to create or update:

   ```
   POST https://api.attio.com/v2/objects/people/records
   Headers:
     Authorization: Bearer {ATTIO_API_KEY}
     Content-Type: application/json

   Body:
   {
     "data": {
       "values": {
         "name": [{ "first_name": "{first_name}", "last_name": "{last_name}" }],
         "email_addresses": [{ "email_address": "{email}" }],
         "phone_numbers": [{ "phone_number": "{phone}" }],
         "job_title": [{ "value": "{title}" }]
       }
     }
   }
   ```

   - Link to company record via matching logic
   - Add to an Attio list tagged with the conference name and date:

   ```
   POST https://api.attio.com/v2/lists/{list_id}/entries
   Headers:
     Authorization: Bearer {ATTIO_API_KEY}
   Body:
   {
     "data": {
       "record_id": "{person_record_id}",
       "entry_values": {
         "conference_name": [{ "value": "{conference}" }],
         "scan_timestamp": [{ "value": "{timestamp}" }],
         "booth_notes": [{ "value": "{notes}" }],
         "interest_level": [{ "value": "{interest_tier}" }]
       }
     }
   }
   ```

## Method 2: Bizzabo Lead Retrieval API

```
GET https://api.bizzabo.com/v1/events/{event_id}/leads
Headers:
  Authorization: Bearer {BIZZABO_TOKEN}
  Content-Type: application/json
```

Response: array of lead objects with `firstName`, `lastName`, `email`, `company`, `title`, `notes`, `scannedAt`, `customFields`.

## Method 3: Swapcard API

```
POST https://developer.swapcard.com/graphql
Headers:
  Authorization: Bearer {SWAPCARD_TOKEN}
Body:
{
  "query": "query { exhibitorLeads(eventId: \"{event_id}\", exhibitorId: \"{exhibitor_id}\") { edges { node { firstName lastName email company jobTitle scannedAt notes qualificationAnswers { question answer } } } } }"
}
```

## Method 4: Manual Badge Scan Logging (Typeform/Tally Fallback)

If the conference does not provide lead retrieval or your sponsorship tier does not include it, create a mobile-friendly Tally or Typeform for booth staff:

- Fields: name, email, company, title, interest level (1-5), key pain points (multi-select), agreed next step (dropdown: demo, trial, follow-up call, just browsing), notes (free text)
- Webhook to n8n → Attio import using Method 1 flow
- This is slower but captures richer qualification data than badge scans alone

## Output Format

Normalize all imported leads to:

| Field | Description |
|-------|-------------|
| `name` | Full name |
| `email` | Work email |
| `company` | Company name |
| `title` | Job title |
| `phone` | Phone number (if captured) |
| `conference_name` | Source conference |
| `conference_date` | Event date |
| `scan_timestamp` | When the badge was scanned |
| `interest_level` | 1-5 qualification tier |
| `booth_notes` | Free-text notes from booth staff |
| `agreed_next_step` | demo / trial / follow-up / nurture |

## Error Handling

- Deduplicate by email before importing — multiple booth staff may scan the same person
- If email field is missing (some badge scans only capture name + company), flag for manual enrichment via Clay
- If the conference platform delays lead export (some release data 24-48 hours post-event), schedule the n8n import workflow to retry daily for 3 days after the event
- Validate email format before CRM import — badge scan data sometimes contains garbled emails from OCR errors
