---
name: cloud-dialer-call
description: Initiate, log, and manage outbound sales calls via cloud dialer APIs
tool: Orum
difficulty: Config
---

# Cloud Dialer Call

Place outbound sales calls using a cloud dialer with automatic CRM logging, call recording, and voicemail drop. This fundamental covers the API operations for initiating a call, logging the outcome, and retrieving call recordings.

## Tool Options

| Tool | API Docs | Best For |
|------|----------|----------|
| Orum | https://www.orum.com/api | AI parallel dialing, highest connect rates |
| PhoneBurner | https://www.phoneburner.com/developer | Power dialing with voicemail drop |
| JustCall | https://developer.justcall.io | SMB teams, native CRM integrations |
| Aircall | https://developer.aircall.io/api-references | Teams with shared numbers, coaching features |
| Kixie | https://developer.kixie.com | Instant connect, local presence dialing |

## Authentication

All tools use API key or OAuth2 bearer tokens.

**Orum:**
```
Authorization: Bearer {ORUM_API_KEY}
Base URL: https://api.orum.com/v1
```

**JustCall:**
```
Authorization: Bearer {JUSTCALL_API_KEY}
Base URL: https://api.justcall.io/v1
```

**Aircall:**
```
Authorization: Bearer {AIRCALL_API_TOKEN}
Base URL: https://api.aircall.io/v1
```

## Operations

### 1. Initiate an outbound call

**Aircall:**
```
POST https://api.aircall.io/v1/calls
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "number_id": {AIRCALL_NUMBER_ID},
  "to": "+14155551234",
  "metadata": {
    "prospect_id": "abc123",
    "campaign": "outbound-email-li-calls",
    "signal_type": "funding_round"
  }
}
```

**JustCall:**
```
POST https://api.justcall.io/v1/calls/outbound
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "from": "+14155559876",
  "to": "+14155551234",
  "contact_name": "Jane Smith",
  "custom_fields": {
    "campaign": "outbound-email-li-calls",
    "prospect_tier": "1"
  }
}
```

### 2. Log call outcome

After the call ends, update the disposition:

**Aircall:**
```
PUT https://api.aircall.io/v1/calls/{CALL_ID}
{
  "tags": ["meeting_set"],
  "comment": "Discussed pipeline challenges. Booked 30-min demo for Thursday."
}
```

**JustCall:**
```
PUT https://api.justcall.io/v1/calls/{CALL_ID}/disposition
{
  "disposition": "meeting_booked",
  "notes": "Interested in demo. Confirmed Thursday 2pm."
}
```

### 3. Drop a pre-recorded voicemail

When a call goes to voicemail, drop a pre-recorded message instead of speaking live:

**PhoneBurner:**
```
POST https://api.phoneburner.com/rest/1/voicemail/drop
{
  "call_id": "{CALL_ID}",
  "voicemail_id": "{PRE_RECORDED_VM_ID}"
}
```

Pre-record 2-3 voicemail variants. Keep each under 20 seconds. Reference the email you sent: "Hi [name], this is [founder] from [company]. I sent you a note earlier this week about [topic]. Would love 15 minutes to discuss. My number is [number]."

### 4. Retrieve call recordings

```
GET https://api.aircall.io/v1/calls/{CALL_ID}
```
Response includes `recording` URL. Download or pass to Fireflies/Gong for transcription and analysis.

### 5. Get call analytics

**Aircall:**
```
GET https://api.aircall.io/v1/calls?direction=outbound&from={START_DATE}&to={END_DATE}
```
Returns all outbound calls with duration, outcome tags, and recording URLs. Aggregate for connect rate and meeting conversion.

## Error Handling

- **Number not reachable**: Log as `call_no_answer` with attempt count. Retry max 3 times across 3 different days/times.
- **Wrong number**: Remove from call list and flag in CRM. Do not retry.
- **Rate limits**: Most dialers allow 1 concurrent call per user/line. Queue calls in n8n and process sequentially.
- **Local presence**: Use local area code matching when available (Kixie, Aircall) to increase connect rates by 2-3x.

## CRM Sync

After every call, push the outcome to your CRM:
```
POST https://api.attio.com/v2/objects/people/records/{PERSON_ID}/notes
{
  "data": {
    "title": "Outbound call - {DISPOSITION}",
    "content": "{CALL_NOTES}",
    "created_at": "{TIMESTAMP}"
  }
}
```

Tag the contact with `last_call_date`, `call_disposition`, and `call_attempt_count`.
