---
name: demo-recap-assembly
description: Extract key points from a demo transcript and assemble a personalized recap email with resources, answers, and next steps
category: Demos
tools:
  - Fireflies
  - Anthropic
  - Attio
  - Loom
  - Cal.com
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - call-transcript-pain-extraction
  - attio-notes
  - attio-deals
  - loom-recording
  - loom-analytics
  - calcom-booking-links
---

# Demo Recap Assembly

This drill takes a completed demo call transcript and generates a structured, personalized recap email within 2 hours of the demo ending. The recap covers: what was discussed, how the product addresses the prospect's specific needs, answers to questions raised, relevant resources, and a clear next step with a booking link.

## Input

- Completed demo call with Fireflies transcript available
- Deal record in Attio with at least: company name, contact name, contact email, deal stage
- Product resource library (case studies, docs, integration guides) accessible as URLs or markdown files
- Cal.com booking link for next meetings

## Steps

### 1. Retrieve and parse the demo transcript

Fetch the transcript from Fireflies using the `fireflies-transcription` fundamental:

```graphql
query { transcript(id: "<transcript-id>") { title, sentences { speaker_name, text }, summary, action_items, duration } }
```

Extract action items using `fireflies-action-items`:
```graphql
query { transcript(id: "<transcript-id>") { action_items { text, assignee } } }
```

### 2. Extract demo-specific signals from transcript

Run `call-transcript-pain-extraction` on the transcript. In addition to pain points, instruct the extraction to capture:

- **Features shown:** Which product features were demonstrated
- **Questions asked:** Every question the prospect asked, with the answer given (or "unanswered" if it was deferred)
- **Concerns raised:** Any hesitations, objections, or skepticism expressed
- **Interest signals:** Moments where the prospect said things like "that's exactly what we need" or asked detailed implementation questions
- **Stakeholders mentioned:** Other people the prospect referenced ("I'd need to show this to my VP of Eng")
- **Current tools/process:** Any mention of their existing workflow or competing tools

Send to Claude:
```
POST https://api.anthropic.com/v1/messages

Prompt: "Analyze this demo transcript. Extract the following in JSON:

{
  'features_demonstrated': [{'feature': '...', 'prospect_reaction': 'positive|neutral|negative', 'pain_addressed': '...'}],
  'questions_asked': [{'question': '...', 'answer_given': '...|unanswered', 'topic': '...'}],
  'concerns': [{'concern': '...', 'how_addressed': '...|not_addressed'}],
  'interest_signals': ['exact quote 1', 'exact quote 2'],
  'stakeholders_mentioned': [{'name': '...', 'role': '...', 'context': '...'}],
  'current_tools': ['tool1', 'tool2'],
  'suggested_next_step': 'technical_deep_dive|proposal_review|stakeholder_demo|pilot_discussion|pricing_discussion',
  'urgency_level': 'high|medium|low'
}

Transcript:
{full_transcript}"
```

### 3. Assemble the recap email

Generate the recap email using Claude:

```
POST https://api.anthropic.com/v1/messages

Prompt: "Write a demo recap email from {sender_name} to {prospect_name} ({prospect_title} at {company}). Use these extracted signals:

{demo_extraction_json}

Rules:
- Tone: professional but warm. First person. No corporate speak.
- Open with a thank-you and reference one specific moment from the demo that showed high interest.
- Section 1 (What We Covered): Bullet the 3-4 key features shown, each tied to a specific pain they mentioned. Use their words where possible.
- Section 2 (Your Questions): Address each question. For answered questions, summarize the answer. For unanswered questions, provide the answer now (research the answer from product docs).
- Section 3 (Resources): Link to 2-3 relevant resources matched to what they showed interest in. Choose from: {resource_library}
- Section 4 (Next Step): Propose the specific next step identified in the extraction. Include a Cal.com booking link: {calcom_link}
- If stakeholders were mentioned, add a line offering to send a one-pager they can share internally.
- Close with a specific date for your next check-in if they don't book within 48 hours.
- Total length: 250-350 words. No fluff.

Return JSON: {'subject': '...', 'body': '...', 'internal_notes': '...'}"
```

### 4. Store the recap in Attio

Using `attio-notes`, create a note on the deal record with:
- Subject: "Demo Recap — {date}"
- Body: The full recap email text
- Tags: `demo-recap`, `follow-up-sequence-start`

Using `attio-deals`, update the deal:
- `last_demo_date`: today
- `demo_recap_sent`: false (will be set to true after sending)
- `suggested_next_step`: the extracted next step
- `prospect_urgency`: the extracted urgency level
- `unanswered_questions`: count of unanswered questions
- `stakeholders_identified`: list of mentioned stakeholders

### 5. Prepare the recap video script (optional)

If the demo included a screen share of specific features, generate a 90-second Loom recap script using Claude:

```
"Write a 90-second Loom video script that recaps the demo for {prospect_name}.
Cover only the top 3 features they reacted positively to: {positive_features}.
For each feature, spend 20 seconds showing it and connecting it to their pain: {pain}.
Close with: 'I've included a link below to book our next conversation. Looking forward to it.'
Keep it conversational — this is a founder speaking directly to a prospect."
```

Use `loom-recording` for recording guidance. After recording, use `loom-analytics` to set up view tracking.

### 6. Log PostHog events

Fire a PostHog event for the recap assembly:
```json
{
  "event": "demo_recap_assembled",
  "properties": {
    "deal_id": "...",
    "features_covered": 4,
    "questions_addressed": 3,
    "unanswered_questions": 1,
    "concerns_raised": 2,
    "stakeholders_mentioned": 1,
    "urgency_level": "high",
    "suggested_next_step": "technical_deep_dive",
    "recap_video_included": true
  }
}
```

## Output

- Personalized demo recap email ready to send (stored in Attio)
- Deal record updated with demo signals and follow-up context
- Optional Loom recap video script
- PostHog event for tracking recap assembly

## Triggers

Run within 2 hours of every completed demo. Can be triggered manually by the founder or automatically via n8n when a Fireflies transcript becomes available for a meeting tagged as "demo."
