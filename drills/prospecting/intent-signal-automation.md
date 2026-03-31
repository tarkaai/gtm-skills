---
name: intent-signal-automation
description: Automate the collection, scoring, and routing of intent signals from website visitors, G2, and enrichment sources into your CRM via n8n
category: Prospecting
tools:
  - n8n
  - Clay
  - Attio
  - PostHog
  - RB2B
fundamentals:
  - website-visitor-identification
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-crm-integration
  - clay-intent-scoring
  - attio-lists
  - attio-deals
  - posthog-custom-events
---

# Intent Signal Automation

This drill builds always-on n8n workflows that collect intent signals in real time, route them to Clay for scoring, and push scored accounts into Attio for outreach. It replaces manual signal checking with an automated pipeline.

## Input

- Working intent score model (from `intent-score-model` drill)
- Website visitor identification tool installed and sending data (RB2B, Koala, or Leadpipe)
- n8n instance with API credentials for Clay, Attio, and PostHog
- Attio CRM with intent-related custom attributes configured

## Steps

### 1. Build the website visitor signal workflow

Create an n8n workflow triggered by a webhook from your visitor identification tool:

**Trigger:** Webhook node receiving POST from RB2B/Koala when a visitor is identified.

**Flow:**
1. **Webhook receive** — parse the visitor payload (company_domain, contact_email, pages_viewed, visit_count)
2. **Filter node** — drop visitors who viewed only the homepage or blog index (low signal). Keep visitors who viewed pricing, case studies, docs, or demo pages.
3. **Clay HTTP node** — POST the visitor data to your Clay intent scoring table using `clay-intent-scoring`. Match on company_domain. Update website_visits_30d and pricing_page_viewed columns.
4. **Wait node** — pause 30 seconds for Clay enrichment to complete
5. **Clay HTTP GET** — retrieve the updated row with the computed intent_score and intent_tier
6. **Switch node** — route by tier:
   - Hot (70+): Create or update Attio deal at "Intent Signal" stage using `attio-deals`. Send Slack notification to founder.
   - Warm (40-69): Add to Attio "Warm Intent" list using `attio-lists`. No immediate notification.
   - Cool/Cold: Log in PostHog only. No CRM action.
7. **PostHog node** — log `intent_signal_received` event with all properties using `posthog-custom-events`

### 2. Build the G2/third-party intent workflow

Create a second n8n workflow for third-party intent signals:

**Trigger:** Webhook from G2 buyer intent, or a scheduled cron (daily at 8am) that polls the G2 API.

**Flow:**
1. **Receive/poll** — get new G2 intent signals since last check
2. **Loop node** — iterate over each signal
3. **Clay HTTP node** — update the Clay scoring table with g2_signal_type and g2_activity_level
4. **Score retrieval** — same as above
5. **Route by tier** — same as above
6. **Dedup check** — before creating an Attio record, check if this company already has an active deal. If yes, update the existing deal notes with the new signal rather than creating a duplicate.

### 3. Build the enrichment signal workflow

Create a third n8n workflow that runs weekly (Sunday evening) to refresh contextual signals:

**Trigger:** n8n cron node, weekly

**Flow:**
1. **Attio HTTP node** — pull all accounts in the target account list from Attio
2. **Clay HTTP node** — for each account, trigger Clay enrichment refresh: funding status, job postings, new hires, tech stack changes
3. **Score recalculation** — Clay automatically recalculates intent_score with updated data
4. **Tier change detection** — compare new tier to previous tier stored in Attio
5. **Alert on tier upgrades** — if an account moved from Cool/Cold to Warm/Hot, send a Slack alert and create an Attio task for outreach
6. **Alert on tier downgrades** — if a Hot account dropped to Cool/Cold (signals decayed), log in PostHog and remove from active outreach queue

### 4. Configure error handling and monitoring

For each workflow:
- Add an error trigger node that sends failures to Slack with the error message and workflow name
- Set retry logic: 3 retries with exponential backoff (30s, 60s, 120s)
- Create a daily health check workflow that verifies all three signal workflows executed successfully in the last 24 hours

### 5. Test the full pipeline

1. Visit your own website pricing page from a non-company IP (use a mobile hotspot)
2. Verify the visitor signal fires, reaches n8n, updates Clay, and routes to Attio
3. Manually trigger a test G2 webhook with sample data
4. Verify enrichment refresh runs and decay is applied correctly
5. Confirm PostHog events are logging for all signal types

## Output

- Three always-on n8n workflows: website visitors, third-party intent, enrichment refresh
- Real-time signal-to-CRM pipeline with automated scoring and routing
- Slack alerts for Hot-tier signals
- PostHog event trail for every signal received and routed

## Triggers

- Website visitor workflow: real-time (webhook-triggered)
- Third-party intent workflow: real-time (webhook) or daily (cron)
- Enrichment refresh workflow: weekly (cron)
