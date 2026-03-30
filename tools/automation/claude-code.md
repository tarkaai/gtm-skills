---
name: gtm-tools-automation-claude-code
description: Claude Code-specific instructions for automation tasks in GTM plays. Reference when the user's configured automation platform is Claude Code.
---

# Claude Code — GTM Skills Reference

When a GTM skill says "set up automation" or "build a workflow", use Claude Code as follows:

## How Claude Code fits into GTM plays

At **Scalable** and **Durable** levels, plays require automation workflows. With Claude Code as your automation platform, you orchestrate these workflows by writing scripts and agents directly — rather than using a visual workflow builder like n8n.

## Common patterns

### Scalable: Build a script-based workflow
1. Claude Code writes a Node.js or Python script that:
   - Fetches new leads from Clay/Apollo API
   - Enriches and scores them
   - Adds to your email tool (Instantly API) or CRM
   - Logs events to PostHog
2. Run on a schedule via cron or a cloud function (Vercel, Railway, Fly.io)

### Scalable: Event-driven via webhooks
1. Deploy a small Express/Fastify endpoint (Claude Code writes it)
2. Point email tool or CRM webhook to your endpoint
3. Endpoint processes event → updates CRM → logs to PostHog
4. Deploy to Vercel serverless functions (Claude Code handles this)

### Durable: AI agent workflows
1. Claude Code creates an agent using the Anthropic SDK or Claude Code SDK
2. Agent runs on a schedule:
   - Reads PostHog experiment results
   - Decides which email variant is winning
   - Updates the active sequence in your email tool via API
   - Logs decision rationale + PostHog event
3. Agent surfaces weekly report: what improved, what to retire, next experiments

### Durable: Continuous optimization loop
```javascript
// Example agent loop (Claude Code writes this)
async function optimizationLoop() {
  const results = await posthog.getExperimentResults(experimentId);
  const winner = results.variants.find(v => v.conversionRate > baseline * 1.1);
  if (winner) {
    await emailTool.setActiveVariant(winner.id);
    await posthog.capture('agent.optimization.applied', { winner: winner.id });
  }
}
```

## Tips
- For Smoke/Baseline plays, skip automation — run manually and focus on signal
- Use Claude Code's file system tools to manage local CSVs, logs, and config files between runs
- Store API keys in `.env` files (never commit); Claude Code reads these automatically
- For scheduling, use Vercel Cron or a simple Railway deployment — Claude Code sets this up
- Claude Code can write, test, and deploy the full automation stack in one session
