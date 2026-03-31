---
name: account-based-cold-calling-baseline
description: >
  Account-Based Cold Calling — Baseline Run. First always-on automation: agent continuously enriches
  new prospects, generates call scripts, logs outcomes to CRM, and produces weekly performance
  reports. Founder executes 150 calls over 2 weeks through a cloud dialer with CRM-synced logging
  and voicemail drop. Validates that the signal-to-meeting pipeline sustains at >=3% call-to-meeting
  rate with always-on prospect sourcing.
stage: "Marketing > Solution Aware"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=3% call-to-meeting rate from 150 calls over 2 weeks with cloud dialer"
kpis: ["Connect rate", "Call-to-meeting rate", "Cost per meeting", "Average call duration", "Best call window (day/time)"]
slug: "account-based-cold-calling"
install: "npx gtm-skills add marketing/solution-aware/account-based-cold-calling"
drills:
  - build-prospect-list
  - enrich-and-score
  - cold-call-framework
  - cold-email-sequence
  - posthog-gtm-events
  - threshold-engine
---

# Account-Based Cold Calling — Baseline Run

> **Stage:** Marketing > Solution Aware | **Motion:** OutboundFounderLed | **Channels:** Direct

## Outcomes

First always-on automation layer for account-based cold calling. The agent continuously sources and enriches new prospects, generates personalized scripts, and tracks all call outcomes. A cloud dialer replaces manual dialing, adding call recording, voicemail drop, and automatic CRM logging. A pre-call email warms prospects so the cold call is not truly cold. After 150 calls over 2 weeks, sustained call-to-meeting rate of >=3% proves the pipeline works with automation backing it.

## Leading Indicators

- Cloud dialer (Aircall or Orum) configured with CRM sync to Attio within first 2 days
- Prospect pipeline continuously producing 15+ new scored, phone-verified contacts per day
- Pre-call email sequence launching automatically when a prospect enters the call queue
- Call recordings flowing to Fireflies for transcription
- PostHog dashboard showing daily call volume, connect rate, and meeting conversion
- Connect rate stabilizing above 15% (dialer local presence and optimal timing working)
- At least 1 meeting booked in the first 3 days of calling

## Instructions

### 1. Set up cloud dialer infrastructure

Configure a cloud dialer for outbound calling. Use Aircall (Professional: $50/user/mo) for a founder-led team, or Orum (Launch: $250/user/mo) if parallel dialing is needed for higher volume.

For Aircall setup via API:
1. Create an outbound number with local presence enabled (area code matching)
2. Configure CRM integration: connect Aircall to Attio so every call automatically creates a note with duration, recording URL, and disposition
3. Record 2-3 voicemail variants (under 20 seconds each) referencing common signals: funding, hiring, tech adoption
4. Set up call tagging: `meeting_booked`, `follow_up`, `not_interested`, `callback`, `voicemail_left`, `no_answer`

Use the `cloud-dialer-call` fundamental for API operations: initiating calls, logging outcomes, dropping voicemails, and retrieving recordings.

Estimated time: 2 hours.

### 2. Build the continuous prospect pipeline

Run the `build-prospect-list` drill configured for ongoing enrichment, not a one-time batch. Set up a Clay table that:

1. Ingests new prospect sources weekly (Apollo saved search, LinkedIn Sales Navigator export, or manual additions)
2. Runs the enrichment waterfall automatically on new rows: phone number (Cognism -> Lusha -> PDL -> Apollo), firmographics (Clearbit), signals (Crunchbase funding, LinkedIn job changes, BuiltWith tech stack)
3. Applies the scoring model validated in Smoke
4. Pushes prospects scoring 70+ with verified phone numbers to Attio automatically

Run the `enrich-and-score` drill to verify the pipeline is producing 15+ qualified contacts per day. If volume is low, widen the ICP slightly or add additional signal sources.

Estimated time: 3 hours.

### 3. Launch pre-call email warming

Run the `cold-email-sequence` drill to create a 2-step email sequence in Instantly that fires before the call:

- **Email 1 (Day 0)**: Short problem-aware email referencing the prospect's buying signal. No pitch. Under 60 words. Purpose: make your name familiar so the cold call opener can say "I sent you a note earlier this week about [topic]."
- **Email 2 (Day 2)**: Follow-up with a relevant insight or data point. Still no hard CTA — the call is the CTA.

Configure n8n to automatically enroll new Attio contacts into the Instantly sequence when they enter the call queue. The call happens Day 3-5 after the first email.

Estimated time: 2 hours.

### 4. Generate call scripts at scale

Run the `cold-call-framework` drill with the full prospect pipeline. For each new batch of prospects entering Attio:

1. Agent pulls the contact's signal data, enrichment, and company context from Attio
2. Generates a personalized call script: signal-based opener, problem statement in their language, open-ended question, bridge, CTA
3. Generates objection responses tailored to the prospect's likely objections (based on company size, role, and industry)
4. Stores the script as an Attio note on the contact record
5. Tags the contact as `call_ready` in Attio

This runs automatically for every new prospect entering the pipeline. The founder opens the contact record before each call and has the script ready.

Estimated time: 1 hour setup, then automatic.

### 5. Configure event tracking

Run the `posthog-gtm-events` drill to set up call-specific tracking:

- `cold_call_attempted` — properties: prospect_id, prospect_tier, signal_type, script_variant, time_of_day, day_of_week
- `cold_call_connected` — properties: prospect_id, duration_seconds, disposition, objections_raised, talk_ratio
- `cold_call_meeting_booked` — properties: prospect_id, meeting_type, source_signal, script_variant
- `cold_call_voicemail_left` — properties: prospect_id, voicemail_variant, attempt_number
- `cold_call_no_answer` — properties: prospect_id, attempt_number

Connect Aircall webhooks to PostHog via n8n so call events fire automatically when the dialer logs an outcome.

Build a PostHog dashboard "Account-Based Cold Calling — Baseline" with panels:
- Daily call volume (attempted, connected, meetings)
- Connect rate trended daily
- Meeting conversion rate trended daily
- Best call windows heatmap (day of week x time of day)
- Signal effectiveness breakdown (meeting rate by signal_type)
- Pipeline value from cold call meetings

Estimated time: 2 hours.

### 6. Execute 150 calls over 2 weeks

**Human action required:** The founder executes calls through the cloud dialer.

Daily cadence: 15 calls per day, 10 business days = 150 calls. Using the dialer:
1. Open Attio, filter contacts tagged `call_ready`, sorted by score descending
2. Review the script note (30 seconds)
3. Initiate the call via the dialer
4. If voicemail: drop the pre-recorded voicemail matching the prospect's signal type
5. If connected: follow the script framework — opener, permission, problem, question, bridge, CTA
6. After the call: the dialer auto-logs to Attio. Add any manual notes about the conversation. PostHog events fire via webhook.
7. If meeting booked: create the Cal.com booking link and send via Attio email

Estimated time: 7.5 hours (15 calls/day x 10 days, ~3 min per attempt including prep).

### 7. Evaluate against threshold

Run the `threshold-engine` drill to evaluate: >=3% call-to-meeting rate from 150 calls over 2 weeks.

The threshold engine computes:
- Call-to-meeting rate: meetings / attempts (target: >=3%, meaning >=5 meetings from 150 calls)
- Connect rate: connected / attempts (benchmark: 15-25%)
- Conversation-to-meeting rate: meetings / connected (benchmark: 10-20%)
- Cost per meeting: (dialer cost + Clay credits + Instantly cost) / meetings
- Pre-call email impact: compare connect rate for prospects who opened the email vs. those who did not
- Signal effectiveness: rank signals by meeting conversion

If PASS: Document the winning configuration (best signals, best times, best script variants, email impact). Proceed to Scalable.

If FAIL: Diagnose using the PostHog dashboard:
- Connect rate low (<15%): phone number quality, call timing, or local presence not working. Try different time blocks or re-enrich numbers.
- Connect rate fine but conversation rate low: opener is not hooking prospects. Test new signal references or problem statements.
- Conversations happening but no meetings: CTA is weak, prospects are not solution-aware enough, or objection handling is failing. Tighten ICP to higher-intent signals.
- Pre-call emails not opening: subject line or sender domain issue. Test new subject lines via Instantly A/B.

Adjust and re-run.

Estimated time: 1.5 hours.

## Time Estimate

- Cloud dialer setup: 2 hours
- Continuous prospect pipeline: 3 hours
- Pre-call email sequence: 2 hours
- Script generation setup: 1 hour
- PostHog event tracking + dashboard: 2 hours
- Call execution (10 days x 45 min): 7.5 hours
- Threshold evaluation: 1.5 hours

**Total: ~20 hours over 2 weeks** (including ~7.5 hours of founder calling time)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — contact records, call logging, pipeline tracking | Standard stack (excluded) |
| PostHog | Event tracking, dashboards, call analytics | Standard stack (excluded) |
| n8n | Automation — dialer-to-CRM sync, prospect pipeline, email enrollment | Standard stack (excluded) |
| Clay | Continuous prospect enrichment, phone waterfall, signal detection | Growth: $495/mo. [clay.com/pricing](https://www.clay.com/pricing) |
| Aircall | Cloud dialer with local presence, recording, voicemail drop, CRM sync | Professional: $50/user/mo. [aircall.io/pricing](https://aircall.io/pricing/) |
| Instantly | Pre-call email warming sequence | Growth: $37/mo. [instantly.ai/pricing](https://instantly.ai/pricing) |
| Fireflies.ai | Call transcription for post-call analysis | Free: 800 min/mo. Pro: $18/user/mo. [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Meeting scheduling for booked calls | Standard stack (excluded) |

**Play-specific cost: ~$87-105/mo** (Aircall $50 + Instantly $37 + Fireflies free tier or $18)

## Drills Referenced

- `build-prospect-list` — continuous prospect sourcing from Apollo into Clay with auto-push to Attio
- `enrich-and-score` — phone waterfall, signal enrichment, scoring, and tier assignment
- `cold-call-framework` — personalized script generation with signal-based openers and objection handling
- `cold-email-sequence` — pre-call warming email sequence via Instantly
- `posthog-gtm-events` — call event taxonomy and PostHog dashboard setup
- `threshold-engine` — evaluates call outcomes against >=3% meeting rate threshold
