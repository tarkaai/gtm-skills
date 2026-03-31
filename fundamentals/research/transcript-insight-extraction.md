---
name: transcript-insight-extraction
description: Use Claude API to extract structured win/loss insights from interview transcripts and survey responses
tool: Anthropic
product: Claude API
difficulty: Config
---

# Extract Win/Loss Insights from Transcripts

Use the Claude API to systematically analyze win/loss interview transcripts and survey responses, extracting structured insights categorized by theme.

## Prerequisites

- Anthropic API key from console.anthropic.com
- Interview transcripts (from Fireflies, Grain, or manual notes)
- n8n instance for automation (recommended)

## Steps

1. **Prepare the transcript for analysis.** Retrieve the transcript from Fireflies API or your storage. Clean it: remove filler words sections, trim speaker labels to first name only, and split into chunks of 50,000 tokens max if the transcript exceeds Claude's efficient processing range.

2. **Call the Claude API with a structured extraction prompt.** Use claude-sonnet-4-20250514 for cost-effective analysis:
   ```
   POST https://api.anthropic.com/v1/messages
   Headers: x-api-key: {ANTHROPIC_API_KEY}, anthropic-version: 2023-06-01
   Body: {
     "model": "claude-sonnet-4-20250514",
     "max_tokens": 4096,
     "temperature": 0.2,
     "messages": [{"role": "user", "content": "TRANSCRIPT:\n{transcript}\n\nAnalyze this win/loss interview transcript. Extract:\n1. OUTCOME: Won or Lost\n2. PRIMARY_REASON: The single biggest factor in the decision (1 sentence)\n3. COMPETITORS_MENTIONED: List of competitor names mentioned\n4. PRODUCT_FEEDBACK: Specific product strengths or gaps mentioned (list each with a direct quote)\n5. SALES_PROCESS_FEEDBACK: What the buyer said about the sales experience (list each with a direct quote)\n6. PRICING_FEEDBACK: Any comments on pricing, packaging, or value perception\n7. DECISION_CRITERIA: What mattered most to this buyer (ranked list)\n8. ACTIONABLE_INSIGHTS: 2-3 specific, concrete things we should change based on this interview\n9. SENTIMENT_SCORE: 1-10 rating of overall buyer sentiment toward us\n10. KEY_QUOTES: 3-5 verbatim quotes that are most revealing\n\nReturn as JSON."}]
   }
   ```

3. **Parse the JSON response.** Extract the structured fields from Claude's response. Validate that all 10 fields are present. If any field is null or missing, re-prompt with a follow-up asking specifically for that field.

4. **Categorize insights by theme.** Group the ACTIONABLE_INSIGHTS into standard categories:
   - `product-gap` — Missing feature or capability
   - `product-strength` — Feature that drove the win
   - `pricing` — Price, packaging, or discount-related
   - `sales-process` — How the sales experience affected the outcome
   - `competitive` — Competitor-specific intelligence
   - `messaging` — How our positioning/messaging landed
   - `timing` — Budget cycle, urgency, or timeline factors

5. **Store insights in your CRM.** Push the structured insights to Attio as a note on the deal record via the Attio MCP. Include: outcome, primary reason, competitors mentioned, sentiment score, and each actionable insight as a separate line. Tag the note as "win-loss-insight" for later querying.

6. **Batch processing for multiple transcripts.** When processing a backlog, loop through transcripts sequentially with a 1-second delay between API calls to respect rate limits. Track processing status: queue each transcript, mark as "processing", then "complete" or "failed". Log any failures for manual review.

7. **Quality check the extraction.** For the first 5 transcripts, manually compare Claude's extraction against the raw transcript. Check: Are the key quotes actually verbatim? Are the insights genuinely actionable (not vague)? Is the sentiment score reasonable? Adjust the prompt if extraction quality is below 90% accuracy.
