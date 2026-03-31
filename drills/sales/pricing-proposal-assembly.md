---
name: pricing-proposal-assembly
description: Assemble a complete pricing proposal from deal pain data — generate tier structure, value anchoring, and presentation script for a single deal
category: Sales
tools:
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - attio-deals
  - attio-notes
  - pain-quantification-prompt
  - roi-model-generation
  - pricing-tier-generation
  - posthog-custom-events
---

# Pricing Proposal Assembly

This drill takes a deal in the Proposed stage with quantified pain data and produces a complete pricing proposal: Good/Better/Best tier structure, value-anchored presentation script, discount guardrails, and a trackable proposal artifact. The seller reviews and presents -- no manual pricing construction required.

## Input

- Attio deal in Proposed stage with `pain_count >= 2` and `pain_quantification_rate >= 0.5`
- ROI model already generated (from `roi-calculator-build` drill) OR sufficient pain data to generate one inline
- Product pricing catalog accessible in `.gtm-config.json` or n8n environment variables

## Steps

### 1. Pull deal context from Attio

Query Attio for the deal record. Extract:
- All quantified pains with dollar estimates and confidence levels
- ROI model if present (`roi_year_1`, `roi_payback_months`, `roi_pain_to_price`)
- Champion name, title, and engagement level
- Economic buyer title
- Company size, industry, revenue estimate
- Competitive situation (any competitor mentions from discovery)
- Budget cycle / fiscal year end if known

If `roi_model_status != "generated"`, run `roi-model-generation` first using the pain data. A pricing presentation without ROI context is presenting blind.

### 2. Validate pain-to-price ratio

Check `pain_to_price_ratio`:
- **>= 5x**: Strong value story. Proceed with full confidence.
- **3-5x**: Moderate. Value anchoring must be precise — reference specific pains, not totals.
- **< 3x**: Weak. Flag for the seller: "Pain-to-price ratio is {ratio}x. Consider additional discovery before presenting pricing. Discounting will not fix a value gap."

If pain data quality is low (confidence = "low" on more than half of pains), re-run `pain-quantification-prompt` on each low-confidence pain with any additional context from recent conversations.

### 3. Generate tier structure

Run `pricing-tier-generation` with the validated deal context. This produces:
- Three tiers (Good/Better/Best) with pricing, features, and value anchoring per tier
- Recommended tier (default: Better)
- Presentation order (default: Best -> Good -> Better for contrast anchoring)
- Anchoring script (what to say live)
- Discount guardrails (max without approval, when acceptable, counter-moves)
- Multi-year upsell structure (if applicable)

### 4. Build the proposal artifact

Assemble the presentation materials:

**For live presentation (call or in-person):**
1. One-page pricing summary with 3 columns (Good/Better/Best)
2. Each column shows: tier name, annual price, key features, value anchor sentence, ROI at this tier
3. "Recommended" badge on Better tier
4. Footer: payment options (annual/quarterly) and multi-year savings if selected

**For email proposal:**
1. Opening paragraph: recap 2-3 key pains discovered (use their exact quotes)
2. ROI summary: "Based on our analysis, you're spending approximately $X/year on [pain]. Our solution delivers [ROI]% return in Year 1 with a [payback] month payback."
3. Pricing table with 3 tiers
4. Recommended tier with 1-sentence justification
5. Next step: specific calendar link or reply request

Store the proposal content in Attio as a note on the deal record.

### 5. Log the proposal creation

Update Attio deal:
- `pricing_proposal_status` = "generated"
- `pricing_tiers_presented` = number of tiers (3)
- `pricing_recommended_tier` = "Better" (or whichever)
- `pricing_recommended_annual` = dollar amount
- `pricing_discount_applied` = percentage

Fire PostHog event:
```json
{
  "event": "pricing_proposal_generated",
  "properties": {
    "deal_id": "...",
    "pain_to_price_ratio": 0,
    "roi_year_1": 0,
    "tiers_count": 3,
    "recommended_tier": "Better",
    "recommended_annual_price": 0,
    "discount_applied_pct": 0,
    "competitive_situation": "none|active_eval|incumbent",
    "generation_method": "manual|automated"
  }
}
```

### 6. Human review checkpoint

**Human action required:** Review the generated proposal before presenting. Check:
- Do the value anchors reference real pains the prospect confirmed?
- Is the recommended tier genuinely the best fit (not just the most expensive)?
- Are the discount guardrails realistic for this deal's competitive context?
- Does the anchoring script sound natural in the seller's voice?

Adjust tone and specifics. The generated content is a starting point optimized by data, but the seller owns the relationship.

## Output

- Complete tier structure with pricing, features, and value anchoring
- Presentation script or email proposal content
- Discount guardrails for this specific deal
- All content stored in Attio as a deal note
- PostHog event tracking the proposal generation

## Triggers

Run manually for each deal reaching Proposed stage with sufficient pain data. At Scalable level, triggered automatically by n8n when a deal enters Proposed with qualifying pain data.
