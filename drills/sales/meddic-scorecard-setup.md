---
name: meddic-scorecard-setup
description: Configure a MEDDIC scoring system in your CRM with custom fields for all 6 elements, scoring rubrics, and qualification thresholds
category: Sales
tools:
  - Attio
  - PostHog
fundamentals:
  - attio-custom-attributes
  - attio-pipeline-config
  - attio-deals
  - posthog-custom-events
---

# MEDDIC Scorecard Setup

This drill creates the infrastructure for structured MEDDIC qualification in your CRM. It sets up custom fields for each of the six MEDDIC elements (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion), defines scoring rubrics, and configures the pipeline stages that map to qualification outcomes.

## Input

- Your ICP definition (output from `icp-definition` drill)
- Access to Attio with admin permissions
- PostHog project for tracking qualification events

## Steps

### 1. Create MEDDIC custom attributes in Attio

Using the `attio-custom-attributes` fundamental, create the following fields on the Deals object:

**Score fields (number, 0-100):**
- `meddic_metrics_score`
- `meddic_economic_buyer_score`
- `meddic_decision_criteria_score`
- `meddic_decision_process_score`
- `meddic_identify_pain_score`
- `meddic_champion_score`
- `meddic_composite_score`

**Status fields (select):**
- `meddic_metrics_status` — options: Quantified, Directional, Vague, Absent
- `meddic_economic_buyer_status` — options: Identified and Engaged, Identified Not Engaged, Unknown
- `meddic_decision_criteria_status` — options: Documented, Partially Known, Unknown
- `meddic_decision_process_status` — options: Mapped, Partially Mapped, Unknown
- `meddic_identify_pain_status` — options: Acute, Moderate, Mild, Absent
- `meddic_champion_status` — options: Active Champion, Potential Champion, No Champion

**Evidence fields (text, long):**
- `meddic_metrics_evidence` — key quotes and data points about prospect's success metrics
- `meddic_economic_buyer_evidence` — who the economic buyer is, their access path, engagement level
- `meddic_decision_criteria_evidence` — documented evaluation criteria and how they rank
- `meddic_decision_process_evidence` — mapped steps from evaluation to purchase, timeline
- `meddic_identify_pain_evidence` — pain points articulated, business impact quantified
- `meddic_champion_evidence` — who the champion is, their influence, and their motivation

**Metadata fields:**
- `meddic_verdict` (select) — options: Qualified, Needs Work, Disqualified
- `meddic_last_assessed` (date) — when the MEDDIC score was last updated
- `meddic_assessment_source` (select) — options: Pre-call Enrichment, Discovery Call, Follow-up Call, Re-qualification
- `meddic_weakest_elements` (text) — comma-separated list of the 1-2 weakest elements
- `meddic_next_actions` (text) — recommended actions to strengthen weak elements

### 2. Define your scoring rubric

Customize the scoring weights based on your enterprise deal dynamics. Default weights:

- **Metrics (15%):** Has the prospect articulated specific, quantifiable business outcomes they expect? Deals with quantified metrics close at higher rates because both sides know what success looks like.
- **Economic Buyer (20%):** Have you identified and engaged the person who controls the budget and can say "yes"? Weighted highest along with Pain because deals die without economic buyer access.
- **Decision Criteria (15%):** Do you know the specific criteria the prospect will use to evaluate solutions? Understanding criteria lets you shape the evaluation in your favor.
- **Decision Process (15%):** Do you know every step from today to signed contract? Mapped processes produce predictable timelines. Unknown processes produce surprises.
- **Identify Pain (20%):** Does the prospect feel acute pain that your solution addresses? Weighted highest along with Economic Buyer because no pain = no urgency = no deal.
- **Champion (15%):** Is there someone inside the organization who will sell for you when you are not in the room?

Composite formula: `(M * 0.15) + (EB * 0.20) + (DC * 0.15) + (DP * 0.15) + (IP * 0.20) + (C * 0.15)`

Threshold tiers:
- **Qualified (70+):** Move to active pipeline. Strong across most elements. Schedule next step immediately.
- **Needs Work (40-69):** Stay in qualification stage. Identify weakest 1-2 elements and address them in next interaction.
- **Disqualified (<40):** Move to nurture or archive. Too many gaps to invest active selling time.

### 3. Configure pipeline stages

Using the `attio-pipeline-config` fundamental, ensure your deal pipeline includes these stages:

1. **New Lead** — just entered the pipeline, not yet assessed
2. **MEDDIC Pre-Scored** — enrichment-based scoring complete, awaiting discovery call
3. **Discovery Scheduled** — call booked to validate MEDDIC signals
4. **MEDDIC Qualified** — composite score >= 70, most elements assessed
5. **MEDDIC Needs Work** — score 40-69, specific element gaps identified
6. **MEDDIC Disqualified** — score < 40, moved to nurture
7. **Champion Engaged** — qualified deal where champion is actively advocating internally
8. **Economic Buyer Meeting** — meeting scheduled or completed with the economic buyer
9. **Decision Criteria Aligned** — prospect's decision criteria mapped and favorable to your solution

### 4. Set up PostHog tracking events

Using the `posthog-custom-events` fundamental, create events:

- `meddic_score_created` — first MEDDIC assessment on a deal (properties: deal_id, composite_score, verdict, source, element_scores)
- `meddic_score_updated` — subsequent re-scoring (properties: deal_id, old_score, new_score, changed_elements)
- `meddic_qualification_passed` — deal crosses the 70 threshold
- `meddic_disqualified` — deal scored below 40
- `meddic_stage_changed` — deal moves between MEDDIC pipeline stages
- `meddic_element_completed` — individual element moves from Unknown/Absent to a positive status (properties: deal_id, element, old_status, new_status)
- `meddic_champion_identified` — champion status changes to Active Champion
- `meddic_economic_buyer_engaged` — economic buyer status changes to Identified and Engaged

### 5. Validate the setup

Create a test deal in Attio. Set MEDDIC scores manually:
- Metrics: 80, Economic Buyer: 60, Decision Criteria: 75, Decision Process: 50, Identify Pain: 90, Champion: 65

Verify:
- Composite score calculates correctly: (80*0.15)+(60*0.20)+(75*0.15)+(50*0.15)+(90*0.20)+(65*0.15) = 12+12+11.25+7.5+18+9.75 = 70.5
- Verdict = Qualified (70.5 >= 70)
- PostHog receives the `meddic_score_created` event
- Deal moves to "MEDDIC Qualified" stage
- Weakest elements correctly identified as Decision Process (50) and Economic Buyer (60)

Delete the test deal after validation.

## Output

- Attio Deals object with 20+ MEDDIC custom attributes (scores, statuses, evidence, metadata)
- Pipeline stages mapped to MEDDIC qualification outcomes
- PostHog events configured for tracking the qualification funnel
- Scoring rubric documented and ready for use by other drills

## Triggers

Run once during setup. Re-run if you change your ICP, scoring weights, or add new MEDDIC-related pipeline stages.
