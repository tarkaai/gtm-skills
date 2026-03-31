---
name: outbound-email-li-calls-baseline
description: >
  Outbound Email/LI/Calls — Baseline Run. First always-on automation of the
  multi-channel outbound sequence. Cold email via Instantly, LinkedIn via
  automation tool, phone calls via structured blocks. Targeting 200+ contacts
  over 2 weeks to prove repeatable ≥ 2% meeting rate.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 2% meeting rate over 2 weeks"
kpis: ["Reply rate", "Meeting rate", "Connect rate"]
slug: "outbound-email-li-calls"
install: "npx gtm-skills add marketing/solution-aware/outbound-email-li-calls"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - cold-call-framework
  - posthog-gtm-events
---

# Outbound Email/LI/Calls — Baseline Run

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Outcomes

The Baseline Run is the first always-on automated version of this play. Email sequences run in Instantly, LinkedIn outreach follows a structured cadence, and phone calls are executed in daily blocks. The agent coordinates timing across channels so the same prospect receives a coherent multi-touch experience. Success: **≥ 2% meeting rate** from 200+ contacts over 2 weeks.

## Leading Indicators

- Email open rate above 50% (validates deliverability and subject lines)
- Email reply rate above 5% (validates copy resonance)
- LinkedIn connection acceptance rate above 25%
- Call connect rate above 15%
- Positive sentiment ratio above 3:1 across all channels
- First meeting booked within 5 business days of campaign launch

## Instructions

### 1. Set up cold email infrastructure in Instantly

Run the `cold-email-sequence` drill. This involves:

1. Verify sending domains are healthy: SPF, DKIM, DMARC configured and passing. Check warmup status — each sending account needs at least 2 weeks of warmup. Use the `instantly-warmup` fundamental.
2. Write the 3-step founder email sequence using the copy validated in Smoke. Personalize the first line of each email using Clay enrichment variables (`{{personalization_line}}`, `{{company_name}}`, `{{pain_point}}`). Use the `instantly-campaign` fundamental to create the campaign.
3. Import the prospect list from Clay to Instantly with all merge fields mapped.
4. Set sending schedule: weekdays, 8-11am in prospect's timezone. Start at 20 sends/day per account and ramp after 3 days.
5. Configure reply detection: positive replies route to Attio as hot leads, negative replies flag for no-recontact.

### 2. Launch LinkedIn outreach in parallel

Run the `linkedin-outreach` drill:

1. Segment your prospect list by tier. Tier 1 (highest-fit): personalize connection note heavily. Tier 2: use templates with light customization.
2. Pre-engage with Tier 1 prospects: like 2-3 recent posts, leave a thoughtful comment. Spend 15 minutes daily for 3-5 days before sending connection requests.
3. Send connection requests at 15-20 per day max. Use the `linkedin-organic-engagement` fundamental. Connection note under 200 characters, referencing something specific about the prospect.
4. After connection accepted, run a 2-message follow-up sequence: Message 1 (Day 1 after accept) — ask a genuine question. Message 2 (Day 5) — soft CTA for a 15-minute call with Cal.com booking link.
5. Track acceptance and reply rates in Attio using the `attio-deals` fundamental.

**Coordinate timing**: Do NOT send a LinkedIn connection request and cold email on the same day to the same prospect. Stagger by 1-2 days. LinkedIn Day 2, Email Day 1, Call Day 5-6.

### 3. Execute structured call blocks

Run the `cold-call-framework` drill:

1. Pull the highest-priority prospects from your Attio pipeline: prospects who opened emails 3+ times, accepted LinkedIn connections, or have strong buying signals.
2. Pre-call research: 60 seconds per prospect — check LinkedIn headline, the signal that triggered outreach, and any prior touchpoints logged in Attio.
3. Execute calls in 60-minute daily blocks. Target 20-30 calls per block. Reference your email: "I sent you a note earlier this week about [topic]."
4. Log every call outcome in Attio immediately: connected/voicemail/gatekeeper, duration, disposition (meeting set, follow-up, not interested, call back).
5. If a prospect already replied positively on email or LinkedIn, skip the cold call — they are already in your pipeline.

### 4. Configure PostHog event tracking

Run the `posthog-gtm-events` drill to set up the outbound event taxonomy:

- `email_sent`, `email_opened`, `email_replied` — with campaign_id, sequence_step, subject_variant
- `linkedin_connection_sent`, `linkedin_connection_accepted`, `linkedin_message_replied`
- `call_attempted`, `call_connected`, `call_meeting_booked`
- `meeting_booked` — with source_channel (email/linkedin/call), first_touch_channel, last_touch_channel

Connect PostHog to Attio via n8n webhook so deal stage changes are tracked automatically. Connect Instantly to PostHog to log email events.

### 5. Monitor and adjust mid-flight

After Week 1, review metrics:
- If email reply rate is below 3%: rewrite subject lines and opening line. Test a different pain point angle.
- If LinkedIn acceptance is below 20%: check if your LinkedIn profile headline speaks to their pain. Simplify connection notes.
- If call connect rate is below 10%: shift call times (try 8-9am or 4-5pm). Use local presence dialing if available.
- If getting replies but not meetings: your CTA is weak. Make the ask more specific and lower-friction.

### 6. Evaluate against threshold

After 2 weeks, pull the full funnel from PostHog and Attio:
- Total prospects contacted (target: 200+)
- Meetings booked across all channels
- Meeting rate = meetings / prospects contacted

**Pass threshold: ≥ 2% meeting rate** (≥ 4 meetings from 200 contacts).

- **PASS**: Document the winning message variants, best-performing channels, and ICP segments. Proceed to Scalable.
- **FAIL**: Diagnose — targeting (wrong ICP), messaging (low reply rate), channel (replies but no meetings), or timing (wrong time of day/week). Fix the weakest link and re-run Baseline.

Record per-channel attribution: which channel was first touch and last touch for each booked meeting.

## Time Estimate

- Email setup and sequence creation: 2 hours
- LinkedIn outreach setup and pre-engagement: 3 hours (spread over first week)
- Call block execution: 5 hours (30-60 min/day over 2 weeks)
- PostHog tracking setup: 1 hour
- Monitoring and evaluation: 1 hour

Total: ~12 hours over 2 weeks.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Cold email sequences | Growth: $30/mo for 5000 contacts (https://instantly.ai/pricing) |
| Clay | Enrichment + personalization variables | Pro: $149/mo (https://www.clay.com/pricing) |
| Apollo | Contact sourcing | Basic: $49/mo (https://www.apollo.io/pricing) |
| Attio | CRM deal tracking | Plus: $29/user/mo (https://attio.com/pricing) |
| LinkedIn Sales Navigator | Prospecting | Core: $99.99/mo (https://business.linkedin.com/sales-solutions/compare-plans) |
| PostHog | Event tracking | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Cal.com | Booking links | Free tier available (https://cal.com/pricing) |

**Estimated play-specific cost: ~$260-430/mo** (Instantly + Clay + Apollo + LinkedIn Sales Nav)

## Drills Referenced

- `cold-email-sequence` — build and launch the 3-step Instantly email campaign with personalization
- `linkedin-outreach` — run the structured LinkedIn connection + messaging sequence
- `cold-call-framework` — structure and execute daily call blocks with CRM logging
- `posthog-gtm-events` — set up the standardized event taxonomy for all 3 channels
