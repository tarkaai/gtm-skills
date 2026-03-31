---
name: call-brief-generation
description: Use Claude to generate a structured meeting preparation brief from assembled account intelligence
tool: Anthropic
difficulty: Config
---

# Call Brief Generation

Given an assembled account intelligence profile, generate a structured meeting preparation brief: talking points, questions to ask, objection preparation, competitive positioning, and a recommended meeting structure. The brief is designed for a founder or AE preparing for a sales call.

## Prerequisites

- Anthropic API key (or OpenAI as fallback)
- Assembled account intelligence profile (from `account-intelligence-assembly`)
- Meeting type known: discovery, demo, negotiation, or executive review
- Your product's value proposition and feature catalog

## API Call

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 3000,
  "temperature": 0.3,
  "messages": [{
    "role": "user",
    "content": "Generate a sales meeting preparation brief.\n\nMeeting type: {meeting_type}\nMy company: {your_company} — {your_value_prop}\n\nAccount intelligence:\n{account_intelligence_json}\n\nGenerate a structured brief with these sections:\n\n1. EXECUTIVE SUMMARY (3 sentences: who they are, why they might buy, biggest risk)\n2. MEETING OBJECTIVES (2-3 specific outcomes to achieve in this meeting)\n3. OPENING (1 sentence referencing something specific and recent about them — a news item, LinkedIn post, or hiring signal — to demonstrate preparation)\n4. KEY QUESTIONS (5-7 questions tailored to this account, ordered by priority, each with a rationale for why to ask it)\n5. TALK TRACKS (for each documented pain point: a 2-sentence positioning statement connecting their pain to your solution)\n6. OBJECTION PREPARATION (predict 3 likely objections based on their profile and competitive landscape, with a 2-sentence response for each)\n7. COMPETITIVE POSITIONING (if competitors are in play: one-liner on how to position against each without trash-talking)\n8. STAKEHOLDER MAP (who is in the meeting, their likely role in the buying process, what each person cares about)\n9. NEXT STEPS TO PROPOSE (based on deal stage: what is the ideal next step to propose at the end of this meeting)\n10. MEETING STRUCTURE (minute-by-minute agenda for a {meeting_duration}-minute call)\n\nReturn as clean markdown. Every recommendation must reference specific data from the account intelligence — no generic advice."
  }]
}
```

## Via OpenAI (Alternative)

```
POST https://api.openai.com/v1/chat/completions
Authorization: Bearer {OPENAI_API_KEY}
Content-Type: application/json

{
  "model": "gpt-4o",
  "messages": [
    { "role": "system", "content": "You are an expert sales strategist generating meeting preparation briefs. Every recommendation must be grounded in the provided account intelligence. Never give generic advice." },
    { "role": "user", "content": "{SAME_PROMPT_AS_ABOVE}" }
  ],
  "max_tokens": 3000,
  "temperature": 0.3
}
```

## Input Requirements

- `meeting_type`: One of `discovery`, `demo`, `negotiation`, `executive_review`, `technical_deep_dive`
- `account_intelligence_json`: Full profile from `account-intelligence-assembly`
- `meeting_duration`: Integer, minutes (default 30)
- `your_company`: Company name
- `your_value_prop`: 2-3 sentence product value proposition

## Output Structure

The generated brief follows this format:

```markdown
## Meeting Brief — {Company Name}
### {Meeting Type} | {Date} | {Duration} min

### Executive Summary
{3 sentences}

### Meeting Objectives
1. {Specific outcome}
2. {Specific outcome}
3. {Specific outcome}

### Opening
"{Personalized opening line referencing recent signal}"

### Key Questions
1. **{Question}** — Rationale: {why this matters for this account}
2. ...

### Talk Tracks
- **Pain: {pain_summary}** → "{positioning statement}"
- ...

### Objection Preparation
| Likely Objection | Response |
|-----------------|----------|
| "{objection}" | "{response}" |
| ... | ... |

### Competitive Positioning
- vs {Competitor}: "{one-liner}"
- ...

### Stakeholder Map
| Name | Title | Likely Role | Cares About |
|------|-------|-------------|-------------|
| ... | ... | ... | ... |

### Proposed Next Step
{What to propose and why}

### Meeting Structure
- 0-3 min: {activity}
- 3-10 min: {activity}
- ...
```

## Cost Estimate

- Claude Sonnet: ~$0.03-0.08 per brief (depends on intelligence profile size)
- At scale (50 briefs/month): ~$2-4/month in API costs
- GPT-4o: ~$0.05-0.10 per brief

## Guardrails

- **Never fabricate data**: If the intelligence profile has gaps (e.g., no recent news), the brief should note "No recent signals found — open the call by asking about their current priorities" rather than inventing news.
- **No generic filler**: Every question, talk track, and objection response must reference data from the intelligence profile. If the brief includes "Tell me about your biggest challenges" without context, the prompt needs tightening.
- **Meeting type awareness**: A discovery brief focuses on questions. A demo brief focuses on pain-to-feature mapping. A negotiation brief focuses on objection handling. The structure adapts.
- **Length limit**: Brief should be scannable in under 5 minutes. If the founder cannot read it in the elevator, it is too long.

## Error Handling

- **API timeout**: Retry once with `max_tokens` reduced to 2000. If still fails, generate a minimal brief with just Executive Summary + Key Questions + Meeting Structure.
- **Low-quality output (generic recommendations)**: The intelligence profile is likely too thin. Re-run `account-intelligence-assembly` with additional Claygent research credits.
- **Hallucinated data in brief**: Always cross-reference the brief's claims against the raw intelligence profile. If the brief mentions a funding round not in the profile, it hallucinated. Log as `brief_hallucination_detected` in PostHog.

## Tool Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best reasoning, strongest at nuanced competitive positioning |
| GPT-4o (OpenAI) | Chat Completions API | Good alternative, slightly faster |
| Gemini (Google) | Generative Language API | Good for accounts with heavy web presence |
| Gong | Deal intelligence + AI prep | Enterprise, uses call history for coaching |
| Dooly | AI meeting prep | Pulls from Salesforce, limited to SF users |
