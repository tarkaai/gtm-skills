---
name: slack-discord-content-posting
description: Create and post value-first original content to Slack/Discord communities that establishes authority
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

# Slack/Discord Content Posting

Create and publish original, value-first content in Slack workspaces and Discord servers. These posts build your reputation as a domain expert and create organic engagement that drives inbound interest. Content is written natively for each platform's culture and norms.

## Input

- Community engagement profiles (from `slack-discord-reconnaissance`)
- Your expertise areas, data, frameworks, and case studies
- Understanding of what content formats perform in each community

## Steps

### 1. Research what works in each community

Using `slack-api-read` or `discord-api-read`, study message patterns in your target communities:

**For Slack:**
- Review the last 200 messages in the 3 most active channels
- Identify which messages get the most thread replies and reactions
- Note common content patterns: questions, resource shares, case studies, hot takes, announcements
- Check if the community has a #showcase, #wins, #resources, or #introductions channel with different norms

**For Discord:**
- Review the last 200 messages in key text and forum channels
- In forum channels, sort by most replied/reacted to see what resonates
- Note whether the community favors short messages, long posts, images, or links
- Check for specific posting channels: #show-and-tell, #resources, #help, #general

### 2. Generate content ideas per community

For each target community, produce 3-5 content ideas matching proven formats:

**The Tactical Playbook** — Step-by-step guide solving a problem the community faces:
- "Here's the exact process we used to [achieve specific outcome]"
- Must be specific with real numbers and steps
- Best for: Slack #resources channels, Discord forum posts

**The Data Share** — Original data, benchmarks, or analysis:
- "We analyzed [X] across [N] companies. Here's what we found."
- Only use if you have genuine, non-obvious data
- Best for: Slack #general or topic channels, Discord forum posts

**The Honest Retrospective** — What you tried, what worked, what didn't:
- "We spent 3 months on [approach]. Here's what I'd do differently."
- Authenticity and specificity make these work
- Best for: Slack thread starters, Discord #general

**The Resource Roundup** — Curated list of useful tools/resources:
- "Tools I've tested for [workflow] — ranked by what actually works"
- Include competitors alongside your own tool (if relevant). Genuine evaluation only.
- Best for: Slack #tools or #resources channels, Discord #resources

**The Discussion Starter** — Prompt the community to share approaches:
- "How are you all handling [emerging challenge]?"
- "What's your current stack for [workflow]?"
- Best for: Slack #general, Discord #general or #chat

### 3. Write the content

**Slack posting rules:**
- Keep posts under 500 words. Slack is a chat platform, not a blog.
- Use Slack mrkdwn formatting: `*bold*` for key points, bullet lists, code blocks for technical content.
- Front-load the value — the first 2-3 lines are what people see before expanding.
- End with an invitation for discussion ("What's been your experience?"), not a CTA.
- If referencing your product, do it mid-post as one data point among many. Never end with a pitch.

**Discord posting rules:**
- Forum posts can be longer (up to 2000 characters per message). For detailed content, use forum channels.
- Use Discord Markdown formatting.
- Apply relevant forum tags when posting.
- In text channels, keep to 3-5 short paragraphs max.
- Include context (who you are, why you know this) in the first sentence, not as a credential flex.

**Content quality checks:**
- Does this teach something the reader didn't know?
- Could this stand alone without any product mention?
- Would the community's top contributors respect this?
- Is every claim backed by a specific number or example?

### 4. Choose posting time

Post during peak community activity hours (from engagement profile):
- **US-focused Slack communities:** 9-11am ET and 1-3pm ET weekdays
- **Global Discord servers:** Stagger across timezones; evening US hours (7-9pm ET) often work
- **Avoid:** Weekends (most B2B communities are quiet), Monday mornings (buried by catch-up chat), Friday afternoons

### 5. Post and engage

Submit the post via API (or manually for communities where API access is restricted).

After posting:
1. **Stay responsive for 2 hours.** Reply to every comment or question promptly. Early engagement generates more visibility.
2. **React to replies** to acknowledge them even if you don't have a full response yet.
3. **Expand on follow-up questions** — these threaded conversations are where authority is built.
4. **Log the post** per `community-engagement-tracking` fundamental.

### 6. Measure and iterate

After 48 hours, record:
- Thread replies count
- Emoji reactions count and type
- Referral sessions from PostHog (via UTM if links included)
- DMs or connection requests received
- Qualitative notes: what resonated, what fell flat

Compare across posts. Identify which formats, topics, and communities produce the most engagement and qualified traffic. Increase frequency in high-performing communities; pause or change strategy in low-performing ones.

## Output

- Published content in a target Slack/Discord community
- Activity log entry with engagement metrics (updated at 24h and 48h)
- Post-mortem notes on what worked

## Triggers

- 1-2 original posts per week during Smoke/Baseline
- 3-5 original posts per week during Scalable/Durable
- Prioritize communities with highest engagement scores from previous posts
