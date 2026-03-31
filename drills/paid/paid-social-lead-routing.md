---
name: paid-social-lead-routing
description: Route leads from LinkedIn Lead Gen Forms and Meta Instant Forms into CRM, enrichment, and email nurture automatically
category: Paid
tools:
  - n8n
  - Attio
  - Clay
  - Loops
  - LinkedIn Ads
  - Meta Ads
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-crm-integration
  - n8n-email-integration
  - attio-contacts
  - attio-deals
  - clay-enrichment-waterfall
  - clay-scoring
  - loops-sequences
  - linkedin-ads-lead-gen-forms
  - meta-ads-lead-forms
---

# Paid Social Lead Routing

This drill automates the journey from "prospect filled out a lead form on LinkedIn/Meta" to "lead is enriched, scored, in CRM, and receiving a nurture email" — all within 5 minutes of submission. Speed matters: leads contacted within 5 minutes convert 9x better than those contacted after 30 minutes.

## Prerequisites

- LinkedIn Lead Gen Forms live (see `linkedin-ads-lead-gen-forms` fundamental)
- Meta Instant Forms live (see `meta-ads-lead-forms` fundamental)
- n8n instance running
- Attio CRM configured with a "Paid Social" lead source tag
- Clay account for enrichment
- Loops account with a nurture sequence ready

## Input

- Lead form submissions from LinkedIn and Meta
- ICP scoring criteria (from `icp-definition` drill)
- Nurture email sequence content (educational, not sales — matches the problem-aware stage)

## Steps

### 1. Build the LinkedIn lead ingestion workflow

Using the `n8n-triggers` and `n8n-workflow-basics` fundamentals, create an n8n workflow:

1. **Trigger**: Schedule node polling LinkedIn Lead Gen API every 15 minutes (or webhook if available)
   - Use `linkedin-ads-lead-gen-forms` fundamental for the API call
   - Store the last-polled timestamp to only fetch new submissions
2. **Extract fields**: Parse the lead response: first_name, last_name, email, job_title, company_name, company_size
3. **Deduplicate**: Check if email already exists in Attio using `attio-contacts`
   - If exists: update the contact with `lead_source: paid-social-linkedin` and add a note with the form name and submission date
   - If new: proceed to enrichment
4. **Enrich**: Send to Clay using `clay-enrichment-waterfall` to fill in: LinkedIn URL, company revenue, funding stage, tech stack, and any other ICP-relevant fields
5. **Score**: Apply ICP scoring using `clay-scoring`. Assign a lead_score (1-100)
6. **Create in Attio**: Using `attio-contacts`, create the contact with all enriched fields. Tag with `source: paid-social-linkedin`, `campaign: <campaign-name>`, `lead_score: <score>`
7. **Create deal**: If lead_score >= 70 (ICP match), create a deal in Attio using `attio-deals` with stage "New Lead"
8. **Trigger nurture**: Add to Loops using `loops-sequences`. If lead_score >= 70: send the "high-intent nurture" sequence. If lead_score < 70: send the "educational nurture" sequence.

### 2. Build the Meta lead ingestion workflow

Same structure as LinkedIn, but with Meta-specific ingestion:

1. **Trigger**: Subscribe to Meta `leadgen` webhook events on your Facebook Page. As a fallback, poll the Leads API every 15 minutes.
2. **Extract fields**: Parse form submission: full_name, email, job_title, company_name
3. **Steps 3-8**: Identical to LinkedIn workflow above. Tag with `source: paid-social-meta` instead.

### 3. Build the high-value lead alert

For leads scoring >= 80 (strong ICP match):

1. Send a Slack notification (or email) to the sales team with: name, company, title, lead score, which ad they responded to, and the form they filled out
2. Create a task in Attio to follow up within 24 hours
3. If you have Cal.com configured, include a suggested meeting link in the alert

### 4. Build the nurture email sequences in Loops

Using the `loops-sequences` fundamental, create two sequences:

**High-intent sequence (lead_score >= 70):**
- Email 1 (immediate): Deliver the promised resource (guide, checklist, etc.). Subject: "Here's your [resource name]"
- Email 2 (day 3): Share a related customer story. "How [company] solved [same problem]"
- Email 3 (day 7): Offer a conversation. "Want to discuss your specific [problem area]? Here's my calendar."
- Email 4 (day 14): Last touch. Share one more relevant resource. No hard sell.

**Educational sequence (lead_score < 70):**
- Email 1 (immediate): Deliver the resource.
- Email 2 (day 5): Share a related blog post or data point.
- Email 3 (day 12): Invite to a webinar or community.
- No sales ask. These leads may not be ICP. Nurture with value and let them self-select.

### 5. Set up lead quality feedback loop

Build an n8n workflow that runs weekly:

1. Pull all paid social leads created in the last 7 days from Attio
2. Check which ones progressed to "Meeting Booked" or "Qualified" stage
3. Calculate: leads submitted, leads enriched, leads scored >= 70, leads that booked meetings
4. Log these metrics as PostHog events: `paid_social_lead_quality_weekly`
5. If meeting rate from scored leads drops below 10%, trigger an alert to review audience targeting

### 6. Handle edge cases

- **Invalid emails**: If Clay enrichment returns an invalid email, tag the lead as "unverifiable" in Attio and skip the Loops sequence
- **Duplicate across platforms**: If the same person submits forms on both LinkedIn and Meta, merge into one Attio contact and attribute to the first touchpoint
- **Form spam**: If more than 5 leads from the same IP or domain in 1 hour, flag for manual review before CRM creation

## Output

- n8n workflow: LinkedIn lead ingestion (polling + enrichment + CRM + nurture)
- n8n workflow: Meta lead ingestion (webhook + enrichment + CRM + nurture)
- n8n workflow: High-value lead alert to sales
- n8n workflow: Weekly lead quality report
- Two Loops nurture sequences (high-intent and educational)
- PostHog events for lead quality tracking

## Triggers

- LinkedIn workflow: every 15 minutes
- Meta workflow: real-time via webhook, fallback poll every 15 minutes
- Lead quality report: weekly on Monday morning
