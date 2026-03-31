---
name: win-loss-insight-extraction
description: Analyze win/loss transcripts and survey responses to extract categorized, actionable insights
category: Research
tools:
  - Anthropic
  - Fireflies
  - Typeform
  - Attio
  - n8n
fundamentals:
  - transcript-insight-extraction
  - fireflies-action-items
  - fireflies-transcription
  - attio-deals
  - n8n-workflow-basics
---

# Win/Loss Insight Extraction

This drill takes raw interview transcripts and survey responses, runs them through structured AI analysis, and produces categorized insights stored in your CRM. The goal is to turn qualitative buyer feedback into quantified patterns that drive decisions.

## Prerequisites

- At least 1 completed win/loss interview transcript (from Fireflies) or survey response (from Typeform)
- Anthropic API key configured
- Attio CRM with the deal linked to the interview
- n8n instance (for automated processing at Baseline+ levels)

## Input

- Fireflies transcript ID(s) for completed interviews
- Typeform webhook payloads for completed surveys
- Deal ID in Attio to link insights back to

## Steps

### 1. Retrieve the raw data

**For interview transcripts:** Use the Fireflies GraphQL API via the `fireflies-action-items` fundamental to fetch the transcript:
```graphql
query { transcript(id: "{transcript_id}") {
  title, transcript_text, summary, action_items, speakers { name }, duration
}}
```

**For survey responses:** Parse the Typeform webhook payload or query the Typeform Responses API:
```
GET https://api.typeform.com/forms/{form_id}/responses?query={deal_id}
```
Extract the hidden fields (deal_id, outcome, contact_name) and all question/answer pairs.

### 2. Run structured insight extraction

Using the `transcript-insight-extraction` fundamental, send the transcript or survey text to Claude API for analysis. The extraction returns 10 structured fields: outcome, primary reason, competitors mentioned, product feedback, sales process feedback, pricing feedback, decision criteria, actionable insights, sentiment score, and key quotes.

For survey responses, adapt the prompt: instead of a transcript, provide the question-answer pairs as structured text and ask Claude to extract the same 10 fields (some fields like key quotes may use the respondent's written answers).

### 3. Validate and enrich the extraction

Review the Claude output for quality:
- Are the KEY_QUOTES actually present in the source transcript? (Compare against raw text)
- Are the ACTIONABLE_INSIGHTS specific enough to act on? "Improve the product" is not actionable. "Add Salesforce integration — mentioned as a dealbreaker by the buyer" is actionable.
- Is the SENTIMENT_SCORE consistent with the overall tone?

If any field is vague or missing, re-prompt Claude with the specific field and ask it to try again with more detail.

### 4. Categorize each insight

Take each item from ACTIONABLE_INSIGHTS and PRODUCT_FEEDBACK and assign a category:
- `product-gap` — Feature or capability we lack
- `product-strength` — Feature that helped us win
- `pricing` — Price, packaging, or value perception
- `sales-process` — How the buying experience affected the outcome
- `competitive` — Direct competitor comparison
- `messaging` — How our positioning/marketing landed with the buyer
- `timing` — Budget, urgency, or market timing factors

Also assign a priority: `high` (mentioned as a primary decision factor), `medium` (mentioned but not decisive), `low` (noted in passing).

### 5. Store insights in the CRM

Using the `attio-deals` fundamental, create a structured note on the deal record in Attio:

```
## Win/Loss Analysis — {Contact Name} — {Date}
**Outcome:** {Won/Lost}
**Primary Reason:** {one sentence}
**Sentiment Score:** {1-10}
**Competitors:** {comma-separated list}

### Decision Criteria (ranked)
1. {criterion}
2. {criterion}
3. {criterion}

### Actionable Insights
- [{category}] [{priority}] {insight text}
- [{category}] [{priority}] {insight text}

### Key Quotes
> "{quote 1}"
> "{quote 2}"
> "{quote 3}"
```

Tag the note as "win-loss-insight" so it can be queried later for aggregation.

### 6. Update deal metadata

On the deal record in Attio, set these custom fields:
- Win/Loss Interview Status: "Analyzed"
- Primary Win/Loss Reason: {from extraction}
- Competitors In Deal: {from extraction}
- Buyer Sentiment Score: {1-10}
- Interview Date: {date}

### 7. Build the automation (Baseline+ levels)

Using `n8n-workflow-basics`, create a workflow that processes insights automatically:
- **Trigger:** Fireflies webhook (transcript ready) or Typeform webhook (survey completed)
- **Step 1:** Fetch the full transcript/response
- **Step 2:** Call Claude API for extraction
- **Step 3:** Validate the output (check all fields present, quotes exist in source)
- **Step 4:** Create the structured note in Attio
- **Step 5:** Update deal metadata fields
- **Step 6:** If any high-priority product-gap insight is found, send a Slack notification to the product channel

## Output

For each processed interview/survey:
- Structured insight note on the Attio deal record, tagged "win-loss-insight"
- Deal metadata fields updated with win/loss reason, competitors, and sentiment
- High-priority insights flagged via Slack (if automation is active)

## Triggers

- **Manual (Smoke):** Run after each interview, triggered by the analyst
- **Automated (Baseline+):** n8n workflow fires on Fireflies transcript webhook or Typeform submission webhook
