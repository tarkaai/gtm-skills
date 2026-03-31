---
name: crm-data-audit
description: Audit CRM records against data quality rules, score completeness and accuracy, and produce a prioritized remediation report
category: Operations
tools:
  - Attio
  - Clay
  - PostHog
fundamentals:
  - attio-contacts
  - attio-deals
  - attio-custom-attributes
  - attio-lists
  - attio-reporting
  - posthog-custom-events
---

# CRM Data Audit

Systematically audit CRM records for completeness, accuracy, freshness, and duplication. Produce a scored report that identifies the highest-impact issues and prioritizes remediation.

## Input

- Attio workspace with existing contact, company, and deal records
- A set of data quality rules (required fields, valid values, freshness thresholds) — either from the `crm-data-quality-rules` drill or manually defined
- Sample size (Smoke: 50 records; Baseline+: all active records)

## Steps

### 1. Define the audit scope

Query Attio for the record set to audit. Use `attio-contacts` to pull contacts and `attio-deals` to pull deals. For Smoke tests, sample 50 records randomly. For Baseline and above, pull all records where deal stage is not "Closed Lost" or "Archived."

### 2. Check field completeness

For each record, verify required fields are populated:

**Contacts:** full_name, email, company (linked), job_title, source, last_contacted, contact_status
**Companies:** name, domain, industry, employee_count
**Deals:** company, primary_contact, deal_value, expected_close_date, stage, source, owner

Score each record: `completeness_score = (populated_required_fields / total_required_fields) * 100`

Use `attio-custom-attributes` to write the `data_quality_score` back to each record.

### 3. Check field validity

Validate field values against allowed sets:
- Deal stages must be in the defined pipeline stages
- Contact status must be one of: Active, Nurture, Do Not Contact, Bounced
- Email addresses must pass regex validation (`^[^@]+@[^@]+\.[^@]+$`)
- Expected close dates must not be in the past for open deals
- Deal values must be positive numbers

Flag invalid values and deduct from the quality score.

### 4. Check freshness

Use `attio-contacts` to query the `last_contacted` field:
- Records with no activity in 30+ days: "stale"
- Records with no activity in 60+ days: "at risk"
- Records with no activity in 90+ days: "dead"

Calculate stale record rate: `(stale_records / total_records) * 100`

### 5. Detect duplicates

Search for duplicate records using these keys:
- **Contacts:** exact email match, or (similar full_name + same company domain)
- **Companies:** exact domain match, or similar company name (Levenshtein distance < 3)

Use `attio-lists` to create a "Potential Duplicates" list containing flagged records.

Calculate duplicate rate: `(duplicate_records / total_records) * 100`

### 6. Compute aggregate scores

Calculate overall data quality metrics:
- **Data quality score:** average of all individual record quality scores
- **Critical error rate:** % of records missing required fields (email, company, stage)
- **Duplicate rate:** % of records with potential duplicates
- **Stale record rate:** % of records with no activity in 30+ days

### 7. Log results

Use `posthog-custom-events` to log:
- `data_quality_audit_completed` with properties: scope (sample/full), record_count, quality_score, critical_error_rate, duplicate_rate, stale_rate
- `data_quality_issue_detected` for each issue found, with properties: record_id, issue_type, severity

Use `attio-reporting` to build a saved view showing records sorted by quality score (ascending) for prioritized remediation.

## Output

- Per-record data quality scores stored as custom attributes in Attio
- Aggregate metrics: quality score, critical error rate, duplicate rate, stale rate
- "Potential Duplicates" list in Attio
- Prioritized remediation view sorted by quality score
- PostHog events for trend tracking over repeated audits
