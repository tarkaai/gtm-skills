---
name: gtm-tools-crm-salesforce
description: Salesforce-specific instructions for CRM tasks in GTM plays. Reference when the user's configured CRM is Salesforce.
---

# Salesforce — GTM Skills Reference

When a GTM skill says "log in your CRM" or "check your CRM", use Salesforce as follows:

## Key objects
- **Lead** — unqualified prospect (pre-conversion)
- **Contact** — qualified individual linked to an Account
- **Account** — company record
- **Opportunity** — active deal in pipeline
- **Task / Activity** — logged touchpoints (calls, emails, meetings)
- **Campaign** — marketing campaign tracking

## Common tasks

### Log an outreach touchpoint
1. Open the Lead or Contact record
2. Click "Log a Call" or "New Task"
3. Set Type (Call / Email / LinkedIn), Status (Completed), and add notes
4. Set a follow-up Task with a due date

### Build an ICP prospect list
1. Use Reports → New Report → Leads or Contacts
2. Filter by: Industry, Title (contains "VP" / "Head of" / "Founder"), Company Size, Lead Source
3. Save and export to CSV or use as a view for outreach

### Track sequence status
1. Add a custom field to Lead: "Sequence Status" (picklist: Not Started / Active / Replied / Meeting Set / Disqualified)
2. Update via Flow or manually as prospects progress
3. Use List Views filtered by Sequence Status

### Sync with email/automation tools
- Instantly → Salesforce: use Zapier or Make trigger on "Reply received" to update Lead Status
- n8n: use Salesforce node to create/update records, log activities, trigger follow-ups

### PostHog sync
- Use n8n Salesforce → PostHog workflow: capture `salesforce.opportunity_created`, `salesforce.lead_converted`, `salesforce.meeting_booked`
- Map Salesforce record IDs to PostHog distinct_id for unified customer view

## Tips
- Use Salesforce Flows (no-code automation) to auto-assign Leads, send alerts, and update fields on status change
- For outbound at scale, connect Salesforce Engage or a sequencing tool (Outreach, Salesloft) rather than logging manually
- Keep Lead → Contact conversion disciplined: only convert when the person is qualified (passes BANT or equivalent)
