---
name: attio-lists
description: Build and manage dynamic and static lists in Attio for segmentation
tool: Attio
product: Attio
difficulty: Beginner
---

# Build Lists in Attio

## Prerequisites
- Attio workspace with contacts and companies populated
- Attio MCP server connected

## Steps

1. **Create static lists.** Use Attio Lists for fixed-membership groups like "Conference Attendees Q1" or "Pilot Customers." Add members manually or via the MCP. Static lists are snapshots — they don't auto-update.

2. **Create filtered views as dynamic lists.** For lists that should update automatically, use Attio's filtered views on the People or Company object. Example: "All contacts where Role Type = Decision Maker AND Last Contacted > 30 days ago" creates an evergreen re-engagement list.

3. **Build ICP target lists.** Create a Company view filtered by your ICP criteria: industry, employee count, location, and any custom fields. Then create a linked People view showing contacts at those companies. This two-layer approach keeps your targeting tight.

4. **Segment for campaigns.** Before any outreach campaign, build a dedicated list. Name it with the campaign and date: "Cold-Email-SaaS-Founders-2024-Q1." Export the list via MCP to feed into your email tool (Instantly or Smartlead).

5. **Maintain list hygiene.** Review lists monthly. Remove bounced emails, unsubscribes, and contacts marked "Do Not Contact." Archive old campaign lists rather than deleting them — you'll want the history for analysis.

6. **Count and validate.** Before using any list for outreach, pull the count via MCP and spot-check 5-10 records to verify the filters captured the right audience.
