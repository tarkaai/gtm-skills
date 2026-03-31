---
name: account-brief-generation
description: Generate an outreach-ready account brief with personalization hooks using an LLM
tool: Anthropic Claude API
difficulty: Config
---

# Generate Account Brief via LLM

Take structured account intelligence data (firmographics, news, tech stack, contacts) and generate a concise, outreach-ready account brief with specific personalization hooks and suggested talk tracks. This fundamental converts raw research data into actionable sales ammunition.

## Prerequisites

- Anthropic API key (or OpenAI API key as fallback)
- Structured account data from `account-intelligence-assembly` or equivalent enrichment
- Your product's value proposition and ICP pain points documented

## Steps

### 1. Prepare the input context

Gather the account data into a single context block:
- Company firmographics (name, size, industry, funding, tech stack)
- Recent news and signals (last 90 days)
- Key contacts (names, titles, LinkedIn activity)
- Any prior interaction history from CRM
- Your product's value proposition and target pain points

### 2. Generate via Anthropic API

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1500,
  "system": "You are generating an account research brief for a sales outreach agent. The brief must be factual, specific, and immediately actionable. No filler. Every sentence must either inform a personalization decision or suggest a concrete outreach angle.\n\nRules:\n- Maximum 500 words\n- Lead with the strongest outreach signal (most recent, most relevant event)\n- Include exactly 3 personalization hooks ranked by strength\n- Each hook must include: the signal, why it matters, and a suggested first-line for an email\n- Identify the best entry point contact and why\n- Flag any risks or disqualifiers\n- Output as structured markdown",
  "messages": [
    {
      "role": "user",
      "content": "Generate an account brief for outreach to {COMPANY_NAME}.\n\nFirmographics:\n{FIRMOGRAPHICS_JSON}\n\nRecent news and signals:\n{NEWS_SIGNALS_JSON}\n\nTech stack:\n{TECH_STACK_JSON}\n\nKey contacts:\n{CONTACTS_JSON}\n\nPrior interactions:\n{CRM_HISTORY or 'None — cold outreach'}\n\nOur product: {PRODUCT_DESCRIPTION}\nOur ICP pain points: {ICP_PAIN_POINTS}\nOur differentiators: {DIFFERENTIATORS}\n\nGenerate the account brief."
    }
  ]
}
```

### 3. Generate via OpenAI API (alternative)

```
POST https://api.openai.com/v1/chat/completions
Authorization: Bearer {OPENAI_API_KEY}
Content-Type: application/json

{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "system",
      "content": "{SAME_SYSTEM_PROMPT_AS_ABOVE}"
    },
    {
      "role": "user",
      "content": "{SAME_USER_PROMPT_AS_ABOVE}"
    }
  ],
  "max_tokens": 1500,
  "temperature": 0.3
}
```

### 4. Expected output structure

The generated brief should follow this format:

```markdown
## Account Brief: {Company Name}
**Generated:** {date} | **Priority:** {High/Medium/Low}

### Top Signal
{The single most important outreach trigger — what happened, when, and why it matters for your product}

### Personalization Hooks (ranked)

1. **{Signal}**: {Why it matters}
   > Suggested first line: "{email opening sentence referencing this signal}"

2. **{Signal}**: {Why it matters}
   > Suggested first line: "{email opening sentence}"

3. **{Signal}**: {Why it matters}
   > Suggested first line: "{email opening sentence}"

### Recommended Entry Point
**{Contact Name}**, {Title} — {Why this person is the best first touch}

### Talk Track
- Open with: {hook}
- Bridge to pain: {connection between their situation and your product's value}
- Ask: {discovery question tailored to their context}

### Risks & Disqualifiers
- {Any red flags: wrong stage, competitor locked in, budget freeze, etc.}
```

### 5. Store the brief

Write the generated brief to Attio as a note on the company record:

```
attio.create_note({
  parent_object: "companies",
  parent_record_id: "{company_id}",
  title: "Account Brief — {date}",
  content: "{generated_brief}",
  tags: ["account-brief", "outreach-ready"]
})
```

### 6. Validate before use

**Human action required:** Scan each brief for 30 seconds before using it in outreach. Check:
- Are the personalization hooks factually accurate?
- Is the recommended entry point still at the company?
- Do the suggested first lines sound natural, not robotic?

Edit any inaccuracies. The LLM provides the structure and connections; the human adds judgment.

## Cost Estimates

- Anthropic Claude Sonnet: ~$0.02-0.04 per brief
- OpenAI GPT-4o: ~$0.03-0.05 per brief
- At scale (200 briefs/month): ~$5-10/month in API costs

## Error Handling

- **Thin output**: Input data was too sparse. Enrich the account further before regenerating (run `account-intelligence-assembly` first).
- **Hallucinated signals**: The LLM invented a funding round or product launch. Always cross-reference the top signal against the raw input data.
- **Generic hooks**: If all 3 hooks say "congrats on growth," the input lacks specific signals. Add news search or job posting data and regenerate.
- **Contact no longer at company**: LinkedIn data in Clay can be stale. Verify the recommended entry point's current role before outreach.
