---
name: linkedin-founder-threads-baseline
description: >
  Founder LinkedIn content — Baseline Run. First always-on cadence: the founder publishes
  3-5 posts per week for 2 weeks with scheduling tools, analytics tracking via Taplio and
  PostHog, and a repeatable lead capture process.
stage: "Marketing > Unaware"
motion: "FounderSocialContent"
channels: "Social"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 5 inbound leads over 2 weeks with repeatable content + engagement process"
kpis: ["Impressions per post", "Engagement rate", "Profile views per week", "Inbound DMs per week", "Leads captured in CRM"]
slug: "linkedin-founder-threads"
install: "npx gtm-skills add marketing/unaware/linkedin-founder-threads"
drills:
  - founder-linkedin-content-batch
  - linkedin-engagement-workflow
  - linkedin-lead-capture
  - posthog-gtm-events
---

# Founder LinkedIn Content — Baseline Run

> **Stage:** Marketing > Unaware | **Motion:** FounderSocialContent | **Channels:** Social

## Outcomes

The founder has a repeatable weekly system: batch-create content on Friday/Monday, schedule via Taplio, run daily engagement, and capture leads into Attio with source attribution. After 2 weeks of consistent posting (6-10 posts total), at least 5 inbound leads are captured in the CRM, proving the process works at a sustainable cadence.

## Leading Indicators

- Week 1 posts match or exceed Smoke-level engagement metrics
- Content batching takes under 1 hour per week (process is efficient)
- Lead capture is happening same-day (not accumulating untracked leads)
- At least 2 leads captured by end of week 1
- Follower growth accelerating (50+ new followers per week)

## Instructions

### 1. Set up Taplio for scheduling and analytics

Sign up for Taplio ($39/mo Starter plan) and connect the founder's LinkedIn account.

Taplio provides:
- Post scheduling with optimal time suggestions
- Per-post analytics (impressions, engagement rate, clicks)
- Audience demographics
- AI-powered post suggestions (useful for ideation, not final copy)

Configure Taplio:
1. Connect LinkedIn account via OAuth
2. Set default posting times (Tuesday-Thursday, 8:00am in ICP timezone)
3. Enable analytics tracking for all published posts

### 2. Set up PostHog event tracking

Run the `posthog-gtm-events` drill to configure event tracking for this play. Define these events:

```
linkedin_post_published    -> properties: post_url, topic_pillar, format, scheduled_date
linkedin_engagement_logged -> properties: post_url, impressions, likes, comments, shares, engagement_rate
linkedin_lead_captured     -> properties: lead_name, lead_title, lead_company, signal_type, source_post_url
linkedin_meeting_booked    -> properties: lead_name, source_post_url, days_from_first_touch
```

For Baseline, events are logged manually or via n8n webhook (see step 5). At Scalable level, these become automated.

### 3. Batch-create content weekly

Run the `founder-linkedin-content-batch` drill every Friday or Monday to produce next week's posts:

1. Review last week's post performance in Taplio. Identify which pillars and formats drove the most engagement and leads.
2. Select topics for next week: lean toward pillars that performed well, test one new angle per week.
3. Generate 4-5 drafts via LLM API using the founder's voice profile.
4. **Human action required:** Founder reviews and edits each draft (target: 15-20 minutes for the batch).
5. Schedule approved posts in Taplio for optimal times across the week.
6. Leave 1 slot open for a reactive/timely post during the week.

### 4. Execute daily engagement workflow

Run the `linkedin-engagement-workflow` drill every posting day:

1. **Pre-post (15 min):** Engage with 5-10 ICP-relevant posts before your post goes live.
2. **Post-publish (3 check-ins):** Reply to all comments at 30 min, 2 hours, and end of day.
3. **DM follow-up:** Send a DM to anyone who shows a buying signal (describes a problem you solve, asks about your product, or DMs you referencing a post).
4. **Profile stalking:** View profiles of ICP-matching people who engaged with your post (triggers a notification to them).

On non-posting days, still spend 10 minutes engaging with others' content to maintain algorithmic momentum.

### 5. Capture and track leads

Run the `linkedin-lead-capture` drill daily:

1. Review new DMs, buying-signal comments, and connection requests.
2. For each lead, create a contact in Attio:
   - `lead_source` = "linkedin-content"
   - `first_touch_post` = URL of the post they engaged with
   - `signal_type` = "dm" | "comment" | "connection" | "profile_view"
   - `lead_status` = "new" | "dm-sent" | "conversation-active" | "meeting-booked"
3. Log a `linkedin_lead_captured` event in PostHog (manually via API call or via an n8n webhook form).

### 6. Run a weekly performance review

Every Friday:
1. Pull Taplio analytics for the week: per-post impressions, engagement rate, top-performing post.
2. Count leads captured in Attio this week.
3. Compute: total impressions, average engagement rate, profile views, follower growth, leads captured.
4. Compare to Baseline targets:
   - Week 1: >= 2 leads
   - Week 2: >= 3 leads (cumulative >= 5)
5. Note which content pillar produced the most leads (not just the most engagement -- engagement without leads is vanity).
6. Adjust next week's content mix based on findings.

### 7. Evaluate against threshold

At the end of 2 weeks:
- Total inbound leads captured in CRM: count Attio records with `lead_source` = "linkedin-content" created in the last 14 days.
- **Pass threshold: >= 5 inbound leads over 2 weeks**
- If PASS: the process is repeatable and producing results. Document the content system (pillars, voice profile, engagement routine, lead capture workflow). Proceed to Scalable.
- If FAIL: diagnose. Low impressions? The hooks are weak -- rewrite using `linkedin-organic-hooks` patterns. High impressions but low leads? The CTA is not compelling or the content is entertaining but not attracting buyers. Adjust and re-run Baseline for another 2 weeks.

## Time Estimate

- Taplio + PostHog setup: 1 hour (one-time)
- Weekly content batch (x2 weeks): 2 hours
- Daily engagement (10 days x 25 min): 4 hours
- Lead capture and logging (10 days x 15 min): 2.5 hours
- Weekly reviews (x2): 1 hour
- Evaluation: 30 minutes
- **Total: ~11-12 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn (free) | Publishing, engaging, DMs | Free |
| Taplio Starter | Scheduling + analytics | [$39/mo](https://taplio.com/pricing) |
| Claude or GPT API | Generating post drafts | ~$0.10/month for 8-10 posts |
| PostHog | Event tracking for attribution | [Free tier: 1M events/mo](https://posthog.com/pricing) |
| Attio | CRM for lead tracking | Free tier or existing plan |

**Baseline total cost: ~$39/mo** (Taplio subscription; everything else is free tier)

## Drills Referenced

- `founder-linkedin-content-batch` -- weekly content generation and scheduling
- `linkedin-engagement-workflow` -- daily engagement routine for reach and lead signals
- `linkedin-lead-capture` -- capturing engagement signals into CRM with attribution
- `posthog-gtm-events` -- setting up event taxonomy for measurement
