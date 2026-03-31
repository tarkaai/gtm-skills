---
name: thought-leadership-program-scalable
description: >
  Thought Leadership Program — Scalable. Automate the content pipeline with n8n workflows, scale to
  5+ posts/week across platforms, add video and podcast repurposing, build multi-channel distribution,
  and hit 60+ qualified leads over 6 months.
stage: "Marketing > ProblemAware"
motion: "FounderSocialContent"
channels: "Social, Content, Events"
level: "Scalable"
time: "80 hours over 6 months"
outcome: ">=50 posts published, >=8 speaking slots, and >=60 qualified leads attributed to thought leadership over 6 months, with engagement rate within 20% of Baseline benchmark"
kpis: ["Weekly content output", "Engagement rate by pillar", "Content-attributed leads/week", "Speaking pipeline conversion rate", "Repurposing multiplier", "Cost per content-attributed lead"]
slug: "thought-leadership-program"
install: "npx gtm-skills add marketing/problem-aware/thought-leadership-program"
drills:
  - founder-linkedin-content-batch
  - content-repurposing
  - conference-cfp-pipeline
  - dashboard-builder
---

# Thought Leadership Program — Scalable

> **Stage:** Marketing > ProblemAware | **Motion:** FounderSocialContent | **Channels:** Social, Content, Events

## Outcomes

Scale the thought leadership program to 5x Baseline output without proportional effort increase. Content generation, repurposing, and distribution are automated via n8n workflows. The founder's review time stays at 30-45 min/week while output scales from 3-4 posts/week to 5+ across multiple platforms. Speaking becomes a systematic pipeline. Content-to-lead attribution is fully instrumented.

**Pass threshold:** >=50 posts published, >=8 speaking slots, and >=60 qualified leads attributed to thought leadership over 6 months, with engagement rate within 20% of Baseline benchmark.

## Leading Indicators

- Content output reaches 5+ posts/week across LinkedIn, Twitter, and blog by month 2
- Engagement rate stays within 20% of Baseline average (quality is not sacrificed for quantity)
- Repurposing multiplier >= 3x (each source post produces 3+ derivative pieces)
- Content-attributed leads trend upward month over month
- Speaking acceptance rate >= 30%
- Cost per content-attributed lead decreasing quarter over quarter

## Instructions

### 1. Automate the Content Pipeline with n8n

Build an n8n workflow that orchestrates weekly content production:

**Trigger:** Every Friday at 9am via n8n cron

**Workflow steps:**
1. Pull last week's post performance from PostHog API: engagement rate, impressions, ICP comments per post
2. Identify the top-performing pillar from last week and the lowest-performing
3. Use Claude API to generate 5-7 draft posts: weight toward the top-performing pillar, test 1 post in a new angle for the underperforming pillar
4. Format each draft with: hook, body, CTA, recommended publish day/time, pillar tag, format type
5. Post drafts to Slack #content-review channel for founder approval
6. **Human action required:** Founder reviews and approves (30-45 min). Marks each draft as approved/edit/reject.
7. On approval, n8n schedules via Taplio API (or Buffer API): distribute across Tuesday-Friday
8. Log all scheduled posts to Attio with pillar, format, and predicted engagement

### 2. Scale Repurposing

Run the `content-repurposing` drill systematically:

**For every LinkedIn post scoring in the top 25% by engagement rate (checked 48h after publish via n8n):**

1. Twitter/X thread: break into 5-7 tweets, schedule via Typefully
2. Blog post: expand into 800-1,200 word article, publish via Ghost or company blog CMS
3. Newsletter section: include as a featured piece in the next weekly/biweekly newsletter
4. Video clip: if the post contains a framework or story, record a 60-90 second Loom or Descript clip. Post as LinkedIn native video.
5. Carousel: convert data-heavy or list posts into LinkedIn carousels using Canva templates

**Build an n8n workflow to automate the detection and routing:**
1. n8n cron (daily): query PostHog for posts published 48h ago with engagement rate > top 25% threshold
2. For qualifying posts, create tasks in the repurposing pipeline: assign format, set deadline, route to Slack
3. Track each derivative piece with a reference to the source post for attribution

### 3. Scale the Speaking Pipeline

Expand the `conference-cfp-pipeline` drill to systematic quarterly submissions:

1. Run `conference-cfp-search` monthly to find 5-10 new open CFPs
2. Maintain a rolling pipeline of 15-20 active CFP submissions in Attio
3. Use Claude API to generate proposals using proven talk topics (from speaking engagements that produced the most leads at Baseline)
4. Add podcast guest appearances as a parallel track: use the `media-target-research` drill to find 10-15 relevant podcasts per quarter, pitch the founder as a guest
5. Track all speaking activity in Attio: submissions, acceptances, talks delivered, leads captured per event

Target: 3-4 speaking slots per quarter (12-16 over 6 months, aim for >=8).

### 4. Deploy Performance Monitoring

Run the `dashboard-builder` drill:

1. Build the PostHog dashboard (5 panels: content output, engagement, growth, attribution, speaking)
2. Implement the thought leadership event taxonomy in PostHog
3. Configure anomaly detection for engagement, growth, and lead generation signals
4. Deploy weekly automated reports via n8n
5. Set up content-to-pipeline attribution tracking with UTMs

### 5. Set Guardrails

Configure n8n alerts for quality maintenance:

- **Engagement floor:** If average engagement rate drops below 80% of Baseline benchmark for 2 consecutive weeks, alert in Slack and reduce posting frequency by 1 post/week until recovery
- **Pillar health:** If any pillar's engagement rate drops below 1.5% for 4 consecutive posts, flag for pillar review (retire or refresh the angle)
- **Founder time cap:** Content review must stay under 45 min/week. If the queue grows, reduce batch size rather than rush review
- **Quality gate:** If more than 30% of posts in a week get below-average engagement, pause automation and audit content quality

### 6. Optimize Based on Data

Monthly optimization cycle:

1. Pull the monthly deep-dive from the `dashboard-builder` drill
2. Identify:
   - Which pillars and formats produce the most leads (not just engagement)?
   - Which speaking events produced leads vs. which were vanity?
   - What posting cadence (days/times) produces the best results?
   - Is the repurposing multiplier increasing or plateauing?
3. Adjust the content plan for the next month:
   - Increase weight on high-performing pillars
   - Retire or refresh underperforming formats
   - Adjust posting schedule based on time analysis
4. Feed optimization insights into the speaking pipeline: pitch topics that generated the most content engagement

## Time Estimate

- 2 hours: n8n content pipeline automation setup
- 1.5 hours/week: Content pipeline operation (generation, approval, scheduling) = 36 hours over 6 months
- 2 hours/month: Repurposing pipeline management = 12 hours over 6 months
- 3 hours/quarter: CFP research and submission = 6 hours over 6 months
- 4 hours: Performance monitoring setup (dashboard, events, anomaly detection)
- 2 hours/month: Monthly optimization review = 12 hours over 6 months
- 8 hours: Speaking preparation and delivery (varies by event count)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Taplio | LinkedIn scheduling + AI assist + analytics | $49/mo (Standard) — [taplio.com/pricing](https://taplio.com/pricing) |
| Typefully | Twitter/X scheduling and thread support | $12/mo (Creator) — [typefully.com](https://typefully.com) |
| n8n | Automation — content pipeline, repurposing, monitoring | $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Analytics — dashboards, attribution, anomaly detection | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — lead attribution and pipeline tracking | $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — CFP scoring, media research | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| Descript or Loom | Video repurposing | Descript $24/mo or Loom $15/mo — [descript.com/pricing](https://www.descript.com/pricing) |
| Claude API | Content generation, proposals | ~$30-50/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Taplio ~$49/mo + Typefully ~$12/mo + Descript/Loom ~$20/mo = ~$80/mo play-specific. n8n, PostHog, Attio, Clay are standard stack.

## Drills Referenced

- `founder-linkedin-content-batch` — automated weekly content generation, review, and scheduling pipeline
- `content-repurposing` — transform top-performing posts into derivative content across platforms and formats
- `conference-cfp-pipeline` — systematic CFP discovery, proposal generation, submission, and acceptance tracking
- `dashboard-builder` — continuous monitoring, anomaly detection, attribution tracking, and weekly/monthly reporting
