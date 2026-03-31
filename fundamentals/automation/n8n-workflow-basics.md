---
name: n8n-workflow-basics
description: Create and structure n8n workflows for GTM automation
tool: n8n
difficulty: Beginner
---

# Build Basic n8n Workflows

## Prerequisites
- n8n instance running (self-hosted or n8n Cloud)
- n8n MCP server connected (see `n8n-mcp-setup`) or API key configured
- Understanding of your automation goal (trigger, action, output)

## Steps

1. **Create a new workflow via MCP.** Use the n8n MCP `create_workflow` operation to create a workflow with a descriptive name following the convention: "[Category] [Action] [Destination]" (e.g., "Leads - Enrich New Signups - Attio"). Alternatively, use the n8n REST API:
   ```
   POST /api/v1/workflows
   { "name": "Leads - Enrich New Signups - Attio", "nodes": [], "connections": {} }
   ```

2. **Understand the node model.** n8n workflows are chains of nodes. Each node receives data, processes it, and passes it to the next. The first node is always a Trigger (what starts the workflow). Middle nodes transform or enrich data. The last node sends data somewhere (CRM, email tool, database).

3. **Add your trigger node.** Select the appropriate trigger type in the workflow definition:
   - **Webhook:** for real-time events from your app
   - **Schedule Trigger:** for periodic tasks (cron expressions)
   - **App trigger:** for events from specific tools (e.g., "Attio: Record Created")
   The trigger determines when your workflow runs.

4. **Add processing nodes.** Chain nodes to transform data. Common node types:
   - **HTTP Request:** call external APIs
   - **IF:** branch on conditions
   - **Set:** reshape data fields
   - **Code:** custom JavaScript for complex logic
   Define nodes and connections in the workflow JSON and update via the MCP or API.

5. **Connect nodes.** Define connections in the workflow's `connections` object. Each connection maps the output of one node to the input of the next. Test individual nodes using the n8n MCP `execute_workflow` operation with sample data before running the full workflow.

6. **Activate and test.** Use the n8n MCP to activate the workflow: `activate_workflow`. Run a manual test first using `execute_workflow` with sample data. Verify each node produces the expected output. Once confirmed, the workflow runs automatically when triggered.
