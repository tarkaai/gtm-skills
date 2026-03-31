---
name: bant-scorecard-setup
description: Configure a BANT scoring system in your CRM with custom fields, scoring rubrics, and qualification thresholds
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

# BANT Scorecard Setup

This drill creates the infrastructure for structured BANT qualification in your CRM. It sets up custom fields for each BANT dimension, defines scoring rubrics, and configures the pipeline stages that map to qualification outcomes.

## Input

- Your ICP definition (output from `icp-definition` drill)
- Access to Attio with admin permissions
- PostHog project for tracking qualification events

## Steps

### 1. Create BANT custom attributes in Attio

Using the `attio-custom-attributes` fundamental, create the following fields on the Deals object:

**Score fields (number, 0-100):**
- `bant_budget_score`
- `bant_authority_score`
- `bant_need_score`
- `bant_timeline_score`
- `bant_composite_score`

**Status fields (select):**
- `bant_budget_status` — options: Confirmed, Likely, Unclear, No Budget
- `bant_authority_status` — options: Decision Maker, Influencer, Champion, Unknown
- `bant_need_status` — options: Critical, Important, Nice to Have, No Need
- `bant_timeline_status` — options: Immediate, This Quarter, This Year, No Timeline

**Metadata fields:**
- `bant_verdict` (select) — options: Qualified, Needs Work, Disqualified
- `bant_last_assessed` (date) — when the BANT score was last updated
- `bant_assessment_source` (select) — options: Pre-call Enrichment, Discovery Call, Follow-up Call, Re-qualification
- `bant_notes` (text) — freeform notes on qualification gaps and next steps

### 2. Define your scoring rubric

Customize the scoring weights based on your business. Default weights:

- **Budget (25%):** Does the prospect have or can they allocate budget for your solution?
- **Authority (25%):** Is this person the decision maker, or can they influence the decision?
- **Need (30%):** How critical is the problem you solve for them? (Weighted highest because no amount of budget, authority, or timeline matters if there is no need.)
- **Timeline (20%):** When do they need to make a decision?

Composite formula: `(B * 0.25) + (A * 0.25) + (N * 0.30) + (T * 0.20)`

Threshold tiers:
- **Qualified (70+):** Move to active pipeline. Schedule next step immediately.
- **Needs Work (40-69):** Stay in qualification stage. Identify which BANT dimension is weakest and address it.
- **Disqualified (<40):** Move to nurture or archive. Do not invest active selling time.

### 3. Configure pipeline stages

Using the `attio-pipeline-config` fundamental, ensure your deal pipeline includes these stages:

1. **New Lead** — just entered the pipeline, not yet assessed
2. **BANT Pre-Scored** — enrichment-based scoring complete, awaiting discovery call
3. **Discovery Scheduled** — call booked to validate BANT signals
4. **BANT Qualified** — composite score >= 70, all dimensions assessed
5. **BANT Needs Work** — score 40-69, specific gaps identified
6. **BANT Disqualified** — score < 40, moved to nurture

### 4. Set up PostHog tracking events

Using the `posthog-custom-events` fundamental, create events:

- `bant_score_created` — first BANT assessment on a deal (properties: deal_id, composite_score, verdict, source)
- `bant_score_updated` — subsequent re-scoring (properties: deal_id, old_score, new_score, changed_dimensions)
- `bant_qualification_passed` — deal crosses the 70 threshold
- `bant_disqualified` — deal scored below 40
- `bant_stage_changed` — deal moves between BANT pipeline stages

### 5. Validate the setup

Create a test deal in Attio. Set BANT scores manually: Budget 80, Authority 60, Need 90, Timeline 50. Verify:
- Composite score calculates correctly: (80*0.25)+(60*0.25)+(90*0.30)+(50*0.20) = 20+15+27+10 = 72
- Verdict = Qualified (72 >= 70)
- PostHog receives the `bant_score_created` event
- Deal moves to "BANT Qualified" stage

Delete the test deal after validation.

## Output

- Attio Deals object with 12 BANT custom attributes
- Pipeline stages mapped to BANT qualification outcomes
- PostHog events configured for tracking qualification funnel
- Scoring rubric documented and ready for use by other drills

## Triggers

Run once during setup. Re-run if you change your ICP or scoring weights.
