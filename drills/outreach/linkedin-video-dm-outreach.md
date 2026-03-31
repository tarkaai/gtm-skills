---
name: linkedin-video-dm-outreach
description: Record personalized Loom videos and deliver them via LinkedIn DMs with pre-engagement warm-up for solution-aware prospects
category: Outreach
tools:
  - Loom
  - LinkedIn
  - Clay
  - Attio
fundamentals:
  - loom-personalized-outreach
  - loom-analytics
  - linkedin-organic-engagement
  - clay-enrichment-waterfall
  - attio-contacts
  - attio-deals
---

# LinkedIn Video DM Outreach

This drill combines personalized Loom video recording with LinkedIn DM delivery. Unlike email-based video outreach (`video-prospecting-outreach`), this drill sends the video link inside a LinkedIn DM, which produces higher open rates (LinkedIn DMs are read 3-5x more than cold email) and leverages the social proof of your LinkedIn profile. The video makes the DM stand out in a sea of text-only messages.

The approach: engage with the prospect's content for 3-5 days, then send a DM containing a 60-second personalized video. The video references something specific from their LinkedIn activity, connects it to a pain point you solve, and offers a low-friction CTA.

## Input

- Scored prospect list from Clay with LinkedIn URLs and enrichment data (name, company, role, pain point, recent signal)
- ICP definition completed (from `icp-definition` drill)
- Loom Business account with CTA buttons enabled
- LinkedIn account (Sales Navigator recommended for InMail if not connected)
- Cal.com booking link for video CTAs
- Attio workspace for tracking

## Steps

### 1. Prepare prospect enrichment for video scripts

Open your Clay table with the target prospect batch. Use the `clay-enrichment-waterfall` fundamental to ensure these columns are populated for each prospect:

- First name
- Company name
- Role/title
- LinkedIn profile URL
- One specific trigger signal (e.g., "just raised Series A", "posted about scaling engineering", "hired 3 new SDRs this month")
- Company website URL

Add a Clay AI formula column that generates two outputs per prospect:

1. **Video hook** (one sentence): "I saw your post about {specific_topic} -- it got me thinking about {connection_to_your_value_prop}."
2. **DM intro** (the text that accompanies the video link in the DM): "Hey {first_name}, recorded a quick 60-second video for you about {topic}. No pitch, just a thought on {pain_point_area}."

### 2. Pre-DM engagement warm-up (3-5 days)

Using the `linkedin-organic-engagement` fundamental, warm up each prospect before the video DM:

- **Day 1**: Like 2-3 of their recent posts. If they have no recent posts, like or comment on their company page content.
- **Day 2**: Leave a substantive comment on one of their posts. Add a data point, a relevant experience, or a genuine question. No product mentions.
- **Day 3-4**: Like 1-2 more posts. If they reply to your comment, continue the conversation.
- **Day 5**: Record and send the video DM (step 3).

Process 5-10 prospects per day through this sequence. Stagger start dates so you have a daily cadence of prospects reaching Day 5.

The warm-up is critical: your name and face appear in their notifications before the DM arrives. When they see your DM, you are a familiar name, not a stranger.

### 3. Record personalized Loom videos

Using the `loom-personalized-outreach` fundamental, record one video per prospect:

1. Open the prospect's LinkedIn profile on screen (they will see you looking at their profile in the video -- this is the personalization signal)
2. Start Loom recording (camera + screen, camera dominant)
3. Follow the 60-second template:
   - **Opening (5s)**: "Hey {first_name}, {your_name} here."
   - **Hook (10s)**: Reference their specific signal from Clay enrichment: "I saw your post about {topic} / noticed {company} just {signal}..."
   - **Connection (15s)**: Bridge to the pain point: "That usually means {pain_point_implication}. We've been working on exactly that with companies like {similar_company}."
   - **Proof (15s)**: One concrete result: "{similar_company} went from X to Y in Z weeks using this approach."
   - **CTA (10s)**: "If that's relevant, I'd love 15 minutes to walk you through it. There's a link below, or just reply here."
4. Stop recording, trim dead space
5. Add CTA button: "Book 15 Minutes" linking to `https://cal.com/{you}/15min?utm_source=loom&utm_medium=linkedin-dm&utm_campaign={campaign_slug}`
6. Name the video: `{company}-{firstname}-li-dm-{campaign_slug}`
7. Copy the share link

Target pace: 3 minutes per video including setup. A 10-prospect batch takes ~30 minutes.

### 4. Craft and send the LinkedIn DM

Using the `linkedin-organic-engagement` fundamental, send the DM with the video link. Structure:

```
Hey {first_name} -- I recorded a quick 60-second video for you after seeing your post about {topic}.

No pitch, just a thought on {pain_point_area}: {loom_share_url}

Curious to hear what you think.
```

Rules:
- Keep the DM text under 300 characters (excluding the URL). Short DMs get read.
- The Loom share link renders with a rich preview in LinkedIn DMs showing the video thumbnail. This is the visual hook.
- Send between 8am-11am in the prospect's timezone.
- Never send more than 15 video DMs per day to avoid LinkedIn restrictions.
- If you are not connected: use LinkedIn Sales Navigator InMail. InMail subject line: "Recorded this for you, {first_name}" (curiosity-driven, no pitch).

### 5. Follow-up sequence

If no response after 5 days, send one text-only follow-up DM:

```
Hey {first_name} -- not sure if you caught the video I sent. Quick summary: {one_sentence_value_prop}.

Happy to jump on a 15-min call if it's relevant: {cal_link}

Either way, enjoyed your recent post about {topic}.
```

If no response after 10 days total: tag in Attio as `linkedin-video-dm-no-response` and route to email channel via `cold-email-sequence` drill.

Never send more than 2 follow-up DMs after the initial video DM.

### 6. Log all activity in CRM

Using the `attio-contacts` fundamental, update each prospect record:

- `video_dm_sent: true`
- `video_dm_date: {date}`
- `video_loom_url: {share_url}`
- `video_dm_campaign: {campaign_slug}`
- `lead_source: linkedin-video-dm`
- `linkedin_engagement_start: {day_1_date}`

Using the `attio-deals` fundamental, create a deal when:
- Prospect replies positively: stage = "Interested"
- Prospect books a meeting via CTA: stage = "Meeting Booked"

### 7. Monitor video engagement

Using the `loom-analytics` fundamental, check video view data daily:

- Who watched (by email if viewer was identified, or infer from timing if DM recipient viewed shortly after receiving)
- Watch percentage per viewer
- CTA button clicks

Priority follow-up rules:
- Watched >75% + no CTA click: send a follow-up DM within 24 hours: "Saw you caught the video -- want me to walk through {specific_feature} live?"
- Watched 25-75%: the video lost them mid-way. Note this for future script optimization.
- Not watched after 48 hours: the DM text did not compel them to click. Test a different intro angle.

## Output

- Personalized Loom videos recorded for each prospect in the batch
- LinkedIn DMs sent with embedded video links
- CRM records updated with engagement data and deal stage
- Priority follow-up queue based on video watch behavior

## Triggers

Run daily. Process 5-10 new prospects through the engagement warm-up each day, resulting in 5-10 video DMs per day (to prospects who completed the 3-5 day warm-up). Total daily time: 45-60 minutes (15 min engagement, 30-45 min recording + sending).
