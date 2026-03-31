---
name: risk-mitigation-delivery
description: Automatically match identified deal risks to mitigation assets and deliver targeted content to the prospect within 24 hours
category: Sales
tools:
  - Attio
  - Anthropic
  - n8n
  - Instantly
  - Loops
fundamentals:
  - attio-deals
  - attio-notes
  - risk-mitigation-matching
  - n8n-workflow-basics
  - n8n-triggers
  - instantly-campaign
  - loops-sequences
  - anthropic-api-patterns
  - posthog-custom-events
---

# Risk Mitigation Delivery

This drill takes the unaddressed risks from a completed risk discovery call and delivers targeted mitigation content to the prospect. For each risk, it matches to the best available asset (case study, security whitepaper, ROI proof, reference contact, product documentation), drafts a personalized delivery message that references the prospect's exact words, and sends it within 24 hours of the call. Speed matters -- the longer a concern sits unaddressed, the more it festers.

## Input

- Risk discovery results from `risk-discovery-call` drill (stored in Attio)
- Deal record with contact email
- Mitigation content library (indexed in Attio or JSON file)

## Steps

### 1. Pull unaddressed risks from CRM

Query Attio for the deal record. Parse `risk_data_json` and filter for risks where:
- `response_effectiveness` is "unaddressed" or "partially_resolved"
- `risk_score` >= 25 (Medium or higher)

Sort by `risk_score` descending. Address the highest-severity risks first.

### 2. Match each risk to mitigation assets

For each unaddressed risk, run the `risk-mitigation-matching` fundamental. This returns:
- Ranked list of content assets that address the specific concern
- Delivery message draft that connects the asset to the prospect's exact words
- Content gap flags if no suitable asset exists

### 3. Draft the mitigation email

Using `anthropic-api-patterns`, generate a personalized email for each risk (or batch into one email if 2+ risks share a category):

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1000,
  "messages": [{
    "role": "user",
    "content": "Draft a follow-up email to {contact_name} at {company_name} that addresses the concerns they raised on our call. Tone: helpful, not defensive. Do not oversell. Acknowledge their concern, provide the relevant resource, and explain specifically how it addresses their worry.\n\nConcerns to address:\n{for each risk: summary, concern_quote, matched_asset_title, matched_asset_url, delivery_message}\n\nRules:\n- Reference their exact words (use the concern_quote)\n- Keep under 200 words\n- One clear CTA: review the material and let us know if questions remain\n- If multiple concerns, group by category\n- Do not use phrases like 'I understand your concern' -- be specific about WHAT you understand\n- Sign from {founder_name}\n\nReturn JSON: {\"subject\": \"...\", \"body\": \"...\", \"assets_attached\": [\"url1\", \"url2\"]}"
  }]
}
```

### 4. Send the mitigation email

Route based on the channel:
- **Direct email (via Loops or Instantly):** Use `instantly-campaign` for one-off sends if prospect is in an active sequence, or `loops-sequences` for lifecycle email if they are in the nurture flow.
- **Manual send (for high-value deals):** Instead of auto-sending, create a draft in Attio with the message and alert the founder: "Mitigation email ready for {company_name}. Review and send."

**Human action required:** For Critical-severity risks (risk_score >= 80), ALWAYS route to manual review. Auto-send only for Medium and High risks.

### 5. Schedule mitigation follow-up

For each risk where mitigation content was sent:
- Set a 3-day follow-up reminder in Attio
- If no response in 3 days, send a brief check-in: "Did the {asset_type} address your concern about {risk_summary}?"
- If the prospect responds positively, update risk status in Attio to "resolved"
- If the prospect raises new concerns, re-run `call-transcript-risk-extraction` on the email thread

### 6. Handle content gaps

For risks where `gap_identified` is true (no suitable asset exists):
- Log the gap in PostHog: `mitigation_content_gap` event
- Create an Attio task: "Create {mitigation_type} for {risk_category}: {risk_summary}"
- In the meantime, offer a direct conversation: "I'd like to address your concern about {risk_summary} directly -- can we schedule a 15-minute call with our {appropriate person: CTO for technical, CEO for vendor, Head of CS for organizational}?"

### 7. Track mitigation delivery

Using `posthog-custom-events`, log:

```json
{
  "event": "risk_mitigation_delivered",
  "properties": {
    "deal_id": "...",
    "risk_id": "risk-001",
    "risk_category": "technical",
    "risk_score": 56,
    "mitigation_type": "case_study",
    "asset_id": "asset-012",
    "delivery_channel": "email",
    "auto_sent": true,
    "hours_since_call": 18,
    "content_gap": false
  }
}
```

Track subsequent events:
- `risk_mitigation_opened` -- prospect opened the email
- `risk_mitigation_asset_viewed` -- prospect clicked the asset link
- `risk_mitigation_resolved` -- risk marked as resolved after mitigation
- `risk_mitigation_failed` -- prospect still concerned after mitigation attempt

## Output

- Personalized mitigation emails sent within 24 hours of risk discovery
- Content gap report for missing mitigation assets
- Follow-up sequence scheduled for each delivered mitigation
- Tracking events for measuring mitigation effectiveness

## Triggers

Triggered automatically by the `risk-discovery-call` drill when unaddressed Medium+ risks are detected. Can also be triggered manually when a seller identifies a new concern via email or chat.
