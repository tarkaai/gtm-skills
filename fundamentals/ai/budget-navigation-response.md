---
name: budget-navigation-response
description: Generate a tailored budget navigation response matched to the objection root cause — find budget, restructure payment, or build internal justification
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Budget Navigation Response Generation

Given a classified budget objection with root cause and deal context, generate a tailored response that helps the prospect navigate the budget constraint. Unlike price objection responses (which reframe value), budget navigation responses focus on finding money, restructuring payment, and arming champions with justification materials.

## Prerequisites

- Classified budget objection (from `budget-objection-classification`)
- Deal record from Attio with pain data, champion, economic buyer
- Historical budget navigation effectiveness data (optional, improves over time)
- Anthropic API key

## API Call

```
POST https://api.anthropic.com/v1/messages
Authorization: x-api-key {ANTHROPIC_API_KEY}
Content-Type: application/json
```

**Request body:**
```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 3000,
  "messages": [
    {
      "role": "user",
      "content": "You are generating a budget navigation response for a B2B sales deal. The prospect has a budget constraint — they are NOT saying the product is overpriced, they are saying they cannot find the money right now.\n\nYour job is to generate a response that helps the prospect FIND or UNLOCK budget. You are a strategic partner helping them solve a procurement problem, not a salesperson pushing a discount.\n\nRoot cause: {root_cause}\nRoot cause details: {root_cause_reasoning}\nNavigability score: {navigability_score}/10\nUrgency: {urgency}/10\n\nDeal context:\n- Company: {company_name}\n- Deal value: ${deal_value}/year\n- Champion: {champion_name}, {champion_title}\n- Economic buyer: {economic_buyer_name}, {economic_buyer_title}\n- Pain-to-price ratio: {pain_to_price_ratio}x\n- Top quantified pains: {top_pains_json}\n- Budget cycle: {fiscal_year_end or 'unknown'}\n- Competitive situation: {none|passive|active}\n\nResponse framework per root cause:\n\n**no_allocated_budget**: Help find money. Options: (1) map the prospect's cost centers for discretionary funds, (2) show how this replaces an existing line item (tool consolidation), (3) propose a pilot small enough to fit in discretionary spend, (4) identify which executive has unallocated budget authority.\n\n**budget_exhausted**: Bridge the gap. Options: (1) defer start to next budget cycle but lock pricing now, (2) propose a quarterly payment structure that splits cost across budget periods, (3) start with a free/low-cost pilot this period and convert to paid next cycle, (4) find end-of-year budget that would otherwise expire.\n\n**wrong_budget_owner**: Navigate the org. Options: (1) identify the correct budget owner and request a warm intro via the champion, (2) arm the champion with a one-page justification they can forward, (3) propose a joint meeting with the champion and budget owner, (4) map which department benefits most from the product and target that budget.\n\n**competing_priorities**: Win the priority contest. Options: (1) quantify the cost of delay using the prospect's own pain data, (2) show how this initiative accelerates or complements the competing priority, (3) propose a phased approach that runs alongside the competing initiative, (4) build a business case that directly competes with the other initiative on ROI.\n\n**procurement_friction**: Reduce friction. Options: (1) ask what procurement requires and proactively provide it (security questionnaires, vendor forms, compliance docs), (2) propose a structure that bypasses procurement thresholds (monthly billing under approval limits, pilot under discretionary spend), (3) connect with procurement directly to unblock, (4) offer to fast-track any vendor qualification steps.\n\n**budget_smokescreen**: Re-qualify the deal. Options: (1) pivot to value — 'Setting budget aside, is this something your team would want to move forward on?', (2) ask directly what the real blocker is, (3) test the champion's commitment by asking them to do something small (intro to another stakeholder, share a document internally), (4) propose a free trial or proof of concept to test genuine interest.\n\nGenerate:\n1. `framework_selected`: The response framework name (e.g., 'find_discretionary_funds', 'defer_and_lock', 'navigate_to_budget_owner')\n2. `verbal_response`: 3-5 sentences the seller should say on the next call. Empathetic, collaborative, not pushy.\n3. `diagnostic_questions`: 2-3 questions to deepen understanding of the budget situation\n4. `follow_up_email`: A short (under 200 words) email the seller can send after the call\n5. `champion_asset`: What material to create for the champion to use internally (budget justification memo, cost-of-delay analysis, phased rollout proposal, etc.)\n6. `payment_structure_options`: If applicable, 2-3 creative payment structures that help the prospect fit the purchase into their budget constraints\n7. `escalation_path`: If the direct path fails, what's the next escalation step\n\nReturn valid JSON."
    }
  ]
}
```

## Response Format

```json
{
  "framework_selected": "defer_and_lock",
  "verbal_response": "I completely understand — budget timing is one of the most common things we work through with our customers. Here's what I'd suggest: we can lock in today's pricing for a start date that aligns with your next budget cycle. That way your team gets the rate protection without having to find budget this quarter. A lot of our customers have found that this actually makes the budget conversation easier internally because the finance team can plan for it.",
  "diagnostic_questions": [
    "When does your next fiscal year or budget planning cycle begin?",
    "If we could structure this so the first payment doesn't hit until Q1, would that change the conversation with your finance team?",
    "Is there a specific date by which budget decisions for next year need to be locked in?"
  ],
  "follow_up_email": "Hi {champion_name},\n\nThanks for the honest conversation about budget timing. I wanted to follow up with the option we discussed.\n\nWe can lock in the current pricing ($X/year) with a deferred start date aligned to your next budget cycle. No payment due until {next_fiscal_start}. This gives your team time to plan while protecting you from any pricing changes.\n\nI've attached a one-page summary you can share with {economic_buyer} that outlines the ROI case and the deferred payment structure.\n\nWould it be helpful if I joined a quick call with {economic_buyer} to walk through the numbers?\n\nBest,\n{seller_name}",
  "champion_asset": "Budget justification memo: one-page document showing (1) annual cost of the problem using the prospect's own pain data, (2) proposed solution cost with deferred payment timeline, (3) ROI and payback period, (4) risk of not acting (competitor advantage, continued cost bleed). Written from the champion's perspective, not the vendor's.",
  "payment_structure_options": [
    {
      "name": "Deferred Start",
      "structure": "Sign now, first payment in {next_fiscal_start}. 12-month term.",
      "benefit_to_buyer": "No budget impact this fiscal year. Can plan for next year's budget.",
      "risk_to_seller": "Revenue recognition delayed. Prospect may change priorities before start date."
    },
    {
      "name": "Quarterly Billing",
      "structure": "Split annual cost into 4 quarterly payments. Each payment stays under ${deal_value/4}.",
      "benefit_to_buyer": "Smaller per-period budget impact. May fit under quarterly discretionary limits.",
      "risk_to_seller": "Higher churn risk with quarterly billing. Slight increase in billing administration."
    }
  ],
  "escalation_path": "If the champion cannot secure budget by deferring, escalate to the economic buyer directly. Propose a 30-minute call focused exclusively on the ROI case and payment flexibility. If the economic buyer is unreachable, this deal should be deprioritized until the next budget cycle."
}
```

## Error Handling

- If `root_cause` is `ambiguous`, return a diagnostic-first response: ask budget-qualifying questions before generating a full response.
- If `navigability_score <= 3`, the response should acknowledge the low probability and recommend the seller deprioritize this deal while maintaining a nurture sequence for the next budget cycle.
- If `is_smokescreen: true`, the response focuses entirely on re-qualification rather than budget navigation.
