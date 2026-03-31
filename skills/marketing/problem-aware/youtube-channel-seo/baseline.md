---
name: youtube-channel-seo-baseline
description: >
  YouTube Channel SEO — Baseline Run. Establish always-on YouTube analytics, a consistent weekly
  publishing cadence, and cross-platform content repurposing to sustain and grow search-driven
  video traffic.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Baseline Run"
time: "40 hours over 8 weeks"
outcome: ">=5,000 views/month from YT_SEARCH traffic, >=50% average view percentage across all videos, and >=15 website visits/month from YouTube"
kpis: ["YT_SEARCH views/month", "Total views/month", "Average view percentage", "CTR", "Subscriber growth rate", "Website referrals from YouTube", "Videos published per week"]
slug: "youtube-channel-seo"
install: "npx gtm-skills add marketing/problem-aware/youtube-channel-seo"
drills:
  - youtube-keyword-research
  - content-repurposing
  - posthog-gtm-events
---

# YouTube Channel SEO — Baseline Run

> **Stage:** Marketing > Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Outcomes

Prove that YouTube search traffic is sustainable at a consistent publishing cadence. The channel publishes 1-2 videos per week, all data flows into PostHog automatically, and each video is repurposed across platforms to multiply reach.

## Leading Indicators

- YT_SEARCH traffic grows week-over-week for 4+ consecutive weeks
- At least 2 videos rank on page 1 of YouTube search for their target keyword within 14 days of publishing
- Subscriber growth rate is positive and accelerating
- Content repurposing drives additional views on LinkedIn/Twitter (>=200 views per clip)
- Website referral traffic from YouTube increases each month

## Instructions

### 1. Expand keyword research

Run the `youtube-keyword-research` drill at full depth:
- Expand autocomplete research to 20 seeds with alphabet-soup expansion
- Validate search volume via Ahrefs YouTube keyword metrics or vidIQ
- Analyze competition for the top 50 keywords
- Build a complete keyword matrix with 30-50 validated topics
- Create an 8-week content calendar: 1-2 videos per week

### 2. Set up always-on analytics

Run the the youtube channel analytics workflow (see instructions below) drill to build the automated data pipeline:
- Configure PostHog event schema for YouTube metrics
- Build the n8n daily sync workflow: channel metrics, per-video metrics, traffic sources, search terms
- Build the PostHog dashboard with 6 panels: channel overview, video leaderboard, SEO performance, traffic source mix, content effectiveness, conversion tracking
- Set up anomaly alerts for search traffic drops, retention spikes, subscriber spikes, and CTR issues
- Configure the weekly performance report

### 3. Configure website conversion tracking

Run the `posthog-gtm-events` drill to track the YouTube-to-website conversion funnel:
- `yt_referral_landed`: fires when a visitor arrives on your website with `utm_source=youtube` or `referrer` contains `youtube.com`
- `yt_referral_engaged`: fires on scroll depth >50% or time on page >30s for YouTube-referred visitors
- `yt_referral_converted`: fires on form submit, demo booking, or signup from YouTube-referred visitors

Add UTM parameters to all YouTube description links: `?utm_source=youtube&utm_medium=video&utm_campaign={video_id}`

### 4. Produce videos at cadence

Run the the youtube video publish workflow (see instructions below) drill 1-2 times per week for 8 weeks.

At Baseline, refine the production workflow:
- Batch script writing: write 2-4 scripts in one session
- **Human action required:** Founder batch-records 2-4 videos in one recording session (more efficient than one-off recordings)
- Agent edits, optimizes metadata, and uploads each video on the scheduled publish date
- Agent uploads corrected captions for each video within 24 hours of publish

### 5. Repurpose each video across platforms

Run the `content-repurposing` drill for each published video:
- Extract 2-3 short clips (30-60 seconds) from each long-form video using Descript
- Create vertical versions (1080x1920) with burned-in captions for YouTube Shorts
- Write LinkedIn posts that reference the video content and link back
- Write Twitter/X threads summarizing the key points
- Schedule repurposed content over the following week

### 6. Review and optimize weekly

Each Monday, review the automated weekly report from the youtube channel analytics workflow (see instructions below):
- Which videos drove the most YT_SEARCH traffic? Schedule follow-up videos on those topics.
- Which videos had the highest retention? Replicate that format and pacing.
- Which search terms are driving traffic that you haven't explicitly targeted? Add them to the keyword matrix.
- Are any videos declining in search traffic? Flag for SEO refresh.

### 7. Evaluate against threshold

After 8 weeks, measure against: >=5,000 views/month from YT_SEARCH traffic, >=50% average view percentage across all videos, and >=15 website visits/month from YouTube.

If PASS: Search traffic is consistent and the funnel works. Proceed to Scalable.
If FAIL: Analyze which videos performed best and worst. If retention is the issue, improve content quality and pacing. If search traffic is the issue, revisit keyword targeting — you may be targeting keywords that are too competitive. If website visits are the issue, strengthen CTAs and description links. Re-run with adjustments.

## Time Estimate

- Keyword research expansion: 4 hours
- Analytics setup (n8n + PostHog): 6 hours
- Video production (12-16 videos x 2 hours each at improved efficiency): 24-32 hours
- Content repurposing (12-16 videos x 30 min each): 6-8 hours
- Weekly review and optimization: 4 hours
- **Total: ~40 hours over 8 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| YouTube Data API v3 | Upload, metadata, search | Free (10K units/day) |
| YouTube Analytics API | Performance metrics | Free |
| OBS Studio | Recording | Free |
| Descript | Editing, transcription, clips | $24/mo Creator |
| vidIQ or TubeBuddy | Keyword research, SEO scoring | $6-18/mo |
| n8n | Workflow automation | Self-hosted free or $20/mo cloud |
| PostHog | Analytics dashboard | Free tier (1M events/mo) or $0+ usage |

**Play-specific cost:** ~$50-60/mo

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- `youtube-keyword-research` — full keyword matrix and 8-week content calendar
- the youtube video publish workflow (see instructions below) — weekly video production and upload pipeline
- the youtube channel analytics workflow (see instructions below) — always-on PostHog dashboard, daily sync, and weekly reports
- `content-repurposing` — turn each video into clips, posts, and threads
- `posthog-gtm-events` — track YouTube-to-website conversion funnel
