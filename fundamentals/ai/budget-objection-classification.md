---
name: budget-objection-classification
description: Classify a budget objection by root cause — distinguishing genuine budget constraints from proxy objections — and score urgency and navigability
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Budget Objection Classification

Given a prospect's budget-related pushback (from a call transcript segment, email, or chat message), classify the root cause and assess whether the budget constraint is navigable. Budget objections are distinct from price objections: the prospect may agree with the value but genuinely lack allocated funds, face procurement hurdles, or need help finding budget from adjacent cost centers.

## Prerequisites

- Budget objection text (transcript segment, email, or manual entry)
- Deal record from Attio with deal value, champion, economic buyer, and discovery data
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
  "max_tokens": 2000,
  "messages": [
    {
      "role": "user",
      "content": "You are classifying a budget objection in a B2B sales deal. Budget objections are NOT the same as price objections. The prospect is NOT saying your product is too expensive — they are saying they do not have the money allocated.\n\nClassify the root cause as ONE of:\n- `no_allocated_budget`: Prospect has no line item for this category. Budget was never planned. Navigability depends on finding discretionary funds or reallocating from another initiative.\n- `budget_exhausted`: Budget existed but is already spent for this period. Navigability depends on timing — when does the next budget cycle start?\n- `wrong_budget_owner`: The person you're talking to doesn't control the relevant budget. Another department, executive, or cost center owns the money.\n- `competing_priorities`: Budget exists but is earmarked for other initiatives. Must prove this is higher priority.\n- `procurement_friction`: Budget may exist but procurement process is blocking (approval chains, vendor qualification, security review, etc.).\n- `budget_smokescreen`: This is not a real budget objection — the prospect is using 'no budget' as a polite way to decline. The real issue is something else (value doubt, timing, champion weakness, competitive preference).\n\nAlso assess:\n- `navigability_score` (1-10): How likely is it that this budget constraint can be overcome? 1 = nearly impossible, 10 = straightforward path exists.\n- `urgency` (1-10): How time-sensitive is the budget situation? High urgency = budget cycle closing, funds expiring, competing initiative about to consume the money.\n- `diagnostic_questions`: 2-3 questions to ask that will confirm the root cause and uncover the path to budget.\n\nDeal context:\n- Company: {company_name}\n- Deal value: ${deal_value}\n- Champion: {champion_name}, {champion_title}\n- Economic buyer: {economic_buyer_name}, {economic_buyer_title} (or 'unknown')\n- Discovery pain-to-price ratio: {pain_to_price_ratio}x\n- Budget cycle: {fiscal_year_end or 'unknown'}\n- Competitive situation: {none|passive|active}\n\nBudget objection (prospect's exact words or paraphrase):\n\"{objection_text}\"\n\nReturn valid JSON:\n{\n  \"root_cause\": \"one of the 6 categories\",\n  \"root_cause_reasoning\": \"2-3 sentences explaining why this classification\",\n  \"navigability_score\": 7,\n  \"navigability_reasoning\": \"Why this score — what path exists or what blocks it\",\n  \"urgency\": 5,\n  \"urgency_reasoning\": \"Why this urgency level\",\n  \"is_smokescreen\": false,\n  \"smokescreen_signals\": [],\n  \"diagnostic_questions\": [\"question 1\", \"question 2\", \"question 3\"],\n  \"recommended_next_action\": \"One clear next step\"\n}"
    }
  ]
}
```

## Response Format

```json
{
  "root_cause": "competing_priorities",
  "root_cause_reasoning": "The prospect mentioned their team is focused on a CRM migration this quarter. Budget exists in the department but is committed to the migration project. This is not a permanent blocker — it's a sequencing problem.",
  "navigability_score": 7,
  "navigability_reasoning": "High navigability because the budget exists, the prospect sees value, and the competing initiative has a known end date. If we can demonstrate urgency or find a way to run in parallel, the budget can be reallocated.",
  "urgency": 6,
  "urgency_reasoning": "The CRM migration is expected to complete in 8 weeks. If we don't stay engaged, the remaining budget may get absorbed by scope creep on the migration.",
  "is_smokescreen": false,
  "smokescreen_signals": [],
  "diagnostic_questions": [
    "When is the CRM migration expected to wrap up, and would there be budget freed up after that?",
    "Is there a way to pilot our solution alongside the migration with a smaller initial commitment?",
    "Who controls the discretionary budget outside the migration project?"
  ],
  "recommended_next_action": "Propose a phased rollout that starts after the CRM migration completes, with pricing locked at today's rate."
}
```

## Smokescreen Detection

The classifier looks for these signals that a budget objection is not genuine:
- Prospect has not asked about pricing details, payment terms, or budget timelines (low engagement with the commercial conversation)
- Pain-to-price ratio is below 3x (weak value foundation suggests the real issue is value, not budget)
- Champion engagement has dropped since the objection (champion losing interest, not fighting for budget)
- Prospect declined a discovery call about their budget process (would not decline if budget were the real blocker)
- Objection appeared immediately after pricing was shared, with no discussion (reflexive pushback)

If `is_smokescreen: true`, the classification includes `smokescreen_signals` and the recommended action shifts to re-qualifying the deal rather than navigating budget.

## Error Handling

- If the objection text is too vague to classify (e.g., "we'll need to think about the budget"), return `root_cause: "ambiguous"` with diagnostic questions to disambiguate.
- If deal context is missing (no economic buyer, no pain data), the classifier still runs but lowers the `navigability_score` and flags: "Classification confidence is lower due to missing deal context. Run discovery to improve accuracy."
