---
name: linkedin-founder-threads-smoke
description: >
  Founder LinkedIn content — Smoke Test. The founder publishes 5 thought leadership
  posts on LinkedIn over 1 week to test whether their personal content can generate
  inbound interest from people who do not yet know they have a problem.
stage: "Marketing > Unaware"
motion: "FounderSocialContent"
channels: "Social"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 3 inbound leads (DMs, comments with buying signals, or connection requests referencing content) in 1 week"
kpis: ["Impressions per post", "Engagement rate", "Profile views", "Inbound DMs"]
slug: "linkedin-founder-threads"
install: "npx gtm-skills add marketing/unaware/linkedin-founder-threads"
drills:
  - founder-linkedin-content-batch
  - linkedin-engagement-workflow
---

# Founder LinkedIn Content — Smoke Test

> **Stage:** Marketing > Unaware | **Motion:** FounderSocialContent | **Channels:** Social

## Outcomes

The founder has published 5 LinkedIn posts over 1 week and proven that their content can attract inbound interest. At least 3 people have reached out via DM, commented with a relevant problem, or sent a connection request referencing the content. This proves the founder's voice and topics resonate with an audience that can become pipeline.

## Leading Indicators

- Posts averaging 500+ impressions (for accounts with <5K followers) or 2x the founder's current average
- Engagement rate above 2% (likes + comments + shares / impressions)
- Profile views increasing day-over-day during the posting week
- At least 1 DM or buying-signal comment by day 3 of the week

## Instructions

### 1. Optimize the founder's LinkedIn profile

**Human action required:** Before publishing any content, the founder must update their LinkedIn profile. Follow the `linkedin-organic-profile` fundamental:

- Rewrite the headline as a value proposition, not a job title. Example: "Helping DevOps teams ship 3x faster | CEO at Acme" instead of "CEO at Acme Corp."
- Write a 150-word About section: line 1-2 = the problem you solve, lines 3-5 = your credibility, lines 6-8 = what you are building and for whom, line 9 = CTA (DM me, book a call, visit link).
- Enable Creator Mode and add 5 relevant topic hashtags.
- Pin 2-3 Featured items: a high-performing post, a link to your product or landing page, and a lead magnet if available.

This is one-time setup. Do not skip it -- an unoptimized profile wastes every impression your content earns.

### 2. Define content pillars and ICP

Define 3 content pillars aligned with problems your ICP experiences before they know a solution exists. These are NOT product-focused topics. They are the upstream problems and frustrations that eventually lead someone to need what you sell.

Example for a DevOps tool company:
- Pillar 1: "Why deployments break" (stories about production incidents and what causes them)
- Pillar 2: "Engineering team velocity" (frameworks and opinions about shipping faster)
- Pillar 3: "The founder-CTO trap" (personal stories about scaling an engineering org)

For each pillar, write down:
- 2-3 specific angles or stories the founder can tell
- Why this topic matters to the ICP (what pain does it touch?)
- What CTA makes sense (comment, DM, link to resource)

### 3. Generate a batch of 5 LinkedIn posts

Run the `founder-linkedin-content-batch` drill to produce 5 posts:

1. Collect 5-10 examples of the founder's existing writing (past LinkedIn posts, emails to the team, blog posts, talk transcripts). If the founder has no existing content, conduct a 30-minute interview and transcribe it.
2. Build a voice profile document from these examples (see `ai-content-ghostwriting` fundamental).
3. Generate 5 drafts via LLM API, one per content pillar (rotate pillars across the 5 posts). Each draft must include a hook, body, and CTA.
4. **Human action required:** Founder reviews each draft. Replace generic phrases with specific numbers, names, and experiences. Strengthen any hook that does not create curiosity or tension in the first line. Approve, revise, or reject each draft.

### 4. Schedule and publish

Schedule the 5 approved posts across the week:
- Tuesday 8am, Wednesday 8am, Thursday 8am (primary posting days)
- Plus 2 posts on Monday and Friday if the founder wants 5/week
- Use LinkedIn's native scheduling (free) or Taplio if available

**Human action required:** The founder publishes these posts. At the Smoke level, do not use automation -- the founder posts manually or via LinkedIn's built-in scheduler.

### 5. Execute daily engagement

Run the `linkedin-engagement-workflow` drill each day a post is published:

1. **Before the post goes live (15 min):** Comment on 5-10 posts from ICP-relevant accounts. Leave substantive 2-4 sentence comments, not "great post." This warms the algorithm.
2. **30 minutes after posting:** Reply to every comment on your post. Ask follow-up questions. Each reply extends the post's reach.
3. **2 hours after posting:** Reply to new comments. Check who liked the post -- if any match your ICP, view their profile (triggers a notification to them).
4. **End of day:** Final reply sweep. Log post metrics: impressions, likes, comments, shares.

### 6. Track engagement and capture leads

For each post, record in a spreadsheet:
- Post URL, topic pillar, format
- Impressions, likes, comments, shares (check 48 hours after publishing)
- Profile views that day (LinkedIn shows this in your analytics)
- Any DMs received referencing the post
- Any comments containing buying signals ("we have this exact problem", "how does your tool handle X?")
- Any connection requests with notes referencing the content

Count as an inbound lead: any DM, buying-signal comment, or content-referencing connection request from someone who matches your ICP.

### 7. Evaluate against threshold

At the end of the week:
- Total inbound leads: count DMs + buying-signal comments + content-referencing connections
- **Pass threshold: >= 3 inbound leads in 1 week**
- If PASS: document which pillars and formats performed best. Proceed to Baseline.
- If FAIL: analyze which posts got engagement vs. which got leads. Adjust: try different pillars, use stronger hooks, add clearer CTAs. Re-run Smoke for another week.

## Time Estimate

- Profile optimization: 30 minutes (one-time)
- Content pillar definition + voice profile: 30 minutes
- AI draft generation + founder review/edit: 45 minutes
- Daily engagement (5 days x 20 min): 1 hour 40 minutes
- Tracking + evaluation: 15 minutes
- **Total: ~3 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn (free) | Publishing posts, engaging, DMs | Free |
| Claude or GPT API | Generating post drafts | ~$0.05 for 5 posts |
| Taplio (optional) | Scheduling + basic analytics | $39/mo Starter -- not required at Smoke level |

**Smoke test total cost: Free** (LinkedIn + LLM API cost is negligible)

## Drills Referenced

- `founder-linkedin-content-batch` -- generates and schedules the week's posts with founder review
- `linkedin-engagement-workflow` -- daily engagement routine to maximize reach and capture leads
