---
name: price-objection-response
description: Diagnose a price objection's root cause, select the highest-win-rate response framework, generate a tailored response, and log the outcome
category: Sales
tools:
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - call-transcript-objection-extraction
  - objection-response-generation
  - pain-quantification-prompt
  - attio-deals
  - attio-notes
  - posthog-custom-events
---

# Price Objection Response

This drill handles the full lifecycle of a single price objection: diagnose the root cause, select the response framework most likely to succeed, generate a tailored response, deliver it, and log the outcome. It converts a "too expensive" moment into structured intelligence.

## Input

- A price objection received during a proposal call, follow-up email, or negotiation
- Deal record in Attio with existing pain data (from `pain-discovery-call` drill)
- The objection itself: either a call transcript segment or email text containing the pushback

## Steps

### 1. Extract and classify the objection

If the objection came from a recorded call, run `call-transcript-objection-extraction` on the transcript to get structured objection data: root cause, severity, emotional tone, and comparison anchor.

If the objection came via email or chat, manually build the objection input:
```json
{
  "objection_quote": "This is more than we budgeted for this quarter",
  "root_cause": "no_budget",
  "severity": 6,
  "emotional_tone": "genuine_concern",
  "comparison_anchor": null
}
```

Classify root cause using these diagnostic questions (ask on the next call or infer from context):
- "Compared to what?" -> `competitor_comparison` or `sticker_shock`
- "What budget did you have in mind?" -> `no_budget` or `authority_gap`
- "What's the cost of not solving this?" -> `value_gap`
- "Is it a matter of timing?" -> `timing`

### 2. Validate pain-to-price ratio

Pull the deal record from Attio. Check if pain data exists:
- If `pain_to_price_ratio >= 5`: strong value foundation. Proceed with confidence.
- If `pain_to_price_ratio` is 3-5: moderate. The response must lean heavily on ROI proof.
- If `pain_to_price_ratio < 3` or no pain data: the objection is likely a symptom of weak discovery. **Recommend re-running discovery before attempting to overcome the price objection.** Generate a note: "Price objection on deal {name} may stem from insufficient pain quantification. Current pain-to-price ratio: {ratio}x. Consider a follow-up discovery call before responding."

If `pain_to_price_ratio < 3`, re-run `pain-quantification-prompt` with any new context from the objection conversation to see if the estimate improves.

### 3. Generate the response

Run `objection-response-generation` with the classified objection and deal context. This returns:
- The selected response framework
- A verbal response script (2-4 sentences)
- Diagnostic follow-up questions
- A follow-up email with supporting data
- A supporting asset recommendation (ROI calculator, case study, TCO comparison, payment options, or business case)

### 4. Human review checkpoint

**Human action required:** Review the generated response before delivery. Check:
- Does the verbal response sound natural for the seller's voice?
- Is the pain-to-price math accurate and defensible?
- Is the follow-up email under 150 words and focused on one key point?
- Is the recommended asset available (or does it need to be created first)?

Adjust tone and specifics as needed. The generated response is a starting point, not a script to read verbatim.

### 5. Deliver the response

On the next call or in a follow-up email:
1. Deliver the verbal response or send the follow-up email
2. Ask the diagnostic questions to deepen understanding
3. Share the supporting asset if appropriate
4. Propose a clear next step

### 6. Log the outcome

After delivery, update the deal record in Attio:
```json
{
  "objection_type": "value_gap",
  "response_framework": "roi_proof",
  "response_delivered_date": "2026-03-30",
  "objection_outcome": "resolved|partially_resolved|unresolved|escalated|lost",
  "days_to_resolution": 3,
  "discount_offered": 0,
  "discount_accepted": false
}
```

Fire PostHog events:
```json
{
  "event": "price_objection_handled",
  "properties": {
    "deal_id": "...",
    "root_cause": "value_gap",
    "framework_used": "roi_proof",
    "outcome": "resolved",
    "severity": 7,
    "pain_to_price_ratio": 12.5,
    "days_to_resolution": 3,
    "discount_percentage": 0
  }
}
```

### 7. Route based on outcome

- **Resolved:** Deal moves forward. Update deal stage in Attio. Trigger next-step workflow.
- **Partially resolved:** Schedule a follow-up conversation. If a supporting asset was not yet sent, send it now. Consider involving the champion to reinforce value internally.
- **Unresolved:** Escalate. If the objection root cause was `authority_gap`, request a meeting with the economic buyer. If `value_gap`, consider running a `pain-based-business-case` drill to build a champion-ready ROI document.
- **Lost:** Log lost reason as "Price" in Attio. Add the objection to the loss analysis dataset for pattern detection.

## Output

- Structured objection data stored in Attio with root cause classification
- Tailored response delivered using the highest-win-rate framework
- PostHog events for response effectiveness tracking
- Routing recommendation for next action based on outcome

## Triggers

Run manually after each price objection is received. At Scalable+ levels, triggered automatically by `objection-detection-automation` drill when a price objection is detected in a call transcript.
