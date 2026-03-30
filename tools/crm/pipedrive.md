---
name: gtm-tools-crm-pipedrive
description: Pipedrive-specific instructions for CRM tasks in GTM plays. Reference when the user's configured CRM is Pipedrive.
---

# Pipedrive — GTM Skills Reference

When a GTM skill says "log in your CRM" or "check your CRM", use Pipedrive as follows:

## Key objects
- **Person** — individual contact
- **Organization** — company linked to persons
- **Deal** — pipeline opportunity (Pipedrive is deal-centric)
- **Activity** — logged touchpoints (call, email, meeting, LinkedIn)
- **Lead** — pre-deal prospect in the Leads Inbox

## Common tasks

### Log a touchpoint
1. Open the Deal or Person record
2. Click "+ Activity" → select type, set done, add outcome notes
3. Schedule the next activity

### Manage outbound prospects
1. Use the **Leads Inbox** for unqualified prospects
2. Promote to Deal when they pass qualification criteria
3. Use custom fields on Person/Deal for sequence status

### Build a prospect list
1. People → Filters → add: Job Title contains, Organization size, etc.
2. Save as a named filter
3. Export or use with email integration

### Sync with email/automation
- Pipedrive has native email sync (Gmail/Outlook)
- Use n8n Pipedrive node to create Deals, log Activities, update stages
- Zapier: connect Instantly/Smartlead reply events → update Pipedrive Person stage

### PostHog sync
- Push Pipedrive events to PostHog via n8n: `pipedrive.deal_created`, `pipedrive.deal_won`, `pipedrive.activity_completed`

## Tips
- Pipedrive is pipeline-centric — great for sales-heavy plays where deal tracking is the priority
- Use Pipedrive's Smart Docs (proposals) for the Proposed stage plays
- Automations (if/then workflows) can auto-move deals, assign owners, and send reminders
