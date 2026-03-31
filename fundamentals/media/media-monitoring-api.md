---
name: media-monitoring-api
description: Monitor media mentions, journalist requests, and PR opportunities via monitoring APIs and HARO-style platforms
tool: Mention
product: Monitoring
difficulty: Config
---

# Media Monitoring API

Set up automated monitoring for brand mentions, competitor coverage, journalist requests for expert sources, and trending topics in your industry. This enables reactive PR (responding to opportunities) and brand tracking (measuring earned coverage).

## Tool Options

| Tool | API/Method | Best For |
|------|-----------|----------|
| Mention | REST API (`api.mention.net/v1`) | Real-time brand and keyword monitoring across web + social |
| Google Alerts | Email-based (no API) | Free, simple brand/keyword alerts |
| Qwoted | Email alerts + web dashboard | Journalist requests for expert sources (HARO alternative) |
| Featured.com | Web platform + email alerts | Expert quote placements in articles |
| Connectively (fka HARO) | Email alerts | Journalist source requests (largest volume) |
| Meltwater | REST API | Enterprise media monitoring + analytics |
| Cision | REST API | Enterprise PR distribution + monitoring |

## Mention API (Primary for brand/keyword monitoring)

### Authentication
```
GET https://api.mention.net/v1/accounts/{account_id}/alerts
Header: Authorization: Bearer {MENTION_API_KEY}
```

### Create a monitoring alert

```http
POST https://api.mention.net/v1/accounts/{account_id}/alerts
Content-Type: application/json

{
  "name": "Brand Mentions - {company_name}",
  "query": {
    "included_keywords": ["{company_name}", "{product_name}"],
    "excluded_keywords": ["{noise_terms}"],
    "sources": ["web", "blog", "forum", "news", "twitter"]
  },
  "languages": ["en"],
  "noise_detection": true
}
```

### Fetch recent mentions

```http
GET https://api.mention.net/v1/accounts/{account_id}/alerts/{alert_id}/mentions?since_id={last_id}&limit=50
```

Response fields:
```json
{
  "mentions": [
    {
      "id": "mention_id",
      "title": "Article title",
      "url": "https://outlet.com/article",
      "source": {"name": "TechCrunch", "type": "news"},
      "published_at": "2026-03-28T10:00:00Z",
      "sentiment": "positive",
      "reach": 50000,
      "snippet": "...excerpt mentioning your brand..."
    }
  ]
}
```

### Create competitor monitoring alerts

Create separate alerts for each competitor. Track when they get coverage and which outlets cover them — those outlets are pitch targets for you.

```http
POST https://api.mention.net/v1/accounts/{account_id}/alerts
{
  "name": "Competitor - {competitor_name}",
  "query": {
    "included_keywords": ["{competitor_name}"],
    "sources": ["web", "news", "blog"]
  }
}
```

## Google Alerts (Free fallback)

No API. Automate via n8n:

1. Create alerts at `https://www.google.com/alerts`:
   - Brand name alert: `"{company_name}"`
   - Competitor alert: `"{competitor_name}"`
   - Topic alert: `{your_topic} AND (report OR study OR research)` (finds data-driven articles you can piggyback on)
2. Set delivery to "As-it-happens" or "Once a day"
3. Set delivery to RSS feed (not email) for n8n ingestion
4. In n8n, use an RSS trigger node pointed at the Google Alerts RSS feed URL
5. Parse each alert item: title, URL, source, date
6. Route to Slack channel and log in Attio

## Qwoted (Journalist Source Requests)

### How it works
Journalists post requests for expert sources on Qwoted. You respond with a quote or insight. If selected, you get a placement (mention + backlink).

### Setup
1. Create account at `https://qwoted.com`
2. Complete your expert profile: name, title, company, expertise topics, bio, headshot
3. Set topic preferences: select 5-10 topics matching your expertise
4. Enable email notifications for matching requests

### Responding to a request
1. Read the journalist's query carefully. They specify: topic, angle, deadline, and what they need (quote, data, full response)
2. Draft a response: 2-3 sentences of direct expert insight. Include a specific stat, example, or contrarian take. Avoid generic advice.
3. Include your name, title, company, and a link to your website or relevant content.
4. Submit before the deadline. Earlier responses get more consideration.

### Automation with n8n
1. Forward Qwoted email alerts to a monitored inbox
2. n8n workflow: parse the email for topic, deadline, and journalist name
3. Use Claude API to draft a response matching the request
4. Route draft to Slack for human review and approval before submitting

## Featured.com (Expert Quote Placements)

### How it works
Featured.com collects expert answers on specific topics, then publishes roundup articles on high-DA sites. You get a backlink and mention.

### Setup
1. Create account at `https://featured.com`
2. Set expertise topics
3. Browse open questions or wait for email alerts
4. Submit 100-200 word expert answers
5. If selected, your quote appears in the published article with a backlink

### Qualifying which questions to answer
- **Topic match**: Only answer questions where you have genuine expertise
- **Publication quality**: Check where the article will be published (DA 30+ preferred)
- **Deadline**: Skip questions with < 24 hours remaining
- **Competition**: Fewer existing answers = higher selection probability

## Building an n8n Monitoring Pipeline

Combine all sources into a single monitoring workflow:

```
Triggers:
  - Mention API webhook (real-time brand mentions)
  - RSS feed poll (Google Alerts, every 1 hour)
  - Email parser (Qwoted alerts, Featured.com alerts)

Processing:
  - Deduplicate by URL
  - Classify: brand_mention | competitor_mention | journalist_request | topic_opportunity
  - Score relevance (1-5) based on source authority and topic match
  - Extract metadata: outlet, author, date, reach, sentiment

Routing:
  - brand_mention -> log in Attio, post to #pr-mentions Slack channel
  - competitor_mention -> log in Attio, flag if new outlet (pitch target)
  - journalist_request -> draft response via Claude, post to #pr-opportunities for review
  - topic_opportunity -> evaluate for reactive pitch, post to #pr-opportunities
```

## Error Handling

- **Mention API rate limit**: 2 requests/second. Use n8n's rate-limiting node.
- **Google Alerts RSS empty**: Alerts can break silently. Verify weekly that feeds still work.
- **Qwoted deadline missed**: Set Slack reminders 24 hours before deadline for high-priority requests.
- **Featured.com rejection**: Not all answers are selected. Track submission-to-publication rate. If below 20%, improve answer quality.

## Pricing

| Tool | Free Tier | Paid |
|------|-----------|------|
| Mention | 14-day trial | From $41/mo Solo (https://mention.com/en/pricing/) |
| Google Alerts | Free (unlimited) | N/A |
| Qwoted | Free (basic access) | Pro from $50/mo |
| Featured.com | Free (limited submissions) | Pro from $99/mo (https://featured.com/pricing) |
| Connectively (HARO) | Free (3 alerts/day) | From $49/mo |
| Meltwater | No free tier | Custom (~$500+/mo) |
