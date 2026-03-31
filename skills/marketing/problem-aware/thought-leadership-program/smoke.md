---
name: thought-leadership-program-smoke
description: >
  Thought Leadership Program — Smoke Test. Audit the founder's existing content, define 3-5 content
  pillars aligned to ICP pain points, produce and publish 5 pieces manually, and validate that the
  founder's content generates measurable engagement and at least 5 qualified inbound signals.
stage: "Marketing > ProblemAware"
motion: "FounderSocialContent"
channels: "Social, Content, Events"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: ">=5 posts published, >=2% average engagement rate, and >=5 qualified inbound signals (DMs, comments from ICP titles, profile views from target companies) within 2 weeks"
kpis: ["Posts published", "Average engagement rate", "ICP-matching comments", "Profile views from ICP titles", "Inbound DMs"]
slug: "thought-leadership-program"
install: "npx gtm-skills add marketing/problem-aware/thought-leadership-program"
drills:
  - threshold-engine
---

# Thought Leadership Program — Smoke Test

> **Stage:** Marketing > ProblemAware | **Motion:** FounderSocialContent | **Channels:** Social, Content, Events

## Outcomes

Prove that the founder's content resonates with problem-aware prospects. At this level, the agent audits existing content, defines content pillars from evidence, helps draft posts, and the founder publishes manually. No scheduling tools, no automation, no budget. The goal is raw signal: does this founder's voice attract the right audience?

**Pass threshold:** >=5 posts published, >=2% average engagement rate, and >=5 qualified inbound signals (DMs, comments from ICP titles, profile views from target companies) within 2 weeks.

## Leading Indicators

- First 2 posts each get >=500 impressions (baseline reach exists)
- At least 1 post gets 3+ comments from people with ICP job titles (VP, Director, Head of)
- Founder receives at least 1 unsolicited DM or connection request mentioning a post
- Engagement rate on pillar-aligned posts exceeds engagement rate on off-pillar posts
- At least 1 post generates a multi-sentence comment (deep engagement, not just emoji reactions)

## Instructions

### 1. Run the Content Audit

Run the the thought leadership content audit workflow (see instructions below) drill:

1. Pull the founder's last 90 days of LinkedIn posts via LinkedIn Creator Analytics (native, no tools required)
2. For each post, record: date, text preview, format, impressions, engagement rate, comment count, and ICP-matching comments
3. Build a Clay table with all content scored by engagement rate (40%), ICP resonance (30%), comment depth (20%), and link performance (10%)
4. Identify the top 10 performing posts and the bottom 10
5. Define 3-5 content pillars from the evidence: topic groups where average score >= 3.5 and ICP alignment is clear
6. Generate a voice profile from the top 10 posts using Claude API
7. Map 1-2 competitor founders' content for gap analysis

At Smoke level, the Clay table can be replaced with a spreadsheet if Clay is not yet configured. The voice profile and pillar definitions are the critical outputs.

### 2. Define the 2-Week Content Plan

Using the content pillars and voice profile from step 1:

1. Select 5-7 topics, one per post, distributed across at least 3 pillars
2. For each topic, define:
   - The specific angle (not "AI in hiring" but "Why we stopped using AI to screen resumes and what we do instead")
   - The format (text-only or image — keep it simple for Smoke)
   - The hook style that performs best from the audit (personal story, data point, contrarian take, or tactical how-to)
   - The CTA (invite a comment, ask a question, link to a resource)
3. Generate drafts using Claude API with the founder's voice profile
4. **Human action required:** Founder reviews every draft. Rewrites hooks that feel generic. Adds specific personal details. Approves or rejects each post.

### 3. Publish and Engage

**Human action required:** The founder publishes manually on LinkedIn, 3-4 posts per week:

1. Post at 8:00-9:00am in the ICP's primary timezone (Tuesday through Thursday are highest-reach days on LinkedIn)
2. For the first 30 minutes after posting, actively engage: reply to every comment within 2 hours, like relevant posts from 3-5 ICP-matching accounts before and after publishing
3. Track engagement on each post in a spreadsheet: impressions (at 24h and 48h), likes, comments (total and from ICP titles), shares, profile views, DMs received

### 4. Evaluate Against Threshold

Run the `threshold-engine` drill:

1. After 2 weeks, compile all post metrics from the tracking spreadsheet
2. Calculate:
   - Total posts published (threshold: >=5)
   - Average engagement rate across all posts (threshold: >=2%)
   - Qualified inbound signals: count of DMs, ICP-title comments, and profile views from target companies (threshold: >=5)
3. Pass threshold: >=5 posts AND >=2% average engagement rate AND >=5 qualified inbound signals
4. Identify which pillars and formats drove the best results

**If PASS:** Content pillars resonate with the audience. Proceed to Baseline with a scheduling tool and expanded distribution.

**If FAIL:** Diagnose:
- Low impressions: founder's network may be too small. Add 50+ targeted connections before re-running.
- Low engagement: hooks are weak or topics are off-target. Revisit pillar selection. Test personal stories vs data-driven posts.
- Low ICP signals: content is attracting the wrong audience. Tighten topic focus to ICP-specific pain points.

## Time Estimate

- 2 hours: Content audit (pull analytics, score, define pillars)
- 1 hour: Voice profile generation
- 2 hours: Draft 5-7 posts with Claude + founder review
- 2 hours: Publishing and engagement over 2 weeks (~15 min/post)
- 1 hour: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn | Content publishing and native analytics | Free — [linkedin.com](https://linkedin.com) |
| Attio | CRM — log content audit results and leads | Free plan (up to 3 users) or $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Claude API (optional) | Draft generation and voice profiling | Usage-based, ~$5-10 for Smoke — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Free. Claude API usage optional and minimal.

## Drills Referenced

- the thought leadership content audit workflow (see instructions below) — audit existing content, define pillars, generate voice profile, and map competitive landscape
- `threshold-engine` — evaluate Smoke test results against the pass threshold and recommend next action (advance, iterate, or pivot)
