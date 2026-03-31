---
name: cold-dm-linkedin-twitter-baseline
description: >
  Cold DMs on LinkedIn/Twitter — Baseline Run. First always-on DM outreach system.
  Agent runs LinkedIn and X outreach in parallel with tracking, hitting 200 DMs over
  2 weeks to prove a sustained >=2% meeting rate.
stage: "Marketing > ProblemAware"
motion: "OutboundFounderLed"
channels: "Social"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: ">=2% meeting rate from >=200 DMs over 2 weeks"
kpis: ["Reply rate by channel", "Positive reply rate", "Meeting book rate", "DMs sent per day", "Time to first reply"]
slug: "cold-dm-linkedin-twitter"
install: "npx gtm-skills add marketing/problem-aware/cold-dm-linkedin-twitter"
drills:
  - linkedin-outreach
  - twitter-dm-outreach
  - posthog-gtm-events
  - threshold-engine
---

# Cold DMs on LinkedIn/Twitter — Baseline Run

> **Stage:** Marketing > ProblemAware | **Motion:** OutboundFounderLed | **Channels:** Social

## Outcomes

Run DM outreach continuously on LinkedIn and X for 2 weeks. Send >=200 total DMs using the winning message variants and ICP segments from Smoke. Prove the play sustains a >=2% meeting rate (>=4 meetings from 200 DMs) with structured tracking.

**Pass threshold:** >=2% meeting rate from >=200 DMs over 2 weeks.

## Leading Indicators

- LinkedIn connection acceptance rate: >=30%
- X DM delivery rate (DMs that land, excluding closed-DM profiles): >=80%
- Reply rate (combined): >=12%
- Positive reply rate: >=6%
- First meeting booked within the first 5 days

## Instructions

### 1. Set up LinkedIn outreach system

Run the `linkedin-outreach` drill. Configure a structured connection-and-message sequence targeting your validated ICP:

1. Import the qualified prospect list from Attio (carried over from Smoke, expanded to 150+ LinkedIn contacts via the `build-prospect-list` drill).
2. Segment into Tier 1 (highest fit, heavy personalization) and Tier 2 (good fit, templated with light customization).
3. Execute the pre-engagement warm-up: like 2-3 posts per prospect for 1 week before sending connection requests.
4. Send connection requests at 15-20 per day. Use the connection note variant that performed best in Smoke.
5. Once connected, run a 3-message DM sequence over 10 days:
   - **Message 1 (Day 1 after accept):** Thank them for connecting. Ask a genuine question about their work. No pitch.
   - **Message 2 (Day 5):** Share a relevant insight or data point. Loosely connect to the problem you solve.
   - **Message 3 (Day 10):** Direct but low-pressure CTA. Suggest a 15-minute call. Include cal.com link.

Target: 100+ LinkedIn DMs sent over the 2-week period.

### 2. Set up X DM outreach system

Run the `twitter-dm-outreach` drill. Configure a structured engagement-to-DM sequence:

1. Import 100+ prospects with valid X handles from Clay into Attio.
2. Filter for active X users (posted within last 14 days).
3. Execute the 5-day engagement warm-up sequence per the drill: Day 1-2 likes, Day 3 reply, Day 4 more likes, Day 5 DM.
4. Process 10-15 new prospects per day through the engagement pipeline.
5. Send DMs using the winning message variant from Smoke. Keep under 280 characters, no links, reference specific content.

Target: 100+ X DMs sent over the 2-week period.

### 3. Configure event tracking

Run the `posthog-gtm-events` drill. Set up these events in PostHog:

| Event | Trigger | Properties |
|-------|---------|------------|
| `dm_engagement_started` | First like/comment on prospect content | channel, prospect_id, icp_segment |
| `dm_connection_sent` | LinkedIn connection request sent | prospect_id |
| `dm_connection_accepted` | LinkedIn connection accepted | prospect_id, days_to_accept |
| `dm_sent` | DM delivered on either platform | channel, prospect_id, message_variant, sequence_step |
| `dm_replied` | Prospect responded | channel, prospect_id, sentiment, response_time_hours |
| `dm_meeting_booked` | Meeting scheduled | channel, prospect_id, deal_value_estimate |

Connect PostHog to Attio via n8n webhook: when `dm_meeting_booked` fires, automatically create a deal in Attio at "Meeting Booked" stage with source = "cold-dm-baseline" and channel property.

### 4. Execute outreach (14 days)

**Human action required:** The founder executes LinkedIn engagement and DMs manually (or uses LinkedIn Sales Navigator for assisted workflow). X outreach can be partially automated via PhantomBuster for likes, but DMs should be sent manually at this stage to maintain quality and learn what works.

Daily routine (60 min/day):
- 20 min: LinkedIn engagement (likes, comments on prospect posts)
- 10 min: LinkedIn DMs (send new messages, respond to replies)
- 20 min: X engagement (likes, replies to prospect posts)
- 10 min: X DMs (send new messages, respond to replies)

Log every interaction in Attio. Track which message variant each prospect received.

### 5. Monitor and adjust mid-flight

At the end of week 1, pull interim metrics from PostHog:
- DMs sent so far (target: >=100 at halfway point)
- Reply rate by channel
- Positive reply rate by message variant

If reply rate on either channel is below 8% after 50+ DMs:
- Review message copy: is it too long, too generic, or too aggressive?
- Check targeting: are you reaching active users who match your ICP?
- Swap in the next-best message variant from Smoke and continue.

### 6. Evaluate against threshold

Run the `threshold-engine` drill at the end of week 2. Pull from PostHog and Attio:
- Total DMs sent (target: >=200)
- Reply rate by channel
- Meetings booked
- Meeting rate = meetings booked / DMs sent

**Pass:** >=2% meeting rate (>=4 meetings from 200 DMs).
**Fail:** <2% meeting rate.

If PASS: document per-channel metrics. Identify which channel, message variant, and ICP segment produced the most meetings per DM. These inform Scalable automation.

If FAIL: diagnose by channel.
- LinkedIn low? Connection acceptance may be the bottleneck. Improve profile and connection note.
- X low? Prospects may not check DMs. Check if DM-closed rate is high (>30%). Consider focusing more on LinkedIn.
- Both low? ICP may not respond to DMs. Re-evaluate whether this play is right for your market.

## Time Estimate

- Prospect list expansion and setup: 2 hours
- Drill configuration (LinkedIn outreach + X DM outreach + PostHog events): 2 hours
- Daily execution (60 min/day x 10 business days): 10 hours total (spread over 2 weeks)
- Mid-flight review: 0.5 hours
- Threshold evaluation: 0.5 hours
- **Total: ~15 hours over 2 weeks** (12 hours net execution + 3 hours setup)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Sales Navigator | Advanced search, InMail, connection tracking | $119.99/mo ([pricing](https://business.linkedin.com/sales-solutions/compare-plans)) |
| X (free account) | DMs and engagement | Free |
| Clay | Prospect enrichment, X handle lookup | Explorer: $149/mo for 2,000 credits ([pricing](https://www.clay.com/pricing)) |
| Attio | CRM, deal tracking | Free tier up to 3 users ([pricing](https://attio.com/pricing)) |
| PostHog | Event tracking, funnels | Free tier: 1M events/mo ([pricing](https://posthog.com/pricing)) |
| n8n | Webhook automation (PostHog to Attio) | Free self-hosted / $20/mo cloud ([pricing](https://n8n.io/pricing)) |

**Total play-specific cost: ~$120-270/mo** (LinkedIn Sales Navigator is the primary cost)

## Drills Referenced

- `linkedin-outreach` -- structured LinkedIn connection and messaging sequence
- `twitter-dm-outreach` -- structured X engagement-to-DM sequence
- `posthog-gtm-events` -- event taxonomy and tracking setup for DM funnel
- `threshold-engine` -- evaluate pass/fail against 2% meeting rate threshold
