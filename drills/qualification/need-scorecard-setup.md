---
name: need-scorecard-setup
description: Configure a need assessment scoring system in your CRM with need categories, severity scales, and qualification thresholds
category: Qualification
tools:
  - Attio
  - PostHog
fundamentals:
  - attio-custom-attributes
  - attio-pipeline-config
  - attio-deals
  - posthog-custom-events
---

# Need Scorecard Setup

This drill creates the infrastructure for structured need assessment in your CRM. It defines business need categories specific to your product, creates scoring fields for each, and configures pipeline stages that map to need-based qualification outcomes.

## Input

- Your ICP definition (output from `icp-definition` drill)
- A list of 5-7 critical business needs your product addresses
- Access to Attio with admin permissions
- PostHog project for tracking need assessment events

## Steps

### 1. Define need categories

Work with the founder to define 5-7 business need categories your product solves. Each category should be:
- Specific enough to score on a call ("reducing manual data entry" not "efficiency")
- Tied to a measurable business outcome ("accelerating deal velocity" not "being better at sales")
- Relevant to your ICP segments

Example categories for a workflow automation product:
1. Reducing manual data entry
2. Improving data accuracy
3. Accelerating workflows
4. Eliminating cross-tool friction
5. Reducing operational cost
6. Improving reporting visibility
7. Scaling without headcount

Store the categories as a JSON array in Attio's campaign notes for reference by other drills.

### 2. Create need assessment custom attributes in Attio

Using the `attio-custom-attributes` fundamental, create the following fields on the Deals object:

**Per-category score fields (number, 1-3):**
- `need_cat_1_score` through `need_cat_7_score` (one per defined category)
- Each uses a 3-point scale: Critical (3), Moderate (2), Low (1), Not Assessed (0)

**Aggregate fields:**
- `need_total_score` (number, 0-21) — sum of all category scores
- `need_critical_count` (number) — count of categories scored 3
- `need_tier` (select) — High Need (score >=15, >=2 Critical), Medium Need (12-14), Low Need (<12)

**Status fields:**
- `need_strongest_category` (text) — which need resonated most
- `need_weakest_category` (text) — lowest-scoring need explored
- `need_assessment_source` (select) — Pre-call Hypothesis, Discovery Call, Follow-up Call, Re-assessment
- `need_last_assessed` (date) — when the need score was last updated
- `need_notes` (text) — freeform notes on need gaps and product fit

**Qualification verdict:**
- `need_verdict` (select) — Qualified (meets minimum threshold), Nurture (close to threshold), Disqualified (well below)

### 3. Define qualification thresholds

Document the scoring rubric:

- **Minimum viable need threshold:** Total score >=12 with at least 2 Critical (severity 3) needs
- **High need:** Total score >=15 — fast-track to demo/proposal
- **Medium need:** Total score 12-14 — qualified but may need nurturing on urgency
- **Low need:** Total score <12 — disqualify from active pipeline, route to content nurture

These thresholds should be calibrated after Smoke test data is collected.

### 4. Configure pipeline stages for need assessment

Using the `attio-pipeline-config` fundamental, ensure your deal pipeline includes:

1. **New Lead** — just entered, not yet assessed
2. **Need Hypothesized** — pre-call need hypothesis generated from enrichment data
3. **Discovery Scheduled** — call booked to validate need hypothesis
4. **Need Assessed** — discovery call complete, scores assigned
5. **Need Qualified** — total score >=12, >=2 Critical needs
6. **Need Disqualified** — total score <12, moved to nurture

### 5. Set up PostHog tracking events

Using the `posthog-custom-events` fundamental, create events:

- `need_assessment_created` — first need assessment on a deal (properties: deal_id, total_score, tier, source)
- `need_assessment_updated` — subsequent re-scoring (properties: deal_id, old_score, new_score, changed_categories)
- `need_qualified` — deal crosses the 12-point threshold with >=2 Critical
- `need_disqualified` — deal scored below threshold
- `critical_need_identified` — a single need scored Critical (properties: deal_id, category, severity)

### 6. Validate the setup

Create a test deal in Attio. Set need scores: cat_1=3, cat_2=2, cat_3=3, cat_4=1, cat_5=2, cat_6=3, cat_7=1. Verify:
- Total score calculates correctly: 3+2+3+1+2+3+1 = 15
- Critical count = 3 (cat_1, cat_3, cat_6)
- Tier = "High Need" (15 >= 15)
- Verdict = "Qualified" (15 >= 12 and 3 >= 2 Critical)
- PostHog receives the `need_assessment_created` event
- Deal moves to "Need Qualified" stage

Delete the test deal after validation.

## Output

- Attio Deals object with need assessment custom attributes (14+ fields)
- Pipeline stages mapped to need qualification outcomes
- PostHog events configured for tracking need assessment funnel
- Need categories documented and stored in Attio campaign notes
- Scoring rubric and qualification thresholds defined

## Triggers

Run once during setup. Re-run if you change your product's value propositions or add/remove need categories.
