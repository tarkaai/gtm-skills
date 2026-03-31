---
name: founder-linkedin-content-batch
description: Generate, review, and schedule a batch of LinkedIn posts in the founder's voice
category: Content
tools:
  - LinkedIn
  - Anthropic Claude API
  - Taplio
  - Buffer
  - Typefully
fundamentals:
  - ai-content-ghostwriting
  - linkedin-organic-hooks
  - linkedin-organic-formats
  - linkedin-organic-posting
  - linkedin-organic-scheduling
---

# Founder LinkedIn Content Batch

This drill produces a week's worth of LinkedIn posts for a founder, from topic selection through scheduling. It combines AI ghostwriting with the founder's review to maintain authenticity while reducing time investment.

## Input

- Content pillars (3-5 topic areas aligned with ICP pain points)
- Founder voice profile document (see `ai-content-ghostwriting` fundamental)
- 5-10 example posts from the founder (or content the founder has written elsewhere)
- Target posting frequency (default: 3-5 posts per week)
- ICP description (who the posts should resonate with)

## Steps

### 1. Select topics for the batch

For each post in the batch, choose a topic from one of your content pillars. Rotate across pillars so the feed has variety. For each topic, define:
- The specific angle (not just "leadership" but "why I stopped doing 1:1s and what replaced them")
- The format (text-only, carousel, story, list, poll -- see `linkedin-organic-formats` fundamental)
- The core insight or experience that makes this post worth reading
- The CTA (what you want readers to do: comment, DM, visit a link, share their experience)

### 2. Generate drafts via LLM

Using the `ai-content-ghostwriting` fundamental, send a batch request to generate all posts for the week. Provide:
- The founder's voice profile
- Example posts
- Each topic with its specific angle and format

For each generated draft, the output should include:
- Hook (first 1-2 lines -- the most important part)
- Body (the substance -- story, insight, framework)
- CTA (closing line that invites engagement)
- Suggested publish day and time

### 3. Founder review and edit

**Human action required:** The founder reviews every draft. For each post:

1. Read the hook. Does it create curiosity or tension in the first line? If not, rewrite it using patterns from the `linkedin-organic-hooks` fundamental.
2. Check authenticity. Replace any generic advice with specific details from the founder's actual experience. Replace "many companies struggle with X" with "we burned $20K on X before we figured out Y."
3. Test the CTA. Does it invite a specific action? "What's your take?" is weak. "What's the worst advice you've gotten about [topic]? Drop it in the comments." is strong.
4. Check length. 150-300 words for text posts. Cut ruthlessly -- every sentence must earn its place.

Mark each post as approved, needs-revision, or rejected. Revised posts go back through the LLM with feedback.

### 4. Schedule the batch

Using the `linkedin-organic-posting` fundamental (via Taplio, Buffer, Typefully, or LinkedIn native scheduling):

1. Schedule approved posts across the week. Default cadence: Tuesday, Wednesday, Thursday at 8:00am in the ICP's primary timezone.
2. Leave 1-2 empty slots for reactive/timely posts that come up during the week.
3. Confirm all posts are queued and scheduled.

### 5. Prepare engagement plan for each post

For each scheduled post, pre-plan:
- 3-5 accounts to engage with BEFORE publishing (see `linkedin-organic-engagement` fundamental -- engaging before posting warms the algorithm)
- A reply template for the most likely comment types (agreement, question, disagreement)
- A DM follow-up plan for anyone who comments with a buying signal

## Output

- {N} LinkedIn posts scheduled for the coming week
- Each post: hook, body, CTA, publish date/time, engagement plan
- Posts stored in scheduling tool ready to publish
- Founder has reviewed and approved all posts

## Triggers

Run this drill weekly, ideally on Friday or Monday, to prepare the following week's content. Time investment: 1-2 hours for the AI + founder review cycle.
