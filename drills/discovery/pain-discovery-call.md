---
name: pain-discovery-call
description: Full pain discovery call lifecycle — transcribe, extract pains, quantify dollar impact, score, and log to CRM
category: Discovery
tools:
  - Fireflies
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - call-transcript-pain-extraction
  - pain-quantification-prompt
  - attio-deals
  - attio-notes
  - posthog-custom-events
---

# Pain Discovery Call

This drill handles everything that happens after a pain discovery call ends: transcript retrieval, automated pain extraction, dollar quantification, CRM logging, and follow-up routing. It converts a conversation into structured, actionable pain intelligence.

## Input

- Completed discovery call with Fireflies recording
- Deal record in Attio (created during `pain-discovery-call-prep`)
- Call prep document with hypothesized pains

## Steps

### 1. Retrieve and verify transcript

Wait for Fireflies to process the transcript (typically 5-15 minutes post-call). Poll the Fireflies API:

```graphql
query {
  transcripts(filter: { date_from: "{today}" }) {
    id
    title
    duration
    sentences { speaker_name text start_time end_time }
    summary
    action_items
  }
}
```

Match the transcript to the deal by meeting title or attendee email. If no transcript is found within 30 minutes, alert the caller and fall back to manual note entry.

Validate the transcript has sufficient content: minimum 200 words of prospect speech (not just the caller talking). If below this threshold, the call likely had limited discovery value — log it but skip automated extraction.

### 2. Extract pain points from transcript

Run the `call-transcript-pain-extraction` fundamental with the full transcript text. This returns:
- Array of identified pains with categories, severity scores, and supporting quotes
- Total quantified pain estimate
- Quantification rate (what percentage of pains have dollar estimates)
- Gaps in discovery (areas not explored)

### 3. Quantify each pain in dollar terms

For each extracted pain where `confidence >= 0.5` and `depth` is "explored" or "quantified," run the `pain-quantification-prompt` fundamental. This combines transcript clues with enrichment data to produce:
- Conservative annual cost estimate
- Low/high range
- Calculation steps with sources
- Pain-to-price ratio

Skip pains with `depth = "surface"` — these need follow-up discovery before quantification.

### 4. Calculate aggregate pain metrics

Compute:
- **Total quantified pain:** Sum of all `estimated_annual_cost` values
- **Pain-to-price ratio:** `total_quantified_pain / product_annual_price`
- **Pain count:** Total number of distinct pains identified
- **Quantification rate:** Pains with dollar estimates / total pains
- **Discovery depth score:** (surface pains * 1 + explored * 2 + quantified * 3) / (pain_count * 3)

### 5. Compare to call prep hypotheses

Pull the call prep document from Attio. Compare:
- Which hypothesized pains were confirmed? (Predicted and found)
- Which hypothesized pains were not mentioned? (Predicted but absent)
- Which pains were unexpected? (Found but not predicted)

This comparison calibrates the pre-call research over time. Log the hit rate for hypothesis accuracy.

### 6. Update CRM with pain data

Using `attio-deals`, update the deal record:
```json
{
  "pain_count": 5,
  "total_quantified_pain": 412800,
  "pain_quantification_rate": 0.8,
  "pain_to_price_ratio": 17.2,
  "strongest_pain": "Manual data entry costing $172K/yr",
  "pain_discovery_date": "2026-03-30",
  "discovery_depth_score": 0.73
}
```

Using `attio-notes`, create a structured note:

```markdown
## Pain Discovery Results — {date}
### Prospect: {company_name} / {contact_name}

### Pain Summary
| # | Pain | Category | Severity | Annual Cost | Confidence |
|---|------|----------|----------|-------------|------------|
| 1 | {pain} | {category} | {severity}/10 | ${cost} | {conf} |
| 2 | ... | ... | ... | ... | ... |

**Total Quantified Pain:** ${total}
**Pain-to-Price Ratio:** {ratio}x
**Quantification Rate:** {rate}%

### Key Quotes
- "{most impactful quote}" — on {pain area}
- "{second quote}" — on {pain area}

### Urgency Signals
- {signal 1}
- {signal 2}

### Gaps (Explore in Follow-Up)
- {area not covered}
- {surface-level pain needing deeper probe}

### Next Steps
- {action items from Fireflies}
```

### 7. Fire tracking events

Using `posthog-custom-events`, log:

```json
{
  "event": "pain_discovery_call_completed",
  "properties": {
    "deal_id": "...",
    "pain_count": 5,
    "total_quantified_pain": 412800,
    "pain_to_price_ratio": 17.2,
    "quantification_rate": 0.8,
    "discovery_depth_score": 0.73,
    "hypothesis_hit_rate": 0.6,
    "call_duration_minutes": 42
  }
}
```

### 8. Route based on results

- **Strong discovery (pain-to-price ratio >= 10x, quantification rate >= 0.7):** Flag as high-priority. Trigger `pain-based-business-case` drill for auto-generated business case.
- **Moderate discovery (5x-10x ratio or 0.4-0.7 quantification):** Schedule a follow-up call focused on the gaps. Run `pain-discovery-call-prep` again targeting the unexplored areas.
- **Weak discovery (< 5x ratio or < 0.4 quantification):** Review whether this prospect is ICP-fit. If yes, try a different discovery approach. If no, move to nurture.

## Output

- Structured pain data stored in Attio with dollar estimates
- Call notes with supporting quotes and next steps
- PostHog events for funnel tracking
- Routing recommendation for next action

## Triggers

Run automatically after every discovery call via n8n workflow triggered by Fireflies transcript completion webhook.
