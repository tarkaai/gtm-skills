---
name: discovery-question-bank
description: Generate and store role-specific discovery question sets for each stakeholder in a deal
category: Discovery
tools:
  - Anthropic
  - Attio
  - Fireflies
fundamentals:
  - discovery-question-generation
  - attio-contacts
  - attio-deals
  - attio-notes
  - fireflies-transcription
---

# Discovery Question Bank

This drill generates tailored discovery questions for each stakeholder in a deal based on their role, the product being sold, and any prior intelligence. The output is a per-stakeholder question set stored in the CRM, ready for call prep.

## Input

- Completed stakeholder map (from `stakeholder-map-assembly` drill)
- Deal record in Attio with linked stakeholders and role classifications
- Product value proposition
- Optional: prior call transcripts, known pain points, competitor mentions

## Steps

### 1. Pull Stakeholder Map from CRM

Query Attio for all stakeholders on the deal:

```
attio.list_records({
  object: "people",
  filter: { linked_deal_id: "{deal_id}" },
  select: ["name", "title", "stakeholder_role", "stakeholder_concerns", "stakeholder_priorities"]
})
```

### 2. Gather Prior Intelligence

For each stakeholder, check if there is existing context:
- Prior call notes from Fireflies (via `fireflies-transcription` — search by participant name)
- Pain points logged in Attio from previous interactions
- Competitor mentions or objections raised
- Information shared by other stakeholders about this person's priorities

This context makes the generated questions dramatically more specific and useful.

### 3. Generate Questions per Stakeholder

Run the `discovery-question-generation` fundamental for each stakeholder:
- Pass the stakeholder's role, title, company, industry
- Include prior intelligence as context
- Receive 8-12 role-specific questions with rationale, good signals, and risk signals

### 4. Prioritize Questions

For each stakeholder's question set, rank by priority:
1. **Must-ask** (3-4 questions): Critical unknowns that determine deal viability. If you only get 15 minutes with this person, ask these.
2. **Should-ask** (3-4 questions): Important for building a complete picture but not blocking.
3. **Nice-to-ask** (2-4 questions): Deepens understanding if time permits.

Use this heuristic:
- Questions about decision criteria and blockers → Must-ask
- Questions about priorities and process → Should-ask
- Questions about context and future plans → Nice-to-ask

### 5. Store in CRM

For each stakeholder, create an Attio note using `attio-notes`:

```
Title: "Discovery Questions — {name} ({role})"
Tag: "discovery-prep"

MUST-ASK:
1. {question} — Signal: {good_signal} | Risk: {risk_signal}
2. ...

SHOULD-ASK:
3. {question} — Signal: {good_signal} | Risk: {risk_signal}
...

NICE-TO-ASK:
7. {question} — Signal: {good_signal} | Risk: {risk_signal}
...
```

### 6. Post-Call: Update and Iterate

After each discovery call:
1. Mark which questions were asked and which remain
2. Log the answers and whether they matched good_signal or risk_signal
3. If new information surfaces, regenerate questions for remaining stakeholders with the updated context
4. Questions that consistently produce useful answers across deals should be promoted to the permanent question library

## Output

- Per-stakeholder discovery question sets stored as Attio notes
- Questions prioritized into must-ask, should-ask, nice-to-ask
- Each question includes rationale and signal interpretation
- Questions evolve as new intelligence is gathered

## Triggers

Run this drill:
- After `stakeholder-map-assembly` completes for a deal
- Before each scheduled discovery call (to update questions with latest intelligence)
- When a new stakeholder is added to the deal
