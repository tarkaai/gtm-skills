---
name: founder-guest-podcasts-baseline
description: >
  Founder Guest Podcast — Baseline Run. Scale to 20+ pitches with tracking infrastructure,
  book 3+ appearances, and measure whether podcast traffic converts to inbound leads.
stage: "Marketing > Unaware"
motion: "PR & Earned Mentions"
channels: "Content"
level: "Baseline Run"
time: "12 hours over 4 weeks"
outcome: "≥ 3 podcast bookings AND ≥ 1 inbound lead from aired episodes"
kpis: ["Pitches sent", "Booking rate", "Episode referral traffic", "Leads from podcast traffic"]
slug: "founder-guest-podcasts"
install: "npx gtm-skills add marketing/unaware/founder-guest-podcasts"
drills:
  - podcast-prospect-research
  - podcast-pitch-outreach
  - posthog-gtm-events
  - threshold-engine
---

# Founder Guest Podcast — Baseline Run

> **Stage:** Marketing → Unaware | **Motion:** PR & Earned Mentions | **Channels:** Content

## Outcomes

Book 3+ podcast guest appearances and generate at least 1 inbound lead from aired episodes. This validates the full cycle: pitch → book → record → air → traffic → lead. Tracking infrastructure proves the channel is measurable.

## Leading Indicators

- Booking rate ≥ 10% of pitches sent (≥ 3 bookings from 20-30 pitches)
- Tracking links receive clicks within 7 days of episode airing
- Referral traffic from podcast UTMs appears in PostHog
- At least 1 listener visits the site and takes a conversion action (signup, form fill, meeting book)

## Instructions

### 1. Expand the podcast prospect list

Run the `podcast-prospect-research` drill at Baseline scale:
- Search ListenNotes with 5-8 keyword combinations
- Cross-reference competitor/peer guest appearances on at least 5 names
- Qualify 25-30 podcasts (active, accepts guests, listen_score >= 20)
- Use Clay to enrich host contact info: run email waterfall (RSS email → Clay email finder → Apollo → LinkedIn)
- Score and rank by composite: topic fit (40%), audience size (30%), accessibility (20%), recency (10%)
- Push top 20-25 to Attio with tier tags

### 2. Set up podcast tracking in PostHog

Run the `posthog-gtm-events` drill to configure podcast-specific events:
- `podcast_pitch_sent` — properties: podcast_name, host_name, pitch_angle, date
- `podcast_booking_confirmed` — properties: podcast_name, recording_date
- `podcast_episode_aired` — properties: podcast_name, episode_url, air_date, tracking_url
- `podcast_referral_visit` — captured automatically via UTM params (utm_source=podcast, utm_medium=guest)
- `podcast_lead_created` — properties: podcast_name, lead_email, conversion_action

### 3. Pitch 20-25 podcast hosts

Run the `podcast-pitch-outreach` drill at Baseline scale:
- Set up a 3-email sequence in Instantly (pitch → follow-up at day 5 → final bump at day 12)
- Personalize each pitch: reference a recent episode, match a pitch angle, include social proof
- Send from the founder's domain via Instantly (maintains personal feel with automation)
- Monitor replies daily and classify: booked / interested / nurture / declined / no response

### 4. Prepare for each booked appearance

Run the the podcast guest preparation workflow (see instructions below) drill for each booking:
- Research the podcast and host (listen to 2-3 episodes, review host's social media)
- Build a talking points document with opening hook, 3-5 core points, stories, and CTA
- Create a tracking link: vanity URL (e.g., yoursite.com/podcast-name) redirecting to UTM-tagged URL
- Send the host a pre-interview packet: bio, headshot, suggested questions, social handles, tracking link for show notes
- After recording: thank-you email, ask for air date, request tracking link in show notes

### 5. Promote aired episodes

When episodes air:
- Share on LinkedIn, Twitter, and email newsletter
- Fire `podcast_episode_aired` event in PostHog
- Monitor UTM traffic in PostHog for 30 days post-air
- Ask host for download numbers at 7 days and 30 days

### 6. Evaluate against threshold

Run the `threshold-engine` drill: (a) did you book ≥ 3 appearances? (b) did aired episodes generate ≥ 1 inbound lead? Both must pass. If booking rate is low, refine pitch angles or target different podcast tiers. If traffic converts poorly, test different CTAs or landing pages.

## Time Estimate

- 3 hours: Podcast research, Clay enrichment, list building
- 3 hours: Pitch writing, personalization, Instantly setup
- 2 hours: Guest preparation (per booking, ~40 min each for 3 bookings)
- 2 hours: PostHog event setup and dashboard configuration
- 2 hours: Reply management, episode promotion, follow-ups

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| ListenNotes | Podcast search and discovery | Free tier or $9/mo for 300 req/day ([pricing](https://www.listennotes.com/api/pricing/)) |
| Clay | Host enrichment and email verification | Credits-based ([pricing](https://clay.com/pricing)) |
| Instantly | Automated pitch sequences | Growth: $37/mo ([pricing](https://instantly.ai/pricing)) |
| Dub.co | Vanity tracking links | Free: 25 links/mo ([pricing](https://dub.co/pricing)) |
| PostHog | Event tracking and UTM attribution | Free tier: 1M events/mo ([pricing](https://posthog.com/pricing)) |
| Attio | Pipeline tracking for podcast pitches | Part of default stack |

**Estimated play-specific cost:** $0-50/mo (ListenNotes free tier + Instantly Growth + Dub.co free)

## Drills Referenced

- `podcast-prospect-research` — find and qualify 25-30 target podcasts with Clay enrichment
- `podcast-pitch-outreach` — send 20-25 automated pitch sequences via Instantly
- `posthog-gtm-events` — configure podcast-specific tracking events
- the podcast guest preparation workflow (see instructions below) — prep the founder and create tracking links for each booking
- `threshold-engine` — evaluate pass/fail against booking + lead thresholds
