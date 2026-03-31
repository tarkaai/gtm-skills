---
name: crm-data-quality-rules
description: Define and enforce data quality rules as custom attributes and validation logic in the CRM
category: Operations
tools:
  - Attio
  - n8n
fundamentals:
  - attio-custom-attributes
  - attio-automation
  - attio-pipeline-config
  - n8n-triggers
  - n8n-workflow-basics
---

# CRM Data Quality Rules

Define explicit data quality rules, encode them as CRM configuration and automation logic, and enforce them at stage-gate transitions so bad data cannot propagate.

## Input

- Attio workspace with pipeline configured
- Understanding of your sales process and which fields matter at each stage
- n8n instance for enforcement automation

## Steps

### 1. Define required fields per pipeline stage

Establish which fields must be populated before a deal can advance:

| Stage | Required Fields |
|-------|----------------|
| Lead | contact_name, email, company, source |
| Qualified | + job_title, employee_count, industry, budget_range |
| Meeting Booked | + decision_maker_identified, pain_point, next_step_date |
| Proposal Sent | + deal_value, expected_close_date, proposal_url |
| Negotiation | + champion_identified, competitor_info, procurement_contact |
| Closed Won | + contract_value, close_date, win_reason |
| Closed Lost | + close_date, loss_reason, loss_detail |

Use `attio-custom-attributes` to create any missing fields. Set field types precisely: use `select` for constrained values, `date` for dates, `currency` for monetary amounts.

### 2. Define valid value constraints

For each select-type field, define the allowed options using `attio-custom-attributes`:
- **Source:** Outbound, Inbound, Referral, Event, Partner, Content
- **Contact Status:** Active, Nurture, Do Not Contact, Bounced
- **Loss Reason:** Price, Timing, Competitor, No Budget, No Need, No Decision, Champion Left

### 3. Build stage-gate enforcement

Use `n8n-triggers` to watch for deal stage changes in Attio. When a stage change is detected, the n8n workflow:

1. Reads the deal record via Attio API
2. Checks required fields for the target stage against the rules table
3. If all required fields are populated and valid: allow the stage change (no action needed — Attio already processed it)
4. If fields are missing: create an Attio note on the deal listing missing fields, revert the stage change via API, and notify the deal owner

Use `n8n-workflow-basics` to build the validation logic as a code node that reads the rules table and iterates over required fields.

### 4. Build freshness rules

Use `attio-automation` to create time-based rules:
- If a deal has no notes or activity logged in 7 days: set `stale_flag` = true, notify owner
- If `stale_flag` has been true for 14+ days: escalate to manager
- If contact `last_contacted` > 30 days: add to "Needs Outreach" list

### 5. Build duplicate prevention rules

Use `n8n-triggers` to intercept new contact/company creation:
1. On new record creation, query Attio for existing records matching email or domain
2. If match found: flag the new record, link it to the existing record, notify the creator
3. If no match: allow creation and proceed

### 6. Document the rules

Store the complete rules definition in an Attio note on a dedicated "Data Quality Standards" company record. This serves as the source of truth that other drills and the audit process reference.

## Output

- Custom attributes created for all required fields across pipeline stages
- n8n workflow enforcing stage-gate field requirements
- n8n workflow enforcing freshness rules
- n8n workflow intercepting duplicate creation
- Documented rules definition stored in Attio
