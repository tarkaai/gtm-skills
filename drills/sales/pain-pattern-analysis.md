---
name: pain-pattern-analysis
description: Analyze pain data across all discovery calls to identify patterns by segment, refine question banks, and prioritize ICP adjustments
category: Sales
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

# Pain Pattern Analysis

This drill aggregates pain data from all discovery calls to surface cross-prospect patterns. It identifies which pains appear most frequently, which segments have the highest total quantified pain, and which discovery questions are most effective at surfacing valuable pains. The output feeds ICP refinement, question bank optimization, and sales playbook updates.

## Input

- At least 10 completed discovery calls with pain extraction data in Attio
- PostHog events from `pain_discovery_call_completed`
- n8n instance for scheduled execution

## Steps

### 1. Extract pain data from CRM

Query Attio for all deals with `pain_discovery_date` set. Pull for each deal:
- Company attributes: industry, headcount range, funding stage, region
- Pain data: pain_count, total_quantified_pain, pain_to_price_ratio, pain_data_json
- Deal outcome: won, lost, or open (if available)

Using `attio-lists`, create a filtered list: "Discovery Calls — Last 30 Days" with all deals that have pain data.

### 2. Build the pain frequency matrix

Parse all `pain_data_json` fields and aggregate:

```json
{
  "pain_categories": {
    "operational": {"count": 23, "avg_severity": 7.2, "avg_annual_cost": 145000, "appears_in_pct_of_calls": 0.85},
    "financial": {"count": 18, "avg_severity": 6.8, "avg_annual_cost": 210000, "appears_in_pct_of_calls": 0.67},
    "technical": {"count": 12, "avg_severity": 5.4, "avg_annual_cost": 89000, "appears_in_pct_of_calls": 0.44},
    "strategic": {"count": 8, "avg_severity": 8.1, "avg_annual_cost": 340000, "appears_in_pct_of_calls": 0.30},
    "compliance": {"count": 4, "avg_severity": 9.0, "avg_annual_cost": 500000, "appears_in_pct_of_calls": 0.15}
  },
  "top_specific_pains": [
    {"summary": "Manual data entry across systems", "frequency": 15, "avg_cost": 160000, "win_correlation": 0.72},
    {"summary": "Inconsistent follow-up causing lost deals", "frequency": 12, "avg_cost": 230000, "win_correlation": 0.65}
  ]
}
```

### 3. Segment by company attributes

Break the pain matrix by segment to find where your product delivers the most value:

- **By industry:** Which industry has the highest average total_quantified_pain?
- **By company size:** Do larger companies have different pain profiles than smaller ones?
- **By funding stage:** Are post-Series A companies more likely to have quantifiable pain?
- **By deal outcome:** Which pains correlate with won deals vs. lost deals?

Use Claude via `hypothesis-generation` to analyze the segmented data and produce:
- Top 3 ICP refinement recommendations (e.g., "Prioritize Series B SaaS companies — they have 2.3x higher quantified pain")
- Top 3 messaging recommendations (e.g., "Lead with operational efficiency pain — it appears in 85% of calls and has the highest win correlation")
- Top 3 question bank updates (e.g., "Add questions about compliance pain for regulated industries — low frequency but very high severity when found")

### 4. Evaluate question effectiveness

For each discovery question in the question bank, calculate:
- **Surface rate:** How often does asking this question surface a new pain?
- **Quantification rate:** When a pain surfaces, how often can it be quantified?
- **Win correlation:** Do deals where this question surfaced pain close at a higher rate?

Rank questions by `surface_rate * quantification_rate * win_correlation`. Retire the bottom 20% and generate replacement questions using Claude.

### 5. Generate the pain intelligence report

Compile findings into a structured report:

```markdown
## Pain Intelligence Report — {date_range}
### Based on {n} discovery calls

### Top Pains by Frequency
| Rank | Pain | Frequency | Avg Cost | Win Correlation |
|------|------|-----------|----------|-----------------|
| 1 | ... | ... | ... | ... |

### Top Pains by Dollar Impact
| Rank | Pain | Avg Cost | Frequency | Confidence |
|------|------|----------|-----------|------------|
| 1 | ... | ... | ... | ... |

### Segment Analysis
- Best segment: {segment} — {avg_pain_to_price_ratio}x ratio
- Emerging segment: {segment} — growing pain in {category}
- Weak segment: {segment} — consider deprioritizing

### Question Bank Performance
- Top performing questions: ...
- Questions to retire: ...
- New questions to test: ...

### ICP Recommendations
1. ...
2. ...
3. ...
```

### 6. Update artifacts

- Store the report as an Attio note on a "Pain Intelligence" record
- Update the question bank file with new/retired questions
- Push segment recommendations to the ICP definition document
- Fire PostHog event: `pain_pattern_analysis_completed` with summary metrics

## Output

- Pain frequency matrix showing which pains matter most
- Segment-level analysis for ICP refinement
- Question effectiveness rankings for discovery optimization
- Actionable recommendations in a structured report

## Triggers

Run bi-weekly (every 2 weeks) via n8n scheduled workflow. Can also be triggered manually after a batch of discovery calls.
