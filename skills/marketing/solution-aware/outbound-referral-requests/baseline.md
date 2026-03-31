---
name: outbound-referral-requests-baseline
description: >
  Outbound Referral Requests — Baseline Run. First always-on referral system with Clay
  enrichment for network mapping, structured PostHog tracking for the full referral funnel,
  and systematic ask cadences across 70 requests over 4 weeks.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Baseline Run"
time: "18 hours over 4 weeks"
outcome: ">=15% intro rate and >=10 qualified intros from 70 requests over 4 weeks"
kpis: ["Request-to-intro rate", "Intro-to-meeting rate", "Days from ask to intro", "Connector response rate"]
slug: "outbound-referral-requests"
install: "npx gtm-skills add marketing/solution-aware/outbound-referral-requests"
drills:
  - referral-network-mapping
  - warm-intro-request
  - posthog-gtm-events
  - threshold-engine
---

# Outbound Referral Requests — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email, Direct

## Outcomes

Prove that outbound referral requests produce a repeatable intro rate at moderate volume. Over 4 weeks, send 70 referral requests and achieve a >=15% intro rate (>=10 actual introductions) with enough quality to book meetings from those intros. This validates that the play works beyond a small manual test and that the intro rate holds as you increase volume.

## Leading Indicators

- Clay enrichment table built with 70+ connector-target pairs scored within the first week
- PostHog tracking firing correctly for all referral funnel events (ask sent, intro received, meeting booked)
- At least 20 asks sent in week 1 with a >=50% open/read rate
- At least 3 intros received by end of week 2 (on pace for 10+ by week 4)
- At least 1 meeting booked from a warm intro by end of week 2
- Connector response rate (any response, positive or negative) >=40%

## Instructions

### 1. Scale the referral network map with Clay

Run the `referral-network-mapping` drill with Clay enrichment enabled. At Baseline, you need 70+ viable connector-target pairs, which requires mapping a larger network:

1. Export all contacts from Attio: customers, advisors, investors, partners, former colleagues, peers. Target: 100-300 contacts.
2. Create a Clay table "Referral Network — Baseline" and import your Attio contacts
3. Create a second Clay table "Referral Targets — Baseline" with 40-50 target accounts (more than 15 because some will have no viable intro path)
4. Use Clay's enrichment waterfall to check employment history, board seats, advisory roles, and mutual LinkedIn connections for every connector-target combination
5. Compute Intro Likelihood (1-10) and Connector Willingness (1-5) scores. Use Clay formula columns for Intro Likelihood based on enrichment data. Connector Willingness remains manual — score based on your relationship strength.
6. Filter to pairs with composite score >=15 (lower threshold than Smoke because you have more volume to test with). You need >=70 viable pairs.
7. Push the top 70+ pairs back to Attio as a list "Referral Map — Baseline"

If you cannot reach 70 pairs, expand your target account list or recruit new connectors (re-engage dormant network contacts, ask advisors for their network introductions).

Estimated time: 4 hours.

### 2. Configure PostHog tracking for the referral funnel

Run the `posthog-gtm-events` drill to set up tracking events for the full referral funnel:

- `referral_ask_sent` — properties: connector_name, target_company, composite_score, channel (email/linkedin), ask_variant (A/B), timestamp
- `referral_ask_opened` — properties: connector_name, channel (email only, via tracking pixel)
- `referral_followup_sent` — properties: connector_name, target_company, days_since_ask
- `referral_intro_received` — properties: connector_name, target_company, response_time_days, intro_channel
- `referral_meeting_booked` — properties: connector_name, target_company, days_from_intro_to_meeting
- `referral_deal_created` — properties: connector_name, target_company, deal_value

Create a PostHog dashboard "Outbound Referral Requests — Baseline" with:
- Referral funnel: ask_sent -> intro_received -> meeting_booked -> deal_created
- Request-to-intro rate over time (weekly)
- Average response time by connector type (customer vs advisor vs investor vs peer)
- Ask variant comparison (A vs B)

Estimated time: 2 hours.

### 3. Generate ask messages at scale

Run the the referral ask copywriting workflow (see instructions below) drill for all 70+ pairs. At Baseline, use Claude to batch-generate:

1. Variant A (Direct ask) and Variant B (Warm-up first) for each pair
2. Forwardable blurb for each pair
3. Quality-check all messages: verify relationship references, confirm blurb is under 60 words, ensure tone matches connector relationship level

Split your 70 asks into A/B test groups: 35 receive Variant A (direct), 35 receive Variant B (warm-up). Track which variant produces a higher intro rate.

Estimated time: 3 hours (batch generation + review).

### 4. Execute the ask cadence

Send asks at a pace of 3-5 per day over 3-4 weeks (not all at once). Follow the `warm-intro-request` drill for execution mechanics:

**Week 1**: Send 20 asks (5/day, Tue-Fri). Start with your highest-scoring pairs.
**Week 2**: Send 20 more asks. Follow up on week 1 non-responses (7-day follow-up).
**Week 3**: Send 20 more asks. Follow up on week 2 non-responses. Handle intros from weeks 1-2.
**Week 4**: Send remaining 10 asks. Complete all follow-ups. Focus on converting intros to meetings.

For each ask:
- Send via the connector's preferred channel
- Log in Attio: date, channel, variant, connector, target
- Fire PostHog event: `referral_ask_sent`
- Set a 7-day follow-up reminder

**Human action required:** Send all asks personally. At Baseline, the founder's name and relationship is what makes these work. Log results for every interaction.

Estimated time: 4 hours (spread over 4 weeks).

### 5. Manage follow-ups systematically

After 7 days with no response, send one follow-up per the `warm-intro-request` drill guidelines. Track:

- How many connectors responded to the follow-up (vs. the initial ask)
- Whether follow-up intros convert at a different rate than first-ask intros
- Which follow-up timing produces the best response (7 days vs. 5 days — test if you have volume)

Fire PostHog event `referral_followup_sent` for each follow-up. If no response after 21 total days (original ask + follow-up), mark as "No Response" and do not send further messages.

Estimated time: 1.5 hours.

### 6. Track and attribute intros

For every intro received:
1. Log `referral_intro_received` in PostHog with response_time_days
2. Update Attio: pair status "Intro Received," deal created in pipeline with source "Warm Intro — {connector name}"
3. Thank the connector within 2 hours
4. Respond to the target within 2 hours
5. Track whether the intro leads to a meeting (fire `referral_meeting_booked`)

Estimated time: 2 hours (across all intros received over 4 weeks).

### 7. Evaluate against threshold

Run the `threshold-engine` drill after 4 weeks. Measure against: >=15% intro rate AND >=10 qualified intros from 70 requests.

Deep analysis:
- **Request-to-intro rate by connector type**: Do customers, advisors, or investors intro at higher rates?
- **Request-to-intro rate by ask variant**: Did Variant A or B win?
- **Response time distribution**: How many days between ask and intro? Is there a cliff (most intros happen within 3 days or never)?
- **Intro-to-meeting conversion**: What percentage of intros led to meetings? This is the quality signal.
- **Composite score accuracy**: Did high-scoring pairs actually convert at higher rates? If not, recalibrate the scoring model.
- **Connector fatigue signal**: Did connectors who received multiple asks (different targets) have declining response rates?

If PASS, proceed to Scalable with documented learnings on what connector types, ask variants, and blurb styles produce the best results.

If FAIL, diagnose whether the issue is: (a) too few viable connector-target pairs (network size problem), (b) low connector willingness (ask quality or relationship problem), (c) connectors acted but intros did not convert (blurb quality or target selection problem). Fix the root cause and re-run.

Estimated time: 1.5 hours.

## Time Estimate

- Network mapping with Clay enrichment: 4 hours
- PostHog tracking setup: 2 hours
- Ask generation and review: 3 hours
- Sending asks (spread over 4 weeks): 4 hours
- Follow-up management: 1.5 hours
- Intro handling and attribution: 2 hours
- Threshold evaluation: 1.5 hours

**Total: ~18 hours over 4 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — connector records, referral map, deal pipeline, intro attribution | Standard stack (excluded) |
| PostHog | Referral funnel tracking, dashboard, A/B variant comparison | Standard stack (excluded) |
| Clay | Network enrichment — employment history, mutual connections, contact data | Launch: $185/mo. Growth: $495/mo. [clay.com/pricing](https://www.clay.com/pricing) |
| LinkedIn | Mutual connection lookup, DM channel for asks | Free (organic features) |

**Play-specific cost: ~$185/mo** (Clay Launch plan sufficient for Baseline volume)

## Drills Referenced

- `referral-network-mapping` — maps your network to targets using Clay enrichment, scores every connector-target pair
- the referral ask copywriting workflow (see instructions below) — batch generates personalized ask messages (2 variants) and forwardable blurbs for all 70+ pairs
- `warm-intro-request` — execution mechanics for sending asks, handling responses, and managing the intro handoff
- `posthog-gtm-events` — configures PostHog tracking for the referral funnel events
- `threshold-engine` — evaluates results against pass/fail threshold and recommends next action
