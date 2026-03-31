---
name: pricing-presentation-framework-smoke
description: >
  Pricing Presentation Framework — Smoke Test. Manually build and present
  value-anchored Good/Better/Best pricing proposals for 5 deals, track
  acceptance vs discount behavior, and validate that leading with quantified
  pain before revealing price improves acceptance rate.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=5 pricing presentations delivered in 1 week with >=60% accepted or advancing without significant discount (<=10%)"
kpis: ["Pricing acceptance rate", "Discount request frequency", "Value recap rate", "Tier match rate"]
slug: "pricing-presentation-framework"
install: "npx gtm-skills add sales/proposed/pricing-presentation-framework"
drills:
  - threshold-engine
---

# Pricing Presentation Framework — Smoke Test

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Prove that building prospect-specific Good/Better/Best pricing proposals anchored to their quantified pain data produces measurably better acceptance rates and lower discount requests than presenting pricing without value context. Target: present pricing to >=5 deals in 1 week with >=60% accepting or advancing to next stage without a discount exceeding 10%.

## Leading Indicators

- At least 5 deals in Proposed stage have `pain_count >= 2` and `pain_quantification_rate >= 0.5`
- ROI model generated for all 5 deals before pricing is presented
- Seller leads with pain recap before revealing price on at least 4 of 5 presentations
- At least 3 prospects engage with the recommended (Better) tier rather than defaulting to cheapest
- Discount requested on fewer than 40% of presentations
- At least 2 prospects advance to contract/close within 5 business days of pricing presentation

## Instructions

### 1. Identify 5 deals ready for pricing

Query Attio for deals in the Proposed stage with sufficient discovery data. Filter for:
- `pain_count >= 2` (at least 2 quantified pain points)
- `pain_quantification_rate >= 0.5` (at least half have dollar estimates)
- `roi_model_status` = "generated" (ROI calculator already built) OR sufficient pain data to generate one now

If fewer than 5 qualify, check deals approaching Proposed stage and ensure discovery is completed. You need 5 deals with real pain data and ROI models. Pricing without quantified value is guessing.

For each qualifying deal, pull from Attio:
- All quantified pains with dollar estimates and confidence levels
- ROI model (year 1 ROI, payback period, pain-to-price ratio)
- Champion name and role
- Company size, industry, and revenue estimate
- Competitive situation (any competitor mentions from discovery)
- Budget cycle / fiscal year end if known

### 2. Run the the pricing proposal assembly workflow (see instructions below) drill for each deal

For each of the 5 deals, execute the the pricing proposal assembly workflow (see instructions below) drill:

1. Validate pain-to-price ratio (>=5x strong, 3-5x moderate, <3x flag for more discovery)
2. Generate ROI model via `roi-model-generation` if not already present
3. Run `pricing-tier-generation` to produce Good/Better/Best tier structure with value anchoring, presentation order, and discount guardrails
4. Build the proposal artifact: one-page pricing comparison with value anchors per tier, ROI framing, and recommended tier highlighted
5. Store the proposal in Attio as a note on the deal record
6. Log `pricing_proposal_generated` in PostHog

Review each generated proposal. Check that value anchors reference real pains the prospect confirmed, not generic language. Adjust the anchoring script to sound natural in the seller's voice.

### 3. Present pricing with value-first framing

**Human action required:** Present pricing to each prospect following this structure:

1. **Recap pains** (2-3 minutes): "Based on our conversations, you mentioned [exact pain quote]. We estimated that costs your team approximately $X per year."
2. **Summarize ROI** (1 minute): "Our analysis shows a [ROI]% return in Year 1 with a [payback]-month payback period."
3. **Reveal tiers** (2-3 minutes): Present in the generated order (typically Best -> Good -> Better). For each tier: name, annual price, key features, value anchor sentence. Recommend Better as the optimal fit.
4. **Pause** (critical): After presenting all three tiers, stop talking. Wait for the prospect to respond. Do not preemptively discount, justify, or fill silence. The pause is where you learn what the prospect actually thinks.

After each presentation, log in Attio:
- `pricing_presentation_format` (live_call, email, in_person)
- `pricing_reaction` (positive, neutral, pushback, silence, asked_for_discount)
- `pricing_tier_selected` or discussed
- `pricing_discount_requested` (true/false)
- `pricing_discount_pct` (if given)

Fire PostHog events: `pricing_presented`, `pricing_reaction_logged`.

### 4. Handle discount requests without caving

If a prospect requests a discount, do NOT immediately concede. Follow the discount guardrails from the proposal:

1. Re-anchor to value: "Let me make sure the value makes sense first — you mentioned [pain] is costing $X/year. At [price], you're looking at [ROI]% return."
2. Offer alternatives before price cuts: restructure payment terms (quarterly vs annual), adjust tier (suggest Good tier instead), or bundle add-ons for perceived value.
3. If a discount is genuinely required (competitive pressure, budget constraint), keep it within the guardrails and log the reason.

Log every discount interaction: `pricing_discount_requested` with `discount_reason` and `pricing_discount_given` with actual percentage.

### 5. Evaluate against threshold

Run the `threshold-engine` drill at the end of 1 week. The threshold engine queries PostHog and Attio to check:
- Total pricing presentations delivered: must be >= 5
- Acceptance or advancement rate: must be >= 60% (accepted proposal OR advanced to next stage)
- Discount discipline: average discount given must be <= 10%

If PASS (>=5 presentations, >=60% acceptance, <=10% average discount): document which value anchoring approaches resonated most, which tier was most frequently selected, and whether the pain recap correlated with acceptance. Proceed to Baseline.

If FAIL: diagnose the failure mode:
- Low acceptance despite strong ROI: presentation framing may be off. Review whether value recap happened before pricing reveal.
- High discount requests: value story may not be landing. Check if pains referenced match what the prospect cares most about.
- Prospects choosing Good tier (cheapest): Better tier may not be differentiated enough or price gap is too large. Adjust tier structure.
- Prospects not engaging with tiers: the format may not work. Test email proposal vs live presentation.

## Time Estimate

- 1 hour: identifying qualifying deals and pulling data from Attio
- 4 hours: running pricing-proposal-assembly 5 times (validate pain, generate tiers, build artifact, review)
- 1.5 hours: delivering presentations and logging outcomes over the week
- 1.5 hours: threshold evaluation, pattern analysis, and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, pain data, pricing proposal storage | Standard stack (excluded from play budget) |
| PostHog | Event tracking for pricing presentations and outcomes | Standard stack (excluded from play budget) |
| Anthropic Claude API | Tier generation via `pricing-tier-generation` | ~$0.50-2 for 5 proposals at Sonnet 4.6 rates ($3/$15 per M tokens) — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Google Sheets / Docs | Proposal artifact formatting | Free with Google Workspace |

**Play-specific cost:** Free (Claude API cost negligible at this volume)

## Drills Referenced

- the pricing proposal assembly workflow (see instructions below) — builds a prospect-specific Good/Better/Best pricing proposal from pain data, generates tier structure with value anchoring, and creates the presentation artifact
- `threshold-engine` — evaluates pass/fail against the >=5 presentations / >=60% acceptance / <=10% discount target at week's end
