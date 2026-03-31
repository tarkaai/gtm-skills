---
name: podcast-sponsor-ad-copy
description: Write host-read podcast ad scripts and talking points for paid sponsorship placements
tool: Anthropic
difficulty: Config
---

# Podcast Sponsor Ad Copy

Generate host-read podcast ad scripts (talking points) for paid sponsorship placements. Unlike written newsletter blurbs, podcast ad copy must sound natural when spoken aloud and give the host enough structure to deliver a compelling read while maintaining their authentic voice.

## Prerequisites

- Booked podcast sponsorship placement (from `podcast-sponsor-rate-negotiation`)
- Ad format confirmed: pre-roll (15-30 sec), mid-roll (60 sec), or post-roll (15-30 sec)
- Landing page URL with tracking parameters configured
- Promo code or vanity URL for verbal CTA
- Understanding of the podcast's tone and audience

## Steps

### 1. Research the podcast's ad style

Before writing, listen to 2-3 recent episodes that contain sponsor reads. Note:
- How does the host transition into ad reads? (Natural segue vs. explicit "a word from our sponsors")
- How conversational is the read? (Script-exact vs. loose talking points)
- Does the host add personal anecdotes or opinions about the product?
- What verbal CTAs do other sponsors use? (URL, promo code, "link in show notes")
- How long are typical reads? (Some hosts go over the contracted time; others are tight)

This tells you whether to provide a full script or talking points.

### 2. Generate ad copy variants

Use the Anthropic API to generate 3 variants:

```
POST https://api.anthropic.com/v1/messages
Authorization: Bearer {ANTHROPIC_API_KEY}
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1024,
  "messages": [{
    "role": "user",
    "content": "Write 3 podcast host-read ad script variants for a {ad_duration}-second ad placement on {podcast_name}. The podcast covers {podcast_topics} for an audience of {audience_description}.\n\nProduct: {product_name} — {product_one_liner}\nKey benefit: {primary_benefit_for_this_audience}\nCTA: Visit {vanity_url} or use promo code {promo_code}\n\nRules:\n- Write as talking points, not a word-for-word script (hosts prefer flexibility)\n- Lead with a problem the listener recognizes, not the product name\n- Include exactly one stat, proof point, or social proof line\n- End with one clear verbal CTA (the vanity URL or promo code)\n- Keep the tone conversational — this will be spoken, not read\n- Variant A: Problem-led (start with a pain point)\n- Variant B: Story-led (start with a brief anecdote or scenario)\n- Variant C: Data-led (start with a surprising stat)\n\nFor each variant, also provide:\n- A one-line transition suggestion the host can use to segue into the read\n- The show notes text (2-3 sentences + the tracked URL) to be included in the episode description"
  }]
}
```

### 3. Validate copy constraints

Check each variant against the ad format requirements:

- **Pre-roll (15-30 sec)**: 40-75 words. One key message + CTA. No room for stories.
- **Mid-roll (60 sec)**: 140-170 words. Problem + benefit + proof + CTA. This is the sweet spot.
- **Post-roll (15-30 sec)**: 40-75 words. Brief recap + CTA. Often repeats the mid-roll CTA.
- **Custom integration (2-5 min)**: 300-700 words. Full discussion-style. Include 3-4 talking points the host can riff on.

Read each variant aloud at natural speaking pace to verify timing. Average speaking rate: ~150 words per minute.

### 4. Build the verbal CTA

Podcast listeners hear the CTA — they cannot click it. Design for recall:

**Option A: Vanity URL**
```
"Head to {yoursite.com/podcast-name} — I set up a special page just for {podcast_name} listeners."
```

The vanity URL must:
- Be short and memorable (max 3 syllables after the domain)
- Be easy to spell when heard aloud
- Redirect to the UTM-tagged landing page (set up via `podcast-sponsor-placement-tracking`)

**Option B: Promo code**
```
"Use code {PODCASTNAME} at checkout for [discount]. That's {spell it out} — {PODCASTNAME}."
```

Promo codes should:
- Match the podcast name (easy to remember)
- Be all-caps, no numbers or special characters
- Be spelled out in the script to prevent confusion

**Option C: Both (preferred for mid-roll)**
```
"Visit {vanity_url} or use code {PROMO} at checkout."
```

### 5. Prepare the submission package

Send to the podcast host/producer before the script deadline:

- **Talking points document**: The selected variant formatted as bullet points (not a rigid script)
- **Show notes text**: 2-3 sentences about your product + the tracked URL for the episode description
- **Vanity URL**: Confirm it resolves correctly
- **Promo code**: Confirm it is active and the discount/offer is live
- **Logo/brand assets**: If the podcast publishes episode art with sponsor logos (provide PNG, 500px+ square)
- **Pronunciation guide**: If your product name has an unusual pronunciation, spell it phonetically

Include a note: "Feel free to put this in your own words — these are talking points, not a script. The URL and promo code are the two things that need to stay exact."

### 6. Log in CRM

Use Attio to record:
- Ad variant selected (A, B, or C) and the angle (problem/story/data)
- Full script text
- Vanity URL and promo code used
- Submission date
- Episode air date

This creates a record for performance comparison across variants and podcasts.

## Output

- 3 host-read ad script variants tailored to the podcast's audience and tone
- Show notes text with tracked URL
- Verbal CTA (vanity URL and/or promo code)
- Submission package ready for the host

## Error Handling

- **Host rewrites the script significantly**: Accept it — hosts know their audience best. Verify the CTA URL and promo code survived intact.
- **Host requests revisions**: Provide revised talking points within 24 hours. Use the Anthropic API to iterate.
- **Promo code conflicts**: Check that the code is not already in use by another campaign before assigning it.
- **Vanity URL not set up**: Prioritize URL setup before script submission. Fall back to "link in the show notes" CTA if the vanity URL is not ready.

## Alternative Tools

- **Anthropic Claude**: Primary for generating ad copy variants
- **OpenAI GPT-4**: Alternative LLM for copy generation
- **Jasper**: AI copywriting tool with ad copy templates
- **Copy.ai**: Alternative AI copywriting platform
- **Descript**: If producing a pre-recorded ad spot, use for recording + editing
