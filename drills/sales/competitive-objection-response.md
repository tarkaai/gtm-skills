---
name: competitive-objection-response
description: Diagnose a competitive objection, match to battlecard intelligence, generate a positioning response, and log the outcome for pattern learning
category: Sales
tools:
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - call-transcript-objection-extraction
  - competitive-positioning-generation
  - attio-deals
  - attio-notes
  - posthog-custom-events
---

# Competitive Objection Response

This drill handles the full lifecycle of a single competitive objection: identify the competitor, classify the objection type, pull battlecard intelligence, generate a tailored positioning response, and log the outcome. It converts "we're also looking at {competitor}" from a threat into a structured competitive intelligence moment.

## Input

- A competitive objection received during a sales call, demo, follow-up, or email
- Deal record in Attio with pain data and decision criteria
- The objection itself: a call transcript segment or email text mentioning the competitor
- Battlecard data for the competitor (from `competitive-battlecard-assembly` drill, stored on Attio Competitor record)

## Steps

### 1. Extract and classify the competitive objection

If the objection came from a recorded call, run `call-transcript-objection-extraction` on the transcript. Extend the extraction to capture competitive-specific fields:

```json
{
  "competitor_name": "Name of the competitor mentioned",
  "competitive_objection_type": "active_evaluation|incumbent_loyalty|feature_comparison|price_comparison|social_proof|switching_cost",
  "objection_quote": "Exact prospect quote",
  "what_they_like_about_competitor": "What the prospect specifically praised (if any)",
  "evaluation_stage": "early_research|shortlist|finalist_comparison|switching_consideration",
  "decision_criteria_revealed": ["Criteria the prospect mentioned as important"],
  "severity": 1-10,
  "emotional_tone": "exploratory|committed|anxious|negotiating"
}
```

If the objection came via email, manually build the classification using the same schema.

### 2. Pull battlecard intelligence

Query Attio for the Competitor record matching `competitor_name`. Extract:
- Their known strengths and weaknesses
- Our historical win rate against them
- Common objections and winning response frameworks
- Trap questions
- Pricing intelligence
- Recent product changes

If no Competitor record exists (first mention of this competitor), create a minimal record and flag for battlecard assembly: "New competitor detected: {name}. Run `competitive-battlecard-assembly` drill to build initial battlecard."

### 3. Match to prospect's decision criteria

Cross-reference the prospect's decision criteria (from the objection extraction and deal record) with the battlecard's comparison data:

- For each decision criterion, determine: are we stronger, weaker, or equal vs this competitor?
- Identify the "hinge criterion" — the one dimension where we have the biggest advantage AND the prospect cares about it
- Identify any "concede criteria" — dimensions where the competitor is genuinely stronger and we should acknowledge it

### 4. Generate the positioning response

Run `competitive-positioning-generation` with:
- The classified objection
- The battlecard data
- The prospect's pain data and decision criteria
- Historical framework effectiveness against this competitor

This returns: positioning framework, verbal response, trap questions, comparison talking points, follow-up email, champion ammunition, and supporting asset recommendation.

### 5. Human review checkpoint

**Human action required:** Review the generated response before delivery. Check:
- Is the positioning factually accurate? (Do not claim capabilities we don't have)
- Does it avoid competitor disparagement? (Reframe any negative language)
- Are the trap questions natural and conversational?
- Is the hinge criterion genuinely our strength?
- Is the follow-up email under 200 words and focused on the prospect's pain?

### 6. Deliver the response

On the next call or in follow-up:
1. Acknowledge the competitor respectfully: "They're a solid company."
2. Pivot immediately to the prospect's pain: "The question is really about which approach solves {their top pain} best for your specific situation."
3. Ask the trap questions to let the prospect discover the gap
4. Share comparison talking points tied to their criteria
5. Propose a clear next step (deep-dive on the hinge criterion, reference call with similar customer, or technical comparison)

### 7. Log the outcome

After delivery, update the deal record in Attio:
```json
{
  "competitor_mentioned": "{competitor_name}",
  "competitive_objection_type": "active_evaluation",
  "positioning_framework": "pain_alignment",
  "positioning_delivered_date": "2026-03-30",
  "competitive_outcome": "differentiated|partially_differentiated|lost_on_criteria|prospect_chose_us|prospect_chose_competitor",
  "hinge_criterion": "{the dimension that mattered most}",
  "days_to_resolution": 5
}
```

Fire PostHog events:
```json
{
  "event": "competitive_objection_handled",
  "properties": {
    "deal_id": "...",
    "competitor_name": "...",
    "competitive_objection_type": "active_evaluation",
    "positioning_framework": "pain_alignment",
    "outcome": "differentiated",
    "severity": 7,
    "hinge_criterion": "...",
    "days_to_resolution": 5,
    "battlecard_version_used": 3
  }
}
```

### 8. Route based on outcome

- **Differentiated:** Prospect acknowledged our advantage. Advance deal. Update battlecard with this win pattern.
- **Partially differentiated:** Prospect still evaluating. Schedule a competitive deep-dive (technical comparison or reference call). Trigger competitive follow-up sequence.
- **Lost on criteria:** Prospect chose the competitor on a specific criterion. Log the loss reason for battlecard improvement. Consider: can we address this gap in product or positioning?
- **Prospect chose us:** Competitive deal won. Extract the deciding factors and add to the battlecard's "When We Win" section.
- **Prospect chose competitor:** Log the loss with full context. Feed into battlecard's "When We Lose" section. This data is gold for future competitive deals.

## Output

- Structured competitive objection data stored in Attio
- Tailored positioning response using battlecard intelligence
- PostHog events for competitive effectiveness tracking
- Battlecard feedback loop (win/loss outcomes improve future responses)

## Triggers

Run manually after each competitive objection at Smoke level. At Baseline+, triggered automatically by `competitive-detection-automation` drill when a competitor mention is detected in a call transcript or email.
