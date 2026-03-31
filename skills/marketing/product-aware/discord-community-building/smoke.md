---
name: discord-community-building-smoke
description: >
  Discord Community Building — Smoke Test. Launch a branded Discord server, seed it
  with 5 value-first discussion threads, invite the first 50 members from existing
  channels, and measure whether the server generates any product-aware engagement
  (questions, feature discussions, or site referrals). Validates that your audience
  will participate in a Discord community before investing in automation.
stage: "Marketing > ProductAware"
motion: "CommunitiesForums"
channels: "Communities, Product"
level: "Smoke Test"
time: "12 hours over 2 weeks"
outcome: "≥ 50 members, ≥ 5 unique daily posters, and ≥ 3 referral sessions to your site within 2 weeks"
kpis: ["Total server members (target ≥ 50)", "Unique daily posters averaged over week 2 (target ≥ 5)", "Referral sessions from Discord to site (target ≥ 3)", "Threads with 3+ replies (target ≥ 3)", "Average time to first reply from team (target < 4 hours)"]
slug: "discord-community-building"
install: "npx gtm-skills add marketing/product-aware/discord-community-building"
drills:
  - slack-discord-reconnaissance
  - slack-discord-content-posting
  - threshold-engine
---

# Discord Community Building — Smoke Test

> **Stage:** Marketing > ProductAware | **Motion:** CommunitiesForums | **Channels:** Communities, Product

## Outcomes

Prove that a Discord server can generate product-aware engagement from your audience. Product-aware visitors already know your product exists but need community validation, peer discussion, and direct access to your team before taking the next step. This test creates a minimal server, seeds it with value-first content, and measures whether your audience will show up and participate.

Pass: ≥ 50 members, ≥ 5 unique daily posters (averaged over week 2), and ≥ 3 referral sessions from Discord to your site within 2 weeks.
Fail: < 50 members or < 3 unique daily posters or 0 referral sessions after 2 weeks.

## Leading Indicators

- At least 10 members join within the first 48 hours of the invite going out (your existing audience has Discord appetite)
- At least 1 organic thread (not started by your team) appears within the first 5 days (members see the server as a place to ask questions, not just consume announcements)
- A member replies to another member's question before your team does (peer-to-peer dynamics are forming)
- At least 1 link shared by your team in Discord generates a click to your site within PostHog (the UTM tracking pipeline works)
- A member references a Discord discussion in another channel (email, Twitter, support ticket) within 2 weeks (the community is becoming a touchpoint in the buyer journey)

## Instructions

### 1. Research Discord community landscape

Run the `slack-discord-reconnaissance` drill scoped to Discord only. Identify:

- 3-5 existing Discord servers where your ICP is active (these are reference models, not competitors)
- Channel structures that work for your industry: what channels do successful communities use? Which are most active?
- Engagement norms: what content formats get replies? How long are typical messages? Do servers use forum channels or text channels for Q&A?
- Your positioning gap: what community experience is missing that you can provide?

Document the findings in a brief (stored in Attio) that will guide your server design.

### 2. Create and configure the Discord server

**Human action required:** Create the Discord server via the Discord client (server creation is not available via API). Name it `{Product Name} Community` or `{Product Name} Hub`.

After creation, configure via the Discord API using the `discord-api-write` fundamental:

**Create channels** (POST `/guilds/{GUILD_ID}/channels`):

| Channel | Type | Purpose |
|---------|------|---------|
| #welcome | text (0) | Auto-greeting for new members. Pin a message explaining what the server is for, community guidelines, and links to key channels. |
| #introductions | text (0) | Members introduce themselves. Seed with 3 team member intros following the format: role, what you work on, one non-work interest. |
| #general | text (0) | Open discussion. This is where organic conversation starts. |
| #help | forum (15) | Product questions and troubleshooting. Forum format so each question becomes a searchable thread. |
| #feature-ideas | forum (15) | Feature requests and product feedback. Forum tags: `idea`, `in-progress`, `shipped`, `wont-do`. |
| #resources | text (0) | Curated links to guides, tutorials, and relevant industry content. Not self-promotional -- include third-party resources too. |
| #announcements | text (0) | Product updates and community news. Read-only for non-team roles (set channel permission overrides). |

**Create roles** (POST `/guilds/{GUILD_ID}/roles`):
- `Team` — your team members (distinct color, appears above other roles)
- `Community Member` — default role for verified members
- `Power User` — to be awarded later to active contributors

**Set verification level** to `Medium` (must have a verified email and be registered on Discord for > 5 minutes) to reduce spam.

### 3. Seed the server with value-first content

Run the `slack-discord-content-posting` drill to create 5 seed threads before inviting anyone:

1. **#general — Discussion starter:** Post a specific, opinionated take on a trend in your space. Ask for community input. Example: "We have been seeing [trend]. Here is how we think about it: [framework]. How are you all approaching this?"

2. **#help — Answered question:** Create a forum post asking a common product question (one you see in support tickets), then reply with a detailed answer. This sets the tone for the channel: questions get thorough responses.

3. **#feature-ideas — Real feature discussion:** Post a feature you are genuinely considering. Share the tradeoffs. Ask for input on the direction. This signals the community has real influence.

4. **#resources — Curated resource list:** Post a list of 5-7 genuinely useful resources for your audience (mix of your content and third-party). Include brief 1-sentence annotations for each.

5. **#general — Behind-the-scenes share:** Post something your audience would find interesting about how your product works or a decision your team made recently. Authenticity over polish.

Each post must include UTM-tagged links where relevant:
```
https://yoursite.com/PAGE?utm_source=discord&utm_medium=community&utm_campaign=discord-community-building&utm_content={channel}_{topic}
```

### 4. Invite the first 50 members

**Human action required:** Generate a Discord invite link (never-expiring, unlimited uses) via the Discord client or API:

```
POST /channels/{WELCOME_CHANNEL_ID}/invites
Body: {"max_age": 0, "max_uses": 0, "unique": false}
```

Distribute the invite through your existing channels, in priority order:

1. **Existing email list:** Send a dedicated email via Loops to your most engaged contacts (opened 3+ emails in the last 30 days). Subject line should be direct: "We launched a Discord for [product] users." Body should be 3 sentences max: what it is, why they should join, the invite link.

2. **In-app:** If you have an in-app messaging system (Intercom), display a one-time banner or message to active users: "Join our Discord community to connect with other [product] users and our team."

3. **Social media:** Post the invite on your LinkedIn and Twitter/X. Lead with what the community offers (peer discussion, direct access to team, feature influence), not what you want from them.

4. **Website:** Add a link to the Discord server in your site footer and docs.

Do NOT buy members, use member-farming bots, or cross-post in unrelated servers. The goal is 50 real, interested members.

### 5. Engage daily for 2 weeks

For 14 days, commit to the following daily routine (30-45 minutes per day):

- **Morning check (10 min):** Read all new messages. Reply to any questions in #help within 4 hours. React to member messages with a relevant emoji to acknowledge them.
- **Post or reply (15 min):** Either start a new discussion thread or give a substantive reply to a member's post. Use the `slack-discord-content-posting` drill content templates.
- **Evening check (10 min):** Reply to any afternoon messages. Note which topics generated discussion vs silence.

Log every interaction using the `community-engagement-tracking` fundamental:
```json
{
  "date": "2026-03-30",
  "platform": "discord",
  "server": "{server_name}",
  "channel": "#help",
  "action": "reply",
  "thread_url": "https://discord.com/channels/{GUILD}/{CHANNEL}/{MESSAGE}",
  "topic": "how to configure X",
  "included_link": true,
  "replies_received": 2
}
```

### 6. Evaluate after 2 weeks

Run the `threshold-engine` drill to measure against the pass threshold. Collect:

- **Member count:** Check via `GET /guilds/{GUILD_ID}?with_counts=true`
- **Unique daily posters:** For each of the last 7 days, count unique message authors across all channels. Average the 7 values.
- **Referral sessions:** Query PostHog for events where `utm_source=discord` in the last 14 days
- **Thread engagement:** Count threads (forum posts or reply chains) with 3+ replies from 2+ unique authors
- **Reply time:** Average time between a member's question in #help and the first team reply

Evaluation:

- **PASS (≥ 50 members, ≥ 5 daily posters, ≥ 3 referral sessions):** Document which content topics generated the most discussion. Note the ratio of team-initiated vs member-initiated threads. Record which invite channel brought the most members. Proceed to Baseline.
- **MARGINAL (30-49 members or 3-4 daily posters):** Diagnose: Did the invite reach enough people? Check open rates on the email. Check in-app message impression count. If members joined but are not posting, the content seeding may not have been compelling enough. Rewrite seed content to be more specific and opinion-driven.
- **FAIL (< 30 members or < 3 daily posters):** Your audience may not be on Discord. Check demographics: if your ICP is enterprise buyers (age 40+), Discord may not be the right platform. Consider pivoting to Slack community or subreddit engagement instead.

## Time Estimate

- Discord landscape research: 2 hours
- Server creation and configuration: 1.5 hours
- Seed content creation (5 threads): 2 hours
- Invite distribution (email, in-app, social, website): 1.5 hours
- Daily engagement (30 min x 14 days): 7 hours
- Threshold evaluation: 30 minutes
- Total: ~12 hours over 2 weeks (front-loaded in week 1, maintenance in week 2)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Discord | Community server hosting | Free ([discord.com](https://discord.com)) |
| PostHog | Referral session tracking via UTM parameters | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Store community research findings and engagement logs | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| Loops | Email invite to existing contacts | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app invite message (optional) | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |

**Estimated monthly cost for Smoke:** $0-49/mo (Discord free, PostHog free tier, Attio free tier; Loops only if you send an invite email)

## Drills Referenced

- `slack-discord-reconnaissance` — discover and rank Discord servers where your ICP is active to inform your own server's channel structure and content strategy
- `slack-discord-content-posting` — create value-first original content for Discord channels that establishes authority and sparks discussion
- `threshold-engine` — evaluate member count, daily active posters, and referral sessions against the pass threshold and recommend next action
