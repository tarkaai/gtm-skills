---
name: lead-score-automation
description: Automated real-time lead scoring pipeline that enriches, scores, tiers, and routes leads without manual intervention
category: Sales
tools:
  - n8n
  - Clay
  - Attio
  - PostHog
fundamentals:
  - n8n-triggers
  - n8n-workflow-basics
  - n8n-crm-integration
  - clay-enrichment-waterfall
  - clay-intent-signals
  - clay-scoring
  - attio-lead-scoring
  - attio-automation
  - posthog-custom-events
---

# Lead Score Automation

This drill builds an always-on scoring pipeline: new leads enter Attio, get enriched in Clay, scored on fit + intent, tiered, and routed — all without manual intervention. It also handles score decay for stale leads and re-scoring when the model is updated.

## Input

- Working lead scoring model (output from `lead-score-model-setup` drill)
- n8n instance with Attio and Clay integrations configured
- Clay table with enrichment columns set up
- PostHog tracking active on website and product

## Steps

### 1. Build the new-lead scoring workflow in n8n

Using `n8n-triggers`, create a workflow triggered by new person creation in Attio:

**Trigger:** Attio webhook — fires when a new person record is created
**Filter:** Only process records where `lead_score` is empty (avoids re-processing)

### 2. Enrich the lead in Clay

When the workflow fires:

1. Extract company_name, domain, contact_email, title from the Attio record
2. Using `n8n-workflow-basics`, POST the lead to your Clay enrichment table via Clay API
3. Wait for enrichment to complete (poll Clay API every 30 seconds, timeout after 5 minutes)
4. Pull enriched data: company size, industry, funding, tech stack, job postings

### 3. Compute fit score

Using the scoring model criteria, calculate fit score in the n8n workflow:

```
fit_score = 0
if employee_count >= 20 AND employee_count <= 500: fit_score += 15
if industry IN target_industries: fit_score += 10
if title MATCHES decision_maker_pattern: fit_score += 15
if tech_stack CONTAINS complementary_tools: fit_score += 5
if geography IN target_markets: fit_score += 5
```

### 4. Compute intent score

Pull behavioral data from PostHog and Clay:

1. Query PostHog for the lead's website events (page views, form submissions) using `posthog-custom-events`
2. Pull intent signal enrichment from Clay using `clay-intent-signals` (funding, job postings, tech changes)
3. Calculate intent score based on model criteria

```
intent_score = 0
if demo_form_submitted: intent_score += 20
if pricing_page_viewed: intent_score += 15
if email_replied: intent_score += 10
if content_downloaded: intent_score += 5
if sessions_last_14d >= 3: intent_score += 5
// Add Clay-sourced signals
if funding_last_90d: intent_score += funding_signal_points
if relevant_job_postings >= 3: intent_score += 25
```

### 5. Assign composite score and tier

```
lead_score = fit_score + intent_score
lead_tier = "Hot" if lead_score >= 80 else "Warm" if lead_score >= 50 else "Cold"
```

### 6. Write scores to Attio

Using `attio-lead-scoring`, update the person record with fit_score, intent_score, lead_score, lead_tier, and last_scored.

### 7. Log to PostHog

Fire a `lead_scored` event with all score components, tier, and `scoring_method: "automated"`.

### 8. Build the intent-update re-scoring workflow

Create a second n8n workflow triggered by PostHog webhook events (pricing_page_viewed, demo_form_submitted, content_downloaded):

1. Look up the person in Attio by email
2. Recalculate intent_score with the new signal
3. Recalculate composite score and tier
4. Update Attio record
5. If tier changed (e.g., Warm -> Hot), fire a `lead_tier_changed` event in PostHog and send a Slack notification

### 9. Build the score decay workflow

Create a third n8n workflow on a daily cron schedule:

1. Query Attio for leads where `last_scored` > 14 days ago AND `intent_score` > 0
2. For each: set `intent_score = intent_score * 0.5` (50% decay)
3. Recalculate composite score and tier
4. Update Attio record
5. Log `lead_score_decayed` event in PostHog

### 10. Build the model-update re-scoring workflow

Create a fourth n8n workflow triggered manually (webhook or button):

1. Query all leads from Attio
2. Re-run the scoring formula with updated criteria/weights
3. Batch update all records
4. Log `scoring_model_updated` event in PostHog with `model_version` property

## Output

- Always-on scoring: every new lead scored within minutes of entering CRM
- Real-time intent updates: scores recalculate when behavioral signals arrive
- Score decay: stale leads automatically deprioritized
- Model versioning: re-score all leads when criteria change

## Triggers

- New-lead workflow: runs automatically on every new Attio person record
- Intent-update workflow: runs on PostHog behavioral events
- Decay workflow: runs daily via cron
- Model-update workflow: triggered manually when scoring criteria change
