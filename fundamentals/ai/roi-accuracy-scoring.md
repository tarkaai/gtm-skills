---
name: roi-accuracy-scoring
description: Compare projected ROI from sales cycle against realized ROI from customer data to calibrate model accuracy
tool: Anthropic
difficulty: Advanced
---

# ROI Accuracy Scoring

Compare the ROI projected during the sales cycle against actual customer outcomes. Produces an accuracy score and calibration recommendations to improve future ROI models.

## Prerequisites

- Original ROI model stored in Attio (from `roi-model-generation`)
- Customer usage/outcome data from PostHog (activation, feature adoption, time savings)
- At least 30 days of post-close customer data
- Anthropic API key

## Steps

### 1. Retrieve projected vs actual data

Pull the original ROI model from the Attio deal record and the customer's actual metrics from PostHog:

```json
{
  "deal_id": "...",
  "projected": {
    "annual_savings": 412800,
    "roi_percentage": 1620,
    "payback_months": 0.7,
    "savings_by_driver": [
      {"driver": "time_savings", "projected_annual": 172800},
      {"driver": "cost_reduction", "projected_annual": 240000}
    ]
  },
  "actual": {
    "months_since_close": 6,
    "measured_savings": {
      "time_savings_hours_per_month": 120,
      "cost_reduction_per_month": 8000
    },
    "customer_reported_satisfaction": 8,
    "feature_adoption_rate": 0.75,
    "support_tickets_filed": 12
  },
  "product_annual_price": 24000
}
```

### 2. Compute accuracy via Claude API

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
  "messages": [{
    "role": "user",
    "content": "Compare projected ROI against actual customer outcomes. Annualize the actual data based on months elapsed. Be precise about what can and cannot be measured.\n\nProjected:\n{projected}\n\nActual (after {months_since_close} months):\n{actual}\n\nReturn this exact JSON:\n{\n  \"accuracy_by_driver\": [\n    {\"driver\": \"...\", \"projected_annual\": 0, \"actual_annualized\": 0, \"accuracy_pct\": 0, \"direction\": \"over|under|accurate\", \"explanation\": \"...\"}\n  ],\n  \"overall_accuracy\": {\n    \"projected_total_savings\": 0,\n    \"actual_annualized_savings\": 0,\n    \"accuracy_pct\": 0,\n    \"projected_roi\": 0,\n    \"actual_roi\": 0\n  },\n  \"calibration_recommendations\": [\n    {\"driver\": \"...\", \"current_assumption\": \"...\", \"recommended_adjustment\": \"...\", \"reason\": \"...\"}\n  ],\n  \"data_gaps\": [\"List any projected savings that cannot be verified with available data\"],\n  \"confidence\": \"high|medium|low\",\n  \"next_measurement_date\": \"YYYY-MM-DD\"\n}"
  }]
}
```

### 3. Validate the accuracy report

Check:
- `accuracy_pct` for each driver equals `(actual_annualized / projected_annual) * 100`
- `overall_accuracy.accuracy_pct` equals `(actual_annualized_savings / projected_total_savings) * 100`
- `actual_roi` equals `((actual_annualized_savings - product_annual_price) / product_annual_price) * 100`
- All `calibration_recommendations` reference specific drivers from the original model
- `data_gaps` lists any driver where actual measurement data is unavailable

### 4. Store the accuracy report

Update the Attio deal record:
- `roi_accuracy_pct` = `overall_accuracy.accuracy_pct`
- `roi_actual_vs_projected` = "over" | "under" | "accurate" (within 20%)
- `roi_last_measured` = today's date
- `roi_next_measurement` = `next_measurement_date`

Store the full accuracy report as an Attio note.

Fire PostHog event:
```json
{
  "event": "roi_accuracy_measured",
  "properties": {
    "deal_id": "...",
    "accuracy_pct": 0,
    "direction": "over|under|accurate",
    "projected_roi": 0,
    "actual_roi": 0,
    "months_since_close": 0,
    "confidence": "high|medium|low"
  }
}
```

## Error Handling

- **Insufficient actual data:** If customer has been live < 30 days, defer measurement. Set `next_measurement_date` to 30 days post-close.
- **Missing driver data:** If a projected savings driver has no corresponding actual measurement, list it in `data_gaps` and exclude from accuracy calculation. Recommend adding tracking for that driver.
- **Extreme over-projection (accuracy < 30%):** Flag the original model's assumptions for review. The discovery data may have been inflated or the implementation may have been incomplete.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Claude (Anthropic) | Messages API | Best for nuanced accuracy analysis |
| GPT-4 (OpenAI) | Chat Completions API | Alternative LLM |
| Spreadsheet | Manual comparison | Simpler but less scalable |
| Metabase | SQL queries | Direct database comparison if data is structured |
