---
name: timing-auto-scoring
description: Automated pipeline that predicts prospect timeline category from enrichment signals before any human contact
category: Sales
tools:
  - n8n
  - Clay
  - Attio
  - PostHog
  - Anthropic
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - clay-enrichment-waterfall
  - clay-intent-signals
  - attio-deals
  - attio-custom-attributes
  - posthog-custom-events
---

# Timing Auto-Scoring

Build an automated pipeline that predicts a prospect's buying timeline before the first human interaction. When a new deal enters Attio, n8n triggers Clay enrichment for timing-relevant signals, Claude scores the signals into a timeline category, and the result routes back to Attio with an auto-assigned follow-up cadence.

## Input

- n8n instance connected to Attio and Clay
- Clay table with timing signal enrichment columns configured
- Attio deal with at least: company name, contact name, contact email
- Anthropic API key for Claude-based scoring

## Steps

### 1. Configure the n8n trigger

Using `n8n-triggers`, create a workflow that fires when a new deal is created in Attio:

```json
{
  "trigger": "attio_webhook",
  "event": "deal.created",
  "filter": "timeline_category IS NULL"
}
```

Also create a secondary trigger for manual re-scoring: an Attio button click or a scheduled daily run that catches any unscored deals.

### 2. Enrich with timing signals via Clay

Using `clay-enrichment-waterfall` and `clay-intent-signals`, push the deal to Clay and enrich with:

| Signal | Source | Timing Relevance |
|--------|--------|-----------------|
| Last funding round date and amount | Crunchbase/PitchBook | Recent funding = budget available, Immediate/Near-term signal |
| Open job postings in relevant department | LinkedIn Jobs/Indeed | Active hiring = building team, Near-term signal |
| Technology stack and recent changes | BuiltWith/Wappalyzer | Stack migration = evaluation window open |
| Competitor contract renewal estimate | Clay Claygent research | Approaching renewal = switching timeline |
| Fiscal year end month | SEC filings/Claygent | Budget cycle awareness |
| Recent news and press releases | Google News/Claygent | Leadership changes, strategic shifts, regulatory |
| Company growth rate (headcount) | LinkedIn/Apollo | Fast growth = urgent scaling needs |
| G2/Capterra review recency | G2 API/scraping | Recent reviews of competitors = active evaluation |

Configure Clay to return a structured row with all signals populated.

### 3. Score signals with Claude

Send enriched signals to Claude for timeline prediction:

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1000,
  "messages": [{
    "role": "user",
    "content": "Based on the following enrichment data, predict this prospect's buying timeline.\n\nCompany: {company_name}\nContact: {contact_name}, {contact_title}\nEnrichment signals:\n{clay_enrichment_data}\n\nClassify as:\n- Immediate (0-30 days): hard deadline or acute pain evident\n- Near-term (1-3 months): clear intent signals, budget likely available\n- Medium-term (3-6 months): some interest indicators but no urgency\n- Long-term (6+ months): early research or no timing signals detected\n\nReturn JSON:\n{\n  \"predicted_timeline_category\": \"...\",\n  \"predicted_target_date\": \"YYYY-MM-DD\",\n  \"confidence\": 1-5,\n  \"key_signals\": [{\"signal\": \"...\", \"weight\": \"high|medium|low\", \"reasoning\": \"...\"}],\n  \"predicted_urgency_drivers\": [\"...\"],\n  \"predicted_slippage_risk\": \"High|Medium|Low\",\n  \"recommended_outreach_timing\": \"immediate|within_week|within_month|nurture\",\n  \"reasoning\": \"...\"\n}"
  }]
}
```

### 4. Write scores back to Attio

Using `attio-deals` and `attio-custom-attributes`:

```
PATCH https://app.attio.com/api/v2/objects/deals/records/{deal_id}
{
  "data": {
    "attributes": {
      "timeline_category": "{predicted_category}",
      "target_close_date": "{predicted_target_date}",
      "urgency_drivers": ["{predicted_drivers}"],
      "timeline_confidence": {confidence},
      "slippage_risk": "{predicted_slippage_risk}",
      "timeline_qualified": false
    }
  }
}
```

Note: `timeline_qualified` stays `false` until a human validates the prediction via a discovery call (using `timing-discovery-call` drill). The auto-score is a pre-qualification estimate.

### 5. Route the deal

Based on predicted timeline:
- **Immediate:** Slack alert to founder. Suggest booking a call within 24 hours.
- **Near-term:** Add to active outreach queue. Priority follow-up within the week.
- **Medium-term:** Add to standard outreach sequence. Monthly check-in cadence.
- **Long-term:** Add to nurture sequence. Quarterly re-scoring trigger.

### 6. Log PostHog events

```javascript
posthog.capture('timing_auto_score_completed', {
  deal_id: '{deal_id}',
  predicted_category: '{predicted_category}',
  confidence: {confidence},
  signal_count: {number_of_signals},
  source: 'auto_enrichment'
});
```

### 7. Track prediction accuracy

When a deal later gets human-validated via `timing-discovery-call`, compare the auto-score prediction against the post-call score:

```javascript
posthog.capture('timing_prediction_accuracy', {
  deal_id: '{deal_id}',
  predicted_category: '{auto_category}',
  actual_category: '{human_validated_category}',
  accurate: predicted === actual,
  days_off: abs(predicted_date - actual_date)
});
```

This feeds the accuracy tracking that informs whether the auto-scoring model needs recalibration.

## Output

- Every new deal auto-scored with a predicted timeline within minutes of CRM entry
- Routing decisions made before any human touch
- Prediction accuracy tracked over time to calibrate the model
- PostHog events for funnel analytics
