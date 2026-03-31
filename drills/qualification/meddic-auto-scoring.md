---
name: meddic-auto-scoring
description: Automated pre-qualification pipeline that enriches and MEDDIC-scores new leads across all 6 elements before human contact
category: Qualification
tools:
  - Clay
  - Attio
  - n8n
  - PostHog
fundamentals:
  - clay-meddic-enrichment
  - clay-scoring
  - clay-table-setup
  - attio-custom-attributes
  - attio-deals
  - n8n-workflow-basics
  - n8n-triggers
  - posthog-custom-events
---

# MEDDIC Auto-Scoring Pipeline

This drill builds an automated pipeline that takes raw leads and produces MEDDIC pre-qualification scores without human involvement. New leads enter via CRM webhook, get enriched in Clay across all six MEDDIC elements, scored, and routed back to CRM with scores, element-level evidence, and a qualification tier.

## Input

- New lead enters Attio (via form submission, import, or outbound list)
- Clay table configured with MEDDIC enrichment columns (from `clay-meddic-enrichment` fundamental)
- n8n instance for orchestration

## Steps

### 1. Set up the trigger workflow in n8n

Using the `n8n-triggers` fundamental, create a workflow triggered by new deal creation in Attio:

- **Trigger:** Attio webhook — fires when a new deal record is created
- **Filter:** Only process deals where `meddic_composite_score` is empty (avoids re-processing already-scored deals)

### 2. Push the lead to Clay for enrichment

When a new deal triggers the workflow:

1. Extract the company name, contact email, contact title, and LinkedIn URL from the Attio record
2. Use the `clay-table-setup` fundamental to add the row to your MEDDIC enrichment table in Clay
3. Trigger Clay's enrichment columns (they run automatically on new rows)
4. Wait for enrichment to complete (poll Clay API every 30 seconds for up to 5 minutes)

### 3. Compute MEDDIC pre-scores in Clay

After enrichment completes, Clay's formula columns calculate per-element scores:

- **Metrics signal score (0-100):** Based on company revenue, growth rate, competitor tool usage, and whether they track quantifiable outcomes in the problem area
- **Economic Buyer signal score (0-100):** Based on contact title seniority, department match, org chart mapping, and whether the budget holder has been identified
- **Decision Criteria signal score (0-100):** Based on tech stack complexity, compliance requirements, relevant job postings, and evaluation signals
- **Decision Process signal score (0-100):** Based on company size, procurement team presence, legal team complexity, and industry regulation (higher score = simpler process)
- **Identify Pain signal score (0-100):** Based on hiring for problem-area roles, negative competitor reviews, news mentions of the problem, and social pain signals
- **Champion signal score (0-100):** Based on LinkedIn engagement with your product category, event attendance, content creation in the space, and organizational influence

Composite: `(M * 0.15) + (EB * 0.20) + (DC * 0.15) + (DP * 0.15) + (IP * 0.20) + (C * 0.15)`

See `clay-meddic-enrichment` fundamental for the detailed formula logic.

### 4. Push scores back to Attio

Using the `attio-deals` fundamental, update the deal record with:
- `meddic_metrics_score`, `meddic_economic_buyer_score`, `meddic_decision_criteria_score`, `meddic_decision_process_score`, `meddic_identify_pain_score`, `meddic_champion_score`
- `meddic_composite_score`
- `meddic_verdict` — Qualified / Needs Work / Disqualified based on thresholds
- `meddic_assessment_source` = "Pre-call Enrichment"
- `meddic_last_assessed` = today's date
- `meddic_weakest_elements` — the 1-2 elements with lowest scores
- Element-level evidence fields with the raw enrichment data that explains each score

### 5. Route the deal based on pre-score

In the same n8n workflow, add routing logic:

- **Composite >= 70 (Qualified):** Move deal to "MEDDIC Pre-Scored" stage. Trigger a Slack notification to the founder: "New MEDDIC-qualified lead: {company} — score {score}. Strongest: {top elements}. Weakest: {bottom elements}. Book discovery call." Include a Cal.com booking link in the notification.
- **Composite 50-69 (Needs Work — High Priority):** Move to "MEDDIC Pre-Scored" stage. Add a note listing which elements are weak and what to probe in discovery. Priority outreach.
- **Composite 40-49 (Needs Work — Low Priority):** Move to "MEDDIC Pre-Scored" stage. Add to outreach queue but deprioritize behind higher-scoring leads.
- **Composite < 40 (Disqualified):** Move to "MEDDIC Disqualified." Add to a nurture sequence. No active sales effort.

### 6. Generate discovery call prep (for qualified leads)

For deals scoring >= 50, use Claude to generate a discovery call prep brief:

1. Analyze which MEDDIC elements are weak (< 50 score)
2. For each weak element, generate 3-4 targeted discovery questions
3. For strong elements, generate 1-2 confirmation questions to validate enrichment data
4. Store the prep brief as an Attio note on the deal

This saves the founder 15-20 minutes of prep per call by pre-generating the question guide.

### 7. Log to PostHog

Using `posthog-custom-events`, fire a `meddic_auto_score_completed` event with properties:
- `deal_id`, `company_name`, `composite_score`, `verdict`
- `metrics_score`, `economic_buyer_score`, `decision_criteria_score`, `decision_process_score`, `identify_pain_score`, `champion_score`
- `weakest_elements`
- `enrichment_hit_rate` (% of enrichment columns that returned data)
- `auto_prep_generated` (boolean, whether discovery prep was generated)

This feeds your qualification funnel analytics.

### 8. Handle enrichment failures

If Clay enrichment fails or returns sparse data (< 40% of columns populated):
- Set `meddic_verdict` = "Needs Work" regardless of score (insufficient data to judge)
- Add an Attio note: "Auto-scoring incomplete — enrichment coverage {X}%. Manual research recommended before discovery call."
- Flag in Slack for manual review
- Log `meddic_auto_score_incomplete` event to PostHog with the failure reason

If a specific element has zero enrichment data:
- Score that element at 25 (not 0, because absence of signal is not proof of absence)
- Flag that element in `meddic_weakest_elements` regardless of score
- Add a note: "{element} could not be assessed via enrichment. Prioritize in discovery call."

## Output

- Every new deal in Attio gets automatic MEDDIC pre-scores within minutes
- Element-level evidence populated for each scored dimension
- Discovery call prep brief auto-generated for qualified leads
- Deals are routed to the correct pipeline stage without manual intervention
- Founder receives Slack alerts for high-scoring leads with booking links
- PostHog tracks the full auto-scoring funnel for analysis

## Triggers

Runs automatically on every new deal creation via n8n webhook. No manual intervention needed. Monitor n8n execution logs weekly for errors. Re-run enrichment quarterly for stale leads in the "Needs Work" stage.
