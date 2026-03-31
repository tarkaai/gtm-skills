---
name: anthropic-api-patterns
description: Use the Claude API for GTM automation — content generation, lead scoring, and agent workflows
tool: Anthropic
product: Claude API
difficulty: Config
---

# Claude API Patterns for GTM

### When to use the Claude API
At Durable level, plays need AI that monitors, decides, and acts. Claude handles: content personalization, lead scoring narratives, competitive analysis, and agent-driven optimization loops.

### Key patterns
1. **Content generation:** Use Claude to draft email copy, social posts, and landing page variants. Always provide context: ICP description, tone guidelines, and 2-3 examples of what works.
2. **Lead scoring narratives:** Feed Clay enrichment data to Claude to generate a human-readable qualification summary for each lead.
3. **Agent monitoring:** Build n8n workflows where Claude reviews PostHog metrics weekly and recommends play adjustments.
4. **Conversation analysis:** Pipe Gong/Fireflies transcripts through Claude to extract objections, buying signals, and next steps.

### Setup
- API key from console.anthropic.com
- Use claude-sonnet-4-20250514 for most GTM tasks (fast, cost-effective)
- Use claude-opus-4-20250514 for complex analysis (deal reviews, competitive intel)
- Set temperature to 0.3 for factual tasks, 0.7 for creative content
