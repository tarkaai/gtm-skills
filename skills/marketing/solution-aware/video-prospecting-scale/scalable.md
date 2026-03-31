---
name: video-prospecting-scale-scalable
description: >
  Video Prospecting at Scale — Scalable Automation. Scale AI-generated video
  outreach to 400+ videos/month with automated batch generation pipelines,
  multi-channel cadences (email + LinkedIn video DMs), A/B testing of video
  variants, and full-funnel PostHog dashboards.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social"
level: "Scalable Automation"
time: "60 hours over 3 months"
outcome: ">=5% response rate at 400+ AI-generated videos/month sustained over 3 months"
kpis: ["Monthly video volume", "Response rate", "Cost per meeting", "Video-to-meeting conversion rate", "Automation efficiency"]
slug: "video-prospecting-scale"
install: "npx gtm-skills add marketing/solution-aware/video-prospecting-scale"
drills:
  - follow-up-automation
  - tool-sync-workflow
  - ab-test-orchestrator
  - linkedin-outreach
---

# Video Prospecting at Scale — Scalable Automation

> **Stage:** Marketing -> Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social

## Outcomes

Scale AI-generated video outreach from 100 (Baseline) to 400+ videos per month. Build fully automated pipelines: prospect enrichment triggers video generation triggers email campaign launch triggers engagement-based follow-up. Add LinkedIn video DM as a parallel channel. Run systematic A/B tests on video length, script structure, CTA placement, subject lines, and ICP segments. The founder's involvement drops to reviewing weekly dashboards and quarterly template re-recordings.

**Pass threshold:** >=5% response rate at 400+ AI-generated videos per month, sustained for 3 consecutive months.

## Leading Indicators

- Video generation pipeline runs end-to-end without manual intervention (Clay -> AI video platform -> Instantly -> follow-up routing)
- Weekly video volume reaches 100+ without proportional increase in founder time
- A/B test results identify at least 2 winning variants that improve response rate by >10% each
- LinkedIn video DM channel produces meetings at a measurable rate (any positive signal counts)
- Cost per meeting from video outreach trends downward month over month
- Automation error rate (failed video generations, broken workflows) stays below 5%

## Instructions

### 1. Build the automated video generation pipeline

Extend the the ai video batch generation workflow (see instructions below) drill into a fully automated weekly pipeline via n8n:

**Pipeline stages:**
1. **Monday 6am — Prospect sourcing:** n8n triggers Clay to pull 100 new prospects matching ICP criteria. Clay enriches each with signals and generates per-prospect video scripts via AI formula.
2. **Monday 8am — Video generation:** n8n reads the enriched Clay table, submits video generation requests to Sendspark/Tavus/HeyGen. Receives webhook callbacks as videos complete.
3. **Monday 2pm — Campaign launch:** n8n exports the prospect + video mapping to Instantly. Creates a new campaign (or adds to an existing weekly campaign). Sends begin on Tuesday morning.
4. **Ongoing — Engagement routing:** The `video-engagement-follow-up` workflow (built at Baseline) runs continuously, routing high/medium/low engagement prospects into appropriate follow-up paths.

Set up error handling: if video generation fails for a prospect, skip that prospect and add to a retry queue. If >10% of a batch fails, alert via Slack for human investigation.

### 2. Connect the full tool stack

Run the `tool-sync-workflow` drill to build n8n sync workflows connecting:

- **Instantly -> Attio:** Email open, click, reply events update the Attio contact record in real-time
- **Video platform -> Attio:** Video view percentage and CTA clicks sync to Attio custom fields
- **Instantly -> PostHog:** All email events fire as PostHog events for funnel analysis
- **Attio -> PostHog:** Deal stage changes fire as PostHog events for pipeline attribution
- **LinkedIn activity -> Attio:** Connection accepts, message replies logged on the contact record

No data should be siloed in a single tool. Every touchpoint appears in both PostHog (for analysis) and Attio (for sales context).

### 3. Add LinkedIn video DMs as a parallel channel

Run the `linkedin-outreach` drill adapted for video:

1. For prospects who have not responded to email after 7 days, send a LinkedIn connection request
2. On connection accept, send a short text message referencing the video: "Hey {first_name}, I sent you a 60-second video about {pain_point} last week. Here's the link in case it got buried: {video_share_url}"
3. If no connection after 14 days, send an InMail with the video link (requires LinkedIn Sales Navigator)
4. Log all LinkedIn touchpoints in Attio and PostHog

Coordinate timing: LinkedIn touches should not overlap with active email sequences for the same prospect. Use Attio's `last_email_touch_date` field as a guard.

### 4. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill. Set up experiments on:

- **Video length:** 45s vs 60s vs 90s (generate 3 template variants)
- **Script structure:** Pain-first vs proof-first vs question-first opening hooks
- **Personalization depth:** Name-only (Sendspark) vs full custom script (Tavus/HeyGen)
- **Email subject lines:** "Recorded something for you" vs "{first_name}, 60 seconds" vs "Quick video about {pain_point}"
- **CTA placement:** End-of-video only vs mid-video + end
- **Send timing:** Tuesday 9am vs Thursday 8am vs Monday 11am

Use PostHog feature flags to randomly assign each prospect batch to control or variant. Run each test for a minimum of 100 sends per variant (200 total) before declaring a winner. Implement winners immediately and start the next experiment.

### 5. Build the performance dashboard

Run the `follow-up-automation` drill to ensure the pipeline handles at scale:

Create a PostHog dashboard with panels:
- **Volume:** Videos generated/sent this week vs last 4-week average
- **Funnel:** video_sent -> email_opened -> thumbnail_clicked -> video_viewed -> replied -> meeting_booked (with conversion rates at each step)
- **A/B test status:** Active experiments, current sample sizes, preliminary results
- **Channel comparison:** Email-only vs email+LinkedIn vs LinkedIn-only response rates
- **Cost efficiency:** Cost per video, cost per response, cost per meeting (trending over time)
- **ICP performance:** Response rate by company size, industry, role, funding stage

Set guardrails: alert via Slack if response rate drops below 3% (40% below target) for any week, or if video generation error rate exceeds 10%.

### 6. Scale volume monthly

- **Month 1:** 100-200 videos/month. Validate the automated pipeline works end-to-end.
- **Month 2:** 200-400 videos/month. Implement A/B test winners. Add LinkedIn channel.
- **Month 3:** 400+ videos/month. Optimize based on 3 months of data. All winning variants in production.

Monitor cost per meeting as volume scales. If cost per meeting increases by >30% as volume grows, the ICP list is diluting -- tighten targeting criteria before scaling further.

### 7. Evaluate against threshold

After 3 months, measure:

- **Response rate:** >=5% average across all months at 400+ videos/month
- **Consistency:** No single month below 4% response rate
- **Efficiency:** Cost per meeting is equal to or lower than Month 1

If PASS: Proceed to Durable. Document the winning pipeline configuration, A/B test winners, and optimal ICP segments.

If FAIL: Diagnose:
- Volume scaling caused quality drop: Tighten ICP criteria, reduce volume to the level where quality holds
- A/B tests produced no winners: The play may have a low ceiling -- check if text-only outperforms at this volume
- LinkedIn channel underperforming: Drop it and reallocate effort to email optimization
- Cost per meeting increasing: AI video costs too high for ROI -- evaluate switching platforms or returning to Loom for highest-priority prospects only

## Time Estimate

- Pipeline automation setup (n8n workflows): 12 hours
- Tool sync configuration: 6 hours
- LinkedIn video DM setup: 4 hours
- A/B test design and implementation: 8 hours
- Dashboard configuration: 4 hours
- Monthly monitoring and optimization (3 months): 20 hours total
- Template re-recording (if A/B tests require): 2 hours
- Evaluation and documentation: 4 hours
- **Total: ~60 hours over 3 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Sendspark or Tavus | AI-personalized video generation at volume | Sendspark $99/mo (Growth) or Tavus $199/mo (Business) — [sendspark.com](https://www.sendspark.com), [tavus.io/pricing](https://www.tavus.io/pricing) |
| Instantly | Cold email sequences at scale | $97/mo (Hypergrowth: 25K emails) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Clay | Automated enrichment + AI script generation | $185-495/mo (Launch-Growth) — [clay.com/pricing](https://www.clay.com/pricing) |
| PostHog | Event tracking, funnels, A/B testing | Free (1M events/mo) or $0.00031/event — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | End-to-end pipeline automation | Free (self-hosted) or $24/mo (cloud) — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | CRM for deal tracking + multi-channel history | Free (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |
| LinkedIn Sales Navigator | LinkedIn outreach + InMail | $99/mo — [linkedin.com/sales](https://www.linkedin.com/sales/) |
| Cal.com | Booking links for video CTAs | Free or $12/mo — [cal.com/pricing](https://cal.com/pricing) |

**Estimated Scalable cost:** ~$400-900/mo (video platform + Instantly Hypergrowth + Clay Growth + LinkedIn Sales Nav)

## Drills Referenced

- the ai video batch generation workflow (see instructions below) — automated weekly pipeline: enrich prospects, generate AI videos, launch campaigns
- `follow-up-automation` — n8n workflows for engagement-based follow-up routing at scale
- `tool-sync-workflow` — connect Instantly, video platform, Attio, PostHog, and LinkedIn into a unified data layer
- `ab-test-orchestrator` — systematic experiments on video length, scripts, subjects, timing, and personalization depth
- `linkedin-outreach` — parallel channel: video DMs and InMails for non-email-responders
