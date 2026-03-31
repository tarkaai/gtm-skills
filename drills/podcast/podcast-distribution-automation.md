---
name: podcast-distribution-automation
description: Automated cross-platform promotion workflow triggered when a new podcast episode publishes
category: Podcast
tools:
  - n8n
  - Descript
  - LinkedIn
  - Loops
  - Attio
  - PostHog
fundamentals:
  - n8n-triggers
  - n8n-workflow-basics
  - podcast-episode-repurposing
  - podcast-tracking-links
  - linkedin-organic-posting
  - loops-broadcasts
  - attio-notes
  - posthog-custom-events
---

# Podcast Distribution Automation

This drill builds an n8n-powered automation that fires when a new episode publishes and executes a multi-day cross-platform promotion sequence. Instead of manually posting about each episode, the agent prepares and schedules all promotion assets in advance and the automation distributes them on a timed cadence.

## Input

- Published episode with finalized show notes and tracking links
- Repurposed assets prepared (clips, audiograms, social posts, pull quotes) from `podcast-episode-repurposing`
- n8n instance configured with social platform credentials
- Email list in Loops for episode notifications

## Steps

### 1. Build the episode promotion trigger

Use `n8n-triggers` to create a webhook or RSS-poll trigger:

**Option A: RSS poll trigger**
Configure n8n to poll your podcast RSS feed every 30 minutes. When a new `<item>` appears that was not present in the previous poll, trigger the promotion workflow.

**Option B: Webhook trigger**
If your hosting platform supports webhooks (Transistor does), configure it to POST to your n8n webhook URL when an episode publishes. Buzzsprout does not support webhooks natively -- use the RSS poll approach.

### 2. Build the Day 0 workflow (publish day)

When triggered, the n8n workflow executes:

1. **Fire PostHog event**: Use `posthog-custom-events` to log `podcast_episode_published` with properties: `episode_number`, `episode_title`, `guest_name`, `publish_date`, `tracking_url`
2. **Send email notification**: Use `loops-broadcasts` to send a "New Episode" email to your podcast subscriber list. Include: episode title, guest name, 2-sentence hook, listen links (Apple Podcasts, Spotify, website), and your tracking URL.
3. **Post to LinkedIn**: Use `linkedin-organic-posting` to publish a launch post. Format: hook about the episode topic, 2-3 key takeaways as bullets, guest tag, episode link.
4. **Post to Twitter/X**: Publish a launch tweet with the episode title, a compelling one-liner from the episode, and a link. Tag the guest.
5. **Update CRM**: Use `attio-notes` to add a note on the episode record in Attio: "Episode published, Day 0 promotion sent."
6. **Notify guest**: Send the guest an automated email with: the episode link, pre-written social posts they can copy-paste to share, a request to share with their audience.

### 3. Build the Day 1-7 drip workflow

Schedule follow-up promotions across the week using n8n delay nodes:

**Day 1**: Post clip #1 (the most compelling 60-second moment) on LinkedIn. Post the same clip on Twitter.

**Day 2**: Share a pull quote image on LinkedIn and Twitter. Post the episode in relevant Slack/Discord communities (if the guest is a community member, tag them).

**Day 3**: Post clip #2 on LinkedIn. Cross-post to YouTube Shorts if video.

**Day 5**: Post a "behind the scenes" or "what I learned from this conversation" reflective post on LinkedIn. This is organic founder content that references the episode without being pure promotion.

**Day 7**: Final clip (#3) on LinkedIn. Share the episode in your email newsletter's next scheduled send (if not a dedicated podcast newsletter).

### 4. Build guest amplification tracking

After sending the guest their share kit (Day 0), track whether they shared:
- Search LinkedIn for the guest's posts mentioning your podcast name or episode title (use `linkedin-organic-feed-search` if available, or check manually)
- If the guest shared, log "Guest amplified: yes" in Attio and engage with their post (like, comment, reshare)
- If the guest has not shared after 3 days, send a gentle reminder with the pre-written posts

### 5. Configure episode-specific tracking links

Use `podcast-tracking-links` to create unique UTM parameters for each promotion channel:

```
LinkedIn posts:  ?utm_source=linkedin&utm_medium=organic&utm_campaign=podcast-ep{number}
Twitter posts:   ?utm_source=twitter&utm_medium=organic&utm_campaign=podcast-ep{number}
Email blast:     ?utm_source=email&utm_medium=newsletter&utm_campaign=podcast-ep{number}
Guest shares:    ?utm_source=guest&utm_medium=social&utm_campaign=podcast-ep{number}
```

This lets you attribute traffic and leads to specific promotion channels per episode.

### 6. Set up recurring promotion for evergreen episodes

For episodes that continue performing well after the initial promotion week:
- Create an n8n workflow that re-shares a clip or quote from a high-performing past episode every 2 weeks
- Select episodes based on: highest download count, highest UTM click-through, highest lead attribution
- Rotate through the back catalog so no episode is re-promoted more than once per quarter

## Output

- Automated 7-day promotion sequence triggered by each new episode publish
- Cross-platform distribution (LinkedIn, Twitter, email, communities)
- Guest amplification tracking and follow-up
- Per-channel UTM tracking for attribution
- Evergreen re-promotion of top episodes

## Triggers

- Primary: Fires automatically when RSS feed updates with a new episode
- Evergreen: Runs bi-weekly on a cron schedule, selecting from the back catalog
