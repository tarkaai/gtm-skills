---
name: voice-message-delivery
description: Deliver personalized voice messages via ringless voicemail and LinkedIn voice notes with coordinated email follow-up
category: Outreach
tools:
  - VoiceDrop.ai
  - lemlist
  - Instantly
  - Attio
  - n8n
fundamentals:
  - ringless-voicemail-drop
  - linkedin-voice-note
  - instantly-campaign
  - attio-deals
  - n8n-workflow-basics
  - n8n-scheduling
---

# Voice Message Delivery

This drill takes the personalized audio files produced by the `voice-message-recording` drill and delivers them to prospects via two channels: ringless voicemail (phone) and LinkedIn voice notes. Each voice message is paired with a same-day follow-up email that references the voicemail, creating a multi-touch impression.

## Input

- Delivery mapping table from the `voice-message-recording` drill (prospect + audio file URL)
- Prospect phone numbers (for ringless voicemail channel)
- Prospect LinkedIn URLs (for LinkedIn voice note channel)
- Instantly account with warmed sending domains (for follow-up emails)
- Cal.com booking link

## Steps

### 1. Segment prospects by available channels

Not every prospect will have both a phone number and a LinkedIn URL. Segment your delivery mapping table:

- **Phone + LinkedIn**: Deliver on both channels (highest response rate)
- **Phone only**: Ringless voicemail + email follow-up
- **LinkedIn only**: LinkedIn voice note + LinkedIn text follow-up
- **Neither**: Exclude from voice play; route to email-only outreach

Use Clay or Attio filters to create these segments. Tag each prospect with their delivery channel(s).

### 2. Deliver ringless voicemails

Using the `ringless-voicemail-drop` fundamental:

1. Upload each prospect's personalized audio file to VoiceDrop.ai (or Slybroadcast)
2. Create a campaign with all phone-eligible prospects
3. Schedule delivery for 9am-11am in each prospect's local timezone (Tuesday-Thursday preferred)
4. Use a local caller ID matching the prospect's area code
5. Set metadata tags: `campaign: outbound-voice-messages`, `level: {current_level}`

Build an n8n workflow using `n8n-scheduling` to automate daily batches:
- Trigger: daily at 7am
- Pull today's batch from Attio (prospects tagged for today's delivery)
- For each prospect: upload audio, create drop, log delivery status
- On success: update Attio record with `vm_phone_delivered: true` and timestamp
- On failure: tag prospect for retry (max 2 retries on different days)

### 3. Deliver LinkedIn voice notes

Using the `linkedin-voice-note` fundamental:

**Option A -- lemlist (fully automated with AI voice):**
1. Create a lemlist campaign with a LinkedIn voice note step
2. Import prospects with their voice scripts (lemlist generates audio via built-in ElevenLabs)
3. Set the voice note step to trigger 1 day after connection acceptance
4. Add a follow-up text message step 1 day after the voice note with your booking link

**Option B -- Expandi/Unipile (bring your own audio):**
1. Upload each prospect's pre-generated audio file from the `voice-message-recording` drill
2. Map audio files to prospects in the campaign
3. Set daily sending limits: start at 10/day, ramp to 20/day over 2 weeks
4. Schedule during business hours in the prospect's timezone

Build coordination logic in n8n using `n8n-workflow-basics`:
- If the prospect is also receiving a ringless voicemail, space the LinkedIn voice note 2-3 days apart
- Never send both channels on the same day -- it looks automated

### 4. Send coordinated follow-up emails

Using the `instantly-campaign` fundamental, create a follow-up email that references the voice message. Send within 1-4 hours of the voice message delivery.

**For voicemail recipients:**
```
Subject: Just left you a voicemail

Hey {first_name},

I just left you a quick voicemail -- wanted to put a voice to the email.

Short version: I noticed {company} {signal}. We've been helping similar {industry} companies {value_prop}.

If 15 minutes makes sense: {booking_link}

Either way, appreciate your time.

{founder_name}
```

**For LinkedIn voice note recipients:**
```
Subject: Sent you a voice note on LinkedIn

Hey {first_name},

I sent you a voice note on LinkedIn -- figured it was quicker than typing out what I wanted to say.

The gist: {one_line_value_prop}. Thought it might be relevant given {signal}.

Calendar's here if you want to chat: {booking_link}

{founder_name}
```

### 5. Handle responses

Route all responses through Attio using the `attio-deals` fundamental:

- **Voicemail callback**: Log in Attio as `vm_callback: true`. Follow the cold call framework for the conversation.
- **LinkedIn voice note reply**: Log in Attio as `linkedin_voice_reply: true`. Respond within 4 hours. Move toward scheduling a call.
- **Email reply**: Standard positive/negative routing. Positive replies create a deal at "Meeting Booked" stage.
- **No response after both channels**: Add to a 7-day follow-up list. One final text-only email referencing both touches: "I left you a voicemail and a LinkedIn note last week..."

### 6. Track all delivery events

Fire PostHog events for every action (via n8n webhooks):

- `voice_message_phone_delivered` -- properties: campaign, prospect_tier, delivery_time, caller_id
- `voice_message_linkedin_delivered` -- properties: campaign, prospect_tier, delivery_time
- `voice_message_email_followup_sent` -- properties: campaign, channel_referenced (phone/linkedin)
- `voice_message_callback_received` -- properties: campaign, channel_originated, time_to_callback
- `voice_message_reply_received` -- properties: campaign, channel (linkedin/email), sentiment
- `voice_message_meeting_booked` -- properties: campaign, first_touch_channel, last_touch_channel

## Output

- Voice messages delivered via phone and/or LinkedIn to all eligible prospects
- Follow-up emails sent within hours of each voice message
- All delivery events tracked in PostHog and logged in Attio
- Response routing configured for callbacks, replies, and meetings

## Triggers

At Smoke: manual delivery of 20-40 messages over 1 week. At Baseline: semi-automated batches of 50-75/week. At Scalable: fully automated daily batches via n8n with 100-150/week. At Durable: autonomous pipeline with AI-optimized timing and script selection.
