---
name: founder-social-content-smoke
description: >
  Founder Social & Content — Smoke Test. Founder creates 5-7 LinkedIn posts with agent assistance,
  posts manually, engages with commenters, and measures whether content drives inbound leads or DMs.
stage: "Marketing > Unaware"
motion: "FounderSocialContent"
channels: "Social"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥ 3 leads or ≥ 2 meetings in 1 week"
kpis: ["Impressions per post", "Engagement rate", "Profile visits", "DMs received", "Leads captured"]
slug: "founder-social-content"
install: "npx gtm-skills add marketing/unaware/founder-social-content"
drills:
  - icp-definition
  - founder-linkedin-content-batch
  - linkedin-engagement-workflow
  - threshold-engine
---

# Founder Social & Content — Smoke Test

> **Stage:** Marketing → Unaware | **Motion:** FounderSocialContent | **Channels:** Social

## Outcomes

Prove that founder-led social content produces inbound interest. The founder publishes 5-7 LinkedIn posts over one week with agent-drafted content, engages personally with commenters, and captures leads from DMs and profile visits. Success = at least 3 inbound leads or 2 meetings booked from content-driven engagement.

## Leading Indicators

- Posts published (target: 5-7 over the week)
- Average impressions per post (target: 500+ for accounts under 5K followers)
- Engagement rate per post (target: 2-5% is good, 5%+ is excellent)
- Profile views during the posting week (target: 50+ weekly)
- DMs received referencing content (target: 1-3 per week)
- Connection requests received with relevant notes

## Instructions

### 1. Define your content ICP

Run the `icp-definition` drill to define who you are creating content for. For this play, focus on:
- Target audience job titles and seniority levels
- Pain points they actively search for solutions to
- LinkedIn usage patterns (are they active on the platform?)
- Content formats they engage with (text, video, carousels, polls)

Document 3-5 content pillars — topic areas where the founder has genuine expertise that overlaps with ICP pain points. Example pillars: "lessons from scaling engineering teams," "why most B2B pricing is wrong," "what we learned burning money on X."

### 2. Generate a week of content drafts

Run the `founder-linkedin-content-batch` drill to produce 5-7 LinkedIn post drafts:

1. Provide the agent with: content pillars, founder voice examples (10+ pieces of existing writing), and ICP pain points.
2. For each post, specify the format: text-only (best for first-time posters), story post, list post, or contrarian take.
3. Each draft must include: a hook that creates curiosity in the first line, a body that delivers a specific insight or experience, and a CTA that invites comments or DMs.

**Human action required:** The founder reviews every draft. Read each hook aloud — does it make you want to read more? Replace any generic advice with specific numbers, names, or experiences from your actual work. Approve, edit, or reject each draft. Target: 80%+ approval on first pass.

### 3. Publish and engage daily

**Human action required:** Post content manually on LinkedIn. Publish 1 post per day, Tuesday through Saturday, between 7:30-9:30am in your ICP's primary timezone.

Run the `linkedin-engagement-workflow` drill daily:

**Before posting (15 minutes):**
- Engage with 5-10 posts from ICP-relevant accounts in your feed. Leave substantive comments that add value — not "great post" but a real insight, counterpoint, or follow-up question.

**After posting (check at 30 min, 2 hours, end of day):**
- Reply to every comment on your post within the same business day.
- Ask follow-up questions to keep comment threads active.
- For anyone who comments with a buying signal (describing a problem your product solves), view their profile and prepare a DM.

**DM follow-up for high-intent signals:**
- When someone comments describing a problem you solve, DMs you about the post, or sends a connection request referencing your content, send a DM.
- First DM: reference their specific comment, ask about their situation. Do NOT pitch your product.
- Log every DM conversation in a spreadsheet: name, company, title, signal type, post URL, status.

### 4. Track results manually

Log each post's performance daily:
- Impressions (from LinkedIn native analytics or Creator Mode dashboard)
- Likes, comments, shares
- Profile views (from LinkedIn Analytics tab)
- DMs received
- Connection requests with relevant notes
- Leads identified (anyone who showed buying intent)

### 5. Evaluate against threshold

Run the `threshold-engine` drill at the end of the week:

**Pass threshold:** ≥ 3 leads or ≥ 2 meetings in 1 week

Count leads as: anyone who (a) DMed asking about your product/approach, (b) commented describing a problem you solve and responded positively to your DM, (c) booked a meeting through your content's CTA, or (d) was referred to you by someone who saw your content.

If PASS: document which content pillars and formats produced the leads. Proceed to Baseline.

If FAIL: diagnose —
- Low impressions? Hooks are weak. Rewrite using the `linkedin-organic-hooks` fundamental patterns.
- High impressions but low engagement? Content is broad, not targeted. Narrow to ICP-specific pain points.
- High engagement but no leads? Content is entertaining but not attracting buyers. Shift pillars toward problems your product solves.
- Good engagement but no DMs? CTA is weak. Replace "thoughts?" with specific action requests: "DM me 'playbook' and I'll send you the template."

Re-run with adjustments.

## Time Estimate

- ICP definition and content pillars: 1 hour
- Content batch generation and founder review: 1.5 hours
- Daily posting and engagement (5 days x 30 min): 2.5 hours
- Evaluation: 15 minutes
- **Total: ~5 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn (free account) | Publishing, engagement, DMs | Free |
| Anthropic Claude API | Content draft generation | ~$0.05/week (https://www.anthropic.com/pricing) |

## Drills Referenced

- `icp-definition` — define who the content targets and which pain points to address
- `founder-linkedin-content-batch` — generate, review, and prepare a week of LinkedIn posts
- `linkedin-engagement-workflow` — daily pre-post and post-publish engagement routine
- `threshold-engine` — evaluate pass/fail against the 3-lead / 2-meeting target
