---
name: media-database-search
description: Search journalist, newsletter, and publication databases to find media targets matching topic and audience criteria
tool: Muck Rack / Prowly / JustReachOut / Anewstip / Hunter Journalists
difficulty: Setup
---

# Media Database Search

Search media databases to find journalists, newsletter editors, and publication contacts that cover topics relevant to your company. These contacts become pitch targets for earned media placements.

## Tool Options

| Tool | API/Method | Best For |
|------|-----------|----------|
| Muck Rack | Web app + API (`api.muckrack.com`) | Largest journalist database, beat tracking, article history |
| Prowly | REST API (`api.prowly.com/v1`) | EU-strong, media lists, journalist contact info |
| JustReachOut | Web app (no public API) | AI-powered journalist matching, pitch scoring |
| Anewstip | REST API (`api.anewstip.com`) | Real-time journalist social media monitoring, topic matching |
| Hunter Journalists | REST API (`api.hunter.io`) | Email finding for journalists discovered via other tools |
| BuzzSumo | REST API (`api.buzzsumo.com/api`) | Find journalists by articles they've written on a topic |

## Muck Rack (Primary for journalist search)

### Search journalists by beat

```http
GET https://api.muckrack.com/journalists?q={topic}&beat={beat_name}&outlet_type={type}
Header: Authorization: Bearer {MUCKRACK_API_KEY}
```

Parameters:
- `q`: Topic keyword (e.g., "AI startups", "B2B SaaS", "developer tools")
- `beat`: Beat/vertical filter (e.g., "technology", "business", "startups")
- `outlet_type`: `newspaper`, `magazine`, `online`, `newsletter`, `podcast`
- `location`: Geographic filter (e.g., "US", "UK")

### Response fields to extract
```json
{
  "journalists": [
    {
      "name": "Jane Reporter",
      "email": "jane@outlet.com",
      "outlet": "TechCrunch",
      "beat": "Startups",
      "recent_articles": [...],
      "twitter_handle": "@janereporter",
      "linkedin_url": "https://linkedin.com/in/janereporter",
      "pitchability_score": 72
    }
  ]
}
```

## BuzzSumo (Find journalists by recent writing)

### Search articles by topic

```http
GET https://api.buzzsumo.com/api/search/articles.json?q={topic}&num_days=30&num_results=50
Header: x-api-key: {BUZZSUMO_API_KEY}
```

Extract the author names and outlets from top-performing articles. These journalists are actively writing about your topic — they are warm targets.

### Find journalist contact from article

```http
GET https://api.buzzsumo.com/api/search/authors.json?q={author_name}
```

Returns social profiles and associated outlets.

## Newsletter Discovery (Manual + API hybrid)

For micro-newsletter targets, use these approaches:

1. **Substack search**: `https://substack.com/search/{topic}` — browse results, check subscriber counts and posting frequency
2. **Beehiiv directory**: `https://www.beehiiv.com/discover` — search by category
3. **SparkLoop partner network**: Search for newsletters in your niche that accept cross-promotions
4. **Letterhead**: Newsletter directory with journalist contact info
5. **Clay enrichment**: Once you have a newsletter URL, use Clay's "Enrich Company" to find the editor's email

### Qualifying a newsletter
- **Active**: Published within last 14 days
- **Relevant**: Covers topics adjacent to your product/expertise
- **Reachable**: Editor email or contact form available
- **Audience match**: Subscriber base overlaps your ICP (check the "About" page for demographic info)
- **Accepts pitches**: Look for "write for us", "guest posts", "sponsored content", or "tips" pages

## Anewstip (Real-time journalist monitoring)

### Search journalists tweeting about your topic

```http
GET https://api.anewstip.com/v1/search/journalists?q={topic}&days=7
Header: x-api-key: {ANEWSTIP_API_KEY}
```

Returns journalists who have tweeted about your topic in the last N days. These are actively thinking about the topic — highest-intent pitch targets.

## Qualifying a Media Target

For each journalist, newsletter, or publication found, evaluate:

1. **Recency**: Have they written about your topic in the last 30 days?
2. **Relevance**: Does their beat/coverage area match your story angle?
3. **Reach**: Estimated audience size (outlet traffic, newsletter subscribers, social following)
4. **Accessibility**: Is contact info available (email preferred, Twitter DM, LinkedIn)?
5. **Pitch history**: Have they responded to pitches before (check Muck Rack response rate)?

Score each target 1-5 and store in Clay or Attio with fields: name, outlet, beat, contact method, email, relevance score, reach score, pitch status.

## Error Handling

- **Rate limited (429)**: Back off per `Retry-After` header. Muck Rack: 60 req/min. BuzzSumo: 10 req/min.
- **No results**: Broaden topic keywords. Try adjacent verticals or search for competitor company names in articles.
- **Stale contacts**: Cross-reference journalist's current outlet via LinkedIn before pitching. Journalists change outlets frequently.
- **No email found**: Fall back to Hunter.io journalist search or Twitter DM.

## Pricing

| Tool | Free Tier | Paid |
|------|-----------|------|
| Muck Rack | No free tier | Custom pricing (~$500+/mo) |
| Prowly | 7-day trial | From $369/mo (https://prowly.com/pricing) |
| JustReachOut | No free tier | From $147/mo (https://justreachout.io/pricing) |
| Anewstip | 14-day trial | From $150/mo |
| BuzzSumo | 30-day trial | From $199/mo (https://buzzsumo.com/pricing) |
| Hunter.io | 25 searches/mo free | From $49/mo (https://hunter.io/pricing) |
