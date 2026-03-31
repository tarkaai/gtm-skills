---
name: attio-pipeline-config
description: Configure your Attio sales pipeline with stages, required fields, and views
tool: Attio
difficulty: Setup
---

# Configure Your Attio Sales Pipeline

## Prerequisites
- Attio workspace with admin access
- Attio MCP server connected (see `attio-mcp-setup`)

## Steps

1. **Create your pipeline via MCP.** Use the Attio MCP to create a Deal object if it does not exist. Create a Status attribute with type "Status" to serve as your pipeline stages. The MCP `create_object` and `create_attribute` operations handle this programmatically.

2. **Define stages via API.** Add stages in order using the Attio API or MCP:
   - Lead
   - Qualified
   - Meeting Booked
   - Proposal Sent
   - Negotiation
   - Closed Won
   - Closed Lost

   Adjust names to match your sales process but keep the count between 5-8 stages.

3. **Add required fields.** Configure these attributes on the Deal object via the MCP: Company (relationship), Contact (relationship), Deal Value (currency), Expected Close Date (date), Source (select: Outbound, Inbound, Referral, Event). Use `create_attribute` for each.

4. **Create filtered views via MCP.** Build views programmatically:
   - Kanban view grouped by Status for daily pipeline review
   - List view filtered to "Expected Close Date within next 30 days" for forecasting
   - "Stale Deals" view filtering deals with no activity in 14+ days

5. **Set up calculated fields.** Add a "Days in Stage" formula field to track how long deals sit in each stage. This powers velocity reporting later. Use the Attio API to define the formula attribute.

6. **Verify configuration.** Use the Attio MCP to list your pipeline stages and validate all required fields are present:
   ```
   Query the Deal object schema → confirm Status attribute has correct stages
   Query Deal attributes → confirm Company, Contact, Value, Close Date, Source exist
   ```
