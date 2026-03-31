---
name: comment-to-dm-play-baseline
description: >
  Comment-to-DM Play — Baseline Run. First always-on automation: systematically comment on ICP prospects'
  LinkedIn posts daily, track engagement in CRM, and convert warm prospects to DM conversations with
  full analytics tracking.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Social"
level: "Baseline Run"
time: "15 hours over 4 weeks"
outcome: "≥ 10 DM conversations and ≥ 4 meetings booked over 4 weeks with full funnel attribution"
kpis: ["Author reply rate", "DM-to-reply conversion", "Comment-to-meeting rate", "Days from first comment to meeting"]
slug: "comment-to-dm-play"
install: "npx gtm-skills add marketing/problem-aware/comment-to-dm-play"
drills:
  - comment-to-dm-cadence
  - posthog-gtm-events
  - linkedin-lead-capture
---

# Comment-to-DM Play — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Social

## Outcomes

Run the comment-to-DM motion continuously for 4 weeks with structured cadence tracking, CRM logging, and analytics. Prove the motion is repeatable: consistent commenting produces consistent DM opportunities, which produce consistent meetings. The agent manages discovery, tracking, and reporting while the founder focuses on commenting and DMs.

## Leading Indicators

- Steady comment volume: ≥ 25 comments per week across target list
- Author reply rate holding at ≥ 15% over 4 weeks
- Prospect cadence pipeline: ≥ 10 prospects in warming/warm stage at any given time
- DM acceptance rate: ≥ 40% of DMs get a substantive reply
- Profile views sustained at 2x pre-play baseline

## Instructions

### 1. Set up the comment-to-DM cadence system

Run the `comment-to-dm-cadence` drill to establish the full tracking system in Attio:

1. Add the `comment_dm_stage` custom field to Person records (values: cold, warming, warm, dm-ready, dm_sent, conversation, meeting_booked)
2. Add tracking fields: `comment_touch_count`, `last_comment_date`, `first_comment_date`, `dm_sent_date`
3. Import your Smoke-level target list (expand to 30-40 prospects)
4. Set each prospect's initial stage based on Smoke results (prospects you already engaged are at least "warming")

### 2. Configure analytics tracking

Run the `posthog-gtm-events` drill to set up the comment-to-DM event taxonomy in PostHog:

| Event | Properties | When Fired |
|-------|-----------|------------|
| `comment_posted` | prospect_name, prospect_tier, post_url, comment_strategy, author_name | After posting each comment |
| `author_reply_received` | prospect_name, post_url, reply_text | When author replies to your comment |
| `prospect_stage_advanced` | prospect_name, from_stage, to_stage, touch_count | When prospect moves to next cadence stage |
| `dm_sent` | prospect_name, dm_type (opening, follow_up, meeting_ask), referenced_post | When DM is sent |
| `dm_reply_received` | prospect_name, reply_sentiment (positive, neutral, negative) | When prospect replies to DM |
| `meeting_booked` | prospect_name, source_post, days_from_first_comment, total_touches | When meeting is booked |

Fire these events via n8n webhooks triggered by CRM updates, or log them manually during daily tracking.

### 3. Execute the daily cadence

Each business day:

**Morning (20-30 min):**
1. The agent runs `prospect-content-discovery` (Option B -- semi-automated via Taplio) to surface today's commentable posts
2. The founder reviews the queue and selects 5-8 posts
3. The agent drafts comments using the `comment-crafting` drill strategies
4. The founder reviews, edits for voice, and posts each comment
5. The agent logs each comment in Attio (increment touch count, update last_comment_date) and fires `comment_posted` events

**Afternoon (10 min):**
6. Check for author replies on today's comments
7. Reply to any authors who responded (keep conversations going)
8. Log replies and fire `author_reply_received` events
9. Update prospect stages: if a prospect now meets DM-ready criteria, advance them

**DM window (as signals appear):**
10. When a prospect reaches DM-ready stage, the agent drafts a DM using the `comment-to-dm-cadence` drill templates
11. The founder reviews and sends the DM
12. Log the DM in Attio, fire `dm_sent` event

### 4. Set up lead capture and enrichment

Run the `linkedin-lead-capture` drill to build the system that enriches DM-ready prospects:

1. When a prospect reaches DM-ready or conversation stage, trigger Clay enrichment: company data, email, technographics
2. Create or update the full lead record in Attio with enriched data
3. Tag the lead with `lead_source = comment-to-dm` and `first_touch_post` = the first post you commented on
4. Track the full attribution chain: first comment date -> DM date -> meeting date -> deal date

### 5. Weekly review and pipeline management

Every Friday (30 min):
1. Review the full prospect pipeline in Attio: how many at each stage (cold, warming, warm, dm-ready, conversation)
2. Identify stalled prospects (no new engagement in 10+ days) and decide: re-engage or deprioritize
3. Add 5-10 new prospects to the target list to replace churned ones
4. Review the week's metrics: comments posted, author replies, DMs sent, meetings booked
5. Note what comment strategies worked best this week

### 6. Evaluate against threshold

After 4 weeks, measure: ≥ 10 DM conversations started AND ≥ 4 meetings booked. Also evaluate the funnel health: is the pipeline filling with new prospects, or are you exhausting your target list?

If PASS, proceed to Scalable. If FAIL, diagnose the funnel stage where conversion breaks down and address it before re-running.

## Time Estimate

- Cadence setup (Attio + PostHog): 2 hours
- Daily commenting and DMs (20 days x 30 min): 10 hours
- Weekly reviews (4 x 30 min): 2 hours
- Lead capture setup: 1 hour
- **Total: ~15 hours over 4 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn (free or Premium) | Commenting, DMs | Free or $29.99/mo (https://www.linkedin.com/premium/) |
| Taplio | Feed monitoring, prospect post tracking | $49/mo (https://taplio.com/pricing) |
| PostHog | Event tracking, funnel analytics | Free up to 1M events (https://posthog.com/pricing) |
| Attio | CRM, prospect cadence tracking | Free up to 3 users (https://attio.com/pricing) |
| Clay | Prospect enrichment | $149/mo Explorer plan (https://clay.com/pricing) |
| n8n | Automation workflows | Free self-hosted or $20/mo cloud (https://n8n.io/pricing) |

## Drills Referenced

- `comment-to-dm-cadence` — the full warming-to-DM conversion sequence with stage tracking
- `posthog-gtm-events` — set up the event taxonomy for comment-to-DM tracking
- `linkedin-lead-capture` — enrich and route DM-ready prospects to CRM pipeline
