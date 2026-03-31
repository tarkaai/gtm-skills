---
name: account-research-brief
description: Assemble account intelligence from CRM and enrichment sources, then generate a structured meeting preparation brief
category: Sales
tools:
  - Attio
  - Clay
  - Anthropic
  - Fireflies
fundamentals:
  - attio-deals
  - attio-notes
  - attio-contacts
  - clay-company-search
  - clay-claygent
  - clay-people-search
  - account-intelligence-assembly
  - call-brief-generation
  - fireflies-transcription
  - anthropic-api-patterns
---

# Account Research Brief

This drill is the core workflow for AI-powered meeting preparation. It takes a scheduled meeting (deal ID + meeting date), researches the account and attendees across multiple data sources, then generates a structured meeting brief with talking points, questions, objection preparation, and a recommended agenda. The output is stored in the CRM and optionally pushed to the caller's inbox before the meeting.

## Input

- Deal ID in Attio (meeting must be associated with a deal)
- Meeting type: `discovery`, `demo`, `negotiation`, `executive_review`, `technical_deep_dive`
- Meeting date and duration
- Attendee names and titles (from calendar invite)
- Your product value proposition (stored in config or provided)

## Steps

### 1. Pull existing deal context from CRM

Query Attio for the deal record and all associated contacts:

```
attio.get_record({ object: "deals", record_id: "{deal_id}" })
```

Extract: company name, domain, deal stage, deal value, prior meeting notes (from Attio notes), any BANT/MEDDIC scores, pain points from prior calls, timeline, competitors mentioned. If prior Fireflies transcripts exist for this deal, use `fireflies-transcription` to pull the most recent transcript and extract key themes.

### 2. Run account intelligence assembly

Execute the `account-intelligence-assembly` fundamental:
- Pull firmographics and tech stack from Clay (`clay-company-search`)
- Research recent news and signals via Claygent (`clay-claygent`)
- Enrich each meeting attendee via Claygent (`clay-people-search`)
- Check for competitive intelligence in Attio

Merge all data into the structured intelligence profile.

### 3. Incorporate prior call context

If this is NOT a first meeting, pull context from prior interactions:
- Query Attio notes tagged `call-prep` or `meeting-notes` for this deal
- Pull the most recent Fireflies transcript summary
- Extract: what was discussed, what was promised, what next steps were agreed, what questions remain open
- Feed this context into the brief generation prompt so the new brief builds on prior conversations, not from scratch

### 4. Generate the meeting brief

Execute the `call-brief-generation` fundamental with:
- The assembled intelligence profile
- Meeting type and duration
- Prior call context (if any)
- Your product value proposition

The brief includes: executive summary, meeting objectives, personalized opening, tailored questions, talk tracks, objection preparation, competitive positioning, stakeholder map, proposed next step, and minute-by-minute agenda.

### 5. Store the brief in CRM

Using `attio-notes`, create a note on the deal record with the full meeting brief. Tag the note as `meeting-brief` with the meeting date in the title:

```
attio.create_note({
  parent: { object: "deals", record_id: "{deal_id}" },
  title: "Meeting Brief — {company_name} — {meeting_date}",
  content: "{brief_markdown}",
  tags: ["meeting-brief"]
})
```

### 6. Track brief generation metrics

Log a PostHog event for each brief generated:

```json
{
  "event": "meeting_brief_generated",
  "properties": {
    "deal_id": "...",
    "meeting_type": "discovery",
    "company_name": "...",
    "meeting_date": "2026-04-02",
    "data_sources_used": ["crm", "clay_firmographics", "clay_news", "clay_contacts", "prior_transcripts"],
    "data_completeness_score": 0.85,
    "brief_sections_generated": 10,
    "generation_time_seconds": 12,
    "is_first_meeting": false
  }
}
```

The `data_completeness_score` is: count of non-empty intelligence sections / total sections. A score below 0.5 means the brief may be too generic.

## Output

- Structured meeting brief stored as Attio note on the deal
- Intelligence profile cached for reuse in follow-up meetings
- PostHog event tracking brief generation quality

## Triggers

- **Manual**: Agent runs this drill when asked to prepare for a meeting
- **Automated (Baseline+)**: n8n workflow triggered 24 hours before any scheduled Cal.com meeting. The workflow queries Cal.com for upcoming meetings, matches them to Attio deals, and runs this drill for each.
- **Re-run**: If new information surfaces (e.g., prospect publishes a blog post, funding announcement), re-run to update the brief before the meeting
