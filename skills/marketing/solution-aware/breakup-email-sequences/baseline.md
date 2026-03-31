---
name: breakup-email-sequences-baseline
description: >
  Breakup Email Sequences — Baseline Run. First always-on automation: breakup emails
  run through Instantly to 100-200 silent prospects with Clay signal detection,
  conditional step delivery based on opens, and PostHog funnel tracking. Validates
  that Smoke re-engagement rates hold at scale over 2 weeks.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 5% re-engagement rate from 150+ breakup emails over 2 weeks with ≥ 1 meeting booked"
kpis: ["Re-engagement rate (target ≥ 5%)", "Signal lift (signal-detected rate vs. no-signal rate)", "Asset conversion rate (asset requests that convert to meetings)", "Bounce rate (target < 2%)"]
slug: "breakup-email-sequences"
install: "npx gtm-skills add marketing/solution-aware/breakup-email-sequences"
drills:
  - breakup-email-copy
  - cold-email-sequence
  - posthog-gtm-events
---

# Breakup Email Sequences — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email

## Outcomes

Move from manual breakup sends (Smoke) to automated delivery at 150+ contacts while maintaining the re-engagement rate. The breakup copy and loss-aversion framing remain the same — what changes is that Instantly handles sending and conditional step logic, Clay handles signal detection at scale, and PostHog tracks the full re-engagement funnel. The founder only handles positive replies.

Pass: 5% or higher re-engagement rate (positive replies / breakup emails sent) from at least 150 breakup emails over 2 weeks, with at least 1 meeting booked from a breakup-recovered prospect.
Fail: Below 5% re-engagement rate after 2 full weeks with 150+ sends, or zero meetings booked.

## Leading Indicators

- Bounce rate stays below 2% (confirms email addresses are still valid despite 30-90 day gap since last contact)
- Signal-detected prospects re-engage at ≥ 2x the rate of no-signal prospects (validates the signal enrichment investment)
- At least 1 "send it" reply to Email 2 within the first 50 sends (the low-friction CTA is working)
- No spam complaints (breakup emails should feel personal, not mass-produced)

## Instructions

### 1. Build the silent prospect pool at scale

Use the `attio-contacts` fundamental to pull all prospects meeting breakup criteria:

- Completed a prior outbound sequence without replying
- Last touch 30-90 days ago
- Not in any active sequence or deal
- Not marked "Do Not Contact"

Export to a Clay table. Target 200+ prospects (over-build by 30% because signal detection and verification will filter some).

### 2. Run signal detection via Clay

Using the `breakup-email-copy` drill's segmentation step, configure Clay to check each prospect for signals that occurred after they went silent:

- **Job change detection:** Use Clay's People Data Labs integration to check if the prospect changed roles. A new role = fresh context, higher breakup reply probability.
- **Company funding:** Use Crunchbase enrichment to check for funding events at the prospect's company.
- **Hiring signals:** Use Clay's job board integration to check if the company posted roles in your product's domain.
- **LinkedIn activity:** Use Clay's LinkedIn enrichment to check for recent posts or engagement related to your problem space.

For each prospect, populate `recent_signal` (the signal description or null) and `signal_relevance` (one sentence connecting the signal to your product's value). Use the `clay-claygent` fundamental for the AI-generated relevance line.

Target: 20-30% of prospects should have a detectable signal.

### 3. Write and load the breakup sequence

Run the `breakup-email-copy` drill to produce the full sequence. At Baseline, you have two campaigns:

**Campaign 1: Signal-detected breakup (3-step)**
- Email 1: Signal-referenced close (Day 0)
- Email 2: Low-friction asset offer, conditional on Email 1 open (Day 4)
- Email 3: Signal value delivery, conditional on Email 1 or 2 open (Day 7)

**Campaign 2: Standard breakup (2-step)**
- Email 1: Honest close (Day 0)
- Email 2: Low-friction asset offer, conditional on Email 1 open (Day 5)

Using the `cold-email-sequence` drill's Instantly setup steps, load both campaigns:

- Map Clay personalization variables: `{{firstName}}`, `{{companyName}}`, `{{prior_sequence_topic}}`, `{{recent_signal}}`, `{{signal_relevance}}`, `{{low_friction_asset}}`
- Set sending schedule: Tuesday-Thursday, 8-10am in the prospect's timezone
- Set daily limit: 25-30 per sending account
- Enable open tracking on Email 1 (needed for conditional step logic)
- Configure conditional delivery: Email 2 only sends if Email 1 was opened; Email 3 only sends if Email 1 or 2 was opened

Use the existing warmed sending accounts from your outbound infrastructure. Do NOT warm up new accounts just for breakup sends — breakups use the same sender identity as the original sequence for continuity.

### 4. Configure PostHog event tracking

Run the `posthog-gtm-events` drill to set up event tracking specific to breakup sequences. Configure these events via Instantly webhooks routed through n8n:

- `breakup_sent` with properties: `{source: "breakup-email-sequences", level: "baseline", step: 1|2|3, segment: "signal"|"no-signal", campaign_id}`
- `breakup_opened` with properties: `{source: "breakup-email-sequences", step: 1|2|3, segment: "signal"|"no-signal"}`
- `breakup_replied` with properties: `{source: "breakup-email-sequences", sentiment: "positive|negative|neutral", reply_type: "meeting_interest|asset_request|maybe_later|remove", segment: "signal"|"no-signal"}`
- `breakup_meeting_booked` with properties: `{source: "breakup-email-sequences", level: "baseline", days_from_breakup_send, original_sequence_slug}`
- `breakup_asset_sent` with properties: `{source: "breakup-email-sequences", asset_type, segment}`

Create a PostHog funnel: `breakup_sent` -> `breakup_opened` -> `breakup_replied (positive)` -> `breakup_meeting_booked`. Create a second funnel for the asset path: `breakup_sent` -> `breakup_replied (asset_request)` -> `breakup_asset_sent` -> `breakup_meeting_booked`.

### 5. Launch and monitor

Activate both campaigns. Send to the signal-detected campaign first (Day 1). Launch the standard campaign on Day 2. Monitor daily:

- Check Instantly Unibox for replies. Classify each reply and update Attio.
- Check bounce rate after the first 50 sends. If above 2%, pause and investigate — email addresses may have gone stale since the original outreach. Run the `clay-email-verification` fundamental on the remaining unsent list.
- Check that conditional step delivery is working correctly — Email 2 should only go to openers.

**Human action required:** The founder responds to positive replies within 2 hours. At Baseline volume (150 contacts), expect 8-15 positive replies over 2 weeks. Handle each reply type per the Smoke-level instructions: meeting interest gets calendar times, asset requests get the resource + 3-day follow-up, "maybe later" gets a 90-day reminder.

For every meeting booked from a breakup reply, create a deal in Attio with tags: `source: breakup-email-sequences`, `breakup_segment: signal|no-signal`, `original_sequence: [prior play slug]`.

### 6. Evaluate results after 2 weeks

Pull PostHog funnel data. Compute:

- Blended re-engagement rate = positive replies / total breakup emails sent
- Signal-detected re-engagement rate vs. no-signal re-engagement rate
- Signal lift = signal rate / no-signal rate (target: ≥ 2x)
- Asset conversion rate = meetings booked from asset requests / asset requests
- Bounce rate = bounced / total sent
- Latent interest ratio = replies from prospects who never opened any prior sequence email / total positive replies

- **PASS (≥ 5% re-engagement rate, ≥ 1 meeting booked):** Baseline is proven. Document: which signals produced the most re-engagement, whether the asset CTA or the direct close performed better, the optimal gap between original sequence end and breakup send. Proceed to Scalable.
- **MARGINAL (3-4.9% re-engagement rate OR 0 meetings from 5+ positive replies):** The re-engagement works but conversion is weak. Diagnose: Are positive replies actually "meeting interest" or just polite acknowledgments? Is the low-friction asset converting to meetings? Tighten the reply classification, improve the asset, and re-run with 100 fresh silent prospects.
- **FAIL (< 3% re-engagement rate):** The automated version underperforms the manual Smoke test. Diagnose: Did the breakup emails land in spam (check Instantly deliverability)? Did the personalization feel templated at scale? Was the sending domain different from the original outreach (breaking continuity)? Fix the root cause and re-run.

## Time Estimate

- Silent prospect pool extraction and Clay signal detection: 3 hours
- Breakup email copywriting and Instantly campaign setup: 2 hours
- PostHog event tracking configuration: 2 hours
- Campaign launch and test batch review: 1 hour
- Reply management over 2 weeks: 2 hours total
- Results evaluation: 2 hours
- Total: ~12 hours over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Breakup email sending, conditional steps, open tracking | Growth plan $37/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Signal detection, enrichment, email verification | Launch plan $185/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM, reply tracking, deal attribution | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Funnel tracking, event logging | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Webhook routing from Instantly to PostHog | Starter $24/mo or self-host free ([n8n.io/pricing](https://n8n.io/pricing)) |
| Cal.com | Meeting booking for re-engaged prospects | Free plan ([cal.com/pricing](https://cal.com/pricing)) |

**Estimated monthly cost for Baseline:** ~$246/mo (uses existing sending infrastructure from prior outbound)

## Drills Referenced

- `breakup-email-copy` — write the 2-3 step breakup sequence with signal vs. no-signal variants and conditional step logic
- `cold-email-sequence` — Instantly campaign setup, sending configuration, and merge field mapping
- `posthog-gtm-events` — configure breakup-specific event tracking and funnel measurement
