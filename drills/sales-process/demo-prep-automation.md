---
name: demo-prep-automation
description: Auto-generate personalized demo prep docs from discovery call transcripts and CRM data
category: Demos
tools:
  - Fireflies
  - Anthropic
  - Attio
  - Loom
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - call-transcript-bant-extraction
  - attio-notes
  - attio-deals
  - loom-recording
  - loom-analytics
---

# Demo Prep Automation

This drill takes discovery call transcripts and CRM context and automatically generates a personalized demo preparation document: pain-to-feature mapping, custom talking points, ROI calculations, and a structured demo flow. Designed for founder-led sales where the founder runs both discovery and demo.

## Input

- Completed discovery call with Fireflies transcript available
- Deal record in Attio with BANT scores (from `bant-discovery-call` drill)
- Product feature catalog (a list of features with descriptions, stored in Attio or a markdown file)

## Steps

### 1. Retrieve discovery transcript and extract pain signals

Fetch the full transcript from Fireflies using the `fireflies-transcription` fundamental:

```graphql
query { transcript(id: "<transcript-id>") { title, sentences { speaker_name, text }, summary, action_items } }
```

Run `call-transcript-bant-extraction` on the transcript. Focus on the `need` dimension -- extract every pain point the prospect mentioned, with exact quotes. Also extract:
- Current workaround or competitor they use
- Impact of the pain (hours wasted, revenue lost, team frustration)
- Stakeholders affected by the pain

### 2. Map pains to product features

Send the extracted pains to Claude with your feature catalog:

```
POST https://api.anthropic.com/v1/messages

Prompt: "Given these prospect pain points and our product feature catalog, create a pain-to-feature mapping. For each pain, identify the product feature that solves it, explain how it solves it in one sentence, and estimate the ROI (time saved, cost reduced, or revenue gained).

Pain points:
{pain_list_with_quotes}

Feature catalog:
{feature_catalog}

Return JSON:
{
  "mappings": [
    {
      "pain": "exact quote from prospect",
      "pain_category": "reporting|automation|integration|visibility|other",
      "feature": "feature name",
      "how_it_solves": "one sentence",
      "roi_estimate": "quantified estimate",
      "demo_priority": 1-5
    }
  ],
  "demo_narrative": "3-4 sentence story arc connecting their current state to the future state with our product",
  "opening_hook": "one sentence that references their specific pain to open the demo"
}"
```

### 3. Generate the demo prep document

Using the pain-to-feature mapping, generate a structured demo prep doc via Claude:

```
## Demo Prep — {Company Name}
### Date: {demo_date}
### Prospect: {name}, {title}

### Opening Hook
{opening_hook} — reference their discovery pain immediately

### Discovery Recap (2 minutes)
Confirm the pains they shared:
- "{pain quote 1}" — we'll address this in section 1
- "{pain quote 2}" — we'll address this in section 2
- "{pain quote 3}" — we'll address this in section 3

### Demo Flow (ordered by priority)

#### Section 1: {Feature solving pain #1} (8 minutes)
- Show: {specific screens/workflows to demo}
- Say: "{how it solves their pain}"
- ROI: "{quantified value}"
- Transition: "You also mentioned {pain #2}..."

#### Section 2: {Feature solving pain #2} (8 minutes)
- Show: {specific screens/workflows to demo}
- Say: "{how it solves their pain}"
- ROI: "{quantified value}"

#### Section 3: {Feature solving pain #3} (5 minutes)
- Show: {specific screens/workflows to demo}
- Say: "{how it solves their pain}"
- ROI: "{quantified value}"

### Closing (5 minutes)
- Total ROI summary: "{combined value}"
- Proposed next step: {based on BANT assessment}
- Questions to ask: {authority and timeline probes if gaps remain}

### Risk Factors
- BANT gaps: {which dimensions scored low and how to address}
- Objections likely: {based on discovery signals}
- Competitor comparison points: {if competitor was mentioned}
```

Store the full doc as an Attio note on the deal using `attio-notes`.

### 4. Prepare follow-up assets

After the demo, the agent should prepare:

1. **Recap video script**: Generate a 2-minute Loom script that recaps the three features shown and their ROI. Use `loom-recording` fundamental for recording guidance.
2. **Follow-up email**: Draft an email referencing the specific pains discussed, features shown, and ROI estimates. Include the Loom link and a Cal.com booking link for the next meeting.
3. **Stakeholder summary**: If the prospect mentioned other decision-makers, generate a one-page summary they can forward internally.

Store all assets as Attio notes on the deal.

### 5. Track demo prep quality

Log a PostHog event for each demo prepped:

```json
{
  "event": "demo_prep_generated",
  "properties": {
    "deal_id": "...",
    "pains_mapped": 3,
    "features_shown": 3,
    "roi_estimated": true,
    "bant_composite": 68,
    "demo_date": "2026-04-02"
  }
}
```

After the demo, log the outcome:

```json
{
  "event": "demo_completed",
  "properties": {
    "deal_id": "...",
    "outcome": "next_step_committed|follow_up_needed|no_interest",
    "pains_addressed": 3,
    "questions_asked": 7,
    "meeting_duration_minutes": 42,
    "recap_video_sent": true
  }
}
```

### 6. Track recap video engagement

Use the `loom-analytics` fundamental to monitor which prospects watch the recap video and for how long. Feed view data back to Attio:

- If prospect watched >80% of recap: flag as high-engagement, prioritize follow-up
- If prospect watched <20% or did not watch: send a text-only recap email as backup
- If prospect clicked the CTA in the video: fast-track to next meeting

## Output

- Personalized demo prep document stored in Attio
- Pain-to-feature mapping with ROI estimates
- Structured demo flow with talking points
- Post-demo follow-up assets (recap video script, email draft, stakeholder summary)
- PostHog events for demo prep and outcome tracking

## Triggers

- Run after every completed discovery call (triggered by `bant-discovery-call` drill completion)
- Re-run if the prospect provides additional context before the demo
