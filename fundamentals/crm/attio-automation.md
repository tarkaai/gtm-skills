---
name: attio-automation
description: Set up Attio automations for deal routing, task creation, and notifications
tool: Attio
difficulty: Intermediate
---

# Automate Workflows in Attio

## Prerequisites
- Attio pipeline and contacts configured
- Attio MCP server connected
- n8n available for complex automations

## Steps

1. **Set up stage-change triggers.** Use n8n with the Attio MCP to watch for deal stage changes. When a deal moves to "Meeting Booked," automatically create a task to prepare the meeting brief. When it moves to "Proposal Sent," set a 3-day follow-up reminder.

2. **Auto-assign deals.** Build an n8n workflow that routes new deals based on criteria: deals over $50K go to a senior rep, deals from inbound go to the inbound team, deals from specific industries go to the specialist. Update the Owner field on the deal automatically.

3. **Create follow-up tasks.** When a deal has no activity for 7 days, trigger an n8n workflow that creates a task in Attio: "Follow up on [Deal Name] — no activity for 7 days." Assign it to the deal owner.

4. **Notify on key events.** Set up n8n triggers for high-value events: deal closed won (notify the team), deal moved to Closed Lost (trigger a loss review task), new deal created over threshold value (alert leadership).

5. **Sync contact status.** When a contact's email bounces in Instantly or Smartlead, update their status in Attio to "Bounced" via n8n. This prevents you from including bad addresses in future campaigns.

6. **Test your automations.** Create a test deal and manually move it through each stage. Verify every trigger fires correctly and every task/notification appears as expected before going live.
