---
name: competitive-discovery-call
description: Structured competitive discovery workflow that extracts competitor intelligence from qualification calls, logs to CRM, and routes to battlecard delivery
category: Sales
tools:
  - Fireflies
  - Anthropic
  - Attio
  - PostHog
fundamentals:
  - fireflies-transcription
  - call-transcript-competitor-extraction
  - competitive-positioning-generation
  - attio-deals
  - attio-notes
  - attio-custom-attributes
  - posthog-custom-events
---

# Competitive Discovery Call

This drill runs after every qualification call to extract competitive intelligence, update the deal record, and (if a known competitor is detected) deliver a tailored battlecard and positioning response. It turns every prospect conversation into a competitive data point that feeds the broader competitive intelligence database.

## Input

- A completed qualification or discovery call with a Fireflies transcript
- Attio deal record for the prospect
- Competitors object in Attio (created by `competitive-battlecard-assembly` or `competitive-intel-aggregation`)

## Steps

### 1. Extract competitive situation from the transcript

Run the `call-transcript-competitor-extraction` fundamental on the call transcript. This produces:
- List of competitors being evaluated with type, stage, and sentiment
- Decision criteria ranked by priority
- Decision process details (timeline, stakeholders, evaluation method)
- Status quo analysis (current solution, switching barriers)
- Competitive risk assessment

### 2. Update the deal record in Attio

Using the Attio MCP, update the deal with competitive situation data:

```json
{
  "competitors_evaluated": "Comma-separated list of competitor names",
  "primary_competitor": "The competitor furthest along in evaluation or most frequently mentioned",
  "competitive_risk": "low|medium|high|critical from extraction",
  "evaluation_method": "From extraction: formal_rfp, informal_comparison, etc.",
  "decision_criteria_top3": "Top 3 criteria from extraction, comma-separated",
  "competitive_situation_date": "Today's date",
  "do_nothing_risk": "low|medium|high from status_quo_analysis"
}
```

Create a structured note on the deal:

```markdown
## Competitive Situation — {date}
**Competitors:** {list}
**Risk Level:** {risk}
**Evaluation Method:** {method}

### Decision Criteria (ranked)
1. {criterion_1} — {priority}
2. {criterion_2} — {priority}
3. {criterion_3} — {priority}

### Per-Competitor Detail
#### {Competitor A}
- **Stage:** {evaluation_stage}
- **Sentiment:** {sentiment} — "{evidence_quote}"
- **Their strengths (cited by prospect):** {strengths}
- **Their gaps (cited by prospect):** {gaps}

### Status Quo
- **Current solution:** {current_solution}
- **Pain with current:** {pains}
- **Switching barriers:** {barriers}

### Discovery Quality
- **Seller score:** {score}
- **Missed questions:** {list of questions seller should have asked}
```

### 3. Route to battlecard delivery (if known competitor)

Check if any extracted competitor name matches a Competitors record in Attio (use fuzzy matching — "HubSpot" matches "Hubspot" matches "hubspot"):

- **Match found:** Retrieve the battlecard from the Competitor record. Run the `competitive-positioning-generation` fundamental with the specific competitor context + this deal's pain data + decision criteria. Deliver the positioning response to the deal owner via Slack or email.
- **No match (new competitor):** Create a new Competitor record in Attio with the data extracted from this call. Flag it for enrichment by `competitive-battlecard-assembly` once 3+ deals mention this competitor.

### 4. Fire PostHog events

Log the following events:

```json
{"event": "competitive_situation_identified", "properties": {"deal_id": "...", "competitor_count": 2, "risk_level": "medium", "call_id": "..."}}
```

For each competitor:
```json
{"event": "competitor_named", "properties": {"deal_id": "...", "competitor_name": "...", "competitor_type": "...", "evaluation_stage": "...", "prospect_sentiment": "..."}}
```

If no competitors found:
```json
{"event": "status_quo_bias_detected", "properties": {"deal_id": "...", "do_nothing_risk": "high", "current_solution": "..."}}
```

### 5. Update competitive frequency table

Query Attio for the Competitors object and increment the `Mention Count` for each competitor identified. This running total powers battlecard prioritization — competitors with the most mentions get the most investment in battlecard quality.

## Output

- Deal record updated with competitive situation data
- Structured competitive note attached to the deal
- Battlecard + positioning response delivered (if known competitor)
- New Competitor record created (if unknown competitor)
- PostHog events logged for pipeline-wide competitive analytics

## Triggers

- **After every qualification call:** Run automatically via n8n when Fireflies publishes a new transcript for a deal in the Qualified pipeline stage
- **Manual re-run:** Can be triggered manually on any deal to re-analyze a specific call
- **Batch backfill:** Run on the last 30 days of transcripts to build initial competitive baseline
