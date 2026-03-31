---
name: community-content-posting
description: Create and publish value-first original content (posts) to target subreddits that establish authority
category: Community
tools:
  - Reddit API
  - AI (Claude / GPT)
fundamentals:
  - reddit-api-read
  - reddit-api-write
  - community-engagement-tracking
---

# Community Content Posting

This drill produces original posts for target subreddits — the kind that earn hundreds of upvotes, get saved, and position you as a domain expert. These are not repurposed blog posts; they are written natively for Reddit's culture and format.

## Input

- Target subreddit engagement profiles (from `community-reconnaissance`)
- Your expertise areas, data, frameworks, and case studies
- Recent trending topics in each target subreddit

## Steps

### 1. Research what performs in each subreddit

Using the `reddit-api-read` fundamental, pull the top posts from each target subreddit:

```
GET /r/SUBREDDIT/top?t=month&limit=50
```

For each subreddit, analyze the top 20 posts and identify:
- **Format patterns**: Are top posts long-form guides, quick tips, questions, data shares, or stories?
- **Title patterns**: Do top titles use numbers ("7 lessons from..."), questions ("How do you handle..."), or statements ("We grew from X to Y by...")?
- **Length**: How long are the top-performing text posts? (usually 300-1000 words on Reddit)
- **Engagement drivers**: What makes people comment — controversy, usefulness, relatability?
- **What's missing**: What topics come up in comments but nobody has written a dedicated post about?

### 2. Generate post ideas per subreddit

For each target subreddit, produce 3-5 post ideas that match the subreddit's proven formats:

**The Data Share** — Original data or analysis the community can't get elsewhere:
- "We analyzed [X] and here's what we found"
- "Benchmarks from [your domain] based on [N] companies"
- Only use if you have genuine, non-obvious data

**The Playbook** — Step-by-step guide to solving a problem the community faces:
- "How to [solve specific problem] — the exact process we used"
- Must be specific and actionable, not generic advice
- Include real numbers and examples

**The Lessons Learned** — Honest retrospective on something you tried:
- "What I learned after [doing X] for [time period]"
- Include failures and what you'd do differently
- Authenticity and specificity are what make these work

**The Tool/Resource Roundup** — Curated list of useful resources:
- "Tools I use for [workflow] — what works and what doesn't"
- Include competitors and alternatives alongside your own (if relevant)
- This only works if you provide genuine evaluation, not a thinly-veiled product pitch

**The Question/Discussion Starter** — Prompt the community to share their approaches:
- "How are you handling [emerging challenge]?"
- "What's your stack for [workflow]?"
- Good for building engagement and learning what the community cares about

### 3. Write the post

**Title rules:**
- Keep under 120 characters
- Be specific: "How we reduced customer churn from 8% to 3% in 90 days" beats "Tips for reducing churn"
- Match the subreddit's title style (check top posts)
- Don't use clickbait — Reddit communities punish it

**Body rules:**
- Open with context: who you are (role/company size, not company name), what you did, why it matters
- Use Reddit's Markdown: headers (`##`), bullet points, bold for key takeaways
- Include specific numbers, timelines, and outcomes
- Break into scannable sections — nobody reads walls of text
- End with an invitation for questions or discussion, not a CTA to your product
- If referencing your own content/tool, do so casually mid-post ("we built a tool to automate this part" or "I wrote a longer guide on step 3"), never as the conclusion

**Length targets by format:**
- Data Share: 400-800 words
- Playbook: 600-1200 words
- Lessons Learned: 300-600 words
- Resource Roundup: 300-500 words
- Question: 100-200 words

### 4. Select optimal posting time

From your subreddit engagement profile, post during peak activity hours. General Reddit engagement peaks:
- **Weekdays**: 8-10am EST and 12-2pm EST
- **Weekends**: 10am-12pm EST
- Avoid posting late evening or overnight (posts get buried before the active audience sees them)

### 5. Submit and engage

Using the `reddit-api-write` fundamental, submit the post. Then:

1. **Stay active for 2 hours after posting**: Reply to every comment promptly. Early engagement signals quality to Reddit's algorithm and pushes the post higher.
2. **Answer questions thoroughly**: Each comment thread is a chance to demonstrate expertise.
3. **Log the post** per `community-engagement-tracking` fundamental with all relevant metadata.

### 6. Measure and iterate

After 48 hours, record:
- Upvote score
- Number of comments
- Referral sessions from PostHog (via UTM if links were included)
- Any DMs or follow requests received
- Qualitative: what resonated, what fell flat

Compare against previous posts. Identify which formats, topics, and subreddits produce the most engagement and referral traffic. Double down on what works.

## Output

- Published Reddit post in a target subreddit
- Activity log entry with engagement metrics (updated at 24h and 48h)
- Post-mortem notes on what worked

## Triggers

- 1-2 original posts per week during Smoke/Baseline
- 3-5 original posts per week during Scalable/Durable
- Prioritize subreddits with highest engagement scores from previous posts
