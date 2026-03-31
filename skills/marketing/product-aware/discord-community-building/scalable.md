---
name: discord-community-building-scalable
description: >
  Discord Community Building — Scalable Automation. Scale to 1,000+ members and
  30+ qualified leads per month by deploying an AI-powered Discord bot for
  automated Q&A triage, running A/B tests on content formats and channel
  structure, launching member programs (Power User, Ambassador), and implementing
  community-health scoring to allocate engagement effort by channel ROI.
stage: "Marketing > ProductAware"
motion: "CommunitiesForums"
channels: "Communities, Product"
level: "Scalable Automation"
time: "50 hours over 3 months"
outcome: "≥ 1,000 members, ≥ 100 DAU, and ≥ 30 qualified leads/month sustained for 2 consecutive months"
kpis: ["Total server members (target ≥ 1,000)", "Daily active users averaged over final month (target ≥ 100)", "Qualified leads per month (target ≥ 30)", "Member-to-member reply ratio (target ≥ 40% of help threads answered by non-team members)", "Content engagement rate — threads with 3+ replies / total posts (target ≥ 50%)", "Bot-assisted resolution rate for routine questions (target ≥ 25%)"]
slug: "discord-community-building"
install: "npx gtm-skills add marketing/product-aware/discord-community-building"
drills:
  - community-health-scoring
  - slack-discord-content-posting
  - ab-test-orchestrator
---

# Discord Community Building — Scalable Automation

> **Stage:** Marketing > ProductAware | **Motion:** CommunitiesForums | **Channels:** Communities, Product

## Outcomes

Find the 10x multiplier for your Discord community. At Baseline, your team manually responded to every thread and posted 3x per week. Scalable deploys the systems that make the community self-sustaining: an AI bot that handles routine questions, member recognition programs that incentivize peer-to-peer help, A/B-tested content formats, and channel-level ROI scoring that tells you exactly where to focus team effort.

Pass: ≥ 1,000 members, ≥ 100 DAU (averaged over the final month), and ≥ 30 qualified leads per month sustained for 2 consecutive months.
Fail: < 1,000 members or < 100 DAU or < 30 qualified leads/month at the end of 3 months.

## Leading Indicators

- Member growth rate exceeds 50 new members per week by month 2 (organic discovery and referral loops are working)
- The AI bot resolves ≥ 25% of #help questions without team intervention by week 6 (bot training data and knowledge base are sufficient)
- At least 10 members earn Power User role within the first 6 weeks (the recognition program motivates engagement)
- Member-initiated threads outnumber team-initiated threads by 2:1 by month 2 (the community is self-generating content)
- Channel health scores stabilize with at least 3 channels scoring "thriving" (60+) by month 2 (the channel structure serves the audience)

## Instructions

### 1. Deploy an AI-powered community bot

Build a Discord bot that handles routine questions and triage in #help. The bot watches for new forum posts and:

1. **Searches your knowledge base** (docs, FAQ, previous resolved threads) for a matching answer
2. **If confidence is high (>80% match):** Posts a reply with the answer, citing the source doc/thread. Adds a reaction asking the member to confirm if this resolved their question.
3. **If confidence is medium (50-80%):** Posts a tentative answer prefixed with "I found something that might help:" and pings the team role for human follow-up.
4. **If confidence is low (<50%):** Does not reply. Routes the thread to the team via the monitoring workflow from Baseline.

Implementation using the `discord-api-read` and `discord-api-write` fundamentals:

- Use Discord's Gateway API (WebSocket) for real-time message events, or poll #help forum for new threads every 2 minutes via n8n
- Send new thread content to Claude API (via `anthropic-api-patterns` fundamental) with a system prompt containing your knowledge base and resolved thread history
- Post the bot's reply via `POST /channels/{THREAD_ID}/messages`
- Track bot performance: `bot_reply_posted`, `bot_reply_confirmed_helpful`, `bot_reply_escalated_to_human`

**Human action required:** Review the bot's first 50 responses. Correct any inaccurate answers. Adjust the confidence thresholds based on false positive/negative rates. Add missing content to the knowledge base when the bot fails to find an answer.

### 2. Launch the member recognition program

Create a tiered recognition system to incentivize peer-to-peer help:

**Power User criteria (automated detection):**
- 20+ messages in the last 30 days
- Active in 3+ channels
- At least 5 replies to other members' questions
- Member for 30+ days

**Ambassador criteria (application-based):**
- Power User for 60+ days
- Contributed a resource post, tutorial, or detailed guide
- Positive community interactions (no warnings or moderation actions)

Build an n8n workflow that runs weekly:
1. Query Discord API for message counts per member (`discord-api-read` fundamental)
2. Score each member against Power User criteria
3. Auto-assign the Power User role via `PUT /guilds/{GUILD_ID}/members/{USER_ID}/roles/{ROLE_ID}`
4. Post a congratulatory message in #announcements tagging the new Power Users
5. Log role changes in Attio for the member's contact record

Power User perks:
- Distinct role color (visible in member list)
- Access to a private #power-users channel for early product previews and direct feedback to the team
- Name featured in monthly community spotlight (posted in #announcements)

Ambassador perks (on top of Power User):
- Quarterly 1-on-1 with a product team member
- Input on product roadmap priorities
- Swag or account credit (configure based on your budget)

### 3. Run A/B tests on content and structure

Run the `ab-test-orchestrator` drill to test community engagement approaches. Run one test at a time, minimum 2 weeks per test:

**Test 1 — Content format:**
- Control: Current mix of discussion starters, resources, and behind-the-scenes posts
- Variant A: Add weekly "Office Hours" threads (scheduled, team answers questions live for 1 hour)
- Variant B: Add weekly "Show & Tell" threads (members share how they use the product)
- Metric: Thread replies per post, unique participants per thread

**Test 2 — Channel structure:**
- Control: Current channel layout
- Variant: Add topic-specific channels based on use case (e.g., #marketing-use-case, #engineering-use-case) alongside general channels
- Metric: Messages per channel per week, DAU change

**Test 3 — Onboarding experience:**
- Control: Current #welcome pin + #introductions channel
- Variant: Implement a Discord onboarding flow (Discord's built-in Onboarding feature via `PATCH /guilds/{GUILD_ID}` with `features: ["COMMUNITY"]`) that asks new members to select their role/use case and routes them to relevant channels
- Metric: First-message rate (% of new members who post within 48 hours of joining), 7-day retention

**Test 4 — CTA placement:**
- Control: UTM links in #resources posts only
- Variant: Add a pinned message in #general with a weekly rotating CTA (try free, book demo, read case study) with tracking
- Metric: Referral sessions per week, conversion rate from Discord

Track all test results in PostHog using the `posthog-experiments` fundamental. Log decisions and outcomes in Attio.

### 4. Implement community health scoring

Run the `community-health-scoring` drill adapted for Discord channels. Score each channel weekly on:

| Signal | Weight | Source |
|--------|--------|--------|
| Message volume | 25% | Discord API — messages in the last 7 days |
| Unique contributors | 25% | Discord API — unique authors in the last 7 days |
| Referral value | 25% | PostHog — sessions from UTM links in this channel |
| Thread engagement | 15% | Discord API — average replies per thread/forum post |
| Growth contribution | 10% | Correlation between channel activity and new member joins |

Classify each channel:
- **Thriving (70-100):** High activity, driving referrals. Increase posting frequency.
- **Healthy (50-69):** Steady activity. Maintain current effort.
- **Declining (30-49):** Activity dropping. Investigate: is the topic still relevant? Try new content formats.
- **Dead (0-29):** Archive or merge with a related channel. Dead channels make the server feel empty.

The weekly health report (generated by the n8n workflow from `community-health-scoring`) tells you exactly where to invest team time and where to cut.

### 5. Scale member acquisition

Layer these growth channels on top of Baseline's invite sources:

- **Community cross-promotion:** Partner with complementary (non-competing) Discord servers for mutual promotion. Post a resource in their server that links to a discussion in yours. Reciprocate.
- **Content flywheel:** Repurpose the best Discord threads into blog posts, Twitter threads, and LinkedIn posts. Credit the community members who contributed. Each piece links back to the Discord for continued discussion.
- **Product-led invites:** Add a "Discuss this in our community" link on feature pages, changelog entries, and error pages in your product. These are high-intent touchpoints.
- **SEO from Discord threads:** If using Discord's forum channels, high-quality threads can be indexed by Google (if the server has Community features enabled and discovery on). Optimize forum post titles with relevant keywords.

Track acquisition by source using the unique invite links from Baseline. Add new invite links for each new acquisition channel.

### 6. Evaluate after 3 months

Run the `threshold-engine` drill. Collect:

- **Member count and growth trend:** Weekly member counts for the full 3 months. Plot the curve.
- **DAU:** Average unique daily posters over the final 30 days
- **Qualified leads:** Attio contacts where `lead_source = discord-community` AND conversion action completed, for each of the last 2 months separately (must meet threshold in both months)
- **Bot resolution rate:** `bot_reply_confirmed_helpful` / total #help threads
- **Member-to-member reply ratio:** Threads where the first reply is from a non-team member / total threads
- **Channel health scores:** Current score distribution across all channels

Evaluation:

- **PASS (≥ 1,000 members, ≥ 100 DAU, ≥ 30 leads/month for 2 consecutive months):** Document the A/B test results and which variants were adopted. Record the channel health score distribution. Note the bot resolution rate and knowledge base gaps. Calculate the fully-loaded cost per qualified lead (tool costs + team time). Proceed to Durable.
- **MARGINAL (700-999 members or 70-99 DAU or 20-29 leads/month):** Analyze which of the three metrics is lagging. If members but low DAU, the retention/engagement problem: review content quality and bot experience. If DAU but low leads, the conversion problem: review CTA placement and link strategy. If leads but low members, the growth problem: expand acquisition channels.
- **FAIL (< 700 members or < 70 DAU or < 20 leads/month):** Review fundamentals: Is the bot creating a bad experience (wrong answers, too aggressive)? Are Power Users actually more engaged or just more talkative? Is the channel structure confusing new members? Consider a server audit: join as a new member and walk through the experience from scratch.

## Time Estimate

- AI bot development and deployment: 10 hours
- Bot monitoring and knowledge base refinement (ongoing): 8 hours over 3 months
- Member recognition program setup: 3 hours
- A/B test design and execution (4 tests): 8 hours
- Community health scoring workflow: 4 hours
- Content creation (scaled cadence): 10 hours over 3 months
- Growth channel partnerships and integration: 4 hours
- Weekly reviews and optimization: 6 hours (30 min/week x 12 weeks)
- Threshold evaluation: 1 hour
- Total: ~50 hours over 3 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Discord | Community hosting, bot hosting | Free; Nitro for server boosts $9.99/mo optional ([discord.com/nitro](https://discord.com/nitro)) |
| PostHog | Event tracking, experiments (A/B tests), funnels | Free tier: 1M events/mo; Experiments require Growth plan ~$0/mo for <1M events ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Monitoring, health scoring, bot orchestration, member recognition automation | Starter ~$24/mo; Pro $60/mo for higher execution volume ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Lead attribution, member tracking, channel health records | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Anthropic API | AI bot responses in #help | Usage-based ~$3/1M input tokens for Sonnet; expect $5-15/mo at this volume ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Loops | Onboarding emails with Discord invites | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost for Scalable:** $60-150/mo (n8n Pro, Anthropic API usage, existing stack tools)

## Drills Referenced

- `community-health-scoring` — score and rank Discord channels by engagement ROI, detect declining channels, and recommend where to reallocate team effort
- `slack-discord-content-posting` — create value-first content at increased cadence, adapted for A/B test variants
- `ab-test-orchestrator` — design, execute, and evaluate A/B tests on content formats, channel structure, onboarding experience, and CTA placement
