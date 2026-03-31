---
name: stakeholder-discovery-call
description: Post-call workflow that extracts per-stakeholder insights, updates sentiment, and tracks discovery progress
category: Discovery
tools:
  - Fireflies
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - stakeholder-sentiment-extraction
  - attio-contacts
  - attio-deals
  - attio-notes
  - attio-custom-attributes
  - posthog-custom-events
---

# Stakeholder Discovery Call

This drill handles everything after a multi-stakeholder discovery call ends: transcript retrieval, per-stakeholder sentiment extraction, priority and concern mapping, consensus/conflict detection, CRM updates, and follow-up routing. It turns a group discovery call into structured intelligence about each individual stakeholder's position.

## Input

- Completed discovery call with Fireflies recording
- Deal record in Attio with stakeholder map
- Discovery question set (from `discovery-question-bank` drill)

## Steps

### 1. Retrieve Transcript

Wait for Fireflies to process the transcript (typically 5-15 minutes post-call). Poll the Fireflies API:

```graphql
query {
  transcripts(filter: { date_from: "{today}", title_contains: "{company_name}" }) {
    id
    title
    sentences { speaker_name, text, start_time, end_time }
    action_items
    questions
  }
}
```

Verify the transcript has speaker labels. If not, match speakers manually from the attendee list.

### 2. Extract Per-Stakeholder Sentiment

Run the `stakeholder-sentiment-extraction` fundamental with the full transcript and the stakeholder map:
- Get per-stakeholder: sentiment, support level, priorities, concerns, questions asked, decision criteria, engagement level
- Get cross-stakeholder: consensus areas, conflict areas, unresolved items

### 3. Extract Action Items

Run the `fireflies-action-items` fundamental:
- Pull all action items from the transcript
- Attribute each action item to a specific stakeholder where possible
- Classify action items by type: follow-up info requested, internal review needed, meeting to schedule, document to share

### 4. Compare to Pre-Call Expectations

Pull the discovery questions from `discovery-question-bank` (stored as Attio notes tagged `discovery-prep`):
- Mark which must-ask questions were answered
- For each answered question, log whether the answer matched good_signal or risk_signal
- Flag must-ask questions that were NOT asked — these need follow-up

### 5. Update Stakeholder Records in CRM

For each stakeholder who participated in the call, update Attio:

```
PATCH attio-custom-attributes for each person:
  stakeholder_sentiment → {extracted_sentiment}
  stakeholder_support_level → {extracted_support_level}
  stakeholder_priorities → {extracted_priorities_json}
  stakeholder_concerns → {extracted_concerns_json}
  engagement_status → Engaged
  discovery_status → {In Progress | Complete}
  last_interaction_date → {call_date}
```

Create an Attio note on the deal with the full extraction summary, tagged `stakeholder-discovery-call`.

### 6. Detect Stakeholder Position Changes

If this is not the first call with this stakeholder, compare current extraction to prior:
- Sentiment improved → log as positive signal
- Sentiment degraded → log as risk signal, create follow-up task
- New concern raised → add to active concerns list
- Prior concern resolved → remove from active list, note what resolved it

### 7. Route Follow-Up Actions

Based on the extraction:
- **For Blockers/Skeptics**: Generate a follow-up plan addressing their specific concerns. Queue for next outreach.
- **For Unresolved items**: Create tasks in Attio for each unresolved question with the responsible stakeholder.
- **For missing stakeholders**: If the call revealed new stakeholders not yet in the map, flag for `stakeholder-map-assembly` re-run.
- **For champions**: If a Champion emerged or strengthened, update their status in Attio.

### 8. Log PostHog Events

```
posthog.capture("discovery_call_completed", {
  "deal_id": "{deal_id}",
  "stakeholders_present": count_present,
  "stakeholders_total": count_total,
  "consensus_areas": count_consensus,
  "conflict_areas": count_conflict,
  "unresolved_items": count_unresolved,
  "questions_answered_pct": pct_must_ask_answered,
  "new_concerns_raised": count_new_concerns
})

for each stakeholder:
  posthog.capture("stakeholder_sentiment_recorded", {
    "deal_id": "{deal_id}",
    "stakeholder_role": role,
    "sentiment": sentiment,
    "support_level": support_level,
    "engagement_level": engagement_level
  })
```

## Output

- Per-stakeholder sentiment, priorities, concerns, and support levels updated in Attio
- Consensus and conflict areas documented on the deal record
- Follow-up actions routed: concern-specific plans for skeptics/blockers, tasks for unresolved items
- Discovery questions updated with answers and signal evaluations
- PostHog events logged for threshold tracking

## Triggers

Run this drill:
- Automatically after every discovery call (triggered by Fireflies webhook)
- Manually after informal stakeholder conversations where notes were taken
