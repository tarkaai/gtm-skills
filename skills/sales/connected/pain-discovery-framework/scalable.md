---
name: pain-discovery-framework-scalable
description: >
  Pain Discovery Framework — Scalable Automation. Analyze pain patterns across all prospects
  to optimize discovery questions, auto-generate business cases from quantified pains, and
  A/B test question strategies to maximize pain-to-price ratios at volume.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=70% of prospects with quantified pains >=10x cost and >=30% faster deal velocity over 2 months"
kpis: ["Pain quantification rate", "Pain-to-price ratio", "AI extraction accuracy", "Business case conversion rate"]
slug: "pain-discovery-framework"
install: "npx gtm-skills add sales/connected/pain-discovery-framework"
drills:
  - pain-pattern-analysis
  - pain-based-business-case
  - ab-test-orchestrator
---

# Pain Discovery Framework — Scalable Automation

> **Stage:** Sales > Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Find the 10x multiplier for pain discovery. Analyze pain data across all prospects to identify which questions surface the highest-value pains, which segments have the most quantifiable pain, and which business case formats convert best. Auto-generate business cases from discovery data. A/B test question strategies to continuously improve.

Target: >= 70% of prospects with quantified pains >= 10x product cost, and >= 30% faster deal velocity for pain-discovered deals vs. pipeline average.

## Leading Indicators

- Cross-prospect pain pattern report surfacing actionable ICP refinements
- Question bank performance rankings differentiating effective from weak questions
- Business cases auto-generated within 24 hours of discovery calls
- A/B test producing a statistically significant winner on pain-to-price ratio
- Pain-discovered deals moving to proposal stage 30%+ faster than non-discovery deals

## Instructions

### 1. Run cross-prospect pain pattern analysis

With 10+ calls of pain data accumulated from Baseline, run the `pain-pattern-analysis` drill. This drill:

- Extracts all pain data from Attio across completed discovery calls
- Builds a pain frequency matrix (which pains appear most, by category and segment)
- Segments pain profiles by industry, company size, and funding stage
- Correlates pain types with deal outcomes (won, lost, open)
- Evaluates question effectiveness (which questions surface the highest-value pains)
- Generates an intelligence report with ICP refinements and question bank updates

**Act on the output:**
- Update your ICP definition to prioritize segments with highest average pain-to-price ratio
- Retire discovery questions with surface_rate < 0.1
- Add new questions targeting gaps the analysis identified
- Brief the sales team on which pain categories correlate most strongly with wins

Schedule this drill to run bi-weekly via n8n.

### 2. Deploy automated business case generation

Configure the `pain-based-business-case` drill to trigger automatically when a deal meets these criteria:
- `pain_to_price_ratio >= 10`
- `pain_quantification_rate >= 0.7`
- `pain_count >= 3`

The drill:
- Validates the deal has sufficient pain data
- Re-quantifies any low-confidence pains with additional enrichment
- Generates a buyer-ready business case using the prospect's own quotes
- Formats it for champion delivery (written from the buyer's perspective, not yours)

**Human action required:** Review every auto-generated business case before sending. The AI gets the structure right, but you need to verify quotes are in context and estimates are defensible. Target: review time < 15 minutes per case.

Set up an n8n workflow that:
1. Monitors Attio for deals meeting the trigger criteria
2. Runs the business case generation drill
3. Sends a Slack notification: "Business case ready for review: {company_name} — ${total_pain} pain, {roi}% ROI"
4. After human approval, delivers the business case to the champion

### 3. A/B test discovery question strategies

Run the `ab-test-orchestrator` drill to test question approaches. Set up experiments:

**Experiment 1: Question ordering**
- Control: Lead with operational pain questions, then financial
- Variant: Lead with strategic/urgency questions, then operational
- Metric: Average pain-to-price ratio per call
- Sample: 20 calls per variant (minimum)

**Experiment 2: Quantification technique**
- Control: Ask "what does that cost you?" directly
- Variant: Use anchoring — "Companies your size typically see $X impact from this — does that sound right?"
- Metric: Quantification rate (% of pains with dollar estimates)
- Sample: 15 calls per variant

**Experiment 3: Discovery depth vs. breadth**
- Control: Explore 5+ pains to moderate depth
- Variant: Deep-dive on top 2-3 pains to full quantification
- Metric: Business case conversion rate (business cases that advance the deal)
- Sample: 20 calls per variant

Use PostHog feature flags to randomly assign each discovery call to a variant. Log the variant in the call's PostHog event properties. Run each experiment for its minimum sample before evaluating.

### 4. Scale call volume with maintained quality

Increase discovery calls to 15-25 per month. The automated pipeline handles:
- Pre-call prep (Clay enrichment + question generation) — runs automatically 24h before each call
- Post-call extraction (transcription + pain extraction + quantification) — runs automatically after each call
- Business case generation — triggers automatically when criteria met
- Pattern analysis — runs bi-weekly

Your manual involvement per call drops to:
- 10 min: review call prep
- 45 min: conduct the call
- 10 min: review extracted pain data and correct errors
- 15 min: review auto-generated business case (when triggered)

### 5. Build the pain-pipeline dashboard

Create a PostHog dashboard connecting pain discovery to pipeline outcomes:

- **Pain-to-Win correlation:** Scatter plot of pain-to-price ratio vs. win probability
- **Segment performance:** Table showing avg pain-to-price ratio by industry/size segment
- **Question effectiveness:** Ranked list of questions by surface_rate * win_correlation
- **Business case impact:** Win rate for deals with business case vs. without
- **Deal velocity:** Average days from discovery call to close, segmented by pain quality tier
- **A/B test results:** Current experiment status and preliminary results

### 6. Evaluate against threshold

After 2 months, measure:
- What % of prospects have quantified pains >= 10x cost? (Target: >= 70%)
- Is deal velocity >= 30% faster for pain-discovered deals? (Compare to pipeline average)
- What is the business case conversion rate? (Business cases that advance deals)
- What is the AI extraction accuracy after corrections? (Target: >= 85%)

If **PASS**: The pattern analysis and automated business cases are multiplying your effectiveness. Proceed to Durable for autonomous optimization.

If **FAIL**: Focus on the weakest metric:
- Low pain-to-price: Run more question experiments; tighten ICP to higher-pain segments
- Slow deal velocity: Investigate whether business cases are reaching the right stakeholders
- Low business case conversion: Review the generation prompt; test different formats
- Low AI accuracy: Expand the extraction training data with more corrected examples

## Time Estimate

- Pattern analysis setup + first run: 4 hours
- Business case automation setup: 6 hours
- A/B test design and setup: 4 hours
- 50 discovery calls (60 min total per call incl review): 50 hours
- Bi-weekly pattern analysis review (4 x 1 hr): 4 hours
- Threshold evaluation: 2 hours
- **Total: ~70 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, pain data, automated triggers | Plus $29/user/mo; Pro $59/user/mo for advanced automation |
| Fireflies | Auto-transcribe all discovery calls | Business $19/user/mo (API access) |
| Claude API (Anthropic) | Pain extraction + quantification + business case generation | Sonnet: $3/$15 per M tokens; ~$0.50-1.00 per call (extraction + business case) |
| PostHog | Analytics, funnels, feature flags, experiments | Free tier or usage-based (~$0.00005/event) |
| n8n | Workflow automation (extraction pipeline, business case triggers, scheduling) | Pro $60/mo |
| Cal.com | Discovery call scheduling | Free or Teams $15/user/mo |
| Clay | Prospect enrichment for call prep at scale | Launch $185/mo or Growth $495/mo |

**Estimated play-specific cost at Scalable:** ~$200-400/mo (Fireflies Business + n8n Pro + Clay Launch + Claude API at volume)

## Drills Referenced

- `pain-pattern-analysis` — Aggregate pain data across prospects; identify patterns, question effectiveness, ICP refinements
- `pain-based-business-case` — Auto-generate buyer-ready business cases from quantified discovery data
- `ab-test-orchestrator` — Design, run, and evaluate A/B tests on discovery question strategies
