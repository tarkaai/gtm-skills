---
name: risk-pattern-analysis
description: Aggregate risk data across all deals to identify patterns by segment, track mitigation effectiveness, and refine risk prediction models
category: Deal Management
tools:
  - Attio
  - PostHog
  - Anthropic
  - n8n
fundamentals:
  - attio-reporting
  - attio-lists
  - posthog-dashboards
  - posthog-cohorts
  - hypothesis-generation
  - n8n-scheduling
---

# Risk Pattern Analysis

This drill aggregates risk data from all discovery calls to surface cross-deal patterns. It identifies which risk categories appear most frequently, which predict deal losses, which mitigations are most effective, and how risk profiles differ by segment. The output feeds risk prediction improvement, mitigation library prioritization, and question bank optimization.

## Input

- At least 15 completed deals with risk extraction data in Attio
- PostHog events from `risk_discovery_call_completed` and `risk_mitigation_delivered`
- n8n instance for scheduled execution

## Steps

### 1. Extract risk data from CRM

Query Attio for all deals with `risk_discovery_date` set. Pull for each deal:
- Company attributes: industry, headcount range, funding stage, region
- Risk data: risk_count, total_risk_score, dominant_risk_category, risk_data_json, mitigation_coverage
- Deal outcome: won, lost, or open (if available)
- Time from risk discovery to close (won) or loss (lost)

Using `attio-lists`, create a filtered list: "Risk Discovery Deals -- Last 60 Days" with all deals that have risk data.

### 2. Build the risk frequency matrix

Parse all `risk_data_json` fields and aggregate:

```json
{
  "risk_categories": {
    "financial": {"count": 28, "avg_severity": 6.8, "avg_likelihood": 5.2, "appears_in_pct_of_deals": 0.72, "loss_correlation": 0.35},
    "technical": {"count": 22, "avg_severity": 7.1, "avg_likelihood": 4.8, "appears_in_pct_of_deals": 0.56, "loss_correlation": 0.28},
    "organizational": {"count": 31, "avg_severity": 7.5, "avg_likelihood": 6.1, "appears_in_pct_of_deals": 0.79, "loss_correlation": 0.52},
    "timeline": {"count": 15, "avg_severity": 5.4, "avg_likelihood": 6.8, "appears_in_pct_of_deals": 0.38, "loss_correlation": 0.18},
    "vendor": {"count": 12, "avg_severity": 6.2, "avg_likelihood": 3.5, "appears_in_pct_of_deals": 0.31, "loss_correlation": 0.42}
  },
  "top_specific_risks": [
    {"summary": "Team adoption resistance", "frequency": 18, "avg_risk_score": 46, "loss_correlation": 0.55, "mitigation_success_rate": 0.62},
    {"summary": "Integration with existing CRM", "frequency": 14, "avg_risk_score": 34, "loss_correlation": 0.22, "mitigation_success_rate": 0.78}
  ]
}
```

### 3. Analyze mitigation effectiveness

For each risk category, calculate:
- **Mitigation attempt rate:** How often was mitigation content delivered for this category?
- **Mitigation success rate:** Of delivered mitigations, how often was the risk marked "resolved"?
- **Time to resolution:** Average days from mitigation delivery to resolution
- **Asset effectiveness:** Which specific assets (case studies, docs, references) resolve risks fastest?
- **Deal impact:** For deals where risks were mitigated vs. not, compare close rates

```json
{
  "mitigation_effectiveness": {
    "financial": {"attempt_rate": 0.85, "success_rate": 0.72, "avg_days_to_resolve": 4.2, "top_asset": "ROI calculator"},
    "technical": {"attempt_rate": 0.90, "success_rate": 0.81, "avg_days_to_resolve": 6.1, "top_asset": "Security whitepaper"},
    "organizational": {"attempt_rate": 0.65, "success_rate": 0.48, "avg_days_to_resolve": 12.5, "top_asset": "Change management guide"},
    "timeline": {"attempt_rate": 0.70, "success_rate": 0.67, "avg_days_to_resolve": 3.8, "top_asset": "Implementation timeline"},
    "vendor": {"attempt_rate": 0.55, "success_rate": 0.60, "avg_days_to_resolve": 8.0, "top_asset": "Customer reference call"}
  }
}
```

### 4. Segment by company attributes

Break the risk matrix by segment to find where risk profiles differ:

- **By industry:** Which industries have different dominant risk categories?
- **By company size:** Do enterprise prospects have more organizational risk than SMBs?
- **By funding stage:** Are bootstrapped companies more financial-risk focused?
- **By deal outcome:** Which risks are most fatal (strongest loss correlation)?
- **By deal value:** Do larger deals have higher total risk scores?

Use Claude via `hypothesis-generation` to analyze the segmented data and produce:
- Top 3 risk prediction improvements (e.g., "For healthcare prospects, always probe compliance risk -- it appears in 90% of deals but is often surfaced late")
- Top 3 mitigation library priorities (e.g., "Create a dedicated change management case study -- organizational risk has the lowest mitigation success rate")
- Top 3 question bank updates (e.g., "For enterprise deals, add questions about internal IT governance -- it surfaces technical risks that small-company questions miss")

### 5. Evaluate risk prediction accuracy

For each deal, compare pre-call risk predictions (from `risk-discovery-call-prep`) against actual risks surfaced:
- **Prediction hit rate:** % of predicted risks that were confirmed
- **Surprise rate:** % of actual risks that were NOT predicted
- **Category accuracy:** Which categories are predicted most/least accurately

Track trends over time. A rising prediction hit rate means the enrichment signals and LLM prompts are improving.

### 6. Identify risk-to-loss pathways

For lost deals, trace the causal chain:
- What was the dominant risk category in lost deals?
- Were the fatal risks identified early (during discovery) or late (at proposal/negotiation)?
- For early-identified fatal risks, was mitigation attempted? Did it fail?
- What percentage of losses had unaddressed Critical risks?

This reveals whether losses come from failure to discover risks (discovery problem) or failure to mitigate them (execution problem).

### 7. Generate the risk intelligence report

Compile findings:

```markdown
## Risk Intelligence Report -- {date_range}
### Based on {n} deals with risk discovery data

### Risk Frequency by Category
| Category | Frequency | Avg Score | Loss Correlation | Mitigation Success |
|----------|-----------|-----------|------------------|-------------------|
| Organizational | 79% of deals | 46 | 0.52 | 48% |
| Financial | 72% | 35 | 0.35 | 72% |
| Technical | 56% | 34 | 0.28 | 81% |
| Timeline | 38% | 37 | 0.18 | 67% |
| Vendor | 31% | 22 | 0.42 | 60% |

### Most Dangerous Risks (Highest Loss Correlation)
1. {risk} -- appears in {n}% of lost deals, only {n}% mitigation success
2. ...

### Mitigation Library Gaps
- {category}: Need {asset_type} -- current success rate only {n}%
- ...

### Risk Prediction Performance
- Overall hit rate: {n}% (trending {up/down/flat})
- Best predicted category: {category} ({n}% accuracy)
- Worst predicted category: {category} ({n}% accuracy, {n}% surprise rate)

### Segment Insights
- {segment} has unique risk: {risk} -- add to prediction model
- {segment} rarely has {category} risk -- deprioritize in prep

### Recommendations
1. **Prediction:** {specific improvement}
2. **Mitigation:** {content to create or process to fix}
3. **Discovery:** {questions to add/remove}
```

### 8. Update artifacts

- Store the report as an Attio note on a "Risk Intelligence" record
- Update the risk question bank with new/retired questions
- Push segment risk profiles to the enrichment signals used by `risk-discovery-call-prep`
- Fire PostHog event: `risk_pattern_analysis_completed` with summary metrics

## Output

- Risk frequency matrix showing which categories matter most
- Mitigation effectiveness analysis for content library prioritization
- Segment-level risk profiles for prediction improvement
- Risk-to-loss pathway analysis for process diagnosis
- Actionable recommendations in a structured report

## Triggers

Run bi-weekly (every 2 weeks) via n8n scheduled workflow. Can also be triggered manually after a significant batch of deal outcomes (wins/losses) are logged.
