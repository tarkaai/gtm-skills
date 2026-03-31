---
name: account-research-automation
description: Fully automated n8n pipeline that researches new accounts on arrival and generates AI-powered briefs
category: Research
tools:
  - n8n
  - Clay
  - Attio
  - Anthropic
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-crm-integration
  - n8n-scheduling
  - clay-claygent
  - clay-enrichment-waterfall
  - account-intelligence-assembly
  - account-brief-generation
  - attio-lists
  - attio-notes
---

# Account Research Automation

This drill builds an always-on n8n pipeline that automatically researches every new target account the moment it enters your CRM. When an account is added to the target list in Attio, the pipeline fires: enriches via Clay, searches for news, detects tech stack, identifies contacts, generates an AI-powered account brief with personalization hooks, and stores everything back in Attio. The human receives a research-complete notification and can outreach immediately.

## Input

- n8n instance with Attio, Clay, and Anthropic API credentials configured
- Clay table template for account enrichment (from `account-research-enrichment` drill)
- Attio workspace with a "Target Accounts" list
- Anthropic API key for brief generation

## Steps

### 1. Build the trigger workflow

Using the `n8n-triggers` fundamental, create a new n8n workflow triggered by:

**Primary trigger:** Attio webhook — fires when a company record is added to the "Target Accounts" list.

```
Trigger: Attio Webhook
Event: record.added_to_list
List: "Target Accounts"
```

**Secondary trigger:** n8n cron schedule — runs daily at 6am to catch any missed webhook events. Queries Attio for companies added to the target list in the last 24 hours that do not have an `account_brief_date` attribute set.

### 2. Build the enrichment node chain

After the trigger fires, chain these nodes:

**Node 1 — Clay Enrichment:**
Send the company domain to Clay via API (`POST https://api.clay.com/v1/tables/{template_table_id}/rows`). This triggers all enrichment columns configured in the template table: firmographics, funding, tech stack, news signals, and contacts.

Poll for completion: `GET /v1/tables/{table_id}/rows/{row_id}` until all enrichment columns are populated (max wait: 120 seconds, poll every 10 seconds).

**Node 2 — Parse Results:**
Extract from the Clay row: employee count, revenue estimate, funding data, tech stack (classified), news signals (top 3), contacts (top 3 with emails).

**Node 3 — CRM History:**
Query Attio for any prior interactions with this company: past deals, meeting notes, emails. Include in the context for brief generation.

### 3. Build the brief generation node

**Node 4 — Generate Account Brief:**
Using the `account-brief-generation` fundamental, send the enriched data to the Anthropic API. The prompt includes all firmographics, news signals, tech stack, contacts, CRM history, and your product's value proposition.

Receive back: structured brief with 3 personalization hooks, recommended entry point, and suggested talk track.

### 4. Build the storage and notification nodes

**Node 5 — Write to Attio:**
- Update company record with enrichment data (firmographics, tech stack, funding)
- Create a note with the generated account brief tagged `account-brief`
- Set `account_brief_date` to today
- Set `account_priority_score` based on signal scoring
- Create or update contact records for discovered contacts

**Node 6 — Notify:**
Send a Slack message (or email via Loops) to the founder/SDR:
```
New account researched: {Company Name}
Priority: {score}/100
Top signal: {top_signal_summary}
Best entry point: {contact_name}, {contact_title}
Brief: {link_to_attio_note}
```

### 5. Build the refresh workflow

Create a separate n8n workflow on a weekly cron schedule:
- Query all companies in the "Active Pipeline" list that have `account_brief_date` older than 30 days
- Re-run enrichment and brief generation for each
- Compare new brief against old brief; if significant changes detected (new funding, executive hire, competitor switch), send an alert

### 6. Build the scoring feedback loop

Create a workflow triggered by deal stage changes in Attio:
- When a deal moves to "Meeting Booked" or "Won," check which research signals were present
- Log to PostHog: `research_signal_converted` with properties: `signal_types_present`, `hook_used`, `research_depth`, `time_to_meeting`
- This data feeds the autonomous optimization loop at Durable level

### 7. Monitor pipeline health

Add error handling per `n8n-error-handling` patterns:
- If Clay enrichment fails, retry once after 60 seconds. If still failing, skip enrichment and generate a partial brief from CRM data only.
- If Anthropic API fails, queue for retry in 15 minutes.
- If Attio write fails, log the error and store the brief locally for manual import.
- Track daily: accounts processed, enrichment hit rate, API errors, average processing time.

## Output

- Fully automated account research pipeline: account enters target list, brief appears in Attio within 5 minutes
- AI-generated personalization hooks ready for immediate outreach
- Weekly refresh of stale account briefs
- Scoring feedback loop measuring which signals predict conversions

## Triggers

- Runs automatically when accounts are added to the target list
- Weekly refresh for pipeline accounts with stale briefs
- At Scalable level, handles 200+ accounts per month with no manual intervention
