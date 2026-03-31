---
name: story-matched-demo-prep
description: Select the highest-resonance customer story for a prospect and generate a complete story-driven demo preparation document
category: Sales
tools:
  - Attio
  - Anthropic
  - Fireflies
  - Gong
fundamentals:
  - story-matching-scoring
  - story-narrative-generation
  - attio-deals
  - attio-notes
  - attio-contacts
  - fireflies-transcription
  - call-transcript-pain-extraction
  - posthog-custom-events
---

# Story-Matched Demo Prep

This drill takes a scheduled demo and produces a complete story-driven preparation document: it selects the best customer story from the library, generates a narrative that weaves product features through the story, and structures the entire demo flow around the prospect seeing themselves in the customer's experience.

## Input

- Scheduled demo with deal record in Attio
- Discovery call transcript (from Fireflies) with extracted pain points
- Story library populated (from `story-library-curation` drill)
- Product feature catalog

## Steps

### 1. Retrieve prospect context

Pull the deal and contact from Attio using `attio-deals` and `attio-contacts`:
- Company name, industry, headcount
- Contact role and title
- Deal stage, value, and notes

Fetch the discovery call transcript from Fireflies using `fireflies-transcription`. Run `call-transcript-pain-extraction` to extract:
- Specific pain points with prospect quotes
- Current workarounds or competitors
- Impact quantification (hours wasted, revenue at risk, team frustration)

### 2. Match the best story

Pull the full story library from Attio (all stories with `story_status: approved`).

Run `story-matching-scoring` with the prospect profile and story library. The scoring fundamental returns a ranked list with:
- `total_score` per story (0-100)
- Dimension-level scores (industry, size, pain overlap, role relevance, result impact)
- Adaptation hints for the top stories

Select the top-ranked story. If the top score is below 50:
- Flag a story gap for this segment
- Use a composite approach: take the closest story and note where adaptation is needed
- Log `story_gap_flagged: true` in PostHog

If two stories score within 5 points, note both in the prep doc and let the rep choose.

### 3. Generate the story narrative

Run `story-narrative-generation` with:
- The selected customer story (full structured record)
- The prospect context (pains, industry, role, discovery quotes)
- The product feature catalog

The narrative fundamental returns:
- Opening hook connecting story to prospect's pain
- Story arc with 3-5 phases (each with narration, product demonstration, and customer quotes)
- Emotional peak moment
- Closing bridge with prospect-specific question
- Feature-to-story mapping

### 4. Assemble the demo prep document

Combine the story match output and narrative into a structured prep doc:

```
## Story-Driven Demo Prep -- {Prospect Company}

### Prospect: {Name}, {Title}
### Demo Date: {date}
### Estimated Duration: 20-25 minutes

### Story Selected
**{Customer Company}**: {story_title}
Match score: {total_score}/100
Key overlap: {rationale from scoring}

### Pre-Demo Intelligence
- Prospect pains: {pain_list_with_quotes}
- Current workaround: {competitor_or_manual_process}
- Impact: {quantified_impact}

---

### Opening (2 minutes)
{opening_hook}

Say: "Before I show you the product, let me tell you about {Customer Company}. They were in almost exactly your situation — {customer challenge adapted to prospect context}."

If the prospect said something relevant in discovery, reference it: "You mentioned '{prospect_quote}' — {Customer} said almost the same thing."

### Story Phase 1: The Problem (3 minutes)
**Narrate:** {story_arc[0].narration}
**Show:** {story_arc[0].product_show}
**Customer quote:** "{story_arc[0].customer_quote}"

Pause after the quote. Let the prospect react. If they relate, probe: "Does that sound familiar?"

### Story Phase 2: The Turning Point (5 minutes)
**Narrate:** {story_arc[1].narration}
**Show:** {story_arc[1].product_show}

This is where you demonstrate the product capability that solved the customer's core pain. Show it in the customer's context, then say: "For your team, this would mean {prospect-specific adaptation}."

### Story Phase 3: The Solution in Action (5 minutes)
**Narrate:** {story_arc[2].narration}
**Show:** {story_arc[2].product_show}

### Story Phase 4: The Results (3 minutes)
**Narrate:** {story_arc[3].narration}
**Customer quote:** "{emotional_peak_quote}"

Say: "They went from {before state} to {after state} in {timeframe}. Given what you told me about {prospect pain}, I'd expect similar results for your team."

### Closing Bridge (2 minutes)
{closing_bridge}

End with: "{closing_question}"

### Objection Prep
If prospect says "our situation is different":
- Acknowledge the difference specifically
- Highlight the structural similarity: "The specifics differ, but the core challenge — {shared pain} — is the same."
- Offer a second story if available: "I can also share how {Story #2 Company} approached it differently."

### Follow-Up Assets
After the demo, prepare:
1. Recap email referencing the customer story and connecting it to the prospect's stated pain
2. The full case study (if published) as a PDF attachment
3. A 1-paragraph "what this means for you" summary bridging the customer's results to the prospect's situation

### Feature-to-Story Map
{table of features shown and which story moment they appeared in}
```

Store the complete prep doc in Attio using `attio-notes`.

### 5. Track demo prep events

Fire PostHog events using `posthog-custom-events`:

```json
{
  "event": "story_demo_prep_generated",
  "properties": {
    "deal_id": "...",
    "story_id": "acme-onboarding-speed",
    "story_match_score": 85,
    "pain_overlap_score": 27,
    "prospect_industry": "B2B SaaS",
    "story_gap_flagged": false,
    "features_mapped": 4,
    "adaptation_depth": "high"
  }
}
```

After the demo, log the outcome:

```json
{
  "event": "story_demo_completed",
  "properties": {
    "deal_id": "...",
    "story_id": "acme-onboarding-speed",
    "outcome": "next_step_committed|follow_up_needed|no_interest",
    "prospect_related_to_story": true,
    "questions_about_story": 4,
    "emotional_connection_observed": true,
    "next_step_type": "proposal_review"
  }
}
```

## Output

- Complete story-driven demo prep document in Attio
- Selected customer story with match rationale
- Structured demo flow with narration, product demonstrations, and customer quotes per phase
- Feature-to-story mapping
- PostHog tracking events for prep and outcome

## Triggers

- Run when a demo is scheduled (Cal.com webhook or deal stage change to "Demo Scheduled")
- Re-run if discovery data updates before the demo
- Re-run if the selected story is retired from the library
