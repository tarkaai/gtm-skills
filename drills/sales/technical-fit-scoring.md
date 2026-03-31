---
name: technical-fit-scoring
description: Score technical fit across deals using enrichment data and discovery results, flag blockers, and route deals by technical readiness
category: Sales
tools:
  - Attio
  - Anthropic
  - n8n
  - PostHog
fundamentals:
  - attio-deals
  - attio-custom-attributes
  - attio-automation
  - attio-reporting
  - n8n-workflow-basics
  - n8n-triggers
  - posthog-custom-events
---

# Technical Fit Scoring

This drill builds and maintains a technical fit scoring system that evaluates every qualified deal on five dimensions: integrations, security/compliance, infrastructure, performance, and data migration. It produces a composite score, flags blockers, routes deals to the right next step, and tracks scoring accuracy over time by comparing predictions to actual outcomes.

## Input

- Attio CRM with deal records containing technical discovery data (from `tech-stack-discovery` and/or `technical-discovery-call` drills)
- Attio custom attributes for technical scoring already created (or this drill creates them)
- n8n for automation (at Scalable level and above)

## Steps

### 1. Set up technical scoring infrastructure in Attio

Create custom attributes on the Deals object if they do not already exist:

**Score fields (number, 0-100):**
- `tech_integrations_score`
- `tech_security_score`
- `tech_infrastructure_score`
- `tech_performance_score`
- `tech_migration_score`
- `tech_composite_fit_score`

**Status fields (select):**
- `tech_verdict` — options: Strong Fit, Moderate Fit, Weak Fit, No Fit
- `tech_assessment_source` — options: Pre-enrichment, Discovery Call, Solutions Engineer, Security Review
- `tech_routing_status` — options: Pending Assessment, Technically Qualified, Needs SE Review, Needs Product Review, Technically Disqualified

**Text fields:**
- `tech_blockers_summary`
- `tech_key_integrations`
- `tech_certifications_required`

**Number fields:**
- `tech_blocker_count`
- `tech_maturity_score` (1-5)

**Date field:**
- `tech_last_assessed`

**Computed field:**
- `tech_composite_fit_score` = (integrations * 0.30) + (security * 0.25) + (infrastructure * 0.15) + (performance * 0.15) + (migration * 0.15)

Use the `attio-custom-attributes` fundamental to create each field via the API:
```
POST https://api.attio.com/v2/objects/deals/attributes
Authorization: Bearer {ATTIO_API_KEY}
Content-Type: application/json

{
  "title": "Tech Integrations Score",
  "api_slug": "tech_integrations_score",
  "type": "number"
}
```

### 2. Build scoring rubric

Define what each score range means per category:

**Integrations (30% weight):**
- 80-100: All required integrations exist natively or via well-documented API. No custom dev needed.
- 60-79: Most integrations available. 1-2 require middleware (Zapier/n8n/Tray) but are achievable.
- 40-59: Several integrations need custom API work. Moderate engineering effort required.
- 20-39: Key integrations missing. Would require significant custom development.
- 0-19: Critical integration impossible with current architecture.

**Security/Compliance (25% weight):**
- 80-100: All required certifications held. Security review will pass without issues.
- 60-79: Most certifications held. 1-2 minor gaps addressable within normal sales cycle.
- 40-59: Some certifications missing but on roadmap. Security review will have findings to remediate.
- 20-39: Major certification gaps. Remediation timeline exceeds typical sales cycle.
- 0-19: Fundamental security architecture mismatch. Cannot meet requirements.

**Infrastructure (15% weight):**
- 80-100: Deployment model matches exactly. No infrastructure concerns.
- 60-79: Minor adjustments needed (region, configuration) but achievable.
- 40-59: Deployment model requires custom arrangement (dedicated instance, specific region).
- 20-39: Significant infrastructure gaps. Would require architectural changes.
- 0-19: Cannot support required deployment model.

**Performance (15% weight):**
- 80-100: Easily meets all SLA, throughput, and scale requirements.
- 60-79: Meets requirements with some optimization or configuration.
- 40-59: Can meet requirements but near current capacity limits.
- 20-39: Cannot meet requirements without significant engineering investment.
- 0-19: Fundamental performance architecture mismatch.

**Data Migration (15% weight):**
- 80-100: Standard migration with existing tooling. Minimal complexity.
- 60-79: Moderate migration requiring some custom mapping or transformation.
- 40-59: Complex migration with significant data transformation needs.
- 20-39: Very complex migration that will delay deployment significantly.
- 0-19: Migration technically infeasible or would result in unacceptable data loss.

### 3. Apply scoring to deals

For each deal with technical discovery data, apply the rubric:

**If scores come from `call-transcript-tech-requirements-extraction`:** Use the LLM-generated scores directly. These are already calibrated to the rubric.

**If scores come from `tech-stack-discovery` (pre-enrichment only):** Apply a confidence discount of 0.7x since these are predictions, not confirmed requirements. Flag the deal as "needs discovery call" to validate.

**Composite score calculation:**
```
composite = (integrations * 0.30) + (security * 0.25) + (infrastructure * 0.15) + (performance * 0.15) + (migration * 0.15)
```

**Verdict mapping:**
- Strong Fit: composite >= 75 AND zero blockers
- Moderate Fit: composite 50-74 OR composite >= 75 with blockers
- Weak Fit: composite 25-49
- No Fit: composite < 25

### 4. Route deals by technical readiness

Based on the verdict, set `tech_routing_status` and trigger next actions:

**Technically Qualified (Strong Fit):**
- Set `tech_routing_status = "Technically Qualified"`
- No additional technical work needed. Proceed with commercial discussions.

**Needs SE Review (Moderate Fit with integration or performance blockers):**
- Set `tech_routing_status = "Needs SE Review"`
- Create a task: "Schedule solutions engineer call — {blocker summary}"
- Notify the SE channel in Slack

**Needs Product Review (Moderate or Weak Fit with feature/roadmap blockers):**
- Set `tech_routing_status = "Needs Product Review"`
- Create a task: "Product team feasibility assessment — {blocker summary}"
- Set a 1-week deadline for product response

**Technically Disqualified (No Fit):**
- Set `tech_routing_status = "Technically Disqualified"`
- Log the disqualification reason for product roadmap analysis
- Move deal to "Technically Disqualified" stage

### 5. Track scoring accuracy

Log a PostHog event for every technical score applied:
```json
{
  "event": "tech_fit_score_applied",
  "properties": {
    "deal_id": "...",
    "composite_score": 72,
    "verdict": "moderate_fit",
    "source": "discovery_call",
    "blocker_count": 1,
    "integrations_score": 65,
    "security_score": 85,
    "infrastructure_score": 90,
    "performance_score": 60,
    "migration_score": 55
  }
}
```

After deal closes (won or lost), compare the technical score at time of close against the outcome:
- Won deals: Was the technical fit score predictive? Did blockers get resolved?
- Lost deals with "technical" as loss reason: Was the score low? If not, the rubric needs recalibration.

Log accuracy events:
```json
{
  "event": "tech_fit_score_accuracy_check",
  "properties": {
    "deal_id": "...",
    "score_at_close": 72,
    "deal_outcome": "won|lost",
    "loss_reason_technical": false,
    "implementation_issues": 0,
    "accuracy_verdict": "accurate|overestimated|underestimated"
  }
}
```

## Output

- Technical scoring infrastructure in Attio
- Every qualified deal scored across 5 technical dimensions
- Deals routed by technical readiness
- Accuracy tracking dataset that improves the rubric over time

## Triggers

- Run scoring after `tech-stack-discovery` (pre-enrichment score)
- Re-score after `technical-discovery-call` (confirmed score)
- Re-score after solutions engineer or security review calls
- Accuracy check triggered by deal stage change to Won or Lost
