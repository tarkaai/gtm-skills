---
name: subreddit-research
description: Discover and evaluate subreddits where your ICP is active using Reddit API and web research
tool: Reddit API
difficulty: Setup
---

# Subreddit Research

Systematically discover, evaluate, and rank subreddits where your Ideal Customer Profile participates. The goal is to find communities where your expertise is relevant and engagement is feasible (not too large to get buried, not too small to matter).

## Step 1: Generate Candidate Subreddits

### Via Reddit API search

```
GET https://oauth.reddit.com/subreddits/search?q=QUERY&limit=25&sort=relevance
```

Run searches for:
- Your product category: `"saas marketing"`, `"developer tools"`, `"project management"`
- Your ICP's job title: `"startup founders"`, `"devops engineers"`, `"product managers"`
- Your ICP's industry: `"fintech"`, `"healthtech"`, `"ecommerce"`
- Problems you solve: `"sales automation"`, `"customer churn"`, `"data pipeline"`
- Competitor names: `"hubspot"`, `"salesforce"`, `"notion"`

### Via web search

Search `site:reddit.com "[your problem domain]"` to find threads, then note which subreddits they appear in.

### Via related subreddits

For each promising subreddit, check its sidebar (description and related subreddits):
```
GET https://oauth.reddit.com/r/SUBREDDIT/about
```
The `description` field often links to sister subreddits.

## Step 2: Evaluate Each Subreddit

For each candidate, collect these metrics:

```
GET https://oauth.reddit.com/r/SUBREDDIT/about
```

Extract from the response:
- `subscribers`: Total subscriber count
- `active_user_count`: Users currently online
- `public_description`: What the community is about
- `submission_type`: `any`, `link`, `self` (text-only)
- `over18`: NSFW flag

Then sample recent posts:
```
GET https://oauth.reddit.com/r/SUBREDDIT/hot?limit=25
```

Calculate:
- **Average post score** (upvotes): Are posts getting traction?
- **Average comments per post**: Is there active discussion?
- **Post frequency**: How many posts per day?
- **Relevance ratio**: What % of recent posts are relevant to your expertise?

## Step 3: Score and Rank

Score each subreddit on a 1-5 scale for:

| Factor | 1 (Poor) | 5 (Excellent) |
|--------|----------|---------------|
| **ICP fit** | Tangentially related | Directly your ICP |
| **Activity** | <1 post/day | 10+ posts/day with discussion |
| **Engagement** | Posts get 0-1 comments | Posts get 10+ comments |
| **Accessibility** | Strict rules, auto-moderation heavy | Open to helpful contributions |
| **Competition** | Saturated with vendors/marketers | Genuine community, few marketers |

**Sweet spot formula**: `ICP_fit * 3 + Activity * 2 + Engagement * 2 + Accessibility * 1.5 + Competition * 1.5`

Subreddits scoring 35+ out of 50 are high priority. 25-35 are worth testing. Below 25, skip.

## Step 4: Document Subreddit Profiles

For each selected subreddit, record:

```json
{
  "subreddit": "r/SaaS",
  "subscribers": 125000,
  "active_users": 450,
  "posts_per_day": 15,
  "avg_comments": 8,
  "icp_fit_score": 5,
  "total_score": 42,
  "posting_rules": "No direct self-promotion. Educational content OK. Flair required.",
  "min_karma": 10,
  "min_account_age_days": 30,
  "best_content_types": ["how-to", "case-study", "question"],
  "peak_activity_utc": "14:00-18:00",
  "key_topics": ["pricing", "growth", "churn", "product-market-fit"],
  "competitor_presence": "low"
}
```

## Step 5: Check Posting Requirements

Many subreddits have minimum karma, account age, or flair requirements. Read:

```
GET https://oauth.reddit.com/r/SUBREDDIT/about/rules
```

Also read the sidebar text (in `about.description`) for unstated rules that moderators enforce. Common rules:
- No self-promotion links
- Must use post flair
- Minimum comment karma in the subreddit before posting
- No affiliate or referral links
- Must include a question or discussion prompt

## Output

A ranked list of 5-15 subreddits with profiles, sorted by total score. This list feeds into the `community-reconnaissance` drill.
