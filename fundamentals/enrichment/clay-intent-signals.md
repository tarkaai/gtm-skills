---
name: clay-intent-signals
description: Enrich leads with behavioral intent signals using Clay's data providers and Claygent
tool: Clay
difficulty: Advanced
---

# Enrich Leads with Intent Signals in Clay

Pull behavioral and timing signals that indicate purchase intent: website visits, content engagement, job postings, funding events, technology changes, and competitor mentions. These signals feed the intent dimension of lead scoring.

## Prerequisites

- Clay account with enrichment credits
- Clay table with leads (company name, domain, contact email at minimum)
- Understanding of which intent signals matter for your ICP

## Steps

### 1. Configure website visitor identification

Add a Clay enrichment column using the **Website Visitor Identification** provider. Input: company domain. Output: recent visitor activity, pages viewed, visit frequency.

If the provider returns no data (common for smaller companies), fall back to the Claygent approach in step 5.

### 2. Set up funding event detection

Add a **Crunchbase** or **PitchBook** enrichment column. Input: company domain. Output: last funding round date, amount, stage.

Score the output:
- Funding in last 30 days: +30 intent points
- Funding in last 90 days: +20 intent points
- Funding in last 180 days: +10 intent points
- No recent funding: +0

### 3. Configure job posting signals

Add a **Job Posting** enrichment column (Clay's built-in or via Claygent scraping). Input: company domain. Query: job postings matching keywords relevant to your product category.

Score the output:
- 3+ relevant job postings: +25 intent points (building a team, need tools)
- 1-2 relevant postings: +10 intent points
- 0 postings: +0

### 4. Detect technology stack changes

Add a **BuiltWith** or **Wappalyzer** enrichment column. Input: company domain. Output: current technology stack.

Score the output:
- Uses a complementary technology: +20 intent points (integration opportunity)
- Uses a competing technology: +15 intent points (displacement opportunity)
- Recently added/removed a tool in your category: +25 intent points
- No relevant tech detected: +0

### 5. Run Claygent for custom intent research

For signals not available via structured providers, use Claygent (Clay's AI agent):

```
Prompt: "Research {company_name} ({domain}). Find:
1. Any recent news about challenges in [your product's problem area]
2. Any public mentions of evaluating tools in [your category]
3. Any leadership changes in [relevant department] in the last 90 days
4. Any conference talks or blog posts about [relevant topic]

Return a JSON object: {news_mentions: int, tool_evaluation_signals: int, leadership_changes: int, thought_leadership: int}"
```

Score: sum of all signals found, capped at 30 intent points.

### 6. Build the composite intent score column

Create a formula column that sums all intent signal scores:

```
intent_score = min(
  funding_signal + job_posting_signal + tech_change_signal + claygent_signal + visitor_signal,
  100
)
```

Cap at 100. This becomes the intent dimension of your lead score.

### 7. Set up scheduled refresh

Intent signals decay. Configure the Clay table to re-run enrichment columns on a schedule:
- Funding and job posting signals: refresh weekly
- Technology signals: refresh monthly
- Claygent research: refresh bi-weekly

Use Clay's built-in scheduling or trigger refreshes via the Clay API from an n8n workflow.

## API Integration

To trigger Clay enrichment from n8n or another automation:

```
POST https://api.clay.com/v1/tables/{table_id}/rows
{
  "data": {
    "company_name": "Acme Corp",
    "domain": "acme.com",
    "contact_email": "jane@acme.com"
  }
}
```

Poll for enrichment completion:
```
GET https://api.clay.com/v1/tables/{table_id}/rows/{row_id}
```

Check that all enrichment columns have populated before pulling the intent score.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Clay | Multi-provider enrichment + Claygent | Best coverage, credit-based pricing |
| Apollo | Intent signals API | Built-in intent data, fewer custom signals |
| Bombora | Intent data API | Specialized B2B intent, topic-level signals |
| 6sense | Revenue AI API | Account-level intent scoring |
| ZoomInfo | Intent signals | Broad coverage, higher price point |
| Leadfeeder | Website visitor identification | Focused on web visit intent |

## Error Handling

- If a provider returns no data, assign 0 points for that signal (not null). Missing data is not negative signal.
- If Claygent times out, retry once. If it fails again, skip and log for manual review.
- If credit balance is low, prioritize: funding > job postings > tech stack > Claygent research.
- Monitor enrichment hit rates. If a provider returns data for <20% of your leads, consider replacing it.
