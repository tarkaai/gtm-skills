---
name: tla-post-selection
description: Identify and score organic LinkedIn posts for Thought Leader Ad promotion based on engagement signals and ICP relevance
category: Paid
tools:
  - LinkedIn
  - Taplio
  - Shield
  - Anthropic API
fundamentals:
  - linkedin-organic-analytics
  - linkedin-ads-thought-leader-setup
  - ai-content-ghostwriting
---

# TLA Post Selection

This drill identifies which organic LinkedIn posts from a thought leader's profile are the best candidates for paid promotion as Thought Leader Ads. Not every popular post makes a good ad. The goal is to find posts that (a) resonated organically, (b) align with the ICP's pain points, and (c) are eligible for promotion.

## Input

- Thought leader's LinkedIn profile (founder, exec, or subject-matter expert)
- ICP description with documented pain points and buying triggers
- Content pillars (the 3-5 topic areas the thought leader posts about)
- Access to LinkedIn analytics via Taplio, Shield, or LinkedIn native analytics

## Steps

### 1. Pull the Post Performance Data

Using the `linkedin-organic-analytics` fundamental, export the thought leader's post data for the last 90 days:

- For each post, capture: post text, format (text/image/video/carousel), publish date, impressions, likes, comments, shares, engagement rate, and any click data
- Sort by engagement rate descending
- Flag the top 20% of posts by engagement rate as "high performers"

If using Taplio:
```
GET https://app.taplio.com/api/v1/analytics/posts?start_date=2026-01-01&end_date=2026-03-30
```

If using Shield:
```
GET https://api.shieldapp.ai/v1/posts?start_date=2026-01-01&end_date=2026-03-30
```

### 2. Filter for TLA Eligibility

Remove posts that LinkedIn does not allow as Thought Leader Ads:

- Remove polls
- Remove "celebrating an occasion" posts
- Remove reshares of other people's content
- Remove posts containing article or newsletter links
- Remove posts older than 365 days
- Keep: text-only, single image, multi-image, native video, document/carousel posts

### 3. Score Posts for Ad Potential

For each eligible post in the top 20%, score on a 1-5 scale across four dimensions:

**Dimension A -- Organic engagement (1-5):**
- 5: Top 5% engagement rate for this profile
- 4: Top 10%
- 3: Top 20%
- 2: Top 40%
- 1: Below top 40%

**Dimension B -- ICP pain-point alignment (1-5):**
Use Claude (via `ai-content-ghostwriting` fundamental) to classify each post against your ICP pain points:
```
Prompt: Score how directly this LinkedIn post addresses the pain points of [ICP description].
Pain points: [list].
Post text: [post text].
Score 1-5 where 5 = directly addresses a top pain point with specificity,
1 = tangentially related or off-topic.
Return score and one-sentence justification.
```

**Dimension C -- Problem-aware framing (1-5):**
- 5: Post agitates a specific problem with data or a story, without pitching a solution
- 4: Post discusses a problem space with light product mention
- 3: Post is educational but solution-oriented
- 2: Post is mostly product/feature focused
- 1: Post is a company announcement or self-promotion

**Dimension D -- Comment quality signal (1-5):**
- 5: Multiple comments from people matching ICP titles (VP, Director, Head of) asking questions or sharing their own experience
- 4: Some ICP-matching commenters with substantive engagement
- 3: High comment count but mostly generic ("great post")
- 2: Low comment count but some quality
- 1: Few or no comments, or mostly bot/spam comments

**Composite score** = A + B + C + D (max 20). Rank all eligible posts by composite score.

### 4. Select the Top 4-6 Posts

From the ranked list, select 4-6 posts for promotion. Apply these selection rules:

- Include at least 2 different content pillars (topic diversity)
- Include at least 2 different formats (e.g., 2 text-only + 2 image posts)
- Do NOT select 2 posts that address the same pain point with the same angle
- If a post has a link in the first comment, note it -- this becomes the click-through destination
- Prefer posts where the thought leader shared a personal story or specific data over posts that give generic advice

### 5. Prepare the Promotion Brief

For each selected post, document:

- Post URL
- Composite score and individual dimension scores
- Primary pain point addressed
- Target audience segment (which ICP sub-segment this post best fits)
- Recommended campaign objective (Engagement for most posts; Brand Awareness if the post has no link)
- Whether the post needs a first-comment link added before promotion

### 6. Validate with the Thought Leader

**Human action required:** Share the selection brief with the thought leader. Confirm they approve each post being promoted. The thought leader may:
- Veto posts they feel are too personal or off-brand for ads
- Suggest additional posts the data might have missed (the founder often knows which posts generated inbound DMs that analytics do not capture)
- Request minor edits before promotion (note: you cannot edit the post after promotion begins without pausing the campaign)

## Output

- Ranked list of eligible posts with composite scores
- 4-6 selected posts with promotion briefs
- Thought leader approval on all selected posts
- Format and topic diversity confirmed
- Eligibility verified for all selected posts

## Triggers

Run this drill every 2-4 weeks, or whenever the thought leader publishes 3+ new posts. The post pool should always be fresh to avoid audience fatigue.
