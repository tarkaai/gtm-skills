---
name: outbound-with-short-video-scalable
description: >
  Outbound With Short Video — Scalable Automation. Scale personalized Loom video
  outreach to 200+ prospects/month with automated enrichment-to-send pipelines,
  segment-level video templates, A/B testing of video elements, and fully automated
  engagement-based follow-up. Find the 10x multiplier.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: ">=10% video completion rate AND >=12 meetings booked over 2 months with <=30 minutes of manual effort per meeting booked"
kpis: ["Video completion rate", "Thumbnail click-through rate", "Meetings booked from video", "Video-to-meeting conversion rate", "Minutes of recording per meeting booked", "Cost per meeting"]
slug: "outbound-with-short-video"
install: "npx gtm-skills add marketing/solution-aware/outbound-with-short-video"
drills:
  - enrich-and-score
  - video-prospecting-outreach
  - video-engagement-follow-up
  - follow-up-automation
  - ab-test-orchestrator
---

# Outbound With Short Video — Scalable Automation

> **Stage:** Marketing -> Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email

## Outcomes

Scale video outreach to 200+ prospects per month without proportional increase in recording time. The 10x multiplier comes from three strategies: (1) segment-level video templates that cover ICP clusters instead of individual prospects, (2) automated enrichment-to-send pipelines that eliminate manual prospect prep, and (3) A/B testing that systematically improves every element of the video outreach funnel. Fully automated follow-up routing handles all post-send workflows.

**Pass threshold:** >=10% video completion rate AND >=12 meetings booked over 2 months AND <=30 minutes of manual effort per meeting booked.

## Leading Indicators

- Segment-level videos achieve >=80% of the completion rate of fully personalized videos (validating the scale strategy)
- A/B test on video length identifies a statistically significant winner (shorter or longer)
- Automated follow-up produces >=50% of meetings without manual intervention
- Enrichment pipeline runs end-to-end without human input (Clay -> scoring -> Instantly -> Loom tracking -> follow-up)
- Cost per meeting from video outreach is <=2x cost per meeting from text-only outreach (premium justified by deal quality)
- Reply sentiment from video outreach is more positive than text-only (video builds trust)

## Instructions

### 1. Build the automated enrichment-to-outreach pipeline

Run the `enrich-and-score` drill to create a Clay table that automatically:

1. Pulls new prospects matching ICP criteria weekly from Apollo/LinkedIn Sales Navigator
2. Runs the enrichment waterfall: firmographics, contact details, technology signals
3. Scores each prospect on ICP fit (weight: company fit 40%, contact fit 35%, timing signals 25%)
4. Assigns each prospect to an ICP segment (e.g., "Series-A-DevTools-CTO", "Growth-Stage-Fintech-VP-Eng")
5. Generates a one-line video hook per prospect using Clay AI: "I noticed {company} {signal} -- {connection to value prop}"
6. Pushes qualified prospects (score >70) to Attio tagged with segment and campaign batch

This pipeline should produce 50-75 qualified prospects per week without manual input.

### 2. Create segment-level video templates

Instead of recording one video per prospect (the Smoke/Baseline approach), create one video per ICP segment. This is the core scalability lever.

For each segment, record a 60-90 second video using the `video-prospecting-outreach` drill:

- **Opening:** "Hey -- if you're a {role} at a {company_type} company, this is for you."
- **Hook:** Reference the common pain point for this segment: "{segment_pain_point} is something I hear from every {role} I talk to..."
- **Value prop:** How your product solves it for this specific segment
- **Proof:** A customer story from a similar company in this segment
- **CTA:** "Link below to grab 15 minutes if this resonates."

Record 5-8 segment videos (one per ICP cluster). These replace 200+ individual recordings.

For the top 10-20 highest-scored prospects each month, still record fully personalized videos. These are your "white glove" tier.

### 3. Build the email campaign with personalized framing

Using `video-prospecting-outreach`, construct the email campaigns:

- The email subject line and first line are still personalized per prospect (using Clay merge fields)
- The video is segment-level (same Loom link for all prospects in that segment)
- The context sentence below the thumbnail is personalized using Clay AI hooks

This hybrid approach gives the FEEL of personalization (their name, their company, their signal in the email) with the SCALE of segment videos.

**Email structure:**
```
Subject: {first_name}, 60 seconds on {pain_point_keyword}

Hey {first_name},

{clay_ai_hook_sentence}

I recorded a quick video that covers exactly this:

[Segment-level Loom GIF thumbnail]

Worth a look?

{your_name}
```

### 4. Deploy fully automated follow-up

Run the `video-engagement-follow-up` drill and the `follow-up-automation` drill together to create a comprehensive post-send automation:

**Automated sequences:**
- High engagement (>75% watched, no CTA click): auto-send personal follow-up from founder email within 24 hours
- Medium engagement (25-75% watched): accelerate follow-up to next day
- Thumbnail clicked but didn't watch full video: send a shorter "2-minute summary" text email
- Positive reply: route to Attio hot deal, notify founder on Slack
- Meeting booked via CTA: auto-confirm, add to Attio pipeline, send prep doc
- Negative reply: mark in Attio, suppress from all future campaigns
- No engagement after full sequence: add to 30-day re-engagement list

**Cross-channel extension:**
- For prospects who watched >50% but didn't reply or book: trigger a LinkedIn connection request with a message referencing the video topic (not the video itself)

### 5. Launch A/B testing program

Run the `ab-test-orchestrator` drill to systematically test video outreach elements. Run one test at a time, minimum 100 prospects per variant:

**Priority test sequence:**

1. **Video length:** 45s vs 90s vs 120s. Measure: completion rate + meeting rate.
2. **Email subject line:** "Quick video for {first_name}" vs "{first_name}, 60 seconds on {pain_point}" vs "Recorded this for {company}". Measure: open rate + thumbnail click rate.
3. **Personalization level:** Fully personalized video vs segment video. Measure: completion rate + meeting rate + recording time per meeting.
4. **Thumbnail type:** Animated GIF vs static screenshot with play button. Measure: thumbnail click rate.
5. **CTA placement:** End only vs mid-video + end. Measure: CTA click rate + meeting rate.

Document each test result. Implement winners permanently before starting the next test.

### 6. Scale to full volume

With the pipeline, segment videos, and A/B test winners in place:

- Week 1-2: Send to 50 prospects/week (ramp up)
- Week 3-4: Send to 75-100 prospects/week
- Month 2: Send to 100-125 prospects/week (200-500/month)

Monitor Instantly deliverability daily during scale-up. If bounce rate exceeds 3% or spam complaints appear, reduce volume and investigate.

### 7. Evaluate against threshold

After 2 months, measure:

- **Video completion rate:** >=10% of videos sent were watched >=75%
- **Meetings booked:** >=12 total from video outreach
- **Efficiency:** <=30 minutes of manual effort per meeting booked (recording time + manual follow-up / total meetings)

Also evaluate:
- Segment videos vs personalized videos: which produces more meetings per hour of effort?
- A/B test winners documented and implemented?
- Pipeline value from video-sourced deals vs text-sourced deals

If PASS: Proceed to Durable. Document the full automated pipeline, winning segment videos, and A/B test results.

If FAIL: Diagnose:
- Completion rate dropped at scale: segment videos less compelling than personalized. Record more segment variants or return to more personalized approach for top-tier prospects.
- Meetings per month plateau: run more aggressive A/B tests on subject lines and follow-up sequences.
- Manual effort too high: automate more of the follow-up; create more segment videos to reduce white-glove recordings.

## Time Estimate

- Enrichment pipeline setup (Clay + n8n): 4 hours
- Segment video recording (8 segments x 15 min each): 2 hours
- White-glove personalized recordings (~40 across 2 months): 3 hours
- Email campaign setup and iteration: 4 hours
- Follow-up automation workflow building: 4 hours
- A/B test design and analysis: 4 hours
- Weekly monitoring and optimization: 8 hours (1hr/week x 8 weeks)
- Pipeline management and deal routing: 8 hours
- Evaluation and documentation: 3 hours
- **Total: ~40 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom | Record segment and personalized videos | $12.50/user/mo (Business) — [loom.com/pricing](https://www.loom.com/pricing) |
| Instantly | Cold email sequences at scale | $97/mo (Hypergrowth: 100K emails, A/B testing) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Clay | Automated enrichment pipeline + AI personalization | $185-495/mo (Launch or Growth) — [clay.com/pricing](https://www.clay.com/pricing) |
| PostHog | Event tracking, funnels, A/B test analysis | Free (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation: enrichment pipeline, follow-up routing | Free (self-hosted) or $24/mo (cloud) — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | CRM deal pipeline tracking | Free (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |
| Cal.com | Video CTA booking links | Free or $12/mo — [cal.com/pricing](https://cal.com/pricing) |
| Apollo | Prospect sourcing for enrichment pipeline | Free (limited) or $49/mo — [apollo.io/pricing](https://www.apollo.io/pricing) |

**Estimated Scalable cost:** ~$350-800/mo (Instantly Hypergrowth + Clay Growth + Loom Business + supporting tools)

## Drills Referenced

- `enrich-and-score` — automated enrichment pipeline with scoring for prospect prioritization
- `video-prospecting-outreach` — record segment and personalized Loom videos, build email campaigns
- `video-engagement-follow-up` — automated follow-up routing based on video watch behavior
- `follow-up-automation` — cross-channel follow-up automation including LinkedIn
- `ab-test-orchestrator` — systematic testing of video length, subject lines, personalization level, and CTA placement
