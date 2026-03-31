---
name: outbound-voice-messages-smoke
description: >
  Outbound Voice Messages -- Smoke Test. Manually record and send 40 personalized
  voice messages via LinkedIn voice notes and phone voicemail to solution-aware
  prospects. Validate whether voice outreach generates higher response rates than
  text-only channels.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Direct, Social"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=5% response rate from 40 voice messages in 1 week"
kpis: ["Response rate", "Callback/reply rate by channel", "Time to first response"]
slug: "outbound-voice-messages"
install: "npx gtm-skills add marketing/solution-aware/outbound-voice-messages"
drills:
  - icp-definition
  - build-prospect-list
  - voice-message-recording
  - threshold-engine
---

# Outbound Voice Messages -- Smoke Test

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Direct, Social

## Outcomes

Prove that personalized voice messages generate responses from solution-aware prospects. Success means at least 2 responses (callbacks, LinkedIn replies, or email replies referencing the voice message) from 40 messages sent across phone voicemail and LinkedIn voice notes within 1 week. No automation, no paid tools beyond free tiers -- the founder records and sends every message manually.

## Leading Indicators

- Voicemail delivery rate above 70% (not all carriers accept ringless VM)
- LinkedIn voice note listen rate above 40% (visible in lemlist or LinkedIn read receipts)
- At least 1 callback or reply within 48 hours of first batch
- Prospects mention the voice message in their reply ("got your voicemail", "heard your voice note")
- Follow-up email open rate above 50% (the voice message creates curiosity)

## Instructions

### 1. Define ICP and build a target list of 40 prospects

Run the `icp-definition` drill. Document firmographic criteria (company size, industry, funding stage), buyer persona (title, seniority, department), top 3 pain points, and 3 trigger signals that make voice outreach timely (new funding, job change, competitor churn).

Run the `build-prospect-list` drill. Source 50-60 contacts from Apollo matching your ICP. Import into Clay. Run enrichment to fill: email, phone number, LinkedIn URL. Score and filter to the top 40. Ensure at least 25 have phone numbers and at least 30 have LinkedIn URLs.

Push to Attio with tags `play:outbound-voice-messages` and `level:smoke`.

### 2. Write voice message scripts

Write 2-3 script variants targeting different pain points identified in your ICP. Each script follows this structure (50-80 words, 20-35 seconds):

1. Greeting with prospect's first name (3 sec)
2. Signal reference -- why you are reaching out now (5 sec)
3. Value hook -- one sentence connecting their signal to your solution (8 sec)
4. CTA -- reference a follow-up email with your calendar link (5 sec)
5. Sign-off (3 sec)

Create a Clay column that maps each prospect to a script variant based on their trigger signal. Add merge fields for first name, company name, and signal.

### 3. Record voice messages manually

Run the `voice-message-recording` drill using the manual recording path (Step 2a). Record each message yourself using your phone's voice memo app or laptop microphone. Target pace: 2-3 minutes per message. The full batch of 40 takes approximately 90 minutes.

**Human action required:** You must record these yourself. This is a Smoke Test -- the point is to validate the channel with authentic founder voice before investing in AI voice cloning. Save files as `vm-{company}-{firstname}.mp3`.

### 4. Deliver voice messages across both channels

Split your 40 prospects across channels based on available contact data:

**Phone voicemail (prospects with phone numbers):**
- Use your personal phone or Google Voice
- Call during 9am-11am in the prospect's timezone
- When it goes to voicemail (most will), leave your pre-written message naturally
- If someone answers live, use the script as a conversation opener
- Log every attempt in Attio immediately: delivered, answered, no-answer, wrong-number

**LinkedIn voice notes (prospects with LinkedIn connections or open profiles):**
- Send a connection request first if not connected (keep note under 200 characters, reference a signal)
- For connected prospects: open LinkedIn messaging, hold the microphone icon, and record your message
- Send a text follow-up message 1 day later with your Cal.com booking link
- Log in Attio: voice_note_sent, connection_pending, message_sent

**Follow-up email (all prospects, same day):**
- Send a brief email within 1-4 hours of the voice message: "Just left you a quick voicemail / sent you a voice note on LinkedIn. Short version: {one_line_value_prop}. Calendar here if it's easier: {booking_link}"
- Send manually from your email client. No sequences needed at Smoke level.

### 5. Track responses for 7 days

Monitor daily:
- Phone callbacks (check missed calls, voicemails, and Attio)
- LinkedIn message replies (check LinkedIn inbox)
- Email replies referencing the voice message
- Meeting bookings via Cal.com

Log every response in Attio with: response channel, response sentiment (positive/neutral/negative), time from delivery to response, and whether a meeting was booked.

### 6. Evaluate against threshold

Run the `threshold-engine` drill. Pull logged data from Attio. Count total responses (callbacks + LinkedIn replies + email replies that reference the voice message). Compare against pass threshold: **>=5% response rate from 40 voice messages in 1 week** (that is, at least 2 responses).

Also record:
- Response rate by channel (phone vs LinkedIn vs email)
- Which script variant generated the most responses
- Average time from delivery to response
- Qualitative notes: what did responders say? Did they mention the voice message?

- **PASS**: Proceed to Baseline. Document which channel and script variant performed best.
- **FAIL**: Diagnose -- was it targeting (wrong ICP), scripting (message didn't resonate), delivery (low phone delivery rate), or timing? Adjust and re-run Smoke.

## Time Estimate

- ICP definition and list building: 1.5 hours
- Script writing: 30 minutes
- Manual voice recording (40 messages): 1.5 hours
- Delivery and follow-up emails: 1.5 hours (spread across 3-4 days)
- Daily monitoring and logging: 30 minutes (5 min/day for 7 days)
- Evaluation: 30 minutes

Total: ~6 hours of active work spread over 1 week.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Prospect enrichment and list building | Free tier: 100 credits/mo (https://www.clay.com/pricing) |
| Apollo | Contact sourcing with phone numbers | Free tier: 50 emails/mo; Basic: $49/mo (https://www.apollo.io/pricing) |
| Attio | CRM for logging all outreach activity | Free tier: 3 users (https://attio.com/pricing) |
| Cal.com | Booking link in follow-up emails | Free tier available (https://cal.com/pricing) |
| PostHog | Event tracking | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Google Voice | Phone calls and voicemails | Free (https://voice.google.com) |

**Estimated play-specific cost: $0** (free tiers sufficient for Smoke volume of 40 messages)

## Drills Referenced

- `icp-definition` -- define ideal customer profile with trigger signals for voice outreach
- `build-prospect-list` -- source and enrich 40+ contacts with phone numbers and LinkedIn URLs
- `voice-message-recording` -- record personalized voice messages (manual path at Smoke)
- `threshold-engine` -- evaluate pass/fail against >=5% response rate threshold
