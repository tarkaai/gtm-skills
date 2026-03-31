---
name: n8n-crm-integration
description: Connect n8n workflows to Attio CRM for automated data sync
tool: n8n
difficulty: Intermediate
---

# Integrate n8n with Your CRM

## Prerequisites
- n8n instance running
- Attio account with API key (see `fundamentals/crm/attio-mcp-setup`)

## Steps

1. **Set up Attio credentials in n8n.** Go to n8n Settings > Credentials > New Credential. Select "Attio" (or use HTTP Header Auth with your Attio API key if the native node is not available). Test the connection by making a simple API call to list your workspace objects.

2. **Create contacts from enriched leads.** Build a workflow: Trigger (webhook from Clay or CSV upload) > Set node (map fields to Attio schema) > Attio node (Create/Update Contact). Map fields: email_address, first_name, last_name, company, title, source. Use "Update if exists" to prevent duplicates.

3. **Create deals from positive signals.** Build a workflow: Trigger (email reply webhook or form submission) > IF node (filter for positive intent) > Attio node (Create Deal). Set the deal stage to "Lead" or "Meeting Requested" and associate it with the contact and company records.

4. **Sync activity data.** After sending emails or booking meetings, push activity records to Attio. Build a workflow that receives events from your email tool and creates Attio notes or activities on the relevant contact record. This gives your sales team full context.

5. **Bi-directional sync.** Set up an Attio trigger in n8n that fires when a deal stage changes. Use this to trigger downstream actions: deal moved to "Closed Won" triggers a welcome email in Loops, deal moved to "Closed Lost" triggers a feedback survey.

6. **Test the full loop.** Create a test contact in n8n, verify it appears in Attio, change the contact's deal stage in Attio, and verify n8n receives the event. This end-to-end test confirms your integration works in both directions.
