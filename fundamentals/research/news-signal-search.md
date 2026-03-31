---
name: news-signal-search
description: Search for recent company news, funding, launches, and leadership changes via web APIs and Clay
tool: Clay
product: Clay
difficulty: Config
---

# News Signal Search

Query recent news about a target company to surface outreach-relevant signals: funding announcements, product launches, executive hires, partnerships, and layoffs. Returns structured signal data that feeds account briefs and personalization hooks.

## Prerequisites

- Clay account with Claygent credits
- Target company name and domain
- Optional: Google Custom Search API key for direct news queries

## Steps

### 1. Search via Clay Claygent

Add a Claygent enrichment column in your Clay table with this prompt:

```
Search for news about {Company Name} ({domain}) from the last 90 days. Return a JSON array of up to 5 items. For each item include:
- "date": approximate publication date (YYYY-MM-DD)
- "type": one of "funding", "product_launch", "executive_hire", "partnership", "acquisition", "layoff", "expansion", "award", "other"
- "headline": one-sentence summary
- "source": publication name
- "outreach_relevance": one sentence explaining why this matters for a sales conversation

If no recent news is found, return an empty array.
```

Cost: 5-10 Clay credits per company.

### 2. Search via Google Custom Search API (alternative)

For higher volume or when Clay credits are limited:

```
GET https://www.googleapis.com/customsearch/v1
  ?key={GOOGLE_API_KEY}
  &cx={SEARCH_ENGINE_ID}
  &q="{Company Name}" news
  &dateRestrict=m3
  &num=5
```

Response contains `items[].title`, `items[].link`, `items[].snippet`. Parse these into the same structured format.

Cost: Google Custom Search API provides 100 free queries/day, then $5 per 1,000 queries.

### 3. Search via Bing News Search API (alternative)

```
GET https://api.bing.microsoft.com/v7.0/news/search
  ?q={Company Name}
  &freshness=Month
  &count=5
Headers:
  Ocp-Apim-Subscription-Key: {BING_API_KEY}
```

Response: `value[].name`, `value[].url`, `value[].description`, `value[].datePublished`.

Cost: Bing News Search v7 offers 1,000 free transactions/month, then $3 per 1,000 transactions.

### 4. Search via Crunchbase API (funding-specific)

For funding events specifically:

```
GET https://api.crunchbase.com/api/v4/entities/organizations/{company_permalink}
  ?card_ids=raised_funding_rounds
  &user_key={CRUNCHBASE_API_KEY}
```

Returns funding rounds with: `announced_on`, `money_raised`, `investment_type`, `lead_investor_identifiers`.

Cost: Crunchbase Basic API is $29/month for 200 calls/month. Pro API starts at custom pricing.

### 5. Score the signals

After retrieval, score each news item for outreach timing:

| Signal Type | Recency | Score |
|---|---|---|
| Funding | Last 30 days | +30 |
| Funding | 31-90 days | +15 |
| Executive hire | Last 30 days | +25 |
| Product launch | Last 30 days | +20 |
| Expansion/new market | Last 60 days | +15 |
| Layoff/restructure | Last 60 days | +10 (pain signal) |

Sum scores. Accounts with composite news score >= 25 are high-priority for outreach.

### 6. Store results

Write the structured news data to your CRM (Attio) as a note on the company record tagged `news-signals`. Include the search date so staleness is trackable.

```
attio.create_note({
  parent_object: "companies",
  parent_record_id: "{company_id}",
  title: "News Signals — {date}",
  content: "{structured_news_json}",
  tags: ["news-signals", "account-research"]
})
```

## Tool Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Clay Claygent | AI-powered web research | Best for small batches, credit-based |
| Google Custom Search API | Structured news search | High volume, 100 free/day |
| Bing News Search API | News-specific search | 1,000 free/month |
| Crunchbase API | Funding events | Best for funding data specifically |
| Apollo | Company signals | Built-in signal feeds, less news depth |
| Meltwater / Mention | Media monitoring | Enterprise-grade, expensive |

## Error Handling

- **Claygent returns empty array**: Company is too small or private for news coverage. Fall back to LinkedIn company page posts and job postings as proxy signals.
- **Google API rate limit**: Spread queries across the day or use Bing as overflow. Cache results for 7 days since news does not change that fast.
- **Stale results**: Always include the search date in stored data. Treat news older than 90 days as expired.
- **False matches**: Company names like "Apple" or "Meta" pollute results. Add industry or domain qualifiers to search queries: `"{Company Name}" {industry} funding OR launch OR hire`.
