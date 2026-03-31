---
name: discord-community-building-baseline
description: >
  Discord Community Building — Baseline Run. Deploy always-on monitoring and
  response workflows via n8n, instrument PostHog event tracking for all
  community-driven traffic, and establish a repeatable content cadence. First
  always-on automation that detects engagement opportunities and routes them
  for response without manual browsing.
stage: "Marketing > ProductAware"
motion: "CommunitiesForums"
channels: "Communities, Product"
level: "Baseline Run"
time: "25 hours over 6 weeks"
outcome: "≥ 200 members, ≥ 20 DAU, and ≥ 10 qualified leads attributed to Discord over 6 weeks"
kpis: ["Total server members (target ≥ 200)", "Daily active users averaged over last 2 weeks (target ≥ 20)", "Qualified leads attributed to Discord (target ≥ 10)", "Average reply time to #help questions (target < 2 hours during business hours)", "Content posts per week by team (target ≥ 3)", "Member-initiated threads per week (target ≥ 5)"]
slug: "discord-community-building"
install: "npx gtm-skills add marketing/product-aware/discord-community-building"
drills:
  - slack-discord-monitoring-automation
  - slack-discord-response-crafting
  - posthog-gtm-events
---

# Discord Community Building — Baseline Run

> **Stage:** Marketing > ProductAware | **Motion:** CommunitiesForums | **Channels:** Communities, Product

## Outcomes

Deploy the first always-on automation layer for your Discord community. The agent monitors channels for engagement opportunities, routes alerts for response, and tracks every community interaction through PostHog. This transforms community management from "check Discord when you remember" to a structured, measurable pipeline with clear lead attribution.

Pass: ≥ 200 members, ≥ 20 DAU (averaged over the final 2 weeks), and ≥ 10 qualified leads (contacts who visited your site from Discord and took a conversion action) over 6 weeks.
Fail: < 200 members or < 20 DAU or < 10 qualified leads after 6 weeks.

## Leading Indicators

- Member growth rate stays above 15 new members per week for the first 4 weeks (invite channels and organic discovery are working)
- The monitoring workflow fires 5-15 alerts per day within the first week of activation (keyword filters are tuned correctly)
- At least 3 #help forum threads per week are started by members (not your team) by week 3 (the community is being used as a support channel)
- PostHog shows ≥ 5 referral sessions per week from Discord by week 2 (UTM tracking is working and members are clicking links)
- At least 2 members post in #feature-ideas unprompted within the first 3 weeks (members see the community as a product influence channel)

## Instructions

### 1. Configure PostHog event tracking

Run the `posthog-gtm-events` drill to set up a complete Discord community event taxonomy in PostHog:

```
discord_referral_visit — visitor arrives at your site with utm_source=discord
  Properties: channel, topic, content_type, member_id
discord_community_signup — visitor signs up after arriving from Discord
  Properties: channel, attribution_message_url, days_since_join
discord_help_thread_created — member creates a new #help forum post
  Properties: thread_id, topic_category, member_tier
discord_help_thread_resolved — team marks a help thread as resolved
  Properties: thread_id, resolution_time_hours, required_escalation
discord_feature_idea_submitted — member posts in #feature-ideas
  Properties: thread_id, idea_category, votes_received
discord_member_joined — new member joins the server
  Properties: invite_source, member_id, join_date
discord_member_churned — member leaves the server
  Properties: member_id, days_active, last_message_date, engagement_tier
```

Build PostHog funnels:
- `discord_referral_visit` -> page viewed (pricing or docs) -> `discord_community_signup`
- `discord_member_joined` -> first message posted -> second week active -> qualified lead

Create PostHog cohorts:
- "Discord community members" — all visitors with `utm_source=discord`
- "Discord power users" — visitors from Discord who visited 3+ pages or spent 5+ minutes

### 2. Deploy keyword monitoring automation

Run the `slack-discord-monitoring-automation` drill, scoped to your Discord server. Build two n8n workflows:

**Workflow 1 — Channel Monitor (runs every 15 minutes):**

Using the `discord-api-read` fundamental, poll all text and forum channels for new messages. For each new message, run keyword matching against three lists:

- **Support signals:** "how do I", "not working", "error", "help", "stuck", "broken", "bug"
- **Buying signals:** "pricing", "plan", "upgrade", "enterprise", "team plan", "how much", "competitor name"
- **Feature signals:** "wish", "would be great if", "feature request", "any plans to", "roadmap"

Route matches to an internal Slack channel (#discord-engagement-queue) with:
```
[{priority}] {signal_type} in #{channel}
> {message_preview}
Keywords: {matched}
Author: {username} (joined {days_ago} days ago)
Link: https://discord.com/channels/{GUILD}/{CHANNEL}/{MESSAGE}
Action: {respond within 1h for support / 4h for buying / 24h for feature}
```

**Workflow 2 — Daily Digest (runs at 9am):**

Aggregate the previous day's activity:
- Total messages across all channels
- New members joined
- Unanswered #help threads (no reply within 8 hours)
- Threads with highest engagement (most replies)
- Any messages from members with the `Power User` role

Post the digest to #discord-engagement-queue in Slack.

### 3. Establish a content cadence

Using the `slack-discord-content-posting` drill, commit to a minimum posting schedule:

| Day | Channel | Content Type |
|-----|---------|-------------|
| Monday | #general | Weekly discussion starter — pose a question about a trend, challenge, or workflow in your space |
| Wednesday | #resources | Curated resource — share a useful article, tool, or framework (mix of yours and third-party) |
| Friday | #general | Behind-the-scenes or product update — what the team shipped, what's being worked on, a lesson learned |

Each post must follow the content quality rules from the drill:
- Lead with value, not self-promotion
- Include UTM-tagged links where relevant
- End with a discussion prompt, not a CTA
- Stay responsive for 2 hours after posting

Additionally, respond to all engagement alerts from the monitoring workflow:
- Support signals: respond in #help with a thorough answer. Use the `slack-discord-response-crafting` drill to draft responses that are specific, actionable, and reference documentation with links.
- Buying signals: respond helpfully. If someone asks about pricing, provide direct information. Do not force them into a sales call.
- Feature signals: acknowledge the idea, share context on whether it's on the roadmap, and tag the thread appropriately.

### 4. Grow membership to 200

Continue invite distribution from Smoke, adding:

- **Onboarding flow integration:** After a user completes signup or onboarding, include a Discord invite in the follow-up email sequence (via Loops). Frame it as: "Join [N] other users in our Discord for tips, help, and product updates."
- **Documentation integration:** Add a "Join our Discord" banner or link on your docs site, especially on pages where users are likely to have follow-up questions.
- **Support ticket follow-up:** When a support ticket is resolved via Intercom, include a Discord invite in the resolution message: "For quick questions, you can also reach us in our Discord community."
- **Content cross-promotion:** In blog posts and social media, mention that the discussion continues in Discord (with invite link).

Track invite source attribution by creating unique invite links per channel:
```
POST /channels/{WELCOME_CHANNEL_ID}/invites
Body: {"max_age": 0, "max_uses": 0, "unique": true}
```
Create one per source (email, in-app, docs, support, social). Log which invite code maps to which source in Attio. Discord's invite metadata includes `uses` count, which tells you how many people joined via each link.

### 5. Implement lead attribution

When a Discord member visits your site and converts, attribute the lead to Discord:

1. All links shared in Discord carry UTM parameters: `utm_source=discord&utm_medium=community&utm_campaign=discord-community-building&utm_content={channel}_{topic}`
2. PostHog captures these automatically on page load
3. When a `discord_community_signup` event fires, use an n8n webhook to:
   - Create or update the contact in Attio using the `attio-contacts` fundamental
   - Set `lead_source` = `discord-community`
   - Set `lead_source_detail` = the specific channel (from `utm_content`)
   - Set `first_touch_url` = the Discord message URL if available
4. For members who visit your site without clicking a UTM link, check PostHog's `$initial_referrer` — if it contains `discord.com`, attribute to Discord as a secondary signal

### 6. Evaluate after 6 weeks

Run the `threshold-engine` drill. Collect:

- **Member count:** `GET /guilds/{GUILD_ID}?with_counts=true`
- **DAU:** For each of the last 14 days, count unique message authors. Average the 14 values.
- **Qualified leads:** Query Attio for contacts where `lead_source = discord-community` AND they completed a conversion action (demo booked, trial started, signup completed) in PostHog
- **Reply time:** Average response time for #help threads (from `discord_help_thread_created` to first team reply timestamp)
- **Content cadence adherence:** Did the team post ≥ 3 times per week for 6 weeks?

Evaluation:

- **PASS (≥ 200 members, ≥ 20 DAU, ≥ 10 qualified leads):** Document which invite source drove the most members. Identify the top 3 content topics by engagement. Note which monitoring keyword groups produced the most actionable alerts. Record cost per qualified lead. Proceed to Scalable.
- **MARGINAL (150-199 members or 15-19 DAU or 7-9 leads):** Diagnose: Check invite source distribution — is growth concentrated in one channel? If DAU is low relative to members, the content is not compelling enough to drive return visits. Review the monitoring alerts — are they being responded to promptly? Check reply time targets.
- **FAIL (< 150 members or < 15 DAU or < 7 leads):** Check: Is the monitoring workflow running reliably (check n8n execution logs)? Are the keyword filters tuned (too many or too few alerts)? Is the server easy to find (check all invite placements)? Is the content schedule being maintained? If fundamentals are working but members are not converting to leads, the problem may be content quality or missing CTAs in the right places.

## Time Estimate

- PostHog event taxonomy setup: 3 hours
- n8n monitoring workflows (build + test): 5 hours
- Content creation (3 posts/week x 6 weeks): 9 hours
- Alert response and engagement (20 min/day x 42 days): 14 hours (partially overlaps with content creation)
- Invite distribution setup (email, docs, support integration): 2 hours
- Lead attribution n8n workflow: 2 hours
- Weekly review and keyword tuning: 3 hours (30 min/week)
- Threshold evaluation: 1 hour
- Total: ~25 hours over 6 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Discord | Community server hosting | Free ([discord.com](https://discord.com)) |
| PostHog | Event tracking, funnels, cohorts, referral attribution | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Monitoring workflows, alert routing, lead attribution automation | Free self-hosted; Starter ~$24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Lead storage, invite source tracking, engagement logging | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Loops | Onboarding email with Discord invite | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app invite, support ticket follow-up with Discord link | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |

**Estimated monthly cost for Baseline:** $24-80/mo (n8n for monitoring; Attio, Loops, Intercom on existing plans from other plays)

## Drills Referenced

- `slack-discord-monitoring-automation` — build n8n workflows that poll Discord channels for keyword matches and route prioritized alerts to an internal engagement queue
- `slack-discord-response-crafting` — draft authentic, value-first responses to Discord threads that build authority and drive inbound interest
- `posthog-gtm-events` — define and implement the Discord community event taxonomy in PostHog for funnels, cohorts, and lead attribution
