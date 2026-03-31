---
name: stakeholder-enrichment-automation
description: Automated workflow that enriches new deals with org chart data and pre-classifies stakeholders
category: Prospecting
tools:
  - Clay
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - org-chart-research
  - stakeholder-role-classification
  - clay-people-search
  - clay-enrichment-waterfall
  - attio-custom-attributes
  - attio-contacts
  - n8n-workflow-basics
  - n8n-crm-integration
  - n8n-triggers
---

# Stakeholder Enrichment Automation

This drill builds an n8n workflow that automatically triggers when a new deal is created in Attio, researches the company's org chart via Clay, classifies stakeholders by buying role, and populates the CRM — so the sales team starts every deal with a pre-built stakeholder map.

## Input

- n8n instance connected to Attio (webhook or polling trigger)
- Clay account with People Search and Claygent credits
- Attio with stakeholder custom attributes already configured (from `stakeholder-research` drill)
- Anthropic API key for role classification

## Steps

### 1. Build the trigger

Using the `n8n-triggers` fundamental, create a workflow triggered by new deal creation in Attio. Configure a webhook on Attio's deal object that fires when a deal moves to the "Connected" stage, or poll Attio every 30 minutes for new deals without a `stakeholder_mapped` flag.

### 2. Extract the company from the deal

When triggered, the workflow reads the deal record from Attio using `n8n-crm-integration`. Extract the linked company name, domain, and LinkedIn company URL. If any are missing, use Clay's company enrichment to fill gaps.

### 3. Run org chart research in Clay

Using `n8n-workflow-basics`, build an HTTP Request node that calls Clay's API to:
1. Create a temporary table row for the company (or use an existing one)
2. Trigger the "Find People at Company" enrichment with filters: Seniority = Director+, Departments = Engineering, Product, Finance, IT, Operations, Procurement
3. Wait for enrichment to complete (poll Clay table status every 30 seconds, timeout after 5 minutes)
4. Read the enriched results — up to 20 contacts per company

### 4. Classify stakeholders via Claude

For each person returned by Clay, call the Anthropic Messages API (using `stakeholder-role-classification` fundamental):
- Send: name, title, department, company context, your product description
- Receive: role classification, confidence level, reasoning
- Batch requests in groups of 5 with 1-second delays to respect rate limits

### 5. Write stakeholders to Attio

For each classified stakeholder, use `attio-contacts` to:
1. Check if the person already exists in Attio (search by email or LinkedIn URL)
2. If new: create a Person record with name, title, email, LinkedIn URL, company link
3. Set custom attributes: `stakeholder_role`, `stakeholder_confidence`, `stakeholder_sentiment` (default: Unknown), `engagement_level` (default: No Contact)
4. Link the person to the deal record

### 6. Generate the stakeholder summary

After all people are processed, use Claude to generate a summary note:
```
Prompt: "Given this stakeholder map for {Company}, summarize the buying committee. List each role found, flag any gaps (missing Economic Buyer, missing Champion), and recommend which stakeholders to engage first. Return as structured text."
```

Write the summary as a note on the deal using `attio-notes`.

### 7. Set the completion flag

Update the deal record with `stakeholder_mapped: true` and `stakeholder_map_date: {today}`. This prevents the workflow from re-triggering for the same deal.

### 8. Error handling

Build error branches in n8n for:
- **Clay enrichment returns 0 people**: Company may be too small or private. Log a warning note on the deal: "Auto-mapping failed — manual research required."
- **Anthropic API error**: Retry once after 5 seconds. If it fails again, classify the person as role=Unknown and flag for manual review.
- **Attio write failure**: Log the error and continue with remaining stakeholders. Do not let one failed write stop the entire workflow.

## Output

- Every new deal at Connected stage automatically gets a pre-built stakeholder map
- 15-20 contacts per account with role classifications and confidence scores
- Summary note on the deal highlighting gaps and recommended first actions
- `stakeholder_mapped` flag set on the deal for tracking coverage

## Triggers

- Runs automatically when a deal enters Connected stage in Attio
- Can be manually triggered for existing deals that were created before automation was set up
