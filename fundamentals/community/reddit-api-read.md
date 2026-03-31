---
name: reddit-api-read
description: Read subreddit posts, comments, and search Reddit via the Reddit API (OAuth2)
tool: Reddit
product: Reddit API
difficulty: Setup
---

# Reddit API — Read Operations

Use the Reddit API to search subreddits, read posts, read comments, and discover relevant communities. All requests require OAuth2 authentication and go to `https://oauth.reddit.com`.

## Authentication

1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app..." at the bottom
3. Select "script" type for personal/server-side use
4. Set redirect URI to `http://localhost:8080` (unused for script apps)
5. Note your **Client ID** (under the app name) and **Client Secret**

Get an access token:

```bash
curl -X POST https://www.reddit.com/api/v1/access_token \
  -u "CLIENT_ID:CLIENT_SECRET" \
  -d "grant_type=password&username=REDDIT_USERNAME&password=REDDIT_PASSWORD" \
  -A "YourApp/1.0 by YourRedditUsername"
```

Response: `{"access_token": "TOKEN", "token_type": "bearer", "expires_in": 86400, ...}`

All subsequent requests use: `Authorization: Bearer TOKEN` and go to `https://oauth.reddit.com`.

## Rate Limits

- Free tier: 100 requests/minute with OAuth
- Always include a descriptive `User-Agent` header: `YourApp/1.0 by YourRedditUsername`
- Free tier is restricted to non-commercial use

## Key Read Endpoints

### Search for subreddits by topic

```
GET https://oauth.reddit.com/subreddits/search?q=QUERY&limit=25&sort=relevance
```

Returns subreddit objects with `display_name`, `subscribers`, `public_description`, `active_user_count`.

### Get subreddit info

```
GET https://oauth.reddit.com/r/SUBREDDIT/about
```

Returns subscriber count, rules, description, and whether the subreddit allows link/text posts.

### Get hot/new/top posts from a subreddit

```
GET https://oauth.reddit.com/r/SUBREDDIT/hot?limit=25
GET https://oauth.reddit.com/r/SUBREDDIT/new?limit=25
GET https://oauth.reddit.com/r/SUBREDDIT/top?t=week&limit=25
```

`t` parameter for /top: `hour`, `day`, `week`, `month`, `year`, `all`.

### Search posts within a subreddit

```
GET https://oauth.reddit.com/r/SUBREDDIT/search?q=QUERY&restrict_sr=true&sort=relevance&t=month&limit=25
```

`restrict_sr=true` limits search to the specified subreddit.

### Get comments on a post

```
GET https://oauth.reddit.com/r/SUBREDDIT/comments/POST_ID?limit=100&sort=top
```

Sort options: `confidence`, `top`, `new`, `controversial`, `old`, `qa`.

### Search all of Reddit

```
GET https://oauth.reddit.com/search?q=QUERY&type=link&sort=relevance&t=month&limit=25
```

`type`: `link` (posts), `sr` (subreddits), `user` (users).

## Response Format

All responses are JSON. Posts are in `data.children[]` with each child having `data.title`, `data.selftext`, `data.url`, `data.score`, `data.num_comments`, `data.author`, `data.created_utc`, `data.subreddit`.

## Error Handling

- **401 Unauthorized**: Token expired. Re-authenticate.
- **403 Forbidden**: Subreddit is private or you lack permissions.
- **429 Too Many Requests**: Rate limited. Back off and retry after `Retry-After` header seconds.
- **503 Service Unavailable**: Reddit is overloaded. Retry with exponential backoff.

## Python (PRAW) Alternative

```python
import praw

reddit = praw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    user_agent="YourApp/1.0 by YourRedditUsername",
    username="REDDIT_USERNAME",
    password="REDDIT_PASSWORD"
)

# Search subreddits
for sr in reddit.subreddits.search("saas marketing", limit=10):
    print(sr.display_name, sr.subscribers)

# Get hot posts
for post in reddit.subreddit("startups").hot(limit=10):
    print(post.title, post.score, post.num_comments)

# Search within a subreddit
for post in reddit.subreddit("SaaS").search("pricing strategy", time_filter="month"):
    print(post.title, post.url)
```

## n8n Alternative

Use the built-in Reddit node in n8n:
- **Get Post**: Retrieve a specific post by ID
- **Get All Posts**: Retrieve posts from a subreddit (hot, new, top, rising)
- **Search**: Search posts across Reddit or within a subreddit
- **Get Profile**: Get a user's profile information

Configure credentials in n8n with your Reddit OAuth2 app credentials.
