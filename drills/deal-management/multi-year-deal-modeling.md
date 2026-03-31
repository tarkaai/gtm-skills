---
name: multi-year-deal-modeling
description: Model multi-year deal structures for a specific prospect — generate term options, discount tiers, and a buyer-facing comparison document
category: Deal Management
tools:
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - attio-deals
  - attio-notes
  - deal-term-modeling
  - contract-comparison-generation
  - pain-quantification-prompt
  - posthog-custom-events
---

# Multi-Year Deal Modeling

This drill takes a deal in the Proposed stage and generates a set of multi-year contract options tailored to the prospect's profile. It produces both internal seller guidance (anchoring strategy, walk-away floor, concession playbook) and a buyer-facing comparison document the champion can circulate for budget approval.

## Input

- Deal record in Attio at Proposed stage with ACV, champion, and economic buyer identified
- Pain data from discovery (quantified pains with dollar estimates)
- Product pricing and packaging
- Knowledge of the prospect's budget cycle and competitive situation

## Steps

### 1. Pull deal context from Attio

Using `attio-deals`, retrieve the deal record. Extract:
- Current ACV or proposed annual price
- Champion name and role
- Economic buyer name and role
- Deal stage and expected close date
- Any competitive intelligence (who else they're evaluating)
- Budget cycle (fiscal year end, procurement deadlines)

Using `attio-notes`, pull discovery notes for pain data. If pain data is missing or `pain_to_price_ratio < 3`, run `pain-quantification-prompt` to estimate before proceeding. Multi-year deals require strong pain justification — a thin business case leads to discount-only negotiations.

### 2. Generate deal term options

Run `deal-term-modeling` with the deal context. This produces 3 ranked options:
- A high-anchor option (highest TCV, most incentives, longest term)
- A target option (the structure you most want the buyer to choose)
- A concession option (minimum acceptable terms if the buyer pushes back)

Review the output:
- Verify discount percentages are within your company's approved range
- Verify TCV calculations are correct
- Verify the anchoring strategy makes sense for this buyer's profile
- If the prospect has strong pain data (ratio > 10x), tighten discounts — they don't need a big incentive

Store the deal term options in Attio as a note on the deal record: "Multi-Year Options Generated" with the full JSON output.

### 3. Generate the buyer-facing comparison

Run `contract-comparison-generation` with the deal term options and prospect context. This produces a comparison document the champion can use internally.

Review the output:
- Is the tone buyer-centric (not vendor sales pitch)?
- Is the risk analysis honest?
- Is the recommendation appropriate for this buyer's situation?

### 4. Prepare the negotiation brief

Assemble the seller-side negotiation brief from the deal-term-modeling output:

```
## Negotiation Brief: {Company Name}

**Target outcome:** {target option name} — {term} years at ${annual_price}/yr (${tcv} TCV)
**Walk-away floor:** {min_term} years at ${min_annual_price}/yr (${min_tcv} TCV)

**Presentation order:** {order with reasoning}

**Concession ladder (give these in order if buyer pushes back):**
1. {First concession — smallest cost to you, highest perceived value to buyer}
2. {Second concession}
3. {Third concession — approaching floor}

**Anchoring notes:**
- Present {highest option} first to set the anchor
- Frame discounts as "rate protection" not "price cut"
- If buyer asks for monthly, show 3-year total cost comparison
- Never discount without getting something back (longer term, upfront payment, case study rights)

**Red flags that mean walk away:**
- Buyer won't commit to any term beyond annual
- Discount request exceeds {max_discount_pct}% without compensating commitment
- Decision maker is absent from negotiation conversations
```

Store this brief in Attio as a private note (not shared with prospect).

### 5. Track and measure

Fire PostHog events:
```json
{
  "event": "multi_year_deal_modeled",
  "properties": {
    "deal_id": "...",
    "current_acv": 24000,
    "target_tcv": 43200,
    "term_years_target": 2,
    "discount_pct_target": 10,
    "options_generated": 3,
    "pain_to_price_ratio": 12.5,
    "competitive_situation": "none|passive|active"
  }
}
```

## Output

- 3 ranked multi-year deal structure options with anchoring strategy
- Buyer-facing comparison document for the champion
- Seller-side negotiation brief with concession ladder and walk-away floor
- Deal record updated in Attio with all generated materials
- PostHog tracking event for pipeline analysis

## Triggers

Run manually when a deal reaches the Proposed stage and a multi-year conversation is appropriate. At Scalable+ levels, triggered automatically when a deal enters Proposed and the account's commitment readiness score is above threshold.
