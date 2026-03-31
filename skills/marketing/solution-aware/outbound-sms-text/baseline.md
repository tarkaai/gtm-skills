---
name: outbound-sms-text-baseline
description: >
  SMS Outbound Sequences — Baseline Run. First always-on SMS automation via
  Twilio and n8n. 3-step sequence with personalized copy, automated reply
  handling, and CRM sync. Targeting 200 prospects over 2 weeks to prove
  repeatable >=4% response rate.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Baseline Run"
time: "15 hours over 2 weeks"
outcome: "≥4% response rate from 200 SMS messages over 2 weeks"
kpis: ["Response rate", "Delivery rate", "Opt-out rate", "Meetings booked"]
slug: "outbound-sms-text"
install: "npx gtm-skills add marketing/solution-aware/outbound-sms-text"
drills:
  - sms-outreach-sequence
  - sms-copy-generation
  - posthog-gtm-events
---

# SMS Outbound Sequences — Baseline Run

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

The Baseline Run is the first always-on automated SMS outreach. Twilio sends messages on a schedule via n8n, replies are automatically classified and routed, and all events flow to PostHog and Attio. The winning message variant from Smoke is the starting template, personalized per prospect via Clay enrichment data. Success: **>=4% response rate** from 200 SMS messages over 2 weeks.

## Leading Indicators

- Delivery rate above 95% in the first 3 days (validates number quality and A2P registration)
- First automated reply classified and routed correctly within 24 hours
- Response rate above 2% after the first 50 sends (on track for threshold)
- Opt-out rate below 3% (validates copy resonance and targeting)
- At least 1 meeting booked from SMS within the first week
- n8n workflow running daily without errors for 5 consecutive days

## Instructions

### 1. Provision SMS infrastructure

Complete A2P 10DLC registration if not done during Smoke. Use the `sms-phone-number-provisioning` fundamental (referenced inside `sms-outreach-sequence` drill):

1. Purchase a local Twilio phone number with SMS capability in a relevant area code
2. Register your brand via Twilio Trust Hub (one-time: $4 brand registration + optional $40 vetting)
3. Register your SMS campaign describing B2B sales outreach use case
4. Assign the phone number to your Messaging Service
5. Wait for registration approval (3-7 business days)

**Do NOT proceed to step 2 until A2P registration status is "Approved."** Sending without registration results in carrier filtering and message blocking.

### 2. Build the prospect list of 200 contacts

Use the `build-prospect-list` drill at higher volume than Smoke. Source from Apollo, enrich via Clay waterfall, verify phone type is mobile.

Requirements per contact:
- Verified mobile phone number (not landline)
- First name, company name, title, industry
- At least one buying signal or enrichment data point for personalization
- Not on the opt-out list from Smoke

Push to Attio with tags `play:outbound-sms-text` and `level:baseline`. Set `sms_campaign_status=active` and `sms_current_step=0`.

### 3. Generate personalized SMS copy

Run the `sms-copy-generation` drill. Use the winning variant from Smoke as the base template. For each prospect, generate a personalized 3-message sequence using Claude:

- Message 1: Signal-based opener with prospect's name, company, and specific context. Under 160 characters. Includes "Reply STOP to opt out."
- Message 2: Proof point referencing a similar company's results. Under 160 characters. CTA: "Reply YES for a 10-min call."
- Message 3: Graceful breakup with Cal.com booking link. Under 160 characters.

Validate every generated message is under 160 characters after merge field resolution. Store in Attio as contact notes.

### 4. Deploy the automated SMS sequence

Run the `sms-outreach-sequence` drill. Build the n8n workflow:

1. **Daily cron trigger** at 9am (or segmented by timezone)
2. **Attio query**: fetch contacts where `sms_campaign_status=active` AND `sms_next_step_date <= today` AND `sms_opted_out != true`
3. **Timezone gate**: verify current time is 8am-6pm in contact's timezone. Reschedule if outside window.
4. **Send via Twilio**: use `sms-provider-send` fundamental with the message for the contact's current sequence step
5. **Update Attio**: increment `sms_current_step`, set `sms_next_step_date` (Day 1 -> Day 3 -> Day 6), update `sms_last_sent_date`
6. **Status callback routing**: Twilio delivery webhooks flow to n8n, which fires PostHog events (`sms_sent`, `sms_delivered`, `sms_failed`) and updates Attio

Daily send limit: 40 messages per day (200 contacts across ~5 days of initial sends, plus follow-up steps staggered over 2 weeks).

### 5. Configure automated reply handling

Wire up inbound reply routing via the `sms-conversation-routing` fundamental (part of `sms-outreach-sequence` drill):

1. Twilio inbound webhook posts to n8n
2. n8n matches sender phone to Attio contact
3. Claude classifies reply sentiment: POSITIVE, NEGATIVE, QUESTION, OPT_OUT, NEUTRAL
4. Route by classification:
   - POSITIVE: create Attio deal, send Cal.com link via SMS, stop sequence, Slack alert to founder
   - NEGATIVE: stop sequence, mark `sms_not_interested=true`, log in Attio
   - QUESTION: Slack alert to founder for manual reply within 2 hours, pause sequence
   - OPT_OUT: trigger opt-out workflow, confirm via SMS, update suppression list
   - NEUTRAL: continue sequence, log reply
5. Fire PostHog event `sms_replied` with sentiment, time_to_reply, sequence_step

### 6. Set up event tracking

Run the `posthog-gtm-events` drill. Configure the SMS event taxonomy in PostHog:

- `sms_sent` — campaign_id, sequence_step, message_variant, prospect_tier
- `sms_delivered` — campaign_id, delivery_time_seconds
- `sms_failed` — campaign_id, error_code
- `sms_replied` — campaign_id, sentiment, time_to_reply_hours, sequence_step
- `sms_opt_out` — campaign_id, sequence_step
- `sms_meeting_booked` — campaign_id, sequence_step, prospect_tier

Connect all via n8n webhooks from Twilio status callbacks and inbound message hooks.

### 7. Monitor and adjust mid-flight

After Week 1 (first 100 sends), review:
- If delivery rate below 90%: check A2P registration status, review error codes, verify phone numbers
- If response rate below 2%: review message copy. Test shorter messages. Check if personalization is resolving correctly.
- If opt-out rate above 5%: message is too salesy or targeting is wrong. Pause, revise copy, narrow ICP.
- If replies are coming but no meetings: CTA is weak. Test direct booking link in Message 1 instead of waiting for Message 3.

### 8. Evaluate against threshold

After 2 weeks, pull the full funnel from PostHog and Attio:
- Total messages sent (target: 200+)
- Delivery rate (target: >95%)
- Total replies and sentiment breakdown
- Response rate = total replies / messages delivered
- Meetings booked from SMS
- Opt-out rate

**Pass threshold: >=4% response rate** (>=8 replies from 200 delivered messages).

- **PASS**: Document the best-performing message copy, response time patterns, and ICP segments. Record delivery rate and opt-out rate as baselines. Proceed to Scalable.
- **FAIL**: Diagnose — phone number quality (low delivery), message copy (low reply), targeting (replies but wrong people), or timing (sent at wrong hours). Fix the weakest link and re-run Baseline.

## Time Estimate

- A2P registration and Twilio setup: 2 hours (+ 3-7 day wait)
- List building and enrichment (200 contacts): 2 hours
- SMS copy generation and validation: 2 hours
- n8n workflow build (send + reply handling): 4 hours
- PostHog event tracking setup: 1 hour
- Monitoring and mid-flight adjustments: 2 hours
- Evaluation: 1 hour
- Manual founder replies to QUESTION/POSITIVE: 1 hour

Total: ~15 hours over 2 weeks.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Twilio | SMS sending and delivery tracking | ~$0.011-0.013/msg effective; ~$1.15/mo/number; A2P registration ~$19-59 one-time (https://www.twilio.com/en-us/sms/pricing/us) |
| Clay | Prospect enrichment and phone verification | Pro: $149/mo (https://www.clay.com/pricing) |
| Apollo | Contact sourcing | Basic: $49/mo (https://www.apollo.io/pricing) |
| Attio | CRM for deal tracking and contact management | Plus: $29/user/mo (https://attio.com/pricing) |
| n8n | Workflow orchestration | Starter: $20/mo (https://n8n.io/pricing) |
| PostHog | Event tracking and funnels | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Anthropic API | Reply sentiment classification | ~$5-10/mo at this volume (https://www.anthropic.com/pricing) |
| Cal.com | Booking links in SMS replies | Free tier (https://cal.com/pricing) |

**Estimated play-specific cost: ~$55-80/mo** (Twilio SMS at 200 msgs ~$2.50 + number $1.15 + n8n $20 + Anthropic ~$5-10; Clay and Apollo costs shared across plays)

## Drills Referenced

- `sms-outreach-sequence` — build and deploy the automated 3-step SMS sequence via Twilio + n8n
- `sms-copy-generation` — generate personalized SMS copy for each prospect using Claude
- `posthog-gtm-events` — set up the SMS event taxonomy for tracking and measurement
