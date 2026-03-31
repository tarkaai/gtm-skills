---
name: youtube-channel-seo-smoke
description: >
  YouTube Channel SEO — Smoke Test. Research YouTube search demand in your niche, produce and
  publish 4 SEO-optimized videos, and measure whether YouTube search drives views and website
  traffic for your ICP.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Smoke Test"
time: "20 hours over 4 weeks"
outcome: ">=1,000 views from YT_SEARCH traffic and >=3 website visits from YouTube in 4 weeks"
kpis: ["YT_SEARCH views", "Total views", "Average view percentage", "Click-through rate", "Website referral visits from YouTube"]
slug: "youtube-channel-seo"
install: "npx gtm-skills add marketing/problem-aware/youtube-channel-seo"
drills:
  - icp-definition
  - youtube-keyword-research
  - youtube-video-publish
  - threshold-engine
---

# YouTube Channel SEO — Smoke Test

> **Stage:** Marketing > Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Outcomes

Prove that your ICP searches for topics you can credibly cover on YouTube, and that optimized videos can rank in YouTube search and drive traffic to your website. This is a signal test — does YouTube search work as a discovery channel for your product?

## Leading Indicators

- YouTube autocomplete returns suggestions matching your ICP pain points (keyword demand exists)
- Uploaded videos appear in YouTube search results within 7 days of publishing
- At least one video achieves >50% average view percentage (content resonates)
- At least one video achieves >4% CTR in search results (title + thumbnail work)

## Instructions

### 1. Define your YouTube content ICP

Run the `icp-definition` drill. Document:
- 3-5 job titles your ICP holds
- 10-20 pain points or questions they would search on YouTube (phrased as search queries, e.g., "how to automate cold outreach", "best crm for startups")
- What content format they expect (tutorial, explainer, comparison, walkthrough)
- What competing channels already serve this audience (list 3-5 competitor YouTube channels)

### 2. Research YouTube keyword demand

Run the `youtube-keyword-research` drill with your ICP pain points as seed keywords.

For the Smoke Test, limit scope:
- Run autocomplete expansion on your top 10 seed keywords
- Skip Ahrefs/vidIQ volume validation (use free autocomplete data only)
- Analyze competition for top 20 keyword suggestions: search each on YouTube, check if the top 3 results are from large channels (>100K subs) or small ones
- Select 4 keywords where competition is Low or Medium
- Build a 4-week content calendar (1 video per week)

### 3. Set up recording environment

Using the `obs-recording-setup` fundamental (referenced within `youtube-video-publish`):
- Install OBS and configure for 1080p screen + webcam recording
- Test audio quality: record 30 seconds, play back, ensure no echo or background noise
- Create a basic scene: screen capture for tutorials, webcam-only for thought leadership

**Human action required:** The founder records all 4 videos. The agent prepares scripts, configures recording, and handles all post-production and upload.

### 4. Produce and publish 4 videos

Run the `youtube-video-publish` drill once per week for 4 weeks. For each video:

1. Agent writes the video script based on the keyword matrix entry
2. **Human action required:** Founder records the video following the script outline
3. Agent imports recording into Descript, removes filler words and dead air, exports final MP4 and SRT captions
4. Agent optimizes title (keyword in first 60 chars), description (keyword in first 2 lines + timestamps), and tags (target keyword + 5-10 related terms)
5. **Human action required:** Founder approves thumbnail design
6. Agent uploads video via YouTube Data API with optimized metadata
7. Agent uploads corrected SRT captions after YouTube processes the video
8. **Human action required:** Founder adds end screens and cards in YouTube Studio

### 5. Track performance manually

After each video has been live for 7 days, pull metrics using the YouTube Analytics API (manual query, no automation yet):
- Views (total and from YT_SEARCH)
- Average view percentage
- Click-through rate
- Traffic sources breakdown
- Top search terms driving traffic

Log results in a spreadsheet or CRM note per video.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to measure results against: >=1,000 views from YT_SEARCH traffic and >=3 website visits from YouTube in 4 weeks.

If PASS: YouTube search is a viable channel. Proceed to Baseline.
If FAIL: Diagnose. If views are low but retention is high, the problem is keyword selection or thumbnail CTR — try different keywords. If views are decent but no website traffic, the problem is CTAs — add stronger calls to action and description links. Re-run with adjustments.

## Time Estimate

- ICP definition and keyword research: 3 hours
- Recording setup and testing: 2 hours
- Video production (4 videos x 3 hours each: script + record + edit + upload): 12 hours
- Performance tracking and analysis: 3 hours
- **Total: ~20 hours over 4 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| YouTube Data API v3 | Video upload and metadata | Free (10K units/day) |
| YouTube Analytics API | Performance metrics | Free |
| OBS Studio | Video recording | Free (open source) |
| Descript | Video editing and transcription | Free plan (1 hr transcription) or $24/mo Creator |

**Play-specific cost:** $0-24/mo (Descript only if free tier exceeded)

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- `icp-definition` — define the target audience and their YouTube search behavior
- `youtube-keyword-research` — find validated search queries with manageable competition
- `youtube-video-publish` — record, edit, optimize, and upload each video
- `threshold-engine` — evaluate pass/fail against the smoke test threshold
