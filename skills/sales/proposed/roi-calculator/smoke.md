---
name: roi-calculator-smoke
description: >
  ROI Calculator & Business Case — Smoke Test. Manually build ROI calculators
  for 5 prospects using discovery pain data, present the calculators, and
  validate that strong ROI (>=5x) correlates with deal advancement.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email, Website"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: ">=5 prospects with >=5x ROI calculated and >=3 reference ROI in decisions within 1 week"
kpis: ["ROI value distribution", "Payback period", "ROI validation rate", "ROI impact on deal velocity"]
slug: "roi-calculator"
install: "npx gtm-skills add sales/proposed/roi-calculator"
drills:
  - roi-calculator-build
  - threshold-engine
---

# ROI Calculator & Business Case — Smoke Test

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email, Website

## Outcomes

Prove that building prospect-specific ROI calculators using their own pain data produces measurably stronger deal progression than presenting pricing without quantified value. Target: build ROI calculators for >=5 prospects showing >=5x ROI, and >=3 prospects cite ROI in their buying decision conversations.

## Leading Indicators

- Pain data sufficient for ROI modeling (>=2 quantified pains) on at least 5 deals in Proposed stage
- ROI calculator completed and shared within 48 hours of discovery for all 5 prospects
- Prospect validates or adjusts calculator inputs (engagement signal) for at least 3 of 5
- Payback period < 6 months on at least 4 of 5 calculators
- At least 2 prospects forward the calculator internally within 5 business days

## Instructions

### 1. Identify 5 deals with sufficient pain data

Query Attio for deals in the Proposed stage that have completed pain discovery. Filter for deals where:
- `pain_count >= 2` (at least 2 quantified pain points)
- `pain_quantification_rate >= 0.5` (at least half have dollar estimates)
- `roi_model_status` is null or "not_started"

If fewer than 5 qualify, check deals approaching Proposed stage and fast-track their pain discovery. You need 5 deals with real pain data to run this test.

For each qualifying deal, pull from Attio:
- All quantified pains with dollar estimates and confidence levels
- Champion name and role
- Company size, industry, and revenue estimate
- Product pricing applicable to this deal
- Any competitor mentions from discovery

### 2. Run the `roi-calculator-build` drill for each deal

For each of the 5 deals, execute the `roi-calculator-build` drill:

1. Validate pain data readiness (pain count, quantification rate, pain-to-price ratio)
2. Re-quantify any low-confidence pains using `pain-quantification-prompt`
3. Generate the structured ROI model via `roi-model-generation` — this produces inputs, assumptions, savings breakdown, costs, summary with ROI percentage and payback period, and sensitivity analysis (conservative/moderate/optimistic)
4. Build the calculator artifact: a Google Sheet with adjustable inputs so the prospect can modify their own numbers and watch the ROI recalculate
5. **Human action required:** Present the calculator to the prospect. Lead with their pain ("You mentioned [quote] — here's what that costs you annually"), show the savings, reveal the ROI, and invite them to adjust any inputs
6. Send the calculator to the prospect after presenting
7. Log ROI metrics and validation status in Attio

Do NOT present a generic ROI. Every calculator must use the prospect's own numbers from discovery. If you don't have their numbers, you don't have enough discovery data — go back and get it.

### 3. Track engagement and influence

For each of the 5 deals, monitor over the following 7 days:
- Did the prospect open the calculator? (Track via Google Sheet view history or hosted link analytics)
- Did the prospect adjust any inputs? (Check Sheet edit history)
- Did the prospect reference ROI in any subsequent conversation? (Log in Attio: `roi_referenced_in_decision = true`)
- Did the deal advance to the next stage within 7 days of ROI presentation?
- Did the prospect share the calculator internally? (Check Sheet sharing or forwarding analytics)

Fire PostHog events for each interaction: `roi_calculator_presented`, `roi_calculator_validated`, `roi_referenced_in_decision`.

### 4. Evaluate against threshold

Run the `threshold-engine` drill at the end of 1 week. The threshold engine queries PostHog and Attio to check:
- Total ROI calculators built and presented: must be >= 5
- Calculators showing >= 5x ROI: must be >= 5
- Prospects who referenced ROI in decision conversations: must be >= 3

If PASS (>=5 with >=5x ROI, >=3 referencing ROI): document which value drivers produced the strongest ROI, which presentation framing resonated most, and whether validated vs unvalidated calculators correlated with deal advancement. Proceed to Baseline.

If FAIL: diagnose the failure mode:
- Weak ROI (<5x on most deals): discovery is not uncovering enough pain. Improve discovery questions targeting time savings, cost reduction, and revenue impact.
- Strong ROI but not referenced: the calculator may not be reaching the economic buyer. Ask champions how budget decisions are made and adjust delivery.
- Low engagement (prospect didn't open/adjust): the format or framing may be wrong. Test a simpler one-page summary vs the full spreadsheet.

## Time Estimate

- 1 hour: identifying qualifying deals and pulling pain data from Attio
- 3 hours: running roi-calculator-build 5 times (validate pain, generate model, build artifact, present)
- 1.5 hours: tracking engagement and logging outcomes over the week
- 1.5 hours: threshold evaluation, analysis, and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, pain data, ROI logging | Standard stack (excluded from play budget) |
| PostHog | Event tracking for calculator engagement | Standard stack (excluded from play budget) |
| Anthropic Claude API | ROI model generation via `roi-model-generation` | ~$0.50-2 for 5 models at Sonnet 4.6 rates ($3/$15 per M tokens) — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Google Sheets | Calculator artifact delivery | Free with Google Workspace |

**Play-specific cost:** Free (Claude API cost negligible at this volume)

## Drills Referenced

- `roi-calculator-build` — builds a prospect-specific ROI calculator from pain data, generates the model, creates the shareable artifact, and captures validation
- `threshold-engine` — evaluates pass/fail against the >=5 calculators / >=3 referenced target at week's end
