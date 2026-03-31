---
name: reddit-api-write
description: Submit posts and comments to Reddit via the Reddit API (OAuth2)
tool: Reddit API
difficulty: Config
---

# Reddit API — Write Operations

Use the Reddit API to submit posts and comments on Reddit. All write operations require OAuth2 authentication with a `script` or `web` app, and the account must have sufficient karma and age for the target subreddit.

## Prerequisites

- Completed `reddit-api-read` fundamental (OAuth2 app created, token obtained)
- Reddit account with positive karma history in target subreddits
- Understanding of each subreddit's posting rules (many subreddits have minimum karma/age requirements)

## Submit a Text Post

```
POST https://oauth.reddit.com/api/submit
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer TOKEN

kind=self&sr=SUBREDDIT&title=POST_TITLE&text=POST_BODY&sendreplies=true
```

Parameters:
- `kind`: `self` (text post) or `link` (link post)
- `sr`: Subreddit name (without r/ prefix)
- `title`: Post title (max 300 characters)
- `text`: Post body in Markdown format
- `url`: For link posts, the URL to submit
- `flair_id`: Optional flair ID (get available flairs via `GET /r/SUBREDDIT/api/link_flair_v2`)
- `sendreplies`: `true` to receive reply notifications

Response: `{"json": {"data": {"name": "t3_POST_ID", "url": "https://reddit.com/r/..."}}}`

## Submit a Comment

```
POST https://oauth.reddit.com/api/comment
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer TOKEN

thing_id=t3_POST_ID&text=COMMENT_TEXT
```

Parameters:
- `thing_id`: The fullname of the post (`t3_ID`) or parent comment (`t1_ID`) to reply to
- `text`: Comment body in Markdown format

Response: `{"json": {"data": {"things": [{"data": {"id": "COMMENT_ID", ...}}]}}}`

## Add UTM Parameters to Links

When including links in posts or comments, always append UTM parameters for tracking:

```
https://yoursite.com/resource?utm_source=reddit&utm_medium=community&utm_campaign=reddit-niche-communities&utm_content=r_SUBREDDIT_NAME
```

This enables PostHog to attribute referral traffic to specific subreddits and posts.

## Important Constraints

1. **Rate limits**: Reddit enforces posting rate limits per account. New accounts may be limited to 1 post per 10 minutes. Established accounts get higher limits.
2. **Subreddit rules**: Many subreddits auto-remove posts from accounts younger than X days or with karma below Y. Check `GET /r/SUBREDDIT/about/rules` and review the sidebar.
3. **Self-promotion rules**: Reddit's site-wide guideline is the "10% rule" — no more than 10% of your submissions should be self-promotional. Most subreddits enforce stricter limits.
4. **Shadowbans**: If your posts consistently get removed or receive zero engagement, your account may be shadowbanned. Check at https://www.reddit.com/api/v1/me to verify your account status.
5. **Markdown formatting**: Reddit uses its own Markdown flavor. Line breaks require two newlines. Links are `[text](url)`. Code blocks use triple backticks or 4-space indentation.

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

# Submit a text post
subreddit = reddit.subreddit("SUBREDDIT")
submission = subreddit.submit(
    title="How we solved X problem",
    selftext="Here is our approach to solving X...\n\n[Full writeup](https://yoursite.com/blog/x?utm_source=reddit&utm_medium=community)"
)

# Submit a comment on a post
submission = reddit.submission(id="POST_ID")
comment = submission.reply("Great question! Here is what worked for us...")

# Reply to a comment
comment = reddit.comment(id="COMMENT_ID")
reply = comment.reply("Adding to this point...")
```

## Error Handling

- **RATELIMIT**: Response includes `ratelimit` field with seconds to wait. Back off accordingly.
- **403 Forbidden**: Account lacks posting permissions in this subreddit. Build karma first.
- **400 Bad Request**: Invalid parameters. Check subreddit allows your post type (some are link-only or text-only).
- **SUBREDDIT_NOTALLOWED**: Your account doesn't meet the subreddit's age/karma requirements.

## Anti-Spam Best Practices

- Space out posts: maximum 2-3 posts per day across all subreddits
- Vary your content — don't post the same text across multiple subreddits
- Engage in comments on other people's posts before posting your own content
- Build genuine karma by being helpful in discussions unrelated to your product
- Never use multiple accounts to upvote your own posts
