---
name: discovery-question-generation
description: Generate role-specific discovery questions for each stakeholder type using Claude API
tool: Anthropic
difficulty: Config
---

# Discovery Question Generation

Use the Claude API to generate tailored discovery questions for each stakeholder role in a B2B buying committee. Questions are calibrated to the stakeholder's role (Economic Buyer, Technical Evaluator, End User, etc.), the product being sold, and any prior intelligence gathered about their priorities.

## Prerequisites

- Anthropic API key from console.anthropic.com
- Stakeholder role classification (from `stakeholder-role-classification` fundamental)
- Product value proposition and competitive positioning
- Optional: prior call notes or pain points for this account

## Steps

### 1. Call the Claude API with stakeholder context

```
POST https://api.anthropic.com/v1/messages
Headers: x-api-key: {ANTHROPIC_API_KEY}, anthropic-version: 2023-06-01
Body: {
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2048,
  "temperature": 0.3,
  "messages": [{"role": "user", "content": "You are preparing discovery questions for a B2B sales call.\n\nContext:\n- Product: {product_description}\n- Company: {prospect_company_name}\n- Industry: {prospect_industry}\n- Stakeholder: {name}, {title}\n- Classified role: {role} (Economic Buyer | Champion | Influencer | Blocker | End User | Gatekeeper)\n- Known pain points (if any): {prior_pains}\n- Prior interactions (if any): {interaction_summary}\n\nGenerate 8-12 discovery questions tailored to this stakeholder's role:\n- Economic Buyer questions should focus on: business impact, ROI expectations, budget timeline, strategic alignment, risk tolerance\n- Champion questions should focus on: internal politics, what they need to build the internal case, what obstacles they foresee, their success metrics\n- Influencer questions should focus on: evaluation criteria, technical requirements, integration concerns, comparison to alternatives\n- Blocker questions should focus on: their concerns directly, security/compliance requirements, what would need to be true for them to support this, incumbent vendor relationship\n- End User questions should focus on: current workflow pain, daily friction points, what they wish they could do, adoption concerns\n- Gatekeeper questions should focus on: procurement process, timeline, required documentation, other stakeholders they recommend engaging\n\nFor each question, include:\n- The question text\n- Why this question matters for this role\n- What a good answer looks like (signal of progress)\n- What a bad answer looks like (signal of risk)\n\nReturn as JSON array: [{\"question\": \"...\", \"rationale\": \"...\", \"good_signal\": \"...\", \"risk_signal\": \"...\"}]"}]
}
```

### 2. Parse and validate the response

Extract the JSON array from the response. Validate:
- Each question object has all 4 fields (question, rationale, good_signal, risk_signal)
- Questions are specific to the role (not generic sales questions)
- Questions reference the prospect's industry or known context where applicable
- No duplicate questions

### 3. Store questions in CRM

Push generated questions to Attio as a note on the contact record:

```json
{
  "data": {
    "note": "Discovery Questions for {name} ({role}):\n\n{formatted_questions}"
  }
}
```

Tag the note as `discovery-prep` for later retrieval by the `account-research-brief` drill.

### 4. Post-call: compare answers to signals

After the discovery call, retrieve the questions and compare actual answers against good_signal and risk_signal. This feeds back into the `stakeholder-sentiment-extraction` fundamental to refine the stakeholder's classification and engagement priority.

## Via Clay (Claygent)

For batch question generation without API calls:
```
Claygent prompt: "Generate 5 discovery questions for {Full Name}, {Title} at {Company Name}. They are a {Stakeholder Role} in a B2B buying decision for {product category}. Tailor questions to their role and likely concerns. Return numbered list."
```

Cost: 5-10 credits per contact. Use for initial bulk prep before a discovery sprint.

## Tool Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Anthropic Claude | Messages API | Best reasoning for nuanced role-specific questions |
| OpenAI GPT-4 | Chat Completions API | Good alternative, similar quality |
| Clay Claygent | Built-in AI column | Convenient for batch processing |
| Gong Engage | Smart follow-up suggestions | Suggests questions based on call patterns |

## Error Handling

- **Generic questions**: If Claude returns questions that could apply to any role, the prompt lacks specificity. Add more context about the product and the stakeholder's known concerns.
- **Too many questions**: Cap at 12. More than that becomes unwieldy in a 30-minute discovery call.
- **API rate limits**: Batch question generation across stakeholders with 1-second delays. A typical deal with 5 stakeholders costs ~$0.02 in API calls.
