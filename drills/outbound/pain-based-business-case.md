---
name: pain-based-business-case
description: Generate a buyer-ready business case from quantified discovery call pain data and deliver it to the prospect's champion
category: Value Engineering
tools:
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - attio-deals
  - attio-notes
  - business-case-generation
  - pain-quantification-prompt
  - posthog-custom-events
---

# Pain-Based Business Case

This drill takes the structured pain data from a discovery call and transforms it into a business case document that the prospect's internal champion can use to secure budget approval. It uses the prospect's own words and quantified pain data to make the case compelling and credible.

## Input

- Deal record in Attio with completed pain extraction (from `pain-discovery-call` drill)
- At least 2 quantified pains with dollar estimates
- Product pricing information
- Champion's name and role

## Steps

### 1. Validate readiness

Pull the deal record from Attio using `attio-deals`. Check:
- `pain_count >= 2` (need at least 2 pains for a credible business case)
- `pain_quantification_rate >= 0.5` (at least half the pains have dollar estimates)
- `pain_to_price_ratio >= 3` (if less than 3x, the ROI story is weak)

If any check fails, return a recommendation to run another discovery call targeting the gaps before generating the business case.

### 2. Re-quantify any low-confidence pains

For pains where `confidence < 0.6`, re-run the `pain-quantification-prompt` fundamental with additional context gathered since the original extraction (follow-up emails, second calls, enrichment data). Update the pain record in Attio with the revised estimate.

### 3. Assemble business case inputs

Build the input object for `business-case-generation`:

```json
{
  "prospect_company": "{from Attio}",
  "prospect_contact": "{champion name and title}",
  "prospect_industry": "{from Attio}",
  "prospect_headcount": "{from Attio}",
  "prospect_revenue": "{from Clay enrichment}",
  "pains": "{parsed from pain_data_json in Attio}",
  "total_quantified_pain": "{from Attio}",
  "product_name": "{your product}",
  "product_annual_price": "{your pricing}",
  "implementation_timeline": "{standard implementation time}",
  "competitive_alternatives": ["Status quo", "{competitor 1}", "{competitor 2}"]
}
```

### 4. Generate the business case

Run the `business-case-generation` fundamental with the assembled inputs. This produces:
- Executive summary
- Current state with cost breakdown using prospect quotes
- Proposed solution
- ROI analysis with payback period
- Risk analysis with mitigations
- Alternatives comparison
- Recommendation and next steps

### 5. Human review checkpoint

**Human action required:** Review the generated business case before sending to the prospect. Check:
- Are the prospect quotes accurate and in context?
- Are the cost estimates defensible?
- Is the ROI calculation reasonable?
- Does the tone sound like the champion's internal pitch, not a vendor's sales deck?

Make any edits needed. The document should feel like the champion wrote it, not like your company generated it.

### 6. Deliver to champion

Options for delivery:
- Attach the business case to a follow-up email drafted for the caller to review and send
- Upload to the deal record in Attio as a file attachment
- If using a document platform (Google Docs, Notion), share the link with the champion

Include a cover note: "Based on our conversation, I put together a summary of the challenges we discussed and what solving them could look like. Feel free to use this internally — I wrote it from your perspective, not ours."

### 7. Track and measure

Fire PostHog events:
```json
{
  "event": "business_case_generated",
  "properties": {
    "deal_id": "...",
    "total_quantified_pain": 412800,
    "pain_to_price_ratio": 17.2,
    "roi_percentage": 1620,
    "payback_period_months": 0.7,
    "pain_count": 5
  }
}
```

Update the deal record:
- `business_case_status` = "sent"
- `business_case_date` = today
- `business_case_roi` = calculated ROI percentage

### 8. Follow up on business case

Set a reminder (via n8n or Attio automation) for 5 business days after sending:
- If no response: send a follow-up asking if the document was helpful and if they need anything else
- If positive response: schedule the next meeting (demo, proposal, technical deep-dive)
- If objection: log the objection, address it, and update the business case if needed

## Output

- Buyer-ready business case document using the prospect's own words
- Deal record updated with business case status and ROI
- PostHog tracking events for pipeline analysis
- Follow-up reminder set

## Triggers

Triggered automatically when a deal's `pain_to_price_ratio >= 10` and `pain_quantification_rate >= 0.7` after a discovery call. Can also be triggered manually for any deal with sufficient pain data.
