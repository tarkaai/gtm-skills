---
name: call-brief-feedback-loop
description: After a meeting, compare the brief's predictions to actual outcomes and score brief quality to improve future generation
category: Discovery
tools:
  - Fireflies
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - attio-notes
  - attio-deals
  - anthropic-api-patterns
  - posthog-custom-events
---

# Call Brief Feedback Loop

After every meeting that used an AI-generated brief, this drill compares the brief's predictions and recommendations against what actually happened in the call. It scores brief quality, identifies which sections were most and least useful, and feeds this data back to improve future brief generation. Over time, this creates a learning loop that makes briefs progressively more accurate and actionable.

## Input

- Deal ID in Attio
- The meeting brief (stored as Attio note tagged `meeting-brief`)
- Fireflies transcript of the completed meeting
- Meeting outcome (next step committed, follow-up needed, stalled, lost)

## Steps

### 1. Retrieve the brief and the transcript

Pull the meeting brief from Attio notes:
```
attio.list_notes({ parent: { object: "deals", record_id: "{deal_id}" }, tag: "meeting-brief" })
```

Pull the call transcript from Fireflies:
```graphql
query { transcript(id: "{transcript_id}") { title, sentences { speaker_name, text }, summary, action_items } }
```

Also pull action items using `fireflies-action-items`.

### 2. Score brief accuracy with Claude

Send both the brief and the transcript to Claude for comparison:

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2000,
  "messages": [{
    "role": "user",
    "content": "Compare this meeting preparation brief against the actual meeting transcript. Score each section of the brief.\n\nBRIEF:\n{brief_markdown}\n\nTRANSCRIPT SUMMARY:\n{transcript_summary}\n\nACTION ITEMS:\n{action_items}\n\nMEETING OUTCOME: {outcome}\n\nScore each brief section on accuracy (did predictions match reality?) and usefulness (was the section actionable during the call?):\n\nReturn JSON:\n{\n  \"sections\": [\n    {\n      \"section\": \"executive_summary\",\n      \"accuracy_score\": 1-5,\n      \"usefulness_score\": 1-5,\n      \"notes\": \"one sentence on what was right or wrong\"\n    }\n  ],\n  \"overall_accuracy\": 1-5,\n  \"overall_usefulness\": 1-5,\n  \"best_section\": \"which section was most valuable\",\n  \"worst_section\": \"which section was least accurate or useful\",\n  \"missed_topics\": [\"topics that came up in the call but were NOT in the brief\"],\n  \"unused_sections\": [\"sections in the brief that were irrelevant to the actual conversation\"],\n  \"improvement_suggestions\": [\"2-3 specific ways to improve briefs for this type of meeting\"]\n}"
  }]
}
```

### 3. Extract new intelligence from the call

From the transcript, extract information that should update the account intelligence profile:
- New pain points mentioned
- New stakeholders referenced
- Updated timeline or budget information
- Competitive mentions
- Next steps agreed

Store these as Attio notes tagged `post-call-intel` and update deal properties (stage, BANT scores, etc.).

### 4. Log brief quality metrics to PostHog

```json
{
  "event": "meeting_brief_scored",
  "properties": {
    "deal_id": "...",
    "meeting_type": "...",
    "overall_accuracy": 4,
    "overall_usefulness": 3,
    "best_section": "key_questions",
    "worst_section": "competitive_positioning",
    "missed_topic_count": 2,
    "unused_section_count": 1,
    "meeting_outcome": "next_step_committed",
    "brief_led_to_positive_outcome": true
  }
}
```

### 5. Build feedback dataset

Over time, these scores build a dataset that reveals:
- Which brief sections consistently score high/low for different meeting types
- Whether higher-quality briefs correlate with better meeting outcomes
- Which data sources contribute most to brief accuracy
- Whether brief quality improves over time (the learning loop is working)

Query this dataset periodically to adjust the brief generation prompt and intelligence assembly priorities.

## Output

- Brief quality scorecard stored as Attio note tagged `brief-feedback`
- Updated deal intelligence from the call
- PostHog events for aggregate quality analysis
- Feedback data that feeds into prompt optimization at Scalable/Durable levels

## Triggers

- Run within 24 hours after every meeting that had an AI-generated brief
- Can be triggered automatically via n8n when Fireflies posts a transcript webhook
