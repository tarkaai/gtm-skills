---
name: analyst-consultant-briefings-baseline
description: >
  Analyst & Consultant Briefings — Baseline Run. Systematize the briefing pipeline with CRM tracking,
  event instrumentation, and a repeatable outreach cadence. First always-on automation: briefing
  request sequences and meeting booking flows. Target >=2 intro meetings over 2 weeks.
stage: "Sales > Qualified"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: ">=2 analyst briefing meetings completed AND >=1 follow-up request from an analyst over 2 weeks"
kpis: ["Briefings completed", "Follow-up requests from analysts", "Briefing request acceptance rate", "Time from outreach to meeting"]
slug: "analyst-consultant-briefings"
install: "npx gtm-skills add sales/qualified/analyst-consultant-briefings"
drills:
  - warm-intro-request
  - posthog-gtm-events
  - meeting-booking-flow
---

# Analyst & Consultant Briefings — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Outcomes

Prove the analyst briefing pipeline is repeatable and measurable. At Baseline, you instrument every step (outreach sent, briefing scheduled, briefing completed, follow-up requested), activate warm intro paths through your network, and set up a proper meeting booking flow. The shift from Smoke: you now track everything in PostHog and Attio, and use warm introductions as the primary outreach channel.

**Pass threshold:** >=2 analyst briefing meetings completed AND >=1 follow-up request from an analyst over 2 weeks.

## Leading Indicators

- Warm intro request-to-introduction rate (target: >=30% — connectors willing to make intros)
- Briefing request acceptance rate (target: >=35% with warm intros vs. >=20% cold)
- Analyst engagement depth: do they ask for product access, customer references, or additional materials?
- Meeting no-show rate (target: <10% — analysts who commit should show up)

## Instructions

### 1. Activate warm intro paths

Run the `warm-intro-request` drill to systematically find mutual connections who can introduce you to target analysts. For each Priority 1 and Priority 2 analyst from your Attio list:
- Check LinkedIn mutual connections
- Query Attio for contacts who work at the analyst's firm or have interacted with them
- Check if existing customers, investors, or advisors have relationships with the analyst

For each warm path found, craft a short intro request: explain why you want the briefing (not "to sell them"), what value the briefing offers the analyst (early access to your market data, perspective on a trend they cover), and a pre-written forwardable message the connector can copy-paste.

Send warm intro requests via LinkedIn DM or email. Track each request in Attio: connector name, analyst target, date sent, status.

### 2. Instrument the briefing pipeline in PostHog

Run the `posthog-gtm-events` drill to configure tracking events for the analyst briefing funnel:
- `analyst_outreach_sent` — briefing request sent (properties: analyst_name, analyst_tier, outreach_channel, warm_or_cold)
- `analyst_briefing_scheduled` — meeting booked (properties: analyst_name, meeting_date, days_from_outreach)
- `analyst_briefing_completed` — meeting happened (properties: analyst_name, analyst_tier, engagement_score, follow_up_requested)
- `analyst_followup_requested` — analyst asked for more info, product access, or next meeting (properties: analyst_name, request_type)
- `analyst_referral_received` — analyst referred a prospect (properties: analyst_name, prospect_name, referral_quality)

These events enable threshold checking, funnel analysis, and the monitoring that Scalable and Durable levels depend on.

### 3. Set up the meeting booking flow

Run the `meeting-booking-flow` drill to create an end-to-end booking experience for analyst briefings:
- Create a Cal.com "Analyst Briefing" event type (30 minutes, 15-minute buffer)
- Connect Cal.com to Attio via n8n: when a briefing is booked, update the analyst's record with meeting date and status
- Fire a `analyst_briefing_scheduled` PostHog event on booking
- Auto-send the briefing document and agenda in the Cal.com confirmation email

### 4. Expand outreach to 10-15 analysts

Using your scored Attio list from Smoke, send briefing requests to 10-15 analysts across Tier 2-4. Prioritize warm intros (from step 1) for Tier 2 analysts. Use direct outreach for Tier 3-4 independents who accept briefings more readily.

For each analyst without a warm path, send the personalized briefing request prepared in Smoke. Update each with current metrics and recent publications.

**Human action required:** Conduct each briefing personally. Use the same agenda structure from Smoke. After each briefing, log an `analyst_briefing_completed` event with an engagement score (1-5) and whether the analyst requested follow-up.

### 5. Process follow-up requests

When an analyst requests follow-up (additional materials, product access, customer references, or a second meeting):
- Fulfill the request within 48 hours
- Log it as an `analyst_followup_requested` event in PostHog
- Update the analyst's Attio record: Briefing Status = "Engaged"
- Schedule a follow-up touchpoint in 2 weeks

Follow-up requests are the strongest signal that an analyst will become a referral source. Prioritize these analysts above all others.

### 6. Evaluate against threshold

Measure against: >=2 briefing meetings completed AND >=1 follow-up request over 2 weeks.

If PASS: Document which outreach channels (warm intro vs. cold) had the highest acceptance rate. Note which analyst tiers are most responsive. Proceed to Scalable.

If FAIL: Diagnose by checking the funnel in PostHog. Where is the drop-off? If outreach-to-scheduled is low, improve messaging or switch to more warm intros. If scheduled-to-completed is low (no-shows), confirm meetings more aggressively. If completed but no follow-ups, the briefing content may not be resonating — adjust positioning or discussion topics.

## Time Estimate

- 3 hours: Map warm intro paths and send intro requests
- 2 hours: Configure PostHog events and meeting booking flow
- 2 hours: Prepare and send 10-15 briefing requests
- 3 hours: Conduct 2-4 briefing meetings (30 min each + prep)
- 2 hours: Process follow-ups, log outcomes, evaluate threshold

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM for analyst records and pipeline tracking | Free tier or existing plan — [attio.com](https://attio.com) |
| PostHog | Event tracking for briefing funnel | Free tier (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Briefing meeting scheduling | Free tier (1 event type) — [cal.com/pricing](https://cal.com/pricing) |
| n8n | Workflow automation (Cal.com → Attio sync) | Free self-hosted or $24/mo cloud — [n8n.io/pricing](https://n8n.io/pricing) |
| Claude API | Briefing document generation | ~$0.03-0.05 per document — [anthropic.com](https://console.anthropic.com) |

**Estimated play-specific cost:** $0-50/mo (free tiers cover most needs at this volume)

## Drills Referenced

- `warm-intro-request` — Maps mutual connections and requests warm introductions to target analysts
- `posthog-gtm-events` — Defines and implements the event taxonomy for the briefing funnel
- `meeting-booking-flow` — Creates the Cal.com → Attio → PostHog booking pipeline
