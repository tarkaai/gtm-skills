---
name: payment-structure-generation
description: Generate creative payment structures that help prospects fit a purchase into budget constraints without discounting
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Payment Structure Generation

Given a deal's financial context and budget constraint details, generate 3-5 creative payment structures that help the prospect afford the purchase without reducing price. The goal is to preserve deal value while removing budget as a blocker.

## Prerequisites

- Deal record from Attio with deal value, term, and prospect financial context
- Budget objection classification (from `budget-objection-classification`)
- Prospect's budget cycle information (fiscal year end, budget planning timeline)
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
  "max_tokens": 2500,
  "messages": [
    {
      "role": "user",
      "content": "Generate creative payment structures for a B2B deal where the prospect has a budget constraint. The goal is to PRESERVE the total deal value while making it easier for the prospect to pay. Never recommend a discount — find structural solutions instead.\n\nDeal context:\n- Annual deal value: ${deal_value}\n- Prospect company size: {headcount} employees\n- Prospect fiscal year end: {fiscal_year_end}\n- Current budget objection root cause: {root_cause}\n- Budget available now: ${available_budget or 'unknown'}\n- Months until next budget cycle: {months_to_next_cycle or 'unknown'}\n- Payment terms the prospect typically accepts: {payment_terms or 'unknown'}\n- Is multi-year acceptable to the prospect: {multi_year_open or 'unknown'}\n\nGenerate 3-5 payment structure options. For each:\n- `name`: Short name for the structure\n- `description`: How it works in 2-3 sentences\n- `payment_schedule`: Array of payment amounts and dates\n- `total_contract_value`: Must equal or exceed the standard annual price\n- `benefit_to_buyer`: Why this helps them with their specific budget constraint\n- `benefit_to_seller`: What the seller gains (commitment, longer term, upfront payment, etc.)\n- `risk_to_seller`: What could go wrong\n- `best_for_root_cause`: Which budget objection root cause this structure works best for\n- `requires_approval`: Whether this structure needs internal approval from the seller's finance/legal\n\nStructure types to consider:\n1. **Deferred start** — sign now, first payment aligned to next budget cycle\n2. **Quarterly billing** — split annual cost into quarterly payments\n3. **Monthly billing** — split into monthly payments (smallest per-period impact)\n4. **Phased rollout** — start with a subset of the product at lower cost, expand later\n5. **Pilot-to-full** — paid pilot at reduced scope, auto-converts to full deal\n6. **Multi-year lock** — commit to 2-3 years, lower annual payment, higher TCV\n7. **Ramp pricing** — lower payment in year 1, increasing in year 2+ as value is proven\n8. **Pay-per-use** — usage-based pricing that starts small and grows\n9. **Budget split** — divide the cost across two departments or cost centers\n10. **Prepay discount** — small discount for full upfront annual payment\n\nReturn valid JSON array of 3-5 options, ranked by fit for this prospect's situation."
    }
  ]
}
```

## Response Format

```json
[
  {
    "name": "Ramp Pricing",
    "description": "Pay 60% of the annual price in year 1, 100% in year 2, and 120% in year 3. Total 3-year value exceeds standard pricing. The prospect gets budget relief now while the seller locks in a higher long-term commitment.",
    "payment_schedule": [
      {"period": "Year 1", "amount": 14400, "note": "60% of standard ACV"},
      {"period": "Year 2", "amount": 24000, "note": "100% of standard ACV"},
      {"period": "Year 3", "amount": 28800, "note": "120% of standard ACV"}
    ],
    "total_contract_value": 67200,
    "benefit_to_buyer": "Fits within this year's remaining budget. Proves ROI before full pricing kicks in.",
    "benefit_to_seller": "3-year commitment with 12% premium over standard 3-year pricing. Higher TCV than annual.",
    "risk_to_seller": "If the prospect churns after year 1, revenue captured is only 60% of one year.",
    "best_for_root_cause": "no_allocated_budget",
    "requires_approval": true
  },
  {
    "name": "Quarterly Billing",
    "description": "Split the $24,000 annual price into 4 quarterly payments of $6,000. No discount, same total value. Each payment may fall under the prospect's quarterly discretionary spending limit.",
    "payment_schedule": [
      {"period": "Q1", "amount": 6000},
      {"period": "Q2", "amount": 6000},
      {"period": "Q3", "amount": 6000},
      {"period": "Q4", "amount": 6000}
    ],
    "total_contract_value": 24000,
    "benefit_to_buyer": "Each quarterly payment stays under discretionary spend thresholds. Easier to approve without CFO sign-off.",
    "benefit_to_seller": "Preserves full deal value. Annual commitment still in place.",
    "risk_to_seller": "Slightly higher churn risk. More billing administration.",
    "best_for_root_cause": "procurement_friction",
    "requires_approval": false
  }
]
```

## Error Handling

- If `deal_value` is missing or zero, return an error: "Cannot generate payment structures without a deal value. Set deal_value in Attio first."
- If fiscal year end is unknown, generate structures that work regardless of budget timing (monthly, phased, pilot).
- If the prospect's available budget is known and is greater than 80% of the deal value, flag: "Budget gap is small. Consider a minor scope adjustment rather than a complex payment structure."
