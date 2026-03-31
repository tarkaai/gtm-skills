---
name: conference-speaking-program-scalable
description: >
  Conference Speaking — Scalable. 10x the speaking pipeline by adding systematic content
  repurposing, A/B testing proposal styles, automating CFP-to-submission workflows,
  and scaling lead capture across all delivered talks.
stage: "Marketing > ProblemAware"
motion: "MicroEvents"
channels: "Events, Social"
level: "Scalable"
time: "60 hours over 6 months"
outcome: "≥10 talks delivered with ≥15 leads per talk average (≥150 total attributed leads) over 6 months"
kpis: ["Talks delivered per quarter", "Leads per talk", "Content repurposing multiplier", "Proposal acceptance rate", "Cost per attributed lead"]
slug: "conference-speaking-program"
install: "npx gtm-skills add marketing/problem-aware/conference-speaking-program"
drills:
  - conference-cfp-pipeline
  - speaking-lead-capture
  - speaking-performance-monitor
  - ab-test-orchestrator
---

# Conference Speaking — Scalable

> **Stage:** Marketing → ProblemAware | **Motion:** MicroEvents | **Channels:** Events, Social

## Outcomes

Scale the speaking program from 3 talks in 10 weeks to 10+ talks in 6 months. The 10x comes from three multipliers: (1) higher CFP submission volume through full automation of discovery-to-submission, (2) higher acceptance rates through A/B testing proposal styles, and (3) higher leads per talk through systematic content repurposing that extends each talk's reach from the conference room to social feeds for weeks afterward.

## Leading Indicators

- 20+ CFP submissions per quarter (up from 5 per bi-weekly cycle)
- Acceptance rate holds or improves above 30%
- Content repurposing multiplier ≥2x (repurposed content generates at least as many leads as the live talk)
- Post-talk follow-up sequence reply rate ≥5%
- Speaking program dashboard shows positive cost-per-lead trend (declining or stable)

## Instructions

### 1. Automate the full CFP-to-submission workflow

Extend the `conference-cfp-pipeline` drill with n8n automation:

1. Build an n8n workflow triggered by a bi-weekly cron schedule:
   - Step 1: Trigger Clay table refresh to scrape CFP aggregators for new open CFPs
   - Step 2: Auto-score new CFPs using the existing scoring formula
   - Step 3: For CFPs scoring 60+, call the `talk-proposal-generation` fundamental via Anthropic API to generate 3 proposal variants per CFP
   - Step 4: Score variants on specificity, audience alignment, and novelty (agent self-evaluation)
   - Step 5: Push the top-scored variant to Attio as a draft proposal with status "ready for review"
   - Step 6: Send Slack notification: "{N} new proposals ready for review"

2. Human review is now batch-mode: review 5-10 proposals in a single 30-minute session, approve/edit/reject each

3. For approved proposals, the n8n workflow auto-submits to platforms with API access (Sessionize, Papercall) and flags manual-submission CFPs for the speaker

This reduces human time per CFP from ~25 minutes (Baseline) to ~5 minutes (review only).

### 2. A/B test proposal styles

Run the `ab-test-orchestrator` drill on proposal writing:

1. Define proposal variants to test:
   - **Style A:** Problem-first (opens with audience pain, builds to solution)
   - **Style B:** Result-first (opens with a specific outcome/number, then explains how)
   - **Style C:** Story-first (opens with a narrative anecdote, then extracts the lesson)
2. For each CFP, generate all 3 styles using `talk-proposal-generation` with different system prompts
3. Randomly assign one style per submission (track style in PostHog as a property on `speaking_cfp_submitted`)
4. After 20+ submissions per style, compare acceptance rates
5. Adopt the winning style as default. Continue testing within the winning style (e.g., title length, abstract structure)

### 3. Scale content repurposing for every talk

After each delivered talk, run `speaking-lead-capture` with full content repurposing:

1. When the talk recording is available, use the `talk-content-repurposing` fundamental:
   - Produce a blog post from the transcript (publish within 7 days of the talk)
   - Extract 3-5 video clips (30-90 seconds each) with captions
   - Generate 3-5 quote graphics for social sharing
2. Build a content distribution schedule in n8n:
   - Day 1-3 post-recording: Publish blog post, share on LinkedIn with conference hashtag
   - Day 4-7: Post first 2 video clips on LinkedIn (space 2 days apart)
   - Day 8-14: Post remaining clips and quote graphics
   - Day 15-21: Cross-post best-performing clip to Twitter/X
3. Every piece of content links back to the companion resource page (UTM-tagged per content piece)
4. Track the "repurposing multiplier": leads from repurposed content / leads from live talk

Target: each talk generates content that produces leads for 3-4 weeks after the event, not just on the day.

### 4. Deploy always-on performance monitoring

Run the `speaking-performance-monitor` drill:

1. Build the PostHog speaking program dashboard with: CFP funnel, lead yield per talk, acceptance rate trend, content repurposing multiplier, cost per lead
2. Set up automated alerts:
   - Acceptance rate drops below 20% → review proposal quality
   - Lead capture rate is zero 48 hours post-talk → check infrastructure
   - Follow-up sequence open rate drops below 30% → refresh email copy
3. Enable the quarterly analysis workflow that generates a speaking program brief with recommendations

### 5. Optimize conference targeting

Using data from the performance monitor, refine which conferences to target:

1. Rank all conferences by leads-per-talk and cost-per-lead
2. Identify the "sweet spot" conference profile: what size, type, region, and topic track produces the best ROI?
3. Weight the CFP scoring formula to prioritize the sweet spot attributes (update Clay scoring columns)
4. Deprioritize conferences that produced talks but few leads (vanity metric trap)
5. Track the impact: does the updated targeting improve average leads-per-talk over the next quarter?

### 6. Evaluate against threshold

- **Pass threshold:** ≥10 talks delivered with ≥15 leads per talk average (≥150 total) over 6 months
- **Pass:** The speaking program is a reliable, scalable channel. Document the operating playbook: CFP cadence, proposal style, content repurposing process, top conference profiles. Proceed to Durable.
- **Marginal pass (10 talks, 10-14 leads/talk average):** Content repurposing may be underperforming. Check: Are clips getting engagement? Is the blog post driving traffic? Is the companion page converting? Optimize repurposing and run one more quarter.
- **Fail (<10 talks in 6 months):** CFP volume or acceptance rate is the bottleneck. Either increase submission volume (target 30+ per quarter) or broaden to include meetups and community events alongside conferences.

## Time Estimate

- 8 hours: n8n automation setup (CFP pipeline, content distribution schedules)
- 4 hours: A/B test design and variant prompt engineering
- 2 hours per talk x 10 talks: Content repurposing review and distribution = 20 hours
- 4 hours: Performance dashboard setup
- 2 hours per month x 6 months: Monitoring, optimization, quarterly analysis = 12 hours
- 16 hours: Talk preparation and delivery (human time, not agent time)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Automated CFP discovery and scoring | Launch: $185/mo (https://www.clay.com/pricing) |
| Descript | Talk recording repurposing (clips, captions) | Creator: $24/mo (https://www.descript.com/pricing) |
| Anthropic API | Proposal generation at scale (~60 proposals/6mo) | ~$5.40/6mo |
| Cal.com | Booking links per talk | Free or Team: $12/user/mo (https://cal.com/pricing) |
| Loops | Post-talk email sequences | Free up to 1,000 contacts (https://loops.so/pricing) |
| Sessionize | Speaker profile, bulk submissions | Free for speakers (https://sessionize.com/pricing) |

**Total Scalable budget:** Clay $185/mo + Descript $24/mo = ~$209/mo

## Drills Referenced

- `conference-cfp-pipeline` — fully automated CFP discovery, scoring, proposal generation, and submission tracking
- `speaking-lead-capture` — lead capture infrastructure with full content repurposing for every talk
- `speaking-performance-monitor` — always-on dashboard, alerts, and quarterly analysis of speaking program ROI
- `ab-test-orchestrator` — A/B test proposal styles to maximize acceptance rates
