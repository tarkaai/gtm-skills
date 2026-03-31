---
name: success-criteria-intelligence
description: AI-powered recommendation engine that suggests optimal success criteria based on historical achievement data, prospect similarity, and product capabilities
category: Sales
tools:
  - Anthropic
  - Attio
  - PostHog
  - n8n
fundamentals:
  - success-criteria-extraction
  - attio-deals
  - attio-reporting
  - attio-notes
  - posthog-dashboards
  - posthog-custom-events
  - hypothesis-generation
  - n8n-workflow-basics
  - n8n-scheduling
---

# Success Criteria Intelligence

This drill builds an AI-powered recommendation system that improves over time. It analyzes historical deals — which success criteria were defined, which were achieved, and which predicted the best outcomes (close rate, retention, expansion) — and uses that data to recommend optimal criteria for new deals.

## Input

- At least 20 completed deals with success criteria defined and outcomes tracked (minimum viable dataset)
- Attio deal records with `success_criteria_status`, outcome data, and retention metrics
- PostHog events tracking success criteria definition and achievement
- n8n instance for scheduled analysis

## Steps

### 1. Build the Historical Achievement Dataset

Query Attio for all deals where `success_criteria_status` = "defined" and the deal has a closed outcome (won or lost). For each deal, extract:

```json
{
  "deal_id": "",
  "company_industry": "",
  "company_headcount": "",
  "deal_size": "",
  "outcome": "won|lost",
  "criteria": [
    {
      "metric": "",
      "target": "",
      "category": "",
      "achievability_score_at_definition": 0,
      "achieved": true|false,
      "actual_value": "",
      "time_to_achieve_days": 0
    }
  ],
  "close_rate_with_criteria": true,
  "retention_months": 0,
  "expanded": true|false,
  "nps_score": 0
}
```

Store this dataset as an Attio list for ongoing reference.

### 2. Compute Achievement Statistics

Using n8n scheduled workflow (weekly), aggregate the achievement data:

- **By category:** What % of efficiency criteria are achieved vs revenue criteria vs adoption criteria?
- **By industry:** Which criteria types perform best for SaaS companies vs agencies vs ecommerce?
- **By deal size:** Do larger deals achieve criteria at different rates?
- **By achievability score:** Validate the scoring model — are criteria scored 80+ actually achieved 80% of the time?
- **Close rate correlation:** Do deals with defined criteria close at higher rates? By how much?
- **Retention correlation:** Do deals where criteria were achieved retain longer?

Push the statistics to PostHog as a dashboard using `posthog-dashboards`.

### 3. Generate Recommendations for New Deals

When a new deal enters Connected stage, the n8n workflow triggers:

1. Pull the prospect's company data from Attio (industry, headcount, use case)
2. Query the achievement dataset for the 10 most similar closed-won deals (match on industry, headcount range, and use case)
3. Rank criteria by: `(historical_achievement_rate * close_rate_correlation * retention_impact)`
4. Call `success-criteria-extraction` with an enriched prompt that includes the historical context:
   - "For companies like {industry} with {headcount} employees, the following criteria have the highest achievement rates: {top_criteria_list}"
   - "Avoid these criteria — they have <40% achievement rate for similar companies: {risky_criteria_list}"
5. Store the recommendations in Attio as a note tagged `criteria-recommendations`

### 4. Track Recommendation Accuracy

For each deal where AI-recommended criteria were used:
- Log which recommendations were accepted by the prospect (vs modified or rejected)
- After the deal closes (won or lost), compare: did the recommended criteria predict the outcome?
- Track `recommendation_acceptance_rate` and `recommendation_accuracy` in PostHog

Fire PostHog events:
- `criteria_recommendation_generated`: properties = `deal_id`, `criteria_count`, `confidence_score`
- `criteria_recommendation_accepted`: properties = `deal_id`, `accepted_count`, `modified_count`, `rejected_count`
- `criteria_outcome_validated`: properties = `deal_id`, `predicted_outcome`, `actual_outcome`, `criteria_achieved_count`

### 5. Achievability Model Calibration

Monthly, run the calibration workflow:

1. Pull all deals where achievability scores were assigned at criteria definition time
2. Compare predicted achievability (the score) against actual achievement (did the customer hit the target?)
3. Calculate calibration: if criteria scored 80+ are only achieved 50% of the time, the model is overconfident
4. Use `hypothesis-generation` to suggest scoring adjustments:
   - "Efficiency criteria at companies with <50 employees are achieving at 60% vs the predicted 80%. Hypothesis: smaller teams have less capacity to measure and report on these metrics. Adjust achievability score down by 20 points for this segment."
5. Apply adjustments to the scoring model and track whether calibration improves

## Output

- Historical achievement dataset maintained in Attio
- Weekly statistics dashboard in PostHog
- AI-generated criteria recommendations for every new Connected deal
- Ongoing calibration of the achievability scoring model
- Recommendation accuracy tracking

## Triggers

- **New deal at Connected stage:** Generate criteria recommendations
- **Weekly (n8n cron):** Recompute achievement statistics
- **Monthly (n8n cron):** Run achievability model calibration
- **Deal closed:** Validate recommendation accuracy
