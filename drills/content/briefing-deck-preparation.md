---
name: briefing-deck-preparation
description: Prepare analyst-specific briefing documents and meeting agendas tailored to each analyst's coverage area and evaluation framework
category: Content
tools:
  - Anthropic
  - Attio
  - Cal.com
fundamentals:
  - briefing-document-creation
  - attio-contacts
  - calcom-booking-links
  - calcom-event-types
---

# Briefing Deck Preparation

This drill prepares everything needed for an analyst or consultant briefing: a tailored one-pager, a meeting agenda, and a Cal.com booking link. Each briefing is customized to the specific analyst's coverage area, terminology, and known evaluation criteria.

## Input

- Analyst contact record from Attio (from the `analyst-target-research` drill)
- Company positioning, metrics, and competitive landscape
- Briefing goal (awareness, inclusion in research, referrals, positioning feedback)

## Steps

### 1. Pull analyst context from Attio

Query the analyst's Attio record using the `attio-contacts` fundamental. Retrieve: name, firm, tier, coverage area, recent publications, and any notes about their evaluation framework or known preferences. If notes are sparse, use Claude API to research the analyst's recent work before proceeding.

### 2. Generate the briefing document

Run the `briefing-document-creation` fundamental with the analyst-specific context. The output is a structured one-pager covering:
- Market context (using the analyst's terminology)
- Company overview (facts, not hype)
- Product approach and differentiation
- Traction metrics (only share what you are comfortable disclosing)
- Competitive positioning (fair and objective)
- 3 discussion topics tailored to the analyst's interests

**Human action required:** Review every briefing document before sending. Verify metrics are accurate, competitive positioning is defensible, and discussion topics align with what you want from this specific analyst.

### 3. Create the meeting agenda

Generate a 30-minute meeting agenda:

```
Analyst Briefing Agenda — {Analyst Name}
Duration: 30 minutes

0:00-0:02  Introductions and context
0:02-0:10  Company overview and market positioning
0:10-0:18  Product demonstration or deep-dive on approach
0:18-0:25  Discussion: {Topic 1}, {Topic 2}
0:25-0:28  Analyst's perspective and feedback
0:28-0:30  Next steps and follow-up
```

Store the agenda as a note on the analyst's Attio record.

### 4. Configure booking for briefings

Use the `calcom-event-types` fundamental to create an "Analyst Briefing" event type (30 minutes, with 15-minute buffer before and after for prep/notes). Use the `calcom-booking-links` fundamental to generate a booking link.

Include in the booking confirmation email: the briefing document (attached or linked) and the agenda, so the analyst can prepare.

### 5. Prepare the briefing request outreach

Draft a briefing request email or LinkedIn message for each analyst. The request should:
- Reference something specific from their recent work (proves you did your homework)
- Explain in one sentence what your company does, using their terminology
- State what you are asking for: a 30-minute briefing to share your approach and get their perspective
- Include the Cal.com booking link
- Attach or link the briefing document

Keep the request under 150 words. Analysts receive dozens of briefing requests. Short and specific wins.

### 6. Log preparation status

Update each analyst's Attio record:
- Briefing Status: "Prepared" (document and outreach ready)
- Briefing Document: link or note with the document content
- Outreach Draft: the briefing request message

## Output

- One tailored briefing document per analyst (stored in Attio)
- Meeting agenda per analyst
- Cal.com booking link for analyst briefings
- Outreach draft per analyst, ready to send

## Triggers

- Run once per analyst before initial outreach
- Re-run before any follow-up briefing (update metrics and competitive landscape)
