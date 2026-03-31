---
name: youtube-preroll-lead-routing
description: Route leads from YouTube pre-roll ad interactions to CRM with enrichment, scoring, and nurture sequence triggering
category: Paid
tools:
  - Google Ads
  - n8n
  - Attio
  - Clay
  - Loops
  - PostHog
fundamentals:
  - google-ads-youtube-reporting
  - google-ads-conversion-tracking
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-crm-integration
  - attio-contacts
  - attio-deals
  - clay-enrichment-waterfall
  - clay-scoring
  - loops-sequences
  - posthog-custom-events
---

# YouTube Pre-roll Lead Routing

Route conversions from YouTube pre-roll campaigns into your CRM. YouTube pre-roll ads generate leads differently from social ads: instead of native lead gen forms, conversions happen on your landing page (form submission, resource download, or Cal.com booking). This drill sets up the workflow from landing page conversion through enrichment, ICP scoring, CRM creation, nurture triggering, and team notification.

## Prerequisites

- Landing page with form submission tracking
- PostHog installed on landing page for event tracking
- Google Ads conversion tracking configured (see `google-ads-conversion-tracking`)
- n8n instance running
- Attio CRM configured
- Clay account for enrichment
- Loops for email nurture sequences

## Input

- Landing page URL(s) used in YouTube pre-roll campaigns
- UTM parameter scheme from `youtube-preroll-creative-pipeline`
- ICP scoring criteria (from Clay)
- Nurture sequence content (problem-aware educational emails)

## Steps

### 1. Configure landing page conversion tracking

Set up PostHog to capture form submissions on your landing page(s):

Using `posthog-custom-events`, fire these events:
- `yt_preroll_page_view` — landing page loaded. Properties: all UTM params, referrer, device type.
- `yt_preroll_form_start` — user starts filling out the form (first field interaction).
- `yt_preroll_form_submit` — form submitted successfully. Properties: email (hashed), company name, UTM params.
- `yt_preroll_resource_download` — resource actually downloaded/accessed after form submission.

Also configure Google Ads conversion tracking: fire a Google Ads conversion tag on `yt_preroll_form_submit` so Google can optimize bidding based on actual conversions. Use the `google-ads-conversion-tracking` fundamental.

### 2. Build the lead routing n8n workflow

Create an n8n workflow triggered by the form submission webhook:

**Trigger:** Webhook from your form tool (Webflow, Tally, Typeform) or PostHog webhook on `yt_preroll_form_submit`.

**Step 1 — Deduplicate:**
- Query Attio using `attio-contacts` to check if this email already exists
- If exists: update the existing contact with `source: youtube-preroll`, add the campaign UTMs as a note, skip to Step 5 (nurture)
- If new: continue to Step 2

**Step 2 — Enrich:**
- Send the email + company name to Clay using `clay-enrichment-waterfall`
- Clay returns: full name, job title, seniority, company size, industry, funding stage, LinkedIn URL, tech stack
- If Clay returns no data (disposable email, consumer email): flag as "low quality" and route to a minimal nurture sequence instead of the full pipeline

**Step 3 — Score:**
- Run the enriched data through Clay ICP scoring using `clay-scoring`
- Score 0-100 based on: title match, seniority match, company size match, industry match, tech stack match
- Classify: High (80-100), Medium (50-79), Low (0-49)

**Step 4 — Create in CRM:**
- Using `attio-contacts`, create a new contact in Attio with:
  - Standard fields: name, email, company, title
  - Custom attributes: `source: youtube-preroll`, `campaign_id`, `ad_variant_id`, `pain_point`, `hook_type` (all from UTM params)
  - Score: ICP score from Clay
  - Status: "New Lead"

**Step 5 — Trigger nurture:**
- Using `loops-sequences`, add the contact to a problem-aware nurture sequence:
  - High score (80+): 3-email sequence over 7 days, with a Cal.com meeting link in email 3
  - Medium score (50-79): 5-email sequence over 14 days, educational content only, meeting link in email 5
  - Low score (0-49): Single email with the resource they requested, no follow-up

**Step 6 — Alert team (high-value leads only):**
- If ICP score >= 80: send a Slack notification:
  ```
  New high-value lead from YouTube preroll
  Name: {name}
  Company: {company} ({employee_count} employees)
  Title: {title}
  ICP Score: {score}
  Campaign: {campaign_name}
  Ad variant: {variant_id}
  ```
- If ICP score >= 90 AND company size > 100: also create a task in Attio for immediate outreach

**Step 7 — Log to PostHog:**
- Fire `yt_preroll_lead_enriched` with properties: score, score_tier, company_size, industry
- Fire `yt_preroll_lead_routed` with properties: nurture_sequence_id, alert_sent (true/false)

### 3. Set up meeting booking tracking

If a nurtured lead books a meeting via Cal.com:
- n8n listens for Cal.com webhook on new booking
- Match the booking email to the Attio contact
- Update the contact status to "Meeting Booked"
- Fire PostHog event: `yt_preroll_meeting_booked` with properties: lead_source, campaign_id, days_from_lead_to_meeting
- Attribute the meeting back to the original YouTube ad variant for ROAS calculation

### 4. Handle edge cases

- **Form spam:** If the form submission has no valid email or a known spam domain (from a blocklist), drop it and log `yt_preroll_spam_blocked` in PostHog.
- **Enrichment failure:** If Clay returns no data after 3 retries, create the contact in Attio with `enrichment_status: failed` and schedule a re-enrichment in 24 hours.
- **Duplicate with different campaign:** If the contact exists but came from a different campaign, add the new campaign as a secondary source attribution. Do not overwrite the original source.

## Output

- n8n workflow: form submission → dedup → enrich → score → CRM → nurture → alert
- All leads in Attio with source attribution, ICP score, and campaign UTMs
- High-value leads trigger Slack alerts and CRM tasks
- PostHog events for the full routing pipeline (enables funnel analysis)
- Meeting bookings attributed back to YouTube ad variants

## Triggers

- **Real-time:** Runs on every form submission (webhook-triggered)
- **Daily:** Batch re-enrichment of any contacts with `enrichment_status: failed`
- **Weekly:** Refresh exclusion list export from Attio to Google Ads (prevent targeting existing leads)
