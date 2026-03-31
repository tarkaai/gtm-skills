---
name: ai-voice-generation
description: Clone a voice from audio samples and generate personalized voice messages at scale via TTS APIs
tool: Voice AI
product: Voice API
difficulty: Setup
---

# AI Voice Generation

Generate AI-cloned voice messages from text scripts. Record a voice sample once, then produce unlimited personalized audio messages by passing prospect-specific scripts to the TTS API. This is the core fundamental for scaling voice outreach beyond manual recording.

## Tool Options

| Tool | API Docs | Best For |
|------|----------|----------|
| ElevenLabs | https://elevenlabs.io/docs/api-reference | Highest quality voice cloning, multilingual, lowest latency |
| Play.ht | https://docs.play.ht/reference | Ultra-realistic clones, emotion control, long-form audio |
| Resemble.AI | https://docs.resemble.ai | Real-time cloning, watermarking, compliance features |
| WellSaid | https://developer.wellsaidlabs.com | Enterprise-grade, SOC 2, team voice management |
| Deepgram | https://developers.deepgram.com/docs/text-to-speech | Low cost at scale, fast inference, developer-friendly |

## Authentication

**ElevenLabs:**
```
xi-api-key: {ELEVENLABS_API_KEY}
Base URL: https://api.elevenlabs.io/v1
```

**Play.ht:**
```
Authorization: Bearer {PLAYHT_API_KEY}
X-User-Id: {PLAYHT_USER_ID}
Base URL: https://api.play.ht/api/v2
```

**Resemble.AI:**
```
Authorization: Bearer {RESEMBLE_API_KEY}
Base URL: https://app.resemble.ai/api/v2
```

## Operations

### 1. Clone a voice from audio sample

Record a 1-3 minute audio sample of the founder speaking naturally. Read a script that includes varied intonation, questions, and statements. Export as WAV or MP3 (16kHz+ sample rate).

**ElevenLabs (instant voice clone):**
```
POST https://api.elevenlabs.io/v1/voices/add
Content-Type: multipart/form-data

name: "founder-outreach-voice"
files: @founder-sample.mp3
description: "Founder voice for outbound sales voice messages"
labels: {"use_case": "outbound_sales", "accent": "american"}
```

Response includes `voice_id` — store this in your `.gtm-config.json` or environment variables.

**Play.ht:**
```
POST https://api.play.ht/api/v2/cloned-voices/instant
Content-Type: multipart/form-data

voice_name: "founder-outreach"
sample_file: @founder-sample.mp3
```

**Resemble.AI:**
```
POST https://app.resemble.ai/api/v2/voices
{
  "name": "founder-outreach",
  "dataset_url": "https://storage.example.com/founder-sample.mp3",
  "callback_uri": "https://your-n8n.example.com/webhook/resemble-voice-ready"
}
```

### 2. Generate a single voice message from text

**ElevenLabs:**
```
POST https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}
Content-Type: application/json

{
  "text": "Hey Sarah, this is Dan from Tarka. I noticed Acme just closed a Series B -- congrats. We've been helping similar dev-tools companies automate their outbound pipeline. Would love 15 minutes to show you what we built. My calendar link is in the email I sent you yesterday. Talk soon.",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.3,
    "use_speaker_boost": true
  }
}
```

Response: audio stream (MP3 by default). Save to file or upload to CDN.

**Play.ht:**
```
POST https://api.play.ht/api/v2/tts
{
  "text": "Hey Sarah, this is Dan from Tarka...",
  "voice": "{CLONED_VOICE_ID}",
  "output_format": "mp3",
  "speed": 1.0,
  "quality": "premium"
}
```

### 3. Batch-generate voice messages for a prospect list

Build an n8n workflow or script that iterates over a Clay/Attio prospect list and generates one audio file per prospect:

```python
import requests
import json

ELEVENLABS_KEY = "your-api-key"
VOICE_ID = "your-cloned-voice-id"

def generate_voice_message(prospect):
    script = f"Hey {prospect['first_name']}, this is Dan from Tarka. " \
             f"I noticed {prospect['company']} {prospect['signal']}. " \
             f"{prospect['value_prop_hook']} " \
             f"Would love to grab 15 minutes -- my calendar's in the email I sent. Talk soon."

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"},
        json={
            "text": script,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
    )

    filename = f"vm-{prospect['slug']}.mp3"
    with open(filename, "wb") as f:
        f.write(response.content)

    return filename
```

Target pace: ~2 seconds per generation via API. A 50-prospect batch completes in under 2 minutes.

### 4. Retrieve voice usage and quota

**ElevenLabs:**
```
GET https://api.elevenlabs.io/v1/user/subscription
```
Returns `character_count` (used), `character_limit` (quota), and `next_character_count_reset_unix`.

### 5. Delete a voice clone

**ElevenLabs:**
```
DELETE https://api.elevenlabs.io/v1/voices/{VOICE_ID}
```

## Voice Message Script Guidelines

Keep messages 20-40 seconds (50-100 words). Structure:
1. **Greeting** (3 sec): "Hey {first_name}, this is {your_name} from {company}."
2. **Signal reference** (5 sec): "I noticed {company} just {trigger_signal}."
3. **Value hook** (8 sec): One sentence connecting their signal to your solution.
4. **CTA** (5 sec): "Would love 15 minutes -- my calendar link is in the email I sent."
5. **Sign-off** (3 sec): "Talk soon."

Never: pitch features, mention pricing, or go over 45 seconds.

## Error Handling

- **Rate limits**: ElevenLabs allows ~100 concurrent requests. Queue in n8n and process sequentially if batching more than 100.
- **Character quota exceeded**: Monitor via subscription endpoint. Switch to a lower-cost model (`eleven_flash_v2` at $0.06/1k chars vs $0.12/1k) or upgrade plan.
- **Audio quality issues**: If cloned voice sounds robotic, increase `similarity_boost` to 0.85. If too monotone, increase `style` to 0.4-0.5.
- **Language mismatch**: Use `eleven_multilingual_v2` for non-English prospects. Specify the language in the text naturally -- the model auto-detects.

## Pricing

| Tool | Plan | Cost | Included |
|------|------|------|----------|
| ElevenLabs | Starter | $5/mo | 30,000 chars (~30 min audio) |
| ElevenLabs | Creator | $22/mo | 100,000 chars (~100 min audio) |
| ElevenLabs | Pro | $99/mo | 500,000 chars (~500 min audio) |
| Play.ht | Creator | $31.20/mo | Unlimited words, 2 clones |
| Play.ht | Unlimited | $99.50/mo | Unlimited words, unlimited clones |
| Resemble.AI | Pay-as-you-go | $0.006/sec | No minimum |
| Deepgram | Pay-as-you-go | $0.0150/1k chars | No minimum |

At ~80 words per message (~400 chars), ElevenLabs Starter handles ~75 messages/mo; Creator handles ~250 messages/mo; Pro handles ~1,250 messages/mo.
