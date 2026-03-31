---
name: crm-data-quality-automation
description: Automated workflows that detect, flag, and fix common CRM data quality issues without manual intervention
category: Operations
tools:
  - Attio
  - n8n
  - Clay
  - PostHog
fundamentals:
  - attio-contacts
  - attio-deals
  - attio-custom-attributes
  - attio-automation
  - attio-lists
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - n8n-error-handling
  - n8n-crm-integration
  - clay-enrichment-waterfall
  - posthog-custom-events
---

# CRM Data Quality Automation

Build always-on n8n workflows that continuously monitor CRM data quality, auto-fix common issues (missing fields via enrichment, stale records via alerts), and escalate complex problems to humans. This is the automation layer that scales data quality from periodic manual audits to continuous enforcement.

## Input

- Attio workspace with data quality rules defined (from `crm-data-quality-rules` drill)
- n8n instance with Attio and Clay integrations configured
- PostHog for metrics tracking
- Data quality score baseline from previous audit

## Steps

### 1. Build the continuous validation workflow

Create an n8n workflow triggered by `n8n-scheduling` (runs every 6 hours):

1. Query Attio for all records modified in the last 6 hours using `attio-contacts` and `attio-deals`
2. For each modified record, run the validation rules:
   - Check required fields for the current stage
   - Validate field formats (email regex, date ranges, positive amounts)
   - Check freshness (last_contacted date)
3. Compute `data_quality_score` per record
4. Use `attio-custom-attributes` to update the score on each record
5. If score dropped below 70: create an Attio note with specific issues and notify the record owner

Use `n8n-error-handling` to handle API failures gracefully — retry transient errors, log persistent failures.

### 2. Build the auto-enrichment trigger

Create an n8n workflow triggered by `n8n-triggers` on new record creation in Attio:

1. When a new contact or company is created, check which required fields are empty
2. If 3+ fields are missing: route the record to Clay for enrichment via `clay-enrichment-waterfall`
3. When Clay returns results, update Attio via `n8n-crm-integration`
4. Recalculate the quality score after enrichment
5. Log the enrichment event to PostHog via `posthog-custom-events`

### 3. Build the stale record manager

Create an n8n workflow triggered by `n8n-scheduling` (runs daily):

1. Query Attio for open deals where `last_contacted` > 30 days
2. For records 30-59 days stale: notify the deal owner with a reminder
3. For records 60-89 days stale: escalate to manager, flag as "at risk"
4. For records 90+ days stale: move to a "Needs Review" list via `attio-lists`, suggest archival

### 4. Build the duplicate detector

Create an n8n workflow triggered by `n8n-scheduling` (runs daily):

1. Query Attio for all contacts created in the last 24 hours
2. For each new contact, search for existing contacts with matching email or (similar name + same company domain)
3. If potential duplicate found: flag both records, create a merge recommendation note on each
4. Add both records to a "Potential Duplicates" list via `attio-lists`
5. Log to PostHog via `posthog-custom-events`: `duplicate_detected` with properties

### 5. Build the data quality scoring engine

Create a comprehensive scoring model as an n8n code node:

```
score = 0
// Completeness (40% weight)
completeness = populated_required_fields / total_required_fields
score += completeness * 40

// Recency (30% weight)
days_since_contact = (today - last_contacted).days
if days_since_contact <= 7: recency = 1.0
elif days_since_contact <= 30: recency = 0.7
elif days_since_contact <= 60: recency = 0.3
else: recency = 0.0
score += recency * 30

// Accuracy (20% weight)
accuracy = valid_fields / total_fields
score += accuracy * 20

// Activity (10% weight)
activity = min(activities_last_30_days / 4, 1.0)
score += activity * 10
```

Write the composite score to each record via `attio-custom-attributes`.

### 6. Build aggregate reporting

Create an n8n workflow triggered by `n8n-scheduling` (runs weekly):

1. Query all active records from Attio
2. Calculate aggregate metrics: average quality score, critical error rate, duplicate rate, stale rate
3. Compare against previous week's metrics
4. Log to PostHog: `data_quality_weekly_summary` with all aggregate metrics
5. Generate a summary and post to Slack or store as an Attio note

## Output

- Continuous validation workflow checking modified records every 6 hours
- Auto-enrichment on new record creation
- Daily stale record detection and escalation
- Daily duplicate detection
- Weighted quality scoring engine
- Weekly aggregate reporting
- All events logged to PostHog for trend analysis

## Triggers

- **Scheduled:** 6-hourly validation, daily stale/duplicate checks, weekly reporting
- **Event-driven:** new record creation triggers enrichment
- **Alert-driven:** quality score drops trigger notifications
