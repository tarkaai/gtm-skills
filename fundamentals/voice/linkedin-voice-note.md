---
name: linkedin-voice-note
description: Send personalized voice notes via LinkedIn messaging using automation tools or API integrations
tool: lemlist
difficulty: Config
---

# LinkedIn Voice Note

Send a voice note as a LinkedIn message to a connected prospect. Voice notes appear as a playable audio clip in the LinkedIn inbox and stand out from text messages -- typical response rates are 3-5x higher than text DMs. This fundamental covers both AI-generated voice notes and manual recording approaches.

## Tool Options

| Tool | Method | Best For |
|------|--------|----------|
| lemlist | AI voice generation (ElevenLabs integration) + automated LinkedIn delivery | Fully automated voice note sequences at scale |
| Expandi | Upload audio file + LinkedIn message automation | Custom audio with smart scheduling |
| Unipile | LinkedIn Messaging API wrapper | Developer-friendly, build custom voice note workflows |
| La Growth Machine | Multichannel sequences with voice note steps | Combined email + LinkedIn voice note cadences |
| HeyReach | Multi-account LinkedIn automation with voice notes | Agency/team use with account rotation |

## Authentication

**lemlist (for AI voice notes):**
```
Authorization: Bearer {LEMLIST_API_KEY}
Base URL: https://api.lemlist.com/api
```

**Unipile (LinkedIn API wrapper):**
```
X-API-KEY: {UNIPILE_API_KEY}
Base URL: https://api.unipile.com/api/v1
```

**Expandi:**
```
Authorization: Bearer {EXPANDI_API_KEY}
Base URL: https://api.expandi.io/api/v1
```

## Operations

### 1. Set up AI voice cloning for LinkedIn voice notes (lemlist)

lemlist integrates with ElevenLabs to clone your voice and generate voice notes from text scripts. One-time setup:

1. In lemlist, navigate to Settings > Voice. Upload a 1-minute audio sample of yourself speaking naturally.
2. lemlist sends the sample to ElevenLabs for instant voice cloning.
3. The cloned voice is available in all LinkedIn voice note sequence steps.

**Via API -- create a campaign with voice note step:**
```
POST https://api.lemlist.com/api/campaigns
{
  "name": "outbound-voice-mar24",
  "sequences": [
    {
      "step": 1,
      "type": "linkedin_visit_profile",
      "delay_days": 0
    },
    {
      "step": 2,
      "type": "linkedin_connection_request",
      "delay_days": 1,
      "note": "Hi {{firstName}}, saw your work at {{companyName}} on {{topic}}. Would love to connect."
    },
    {
      "step": 3,
      "type": "linkedin_voice_message",
      "delay_days": 3,
      "condition": "connected",
      "voice_script": "Hey {{firstName}}, thanks for connecting. I noticed {{companyName}} {{signal}}. We've been helping similar companies {{value_prop}}. Would love to grab 15 minutes if you're open to it -- my calendar link is in the follow-up message I'll send. Talk soon."
    },
    {
      "step": 4,
      "type": "linkedin_message",
      "delay_days": 4,
      "condition": "no_reply",
      "text": "Hey {{firstName}} -- just sent you a voice note. Here's my calendar if it's easier: {{booking_link}}"
    }
  ]
}
```

### 2. Send a voice note via LinkedIn Messaging API (Unipile)

Unipile wraps LinkedIn's messaging capabilities, including voice note delivery:

```
POST https://api.unipile.com/api/v1/messages
Content-Type: multipart/form-data

account_id: {LINKEDIN_ACCOUNT_ID}
recipient_id: {PROSPECT_LINKEDIN_URN}
type: "voice_note"
audio_file: @vm-sarah-acme.mp3
```

The audio file must be:
- Format: MP3 or M4A
- Duration: under 60 seconds
- Sample rate: 16kHz or higher

### 3. Upload pre-generated audio for Expandi voice note step

```
POST https://api.expandi.io/api/v1/campaigns/{CAMPAIGN_ID}/steps/{STEP_ID}/audio
Content-Type: multipart/form-data

audio: @vm-sarah-acme.mp3
lead_id: "{LEAD_ID}"
```

For batch campaigns, map each prospect to their personalized audio file. Expandi plays the audio as a LinkedIn voice note when the sequence step triggers.

### 4. Monitor voice note delivery and engagement

**lemlist:**
```
GET https://api.lemlist.com/api/campaigns/{CAMPAIGN_ID}/stats
```

Returns per-step metrics including: `voice_notes_sent`, `voice_notes_listened`, `replies_after_voice`, `meetings_from_voice`.

**Unipile:**
```
GET https://api.unipile.com/api/v1/messages?type=voice_note&account_id={ACCOUNT_ID}
```

Returns delivery status and read receipts for voice messages.

### 5. Pause or stop voice note delivery

```
PUT https://api.lemlist.com/api/campaigns/{CAMPAIGN_ID}/pause
```

Pause immediately if: LinkedIn sends a restriction warning, reply rate drops below 2%, or more than 3 prospects report the message as spam.

## Voice Note Script Guidelines

LinkedIn voice notes have a 60-second limit. Target 20-30 seconds for outbound:

1. **Name drop** (3 sec): "Hey {first_name}..."
2. **Context** (5 sec): "I just connected with you because..."
3. **Signal reference** (5 sec): Why now -- reference their company news, role, or content.
4. **Value hook** (8 sec): One sentence about what you help companies like theirs do.
5. **Soft CTA** (5 sec): "Sending you a quick message with my calendar -- no pressure."
6. **Close** (3 sec): "Talk soon."

Tone: conversational, not scripted. Speak as if leaving a message for a colleague, not reading from a teleprompter. Slight imperfections (um, brief pause) actually increase trust.

## Safety Guardrails

- **Daily limits**: Maximum 20-30 voice notes per day via automation. LinkedIn monitors unusual messaging patterns.
- **Connection required**: Voice notes can only be sent to 1st-degree connections. The prospect must accept your connection request first.
- **Warm-up**: New LinkedIn accounts need 2-3 weeks of manual activity before automated voice notes. Start with 5/day and ramp to 20 over 2 weeks.
- **Personalization**: Never send identical voice scripts to more than 10 people. Use merge fields for prospect-specific details.
- **Stop on reply**: If a prospect replies to anything in the sequence, immediately stop all automated steps and hand off to human conversation.

## Error Handling

- **LinkedIn restriction**: Pause all automation for 72 hours. Reduce daily volume by 50% when resuming. Never exceed 25 voice notes/day even after ramp-up.
- **Audio rejected**: LinkedIn may reject audio files that are too short (<3 sec), too long (>60 sec), or in unsupported format. Re-encode as MP3 at 128kbps.
- **Prospect not connected**: Voice note step will fail if the connection request was not accepted. Set the step condition to `connected` to skip unconnected prospects.
- **AI voice sounds unnatural**: Increase ElevenLabs `stability` to 0.6 and `similarity_boost` to 0.8. Re-record your voice sample with more natural cadence if persistent.

## Pricing

| Tool | Plan | Cost | Voice Notes Included |
|------|------|------|---------------------|
| lemlist | Multichannel Expert | $99/user/mo | Unlimited (includes AI voice generation) |
| Expandi | Business | $99/seat/mo | Unlimited (bring your own audio) |
| Unipile | Growth | $47/mo per account | API calls included |
| La Growth Machine | Pro | $100/seat/mo | Unlimited multichannel |
| HeyReach | Starter | $79/seat/mo | Multi-account voice notes |

Note: lemlist includes ElevenLabs AI voice generation in the price. Other tools require you to generate audio separately (using the `ai-voice-generation` fundamental) and upload it.
