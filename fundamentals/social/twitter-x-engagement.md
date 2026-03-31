---
name: twitter-x-engagement
description: Engage with target prospects on Twitter/X through likes, replies, retweets, and quote posts
tool: X
product: X Organic
difficulty: Setup
---

# Twitter/X Engagement

Build visibility and warm up prospects on X before sending DMs. Engagement creates familiarity so your DM does not arrive cold.

## Option A: X API v2 (Direct)

### Like a Post

```
POST https://api.x.com/2/users/{user_id}/likes
Authorization: Bearer {USER_ACCESS_TOKEN}

{
  "tweet_id": "{POST_ID}"
}
```

Rate limit: 1,000 likes per 24 hours.

### Reply to a Post

```
POST https://api.x.com/2/tweets
Authorization: Bearer {USER_ACCESS_TOKEN}

{
  "text": "Your reply text",
  "reply": {
    "in_reply_to_tweet_id": "{POST_ID}"
  }
}
```

Rate limit: 100 posts per 24 hours (includes original posts and replies).

### Retweet a Post

```
POST https://api.x.com/2/users/{user_id}/retweets
Authorization: Bearer {USER_ACCESS_TOKEN}

{
  "tweet_id": "{POST_ID}"
}
```

### Quote Post

```
POST https://api.x.com/2/tweets
Authorization: Bearer {USER_ACCESS_TOKEN}

{
  "text": "Your commentary here",
  "quote_tweet_id": "{POST_ID}"
}
```

### Search for Prospect Posts

```
GET https://api.x.com/2/tweets/search/recent?query=from:{username}&max_results=10&tweet.fields=created_at,public_metrics
```

Returns recent posts from a specific user. Use this to find posts to engage with before sending a DM.

## Option B: PhantomBuster Automations

### Twitter Auto Liker

Automatically like posts from a list of X profiles. Set up via PhantomBuster:

1. Select the Twitter Liker Phantom.
2. Provide a spreadsheet of X profile URLs.
3. Configure: like the 2-3 most recent posts per profile.
4. Rate: 10 profiles per launch, 5 launches per day.

### Twitter Auto Replier

PhantomBuster does not offer a direct auto-reply Phantom for X. For automated replies, use the X API v2 reply endpoint via n8n.

## Option C: Typefully / Hypefury

Content scheduling tools that support engagement workflows:
- Queue replies to specific posts.
- Schedule engagement sessions.
- Track which accounts you have engaged with.

## Engagement-Before-DM Workflow

For cold DM plays, run this sequence over 3-5 days before sending a DM:

1. **Day 1**: Like 2-3 of the prospect's recent posts.
2. **Day 2**: Reply to one post with a substantive comment (add a data point, share a related experience, or ask a follow-up question). Keep it under 280 characters. Do NOT mention your product.
3. **Day 3-4**: Like 1-2 more posts. Retweet one if it is genuinely relevant to your audience.
4. **Day 5**: Send the DM. Reference their content: "Your post on [topic] caught my eye -- [specific observation]. Quick question: [one sentence about their problem]."

This sequence makes your handle familiar in their notifications before the DM arrives.

## Rate Limits Summary

| Action | Limit | Window |
|--------|-------|--------|
| Like | 1,000 | 24 hours |
| Post/Reply | 100 | 24 hours |
| Retweet | 1,000 | 24 hours |
| Search | 450 | 15 minutes (Basic) |

## Error Handling

- **403 Forbidden**: Cannot engage with a protected account or blocked user. Skip.
- **429 Too Many Requests**: Rate limit exceeded. Read `x-rate-limit-reset` header and wait.
- **409 Conflict**: Already liked/retweeted this post. Silently skip.
- **404 Not Found**: Post has been deleted or account suspended. Remove from queue.
