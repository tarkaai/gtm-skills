---
name: gtm-tools-crm-hubspot
description: HubSpot-specific instructions for CRM tasks in GTM plays. Reference when the user's configured CRM is HubSpot.
---

# HubSpot — GTM Skills Reference

When a GTM skill says "log in your CRM" or "check your CRM", use HubSpot as follows:

## Key objects
- **Contact** — individual prospect or customer
- **Company** — organization linked to contacts
- **Deal** — pipeline opportunity
- **Ticket** — support/CS case
- **List** — static or smart (dynamic) contact/company lists

## Common tasks

### Log an outreach touchpoint
1. Open the Contact record
2. Click "Log Activity" → select type (Email / Call / LinkedIn message)
3. Add outcome notes and set next activity date

### Build an ICP prospect list
1. Contacts → Lists → Create List → Active (dynamic) List
2. Set filters: Job Title contains, Company Size between, Industry is
3. Name it clearly (e.g., "ICP — Series A Fintech CTOs")
4. Use this list for sequences or ad audiences

### Run an email sequence
1. Sales Hub → Sequences → Create Sequence
2. Add steps: email day 1, follow-up day 4, LinkedIn day 7, final email day 10
3. Enroll contacts from the ICP list

### Sync with automation
- HubSpot has native n8n and Zapier nodes
- Use HubSpot workflows (no-code) to trigger on Contact property changes
- Connect to PostHog via n8n: push HubSpot timeline events as PostHog events

### PostHog sync
- Use HubSpot → n8n → PostHog: `hubspot.contact_created`, `hubspot.deal_stage_changed`, `hubspot.meeting_booked`
- Enrich PostHog persons with HubSpot lifecycle stage

## Tips
- HubSpot's free CRM tier is surprisingly capable for Smoke/Baseline levels
- Use HubSpot's meeting scheduler link (free) instead of Calendly for a unified experience
- Marketing Hub's smart lists are powerful for ABM — target companies by engagement score
