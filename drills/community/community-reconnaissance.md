---
name: community-reconnaissance
description: Discover, evaluate, and rank online communities where your ICP is active, then build engagement profiles for each
category: Community
tools:
  - Reddit API
  - Web Search
  - Attio
fundamentals:
  - subreddit-research
  - reddit-api-read
  - attio-lists
---

# Community Reconnaissance

This drill maps the online communities where your ICP participates, evaluates them for engagement potential, and produces a ranked target list with engagement profiles. It runs once at the start of the play and is refreshed quarterly.

## Input

- ICP definition (firmographics, job titles, pain points, triggering events) from the `icp-definition` drill
- Your product category and the problems you solve
- Competitor names

## Steps

### 1. Generate keyword lists for discovery

From your ICP definition, produce three keyword lists:

**Pain-point keywords** — the problems your ICP talks about:
- Extract the top 3 pain points from your ICP doc
- For each, generate 3-5 natural-language phrases people use when describing that pain (e.g., "how do I track churn" not "churn analytics platform")
- Include frustrated/venting variants: "tired of X", "struggling with X", "is there a better way to X"

**Category keywords** — what your product category is called:
- Your product category name and synonyms
- "best [category] tool", "[category] software recommendations", "[category] for [ICP role]"
- Comparison queries: "[competitor] vs", "[competitor] alternative"

**ICP role keywords** — where your ICP identifies themselves:
- Job titles: "startup founder", "VP of engineering", "head of growth"
- Industry terms: "B2B SaaS", "fintech startup", "devtools"

### 2. Discover candidate communities

Using the `subreddit-research` fundamental, run searches across all three keyword lists. For each search:
- Call the Reddit subreddit search endpoint with each keyword phrase
- Collect all unique subreddits returned
- Also search `site:reddit.com "[keyword]"` via web search to find threads in subreddits the API search might miss
- Note which subreddits appear repeatedly across multiple keyword searches (high signal)

Target: 20-40 candidate subreddits before filtering.

### 3. Evaluate each candidate

For each candidate subreddit, using the `reddit-api-read` fundamental:

1. **Get subreddit info**: `GET /r/SUBREDDIT/about` — extract subscriber count, active users, description, submission type
2. **Sample recent posts**: `GET /r/SUBREDDIT/hot?limit=25` — calculate average score, average comments, post frequency
3. **Check relevance**: Read the 25 most recent posts. Count how many are directly relevant to your expertise. Calculate relevance ratio.
4. **Check rules**: `GET /r/SUBREDDIT/about/rules` — note any restrictions on links, self-promotion, account age, or karma minimums
5. **Assess competition**: Count how many of the recent posts/comments are from obvious vendors or marketers vs. genuine community members

Score each subreddit using the scoring formula from the `subreddit-research` fundamental (ICP fit, activity, engagement, accessibility, competition).

### 4. Rank and select

Sort by total score. Select:
- **Top tier (3-5 subreddits, score 35+)**: Primary communities for daily engagement
- **Second tier (5-8 subreddits, score 25-34)**: Weekly engagement, test for promotion to top tier
- **Watch list (remaining)**: Monitor only, engage when high-opportunity threads appear

### 5. Build engagement profiles

For each selected subreddit, produce an engagement profile:

```markdown
## r/SUBREDDIT Engagement Profile

- **Subscribers**: X | **Active**: Y | **Posts/day**: Z
- **Score**: XX/50
- **Posting rules**: [summarize key rules]
- **Minimum requirements**: [karma, account age, flair]
- **Best content types**: [what gets upvoted here — how-tos, stories, questions, data]
- **Peak activity hours (UTC)**: [when posts get the most engagement]
- **Key recurring topics**: [pricing, hiring, churn, tooling, etc.]
- **Top contributors**: [note 3-5 regular contributors who set the tone]
- **Competitor presence**: [none / low / moderate / saturated]
- **Your angle**: [specific expertise you can offer here that isn't already covered]
- **First engagement plan**: [what your first 5 interactions should look like]
```

### 6. Store in CRM

Using the `attio-lists` fundamental, create an Attio list called "Community Targets" with entries for each subreddit. Include the engagement profile data as structured fields. This enables tracking engagement metrics per community over time.

## Output

- Ranked list of 10-15 target subreddits with engagement profiles
- Attio list with community targets and metadata
- Three keyword lists (pain-point, category, ICP role) for use in monitoring

## Triggers

- Run once at play start
- Re-run quarterly or when ICP changes
- Ad-hoc when a new relevant community is discovered
