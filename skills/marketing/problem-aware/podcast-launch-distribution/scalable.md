---
name: podcast-launch-distribution-scalable
description: >
  Branded Podcast Launch — Scalable Automation. Multiply podcast reach through batch production, automated
  repurposing, cross-promotion partnerships, and A/B tested distribution to hit 2,000+ downloads/episode.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: ">=2,000 downloads/episode and >=30 qualified leads/quarter over 6 months"
kpis: ["Downloads per episode (30-day)", "Content pieces per episode", "Cross-promotion partner count", "Cost per lead from podcast", "Subscriber growth rate"]
slug: "podcast-launch-distribution"
install: "npx gtm-skills add marketing/problem-aware/podcast-launch-distribution"
drills:
  - content-repurposing
  - ab-test-orchestrator
  - dashboard-builder
---
# Branded Podcast Launch — Scalable Automation

> **Stage:** Marketing -> Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Outcomes
Find the 10x multiplier. Each episode now generates 15-20 derivative content pieces across platforms. Batch recording sessions (2-3 episodes per session) reduce production overhead. Cross-promotion partnerships with guests and complementary podcasts expand reach beyond your direct audience. A/B testing identifies which episode formats, topics, and promotion strategies drive the most downloads and leads.

## Leading Indicators
- Repurposed content output: >=15 pieces per episode (clips, posts, audiograms, newsletter blurbs)
- Cross-promotion: >=50% of guests share the episode with their audience
- Subscriber count (RSS + platform followers) growing >=10% month-over-month
- At least 2 cross-promotion partnerships with complementary podcasts active
- Cost per podcast-attributed lead decreasing month-over-month

---

## Budget

**Play-specific tools & costs**
- Buzzsprout/Transistor: $18-49/mo (higher tier for more upload hours and analytics)
- Riverside Business: $24/mo (multiple studios, advanced features)
- Descript Business: $33/mo (unlimited transcription, team features)
- Opus Clip or Headliner: $15-19/mo (automated clip extraction)
- Castmagic: $23/mo (AI show notes and social post generation)

**Total play-specific:** ~$115-150/mo

_Your CRM, PostHog, and automation platform are not included -- standard stack paid once._

---

## Instructions

### 1. Switch to batch recording sessions

Instead of recording one episode per week, batch-record 2-3 episodes per session. This reduces context-switching overhead and lets the founder focus recording into 1-2 days per month.

Schedule recording days:
- **Week 1, Tuesday**: Record episodes for weeks 1-2 (2 episodes back-to-back, 30 min each with 15 min break)
- **Week 3, Tuesday**: Record episodes for weeks 3-4

Run the the podcast episode production workflow (see instructions below) drill for each episode, but with batch optimizations:
- Keep Riverside studio configured and ready (no setup time per episode)
- Prepare all talking points for the batch in one session
- Edit all episodes in a single Descript project for consistency

### 2. Automate content repurposing

Run the `content-repurposing` drill adapted for podcast episodes. For each published episode, the agent produces:

1. **3-5 short clips** (30-90 seconds): Use Opus Clip or Descript to identify high-engagement moments. Export in vertical (1080x1920) for Reels/Shorts and square (1080x1080) for feed posts.
2. **2-3 audiograms** (if audio-only): Use Headliner to create waveform videos with captions.
3. **Blog post**: Transform the episode transcript into a 1,000-1,500 word blog post optimized for SEO. Publish on your blog with the episode embed.
4. **3 LinkedIn posts**: One per key insight, using hook-story-takeaway format.
5. **3 Twitter threads**: Condense key insights into 3-5 tweet threads.
6. **1 newsletter section**: 100-150 word blurb for your regular newsletter.
7. **3-5 pull quote images**: Quotable sentences formatted as branded image cards.

Build this as an n8n workflow: when an episode enters "published" status in Attio, the workflow generates asset checklists and drafts using Claude. The agent produces first drafts; human reviews and approves.

### 3. Scale the guest booking pipeline

Expand the the podcast guest booking workflow (see instructions below) drill to higher volume:
- Maintain a prospect list of 100+ potential guests in Clay (refresh monthly)
- Send 10-15 invitations per week via Instantly (Tier 2-3 use automated sequences, Tier 1 get personal emails)
- Target: book 2 months of episodes ahead at all times
- Track booking rate by tier and optimize invitation copy for the lowest-converting tier

Start booking "dream guests" (Tier 1) by leveraging your growing listener count and published episode catalog as social proof in invitations.

### 4. Launch cross-promotion partnerships

Identify 3-5 podcasts with complementary (not competing) audiences. Propose mutual promotion:
- **Ad swap**: Each show runs a 30-second pre-roll or mid-roll for the other show. Free. High trust because it is a host endorsement.
- **Guest swap**: You appear on their show, they appear on yours. Each show's audience discovers the other.
- **Newsletter cross-promotion**: Mention each other's episodes in your respective newsletters.

Use `dashboard-builder` to track which cross-promotion partnerships drive the most new subscribers and attribute leads by source.

### 5. A/B test episode and promotion variables

Run the `ab-test-orchestrator` drill to systematically test:

**Episode variables:**
- Episode length: 20 min vs 40 min vs 60 min -- which length gets highest completion rate?
- Format: solo vs interview vs panel -- which drives more downloads?
- Title style: question titles ("How do you...?") vs statement titles ("The secret to...") vs guest-name-first titles

**Promotion variables:**
- LinkedIn post format: text-only vs video clip vs audiogram -- which gets more clicks?
- Publish day: Tuesday vs Wednesday vs Thursday
- Email subject lines: episode title vs guest name vs teaser question
- CTA type: "Listen now" vs "Check out the episode" vs specific offer

Run each test for at least 4 episodes (2 control, 2 variant) before declaring a winner. Log results in PostHog.

### 6. Build the podcast performance monitoring system

Run the `dashboard-builder` drill to create comprehensive analytics:

1. PostHog dashboard: downloads by episode, traffic by promotion channel, lead funnel (visit -> signup -> meeting), episode long-tail value curve
2. Weekly automated report via n8n: episode performance vs benchmark, top-performing promotion assets, guest amplification rate
3. Attio enrichment: per-episode ROI score based on (leads * estimated deal value) / (production time + tool costs)
4. Pattern analysis after 20+ episodes: which topics, guests, formats, and promotion channels produce the best ROI?

Use the pattern analysis to inform guest selection, topic planning, and promotion strategy going forward.

### 7. Evaluate against threshold

Measure after 6 months:
- Average downloads per episode (30-day window): target >=2,000
- Total qualified leads from podcast per quarter: target >=30
- Content output per episode: target >=15 pieces
- Subscriber growth: target >=10% month-over-month

If PASS: Move to Durable. The podcast is a proven, scalable channel.
If FAIL: Identify the bottleneck. Low downloads? Focus on cross-promotion and guest audience leverage. Low leads? Optimize CTAs, landing pages, and tracking links. Low repurposing output? Invest in better automation tooling.

---

## Time Estimate
- Batch recording setup: 2 hours (one-time)
- Repurposing automation setup: 4 hours (one-time)
- Cross-promotion outreach: 3 hours (one-time)
- A/B test design: 2 hours (one-time)
- Performance monitoring setup: 3 hours (one-time)
- Weekly batch recording (2 episodes): 2 hours/session, 2x/month = 4 hours/month
- Weekly editing and repurposing review: 2 hours/week
- Weekly guest pipeline maintenance: 1 hour/week
- Weekly analytics review: 0.5 hours/week

Setup: 14 hours. Ongoing: ~15 hours/month.

---

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Buzzsprout | Podcast hosting, analytics, distribution | $18/mo (6h upload) |
| Transistor | Alternative hosting with analytics API | $49/mo (100K downloads) |
| Riverside | Batch recording sessions | $24/mo (Business plan) |
| Descript | Editing, transcription, clip extraction | $33/mo (Business plan) |
| Opus Clip | AI-powered clip extraction | $19/mo (Pro plan) |
| Headliner | Audiogram generation | $15/mo (Pro plan) |
| Castmagic | AI show notes and social post generation | $23/mo (Starter plan) |
| n8n | Distribution and repurposing automation | Self-hosted free or $20/mo cloud |
| Clay | Guest prospecting at scale | $149/mo (Explorer) |
| PostHog | Episode analytics and A/B testing | Free: 1M events/mo |
| Attio | Guest pipeline and episode ROI tracking | Free tier available |

---

## Drills Referenced
- the podcast episode production workflow (see instructions below) -- batch recording and publishing workflow
- `content-repurposing` -- transform each episode into 15+ derivative assets
- the podcast guest booking workflow (see instructions below) -- scaled guest pipeline with Tier 1 targeting
- `ab-test-orchestrator` -- test episode formats, promotion channels, and CTAs
- `dashboard-builder` -- comprehensive analytics, reporting, and pattern analysis
