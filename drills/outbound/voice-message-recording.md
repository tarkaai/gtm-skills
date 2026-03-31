---
name: voice-message-recording
description: Generate personalized voice messages for a prospect batch using AI voice cloning or manual recording
category: Outreach
tools:
  - ElevenLabs
  - Clay
  - Attio
fundamentals:
  - ai-voice-generation
  - clay-enrichment-waterfall
  - attio-contacts
---

# Voice Message Recording

This drill produces a batch of personalized voice messages -- one per prospect -- ready for delivery via ringless voicemail or LinkedIn voice note. It covers both manual recording (Smoke level) and AI-generated voice cloning (Baseline+).

## Input

- Prospect list in Clay or Attio with enrichment data (name, company, role, trigger signal)
- ICP definition with pain points and value propositions
- For AI generation: founder voice sample (1-3 minute audio clip)
- For manual recording: phone or laptop with microphone

## Steps

### 1. Prepare prospect-specific scripts

Open your Clay table with the target prospect batch. Each prospect needs these columns populated:

- First name
- Company name
- Trigger signal (e.g., "just raised Series A", "hired 3 engineers this month", "switched to {competitor}")
- Value prop hook (one sentence connecting their signal to your solution)

If columns are missing, use the `clay-enrichment-waterfall` fundamental to fill gaps. Add a Clay AI formula column that generates a complete voice script per prospect:

```
Template:
"Hey {first_name}, this is {founder_name} from {company}. I noticed {company_name} {signal}. {value_prop_hook}. Would love to grab 15 minutes -- I'll send my calendar link in a follow-up message. Talk soon."
```

Target length: 50-80 words (20-35 seconds of audio).

### 2a. Manual recording (Smoke level)

Record each message yourself using your phone's voice memo app, Loom audio-only, or your laptop microphone.

Workflow per prospect:
1. Open the prospect's script in Clay
2. Read it aloud naturally -- do NOT sound like you're reading
3. If you stumble, re-record immediately (faster than editing)
4. Save as MP3 or M4A
5. Name the file: `vm-{company-slug}-{firstname}.mp3`

Target pace: 2-3 minutes per message including setup. A 20-prospect batch takes ~50 minutes.

Tips for natural delivery:
- Smile while recording -- it changes your tone
- Stand up -- it adds energy to your voice
- Pause briefly after the prospect's name -- it sounds more personal
- Vary your intonation -- monotone = instant delete

### 2b. AI voice generation (Baseline+ level)

Use the `ai-voice-generation` fundamental:

1. **One-time setup**: Upload your founder voice sample to ElevenLabs (or Play.ht / Resemble.AI). Store the returned `voice_id`.

2. **Batch generation**: Build an n8n workflow or script that:
   - Pulls prospect scripts from Clay (the AI formula column from Step 1)
   - Calls the ElevenLabs TTS API for each script with your cloned voice
   - Saves each audio file with the naming convention `vm-{company-slug}-{firstname}.mp3`
   - Uploads the audio URL back to a Clay column for delivery mapping

3. **Quality check**: Listen to a random sample of 5 messages from each batch. Check for:
   - Pronunciation of company names and prospect names
   - Natural intonation (not robotic or flat)
   - Correct pacing (not too fast, not too slow)
   - No audio artifacts or glitches

   If names are mispronounced, add phonetic spelling to the script: "Hey Sarah at Ack-me Corp" instead of "Hey Sarah at Acme Corp" (if the AI mispronounces it).

### 3. Build the delivery mapping

Create a mapping table (in Clay or CSV) connecting each prospect to their audio file:

| Prospect Email | First Name | Company | Phone | LinkedIn URL | Audio File URL | Audio Duration |
|----------------|------------|---------|-------|-------------|----------------|----------------|

This table feeds into the `voice-message-delivery` drill for both ringless voicemail and LinkedIn voice note channels.

### 4. Log in CRM

Using the `attio-contacts` fundamental, update each prospect record in Attio with:
- `voice_message_generated: true`
- `voice_message_url: {audio_file_url}`
- `voice_message_campaign: {campaign_slug}`
- `voice_message_script: {script_text}`

This creates an audit trail and prevents duplicate messages to the same prospect.

## Output

- One personalized audio file per prospect (MP3, 20-35 seconds)
- Delivery mapping table linking prospects to their audio files
- CRM records updated with voice message metadata

## Triggers

Run for each new prospect batch entering the voice message play. At Smoke: 1 batch of 20-40 prospects. At Baseline: 2-3 batches per week of 25-50. At Scalable: daily batches of 50+ via automated pipeline.
