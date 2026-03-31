---
name: linkedin-video-dms-smoke
description: >
  LinkedIn Video DMs — Smoke Test. Record personalized 60-second Loom videos and send them via
  LinkedIn DMs to solution-aware prospects. Validate that video DMs produce higher engagement than
  text-only outreach with a 30-prospect manual test.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Social"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=8% response rate from 30 video DMs in 1 week"
kpis: ["Response rate", "Video watch rate", "Watch completion percentage", "Time to first response"]
slug: "linkedin-video-dms"
install: "npx gtm-skills add marketing/solution-aware/linkedin-video-dms"
drills:
  - icp-definition
  - build-prospect-list
  - threshold-engine
---

# LinkedIn Video DMs — Smoke Test

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Social

## Outcomes

Prove that personalized video DMs on LinkedIn generate responses from solution-aware prospects. A response rate of >=8% from 30 video DMs validates that video-in-DM is a viable channel worth systematizing. This is a manual, founder-executed test with no automation and no recurring cost beyond Loom Business.

## Leading Indicators

- Video watch rate >=40% (prospects are clicking and watching the Loom link in the DM)
- Average watch completion >=60% (the video script holds attention past the halfway point)
- At least 1 meeting booked directly from a Loom CTA click (proves the full funnel works end-to-end)
- Positive reply sentiment on >=50% of responses (responses are engagement, not "stop messaging me")

## Instructions

### 1. Define ICP and build a 30-prospect list

Run the `icp-definition` drill to document your Ideal Customer Profile for this play. Focus on solution-aware prospects: people who know the category of solution they need but have not chosen a vendor. Indicators: they post about the problem space, follow competitors, or have recently adopted adjacent tools.

Run the `build-prospect-list` drill to source 30-40 prospects matching this ICP from Clay. For each prospect, ensure you have: first name, company name, role, LinkedIn profile URL, and one specific trigger signal (recent post topic, funding event, job change, hiring activity). Export to Attio CRM.

### 2. Execute 3-5 day engagement warm-up (manual)

For each prospect, spend 3-5 days engaging with their LinkedIn content before sending the video DM:

- **Day 1**: Like 2-3 of their recent posts.
- **Day 2**: Leave a substantive comment on one post. Add a genuine insight or question. No product mentions.
- **Day 3-4**: Like 1-2 more posts. Reply if they respond to your comment.
- **Day 5**: Record and send the video DM (step 3).

Stagger prospects so you start 5-6 per day. After 5 days of warm-up, you will have a steady flow of prospects ready for video DMs.

**Human action required:** All engagement is manual. Spend 15 minutes daily on warm-up engagement across your prospect batch.

### 3. Record personalized Loom videos

For each prospect reaching Day 5 of warm-up, record a 60-second Loom video:

1. Open the prospect's LinkedIn profile on your screen (visible in the recording as personalization proof).
2. Start Loom recording (camera + screen).
3. Follow this script structure:
   - **Opening (5s):** "Hey {first_name}, {your_name} here."
   - **Hook (10s):** Reference their specific content or signal: "I saw your post about {topic} / noticed {company} just {signal}..."
   - **Connection (15s):** Bridge to their pain: "That usually means {implication}. We have been working on exactly that with companies like {similar_company}."
   - **Proof (15s):** One concrete result: "{similar_company} went from X to Y in Z weeks."
   - **CTA (10s):** "If that is relevant, there is a link below to grab 15 minutes."
4. Trim dead space. Add CTA button: "Book 15 Minutes" linked to your Cal.com booking URL with UTM params: `?utm_source=loom&utm_medium=linkedin-dm&utm_campaign=smoke-video-dms`.
5. Name the video: `{company}-{firstname}-li-dm-smoke`.

**Human action required:** Record each video. Target pace: 3 minutes per video. A 6-prospect batch takes ~18 minutes.

### 4. Send LinkedIn DMs with video links

For each recorded video, send a LinkedIn DM:

```
Hey {first_name} -- recorded a quick 60-second video for you after seeing your post about {topic}.

No pitch, just a thought on {pain_point_area}: {loom_share_url}

Curious to hear what you think.
```

Rules:
- Keep DM text under 300 characters (excluding URL).
- Send between 8am-11am in prospect's timezone.
- Maximum 10 video DMs per day.
- If not connected: send a connection request with a note referencing their content. Once accepted, send the video DM. Do not use InMail at Smoke level.

**Human action required:** Send each DM manually. Log the send date and Loom URL in Attio.

### 5. Track results manually

For each video DM sent, track in Attio:
- `video_dm_sent`: true
- `video_dm_date`: send date
- `video_loom_url`: Loom share link
- `lead_source`: linkedin-video-dm

Check Loom analytics daily: who watched, watch percentage, CTA clicks. Update Attio:
- `video_watched`: true/false
- `video_watch_pct`: percentage
- `video_cta_clicked`: true/false

For prospects who watched >75% but did not respond, send one text-only follow-up DM 3 days later:

```
Hey {first_name} -- not sure if you caught the video. Quick summary: {one_sentence_value_prop}.

Worth a 15-min chat? {cal_link}
```

### 6. Evaluate against pass threshold

Run the `threshold-engine` drill after 1 week. Pull data from Attio:
- Total video DMs sent (target: 30)
- Responses received (target: >=3, which is >=8% of 30)
- Video watch rate (leading indicator)
- Meetings booked (bonus metric)

**PASS (>=8% response rate):** Proceed to Baseline. Document which ICP segments, trigger signals, and video hooks produced the best responses.

**FAIL (<8% response rate):** Diagnose:
- If watch rate <20%: the DM text is not compelling prospects to click. Rewrite the DM intro.
- If watch rate >40% but response rate <8%: the video content is not converting. Revise the script -- likely the proof point or CTA is weak.
- If prospects are not connected and connection requests are ignored: target a different ICP segment or try warm-up engagement for longer.

## Time Estimate

- ICP definition and list building: 1.5 hours
- Engagement warm-up: 15 min/day for 7 days = 1.75 hours
- Video recording: 30 prospects x 3 min = 1.5 hours
- DM sending and tracking: 30 min/day for 5 days = 2.5 hours (overlaps with warm-up)
- Evaluation: 30 minutes
- **Total: ~6 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom Business | Record personalized videos with CTA buttons and analytics | $12.50/creator/mo (annual) |
| LinkedIn (free) | Send DMs to connections | Free |
| Clay | Prospect enrichment and signal detection | $185/mo (Launch plan) |
| Attio | CRM tracking | Included in standard stack |
| Cal.com | Booking link for video CTAs | Included in standard stack |

**Play-specific cost at Smoke level:** ~$12.50/mo (Loom Business). Clay and Attio are standard stack costs shared across plays.

## Drills Referenced

- `icp-definition` — define your Ideal Customer Profile and buyer persona for targeting
- `build-prospect-list` — source and enrich 30-40 prospects from Clay into Attio
- `threshold-engine` — evaluate pass/fail against the 8% response rate threshold
