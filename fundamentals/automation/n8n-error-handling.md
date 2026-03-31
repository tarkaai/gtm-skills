---
name: n8n-error-handling
description: Add error handling and retry logic to n8n workflows
tool: n8n
difficulty: Intermediate
---

# Handle Errors in n8n Workflows

## Prerequisites
- At least one active n8n workflow
- Notification channel (Slack or email) for error alerts

## Steps

1. **Enable workflow error handling.** In workflow settings (gear icon), enable "Error Workflow" and select a dedicated error-handling workflow. This workflow receives error details (failed node, error message, input data) whenever any node in the main workflow fails.

2. **Build your error workflow.** Create a workflow named "Error Handler - Alerts". Add a Slack or Email node that sends the error details to your team channel. Include: workflow name, failed node name, error message, and timestamp. This ensures no failure goes unnoticed.

3. **Add retry logic to API nodes.** For HTTP Request and integration nodes that call external APIs, go to node Settings > "On Error" and select "Retry on Fail". Set max retries to 3 with increasing intervals (1s, 5s, 15s). Most API failures are transient and resolve on retry.

4. **Use try/catch patterns.** For critical workflow sections, add an Error Trigger node that catches failures from specific nodes. Route caught errors to a logging node and optionally continue the workflow with fallback data instead of stopping entirely.

5. **Handle rate limits.** When calling APIs that enforce rate limits (Clay, Apollo, Instantly), add a Wait node between iterations. Set a 1-2 second delay between API calls. For batch operations, use the Split In Batches node with a delay between batches.

6. **Monitor workflow execution.** Check n8n's Execution History daily during the first week of a new workflow. Filter by "Error" status to find failures. Common issues: expired API credentials (re-authenticate), changed API response format (update field mappings), and rate limiting (add delays).
