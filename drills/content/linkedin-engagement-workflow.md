---
name: linkedin-engagement-workflow
description: Execute pre-post and post-publish engagement on LinkedIn to maximize reach and capture leads
category: Content
tools:
  - LinkedIn
  - Attio
  - n8n
fundamentals:
  - linkedin-organic-engagement
  - linkedin-organic-dms
  - attio-contacts
  - n8n-triggers
---

# LinkedIn Engagement Workflow

This drill defines the daily engagement routine that makes founder LinkedIn content actually work. Posting alone is not enough -- strategic engagement before and after publishing is what drives reach, builds relationships, and converts viewers into leads.

## Input

- Today's scheduled LinkedIn post (from `founder-linkedin-content-batch` drill)
- List of 10-20 ICP-relevant accounts to engage with (peers, prospects, industry voices)
- CRM access to log new leads from engagement

## Steps

### 1. Pre-post engagement (15 minutes, do this BEFORE your post goes live)

Using the `linkedin-organic-engagement` fundamental:

1. Open LinkedIn and go to your feed.
2. Find 5-10 posts from people in your target accounts list or ICP-adjacent voices.
3. Leave a substantive comment on each -- not "great post" but a comment that adds value: share a related experience, offer a counterpoint, add a data point, or ask a genuine follow-up question.
4. Each comment should be 2-4 sentences. Your profile photo and headline appear next to every comment, so each one is a micro-impression on the commenter's audience.
5. Like 5-10 additional posts from ICP-relevant accounts. This puts your profile in their notifications.

Why this works: LinkedIn's algorithm notices your activity and is more likely to distribute your next post to the audiences of people you just engaged with.

### 2. Post-publish engagement (check at 30 min, 2 hours, and end of day)

After your post goes live:

**At 30 minutes:**
- Reply to every comment that has appeared. Ask a follow-up question to keep the thread going. Each reply counts as additional engagement and extends the post's reach window.
- If someone shares a relevant experience in their comment, reply with something that shows you actually read it: "That's a great point about [specific thing they said] -- we had a similar experience when..."

**At 2 hours:**
- Reply to all new comments.
- Check who liked the post. If anyone who liked it matches your ICP (check their headline/title), view their profile. This puts a notification in their inbox ("Founder at X viewed your profile") and often triggers a connection request or DM from them.
- If the post is performing well (2x your average engagement), share it to your LinkedIn Stories or mention it in a follow-up comment to extend reach.

**At end of day:**
- Final reply sweep on all comments.
- Log post performance: impressions, likes, comments, shares.

### 3. DM follow-up for high-intent signals

Using the `linkedin-organic-dms` fundamental:

When any of these signals appear, send a DM:
- Someone comments describing a problem your product solves ("We've been struggling with exactly this...")
- Someone asks about your product or approach in the comments
- Someone DMs you referencing the post
- A connection request arrives with a note mentioning your content

DM template (adapt to context):
"Hey [name], thanks for your comment on my post about [topic]. Your point about [specific thing they said] really resonated. Curious -- are you currently dealing with [problem area]? Would love to hear more about your situation."

Do NOT pitch your product in the first DM. The goal is to start a conversation and understand their situation. Move to a call only after they confirm they have the problem.

### 4. Log leads in CRM

Using the `attio-contacts` fundamental, for every person who shows buying intent:

1. Create or update their contact record in Attio
2. Set `lead_source` = "linkedin-content"
3. Set `first_touch_post` = the LinkedIn post URL that triggered their engagement
4. Set `lead_status` = "dm-sent" or "conversation-active" or "meeting-booked"
5. Add a note with their original comment or DM text for context

### 5. Build an engagement target list (weekly refresh)

Maintain a list of 20-30 LinkedIn accounts to regularly engage with. Categories:
- **ICP prospects**: People at companies that could buy your product
- **Industry peers**: Other founders or leaders whose audience overlaps with your ICP
- **Big accounts**: Influencers in your space with 10K+ followers (commenting on their posts gives you exposure to their audience)

Refresh this list weekly. Remove accounts that are not active or relevant. Add new accounts you discover through your post engagement.

## Output

- Daily engagement completed (pre-post + post-publish)
- All comments replied to within same business day
- High-intent DMs sent to qualified engagers
- New leads logged in CRM with source attribution
- Engagement target list maintained

## Triggers

Run this drill daily on every day a post is published. On non-posting days, still do the pre-post engagement routine (step 1) to maintain algorithmic momentum. Total daily time: 20-30 minutes.
