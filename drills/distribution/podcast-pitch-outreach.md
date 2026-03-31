---
name: podcast-pitch-outreach
description: Craft and send personalized podcast guest pitch sequences to podcast hosts
category: Podcast
tools:
  - Instantly
  - Attio
  - Clay
fundamentals:
  - podcast-pitch-email
  - instantly-campaign
  - attio-contacts
  - clay-enrichment-waterfall
---

# Podcast Pitch Outreach

This drill takes a qualified podcast list and runs a personalized pitch campaign to book the founder as a guest. It handles pitch copy creation, personalization, sending, and reply management.

## Input

- Enriched podcast prospect list from `podcast-prospect-research` drill (in Attio or Clay)
- Founder's bio, areas of expertise, and 3-5 ready pitch angles
- Founder's social proof: prior speaking, published content, podcast appearances, notable achievements
- Calendar link for booking (Cal.com or Calendly)

## Steps

### 1. Prepare pitch angles

Before sending any emails, define 3-5 distinct pitch angles the founder can speak on. Each angle should be:
- Specific enough to be an episode topic (not "I can talk about marketing")
- Tied to a trend, contrarian take, or data point
- Relevant to the podcast's audience

Example angles:
- "Why most B2B startups waste 60% of their marketing budget on the wrong stage"
- "How we grew from $0 to $1M ARR using only founder-led sales"
- "The AI agent stack replacing traditional SDR teams"

### 2. Create the founder one-sheet

Build a one-page document (Google Doc or Notion page) that includes:
- Founder headshot (high-res link)
- Bio (50 words and 150 words versions)
- Company one-liner
- 3-5 episode topic ideas with bullet-point talking points
- Links to prior podcast appearances or talks
- Social media links
- Calendar booking link

Host this at a public URL. Include this link in follow-up emails when a host expresses interest.

### 3. Personalize each pitch

For each podcast on the list, customize the pitch using `podcast-pitch-email` framework:
- Listen to or read the description of a recent episode. Write one specific sentence about it.
- Match one of your pitch angles to the podcast's usual topics.
- Reference a previous guest to show you understand the show's format.

Use Clay columns to store personalization variables: `recent_episode_topic`, `recent_guest_name`, `specific_observation`, `best_pitch_angle`.

### 4. Send pitches

**Smoke (5-10 pitches):** Send manually from the founder's personal email. Higher trust, appropriate for low volume.

**Baseline (15-25 pitches):** Use Instantly with the `instantly-campaign` fundamental. Create a campaign with the 3-email sequence from `podcast-pitch-email`. Map Clay merge fields. Set sending schedule: Tue-Thu, 9am-11am in the host's timezone.

**Scalable (50+ pitches):** Use Instantly with inbox rotation across 2-3 sending accounts. Segment by podcast tier: Tier 1 gets the most personalized version, Tier 3 can use lighter personalization.

### 5. Handle replies

Monitor Instantly (or inbox) for replies. Classify and act:

- **"Yes, let's book"**: Immediately reply with the founder's calendar link and one-sheet. Update Attio: status = "booked", add recording date.
- **"Send more info"**: Reply with the one-sheet link and 2-3 specific topic ideas tailored to their show. Update Attio: status = "interested".
- **"Not right now"**: Reply thanking them, ask if you can re-pitch in 3 months. Update Attio: status = "nurture", set reminder.
- **"Fill out our guest form"**: Go to their form and submit. Update Attio: status = "form submitted".
- **"No thanks"**: Reply graciously. Update Attio: status = "declined". Do not re-pitch.
- **No reply after full sequence**: Update Attio: status = "no response". Re-pitch in 6 months with a new angle.

### 6. Track conversion metrics

Log in PostHog or a tracking spreadsheet:
- Emails sent
- Open rate
- Reply rate
- Positive reply rate (interested + booked)
- Booking rate (booked / emails sent)
- Time from first pitch to recording date

Target benchmarks: 30-50% open rate, 10-20% reply rate, 5-10% booking rate.

## Output

- Podcast guest bookings in the founder's calendar
- Attio list updated with pitch status for every podcast
- Conversion metrics for optimizing future pitch campaigns

## Triggers

- Run once per batch of new podcast prospects
- Re-run the sequence with new angles every quarter for "no response" contacts
