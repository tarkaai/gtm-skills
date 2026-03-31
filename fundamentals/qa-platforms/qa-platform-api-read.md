---
name: qa-platform-api-read
description: Read questions, answers, tags, and user profiles from Q&A platforms (Stack Overflow, Quora, Dev.to)
tool: Stack Exchange
product: API
difficulty: Setup
---

# Q&A Platform API -- Read Operations

Read questions, answers, tags, and user profiles from Q&A platforms. Stack Overflow has a public API. Quora has no official API (use web scraping or third-party services). Dev.to has a public API.

## Stack Exchange API (Stack Overflow, Server Fault, Super User, etc.)

Base URL: `https://api.stackexchange.com/2.3`

### Authentication

Register an app at https://stackapps.com/apps/oauth/register to get an API key. An API key is not required but raises your rate limit from 300 to 10,000 requests/day.

```
# Append to all requests:
?key=YOUR_API_KEY&site=stackoverflow
```

The `site` parameter selects the Stack Exchange site: `stackoverflow`, `serverfault`, `superuser`, `askubuntu`, etc.

### Search for questions by keywords

```bash
curl "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=creation&q=KEYWORDS&tagged=TAG1;TAG2&accepted=false&answers=0&site=stackoverflow&key=YOUR_API_KEY&filter=withbody&pagesize=50"
```

Key parameters:
- `q`: Free-text search query
- `tagged`: Semicolon-separated tags to filter by (e.g., `python;api`)
- `accepted=false`: Only questions without an accepted answer (high opportunity)
- `answers=0` or `answers=1`: Questions with few answers (less competition)
- `sort`: `creation` (newest), `votes`, `activity`, `relevance`
- `filter=withbody`: Include question body text in response (costs more quota)
- `pagesize`: Max 100

### Get questions by tag

```bash
curl "https://api.stackexchange.com/2.3/questions?order=desc&sort=creation&tagged=TAG&site=stackoverflow&key=YOUR_API_KEY&pagesize=50"
```

### Get a specific question with answers

```bash
curl "https://api.stackexchange.com/2.3/questions/QUESTION_ID?order=desc&sort=votes&site=stackoverflow&key=YOUR_API_KEY&filter=withbody"

# Get answers for a question
curl "https://api.stackexchange.com/2.3/questions/QUESTION_ID/answers?order=desc&sort=votes&site=stackoverflow&key=YOUR_API_KEY&filter=withbody"
```

### Get unanswered questions by tag

```bash
curl "https://api.stackexchange.com/2.3/questions/unanswered?order=desc&sort=creation&tagged=TAG&site=stackoverflow&key=YOUR_API_KEY&pagesize=50"
```

### Get tag info and related tags

```bash
# Tag details
curl "https://api.stackexchange.com/2.3/tags/TAG/info?site=stackoverflow&key=YOUR_API_KEY"

# Related tags (find adjacent topics)
curl "https://api.stackexchange.com/2.3/tags/TAG/related?site=stackoverflow&key=YOUR_API_KEY"

# Tag synonyms
curl "https://api.stackexchange.com/2.3/tags/TAG/synonyms?site=stackoverflow&key=YOUR_API_KEY"
```

### Get user profile and stats

```bash
curl "https://api.stackexchange.com/2.3/users/USER_ID?site=stackoverflow&key=YOUR_API_KEY"

# User's top answers
curl "https://api.stackexchange.com/2.3/users/USER_ID/answers?order=desc&sort=votes&site=stackoverflow&key=YOUR_API_KEY&pagesize=20"
```

### Response format

All responses are JSON wrapped in a common envelope:

```json
{
  "items": [
    {
      "question_id": 12345,
      "title": "How to parse JSON in Python?",
      "body": "<p>HTML body of the question...</p>",
      "tags": ["python", "json", "parsing"],
      "score": 42,
      "answer_count": 3,
      "view_count": 15000,
      "is_answered": true,
      "accepted_answer_id": 12346,
      "creation_date": 1711843200,
      "owner": {"user_id": 999, "display_name": "username", "reputation": 5000}
    }
  ],
  "has_more": true,
  "quota_max": 10000,
  "quota_remaining": 9950
}
```

### Rate limits

- Without API key: 300 requests/day per IP
- With API key: 10,000 requests/day
- With access token: 10,000 requests/day
- Responses are compressed (gzip). Always send `Accept-Encoding: gzip`.

## Dev.to API

Base URL: `https://dev.to/api`

### Authentication

Generate an API key at https://dev.to/settings/extensions. Include in requests:

```
api-key: YOUR_DEV_TO_API_KEY
```

### Search articles (questions tagged with #discuss or #help)

```bash
curl "https://dev.to/api/articles?tag=discuss&top=7&per_page=30" \
  -H "api-key: YOUR_DEV_TO_API_KEY"

# Search by keyword
curl "https://dev.to/api/articles?tag=help&per_page=30" \
  -H "api-key: YOUR_DEV_TO_API_KEY"
```

### Get article comments

```bash
curl "https://dev.to/api/comments?a_id=ARTICLE_ID" \
  -H "api-key: YOUR_DEV_TO_API_KEY"
```

## Quora (No Official API)

Quora does not provide a public API. Options for programmatic access:

1. **Web scraping with Playwright/Puppeteer**: Navigate to `https://www.quora.com/search?q=KEYWORDS`, parse question titles, URLs, answer counts, and follower counts from the DOM. Respect robots.txt and rate-limit to 1 request per 5 seconds.

2. **Quora Spaces RSS**: Some Quora Spaces publish RSS feeds at `https://www.quora.com/q/SPACE_NAME/rss`. Monitor these with n8n's RSS node.

3. **Third-party services**: Services like Serper.dev or SerpAPI can search Quora programmatically by running `site:quora.com KEYWORDS` queries and returning structured results.

4. **Google Custom Search API**: Configure a custom search engine restricted to `quora.com` and query it via the Google CSE API.

```bash
# Using SerpAPI to search Quora
curl "https://serpapi.com/search.json?engine=google&q=site:quora.com+YOUR+KEYWORDS&api_key=YOUR_SERPAPI_KEY&num=20"
```

## Error Handling

- **400 Bad Request**: Invalid parameters. Check tag names and site parameter.
- **401 Unauthorized**: Invalid or expired access token. Re-authenticate.
- **402 Payment Required**: Quota exceeded. Wait until daily reset (midnight UTC).
- **429 Too Many Requests**: Backoff. Check `backoff` field in response -- wait that many seconds.
- **502/503**: Service temporarily unavailable. Retry with exponential backoff.
- **Throttle field**: Stack Exchange responses include `backoff` (seconds to wait) when you are being throttled.
