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

1. **Generate API keys.** In PostHog, go to Settings > Personal API Keys and create a new key with read access to all resources. Note your Project API Key (from Project Settings) as well. You need both: the personal key for querying and the project key for event ingestion.

2. **Install the PostHog MCP server.** Add the PostHog MCP server configuration to your Claude Code MCP config. Set the required environment variables: `POSTHOG_API_KEY` (personal API key), `POSTHOG_PROJECT_ID` (your project ID), and `POSTHOG_HOST` (https://app.posthog.com for cloud, or your self-hosted URL).

3. **Verify the connection.** Ask Claude Code to query recent events from PostHog. The MCP server should return event data. If you get authentication errors, verify your personal API key has the correct scopes and your project ID is correct.

4. **Understand available operations.** The PostHog MCP server supports: querying events, running HogQL queries, listing feature flags, reading experiment results, fetching insight data, and querying persons/cohorts. This lets Claude Code analyze your data and build insights programmatically.

5. **Set up HogQL access.** The most powerful PostHog MCP capability is running HogQL queries -- PostHog's SQL dialect. Claude Code can write and execute queries like: "SELECT count() FROM events WHERE event = 'signup_completed' AND timestamp > now() - interval 7 day". This enables ad-hoc analysis.

6. **Test a practical query.** Ask Claude Code to use the PostHog MCP to answer a GTM question: "What was our signup conversion rate this week vs last week?" Verify the query runs, returns accurate data, and Claude Code interprets the results correctly.
