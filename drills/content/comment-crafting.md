---
name: comment-crafting
description: Write high-value LinkedIn comments that build familiarity and earn the right to DM prospects
category: Content
tools:
  - LinkedIn
  - Anthropic
fundamentals:
  - linkedin-organic-engagement
  - linkedin-organic-profile
  - ai-content-ghostwriting
---

# Comment Crafting

This drill teaches agents how to write LinkedIn comments that are valuable enough to get noticed, remembered, and ultimately open the door to DMs. The comment is the product in the comment-to-DM play -- a bad comment wastes a touch, and a good comment builds relationship equity.

## Input

- Daily comment queue from `prospect-content-discovery` drill (5-10 posts with URLs and context)
- ICP definition with pain points and domain expertise areas
- Founder's voice/tone guide (or 5+ examples of their best LinkedIn comments for style matching)

## Steps

### 1. Read the post thoroughly before commenting

For each post in your daily queue:
1. Read the entire post, not just the hook
2. Read the top 5-10 existing comments
3. Identify: What is the author's main argument? What did they get right? What did they miss? What related experience or data can you add?

Do NOT comment if you have nothing substantive to say. Skip the post and move to the next one. Five great comments beat ten mediocre ones.

### 2. Choose a comment strategy

Select one of these approaches based on the post content and your goal:

**Add Value (primary strategy, use 60% of the time):**
Share a relevant experience, data point, or framework that extends the author's point. "We ran into exactly this at [company]. What worked for us was [specific approach]. The key insight was [lesson]."

**Respectful Counterpoint (use 20% of the time):**
Disagree with a specific point and explain why. "Interesting take. I've seen it work differently -- [specific example]. I think the variable is [factor the author didn't consider]." Never be contrarian for attention. Only disagree when you genuinely see it differently and can articulate why.

**Ask a Sharp Question (use 15% of the time):**
Ask a question that shows you understood the post deeply and want to go further. "Great breakdown. Curious about one thing -- how do you handle [specific edge case or follow-up scenario]? We found that's where most of these approaches break down."

**Personal Story (use 5% of the time):**
Share a brief, relevant personal experience that resonates with the post. "This hit home. Last month we [situation]. The hardest part was [specific challenge]. Still figuring out [ongoing question]." Vulnerability and specificity make these comments memorable.

### 3. Write the comment

Rules for every comment:

- **Length**: 2-5 sentences. Long enough to be substantive, short enough to be read. Never write single-sentence comments ("Great post!" "So true!" "Love this!"). Never write 3-paragraph essays.
- **Specificity**: Reference a specific point from the post. "Your point about [X]..." proves you actually read it.
- **No self-promotion**: Never mention your product, company, or what you sell in comments. The goal is relationship building, not pitching. Your LinkedIn headline does the selling passively.
- **No links**: Do not drop links to your content, product, or blog in comments. This looks like spam and gets hidden by LinkedIn's algorithm.
- **Authentic voice**: Write in the founder's natural speaking style. Use contractions. Avoid corporate jargon. Be direct.
- **End with engagement**: Where natural, end with a question or statement that invites the author to reply. A reply from the author creates a public back-and-forth that builds visible familiarity.

### 4. Generate comments using AI assistance

Using the `ai-content-ghostwriting` fundamental, generate comment drafts for efficiency at scale:

**Prompt template for Claude:**
```
You are ghostwriting LinkedIn comments for {founder_name}, {founder_title} at {company}.

Voice guidelines: {paste 3-5 example comments from the founder}

Post to comment on:
Author: {author_name}
Post text: {full post text}
Top existing comments: {paste 2-3 top comments}

Strategy: {add_value | counterpoint | sharp_question | personal_story}

Write a 2-4 sentence comment that:
1. References a specific point from the post
2. Adds genuine value (new angle, experience, or data)
3. Matches the founder's voice
4. Does NOT mention {company} or {product}
5. Invites a reply naturally

Output ONLY the comment text, no preamble.
```

Review every AI-generated comment before posting. Edit for voice accuracy and authenticity. Never post a comment that sounds templated or generic.

### 5. Post comments at optimal times

- Comment within 1-4 hours of the post going live for maximum visibility
- LinkedIn surfaces recent comments higher in the comment thread
- Early comments (first 10-20) get seen by everyone who reads the post later
- Do not batch-post all 5-10 comments at once. Space them across the morning to look natural and avoid LinkedIn flagging

### 6. Track which comments get replies

After posting, record:
- Post URL and author name
- Comment text and strategy used
- Whether the author replied to your comment (critical signal)
- Whether other commenters engaged with your comment (likes, replies)
- Time from comment to any author response

Author replies are the key leading indicator. If an author replies to your comment, they now recognize your name. This is the signal that you can DM them within the next 2-7 days.

## Output

- 5-10 high-quality comments posted daily
- A log of each comment with strategy, text, and response tracking
- Identification of which prospects replied (DM-ready prospects)

## Triggers

Run daily, immediately after the `prospect-content-discovery` drill delivers the day's comment queue. Time: 20-40 minutes for manual comment writing, 10-20 minutes with AI assistance.
