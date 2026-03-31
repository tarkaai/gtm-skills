---
name: outbound-voice-messages-baseline
description: >
  Outbound Voice Messages -- Baseline Run. Deploy AI voice cloning and semi-automated
  delivery to send 150 personalized voice messages via ringless voicemail and LinkedIn
  voice notes over 2 weeks. First always-on voice outreach pipeline.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Direct, Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=6% response rate from 150 voice messages over 2 weeks"
kpis: ["Response rate by channel", "Cost per response", "Callback/reply quality", "Time to meeting"]
slug: "outbound-voice-messages"
install: "npx gtm-skills add marketing/solution-aware/outbound-voice-messages"
drills:
  - voice-message-recording
  - voice-message-delivery
  - posthog-gtm-events
  - threshold-engine
---

# Outbound Voice Messages -- Baseline Run

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Direct, Social

## Outcomes

Prove that AI-cloned voice messages delivered via ringless voicemail and LinkedIn voice notes produce repeatable responses at 3-4x the volume of Smoke. Success means at least a 6% response rate from 150 voice messages over 2 weeks, with responses converting to meetings. This is the first level using AI voice generation and tool-assisted delivery.

## Leading Indicators

- AI-cloned voice passes quality check (indistinguishable from manual recording in blind test)
- Ringless voicemail delivery rate above 75%
- LinkedIn voice note listen rate above 40%
- At least 3 responses in the first week
- Response sentiment is predominantly positive or neutral (negative reply rate below 3%)
- Follow-up emails referencing the voice message have open rates above 50%

## Instructions

### 1. Set up AI voice cloning

Run the `voice-message-recording` drill using the AI generation path (Step 2b).

One-time setup:
1. Record a 2-3 minute audio sample of yourself speaking naturally. Read a script that includes greetings, questions, statements, and varied intonation. Export as MP3 at 16kHz+ sample rate.
2. Upload the sample to ElevenLabs using the `ai-voice-generation` fundamental. Store the returned `voice_id` in your environment config.
3. Generate a test message for a fictional prospect. Listen to it. Adjust `stability` (0.4-0.6) and `similarity_boost` (0.7-0.85) until the output sounds natural and matches your voice.
4. **Human action required:** Have a colleague listen to the AI-generated message without telling them it is AI. If they can tell, re-record your sample with more natural cadence and regenerate.

### 2. Build a prospect list of 175-200 contacts

Run the `build-prospect-list` drill at higher volume than Smoke. Source from Apollo, enrich in Clay. Requirements:
- At least 120 prospects with verified phone numbers (for ringless voicemail)
- At least 130 prospects with LinkedIn URLs (for voice notes)
- Scored and filtered to ICP fit score above 70
- Push to Attio with tags `play:outbound-voice-messages` and `level:baseline`

Prepare 3-4 script variants based on the winning variant from Smoke, plus 2 new variants testing different value prop hooks and signal references.

### 3. Batch-generate voice messages

Run the `voice-message-recording` drill (AI generation path) for the full prospect list:

1. Build Clay AI formula columns that generate a personalized script per prospect using their trigger signal, company name, and first name
2. Run the batch generation via ElevenLabs API -- 150 messages at ~400 chars each uses approximately 60,000 characters (fits within ElevenLabs Creator plan at $22/mo)
3. Quality-check a random sample of 10 messages per script variant. Listen for name pronunciation, natural pacing, and correct signal references.
4. Upload audio files to cloud storage and map each prospect to their audio URL in Clay

### 4. Configure event tracking

Run the `posthog-gtm-events` drill to set up the voice message event taxonomy. Configure these events in PostHog:

- `vm_phone_generated`, `vm_phone_delivered`, `vm_phone_failed`, `vm_phone_callback`
- `vm_linkedin_sent`, `vm_linkedin_listened`, `vm_linkedin_replied`
- `vm_followup_email_sent`, `vm_followup_email_opened`, `vm_followup_email_replied`
- `vm_meeting_booked` with properties: source_channel, prospect_tier, script_variant

Connect PostHog to Attio via n8n webhook so response events sync to CRM records automatically.

### 5. Deliver voice messages across both channels

Run the `voice-message-delivery` drill:

**Week 1 -- Phone voicemail batch (75 messages):**
1. Upload personalized audio files to VoiceDrop.ai
2. Schedule delivery: 25 messages/day for 3 days (Tue-Thu), 9am-11am in prospect timezone
3. Use local caller ID matching each prospect's area code
4. Send follow-up emails within 2 hours of each batch via Instantly

**Week 1-2 -- LinkedIn voice notes (75 messages):**
1. Set up a lemlist campaign with LinkedIn voice note steps (or upload audio to Expandi)
2. Send connection requests to unconnected prospects in Week 1
3. Deliver voice notes to connected prospects: 15/day over 5 days in Week 2
4. Send LinkedIn text follow-up 1 day after each voice note with booking link

**Week 2 -- Remaining phone batch:**
5. Deliver remaining phone voicemails to fill the 150 total
6. Send corresponding follow-up emails

Coordinate in n8n: if a prospect is receiving both phone VM and LinkedIn voice note, space them 3+ days apart.

### 6. Monitor and adjust mid-flight

Check metrics daily during the 2-week run:
- Phone callback rate -- if below 1% after 50 deliveries, review scripts and delivery timing
- LinkedIn reply rate -- if below 3% after 30 voice notes, adjust script tone or prospect tier targeting
- Negative reply rate -- if above 3% on any channel, pause and review messaging
- Email follow-up open rate -- if below 40%, test different subject lines

Make one adjustment per week maximum. Do not change multiple variables simultaneously.

### 7. Evaluate against threshold

Run the `threshold-engine` drill. Pull data from PostHog and Attio. Measure against: **>=6% response rate from 150 voice messages over 2 weeks** (at least 9 responses).

Calculate:
- Response rate by channel (phone callback rate, LinkedIn reply rate, email reply rate)
- Cost per response: (ElevenLabs + VoiceDrop.ai + lemlist monthly cost) / responses
- Meeting conversion: responses that became scheduled meetings
- Best-performing script variant by response rate
- Best delivery time windows by callback/reply rate

- **PASS**: Proceed to Scalable. Document the winning channel mix, script variants, and delivery timing.
- **FAIL**: Diagnose -- AI voice quality (do callbacks reference sounding "off"?), delivery issues (low phone delivery rate?), targeting (wrong ICP segment?), or scripting (no resonance?). Fix and re-run.

## Time Estimate

- AI voice clone setup: 1 hour (one-time)
- List building and enrichment: 2 hours
- Script variant creation and Clay formulas: 1.5 hours
- Batch voice generation and quality check: 1.5 hours
- VoiceDrop.ai and lemlist campaign setup: 2 hours
- Instantly follow-up email setup: 1 hour
- PostHog event tracking configuration: 1.5 hours
- Daily monitoring over 2 weeks: 3.5 hours (15 min/day)
- Mid-flight adjustments: 1.5 hours
- Final evaluation: 1.5 hours

Total: ~18 hours over 2 weeks.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| ElevenLabs | AI voice cloning and message generation | Creator: $22/mo for 100K chars (~250 messages) (https://elevenlabs.io/pricing) |
| VoiceDrop.ai | Ringless voicemail delivery | Starter: $95/mo for ~1,000 VMs (https://www.voicedrop.ai/pricing) |
| lemlist | LinkedIn voice note automation | Multichannel Expert: $99/user/mo (https://www.lemlist.com/pricing) |
| Clay | Enrichment and script generation | Pro: $149/mo (https://www.clay.com/pricing) |
| Instantly | Follow-up email delivery | Growth: $30/mo (https://instantly.ai/pricing) |
| Attio | CRM for tracking all activity | Free tier: 3 users (https://attio.com/pricing) |
| PostHog | Event tracking and funnels | Free tier: 1M events/mo (https://posthog.com/pricing) |

**Estimated play-specific cost: ~$250-400/mo** (ElevenLabs Creator + VoiceDrop Starter + lemlist + Instantly)

## Drills Referenced

- `voice-message-recording` -- AI-generate personalized voice messages for the full prospect batch
- `voice-message-delivery` -- deliver via ringless voicemail (VoiceDrop.ai) and LinkedIn voice notes (lemlist)
- `posthog-gtm-events` -- configure voice message event taxonomy for tracking
- `threshold-engine` -- evaluate pass/fail against >=6% response rate
