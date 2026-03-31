---
name: alumni-campus-pro-orgs-baseline
description: >
  Alumni & Campus Outreach — Baseline Run. Set up always-on tracking and a repeatable
  engagement cadence across proven alumni, campus, and professional org communities.
  First continuous automation — agent monitors and responds, human posts and takes meetings.
stage: "Marketing > Unaware"
motion: "Communities & Forums"
channels: "Communities, Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 2 meetings booked over 2 weeks with full attribution tracking"
kpis: ["Referral sessions by community (weekly)", "Signup or meeting conversion rate by community", "Posts published per week", "Response rate on posts (replies/reactions per post)", "Inbound DMs or inquiries"]
slug: "alumni-campus-pro-orgs"
install: "npx gtm-skills add marketing/unaware/alumni-campus-pro-orgs"
drills:
  - posthog-gtm-events
  - community-monitoring-automation
  - community-response-crafting
---

# Alumni & Campus Outreach — Baseline Run

> **Stage:** Marketing → Unaware | **Motion:** Communities & Forums | **Channels:** Communities, Other

## Outcomes

Prove that community engagement produces meetings repeatably over 2 weeks with tracking and attribution in place. The agent sets up monitoring, crafts responses, and tracks metrics. The human posts content and takes meetings. This is the first always-on automation layer.

## Leading Indicators

- PostHog tracking events flowing for all community-driven traffic
- Automated alerts firing for relevant community discussions within target communities
- At least 6 posts/responses published across 2 weeks
- Referral sessions trending upward week-over-week
- At least 2 inbound DMs or inquiries in 2 weeks

## Instructions

### 1. Set up community attribution tracking

Run the `posthog-gtm-events` drill to create the event taxonomy for this play. Define and implement these custom events:

```
alumni_campus_community_post     — fired when content is published to a community
alumni_campus_referral_visit     — fired on site visit with utm_campaign=alumni-campus-pro-orgs
alumni_campus_signup             — fired on signup where first_touch is community referral
alumni_campus_meeting_booked     — fired when a meeting is booked from community-sourced lead
```

For each event, include properties: `community_name`, `community_type` (alumni/campus/professional), `platform` (linkedin/slack/discord/email), `content_type` (post/comment/dm/resource), `post_url`.

Create a PostHog saved insight: "Alumni & Campus Outreach — Baseline" showing:
- Referral sessions by community (bar chart, grouped by `community_name`)
- Conversion funnel: `alumni_campus_referral_visit` → `alumni_campus_signup` → `alumni_campus_meeting_booked`
- Weekly trend of referral sessions (line chart)

### 2. Build community monitoring automation

Run the `community-monitoring-automation` drill adapted for alumni/campus/professional communities beyond Reddit:

**For Slack/Discord communities (where your bot or integration can read messages):**
Build an n8n workflow that polls target Slack channels (via Slack API) and Discord channels (via Discord API) for messages matching your keyword lists. Route relevant threads to a `#community-engagement` Slack channel with priority labels.

```
Schedule Trigger (every 2 hours)
  → Slack API Node: Read messages from target channels (last 2 hours)
  → Discord API Node: Read messages from target channels (last 2 hours)
  → Merge Node: Combine all results
  → Function Node: Filter by keyword match (pain-point and buying-intent keywords from Smoke)
  → IF Node: Score > threshold → route to alert channel
  → Slack Alert Node:
      Channel: #community-engagement
      Format: "[PRIORITY] New thread in {community_name} ({platform})
               Topic: {message_summary}
               Keywords: {matched_keywords}
               Action: Respond within {SLA based on priority}"
```

**For LinkedIn Groups and email lists (no API polling):**
Set up Google Alerts or Syften monitors for your ICP keywords scoped to community platforms. Route alerts through n8n to the same `#community-engagement` channel.

Target: 3-8 actionable alerts per day across all monitored communities.

### 3. Execute repeatable engagement cadence

Establish a consistent weekly rhythm:

**Monday:** Review the previous week's community metrics in PostHog. Identify which communities drove the most referral sessions. Plan the week's content topics based on active discussions.

**Tuesday-Thursday:** Run the `community-response-crafting` drill to respond to 2-3 flagged threads per day. For each response:
- Analyze the thread context and existing responses
- Determine the response archetype (Expert Answer, Framework Share, Experience Report, Resource Curator, Follow-up Question)
- Draft the response following the drill's formatting and content rules
- Include UTM-tracked links only where genuinely helpful (maximum 1 in 5 responses)

**Human action required:** Post responses in communities where bot posting is prohibited (most alumni and professional groups). The agent drafts, the human posts.

**Friday:** Publish 1-2 original content pieces across top-performing communities. Use insights from the week's discussions to write content that addresses active questions or gaps.

### 4. Track and attribute every interaction

Log each community interaction using the `community-engagement-tracking` fundamental:

```json
{
  "date": "{date}",
  "community_name": "{name}",
  "community_type": "alumni|campus|professional",
  "platform": "linkedin|slack|discord|email",
  "action": "post|comment|dm|resource_share",
  "post_url": "{url}",
  "content_type": "expert_answer|framework|experience_report|resource_list|discussion_starter",
  "included_link": true|false,
  "reactions_48h": 0,
  "replies_48h": 0,
  "referral_sessions_48h": 0,
  "dms_received": 0,
  "meetings_booked": 0
}
```

Update Attio contacts for anyone who engages: set `lead_source` to `community-{community_name}` and `lead_source_detail` to the specific post or thread URL.

### 5. Evaluate against threshold

After 2 weeks, run the `threshold-engine` drill:

- Pull `alumni_campus_meeting_booked` events from PostHog for the 2-week window
- Cross-reference with Attio deals where `lead_source` starts with `community-`
- Compare against threshold: **≥ 2 meetings booked over 2 weeks**

**PASS (≥ 2 meetings):** Proceed to Scalable. Document: which communities produced meetings, which content types drove engagement, what the conversion funnel looks like.
**FAIL (< 2 meetings):** Review metrics to diagnose. If referral sessions are high but meetings are low, the problem is conversion — improve CTAs or landing page. If referral sessions are low, the problem is community selection or content quality. Adjust and re-run Baseline.

## Time Estimate

- PostHog event setup and dashboard creation: 2 hours
- n8n monitoring workflow build: 3 hours
- Content creation and response crafting (2 weeks): 5 hours
- Tracking, logging, and evaluation: 2 hours
- **Total: 12 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Attribution tracking, funnels, referral analytics | Free tier: 1M events/mo (https://posthog.com/pricing) |
| n8n | Monitoring automation, alert routing | Free self-hosted or €24/mo Starter cloud (https://n8n.io/pricing) |
| Attio | Contact attribution, interaction logging | Free tier available (https://attio.com/pricing) |
| Syften | Keyword monitoring for LinkedIn/forum communities | $19.95/mo Entry plan (https://syften.com/) — optional, use if LinkedIn Groups or forums need monitoring |

**Estimated play-specific cost at Baseline level:** $0-20/mo (PostHog free tier, n8n self-hosted or Starter, Syften optional)

## Drills Referenced

- `posthog-gtm-events` — set up the event taxonomy and attribution tracking for community-driven traffic
- `community-monitoring-automation` — build n8n workflows to surface relevant discussions across Slack, Discord, and monitored platforms
- `community-response-crafting` — produce high-quality, community-appropriate responses that build authority and generate inbound interest
