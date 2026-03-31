---
name: posthog-mcp-setup
description: Install and configure the PostHog MCP server for Claude Code integration
tool: PostHog
difficulty: Setup
---

# Set Up PostHog MCP Server

## Prerequisites
- PostHog account with a project API key and personal API key
- Claude Code installed with MCP support

## Steps

1. **Generate API keys.** Via the PostHog API or dashboard, create a personal API key with read access to all resources. Note the Project API Key from project settings. You need both: the personal key for querying and the project key for event ingestion.

2. **Install the MCP server.** Add the PostHog MCP server to your Claude Code MCP config file (`.claude/settings.json` or project-level `.mcp.json`):

```json
{
  "posthog": {
    "command": "npx",
    "args": ["-y", "@anthropic/posthog-mcp"],
    "env": {
      "POSTHOG_API_KEY": "<personal-api-key>",
      "POSTHOG_PROJECT_ID": "<project-id>",
      "POSTHOG_HOST": "https://app.posthog.com"
    }
  }
}
```

For self-hosted PostHog, set `POSTHOG_HOST` to your instance URL.

3. **Verify the connection.** After restarting Claude Code, use the MCP to query recent events. Expected successful output: a list of event objects with `event`, `timestamp`, and `properties` fields. Authentication errors indicate an incorrect personal API key or project ID.

4. **Available MCP operations.** The PostHog MCP server supports:
   - `query_events` -- fetch events with filters
   - `run_hogql_query` -- execute HogQL (PostHog SQL dialect) queries
   - `list_feature_flags` -- read flag configurations
   - `get_experiment_results` -- read A/B test outcomes
   - `get_insight` -- fetch saved insight data
   - `query_persons` -- look up user records and cohort membership

5. **Test HogQL access.** Run a test query through the MCP:
```sql
SELECT count() FROM events WHERE event = 'signup_completed' AND timestamp > now() - interval 7 day
```
Verify the query executes and returns a numeric result. HogQL is the primary interface for ad-hoc PostHog analysis.

6. **Security.** Store API keys in environment variables or a `.env` file listed in `.gitignore`. Never commit keys to version control. Rotate keys immediately if exposed.
