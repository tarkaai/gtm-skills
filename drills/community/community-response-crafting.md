---
name: community-response-crafting
description: Craft authentic, value-first responses to community threads that build authority and generate inbound interest
category: Community
tools:
  - Reddit API
  - AI (Claude / GPT)
fundamentals:
  - reddit-api-read
  - reddit-api-write
  - community-engagement-tracking
---

# Community Response Crafting

This drill produces high-quality, community-appropriate responses to Reddit threads. The goal is genuine helpfulness that builds authority — not thinly-veiled marketing. Every response must pass the "would I upvote this if I didn't work here?" test.

## Input

- A thread URL or post ID to respond to
- Your product's expertise areas and relevant content (blog posts, guides, case studies)
- The subreddit's engagement profile (from `community-reconnaissance`)

## Steps

### 1. Analyze the thread

Using the `reddit-api-read` fundamental, fetch the post and its existing comments:

```
GET /r/SUBREDDIT/comments/POST_ID?limit=100&sort=top
```

Analyze:
- **What is the poster actually asking for?** (Not what you want to sell them — what they need)
- **What have existing comments already covered?** (Don't repeat what's been said)
- **What's the gap?** (What hasn't been addressed, or what's been addressed poorly)
- **What's the sentiment?** (Are people frustrated? Curious? Debating?)
- **How old is the thread?** (Posts older than 48 hours get minimal visibility; prioritize fresh threads)

### 2. Determine response type

Based on the analysis, choose one of these response archetypes:

**The Expert Answer** — When the poster has a specific question and you have deep expertise:
- Lead with the direct answer (no preamble)
- Explain the reasoning or tradeoffs
- Include specific numbers, benchmarks, or examples from experience
- Optionally link to a detailed resource if genuinely helpful

**The Framework Share** — When the poster needs a structured approach to a complex problem:
- Present a numbered framework or decision matrix
- Explain each step briefly
- Offer to elaborate on any step in replies

**The Experience Report** — When the poster wants to hear what worked for others:
- Share a specific, real experience (with numbers if possible)
- Be honest about what didn't work too
- Keep it concise — 2-3 paragraphs max
- End with what you'd do differently

**The Resource Curator** — When the poster needs to explore options:
- List 3-5 relevant resources (not just yours)
- Briefly describe each with pros/cons
- If your resource is relevant, include it as ONE item among several — never the only recommendation

**The Follow-up Question** — When the post is unclear or you need context to give a useful answer:
- Ask a clarifying question that shows you read the post carefully
- This builds engagement and positions you as thoughtful, not just drive-by commenting

### 3. Draft the response

Write the response following these rules:

**Formatting rules:**
- First line must directly address the question or topic (no "Great question!" or "Hey there!")
- Use Reddit Markdown: `**bold**`, bullet points, numbered lists, `code blocks`
- Keep total length under 300 words for comments, under 800 words for detailed posts
- Use paragraph breaks every 2-3 sentences for readability
- No emoji. No exclamation marks unless genuinely warranted.

**Content rules:**
- Lead with value, not credentials. Don't say "As a [title] at [company]..." as the opening line.
- Be specific. "We reduced churn by 23% in 6 weeks" beats "We improved retention."
- Include dissenting views. Acknowledging tradeoffs builds credibility.
- If linking to your own content, it must be genuinely the best resource for this specific question. The link should come after substantive value, never before it.
- Never link to a landing page, pricing page, or demo booking page. Only link to educational content (blog posts, open-source tools, frameworks).
- If you have no unique value to add, don't respond. Skipping a thread is better than posting filler.

**Self-promotion guardrails:**
- Maximum 1 in 10 responses should include a link to your own content
- When you do link, frame it as "I wrote about this in more detail here" or "We open-sourced a tool that does this" — not "Check out our product"
- If the subreddit rules say "no self-promotion," follow the rules. Period.

### 4. Review before posting

Before submitting, verify:
- [ ] Does this response directly address what the poster asked?
- [ ] Would I upvote this response if I saw it from a stranger?
- [ ] Is this the most helpful response in the thread, or am I just adding noise?
- [ ] Have I followed the subreddit's posting rules?
- [ ] If I included a link, is it genuinely the best resource (not just my resource)?
- [ ] Is the tone conversational, not corporate?

### 5. Post and track

Using the `reddit-api-write` fundamental, submit the comment:

```
POST /api/comment
thing_id=t3_POST_ID&text=YOUR_RESPONSE
```

If including a link, ensure it has UTM parameters per the `community-engagement-tracking` fundamental.

Log the interaction in your activity log:
- Date, subreddit, post URL, response type, link included (y/n), topic

### 6. Follow up

Check the thread 24 hours later using `reddit-api-read`:
- Did anyone reply to your comment? Respond to follow-ups promptly.
- What was your upvote count? Log it.
- Did the OP mark your response as helpful?

Responding to follow-ups is where authority is built. A drive-by comment is fine; a back-and-forth conversation where you help solve a real problem is what generates DMs and referral traffic.

## Output

- A posted comment or reply on Reddit
- Activity log entry with engagement metrics
- Follow-up interactions logged within 24-48 hours

## Triggers

- Triggered by keyword monitoring alerts (from `community-monitoring-automation` drill)
- Triggered by manual browsing during designated community engagement time
- Daily: respond to 2-5 threads across target subreddits
