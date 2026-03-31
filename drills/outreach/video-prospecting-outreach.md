---
name: video-prospecting-outreach
description: Record personalized Loom videos for a prospect batch and send via cold email with embedded GIF thumbnails
category: Outreach
tools:
  - Loom
  - Instantly
  - Clay
  - Attio
fundamentals:
  - loom-personalized-outreach
  - loom-embed-in-email
  - loom-analytics
  - instantly-campaign
  - clay-enrichment-waterfall
  - attio-contacts
---

# Video Prospecting Outreach

This drill covers the end-to-end workflow of recording personalized Loom videos for a batch of prospects and sending them via cold email with embedded animated GIF thumbnails. The personalized video approach consistently outperforms text-only cold email on reply rate and meeting conversion because it builds trust and demonstrates effort.

## Input

- Prospect list in Clay or Attio with enrichment data (name, company, role, pain point, recent signal)
- ICP definition (from `icp-definition` drill)
- Loom Business account with CTA buttons enabled
- Instantly account with warmed sending domains
- Cal.com booking link for video CTAs

## Steps

### 1. Prepare prospect enrichment for video scripts

Open your Clay table with the target prospect batch. For each prospect, you need these columns populated:

- First name
- Company name
- Role/title
- One specific pain point or trigger signal (e.g., "just raised Series A", "hiring 5 engineers", "competitor of {customer}")
- Company website URL (for screen share during recording)

Use the `clay-enrichment-waterfall` fundamental to fill gaps. Add a Clay AI formula column that generates a one-sentence video hook for each prospect based on their signal: "I noticed {company} just {signal} -- that usually means {pain_point_connection}."

### 2. Batch-record personalized Loom videos

Using the `loom-personalized-outreach` fundamental, record one video per prospect:

1. Open the prospect's website in your browser
2. Start Loom recording (camera + screen)
3. Follow the 60-90 second template: greeting by name, reference their signal, connect to your value prop, brief proof point, CTA
4. Stop recording, trim, add CTA button linking to Cal.com
5. Name the video: `{company}-{firstname}-{campaign-slug}`
6. Copy the share link

Target pace: 2-3 minutes per video including setup. A 20-prospect batch takes ~50 minutes.

### 3. Build the Loom-to-email mapping

After recording, build a CSV or Clay table column mapping each prospect to their Loom video:

| Prospect Email | First Name | Company | Loom Video ID | Loom Share URL | Loom GIF URL |
|----------------|------------|---------|---------------|----------------|--------------|

The Loom GIF URL format: `https://cdn.loom.com/sessions/thumbnails/{video-id}-with-play.gif`
The Loom share URL format: `https://www.loom.com/share/{video-id}`

Export this mapping for Instantly campaign import.

### 4. Build the email campaign in Instantly

Using the `loom-embed-in-email` fundamental, create the campaign:

**Email 1 (Day 0) -- Video email:**
```
Subject: Quick video for you, {first_name}

Hey {first_name},

I recorded a 60-second video just for you:

[Embedded Loom GIF thumbnail linked to video]

{one-line context from Clay AI hook}

If it resonates, there's a link in the video to grab 15 minutes.

{your_name}
```

**Email 2 (Day 3) -- Text follow-up:**
```
Subject: Re: Quick video for you, {first_name}

Hey {first_name}, did you get a chance to watch the video I sent?

Quick summary: {value_prop_one_liner}.

Happy to walk through it live if helpful — here's my calendar: {cal_link}

{your_name}
```

**Email 3 (Day 7) -- Breakup:**
```
Subject: Re: Quick video for you, {first_name}

{first_name} — I know inboxes are brutal so I'll keep this short.

If {pain_point} isn't a priority right now, no worries at all. But if it is, I'd love 15 minutes to show you what we built for {similar_company}.

Either way, the video is here if you want to watch it later: {loom_share_url}

{your_name}
```

Using the `instantly-campaign` fundamental, upload the prospect CSV with Loom video IDs mapped as merge fields. Set sending schedule to weekdays, 8am-11am in prospect's timezone. Enable open and click tracking.

### 5. Log prospect data in CRM

Using the `attio-contacts` fundamental, update each prospect record in Attio with:
- `video_sent: true`
- `video_loom_url: {share_url}`
- `video_campaign: {campaign_slug}`
- `video_sent_date: {date}`

This ensures the sales team can find and reference the video in follow-up conversations.

### 6. Monitor video engagement

Using the `loom-analytics` fundamental, check video view data daily during the campaign:

- Who watched (by email if viewer was identified)
- Watch percentage per viewer
- CTA button clicks

Priority follow-up rules:
- Watched >75%: HOT -- follow up within 24 hours with a specific meeting request
- Watched 25-75%: WARM -- send the text follow-up (Email 2) immediately instead of waiting
- Watched <25% or did not watch: let the sequence continue on schedule

Update Attio contact records with `video_watched: true`, `video_watch_pct: {percentage}`.

## Output

- Personalized Loom videos recorded for each prospect in the batch
- Cold email campaign launched in Instantly with embedded video thumbnails
- CRM records updated with video engagement data
- Priority follow-up queue based on video watch behavior

## Triggers

Run this drill for each new prospect batch. Typical cadence: 1-2 batches per week of 10-25 prospects each at Smoke/Baseline level, scaling to 50+ per week at Scalable level.
