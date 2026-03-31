---
name: youtube-channel-seo-scalable
description: >
  YouTube Channel SEO — Scalable Automation. Multiply output by optimizing existing videos in bulk,
  A/B testing thumbnails and titles, and scaling production without proportional effort through
  templated workflows and content series.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Scalable Automation"
time: "50 hours over 3 months"
outcome: ">=20,000 views/month from YT_SEARCH, CTR >=5% channel average, and >=50 website visits/month from YouTube"
kpis: ["YT_SEARCH views/month", "Total views/month", "CTR (channel average)", "Average view percentage", "Subscriber growth/month", "Website referrals/month", "Videos published/month", "Search ranking positions"]
slug: "youtube-channel-seo"
install: "npx gtm-skills add marketing/problem-aware/youtube-channel-seo"
drills:
  - youtube-keyword-research
  - ab-test-orchestrator
---

# YouTube Channel SEO — Scalable Automation

> **Stage:** Marketing > Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Outcomes

Find the 10x multiplier: scale YouTube search traffic without proportionally scaling founder recording time. Achieve this by optimizing existing videos (get more from what you have), A/B testing thumbnails and titles (increase CTR on every video), and creating templated content series (reduce per-video production time).

## Leading Indicators

- Existing video optimization lifts YT_SEARCH views by >=20% within 30 days of metadata updates
- A/B tests identify thumbnail/title variants that improve CTR by >=1 percentage point
- Templated series reduce per-video production time from 3 hours to 1.5 hours
- At least 5 videos rank in top 3 YouTube search results for their target keyword
- YouTube algorithm begins recommending your videos (SUGGESTED traffic grows)

## Instructions

### 1. Audit and optimize all existing videos

Run the the youtube seo optimization workflow (see instructions below) drill across the entire channel:

1. Pull the complete video inventory with metadata and analytics
2. Score each video's SEO health (0-100 scale based on title, description, tags, captions, CTR, retention)
3. Prioritize optimization: sort by `views * (100 - seo_score)` to fix high-traffic videos with the worst SEO first
4. For each optimization candidate:
   - Update title to include target keyword in first 60 characters
   - Rewrite description first 2 lines with keyword and compelling hook
   - Add timestamps/chapters to description if missing
   - Update tags with target keyword + related terms from keyword matrix
   - Download auto-generated captions, correct errors, upload corrected SRT
   - Flag low-CTR videos for thumbnail redesign
5. Log all changes with before/after data for impact measurement

Target: optimize 10-20 existing videos in the first 2 weeks. Expect 20-50% increase in search traffic for optimized videos.

### 2. Launch thumbnail and title A/B testing

Run the `ab-test-orchestrator` drill adapted for YouTube:

**Thumbnail tests:**
- Use TubeBuddy's built-in A/B test feature ($14.50/mo Legend plan) which alternates thumbnails and measures CTR
- Or manual A/B: run thumbnail A for 7 days, switch to thumbnail B for 7 days, compare CTR in YouTube Analytics
- Test variables one at a time: text overlay vs no text, face close-up vs screen grab, color scheme A vs B
- Run on videos with >=1,000 impressions/week for statistical significance

**Title tests:**
- Same approach: alternate titles weekly, measure CTR
- Test variables: question vs statement, with year vs without, with number vs without, keyword position

Run 2 tests per month. After each test, apply the winner permanently and apply the learning to all future videos.

### 3. Build templated content series

Identify your top 2-3 performing content formats from Baseline data (e.g., "X vs Y comparison", "How to do Z in 10 minutes", "Top 5 tools for W"). For each format, create a production template:

**Template includes:**
- Standard intro sequence (reusable across all videos in the series)
- Section structure with timing targets
- Standard B-roll or screen recording patterns
- Standard CTA sequence and end screen layout
- Metadata template: title formula, description boilerplate, tag set

Templated production cuts per-video time by 40-50% because the agent can pre-fill the script, metadata, and post-production settings.

### 4. Scale to 2-3 videos per week

With templates and optimized workflows:
- Agent prepares 4-6 scripts per batch from the keyword matrix
- **Human action required:** Founder batch-records 4-6 videos in one 3-hour session
- Agent handles all editing, optimization, captioning, and uploading
- Agent schedules videos across the week (Tuesday, Thursday, Saturday perform best for B2B)

### 5. Expand keyword coverage

Run `youtube-keyword-research` monthly to:
- Discover new keywords from YouTube search term data (what queries are people using that you haven't targeted?)
- Identify keyword gaps: topics where competitors rank but you don't
- Find long-tail opportunities: queries with low competition and clear commercial intent
- Plan content series around keyword clusters (group related keywords into playlists)

### 6. Build internal linking via playlists and end screens

Organize all videos into topic-based playlists. Each playlist targets a keyword cluster:
- "AI Agent Tutorials" playlist for all agent-building content
- "CRM Setup Guides" playlist for all CRM content
- etc.

Configure end screens to recommend the next video in the same playlist. This increases session time, which YouTube rewards with more recommendations.

### 7. Evaluate against threshold

After 3 months, measure against: >=20,000 views/month from YT_SEARCH, CTR >=5% channel average, and >=50 website visits/month from YouTube.

If PASS: The channel has found its 10x. Proceed to Durable.
If FAIL: If search views are high but CTR is low, focus on thumbnail/title testing. If CTR is high but total views are low, the problem is keyword volume — target higher-volume keywords. If website visits lag behind views, optimize description CTAs and add mid-roll cards linking to your site. Re-run the underperforming dimension.

## Time Estimate

- SEO audit and bulk optimization: 8 hours
- A/B test setup and management: 6 hours
- Template creation (3 series): 4 hours
- Video production (24-36 videos at 1.5 hours each with templates): 36-54 hours
- Monthly keyword refresh: 3 hours
- Playlist and internal linking setup: 2 hours
- **Total: ~50 hours over 3 months** (excluding founder recording time)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| YouTube Data API v3 | Upload, metadata, bulk updates | Free (10K units/day) |
| YouTube Analytics API | Performance metrics | Free |
| OBS Studio | Recording | Free |
| Descript | Editing, transcription, clips | $24/mo Creator |
| TubeBuddy | A/B testing, bulk processing, SEO scoring | $14.50/mo Legend |
| vidIQ | Keyword research, competitor tracking | $17.50/mo Boost |
| n8n | Workflow automation | Self-hosted free or $20/mo cloud |
| PostHog | Analytics and dashboards | Free tier or usage-based |

**Play-specific cost:** ~$75-95/mo

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- the youtube seo optimization workflow (see instructions below) — audit and optimize all existing video metadata, captions, and thumbnails
- `youtube-keyword-research` — monthly keyword refresh and content series planning
- the youtube video publish workflow (see instructions below) — templated video production at 2-3x cadence
- `ab-test-orchestrator` — systematic thumbnail and title A/B testing
