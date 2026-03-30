---
name: gtm-tools-crm-attio
description: Attio-specific instructions for CRM tasks in GTM plays. Reference when the user's configured CRM is Attio.
---

# Attio CRM — GTM Skills Reference

When a GTM skill says "log in your CRM" or "check your CRM", use Attio as follows:

## Key objects
- **People** — individual contacts
- **Companies** — company records linked to people
- **Deals** — pipeline opportunities (if using Attio's deal tracking)
- **Lists** — custom collections of records (use for ICP target lists, outbound sequences, etc.)

## Common tasks

### Log an outreach touchpoint
1. Open the Person record
2. Add a Note with the touchpoint type (email, call, LinkedIn) and outcome
3. Set the Status attribute (e.g., "Contacted", "Replied", "Meeting Booked")
4. Set a follow-up task if needed

### Build an ICP list
1. Go to Lists → New List → People or Companies
2. Filter by attributes: industry, company size, role title, location
3. Save as a named list (e.g., "Q2 Outbound ICP — Series A SaaS")

### Track outbound sequence status
1. Create a custom attribute on People: "Sequence Status" (select: Not Started / In Sequence / Replied / Meeting Booked / Not Interested)
2. Update as you progress through outreach
3. Use list views filtered by Sequence Status for daily work

### Sync with email/automation
- Attio has native integrations with Instantly, Clay, and most email tools
- Use Attio's API or Zapier/n8n to push events from email tools to People records
- Webhook URL pattern: Settings → Integrations → Webhooks

### PostHog sync
- Push CRM events to PostHog via n8n: `crm.contact_created`, `crm.deal_updated`, `crm.meeting_booked`
- Use PostHog person properties to enrich with CRM data

## Tips
- Use Attio's email integration to auto-log sent/received emails to contact records
- Set up Views (filtered + sorted list views) for your daily outbound workflow
- Attio's AI enrichment can auto-fill company data from a domain or LinkedIn URL
