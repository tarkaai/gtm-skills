---
name: business-case-assembly
description: End-to-end workflow to build a champion-ready business case from discovery pain data, ROI model, strategic alignment, and risk mitigation
category: Value Engineering
tools:
  - Attio
  - Anthropic
  - PostHog
  - Clay
fundamentals:
  - attio-deals
  - attio-notes
  - attio-custom-attributes
  - call-transcript-pain-extraction
  - pain-quantification-prompt
  - roi-model-generation
  - business-case-generation
  - strategic-alignment-mapping
  - risk-mitigation-matching
  - roi-narrative-generation
  - stakeholder-role-classification
  - posthog-custom-events
---

# Business Case Assembly

This drill orchestrates the full business case creation workflow: extract pain from discovery transcripts, quantify the dollar impact, generate an ROI model, map strategic alignment to the prospect's initiatives, match risks to mitigation assets, and produce a champion-ready business case document with persona-specific executive narratives.

Unlike `pain-based-business-case` (which focuses on pain-to-case conversion), this drill adds strategic alignment mapping, stakeholder-specific narratives, and risk mitigation matching to produce a more comprehensive business case suitable for enterprise approval chains.

## Input

- Deal record in Attio at stage >= Aligned
- At least 1 discovery call transcript (from Fireflies or Gong)
- Product pricing and value proposition
- Optional: known strategic initiatives for the prospect company

## Steps

### 1. Extract and quantify pain

Pull the deal record from Attio using `attio-deals`. Check if pain data already exists:
- If `pain_count >= 2` and `pain_quantification_rate >= 0.5`: proceed to step 2
- If pain data is missing or insufficient: run `call-transcript-pain-extraction` on the latest transcript, then run `pain-quantification-prompt` on each extracted pain to estimate dollar impact

Validation gate: the deal must have `pain_to_price_ratio >= 3` before proceeding. If ratio < 3, return a recommendation for additional discovery rather than generating a weak business case.

### 2. Map the buying committee

Run `stakeholder-role-classification` on all known contacts at the account:
- Identify the Economic Buyer (who signs the check)
- Identify the Champion (who will carry the business case internally)
- Identify potential Blockers (security, legal, procurement)

Store classifications in Attio. If no Economic Buyer is identified, flag the deal as at risk and recommend discovery to find the budget holder before building the business case.

### 3. Map strategic alignment

Run `strategic-alignment-mapping` with the prospect's known strategic initiatives and your product value propositions. This produces:
- Initiative-to-value-prop mappings with alignment strength
- Executive narratives per initiative
- An overall alignment score

Store the alignment data in Attio. Strong alignments (score >= 0.6) feed into the strategic framing section of the business case.

### 4. Generate the ROI model

Run `roi-model-generation` with the validated pain data, product pricing, and company enrichment data. This produces:
- Structured inputs and assumptions
- 3-year savings breakdown by value driver
- Summary: ROI percentage, payback period, pain-to-price ratio
- Sensitivity analysis (conservative/moderate/optimistic)

Validate mathematical consistency. Store the model in Attio.

### 5. Generate executive-specific ROI narratives

For each identified executive stakeholder (Economic Buyer, key Influencers), run `roi-narrative-generation` with:
- The executive's role and known priorities
- The ROI model output
- The strategic alignment mappings

This produces persona-specific narratives: CFO gets payback period and NPV framing, CEO gets strategic positioning, CTO gets technical efficiency framing.

### 6. Match risks to mitigation assets

Pull risks from the deal record (from `call-transcript-risk-extraction` if available). Run `risk-mitigation-matching` against your content library:
- Match each identified risk to the best case study, security doc, or reference
- Identify content gaps where no good mitigation asset exists
- Generate delivery messages for the top mitigations

If no explicit risks are recorded, use `hypothesis-generation` to predict likely executive objections based on industry, company size, and deal size.

### 7. Assemble the business case

Run `business-case-generation` with all assembled inputs:
- Pain data with prospect quotes
- ROI model with sensitivity analysis
- Strategic alignment narratives
- Risk analysis with matched mitigations
- Executive-specific framing for the primary audience

The output is a structured business case document: executive summary, current state costs, proposed solution, financial analysis, strategic alignment, risk mitigation, alternatives comparison, and recommendation.

### 8. Human review checkpoint

**Human action required:** Review the generated business case. Verify:
- Prospect quotes are accurate and in context
- Financial estimates are defensible
- Strategic alignment claims are grounded in real initiative data
- The tone reads as champion-authored, not vendor-authored

### 9. Deliver and track

Deliver the business case to the champion via email or document sharing. Update Attio:
- `business_case_status` = "sent"
- `business_case_date` = today
- `business_case_roi` = calculated ROI percentage
- `business_case_alignment_score` = strategic alignment score

Fire PostHog event:
```json
{
  "event": "business_case_assembled",
  "properties": {
    "deal_id": "...",
    "pain_count": 0,
    "total_quantified_pain": 0,
    "roi_percentage": 0,
    "payback_months": 0,
    "alignment_score": 0.0,
    "risk_mitigations_matched": 0,
    "exec_narratives_generated": 0,
    "assembly_method": "manual|semi-auto|full-auto"
  }
}
```

Set a follow-up reminder for 5 business days.

## Output

- Champion-ready business case document with ROI, strategic alignment, and risk mitigation
- Executive-specific ROI narratives for each stakeholder
- Deal record updated with business case metrics
- PostHog events for pipeline analysis
- Follow-up reminder set

## Triggers

Run when a deal at Aligned stage has `pain_count >= 2` and the prospect needs internal approval. At Scalable+ levels, triggered automatically by `roi-auto-generation` drill.
