---
name: attio-pipeline-config
description: Configure your Attio sales pipeline with stages, required fields, and views
tool: Attio
difficulty: Setup
---

# Configure Your Attio Sales Pipeline

## Prerequisites
- Attio workspace with admin access
- Attio MCP server connected (see `fundamentals/crm/attio-mcp-setup`)

## Steps

1. **Create your pipeline.** In Attio, go to Objects and create a Deal object if it doesn't exist. Add a Status attribute with type "Status" to serve as your pipeline stages.

2. **Define stages.** Add these stages in order: Lead, Qualified, Meeting Booked, Proposal Sent, Negotiation, Closed Won, Closed Lost. Adjust names to match your sales process but keep the count between 5-8 stages.

3. **Add required fields.** For each deal, configure these attributes as required: Company (relationship), Contact (relationship), Deal Value (currency), Expected Close Date (date), Source (select — Outbound, Inbound, Referral, Event).

4. **Create views.** Build a Kanban view grouped by Status for daily pipeline review. Add a List view filtered to "Expected Close Date is within next 30 days" for forecasting. Create a "Stale Deals" view filtering deals with no activity in 14+ days.

5. **Set up calculated fields.** Add a "Days in Stage" formula field to track how long deals sit in each stage. This powers your velocity reporting later.

6. **Verify via MCP.** Use the Attio MCP to list your pipeline stages and confirm the configuration is correct: query the Deal object schema and validate all required fields are present.
