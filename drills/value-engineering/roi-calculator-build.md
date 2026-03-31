---
name: roi-calculator-build
description: Build a prospect-specific ROI calculator from discovery pain data, present it, and capture validation
category: Value Engineering
tools:
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - attio-deals
  - attio-notes
  - roi-model-generation
  - pain-quantification-prompt
  - posthog-custom-events
---

# ROI Calculator Build

This drill takes quantified pain data from a discovery call and produces a prospect-specific ROI calculator. The calculator uses the prospect's own numbers, shows conservative/moderate/optimistic scenarios, and is designed to be shared with the prospect for validation and internal circulation.

## Input

- Deal record in Attio with completed pain extraction (from `pain-discovery-call` drill)
- At least 2 quantified pains with dollar estimates
- Product pricing and implementation cost
- Champion's name and role

## Steps

### 1. Validate readiness

Pull the deal record from Attio using `attio-deals`. Check:
- `pain_count >= 2` (need at least 2 value drivers for a credible ROI model)
- `pain_quantification_rate >= 0.5` (at least half the pains have dollar estimates)
- `pain_to_price_ratio >= 3` (if less than 3x, the ROI story is weak — recommend additional discovery)

If any check fails, return a recommendation to run another discovery call before building the calculator.

### 2. Re-quantify weak pains

For any pain where `confidence < 0.6`, re-run the `pain-quantification-prompt` fundamental with any additional context gathered since the original extraction (follow-up emails, second calls, enrichment data). Update the pain record in Attio with the revised estimate.

### 3. Generate the ROI model

Run `roi-model-generation` with the deal's pain data, product pricing, and prospect enrichment data. This produces:
- Model inputs (each marked as adjustable or fixed)
- Assumptions with cited sources
- Annual savings breakdown by value driver (3-year horizon)
- Annual costs (license + implementation + training)
- Summary: ROI percentage, payback period, pain-to-price ratio
- Sensitivity analysis: conservative/moderate/optimistic scenarios

### 4. Build the calculator artifact

Format the ROI model into a shareable artifact. Options:
- **Google Sheet** (recommended for self-service): Create a spreadsheet with an Inputs tab (prospect adjusts their numbers), Calculations tab (formulas auto-update), and Summary tab (visual ROI output). Use the Google Sheets API to create and populate programmatically.
- **PDF business case**: Run the `pain-based-business-case` drill to produce a champion-ready document.
- **Interactive web page**: If you have a hosted ROI calculator, pre-populate it with the prospect's inputs and generate a unique shareable link.

Whichever format, ensure the prospect can adjust inputs and see ROI change in real time. This builds trust — they see their own numbers, not yours.

### 5. Present the ROI

**Human action required:** Present the ROI calculator to the prospect. Recommended framing:

1. Anchor to their pain first: "Based on our conversation, you mentioned [quote from discovery]. Here's what that costs you annually."
2. Show the savings: "If we solve [pain], here's the projected impact using your numbers."
3. Reveal the ROI: "At [price], you're looking at [X]x return in year 1 with payback in [Y] months."
4. Invite validation: "These are based on what you told me — please adjust any inputs that don't feel right."

Send the calculator to the prospect after the presentation. Track when they open it.

### 6. Capture validation

After presenting, update Attio:
```json
{
  "roi_presented": true,
  "roi_presented_date": "2026-03-30",
  "roi_prospect_validated": true|false,
  "roi_prospect_adjustments": "Description of any input changes the prospect made",
  "roi_final_value": 0,
  "roi_final_payback_months": 0,
  "roi_referenced_in_decision": false
}
```

Fire PostHog events:
```json
{
  "event": "roi_calculator_presented",
  "properties": {
    "deal_id": "...",
    "roi_percentage": 0,
    "payback_months": 0,
    "pain_to_price_ratio": 0,
    "pain_count": 0,
    "format": "spreadsheet|pdf|web"
  }
}
```

When the prospect validates or adjusts:
```json
{
  "event": "roi_calculator_validated",
  "properties": {
    "deal_id": "...",
    "prospect_adjusted": true|false,
    "original_roi": 0,
    "adjusted_roi": 0,
    "adjustment_direction": "up|down|unchanged"
  }
}
```

### 7. Track ROI influence on deal progression

Set a reminder for 7 days post-presentation. Check:
- Did the prospect reference ROI in subsequent conversations?
- Did the deal advance to the next stage within 7 days of ROI presentation?
- Did the prospect share the calculator internally (track forwarding if using a hosted link)?

Log `roi_referenced_in_decision = true` in Attio if ROI was cited in any buying decision conversation.

## Output

- Prospect-specific ROI calculator (spreadsheet, PDF, or web link)
- Deal record updated with ROI metrics and validation status
- PostHog events for pipeline analysis of ROI effectiveness
- Tracking of whether ROI influenced the buying decision

## Triggers

Run manually after discovery call produces >= 2 quantified pains. At Scalable+ levels, triggered automatically when deal pain data meets readiness thresholds.
