---
name: n8n-workflow-basics
description: Create and structure n8n workflows for GTM automation
tool: n8n
difficulty: Beginner
---

# Build Basic n8n Workflows

## Prerequisites
- n8n instance running (self-hosted or n8n Cloud)
- Understanding of your automation goal (trigger, action, output)

## Steps

1. **Create a new workflow.** In n8n, click "New Workflow" and give it a descriptive name following the convention: "[Category] [Action] [Destination]" (e.g., "Leads - Enrich New Signups - Attio"). This naming helps you find workflows as your count grows.

2. **Understand the node model.** n8n workflows are chains of nodes. Each node receives data, processes it, and passes it to the next. The first node is always a Trigger (what starts the workflow). Middle nodes transform or enrich data. The last node sends data somewhere (CRM, email tool, database).

3. **Add your trigger node.** Select the appropriate trigger: Webhook (for real-time events from your app), Schedule (for periodic tasks), or an app-specific trigger (e.g., "Attio: Record Created"). The trigger determines when your workflow runs.

4. **Add processing nodes.** Chain nodes to transform data. Common patterns: HTTP Request node (call external APIs), IF node (branch on conditions), Set node (reshape data fields), Code node (custom JavaScript for complex logic).

5. **Connect nodes.** Drag connections between nodes to define the data flow. Each connection passes the output of one node as input to the next. Use the "Test step" button on each node to verify it processes data correctly before running the full workflow.

6. **Activate and test.** Run the workflow manually first using "Test Workflow" with sample data. Verify each node produces the expected output. Once confirmed, toggle the workflow to Active so it runs automatically when triggered.
