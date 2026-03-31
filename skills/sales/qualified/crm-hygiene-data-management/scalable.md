---
name: crm-hygiene-data-management-scalable
description: >
  CRM Hygiene & Data Quality — Scalable Automation. Deploy always-on data quality workflows
  that auto-validate, auto-enrich, auto-deduplicate, and auto-score 500+ records with a
  weighted quality model. Reduce manual cleanup time by >=70%.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=90% data quality score across 500+ records and >=70% reduction in manual cleanup time over 2 months"
kpis: ["Data quality score", "Automation coverage", "Manual cleanup time reduction", "Enrichment success rate"]
slug: "crm-hygiene-data-management"
install: "npx gtm-skills add sales/qualified/crm-hygiene-data-management"
drills:
  - crm-data-quality-automation
  - crm-duplicate-prevention
---

# CRM Hygiene & Data Quality — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** OutboundFounderLed | **Channels:** Product

## Outcomes

The 10x multiplier for data quality: move from reactive auditing to proactive, always-on automation that monitors, validates, enriches, deduplicates, and scores records continuously. The system handles 500+ active records without proportional manual effort. Manual cleanup time drops by >=70% because the automation catches and fixes issues before they accumulate.

**Pass threshold:** >=90% data quality score across 500+ active records and >=70% reduction in manual cleanup time over 2 months.

## Leading Indicators

- Continuous validation workflow running every 6 hours without failures
- Auto-enrichment firing on every new record creation (< 1 hour latency)
- Duplicate prevention intercepting new record creation in real time
- Stale record manager sending daily alerts to deal owners
- Weekly quality reports auto-generated and posted to Slack
- Manual cleanup time tracked and declining week-over-week

## Instructions

### 1. Deploy Full Data Quality Automation

Run the `crm-data-quality-automation` drill to build the always-on automation layer:

**Continuous validation (every 6 hours):**
1. Build an n8n workflow on a 6-hour cron schedule
2. Query Attio for all records modified in the last 6 hours
3. Run validation rules against each record: required fields, format validation, freshness check
4. Compute and write the weighted quality score per record:
   - Completeness: 40% weight (populated required fields / total required fields)
   - Recency: 30% weight (days since last contact, scaled 0-1)
   - Accuracy: 20% weight (valid fields / total fields)
   - Activity: 10% weight (activities in last 30 days, capped at 4)
5. If score drops below 70: create Attio note with specific issues, notify owner
6. Log every validation run to PostHog

**Auto-enrichment on creation:**
1. Build an n8n workflow triggered by new record creation in Attio
2. Check which required fields are empty
3. If 3+ fields missing: route to Clay enrichment waterfall
4. Sync enriched data back, only filling empty fields
5. Recalculate quality score post-enrichment
6. Log enrichment event to PostHog with fields_attempted and fields_filled

**Stale record management (daily):**
1. Build an n8n workflow on a daily cron schedule
2. Query open deals where last_contacted > 30 days
3. 30-59 days stale: notify deal owner
4. 60-89 days stale: escalate to manager, add "at risk" tag
5. 90+ days stale: move to "Needs Review" list, suggest archival

**Weekly aggregate reporting:**
1. Build an n8n workflow on a weekly cron schedule (Monday 8 AM)
2. Query all active records, calculate aggregate metrics
3. Compare against previous week
4. Generate summary: overall score, top issues, per-rep compliance, delta from last week
5. Post to Slack and log to PostHog

### 2. Deploy Duplicate Prevention

Run the `crm-duplicate-prevention` drill to catch duplicates at the point of creation:

**Real-time interceptor:**
1. Build an n8n workflow triggered by new record creation
2. Run exact match: search Attio for contacts with same email or companies with same domain
3. Run fuzzy match: for contacts at the same domain, compare normalized names (lowercase, strip prefixes/suffixes). Flag if similarity > 80%
4. For companies: normalize names (remove Inc., LLC, Ltd., etc.), flag if similarity > 85%

**On confirmed duplicate:**
1. Create notes on both records explaining the match
2. Add to "Pending Merge" list in Attio
3. Generate merge recommendation: which record to keep (more complete data wins)

**On fuzzy match:**
1. Create a note flagging the potential match
2. Add to "Review Duplicates" list (separate from confirmed)
3. Do not auto-merge — human reviews weekly

**Batch cleanup for historical data:**
1. Export all contacts to Clay
2. Run Clay deduplication with composite key (email + domain)
3. Run a second pass with name + domain for fuzzy matches
4. Import duplicate pairs back to Attio as "Historical Duplicates" list
5. Process the list over the first 2 weeks

### 3. Measure Manual Cleanup Time Reduction

Track the time shift from manual to automated:

1. Log all manual cleanup actions by reps in Attio (create a "Manual Fix" activity type)
2. Compare hours per week spent on manual data cleanup against the Baseline period
3. Calculate: `reduction = 1 - (current_manual_hours / baseline_manual_hours)`
4. Target: >=70% reduction

Set up a PostHog event `manual_data_fix` that reps log when they manually correct a record. Track the weekly count and compare against the Baseline-era count.

### 4. Correlate Quality with Sales Outcomes

Use PostHog to analyze whether data quality impacts sales:

1. Segment deals by quality score bucket: high (85+), medium (70-84), low (<70)
2. Compare win rates across segments
3. Compare average days to close across segments
4. Compare forecast accuracy (predicted close date vs actual) across segments

If high-quality deals close faster or at higher rates, this correlation justifies the automation investment and provides the baseline the Durable optimization loop will improve upon.

### 5. Evaluate Against Threshold

After 2 months, measure:

- Average quality score across all 500+ active records: target >=90%
- Manual cleanup time reduction: target >=70%
- Automation uptime: all workflows running without manual intervention for 4+ consecutive weeks
- Enrichment success rate: >=60% of auto-enrichment attempts fill at least 1 field

If all thresholds met: move to Durable. The automation is working — now optimize it autonomously.
If not: identify the bottleneck. Low quality score → tighten validation rules. High manual time → automate the remaining manual steps. Low enrichment rate → try additional Clay data providers.

## Time Estimate

- 12 hours: Build continuous validation workflow (n8n, scoring model, alerts)
- 8 hours: Build auto-enrichment trigger and Clay integration
- 6 hours: Build stale record manager
- 10 hours: Deploy duplicate prevention (real-time + batch historical cleanup)
- 4 hours: Set up weekly reporting workflow
- 4 hours: Correlate quality with sales outcomes in PostHog
- 16 hours: Monitoring and iteration over 2 months (~2 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — record storage, validation, quality scores, views | $29/user/mo (Plus) or $86/user/mo (Pro) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — auto-fill missing fields, deduplication | $185/mo (Launch) or $495/mo (Growth for CRM sync) — [clay.com/pricing](https://www.clay.com/pricing) |
| n8n | Automation — validation, enrichment, stale management, dedup, reporting | €60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Analytics — quality trend dashboards, sales correlation | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost this level:** ~$200-400/mo. Primary drivers: Clay ($185-495/mo depending on enrichment volume), n8n Pro ($60/mo for higher execution count from 6-hourly workflows).

## Drills Referenced

- `crm-data-quality-automation` — always-on workflows that validate, enrich, deduplicate, and score CRM records on continuous schedules
- `crm-duplicate-prevention` — real-time duplicate detection at point of creation with exact and fuzzy matching, plus batch historical deduplication
