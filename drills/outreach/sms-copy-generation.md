---
name: sms-copy-generation
description: Generate personalized SMS outreach copy using prospect data, pain signals, and AI
category: SMS
tools:
  - Anthropic
  - Clay
  - Attio
fundamentals:
  - clay-claygent
  - attio-contacts
---

# SMS Copy Generation

Generate high-converting SMS outreach copy personalized to each prospect using their enrichment data, buying signals, and pain points. SMS copy is fundamentally different from email: it must be conversational, ultra-concise, and feel like a human text, not a marketing blast.

## Input

- Prospect list in Attio with enrichment data: first_name, company, title, pain_signal, industry
- ICP document with pain points and value propositions
- Company proof points (customer results, case studies with specific metrics)

## Steps

### 1. Assemble personalization context per prospect

For each prospect, pull from Attio and Clay:
- First name, company name, title
- The buying signal that triggered outreach (job change, funding, hiring)
- Company industry and size
- Any prior touchpoints (email opens, LinkedIn connections)

### 2. Generate SMS copy via Claude

For each prospect, generate the 3-message sequence using this prompt structure:

```
You are writing a 3-message SMS outreach sequence from a B2B startup founder to a prospect.

CONSTRAINTS:
- Each message MUST be under 155 characters (leave room for merge field expansion)
- Write like a real person texting, not a marketer
- No emojis except one thumbs-up or similar if natural
- No ALL CAPS words
- No exclamation points
- No "Hey there!" or "Hope this finds you well"
- Message 1 MUST end with "Reply STOP to opt out"
- Use contractions (we're, you're, I'd)
- Reference something specific about the prospect or their company

PROSPECT CONTEXT:
- Name: {{first_name}}
- Company: {{company}}
- Title: {{title}}
- Signal: {{signal_description}}
- Industry: {{industry}}

OUR VALUE PROP: {{one_sentence_value_prop}}
OUR PROOF POINT: {{customer_name}} achieved {{specific_result}} in {{timeframe}}
BOOKING LINK: {{cal_link}}

Write 3 messages:
MSG 1 (Day 1): Pain-aware opener referencing the signal. Soft question CTA. Include STOP opt-out.
MSG 2 (Day 3): Proof point from a similar company. Reply YES CTA.
MSG 3 (Day 6): Graceful breakup with booking link.
```

### 3. Validate character counts

After generation, programmatically verify each message is under 160 characters after merge field resolution. If over, regenerate with stricter length constraint. Multi-segment messages (>160 chars) cost 2x and display poorly on some devices.

### 4. Store copy variants

Save generated copy to Attio as contact notes tagged `sms-copy`. Store the variant ID so you can track which copy version each prospect received for A/B analysis.

### 5. Generate A/B variants at scale

For Scalable level, generate 2-3 variants of Message 1 (the opener) per ICP segment:
- Variant A: Signal-based opener (references the specific buying signal)
- Variant B: Pain-based opener (references a common industry pain point)
- Variant C: Social-proof opener (leads with a relevant customer result)

Assign variants randomly using PostHog feature flags. Track reply rate per variant.

## Output

- Personalized 3-message SMS sequence per prospect stored in Attio
- Character-count validated
- A/B variant assignments logged for experiment tracking
