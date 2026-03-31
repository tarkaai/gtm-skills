---
name: timing-discovery-call
description: Run a structured discovery call focused on urgency extraction — prep timing questions, record, extract timeline signals, score, and log to CRM
category: Sales
tools:
  - Fireflies
  - Attio
  - Anthropic
  - Cal.com
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - call-transcript-timing-extraction
  - attio-deals
  - attio-notes
  - calcom-booking-links
---

# Timing Discovery Call

Full lifecycle of a timing-focused discovery call: pre-call research to identify likely urgency drivers, question preparation targeting the weakest timing signals, transcript analysis for timeline extraction, and CRM logging. Designed for founder-led sales where the founder is on the call.

## Input

- Deal record in Attio with any pre-enrichment data (company info, funding stage, job postings)
- Cal.com booking link for scheduling
- Fireflies configured to auto-join meetings
- (Optional) Pre-enrichment timing signals from Clay (budget cycle, contract renewal, funding round)

## Steps

### 1. Pre-call timing research

Before the call, gather context that hints at the prospect's timeline:

1. Pull the deal record from Attio using `attio-deals`: get company name, contact role, existing `timeline_category` if set, any notes from prior interactions
2. Check for pre-enrichment timing signals:
   - Recent funding round → likely has budget now, potential Immediate/Near-term
   - Job postings in relevant area → building a team, Near-term signal
   - Contract renewal window for competitor product → potential switching timeline
   - Fiscal year end approaching → budget-expiration urgency
   - Recent leadership change → new exec mandate possible
3. Identify the biggest timing unknowns — what do you NOT know about their timeline?

### 2. Generate timing question guide

Use Claude to generate a customized question guide based on the pre-call research:

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1000,
  "messages": [{
    "role": "user",
    "content": "Generate a timing-focused discovery call question guide for this prospect.\n\nCompany: {company_name}\nContact: {contact_name}, {contact_title}\nPre-enrichment signals: {signals}\nUnknowns: {unknowns}\n\nGenerate 6-8 questions in 3 categories:\n\n1. **Trigger questions** (what's driving urgency):\n   - 'What's driving you to look at this now?'\n   - 'Has something changed recently that makes this a priority?'\n   - Custom based on signals\n\n2. **Timeline questions** (when do they need to act):\n   - 'When do you need this in place?'\n   - 'What does your evaluation process typically look like?'\n   - Custom based on unknowns\n\n3. **Consequence questions** (what happens if they don't act):\n   - 'What happens if you don't solve this by [their stated date]?'\n   - 'What's the cost of waiting another quarter?'\n   - Custom based on pain severity\n\nOrder the questions to flow naturally in conversation. Mark the 2-3 most critical questions with [MUST ASK]."
  }]
}
```

### 3. Execute the call

**Human action required:** Conduct the discovery call. The agent cannot join calls but can prepare the guide above.

During the call, focus on:
- Asking the [MUST ASK] questions naturally within the first 15 minutes
- Listening for urgency language: "need to," "have to," "by Q3," "before the board meeting," "contract expires"
- Listening for anti-urgency language: "just exploring," "no rush," "sometime this year," "when we get around to it"
- Probing vague timelines: if they say "Q3," ask "is that a hard deadline or a target?"
- Multi-threading: if possible, ask "does your team agree on this timeline?"

Fireflies auto-records and transcribes the call.

### 4. Extract timing signals from transcript

After the call, run the `call-transcript-timing-extraction` fundamental:

1. Retrieve the transcript from Fireflies
2. Send to Claude for timing extraction
3. Receive structured JSON with: timeline_category, target_date, urgency_drivers, timeline_confidence, slippage_risk, consequence_of_inaction, effective_questions

### 5. Score and log to Attio

Update the deal record using `attio-deals`:

```
PATCH https://app.attio.com/api/v2/objects/deals/records/{deal_id}
{
  "data": {
    "attributes": {
      "timeline_category": "{extracted_category}",
      "target_close_date": "{extracted_target_date}",
      "urgency_drivers": ["{driver_1}", "{driver_2}"],
      "timeline_confidence": {extracted_confidence},
      "slippage_risk": "{extracted_risk}",
      "consequence_of_inaction": "{extracted_consequence}",
      "timeline_qualified": true,
      "timeline_qualified_date": "{today}"
    }
  }
}
```

Add a note using `attio-notes` with the full timing analysis and recommended follow-up cadence.

### 6. Fire PostHog events

Log the qualification event:

```javascript
posthog.capture('timeline_category_assigned', {
  deal_id: '{deal_id}',
  category: '{timeline_category}',
  confidence: {timeline_confidence},
  urgency_drivers: ['{drivers}'],
  slippage_risk: '{slippage_risk}',
  source: 'discovery_call'
});
```

### 7. Determine next action

Based on extraction results:
- **Immediate + Confidence >= 4:** Schedule next step within 48 hours. Alert founder via Slack.
- **Near-term + Confidence >= 3:** Schedule follow-up within 1 week. Add to active pipeline cadence.
- **Medium-term:** Add to nurture with monthly check-in. Set a calendar reminder for re-qualification in 60 days.
- **Long-term:** Add to long-term nurture. Set a calendar reminder for re-qualification in 90 days.
- **Confidence <= 2 (any category):** Schedule a dedicated follow-up call specifically to nail down timeline. Note: "Timeline unclear — needs validation."

## Output

- Deal record in Attio updated with all timeline fields
- PostHog event logged for analytics
- Recommended follow-up cadence and next action
- Note in Attio with full timing analysis
- Effective questions documented for use in future calls
