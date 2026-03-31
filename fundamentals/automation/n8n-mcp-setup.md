---
name: n8n-mcp-setup
description: Install and configure the n8n MCP server for Claude Code integration
tool: n8n
product: n8n
difficulty: Setup
---

# Set Up n8n MCP Server

## Prerequisites
- n8n instance running (self-hosted or cloud)
- n8n API key generated (Settings > API > Create API Key)
- Claude Code installed with MCP support

## Steps

1. **Install the n8n MCP server.** Add the n8n MCP server to your Claude Code configuration. In your `.claude/settings.json` or MCP config file, add the n8n server with your instance URL and API key. The MCP server wraps n8n's REST API for use by Claude Code.

2. **Configure authentication.** Set the n8n API key as an environment variable: `N8N_API_KEY=your-key-here`. Set the base URL: `N8N_BASE_URL=https://your-n8n-instance.com`. The MCP server uses these to authenticate API calls.

3. **Verify the connection.** Ask Claude Code to list your n8n workflows. The MCP server should return your active workflows with their names, IDs, and status. If you get an authentication error, double-check your API key and base URL.

4. **Understand available operations.** The n8n MCP server supports: listing workflows, getting workflow details, creating new workflows, activating/deactivating workflows, executing workflows manually, and reading execution history. These operations let Claude Code manage your automation directly.

5. **Set up workflow templates.** Create a few template workflows in n8n that Claude Code can duplicate and customize: "Template - CRM Sync", "Template - Email Campaign Trigger", "Template - Scheduled Report". This gives the agent starting points rather than building from scratch.

6. **Test end-to-end.** Ask Claude Code to create a simple workflow using the MCP server: a Schedule Trigger that sends a Slack message. Verify the workflow appears in your n8n instance and runs correctly. This confirms the full integration is working.
