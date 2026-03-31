---
name: qualified-prospect-calls-baseline
description: >
  Founder calls to prospects — Baseline Run. First always-on automation layer: agent
  continuously enriches and scores prospects, sequences pre-call and post-call emails
  around the founder's call blocks, tracks every touchpoint in PostHog, and measures
  whether the 2% meeting rate holds over 2 weeks of sustained calling.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 2% meeting rate (meetings booked / total prospects contacted) over 2 weeks"
kpis: ["Meeting rate", "Connect rate", "Reply rate (email + LinkedIn)", "Cost per meeting", "Pipeline value generated"]
slug: "qualified-prospect-calls"
install: "npx gtm-skills add sales/qualified/qualified-prospect-calls"
drills:
  - cold-call-framework
  - cold-email-sequence
  - linkedin-outreach
  - meeting-booking-flow
  - posthog-gtm-events
  - threshold-engine
---

# Founder Calls to Prospects — Baseline Run

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Outcomes

Achieve a 2% or higher meeting rate across all contacted prospects (calls + email + LinkedIn combined) over 2 sustained weeks. This proves the play is repeatable — not a one-week fluke — and that the multi-channel cadence (call + email + LinkedIn) compounds the founder's direct outreach.

## Leading Indicators

- Email open rate above 50% (founder name in From field drives opens)
- LinkedIn connection acceptance rate above 30%
- Connect rate on calls sustains at or above Smoke-level baseline
- At least 1 inbound reply referencing the call ("I saw you called, what's this about?")
- PostHog funnel shows clear progression: prospect contacted -> engaged -> meeting booked

## Instructions

### 1. Set up multi-channel event tracking

Run the `posthog-gtm-events` drill to configure the full event taxonomy for this play. Define and implement these events:

- `qpc_prospect_contacted` — fires when a prospect enters the cadence (any first touch). Properties: prospect_id, tier, signal_type, channels_planned
- `qpc_call_attempted` — fires per dial. Properties: prospect_id, time_of_day, day_of_week
- `qpc_call_connected` — fires when prospect answers. Properties: prospect_id, duration_seconds, disposition
- `qpc_email_sent` — fires per email step. Properties: prospect_id, sequence_step, subject_line_variant
- `qpc_email_replied` — fires on reply. Properties: prospect_id, sentiment (positive/negative/neutral)
- `qpc_linkedin_sent` — fires per LinkedIn message. Properties: prospect_id, message_step
- `qpc_linkedin_replied` — fires on LinkedIn reply. Properties: prospect_id, sentiment
- `qpc_meeting_booked` — fires when meeting is confirmed. Properties: prospect_id, source_channel (call/email/linkedin), signal_type, days_since_first_touch

Connect PostHog to Attio via n8n webhook so deal stage changes flow automatically.

### 2. Build the prospect cadence list

Using the ICP and scoring model validated in Smoke, source 100-150 new prospects. Run the `cold-call-framework` drill prerequisites: enrich all prospects with direct phone numbers via Clay waterfall. Score and tier them. Push to Attio with tags `qpc-baseline` and the prospect tier (hot/warm).

Split prospects into daily batches of 10-15 to sustain a consistent calling rhythm over 2 weeks.

### 3. Launch the email pre-warm sequence

Run the `cold-email-sequence` drill. Configure a 3-step sequence in Instantly that runs BEFORE the call:

- **Email 1 (Day 0)**: Short, personal email from the founder. Reference the prospect's signal. No CTA — just plant the name. Under 60 words.
- **Email 2 (Day 2)**: Share one relevant insight or data point. Still no hard ask.
- **Day 3-4**: Founder calls. The prospect has now seen the founder's name twice in their inbox.

This pre-warm makes the cold call warmer. Set up A/B testing on Email 1 subject lines (test 2 variants with 50 prospects each).

### 4. Launch LinkedIn connection outreach in parallel

Run the `linkedin-outreach` drill. Send connection requests to the same prospect list on Day 0 (same day as Email 1). Keep the connection note under 200 characters, referencing the same signal. This creates a 3-channel surround: email + LinkedIn + phone all within the first week.

After connection acceptance, send a single follow-up message on Day 5 offering value (not a pitch). If the prospect has not responded to any channel by Day 10, send the final LinkedIn message with a Cal.com booking link.

### 5. Execute structured call blocks

**Human action required:** The founder calls prospects on Days 3-4 of each prospect's cadence (after 2 emails have been sent). Follow the `cold-call-framework` drill structure. The opener now has a built-in advantage: "I sent you a note earlier this week about [signal] — wanted to follow up personally."

Call 10-15 prospects per session, 3 sessions per week. Log every call in Attio immediately using the structured fields established in Smoke.

### 6. Configure post-call follow-up automation

Run the `meeting-booking-flow` drill for Cal.com setup if not done in Smoke. Then build a post-call email automation in n8n:

- If call connected + meeting set: send calendar confirmation + pre-meeting brief
- If call connected + "send me an email": trigger a personalized follow-up within 1 hour with Cal.com link
- If voicemail left: send a follow-up email 2 hours later referencing the voicemail
- If no answer after 2 attempts: add to the email-only nurture sequence

### 7. Monitor daily and adjust mid-flight

Check PostHog daily after the first 3 days. If:

- Email open rate is below 40%: rewrite subject lines, check deliverability with Instantly dashboard
- Connect rate is below 15%: shift call times (try early morning or late afternoon), verify phone numbers
- All connected calls result in "not interested": the problem statement is wrong — rewrite the opener and problem framing

### 8. Evaluate against threshold

After 2 weeks, run the `threshold-engine` drill. Compute:

- Total prospects contacted (entered cadence across any channel)
- Total meetings booked (from any channel)
- Meeting rate = meetings / prospects contacted
- Break down meeting source: calls vs email replies vs LinkedIn replies

**Pass: meeting rate >= 2%.** Proceed to Scalable.

**Fail: meeting rate < 2%.** Diagnose by channel:
- If calls are working but email/LinkedIn are not: the multi-channel cadence needs tuning, but the core play (phone) is valid. Adjust messaging and timing.
- If email/LinkedIn work but calls do not: the phone number quality or call script is the bottleneck. Focus on enrichment and script iteration.
- If nothing works: revisit ICP. The prospects may not have the pain you think they have.

## Time Estimate

- Event tracking setup: 1 hour (agent)
- Prospect sourcing + enrichment + scoring: 2 hours (agent)
- Email sequence + LinkedIn setup: 2 hours (agent)
- Call execution: 4.5 hours across 2 weeks (human, 3 sessions/week x 30 min)
- Post-call automation + monitoring: 1.5 hours (agent)
- Threshold evaluation + analysis: 1 hour (agent)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM, call logging, deal tracking | Free tier or Pro: $29/user/mo |
| Clay | Enrichment + phone number waterfall | Explorer: $149/mo (https://clay.com/pricing) |
| Instantly | Email sequencing + warmup | Growth: $30/mo (https://instantly.ai/pricing) |
| Cal.com | Meeting booking | Free tier or Team: $12/user/mo (https://cal.com/pricing) |
| PostHog | Event tracking + funnels | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Apollo | Initial prospect sourcing | Free tier: 60 credits/mo (https://apollo.io/pricing) |

**Estimated play-specific cost at this level:** $30-180/mo depending on volume and tier

## Drills Referenced

- `cold-call-framework` — call script structure, objection handling, per-call logging
- `cold-email-sequence` — 3-step pre-warm email sequence in Instantly
- `linkedin-outreach` — parallel LinkedIn connection + messaging cadence
- `meeting-booking-flow` — Cal.com event types, CRM sync, and post-meeting automation
- `posthog-gtm-events` — full event taxonomy for multi-channel tracking
- `threshold-engine` — 2% meeting rate pass/fail evaluation
