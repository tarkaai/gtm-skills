---
name: video-prospecting-scale-smoke
description: >
  Video Prospecting at Scale — Smoke Test. Record 20-30 personalized Loom videos
  for named prospects, embed in cold emails, and validate whether AI-assisted
  video outreach produces higher response rates than text-only for solution-aware
  audiences.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=5% response rate from 30 personalized video emails in 1 week"
kpis: ["Response rate", "Video completion rate", "Time to response"]
slug: "video-prospecting-scale"
install: "npx gtm-skills add marketing/solution-aware/video-prospecting-scale"
drills:
  - icp-definition
  - build-prospect-list
  - video-prospecting-outreach
  - threshold-engine
---

# Video Prospecting at Scale — Smoke Test

> **Stage:** Marketing -> Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social

## Outcomes

Send 30 personalized Loom videos to named prospects. Each video is 60-90 seconds, recorded by the founder, referencing the prospect's name, company, and a specific enrichment signal. Embed the video as a GIF thumbnail in a cold email via Instantly. Validate that personalized video outreach produces a measurably higher response rate than text-only cold email for solution-aware prospects.

**Pass threshold:** >=5% response rate (replies with positive or neutral sentiment) from 30 video emails in 1 week.

## Leading Indicators

- Video thumbnail click rate >15% (prospects click the embedded GIF to watch)
- Average video watch percentage >40% (content holds attention past the hook)
- At least 1 reply explicitly references the video ("saw your video", "thanks for the video")
- Video emails achieve higher open rate than your historical text-only baseline

## Instructions

### 1. Define ICP and build target list

Run the `icp-definition` drill to document the firmographic and persona criteria for this video outreach test. Focus on solution-aware prospects: companies already using a competing product, evaluating tools in your category, or showing active buying signals (job postings, funding, tech stack changes).

Run the `build-prospect-list` drill to source 30-40 contacts matching this ICP from Clay and Apollo. For each prospect, ensure you have: first_name, company, role, website_url, and at least one enrichment signal (recent funding, new executive hire, competitor usage, relevant job posting). Export to Attio CRM.

### 2. Record personalized Loom videos

Run the `video-prospecting-outreach` drill. For each prospect in the batch:

1. Open the prospect's company website on screen
2. Record a 60-90 second Loom video following this structure:
   - **Opening (5-10s):** "Hey {first_name}, this is {sender_name} from {sender_company}."
   - **Hook (10-15s):** Reference their specific signal: "I noticed {company} just {signal}..."
   - **Value prop (20-30s):** Connect the signal to your product's value for their situation
   - **Proof (15-20s):** One result from a similar company
   - **CTA (10s):** "There's a link below to grab 15 minutes if this resonates."
3. Trim the video, add a CTA button linking to Cal.com
4. Name the video: `{company}-{firstname}-smoke-video`

Target 30 videos. At 2-3 minutes per recording (including setup), this takes 60-90 minutes.

**Human action required:** The founder must record these videos personally. The agent prepares prospect data, generates per-prospect script drafts from enrichment signals, sets up the email campaign, and tracks results.

### 3. Send video emails via Instantly

Using the `video-prospecting-outreach` drill's email setup steps:

1. Build a CSV mapping each prospect to their Loom video ID, share URL, and GIF thumbnail URL
2. Create a 3-step email sequence in Instantly:
   - **Email 1 (Day 0):** Video email with embedded GIF thumbnail linked to the Loom share URL
   - **Email 2 (Day 3):** Text follow-up referencing the video
   - **Email 3 (Day 7):** Breakup email with the video link as a fallback
3. Send to 30 prospects on weekdays, 8am-11am in their timezone

### 4. Track results manually

For each prospect, log in Attio:
- `video_sent: true`, `video_sent_date: {date}`
- `video_watched: true/false` (check Loom dashboard daily)
- `video_watch_pct: {percentage}` (from Loom viewer analytics)
- `video_cta_clicked: true/false`
- `email_replied: true/false`, `reply_sentiment: positive/neutral/negative`
- `meeting_booked: true/false`

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate:

- **Response rate:** Count replies with positive or neutral sentiment / 30 videos sent. Target: >=5%
- **Video engagement:** Count prospects who watched >=50% of the video. Log as a secondary metric.

If PASS: The video approach generates responses above threshold. Proceed to Baseline to add AI-generated video at volume and always-on tracking.

If FAIL: Diagnose the failure point:
- Low thumbnail clicks (<10%): Email subject line or GIF thumbnail not compelling. Test different subjects.
- Low video completion (<30% average): Videos too long or irrelevant. Shorten to 45-60 seconds. Front-load the hook.
- Watched but no replies: CTA weak or value prop not landing. Refine the video script's closing.
- Low open rate: Subject lines need work. Irrelevant to video, fix before re-testing.

## Time Estimate

- ICP definition and prospect list building: 1.5 hours
- Video recording (30 videos at 3 min each): 1.5 hours
- Email campaign setup in Instantly: 30 minutes
- Daily Loom dashboard check for 1 week: 30 minutes total
- Threshold evaluation and analysis: 30 minutes
- **Total: ~5 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom | Record personalized prospect videos | Free (Starter: 25 videos, 5-min limit) or $12.50/user/mo (Business, unlimited) — [loom.com/pricing](https://www.loom.com/pricing) |
| Instantly | Send cold email sequences with video embeds | $37/mo (Growth: 5,000 emails) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Clay | Enrich prospects with signals for personalization | $185/mo (Launch: 2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Cal.com | Booking link for video CTAs | Free (basic) or $12/mo (Team) — [cal.com/pricing](https://cal.com/pricing) |
| Attio | CRM to log video engagement and deals | Free (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |

**Estimated Smoke cost:** $0-50/mo (Loom free tier may suffice for 30 videos; Instantly and Clay may have existing subscriptions)

## Drills Referenced

- `icp-definition` — define target prospect criteria for video outreach
- `build-prospect-list` — source and enrich 30-40 prospects from Clay/Apollo
- `video-prospecting-outreach` — record Loom videos and build email campaign with embedded thumbnails
- `threshold-engine` — evaluate response rate against pass criteria
