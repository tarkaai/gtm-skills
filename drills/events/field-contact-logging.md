---
name: field-contact-logging
description: Log in-person conversations from field visits as structured CRM records with qualification data
category: Field
tools:
  - Attio
  - PostHog
  - n8n
fundamentals:
  - attio-contacts
  - attio-notes
  - attio-deals
  - posthog-custom-events
  - n8n-triggers
---

# Field Contact Logging

This drill provides a structured workflow for logging every in-person conversation from a field prospecting session. The founder captures raw notes (voice memo, quick text, or post-visit debrief), and the agent transforms them into structured CRM records with qualification data and next steps.

## Input

- Raw conversation notes from the founder (voice transcript, text notes, or dictation)
- Venue and date of the field visit
- Business card photos or LinkedIn profile URLs collected during visits

## Steps

### 1. Capture raw input

After each field visit session, the founder provides raw notes. Acceptable formats:

- **Voice memo transcription**: Use a transcription service (Whisper API, Deepgram, or phone's built-in transcription) to convert voice memos to text. The founder records a quick debrief in the car after each stop.
- **Quick text notes**: Bullet points typed during or immediately after conversations.
- **Business card photos**: Extract name, title, company, email, phone using OCR or manual entry.

The agent should prompt the founder with: "For each person you spoke with, tell me: their name, title, company, what you talked about, whether they seemed interested, and what you agreed to do next."

### 2. Parse conversations into structured records

For each person the founder spoke with, extract:

- **Contact info**: name, title, company, email (if exchanged), phone, LinkedIn URL
- **Venue**: where the conversation happened
- **Duration**: approximate conversation length
- **Pain identified**: yes/no + description
- **Interest level**: hot (wants a meeting), warm (interested but no commitment), cold (polite but not interested), not-ICP (wrong fit)
- **Current solution**: what they use today for the problem you solve
- **Next step**: specific action (send email, book demo, connect on LinkedIn, no follow-up)
- **Follow-up date**: when to follow up

### 3. Create or update CRM records

For each contact, use the `attio-contacts` fundamental to:

1. Search Attio for existing records by email or name + company
2. If found, update the record with new information
3. If not found, create a new Person record with all captured fields
4. Link to the Company record (create if needed)
5. Tag with `source: field-visit` and `venue: {venue name}`

### 4. Log the structured field note

Use the `attio-notes` fundamental to create a note on each Person record following the structured template:

```
## Visit Details
- Location: {venue name and address}
- Date: {YYYY-MM-DD}
- Visit type: drop-in

## Conversation
- Person: {name}
- Title: {title}
- Company: {company}
- Duration: {minutes}

## Qualification
- Pain identified: {yes/no — description}
- Budget authority: {yes/no/unknown}
- Timeline: {immediate/this quarter/this year/exploring}
- Current solution: {description}

## Outcome
- Result: {meeting booked | follow-up requested | not interested | not ICP}
- Next step: {specific action}
- Follow-up date: {YYYY-MM-DD}
```

### 5. Create deals for qualified contacts

For contacts marked as "hot" (wants a meeting) or "warm" with a clear next step, use the `attio-deals` fundamental to create a Deal record:

- Stage: "Meeting Requested" or "Follow-Up"
- Source: "Field Visit"
- Expected close date: based on stated timeline
- Notes: link to the field visit note

### 6. Track field visit events in PostHog

Use the `posthog-custom-events` fundamental to fire events for analytics:

- `field_visit_completed` — properties: venue, date, num_conversations
- `field_conversation_logged` — properties: venue, interest_level, pain_identified, outcome
- `field_meeting_booked` — properties: venue, source_conversation_date
- `field_followup_created` — properties: venue, followup_type, followup_date

### 7. Create follow-up tasks

Use `n8n-triggers` to schedule automated follow-up reminders:

- For "send email" next steps: trigger an n8n workflow that drafts a follow-up email referencing the conversation and sends it via the founder's email (not cold email tooling — this is warm follow-up)
- For "book demo" next steps: send the Cal.com booking link with a personal note
- For "connect on LinkedIn" next steps: remind the founder to send a connection request with a personalized note

## Output

- Structured CRM records for every person contacted in the field
- Qualification data attached to each contact
- Deals created for hot/warm leads
- PostHog events for funnel analytics
- Follow-up tasks scheduled and tracked

## Triggers

Run this drill after every field visit session. Ideally the founder does a voice debrief within 1 hour of finishing visits while details are fresh.
