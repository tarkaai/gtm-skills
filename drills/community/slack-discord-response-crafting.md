---
name: slack-discord-response-crafting
description: Craft authentic, value-first responses to Slack/Discord community threads that build authority and generate inbound interest
category: Community
tools:
  - Slack API
  - Discord API
  - AI (Claude / GPT)
fundamentals:
  - slack-api-read
  - slack-api-write
  - discord-api-read
  - discord-api-write
  - community-engagement-tracking
---

# Slack/Discord Response Crafting

Produce high-quality, community-appropriate responses to Slack and Discord threads. The goal is genuine helpfulness that builds authority and trust. Every response must pass the test: "Would a community veteran upvote/react to this if they didn't know I worked at this company?"

## Input

- A message or thread URL/link to respond to (from keyword monitoring alerts or manual browsing)
- Your product's expertise areas and relevant resources (blog posts, docs, open-source tools)
- The community's engagement profile (from `slack-discord-reconnaissance`)

## Steps

### 1. Analyze the conversation

Using `slack-api-read` or `discord-api-read`, fetch the message and its thread:

**Slack:**
```
GET conversations.replies?channel={CHANNEL_ID}&ts={THREAD_TS}
```

**Discord:**
```
GET /channels/{CHANNEL_ID}/messages?around={MESSAGE_ID}&limit=50
```

Analyze:
- **What is the person actually asking?** Separate the stated question from the underlying need.
- **What has already been said?** Read all existing replies. Do not repeat advice already given.
- **What is the gap?** What hasn't been addressed, or what was addressed incorrectly?
- **What is the community context?** Is this a casual chat, a technical help channel, or a showcase channel?
- **How fresh is the thread?** Slack threads older than 24 hours get minimal visibility. Discord forum posts stay visible longer.

### 2. Determine response type

Choose the response archetype that fits:

**The Expert Answer** — The person has a specific question and you have deep knowledge:
- Lead with the direct answer. No preamble.
- Explain the reasoning or tradeoffs.
- Include specific numbers, benchmarks, or examples from experience.
- Optionally link to a detailed resource if genuinely the best resource for this question.

**The Framework Share** — The person needs a structured approach to a complex problem:
- Present a numbered framework or decision matrix.
- Keep it concise (Slack/Discord messages should be scannable).
- Offer to elaborate on any step in follow-up replies.

**The Experience Report** — The person wants to hear what worked for others:
- Share a specific, real experience with outcomes (numbers if possible).
- Be honest about what didn't work.
- Keep to 2-3 short paragraphs.

**The Resource Curator** — The person needs to explore options:
- List 3-5 relevant resources (not just yours).
- Briefly describe each with a one-line assessment.
- If your resource fits, include it as ONE among several.

**The Clarifying Question** — The post is ambiguous or you need context:
- Ask a specific question that shows you read the original message carefully.
- This positions you as thoughtful and opens a conversation thread.

### 3. Draft the response

**Slack formatting rules:**
- Use Slack mrkdwn: `*bold*`, `_italic_`, `` `code` ``, ` ```code block``` `
- Use bullet points for lists
- Keep messages under 500 words. Slack messages are read in a compact UI.
- Thread replies are preferred over channel-level messages.
- No emoji spam. One relevant reaction on the original message is fine.

**Discord formatting rules:**
- Use Discord Markdown: `**bold**`, `*italic*`, `` `code` ``
- Keep messages under 2000 characters (Discord's hard limit).
- For longer responses, split across 2-3 messages in sequence.
- In forum channels, make your first reply substantive — it sets the tone for the thread.

**Content rules (both platforms):**
- Lead with value. Do not open with "Hey!" or "Great question!"
- Be specific. "We reduced onboarding time from 14 days to 3 days" beats "We improved onboarding."
- Acknowledge tradeoffs. Showing nuance builds credibility.
- If linking to your own content, it must be the best resource for this specific question. The link comes after substantive value, never as the opening.
- Never link to a pricing page, demo page, or signup page. Only link to educational content.
- If you have nothing unique to add, skip the thread. Not responding is better than adding noise.

**Self-promotion guardrails:**
- Maximum 1 in 10 responses should include a link to your own content.
- Frame it as: "I wrote about this in detail here" or "We open-sourced a tool that does this" — not "Check out our product."
- If the community rules prohibit self-promotion, follow them without exception.
- In paid communities, rules are usually stricter. Read them twice.

### 4. Review before posting

Verify before submitting:
- [ ] Does this directly address what was asked?
- [ ] Would I react positively to this response from a stranger?
- [ ] Am I adding unique value, not just echoing what others said?
- [ ] Did I follow this community's specific rules?
- [ ] If I included a link, is it genuinely the best resource?
- [ ] Is the tone peer-to-peer, not corporate?

### 5. Post and track

Using `slack-api-write` or `discord-api-write`, submit the response. For third-party communities where API posting is not possible, the agent drafts the response and the human posts it manually.

If including a link, ensure UTM parameters per the `community-engagement-tracking` fundamental:
```
?utm_source=slack&utm_medium=community&utm_campaign=communities-slack-discord&utm_content={workspace}_{channel}_{topic}
```

Log the interaction:
- Date, platform, community name, channel, thread URL, response type, link included (y/n), topic

### 6. Follow up within 24 hours

Check the thread using `slack-api-read` or `discord-api-read`:
- Did anyone reply to your message? Respond promptly.
- Did your message get reactions? Note which.
- Did anyone DM you? Log the DM conversation in Attio.

Follow-up conversations are where relationships are built. A single response is a data point; a multi-reply conversation where you solve someone's real problem is what generates DMs and inbound interest.

## Output

- A posted response in a Slack/Discord community thread
- Activity log entry with engagement metrics
- Follow-up interactions logged within 24 hours

## Triggers

- Triggered by keyword monitoring alerts (from `slack-discord-keyword-monitoring` fundamental via n8n)
- Triggered by manual browsing during designated community engagement time
- Daily target: respond to 3-5 threads across target communities
