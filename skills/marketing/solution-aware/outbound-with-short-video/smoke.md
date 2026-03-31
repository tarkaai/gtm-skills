---
name: outbound-with-short-video-smoke
description: >
  Outbound With Short Video — Smoke Test. Record 15-25 personalized Loom videos
  addressed to named prospects, embed in cold emails, and measure whether video
  outreach produces higher watch-through and meeting rates than text-only.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: ">=10% video completion rate AND >=2 meetings booked from video outreach in 1 week"
kpis: ["Video completion rate", "Thumbnail click-through rate", "Meetings booked from video"]
slug: "outbound-with-short-video"
install: "npx gtm-skills add marketing/solution-aware/outbound-with-short-video"
drills:
  - icp-definition
  - build-prospect-list
  - video-prospecting-outreach
  - threshold-engine
---

# Outbound With Short Video — Smoke Test

> **Stage:** Marketing -> Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email

## Outcomes

Send 15-25 personalized Loom videos to named prospects. Each video is 60-90 seconds, recorded by the founder, referencing the prospect's name, company, and a specific signal or pain point. Embed the video as a GIF thumbnail in a cold email via Instantly. Measure whether prospects watch the video and whether it leads to booked meetings.

**Pass threshold:** >=10% video completion rate (watched >75% of the video) AND >=2 meetings booked in 1 week.

## Leading Indicators

- Thumbnail click rate >15% (prospects are curious enough to click the video)
- Average watch percentage >50% (the video content is holding attention)
- At least 1 positive reply mentioning the video (qualitative signal that video is differentiating)
- Video emails have higher open rate than your text-only baseline (subject line + thumbnail preview working)

## Instructions

### 1. Define your ICP and build a target list

Run the `icp-definition` drill to document your Ideal Customer Profile for this video outreach test. Focus on the firmographic and persona criteria that define your best prospects: company size, industry, role/title, and the top 3 pain points your product solves.

Run the `build-prospect-list` drill to source 20-30 contacts matching this ICP from Clay and Apollo. For each prospect, ensure you have: first name, company name, role, company website URL, and at least one enrichment signal (recent funding, new hire, job posting, competitor usage). Export to Attio CRM.

### 2. Record personalized Loom videos

Run the `video-prospecting-outreach` drill. For each prospect in your batch:

1. Open the prospect's company website on your screen
2. Record a 60-90 second Loom video following this structure:
   - **Opening (5-10s):** "Hey {first_name}, this is {your_name} from {your_company}."
   - **Hook (10-15s):** Reference their specific signal: "I saw {company} just {signal}..."
   - **Value prop (20-30s):** Connect the signal to your product's value
   - **Proof (15-20s):** One quick proof point from a similar company
   - **CTA (10s):** "There's a link below to grab 15 minutes if this resonates."
3. Trim the video, add a CTA button linking to your Cal.com booking page
4. Name the video: `{company}-{firstname}-smoke-video`

Target 15-25 videos. At 2-3 minutes per video (including setup), this takes 45-75 minutes.

**Human action required:** The founder must record these videos personally. AI agents can prepare the prospect data, generate video scripts from enrichment signals, and set up the email campaign, but the recording requires a human on camera.

### 3. Send video emails via Instantly

Using the `video-prospecting-outreach` drill's email setup steps:

1. Build a CSV mapping each prospect to their Loom video ID
2. Create a 3-step email sequence in Instantly:
   - Email 1 (Day 0): Video email with embedded GIF thumbnail
   - Email 2 (Day 3): Text follow-up referencing the video
   - Email 3 (Day 7): Breakup email with the video link as a "watch later" option
3. Send to your 15-25 prospects on weekdays, 8am-11am in their timezone

### 4. Track results manually

For each prospect, log in Attio:
- Video sent: yes/no
- Video watched: yes/no (check Loom dashboard daily)
- Watch percentage (from Loom analytics)
- CTA clicked: yes/no
- Email replied: yes/no + sentiment
- Meeting booked: yes/no

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate:
- **Video completion rate:** Count prospects who watched >=75% of the video / total videos sent. Target: >=10%
- **Meetings booked:** Count total meetings from this campaign. Target: >=2

If PASS: The video approach generates engagement and meetings. Proceed to Baseline to automate and scale.

If FAIL: Diagnose the failure point:
- Low thumbnail click rate (<10%): The email subject line or thumbnail is not compelling. Test different subject lines.
- Low completion rate: Videos are too long or not relevant enough. Shorten to 45-60 seconds and front-load the hook.
- Watched but no meetings: The CTA is weak or the value prop is not landing. Refine the video script.

## Time Estimate

- ICP definition and prospect list: 1 hour
- Video recording (20 videos at 3 min each): 1 hour
- Email campaign setup in Instantly: 30 minutes
- Daily monitoring for 1 week: 30 minutes total
- Evaluation and analysis: 30 minutes
- **Total: ~4 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom | Record personalized prospect videos | Free (Starter: 25 videos, 5-min limit) or $12.50/user/mo (Business, unlimited) — [loom.com/pricing](https://www.loom.com/pricing) |
| Instantly | Send cold email sequences with video embeds | $37/mo (Growth: 5,000 emails) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Clay | Enrich prospects with signals for video personalization | $185/mo (Launch: 2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Cal.com | Booking link for video CTAs | Free (basic) or $12/mo (Team) — [cal.com/pricing](https://cal.com/pricing) |
| Attio | CRM to log video engagement and deals | Free (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |

**Estimated Smoke cost:** $0-50/mo (Loom free tier may suffice for 25 videos; Instantly and Clay may have existing subscriptions)

## Drills Referenced

- `icp-definition` — define target prospect criteria for video outreach
- `build-prospect-list` — source and enrich 20-30 prospects from Clay/Apollo
- `video-prospecting-outreach` — record Loom videos and build email campaign with embedded thumbnails
- `threshold-engine` — evaluate video completion rate and meeting count against pass criteria
