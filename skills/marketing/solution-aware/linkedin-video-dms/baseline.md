---
name: linkedin-video-dms-baseline
description: >
  LinkedIn Video DMs — Baseline Run. First always-on LinkedIn video DM operation with structured
  workflows, PostHog event tracking, and engagement-based follow-up routing. Scale from 30 to 100
  video DMs over 2 weeks with repeatable daily cadence.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=10% response rate from 100 video DMs over 2 weeks"
kpis: ["Response rate", "Video watch rate", "Watch-to-response ratio", "Meeting booking rate", "Cost per meeting"]
slug: "linkedin-video-dms"
install: "npx gtm-skills add marketing/solution-aware/linkedin-video-dms"
drills:
  - posthog-gtm-events
  - video-engagement-follow-up
---

# LinkedIn Video DMs — Baseline Run

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Social

## Outcomes

Prove that LinkedIn video DMs produce repeatable results at steady-state volume. Move from ad-hoc manual sending (Smoke) to a structured daily cadence of 7-10 video DMs with PostHog event tracking and engagement-based follow-up routing. A >=10% response rate from 100 video DMs over 2 weeks validates that the workflow is repeatable and the economics justify scaling.

## Leading Indicators

- Video watch rate >=50% (DM intro copy is compelling enough that half of recipients click)
- Average watch completion >=65% (script improvements from Smoke are holding attention)
- Watch-to-response ratio >=20% (prospects who watch are engaging back)
- At least 3 meetings booked from Loom CTA clicks or DM replies (full funnel conversion)
- Positive sentiment on >=60% of responses

## Instructions

### 1. Configure the LinkedIn video DM outreach workflow

Run the the linkedin video dm outreach workflow (see instructions below) drill to set up the structured daily workflow. This drill covers:

- Prospect enrichment preparation in Clay with video hook generation
- 3-5 day pre-DM engagement warm-up sequence on LinkedIn
- Batch video recording with standardized script template
- DM sending with embedded Loom links
- Follow-up sequences based on video engagement data
- CRM logging in Attio at every step

Configure the drill for Baseline volume: 7-10 new prospects entering the warm-up pipeline daily, producing 7-10 video DMs per day after the initial 5-day ramp.

### 2. Set up PostHog event tracking

Run the `posthog-gtm-events` drill to define and implement the event taxonomy for this play. Configure these events:

| Event | Trigger | Properties |
|-------|---------|------------|
| `video_dm_warmup_started` | First engagement action on prospect's content | prospect_id, icp_segment |
| `video_dm_recorded` | Loom video saved and named | prospect_id, video_id, video_length_seconds |
| `video_dm_sent` | LinkedIn DM delivered with Loom link | prospect_id, video_id, message_variant, day_of_week, time_of_day |
| `video_dm_watched` | Prospect viewed the Loom video | prospect_id, video_id, watch_percentage, cta_clicked |
| `video_dm_replied` | Prospect responded to the DM | prospect_id, sentiment (positive/neutral/negative), days_since_send |
| `video_dm_meeting_booked` | Meeting scheduled from CTA click or DM reply | prospect_id, source (cta_click/dm_reply), deal_value |
| `video_dm_followup_sent` | Text follow-up DM sent after no response | prospect_id, followup_number (1 or 2), followup_variant |

Events flow into PostHog via n8n webhooks triggered by manual logging in Attio (at Baseline, event capture is semi-manual -- the agent logs the event when updating Attio).

### 3. Launch the engagement-based follow-up system

Run the `video-engagement-follow-up` drill adapted for LinkedIn DMs instead of email. Configure the routing logic:

**High engagement (watched >75%):**
- If CTA clicked: monitor for Cal.com booking. If no booking within 24 hours, send a follow-up DM: "Saw you caught the video, {first_name}. Want me to walk through {feature} live? Here are a few times: {cal_link}"
- If no CTA click: send a follow-up DM referencing the video content: "Hey {first_name} -- curious what you thought about the {topic} angle from the video. Worth a quick chat?"

**Medium engagement (watched 25-75%):**
- Video lost them mid-way. Send a text-only follow-up 3 days later with a different angle -- lead with the proof point instead of the problem statement.

**Low engagement (watched <25%) or never watched:**
- The DM text or timing did not land. Wait 5 days, then send one text-only follow-up with no video reference:
  ```
  Hey {first_name} -- saw your recent post about {topic}. We helped {similar_company} achieve {result}. Worth 15 minutes? {cal_link}
  ```
- If still no response after 10 days total, route to email channel via `cold-email-sequence` drill (different channel, different approach).

### 4. Execute daily for 2 weeks

Run the workflow daily:

- **Morning (15 min):** Engagement warm-up actions for prospects in Days 1-4 of the pipeline.
- **Mid-morning (45 min):** Record 7-10 videos for prospects reaching Day 5. Send DMs.
- **Afternoon (15 min):** Check Loom analytics. Send follow-ups based on engagement routing. Update Attio records. Log PostHog events.

After 5 days of ramp-up, the pipeline reaches steady state: 7-10 video DMs going out daily, with prospects at every stage of the warm-up and follow-up pipeline simultaneously.

### 5. Analyze and evaluate at week 2

Pull PostHog data and Attio records:

- Total video DMs sent (target: 100)
- Response rate (target: >=10%)
- Video watch rate (segment by ICP tier and time of send)
- Watch-to-response ratio (measures video quality independent of DM delivery)
- Meetings booked and pipeline value created
- Cost per meeting: (Loom Business + LinkedIn time allocation) / meetings booked

**PASS (>=10% response rate):** Proceed to Scalable. Document:
- Best-performing ICP segments (which prospects respond most to video DMs?)
- Best video script patterns (which hooks produce highest watch completion?)
- Optimal send timing (day of week and time of day with highest watch rates)
- Follow-up effectiveness (which engagement-based branch converts best?)

**FAIL (<10% response rate):** Diagnose using the funnel data:
- Watch rate <30%: DM text is not driving clicks. Test 3 DM intro variants over next week.
- Watch rate >50% but response <10%: video is engaging but CTA is weak. Shorten videos to 45 seconds and strengthen the proof point.
- Follow-up producing most responses: your initial DM timing or messaging is off. Lean into the follow-up angle as the primary message.

## Time Estimate

- Drill setup and PostHog configuration: 2 hours
- Daily engagement warm-up: 15 min/day x 10 working days = 2.5 hours
- Daily video recording + sending: 45 min/day x 10 working days = 7.5 hours
- Daily follow-up and tracking: 15 min/day x 10 working days = 2.5 hours
- Weekly analysis: 1 hour x 2 = 2 hours
- Final evaluation: 1.5 hours
- **Total: ~18 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom Business | Personalized video recording with CTAs and analytics | $12.50/creator/mo (annual) — [pricing](https://www.atlassian.com/software/loom/pricing) |
| LinkedIn Sales Navigator Core | InMail for unconnected prospects, advanced search filters | $79.99/mo (annual) — [pricing](https://business.linkedin.com/sales-solutions/compare-plans) |
| Clay | Prospect enrichment and AI video hook generation | $185/mo (Launch plan) — [pricing](https://university.clay.com/docs/plans-and-billing) |
| PostHog | Event tracking and funnel analytics | Free up to 1M events/mo — [pricing](https://posthog.com/pricing) |
| Attio | CRM logging and deal tracking | Included in standard stack |
| Cal.com | Booking links for video CTAs | Included in standard stack |

**Play-specific cost at Baseline:** ~$92/mo (Loom Business $12.50 + LinkedIn Sales Navigator Core $79.99). Clay and PostHog are standard stack costs.

## Drills Referenced

- the linkedin video dm outreach workflow (see instructions below) — structured daily workflow for recording and sending video DMs via LinkedIn
- `posthog-gtm-events` — define and implement event taxonomy for video DM tracking in PostHog
- `video-engagement-follow-up` — route follow-ups based on Loom video watch behavior
