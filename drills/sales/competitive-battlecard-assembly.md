---
name: competitive-battlecard-assembly
description: Build and maintain per-competitor battlecards from deal transcripts, win/loss data, and market intelligence, stored as structured records in CRM
category: Sales
tools:
  - Attio
  - Anthropic
  - Clay
  - n8n
fundamentals:
  - competitive-intel-aggregation
  - competitive-positioning-generation
  - call-transcript-objection-extraction
  - attio-deals
  - attio-notes
  - attio-custom-attributes
  - clay-claygent
  - clay-company-search
  - n8n-workflow-basics
  - n8n-scheduling
---

# Competitive Battlecard Assembly

This drill builds structured, data-backed competitive battlecards for each named competitor that appears in your sales pipeline. Unlike static documents, these battlecards are living CRM records that update automatically as new deal data, win/loss outcomes, and competitive intelligence accumulate.

## Input

- Attio CRM with deal records that have `competitor_mentioned` attributes
- At least 3 completed deals where a specific competitor was mentioned
- Clay account for competitor company enrichment
- Anthropic API key for synthesis

## Steps

### 1. Initialize the Competitors object in Attio

If not already created (check first via Attio MCP), create a custom object called "Competitors" with these attributes:

| Attribute | Type | Purpose |
|-----------|------|---------|
| Name | Text | Competitor company name |
| Website | URL | Competitor's primary website |
| Mention Count | Number | Total times mentioned across all deals |
| Win Rate Against | Number (%) | Deals won when this competitor was in the deal |
| Loss Rate Against | Number (%) | Deals lost to this competitor |
| Avg Deal Size (Competitive) | Currency | Average deal size in competitive deals with them |
| Their Strengths | Text (multi-line) | Synthesized from buyer quotes |
| Their Weaknesses | Text (multi-line) | Synthesized from buyer quotes |
| Our Differentiators | Text (multi-line) | Where we win most often |
| Common Objections | Text (multi-line) | Recurring objections in competitive deals |
| Winning Frameworks | Text (multi-line) | Response frameworks with highest win rate against them |
| Trap Questions | Text (multi-line) | Questions that highlight our strengths vs their gaps |
| Pricing Intel | Text (multi-line) | Known pricing from prospects and public sources |
| Recent Changes | Text (multi-line) | Product/pricing changes detected by monitoring |
| Last Updated | Date | When this record was last refreshed |
| Battlecard Version | Number | Incremented on each refresh |

### 2. Aggregate deal data per competitor

Query Attio for all deals where `competitor_mentioned` matches the target competitor. For each deal, extract:
- Deal outcome (won/lost/open)
- Objection data (from `call-transcript-objection-extraction` results stored in notes)
- Pain data (from discovery notes)
- Decision criteria mentioned
- Win/loss reasons (if closed)
- Buyer quotes about the competitor

Use Claude API to synthesize across all deals:

```json
{
  "prompt": "You are analyzing {n} sales deals where {competitor_name} was mentioned as a competitor. Synthesize the following data into a competitive battlecard.\n\nDeal data:\n{deals_json}\n\nFor each section, use ONLY information from the deal data. Do not invent strengths or weaknesses. Quote buyers directly where possible.\n\nReturn JSON:\n{\n  \"their_strengths\": [\"Strength 1 with supporting buyer quote\", ...],\n  \"their_weaknesses\": [\"Weakness 1 with supporting buyer quote\", ...],\n  \"our_differentiators\": [\"Differentiator 1 — why it matters to buyers\", ...],\n  \"common_objections\": [{\"objection\": \"...\", \"frequency\": n, \"best_response\": \"...\"}],\n  \"winning_frameworks\": [{\"framework\": \"...\", \"win_rate\": 0.xx, \"sample_size\": n}],\n  \"trap_questions\": [\"Question that surfaces their weakness without naming them\", ...],\n  \"pricing_intel\": {\"known_range\": \"...\", \"packaging\": \"...\", \"discount_patterns\": \"...\"},\n  \"deal_patterns\": {\"we_win_when\": \"...\", \"we_lose_when\": \"...\", \"key_decision_criteria\": [\"...\"]}\n}"
}
```

### 3. Enrich with public competitive intelligence

Run Clay enrichment on the competitor:
- Company search via `clay-company-search` for firmographics, headcount, funding, tech stack
- Claygent scrape of their pricing page, features page, and recent blog posts via `clay-claygent`
- G2/Capterra ratings (if available via Clay enrichment)

Append public intel to the battlecard.

### 4. Store the battlecard in Attio

Update the Competitor record with all synthesized data. Create a structured note with the full battlecard:

```markdown
## {Competitor Name} Battlecard v{version}
**Updated:** {date} | **Deals analyzed:** {n} | **Win rate against:** {win_rate}%

### When We Win
{synthesized from deals where we beat them}

### When We Lose
{synthesized from deals where they beat us}

### Their Strengths (from buyer quotes)
{bulleted list with actual buyer quotes}

### Their Weaknesses (from buyer quotes)
{bulleted list with actual buyer quotes}

### Top Objections & Responses
| Objection | Frequency | Best Response Framework | Win Rate |
|-----------|-----------|------------------------|----------|

### Trap Questions
{questions that surface their gaps without naming them}

### Pricing Intelligence
{known pricing, packaging, discount patterns}

### Recent Product/Market Changes
{from competitor-changelog-monitoring if available}
```

### 5. Set up automated refresh

Create an n8n workflow triggered weekly (Monday 7 AM):
1. Query Attio for new deals involving each tracked competitor in the past 7 days
2. If new data exists, re-run the synthesis (Step 2) with all historical + new data
3. Update the Competitor record and increment `Battlecard Version`
4. If win rate against any competitor drops below 40%, send Slack alert
5. Fire PostHog event: `battlecard_refreshed` with competitor name, deal count, win rate

## Output

- Structured Competitor records in Attio with data-backed battlecards
- Weekly automated refresh incorporating new deal data
- Win rate tracking per competitor over time
- Alerts when competitive position degrades

## Triggers

- **Initial build:** Run manually for each competitor with 3+ deal mentions
- **Refresh:** Weekly cron via n8n, or triggered when a new deal closes involving a tracked competitor
- **Alert:** Immediate Slack notification if win rate drops below threshold
