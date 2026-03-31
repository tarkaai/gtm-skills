---
name: demo-follow-up-sequence-baseline
description: >
  Demo Follow-Up Sequence — Baseline Run. First always-on follow-up cadence using Instantly/Loops
  for sequenced email delivery, PostHog for engagement tracking, and structured content selection
  per deal. Agent assembles recaps and queues follow-up touches; founder approves sends.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Baseline Run"
time: "15 hours over 2 weeks"
outcome: ">=80% of demos followed up with structured sequence over 2 weeks, >=55% scheduling next step within 10 days"
kpis: ["Sequence completion rate", "Response rate by touch number", "Next step conversion rate", "Time from demo to next step (days)", "Resource engagement rate by asset type"]
slug: "demo-follow-up-sequence"
install: "npx gtm-skills add sales/connected/demo-follow-up-sequence"
drills:
  - demo-recap-assembly
  - demo-follow-up-cadence
  - posthog-gtm-events
---

# Demo Follow-Up Sequence — Baseline Run

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Email, Direct

## Outcomes

Move from manual follow-up execution to a repeatable, tool-assisted cadence. The agent assembles recaps and queues the full multi-touch sequence in Instantly or Loops. The founder approves and monitors. Every touch is tracked in PostHog, producing data on which touches, timing, and content types drive the highest next-step conversion.

**Pass threshold:** >=80% of demos followed up with structured sequence over 2 weeks, >=55% scheduling next step within 10 days.

## Leading Indicators

- Recap emails queued within 20 minutes of transcript availability for >=90% of demos
- Sequence completion rate >=85% (touches 0-4 all sent unless prospect responded first)
- Day 3 value asset click-through rate >=25%
- Average time from demo to next-step booking decreasing week-over-week
- Response rate on engagement-based touches (Day 5-7) higher than generic time-based touches

## Instructions

### 1. Set Up PostHog Event Tracking

Run the `posthog-gtm-events` drill to establish the event taxonomy for demo follow-ups. Configure these specific events:

| Event | When Fired | Key Properties |
|-------|-----------|----------------|
| `demo_recap_assembled` | Agent generates recap | `deal_id`, `features_covered`, `questions_addressed`, `urgency_level` |
| `demo_follow_up_sent` | Each follow-up touch sent | `deal_id`, `touch_number`, `touch_type`, `channel`, `personalized` |
| `demo_follow_up_opened` | Prospect opens follow-up email | `deal_id`, `touch_number` |
| `demo_follow_up_clicked` | Prospect clicks a link in follow-up | `deal_id`, `touch_number`, `asset_type`, `link_url` |
| `demo_follow_up_replied` | Prospect replies to any touch | `deal_id`, `touch_number`, `sentiment` |
| `next_step_booked` | Prospect books next meeting | `deal_id`, `next_step_type`, `touches_to_book`, `days_since_demo` |
| `follow_up_sequence_completed` | Sequence ends (any reason) | `deal_id`, `outcome`, `total_touches_sent`, `total_responses` |

Connect PostHog to Attio via webhook so deal properties update automatically when events fire.

### 2. Run Demo Recap Assembly for Every Demo

Run the `demo-recap-assembly` drill after each demo, same as Smoke. The difference at Baseline: the agent now also prepares the full 5-touch cadence content (not just the recap) based on the demo extraction.

For each demo, the agent produces:
- Touch 0: Personalized recap email (same as Smoke)
- Touch 1: Check-in email with unanswered question answers
- Touch 2: Value asset email matched to demo context
- Touch 3: Engagement-based email (high-engagement and low-engagement variants)
- Touch 4: Momentum check email

All content is stored as Attio deal notes, tagged by touch number.

### 3. Configure Follow-Up Delivery via Instantly or Loops

Run the `demo-follow-up-cadence` drill to set up sequenced email delivery:

**Option A — Loops (recommended for warm contacts):**
Create a Loops transactional sequence for demo follow-ups. Each touch is a separate transactional email triggered by the agent at the scheduled time. Merge fields pull from Attio deal data. Use Loops for its deliverability advantage with warm contacts.

**Option B — Instantly (for higher volume):**
Create an Instantly campaign template for demo follow-ups. Upload each deal's cadence content as a personalized sequence. Set the timing: Day 0, Day 1, Day 3, Day 5-7, Day 10. Enable open and click tracking.

For either option:
- Configure reply detection to pause the sequence immediately on any response
- Set up tracking links on all resource URLs
- Enable open tracking to inform the Day 5-7 engagement-based touch

**Human action required:** Review the agent-generated cadence content for each deal before approving the sequence to send. At Baseline, every sequence should be reviewed before launch — automation without review comes at Scalable.

### 4. Execute Engagement-Based Branching

At the Day 5-7 touch, the cadence branches based on prospect engagement:

1. Pull engagement data: email opens, link clicks (from Instantly/Loops tracking), Loom video views (from Loom analytics), website visits (from PostHog)
2. If prospect showed high engagement (opened >=2 emails AND clicked >=1 link OR watched recap video >50%): send the "propose next step directly" variant
3. If prospect showed low engagement (no opens, no clicks): send the "different angle" variant
4. Log which branch was taken in PostHog for later analysis

### 5. Monitor Cadence Performance

Track these metrics daily:
- Sequences active vs completed this week
- Response rate by touch number (which touch gets the most replies?)
- Asset engagement by type (which resources get clicked?)
- Average touches before next-step booking
- Sequence exit reasons (positive reply, negative reply, booked meeting, no response)

Log findings in Attio as a campaign note weekly. Identify:
- The "magic touch" — the touch number with the highest response rate
- The strongest asset type — which resource drives the most engagement
- Timing patterns — are certain days/times producing more responses

### 6. Evaluate Against Threshold

After 2 weeks of running the cadence on all demos:

1. Count total demos in the evaluation window
2. Count demos with a completed follow-up sequence (>=4 touches sent or early exit due to response)
3. Calculate: sequence coverage rate, response rate, next-step booking rate
4. Compare against threshold: >=80% coverage AND >=55% next-step booking rate

If PASS: The always-on cadence is producing consistent results. Proceed to Scalable to automate the trigger-to-send pipeline and add A/B testing.
If FAIL: Diagnose by touch — which touch has the lowest response rate? Is the issue delivery (emails not getting opened), content (opened but not clicked), or conversion (engaged but not booking)? Fix the weakest link and re-run.

## Time Estimate

- 2 hours: Set up PostHog event tracking and Instantly/Loops configuration
- 8 hours: Run demo-recap-assembly + review and approve cadences (~45 min per demo x 10-12 demos)
- 3 hours: Daily monitoring and weekly analysis
- 2 hours: Threshold evaluation and cadence refinement

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies | Demo call transcription | Free (800 min/mo) or $18/user/mo Pro — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Attio | CRM — deal tracking, cadence content storage | Free or $29/user/mo Plus — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Event tracking, engagement monitoring | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Transactional email delivery for warm follow-ups | Free (1K contacts) or $49/mo (5K contacts) — [loops.so/pricing](https://loops.so/pricing) |
| Instantly | Alternative: sequenced email with tracking | $37/mo Growth or $97/mo Hypergrowth — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Cal.com | Booking links in follow-up emails | Free or $12/user/mo — [cal.com/pricing](https://cal.com/pricing) |
| Loom | Optional recap video with view analytics | Free or $15/user/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |

**Estimated play-specific cost this level:** ~$37-49/mo (Instantly Growth or Loops paid plan). Fireflies Pro if exceeding free tier: +$18/mo. Total: ~$55-67/mo.

## Drills Referenced

- `demo-recap-assembly` — extract demo signals from transcript and generate personalized recap + full cadence content
- `demo-follow-up-cadence` — execute the structured multi-touch follow-up sequence with engagement-based branching
- `posthog-gtm-events` — set up the event taxonomy for tracking every follow-up touch and outcome
