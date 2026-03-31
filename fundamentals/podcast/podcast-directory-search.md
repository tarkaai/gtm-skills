---
name: podcast-directory-search
description: Search podcast directories to find shows matching topic, audience size, and guest format criteria
tool: ListenNotes
difficulty: Setup
---

# Podcast Directory Search

Search podcast databases to find shows that match your founder's expertise, target audience overlap, and guest booking format.

## Tool Options

| Tool | API | Best For |
|------|-----|----------|
| ListenNotes | REST API (`api.listennotes.com/api/v2`) | Largest index (3M+ podcasts), keyword + genre search, audience size estimates |
| Podchaser | GraphQL API (`api.podchaser.com/graphql`) | Rich creator data, guest cross-references, contact info |
| Rephonic | REST API (`api.rephonic.com/v2`) | Audience overlap analysis, similar-show recommendations, listener demographics |
| Spotify for Podcasters | Web dashboard (no public API) | Show-level analytics if you have your own show |
| Apple Podcasts | RSS + iTunes Search API | Chart rankings, category browsing |

## ListenNotes API (Primary)

### Authentication
```
GET https://api.listennotes.com/api/v2/search
Header: X-ListenAPI-Key: {LISTENNOTES_API_KEY}
```

Free tier: 5 requests/min. Paid: starts at $9/mo for 300 requests/day.

### Search for podcasts by topic

```http
GET https://api.listennotes.com/api/v2/search?q={keyword}&type=podcast&language=English&len_min=15&len_max=90&genre_ids={genre_id}&sort_by_date=0
```

Parameters:
- `q`: Topic keyword (e.g., "B2B SaaS", "developer tools", "startup growth")
- `type`: `podcast` (find shows) or `episode` (find episodes where guests appeared)
- `genre_ids`: Comma-separated. 93=Business, 127=Technology, 67=Entrepreneurship, 94=Business News, 171=Management
- `sort_by_date`: 0 = relevance, 1 = date
- `offset`: Pagination (10 results per page)

### Response fields to extract
```json
{
  "results": [
    {
      "id": "podcast_id",
      "title_original": "Show Name",
      "description_original": "Show description",
      "total_episodes": 150,
      "listen_score": 45,
      "listen_score_global_rank": "top 5%",
      "website": "https://show-website.com",
      "email": "host@show.com",
      "rss": "https://feed-url.com/rss",
      "genre_ids": [93, 127]
    }
  ]
}
```

Key field: `listen_score` (0-100). For micro-podcasts (Smoke test targets), look for scores 20-50. For Scalable, target 40-70.

### Get podcast details

```http
GET https://api.listennotes.com/api/v2/podcasts/{podcast_id}
```

Returns: episode count, average episode length, last publish date (stale shows = skip), and RSS feed URL.

### Search for episodes with guest appearances

```http
GET https://api.listennotes.com/api/v2/search?q={competitor_founder_name}&type=episode
```

Use this to find which podcasts have hosted founders similar to yours. These are warm targets — the host already books founder guests.

## Podchaser API (Contact + Guest Data)

### Authentication
```
POST https://api.podchaser.com/graphql
Header: Authorization: Bearer {PODCHASER_TOKEN}
```

### Find podcast by name
```graphql
query {
  podcasts(searchTerm: "show name", first: 5) {
    data {
      id
      title
      description
      webUrl
      ratingAverage
      ratingCount
      episodes(first: 1) { data { id title } }
    }
  }
}
```

### Get creator contacts
```graphql
query {
  podcast(identifier: { id: "podcast_id", type: PODCHASER }) {
    creators {
      data {
        name
        socialLinks { url platform }
      }
    }
  }
}
```

## Rephonic API (Audience Overlap)

### Find similar podcasts
```http
GET https://api.rephonic.com/v2/podcasts/{podcast_id}/similar
Header: Authorization: Bearer {REPHONIC_TOKEN}
```

Returns podcasts with overlapping audiences. Use this to expand your target list once you find one good-fit show.

### Get listener demographics
```http
GET https://api.rephonic.com/v2/podcasts/{podcast_id}/demographics
```

Returns: listener age, gender, interests, geographic distribution. Match against your ICP.

## Qualifying a Podcast

For each podcast found, evaluate:

1. **Active**: Last episode published within 30 days (skip dormant shows)
2. **Guest format**: Check recent episodes for guest interviews (vs solo/co-host only)
3. **Audience match**: Topic overlap with your founder's expertise
4. **Reach**: ListenNotes `listen_score` or estimated downloads per episode
5. **Accessibility**: Contact info available (email, Twitter DM, website contact form)

Store qualified podcasts in a Clay table or Attio list with fields: show name, host name, contact method, listen score, topic fit score (1-5), last guest episode date, pitch status.

## Error Handling

- **Rate limited (429)**: Back off and retry after the `Retry-After` header duration
- **No results**: Broaden search terms. Try adjacent topics or search for competitor founder names as episode guests
- **Stale data**: Cross-reference ListenNotes data with the podcast's RSS feed for latest episode dates
