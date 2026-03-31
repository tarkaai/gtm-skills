---
name: attio-deals
description: Create, update, and manage deals in Attio throughout the sales cycle
tool: Attio
product: Attio
difficulty: Beginner
---

# Manage Deals in Attio

## Prerequisites
- Attio pipeline configured (see `attio-pipeline-config`)
- Attio MCP server connected

## Steps

1. **Create a deal.** Use the Attio MCP to create a new record on the Deal object. Always include: deal name (format: "Company - Opportunity"), associated company, primary contact, deal value, source, and expected close date.

2. **Move deals through stages.** Update the Status attribute when a deal progresses. Always add a note explaining why the stage changed — this creates an audit trail for pipeline reviews.

3. **Log activities.** After every touchpoint (email, call, meeting), create a note on the deal with the date, type, summary, and next step. This feeds your activity-based reporting.

4. **Update deal values.** When pricing discussions happen, update the deal value immediately. If the deal scope changes, note the reason for the value change.

5. **Close deals.** When closing won: set Status to Closed Won, record the actual close date, and update final deal value. When closing lost: set Status to Closed Lost and add a "Lost Reason" from your predefined list (Price, Timing, Competitor, No Decision, Bad Fit).

6. **Batch operations.** For bulk deal updates (e.g., marking stale deals), use the Attio MCP to query deals matching your criteria, then update them in a loop. Always log what changed and why.
