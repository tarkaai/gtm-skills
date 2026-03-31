---
name: pain-discovery-call-prep
description: Research the prospect, generate a tailored pain-question guide, and set up recording before a discovery call
category: Sales
tools:
  - Attio
  - Clay
  - Fireflies
  - Anthropic
  - Cal.com
fundamentals:
  - attio-deals
  - attio-notes
  - clay-company-search
  - clay-claygent
  - fireflies-transcription
  - calcom-booking-links
  - anthropic-api-patterns
---

# Pain Discovery Call Prep

This drill prepares a founder or AE for a structured pain-discovery call. It researches the prospect's company, identifies likely pain areas, generates a tailored question guide, and ensures recording is active. The output is a call prep document stored as an Attio note on the deal.

## Input

- Deal record in Attio with at least: company name, contact name, contact title, industry
- Cal.com booking link (meeting already scheduled)
- Fireflies configured to auto-join meetings

## Steps

### 1. Pull deal context from CRM

Query Attio for the deal record:
```
attio.get_record({ object: "deals", record_id: "{deal_id}" })
```

Extract: company name, contact name, contact title, industry, company size, any existing notes from prior touchpoints, and the deal stage.

### 2. Enrich the prospect company

Use the `clay-company-search` fundamental to pull firmographic data: headcount, revenue estimate, funding stage, tech stack, recent news, and job openings. Use `clay-claygent` to find:
- Recent press releases or blog posts (pain signals in their own words)
- Job postings that reveal operational gaps (e.g., hiring for a role your product replaces)
- Competitor mentions or review site complaints
- Industry-specific regulatory or market pressures

Store the enrichment summary in the deal record.

### 3. Identify likely pain areas

Send the enrichment data to Claude via `anthropic-api-patterns` to generate hypothesized pain areas:

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1500,
  "messages": [{
    "role": "user",
    "content": "Based on this prospect profile, identify the 5 most likely pain points they experience that our product could solve.\n\nProspect: {company_name}, {industry}, {headcount} employees, {funding_stage}\nContact: {contact_name}, {contact_title}\nRecent signals: {enrichment_signals}\nOur product solves: {product_value_prop}\n\nFor each pain, provide:\n1. The pain (one sentence)\n2. Why this company likely has it (based on their profile)\n3. A discovery question to surface it (open-ended, not leading)\n4. A follow-up question to quantify it (asks for numbers, time, money)\n5. A trigger question to establish urgency (why now?)"
  }]
}
```

### 4. Build the call prep document

Structure the output into a call prep document:

```markdown
## Discovery Call Prep — {company_name}
### Date: {call_date}
### Contact: {contact_name}, {contact_title}

### Company Context
- {headcount} employees, {industry}, {funding_stage}
- Key signals: {2-3 bullet points from enrichment}

### Hypothesized Pains
1. **{Pain area}**
   - Why likely: {reasoning}
   - Discovery Q: "{open-ended question}"
   - Quantify Q: "{follow-up asking for numbers}"
   - Urgency Q: "{why-now question}"

2. **{Pain area}** ...

### Call Structure (45 minutes)
- 0-5 min: Rapport + agenda setting
- 5-10 min: Ask about their current situation and priorities
- 10-30 min: Pain discovery (use questions above, follow the energy)
- 30-40 min: Quantification deep-dive on top 2-3 pains
- 40-45 min: Next steps + confirm stakeholders

### Rules for the Caller
- Listen more than talk (target 70/30 prospect-to-caller ratio)
- Never pitch during discovery — only ask questions
- When a pain surfaces, go deeper: "Tell me more about that" / "What does that cost you?"
- Capture exact quotes — they power the business case later
- If the prospect mentions a number, confirm it: "So roughly $X per year?"
```

### 5. Store prep in CRM

Using `attio-notes`, create a note on the deal record with the full call prep document. Tag the note as `call-prep` for easy retrieval.

### 6. Verify recording is active

Check that Fireflies is configured to auto-join the scheduled meeting. Query the Fireflies API:
```graphql
query { user { integrations { calendar_connected } } }
```

If the meeting is on Cal.com, verify the calendar sync is active. If Fireflies is not connected, send a Slack alert to the caller: "Fireflies is not configured for tomorrow's call with {company_name}. Recording will not be automatic — start manual recording."

## Output

- Enriched deal record in Attio with company context
- Call prep document stored as an Attio note
- Fireflies recording verified for the meeting
- Caller has a structured question guide before walking into the call

## Triggers

Run this drill 24 hours before every scheduled discovery call. Can be triggered automatically via n8n when a Cal.com booking event fires.
