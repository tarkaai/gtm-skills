---
name: n8n-error-handling
description: Add error handling and retry logic to n8n workflows
tool: n8n
product: n8n
difficulty: Intermediate
---

# Handle Errors in n8n Workflows

## Prerequisites
- At least one active n8n workflow
- Notification channel (Slack or email) for error alerts

## Steps

1. **Enable workflow error handling.** In the workflow settings JSON, set `"onError": "errorWorkflow"` and reference a dedicated error-handling workflow by ID. This workflow receives error details (failed node, error message, input data) whenever any node in the main workflow fails. Configure via the n8n MCP or API:
   ```
   PATCH /api/v1/workflows/<id>
   { "settings": { "errorWorkflow": "<error-workflow-id>" } }
   ```

2. **Build your error workflow.** Create a workflow named "Error Handler - Alerts" via the n8n MCP. Add a Slack or Email node that sends error details to your team channel. Include: workflow name, failed node name, error message, and timestamp. This ensures no failure goes unnoticed.

3. **Add retry logic to API nodes.** For HTTP Request and integration nodes that call external APIs, configure retry settings in the node parameters:
   ```json
   { "onError": "retryOnFail", "maxRetries": 3, "retryIntervalMs": [1000, 5000, 15000] }
   ```
   Most API failures are transient and resolve on retry.

4. **Use try/catch patterns.** For critical workflow sections, add an Error Trigger node that catches failures from specific nodes. Route caught errors to a logging node and optionally continue the workflow with fallback data instead of stopping entirely.

5. **Handle rate limits.** When calling APIs that enforce rate limits (Clay, Apollo, Instantly), add a Wait node between iterations. Set a 1-2 second delay between API calls. For batch operations, use the Split In Batches node with a delay between batches.

6. **Monitor workflow execution.** Use the n8n MCP `get_executions` operation or API (`GET /api/v1/executions?status=error`) to check for failures daily during the first week of a new workflow. Common issues: expired API credentials (re-authenticate), changed API response format (update field mappings), and rate limiting (add delays).
