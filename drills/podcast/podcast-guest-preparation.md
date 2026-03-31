---
name: podcast-guest-preparation
description: Prepare the founder for a podcast guest appearance with talking points, bio assets, and tracking links
category: Podcast
tools:
  - Attio
  - PostHog
  - Dub.co
  - Cal.com
fundamentals:
  - podcast-tracking-links
  - attio-contacts
  - calcom-booking-links
  - posthog-custom-events
---

# Podcast Guest Preparation

This drill prepares everything the founder needs before, during, and immediately after a podcast recording. It ensures every appearance is tracked, maximizes impact, and captures follow-up opportunities.

## Input

- Confirmed podcast booking (podcast name, host name, recording date, episode topic)
- Founder's calendar with the recording slot booked
- The pitch angle that was accepted

## Steps

### 1. Research the podcast and host

Before the recording, gather context:
- Listen to 2-3 recent episodes of the show. Note the host's interview style (rapid-fire Q&A, deep-dive conversation, storytelling format).
- Read the host's LinkedIn and Twitter. Note any recent posts or opinions relevant to the episode topic.
- Check if the podcast has a pre-interview questionnaire (many do). Fill it out thoroughly — hosts use it to structure the episode.
- Identify the podcast's audience: what are their job titles, company sizes, pain points? Tailor talking points accordingly.

### 2. Build talking points

Create a structured talking points document for the founder:

```
## Episode: {{podcast_name}} — {{episode_topic}}
## Recording: {{recording_date}}

### Opening (first 2 min)
- Hook: {{attention-grabbing stat, story, or contrarian take related to topic}}
- Context: {{why founder is credible on this topic — 1 sentence}}

### Core talking points (3-5 points)
1. {{Point 1}}: {{Key insight + supporting evidence/story}}
2. {{Point 2}}: {{Key insight + supporting evidence/story}}
3. {{Point 3}}: {{Key insight + supporting evidence/story}}

### Stories to tell
- {{Story 1}}: {{Brief narrative that illustrates a key point — specific, with details}}
- {{Story 2}}: {{Customer success story or failure lesson}}

### Questions to expect
- "How did you get started with X?" → {{prepared answer}}
- "What's your advice for someone just starting?" → {{prepared answer}}
- "What's next for your company?" → {{prepared answer}}

### CTA (closing)
- "If you want to learn more, head to {{vanity_url}} — I set up a link just for {{podcast_name}} listeners."
- Offer: {{free resource, trial, or consultation specific to this audience}}
```

### 3. Create tracking links

Use `podcast-tracking-links` to create:
- A vanity URL specific to this podcast (e.g., `yoursite.com/saas-podcast`)
- UTM parameters: `utm_source=podcast&utm_medium=guest&utm_campaign={{podcast_slug}}&utm_content={{episode_date}}`
- A landing page or dedicated offer if appropriate (e.g., extended trial for podcast listeners)

Log the tracking link in PostHog using `posthog-custom-events`: fire a `podcast_appearance_scheduled` event with properties: podcast_name, host_name, recording_date, tracking_url.

### 4. Prepare technical setup

Send the founder a pre-recording checklist:
- **Audio**: Use a quality microphone (not laptop speakers). Test audio 15 min before.
- **Video** (if video podcast): Good lighting, clean background, camera at eye level.
- **Environment**: Quiet room, phone on silent, notifications off.
- **Recording backup**: Record locally using QuickTime or OBS as a backup in case the host's recording fails.

### 5. Send host a pre-interview packet

Email the host 2-3 days before recording:
- Founder's bio (50-word version for the intro)
- Headshot (link to high-res image)
- 3-5 suggested questions or topics (makes the host's prep easier)
- Social media handles for tagging when the episode drops
- Any links to include in show notes (tracking URL, relevant blog posts)

### 6. Post-recording follow-up

Within 24 hours of recording:
- Send the host a thank-you email
- Ask when the episode will air
- Ask them to include your tracking link in the show notes
- Offer to promote the episode to your audience when it drops
- Update Attio: move from "booked" to "recorded", set reminder for air date

Within 24 hours of episode airing:
- Share the episode on LinkedIn, Twitter, and newsletter
- Fire a `podcast_episode_aired` PostHog event with properties: podcast_name, episode_url, air_date
- Begin tracking UTM traffic in PostHog

## Output

- Talking points document for the founder
- Tracking links created and tested
- Host has all assets needed for show notes and intro
- Post-recording follow-up completed
- Attio and PostHog updated

## Triggers

- Run once per confirmed podcast booking, starting 5 days before recording date
