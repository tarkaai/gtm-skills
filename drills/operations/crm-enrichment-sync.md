---
name: crm-enrichment-sync
description: Automatically enrich CRM records with missing data from Clay and sync updates back to Attio
category: Operations
tools:
  - Clay
  - Attio
  - n8n
fundamentals:
  - clay-table-setup
  - clay-enrichment-waterfall
  - clay-deduplication
  - attio-contacts
  - attio-custom-attributes
  - n8n-crm-integration
  - n8n-workflow-basics
---

# CRM Enrichment Sync

Automatically detect CRM records with missing fields, route them through Clay for enrichment, deduplicate, and sync enriched data back to Attio. Reduces manual data entry and improves record completeness.

## Input

- Attio workspace with contacts and companies
- Clay workspace with enrichment credits
- n8n instance for orchestration
- List of fields to enrich: company size, industry, revenue, job title, LinkedIn URL, phone

## Steps

### 1. Identify records needing enrichment

Build an n8n workflow using `n8n-crm-integration` that queries Attio for records where key enrichment fields are empty:
- Contacts missing: job_title, linkedin_url, phone
- Companies missing: employee_count, industry, annual_revenue, tech_stack

Filter to only Active contacts and open deals to avoid wasting enrichment credits on dead records.

### 2. Export to Clay

Use `clay-table-setup` to create a Clay table for enrichment. Push the incomplete records from n8n to Clay with their existing data (name, email, company domain) as seed columns.

### 3. Run enrichment waterfall

Use `clay-enrichment-waterfall` to enrich records through multiple data providers in sequence:
- First try: email-based lookup (highest match rate for contacts)
- Second try: domain + name lookup (for contacts not found by email)
- Third try: domain-only lookup (for company-level fields)

Each provider fills different fields. The waterfall approach maximizes coverage while minimizing credit waste.

### 4. Deduplicate before sync

Before pushing enriched data back to Attio, run `clay-deduplication` on the enriched table:
- Dedup key: email + company domain
- Remove any records that would create duplicates in Attio
- Log duplicate matches for separate review

### 5. Sync enriched data to Attio

Use `n8n-crm-integration` to push enriched fields back to Attio:
- Match records by email (contacts) or domain (companies)
- Only update fields that were previously empty — never overwrite existing data
- Use `attio-custom-attributes` to write enrichment metadata: `enrichment_date`, `enrichment_source`, `enrichment_confidence`

### 6. Measure enrichment effectiveness

Track enrichment success rate: `(fields_filled / fields_attempted) * 100`

Use `n8n-workflow-basics` to log enrichment results:
- Records attempted
- Records successfully enriched
- Fields filled per record (average)
- Credits consumed
- Cost per enriched record

## Output

- n8n workflow that detects incomplete records, routes through Clay, and syncs back to Attio
- Enrichment metadata on every touched record (date, source, confidence)
- Enrichment effectiveness metrics for ROI tracking
- Deduplication check preventing enrichment from creating duplicates

## Triggers

- **On-demand:** Run manually when preparing for an audit
- **On record creation:** Trigger enrichment when a new contact or company is created with missing fields
- **Scheduled:** Run weekly to catch records that slipped through
