---
name: roi-calculator-baseline
description: >
  ROI Calculator & Business Case — Baseline Run. Scale ROI calculator delivery
  to 15-20 deals with automated business case generation, structured event
  tracking, and measurement of ROI impact on deal velocity and close rates.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email, Website"
level: "Baseline Run"
time: "24 hours over 2 weeks"
outcome: ">=70% of prospects with >=5x ROI and >=40% faster close time for strong-ROI deals over 2 weeks"
kpis: ["ROI distribution", "Deal velocity by ROI tier", "Close rate by ROI tier", "Business case conversion rate"]
slug: "roi-calculator"
install: "npx gtm-skills add sales/proposed/roi-calculator"
drills:
  - roi-calculator-build
  - pain-based-business-case
  - posthog-gtm-events
  - threshold-engine
---

# ROI Calculator & Business Case — Baseline Run

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email, Website

## Outcomes

Scale ROI calculator delivery to 15-20 deals over 2 weeks. Add automated business case generation for high-value deals. Prove that strong ROI (>=5x) measurably accelerates deal velocity: prospects with strong ROI close >=40% faster than those with weak ROI (<3x). Target: >=70% of prospects achieve >=5x ROI, and strong-ROI deals close >=40% faster.

## Leading Indicators

- ROI calculator completed within 48 hours of discovery for all deals entering Proposed stage
- Business case auto-generated for every deal with pain-to-price ratio >=5x
- Prospect calculator engagement rate >=50% (opened and viewed within 3 business days)
- Champion-ready business cases reviewed and sent within 24 hours of generation
- At least 10 deals have complete ROI tracking data (calculator presented, validated, outcome logged)

## Instructions

### 1. Configure comprehensive event tracking

Run the `posthog-gtm-events` drill to set up the ROI calculator event taxonomy:

- `roi_model_generated` — fired when `roi-model-generation` fundamental completes (properties: deal_id, roi_percentage, payback_months, pain_count)
- `roi_calculator_presented` — fired when calculator is shared with prospect (properties: deal_id, format, roi_percentage, pain_to_price_ratio)
- `roi_calculator_validated` — fired when prospect adjusts or confirms inputs (properties: deal_id, adjusted, original_roi, adjusted_roi)
- `roi_referenced_in_decision` — fired when prospect cites ROI in a buying conversation (properties: deal_id, context)
- `business_case_generated` — fired when business case document is produced (properties: deal_id, roi_percentage, pain_count)
- `business_case_sent` — fired when business case is delivered to prospect (properties: deal_id, delivery_method)
- `deal_closed_won` / `deal_closed_lost` — fired at deal conclusion (properties: deal_id, had_roi_calculator, roi_tier)

Build a PostHog funnel: `roi_model_generated` -> `roi_calculator_presented` -> `roi_calculator_validated` -> `roi_referenced_in_decision` -> `deal_closed_won`

### 2. Run ROI calculator builds at scale

For every deal entering the Proposed stage over 2 weeks, run the `roi-calculator-build` drill:

1. Validate pain data readiness
2. Re-quantify weak pains
3. Generate the ROI model
4. Build the calculator artifact (Google Sheet)
5. **Human action required:** Present and send the calculator
6. Capture validation and engagement

Target: 15-20 calculators built and presented over 2 weeks. Track the time from discovery completion to calculator delivery — aim for < 48 hours.

### 3. Generate business cases for high-value deals

For every deal where `pain_to_price_ratio >= 5` and the deal value exceeds your median ACV, run the `pain-based-business-case` drill. This generates a champion-ready document that:
- Uses the prospect's own pain quotes and numbers
- Shows the ROI analysis from the calculator in a narrative format
- Includes risk analysis with mitigations
- Compares alternatives (status quo, competitors)
- Ends with a clear recommendation and next steps

**Human action required:** Review each business case for accuracy before sending. The document should read like the champion wrote it, not like a vendor pitch. Check that pain quotes are accurate, cost estimates are defensible, and the ROI matches the calculator output.

Attach the business case to the calculator delivery: "Here's the ROI calculator with your numbers, and a summary document you can share with your team."

### 4. Segment deals by ROI tier

As calculators are completed, segment deals in Attio:
- **Strong ROI (>=5x):** High priority. These deals should close. If they stall, the problem is not value — investigate champion strength, authority access, or timing.
- **Moderate ROI (3-5x):** Viable but need reinforcement. Look for additional value drivers not yet quantified. Consider running a second discovery call targeting revenue impact or risk mitigation.
- **Weak ROI (<3x):** Red flag. Either discovery missed significant pain, or this prospect is not a good fit. Consider disqualifying rather than discounting — low ROI deals that close become high churn risk.

### 5. Measure ROI impact on deal velocity

At the end of 2 weeks, pull from PostHog and Attio:
- Average days from Proposed to Close for strong-ROI deals (>=5x)
- Average days from Proposed to Close for weak-ROI deals (<3x)
- Calculate the velocity difference: `(weak_days - strong_days) / weak_days * 100`
- Close rate for strong-ROI vs weak-ROI deals
- Business case engagement rate (opened / sent)
- Calculator validation rate (prospect adjusted or confirmed / presented)

Run the `threshold-engine` drill. Pass criteria: >=70% of deals have >=5x ROI AND strong-ROI deals close >=40% faster than weak-ROI deals.

If PASS: the ROI calculator is a proven deal accelerator. Document which value drivers produce the strongest ROI (time savings vs cost reduction vs revenue increase vs risk mitigation). Proceed to Scalable.

If FAIL: diagnose the bottleneck:
- Low ROI percentage (<70% at >=5x): discovery quality is inconsistent. Standardize discovery questions around the strongest value drivers from Smoke.
- No velocity difference: ROI is not reaching the decision-maker. Test different delivery methods: present to economic buyer directly, embed ROI in the proposal document, or have the champion present the business case.
- Low engagement (prospects not opening calculators): simplify the format. Test a one-page ROI summary email vs the full spreadsheet.

## Time Estimate

- 4 hours: configuring PostHog events and building the tracking funnel
- 10 hours: running roi-calculator-build on 15-20 deals (faster with practice from Smoke)
- 4 hours: generating and reviewing business cases for high-value deals
- 3 hours: monitoring engagement and logging outcomes
- 3 hours: measurement, analysis, segmentation, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, pain data, ROI logging, segmentation | Standard stack (excluded) |
| PostHog | Event tracking, funnels, ROI tier analysis | Standard stack (excluded) |
| n8n | Workflow orchestration for event routing | Standard stack (excluded) |
| Anthropic Claude API | ROI model generation + business case generation | ~$5-15/mo at 15-20 deals — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Google Sheets | Calculator artifact delivery | Free with Google Workspace |
| Loom (optional) | Video walkthrough of calculator for remote presentations | Free (5 min limit) or Business $12.50/mo — [pricing](https://www.loom.com/pricing) |

**Play-specific cost:** ~$5-15/mo (Claude API only; Google Sheets is free)

## Drills Referenced

- `roi-calculator-build` — builds prospect-specific ROI calculators from pain data, generates the model, creates artifacts, captures validation
- `pain-based-business-case` — generates champion-ready business case documents for high-value deals using prospect pain data and ROI analysis
- `posthog-gtm-events` — configures the full event tracking pipeline for the ROI calculator play
- `threshold-engine` — evaluates pass/fail against the >=70% strong ROI / >=40% velocity improvement target
