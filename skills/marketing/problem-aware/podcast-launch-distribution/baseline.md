---
name: podcast-launch-distribution-baseline
description: >
  Branded Podcast Launch — Baseline Run. Establish a weekly episode cadence with automated distribution,
  guest booking pipeline, and PostHog tracking to sustain 500+ downloads/episode over 10 weeks.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=500 downloads/episode and >=10 qualified leads from first 10 episodes over 10 weeks"
kpis: ["Downloads per episode (7-day)", "Episode-to-lead conversion rate", "Guest booking rate", "Listener growth week-over-week"]
slug: "podcast-launch-distribution"
install: "npx gtm-skills add marketing/problem-aware/podcast-launch-distribution"
drills:
  - posthog-gtm-events
  - threshold-engine
---
# Branded Podcast Launch — Baseline Run

> **Stage:** Marketing -> Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Outcomes
First always-on automation. The podcast runs on a consistent weekly schedule. Distribution is automated -- publishing an episode triggers a multi-day promotion sequence across channels. A guest booking pipeline feeds the show with relevant guests. PostHog tracks every episode's impact on website traffic and leads. Results hold over 10 weeks.

## Leading Indicators
- Downloads per episode increasing or holding steady week-over-week
- At least 3 guests booked 2+ weeks ahead at any given time (pipeline health)
- Automated distribution workflow fires correctly each publish day
- UTM-attributed traffic from podcast exceeds baseline website traffic by >=5%
- At least 1 qualified lead per episode on average

---

## Budget

**Play-specific tools & costs**
- Buzzsprout or Transistor: $12-19/mo (podcast hosting with analytics)
- Riverside Creator: $15/mo (high-quality remote recording)
- Descript Pro: $24/mo (editing and transcription)
- Cal.com: Free tier or $12/mo (guest booking links)

**Total play-specific:** ~$50-70/mo

_Your CRM, PostHog, and automation platform are not included -- standard stack paid once._

---

## Instructions

### 1. Build the guest booking pipeline

Run the the podcast guest booking workflow (see instructions below) drill to create a repeatable system for sourcing and booking guests:

1. Define your ideal guest profile at each tier (Tier 1: big names, Tier 2: domain experts, Tier 3: customers/practitioners)
2. Use Clay to build a prospect list of 30-50 potential guests
3. Enrich contacts and send the first batch of 15-20 invitations
4. Set up an Attio pipeline to track: Sourced -> Invited -> Interested -> Booked -> Recorded -> Published
5. Configure Cal.com with a dedicated "Podcast Recording" event type: 45-minute slots, buffer time before/after, available Tue-Thu 10am-4pm

Target: maintain at least 3 booked guests at all times, with the next 3-4 weeks of episodes scheduled.

### 2. Set up automated episode distribution

Run the the podcast distribution automation workflow (see instructions below) drill to build the always-on promotion system:

1. Configure an n8n workflow that triggers when your RSS feed updates with a new episode
2. The workflow executes a 7-day promotion sequence per episode:
   - Day 0: Email notification to subscribers (Loops), LinkedIn launch post, Twitter post, guest notification
   - Day 1: First video/audio clip on LinkedIn and Twitter
   - Day 2: Pull quote image post, community shares
   - Day 3: Second clip on LinkedIn
   - Day 5: Reflective founder post referencing the episode
   - Day 7: Third clip, newsletter mention
3. Test the workflow end-to-end with your next episode before relying on it

### 3. Configure analytics tracking

Run the `posthog-gtm-events` drill to set up event tracking for the podcast:

Track these events in PostHog:
- `podcast_episode_published`: properties = episode_number, title, guest_name, publish_date
- `podcast_utm_click`: automatically captured via UTM parameters (utm_source=podcast)
- `podcast_lead_created`: when a contact with utm_source=podcast submits a form or books a meeting
- `podcast_episode_shared`: when the guest or a listener shares on social (logged manually or via social monitoring)

Build a basic PostHog dashboard: traffic by episode (utm_campaign breakdown), podcast referral funnel (visit -> lead -> meeting), and downloads trend from hosting platform data.

### 4. Establish weekly production cadence

Settle into a repeatable weekly rhythm:

- **Monday**: Record this week's episode (guest is pre-booked via the pipeline)
- **Tuesday**: Edit the episode, write show notes, prepare clips and social posts
- **Wednesday AM**: Publish the episode. Automated distribution fires.
- **Wednesday-Tuesday**: Automated promotion runs. Agent monitors engagement and replies to comments.
- **Friday**: Review this week's episode metrics. Source and invite next batch of guests.

Run the the podcast episode production workflow (see instructions below) drill (from Smoke level) for each episode -- but now with more polish: consistent intro/outro, better editing, branded clip templates.

### 5. Prepare repurposed content per episode

For each episode, prepare the distribution assets BEFORE publish day so the automation has content to distribute:
- 3 short clips (30-60 seconds each) extracted via Descript
- 3 LinkedIn posts (one per clip, plus the launch post)
- 3 Twitter posts
- Show notes with timestamps and takeaways
- 1 newsletter blurb
- 2-3 pull quote images

Store these in a folder per episode so the n8n automation can pull from them.

### 6. Evaluate against threshold

Run the `threshold-engine` drill after 10 episodes. Measure:
- Average downloads per episode at 7 days: target >=500
- Total qualified leads from podcast across 10 weeks: target >=10
- Guest pipeline health: are you consistently booking 3+ weeks ahead?

If PASS: Move to Scalable. The weekly cadence and automated distribution are working.
If FAIL: Diagnose. Low downloads? Check promotion reach -- are you cross-posting enough, are guests sharing? Low leads? Check your CTAs and tracking links -- are you giving listeners a clear reason to visit your site?

---

## Time Estimate
- Guest pipeline setup: 3 hours (one-time)
- Distribution automation setup: 3 hours (one-time)
- Analytics setup: 2 hours (one-time)
- Weekly episode production: ~2 hours/week x 10 weeks = 20 hours
- Weekly guest sourcing and booking: ~0.5 hours/week x 10 weeks = 5 hours

Setup: 8 hours. Ongoing: 2.5 hours/week.

---

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Buzzsprout | Podcast hosting, RSS, analytics | $12/mo (3h upload) |
| Transistor | Alternative hosting, multiple shows | $19/mo (unlimited shows) |
| Riverside | Remote recording | $15/mo (Creator plan) |
| Descript | Editing, transcription, clip extraction | $24/mo (Pro plan) |
| Cal.com | Guest booking links | Free tier or $12/mo |
| n8n | Distribution automation workflows | Self-hosted free or $20/mo cloud |
| Loops | Episode email notifications | Free: 1K contacts. $25/mo: 5K |
| PostHog | Episode attribution and analytics | Free: 1M events/mo |
| Clay | Guest prospecting and enrichment | $149/mo (Explorer) |
| Attio | Guest pipeline and episode tracking | Free tier available |

---

## Drills Referenced
- the podcast guest booking workflow (see instructions below) -- build and maintain the guest sourcing and booking pipeline
- the podcast distribution automation workflow (see instructions below) -- automated 7-day cross-platform promotion per episode
- `posthog-gtm-events` -- configure PostHog event tracking for podcast attribution
- `threshold-engine` -- evaluate downloads and leads against Baseline threshold
