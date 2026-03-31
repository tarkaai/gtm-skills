---
name: reddit-ads-subreddit-targeting
description: Research, score, and build subreddit-based ad targeting clusters for Reddit Ads campaigns
category: Paid
tools:
  - Reddit API
  - Reddit Ads API
  - Clay
fundamentals:
  - subreddit-research
  - reddit-ads-audience-targeting
  - reddit-api-read
  - clay-scoring
---

# Reddit Ads Subreddit Targeting

This drill builds optimized subreddit targeting for Reddit Ads campaigns. It combines organic subreddit research with paid advertising audience sizing to find the communities where your ICP is most active and ads are most cost-effective.

## Input

- ICP definition: target persona, industry, pain points
- Product category and problem domain keywords
- Budget constraint (determines how many subreddits to target)

## Steps

### 1. Discover candidate subreddits

Using the `subreddit-research` fundamental, generate a list of 15-20 candidate subreddits. Search by:

- Product category keywords (e.g., "devops tools", "sales automation")
- ICP job titles (e.g., "startup founders", "engineering managers")
- Problem-domain terms (e.g., "deployment failures", "customer churn")
- Competitor names (e.g., "hubspot alternative", "salesforce")
- Industry terms (e.g., "fintech", "SaaS")

### 2. Score each subreddit for ad potential

Using the `reddit-api-read` fundamental, pull data for each candidate:

```
GET https://oauth.reddit.com/r/{subreddit}/about
GET https://oauth.reddit.com/r/{subreddit}/hot?limit=25
```

Score on 5 dimensions (1-5 each):

| Dimension | What to check | 1 (Skip) | 5 (Target) |
|---|---|---|---|
| ICP density | Do posts discuss problems your product solves? | Tangential | Core ICP problems daily |
| Subscriber count | How large is the audience? | <5k (too small for ads) | 50k-500k (ideal for ads) |
| Engagement quality | Are comments substantive? | Memes and one-liners | Detailed technical discussions |
| Commercial tolerance | How do users react to company content? | Hostile to anything commercial | Accept useful tools and resources |
| Competition | Are competitors advertising here? | Saturated with ads | Few or no competitor ads |

Calculate composite score: `ICP_density * 3 + subscribers * 2 + engagement * 2 + tolerance * 2 + competition * 1`

Subreddits scoring 35+ out of 50: high priority. 25-35: test candidate. Below 25: skip for paid.

### 3. Check ad eligibility

Not all subreddits accept ads. Using the `reddit-ads-audience-targeting` fundamental, check each subreddit's estimated reach:

```
GET https://ads-api.reddit.com/api/v3/accounts/{account_id}/audience_estimate
{
  "target": {"subreddits": ["{subreddit_name}"], "geos": [{"country": "US"}]}
}
```

If a subreddit returns zero or very low estimated reach, it may not be in Reddit's ad inventory. Remove it from your list.

### 4. Build targeting clusters

Group the top-scoring, ad-eligible subreddits into 2-3 clusters based on theme:

**Cluster structure:**
- Each cluster: 3-5 subreddits with a shared theme
- Include 1 large subreddit (100k+ subscribers) per cluster for reach
- Include 2-3 niche subreddits (10k-100k) per cluster for precision
- Keep subreddits within a cluster related to each other (users likely overlap)

**Example for a DevOps tool:**

| Cluster | Subreddits | Est. Daily Reach | Theme |
|---|---|---|---|
| Core DevOps | r/devops, r/kubernetes, r/docker | 250,000 | Technical practitioners |
| SRE/Platform | r/sysadmin, r/aws, r/terraform | 400,000 | Infrastructure operators |
| Startup Tech | r/startups, r/SaaS, r/webdev | 300,000 | Startup builders |

### 5. Set cluster-level budget allocation

Allocate budget across clusters based on ICP density score:

- Highest ICP density cluster: 50% of budget
- Second cluster: 30% of budget
- Third cluster (experimental): 20% of budget

Within each cluster, budget is distributed evenly across subreddits by the ad platform.

### 6. Validate with sample content analysis

For each cluster, pull the top 10 posts from the past week using `reddit-api-read`:

```
GET https://oauth.reddit.com/r/{subreddit}/top?t=week&limit=10
```

Check: Are the top posts relevant to your offering? Would your ad feel native alongside these posts? If the top posts are memes and your ad is a technical resource, reconsider the cluster.

If using Clay, run `clay-scoring` on the post authors to confirm they match your ICP firmographics.

### 7. Document and handoff

Produce a targeting document:

```json
{
  "clusters": [
    {
      "name": "Core DevOps",
      "subreddits": ["devops", "kubernetes", "docker"],
      "estimated_reach": 250000,
      "icp_density_score": 4.5,
      "budget_allocation": 0.50,
      "creative_tone": "technical, peer-to-peer",
      "best_content_types": ["data-driven findings", "tool comparisons", "post-mortems"]
    }
  ]
}
```

This document feeds directly into the `reddit-ads-campaign-build` drill for ad group creation.

## Output

- 2-3 subreddit targeting clusters with 3-5 subreddits each
- Scoring matrix for all evaluated subreddits
- Estimated reach per cluster
- Budget allocation recommendation
- Creative tone guidance per cluster
- Targeting document for campaign build handoff

## Triggers

- Run once at Smoke level (initial subreddit selection)
- Re-run monthly at Baseline+ levels (new subreddits emerge, old ones change)
- Re-run when ad group performance declines (subreddit fatigue)
