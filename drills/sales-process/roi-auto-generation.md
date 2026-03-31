---
name: roi-auto-generation
description: Automatically generate ROI calculators and business cases from CRM deal data without manual intervention
category: Value Engineering
tools:
  - Attio
  - Anthropic
  - n8n
  - PostHog
fundamentals:
  - attio-deals
  - attio-notes
  - attio-automation
  - roi-model-generation
  - business-case-generation
  - pain-quantification-prompt
  - n8n-triggers
  - n8n-workflow-basics
  - posthog-custom-events
---

# ROI Auto-Generation

This drill creates an always-on n8n workflow that monitors Attio for deals reaching the proposal stage with sufficient pain data, then automatically generates ROI calculators and business cases. The seller reviews and sends — no manual model building required.

## Input

- Attio pipeline configured with deal stages including Proposed
- Pain data populated on deals from `pain-discovery-call` drill
- n8n instance with Attio and Anthropic integrations configured
- Product pricing stored in `.gtm-config.json` or n8n environment variables

## Steps

### 1. Build the trigger workflow in n8n

Create an n8n workflow with an Attio webhook trigger:
- **Trigger:** Attio deal stage changes to "Proposed" OR `pain_count` attribute updated on a deal in Proposed stage
- **Filter:** Only proceed if `pain_count >= 2` AND `pain_quantification_rate >= 0.5` AND `roi_model_status != "generated"`
- **Rate limit:** Maximum 10 auto-generations per day to control API costs

### 2. Enrich and validate pain data

When the trigger fires:
1. Pull the full deal record from Attio including all pain data, champion info, and company enrichment
2. For each pain where `confidence < 0.6`, re-run `pain-quantification-prompt` with any new context
3. Validate that `pain_to_price_ratio >= 3` after re-quantification
4. If ratio < 3, skip auto-generation and send Slack alert: "Deal {name} has weak ROI ({ratio}x). Consider additional discovery before proposal."

### 3. Generate the ROI model

Run `roi-model-generation` with the validated pain data. This produces the full structured model with inputs, assumptions, savings breakdown, costs, summary, and sensitivity analysis.

Store the model in Attio as a note on the deal record.

### 4. Generate the business case document

Run `business-case-generation` with the ROI model output plus prospect context. This produces the champion-ready business case: executive summary, current state with prospect quotes, proposed solution, ROI analysis, risk analysis, alternatives comparison, and recommendation.

### 5. Package and notify

Build the deliverable:
1. Generate a Google Sheet ROI calculator (via Sheets API) pre-populated with the prospect's inputs
2. Generate a PDF business case (via Puppeteer or Markdown)
3. Attach both to the Attio deal record
4. Send a Slack notification to the deal owner: "ROI calculator and business case auto-generated for {company}. ROI: {X}x, payback: {Y} months. Review and send: {link}"

### 6. Track auto-generation metrics

Fire PostHog events:
```json
{
  "event": "roi_auto_generated",
  "properties": {
    "deal_id": "...",
    "trigger": "stage_change|pain_update",
    "roi_percentage": 0,
    "payback_months": 0,
    "pain_count": 0,
    "generation_time_seconds": 0,
    "skipped": false,
    "skip_reason": null
  }
}
```

Track downstream: when the seller sends the auto-generated materials, fire `roi_calculator_presented` with `auto_generated: true` to compare conversion rates of auto-generated vs manually built ROI materials.

### 7. Handle edge cases

- **Missing champion data:** Generate the ROI model but flag the business case as incomplete (no champion perspective). Alert seller to identify champion before sending.
- **Competitor mentioned in deal:** Include competitive positioning in the alternatives comparison section of the business case.
- **Very high ROI (>20x):** Flag for human review. Extremely high projections may indicate inflated pain data or missing cost factors. Add a warning note.
- **Generation failure:** If Claude API returns an error or invalid JSON, retry once. On second failure, alert the seller and log the error.

## Output

- Auto-generated ROI calculator (Google Sheet)
- Auto-generated business case (PDF)
- Both attached to the Attio deal record
- Seller notified via Slack with review link
- PostHog events tracking auto-generation volume and downstream effectiveness

## Triggers

Runs continuously as an n8n workflow. Fires on Attio deal stage changes and pain data updates. No manual intervention needed for the generation — seller reviews before sending.
