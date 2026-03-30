---
name: gtm-tools-crm-clarify
description: Clarify-specific instructions for CRM tasks in GTM plays. Reference when the user's configured CRM is Clarify.
---

# Clarify — GTM Skills Reference

When a GTM skill says "log in your CRM" or "check your CRM", use Clarify as follows:

## Key objects
- **Contact** — individual person
- **Company** — organization
- **Opportunity** — deal/pipeline item
- **Note** — logged communication and context
- **Field** — custom attributes on any object

## Common tasks

### Log outreach activity
1. Open the Contact record
2. Add a Note with type (email, call, LinkedIn) and outcome
3. Set a custom field for "Sequence Status" if not already present
4. Schedule a follow-up reminder

### Build prospect lists
1. Use Clarify's filter views on Contacts or Companies
2. Filter by: job title, company size, industry, custom fields
3. Save as a named view for your outbound workflow

### Track sequence progress
1. Create a custom select field on Contact: "Sequence Status"
2. Values: Not Started → Active → Replied → Meeting Set → Closed
3. Update as you progress; use filtered views to manage daily work

### Sync with automation
- Use Clarify's API or Zapier/n8n integrations
- n8n: Clarify node (or HTTP request to Clarify API) to create contacts, log notes, update fields
- Connect email tool replies → Clarify contact status update via n8n webhook

### PostHog sync
- Push Clarify events to PostHog via n8n: `clarify.contact_created`, `clarify.opportunity_updated`, `clarify.meeting_booked`

## Tips
- Clarify is AI-native — it can auto-summarize meeting notes and suggest next actions
- Use Clarify's relationship intelligence to identify warm intro paths to prospects
- Good fit for founder-led sales where context and relationship history matter most
