---
name: need-auto-scoring
description: Automated pre-call need hypothesis pipeline that enriches prospects and predicts likely need profiles before discovery
category: Sales
tools:
  - Clay
  - Attio
  - n8n
  - PostHog
  - Anthropic
fundamentals:
  - clay-intent-scoring
  - clay-enrichment-waterfall
  - clay-scoring
  - clay-table-setup
  - attio-custom-attributes
  - attio-deals
  - n8n-workflow-basics
  - n8n-triggers
  - posthog-custom-events
---

# Need Auto-Scoring Pipeline

This drill builds an automated pipeline that generates a need hypothesis for every new lead before any human contact. Using enrichment data — job postings, tech stack, company news, industry, and growth signals — it predicts which business need categories are likely relevant and assigns pre-call need scores. This is not qualification; it is hypothesis generation to make discovery calls focused and efficient.

## Input

- New lead enters Attio (via form submission, import, or outbound list)
- Need categories defined (from `need-scorecard-setup` drill)
- Clay table with need-relevant enrichment columns
- n8n instance for orchestration

## Steps

### 1. Set up the trigger workflow in n8n

Using the `n8n-triggers` fundamental, create a workflow triggered by new deal creation in Attio:

- **Trigger:** Attio webhook — fires when a new deal record is created
- **Filter:** Only process deals where `need_total_score` is 0 or empty (avoids re-processing)

### 2. Push the lead to Clay for need-relevant enrichment

When a new deal triggers the workflow:

1. Extract company name, contact email, LinkedIn URL, and industry from the Attio record
2. Use the `clay-table-setup` fundamental to add the row to your Need Assessment enrichment table
3. Trigger Clay's enrichment columns (they run automatically on new rows)
4. Wait for enrichment to complete (poll Clay API every 30 seconds for up to 5 minutes)

### 3. Enrich with need-relevant signals

Configure Clay enrichment columns using `clay-enrichment-waterfall` and `clay-intent-scoring`:

**Job posting analysis:**
- Pull active job listings from the prospect's company
- Scan for keywords that map to your need categories (e.g., "data entry" maps to "reducing manual data entry," "reporting" maps to "improving reporting visibility")
- Score: number of matching job postings * relevance weight

**Tech stack analysis:**
- Identify current tools via BuiltWith, Wappalyzer, or job posting mentions
- Map gaps: if they use Tool A but not Tool B (which solves a need your product addresses), that is a need signal
- Flag competitors: if they use a competitor product, this is both a need signal and a potential switching trigger

**Company news and growth signals:**
- Recent funding → likely scaling needs (automation, reporting visibility)
- Headcount growth >20% → operational efficiency needs
- New leadership in relevant departments → potential mandate for change
- Industry regulatory changes → compliance or process needs

**Industry benchmarks:**
- Compare the prospect's company profile to your existing customers in the same industry
- Which need categories are most common among similar companies that bought?

### 4. Generate need hypothesis via Claude

After enrichment, use Claude to synthesize the signals into a need hypothesis:

```json
{
  "model": "claude-sonnet-4-20250514",
  "messages": [{
    "role": "user",
    "content": "Based on the following enrichment data for {company_name}, predict which of these need categories are likely relevant and assign pre-call hypothesis scores (1-3). Return JSON.\n\nNeed categories: {categories_json}\n\nEnrichment signals:\n- Job postings: {job_data}\n- Tech stack: {tech_stack}\n- Recent news: {news}\n- Industry: {industry}\n- Company size: {size}\n- Growth rate: {growth}\n\nReturn:\n{\n  \"hypothesized_needs\": [\n    {\"category\": \"...\", \"predicted_severity\": 1-3, \"evidence\": \"string\", \"confidence\": 0.0-1.0}\n  ],\n  \"overall_need_hypothesis_score\": 0-21,\n  \"discovery_priority_categories\": [\"categories to probe first on the call\"],\n  \"recommended_questions\": [\"tailored questions based on the signals\"]\n}"
  }]
}
```

### 5. Push hypothesis scores to Attio

Using `attio-deals`, update the deal record with pre-call hypothesis scores:
- Set each `need_cat_N_score` to the predicted severity
- Set `need_total_score` to the overall hypothesis score
- Set `need_assessment_source` = "Pre-call Hypothesis"
- Set `need_last_assessed` = today

Add an Attio note with the full hypothesis: which need categories are predicted strong, which are weak, what evidence supports each prediction, and what to probe in discovery.

### 6. Route based on hypothesis

In the n8n workflow, add routing logic:

- **High predicted need (score >=15):** Move to "Need Hypothesized" stage. Slack alert to founder: "High-need lead: {company} — predicted score {score}. Top needs: {top 2 categories}. Book discovery ASAP."
- **Medium predicted need (10-14):** Move to "Need Hypothesized." Note which categories are uncertain and need discovery validation.
- **Low predicted need (<10):** Move to "Need Hypothesized" with lower priority. Consider batch processing these leads rather than individual discovery calls.

### 7. Log to PostHog

Using `posthog-custom-events`, fire a `need_hypothesis_generated` event:
```json
{
  "event": "need_hypothesis_generated",
  "properties": {
    "deal_id": "...",
    "company_name": "...",
    "hypothesis_score": 16,
    "predicted_critical_count": 3,
    "enrichment_coverage": 0.85,
    "top_need_category": "reducing manual data entry",
    "confidence": 0.7
  }
}
```

### 8. Handle enrichment failures

If Clay enrichment fails or returns sparse data (< 40% of columns populated):
- Generate a minimal hypothesis using only available data
- Set confidence to "low" in the Attio note
- Flag for manual research: "Need hypothesis incomplete — enrichment coverage {X}%. Review before discovery call."
- Do not auto-route to high priority regardless of score

## Output

- Every new deal in Attio gets a pre-call need hypothesis within minutes
- Discovery calls are pre-loaded with tailored questions based on predicted needs
- Founder sees which need categories to probe and which have strong evidence
- PostHog tracks hypothesis generation for later accuracy analysis

## Triggers

Runs automatically on every new deal creation via n8n webhook. No manual intervention needed. Monitor n8n execution logs weekly for errors.
