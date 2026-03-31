---
name: podcast-launch-distribution-smoke
description: >
  Branded Podcast Launch — Smoke Test. Record and publish 3 podcast episodes, distribute manually,
  and measure whether the format generates downloads and inbound leads from problem-aware audiences.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=100 downloads and >=2 inbound leads from first 3 episodes"
kpis: ["Total downloads (all episodes)", "Inbound leads attributed to podcast", "Listener-to-website click-through rate"]
slug: "podcast-launch-distribution"
install: "npx gtm-skills add marketing/problem-aware/podcast-launch-distribution"
drills:
  - icp-definition
  - podcast-guest-preparation
  - threshold-engine
---
# Branded Podcast Launch — Smoke Test

> **Stage:** Marketing -> Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Outcomes
Prove that a branded podcast produces ANY leading indicators: downloads accumulate, at least some listeners visit your site, and at least 2 convert into identifiable leads. No paid tools required. No automation. Just record, publish, promote by hand, and measure.

## Leading Indicators
- Episode download count trending upward across the 3 episodes (episode 3 > episode 1)
- UTM-tagged clicks from podcast show notes and social posts
- At least 1 listener engages on social media (comment, DM, share)
- At least 1 listener visits your website from a podcast tracking link

---

## Budget

**Play-specific cost:** Free

- Recording: Riverside free tier (2 hours/month) or Zoom
- Hosting: Spotify for Podcasters (free) or Buzzsprout free tier (2 hours/month)
- Editing: Descript free tier (1 hour/month transcription) or GarageBand/Audacity
- Distribution: Apple Podcasts, Spotify (free directory submissions)

_Your CRM, PostHog, and automation platform are not included -- standard stack paid once._

---

## Instructions

### 1. Define your podcast ICP and positioning

Run the `icp-definition` drill to define who this podcast is for. Document:
- Target listener job titles and seniority (e.g., "seed-stage B2B SaaS founders")
- Top 3-5 pain points they search for or discuss in communities
- Competing podcasts they already listen to (search ListenNotes for 3-5 shows in your space)
- Your unique angle: what perspective can you offer that existing shows do not?

Choose a format:
- **Solo**: Founder shares insights, frameworks, lessons learned. Lowest production effort. Works when the founder has strong opinions and existing audience.
- **Interview**: Founder interviews guests. Higher production effort but brings guest audiences and cross-promotion. Best for new podcasts with small initial audience.
- **Co-host**: Two people discuss topics. Good chemistry required. Middle ground on effort.

Name the podcast. Keep it descriptive and keyword-rich for directory search (e.g., "The $0 to $1M Playbook" not "Dan's Thoughts").

### 2. Set up the podcast infrastructure

Before recording, complete the one-time setup:

1. Create a hosting platform account (Buzzsprout free tier or Spotify for Podcasters)
2. Configure show-level settings: title, description, cover art (3000x3000px square), category, language
3. Create a Riverside studio for recording
4. Create a tracking link for the podcast: `yoursite.com/podcast` redirecting to `yoursite.com/?utm_source=podcast&utm_medium=owned&utm_campaign=branded-podcast` (see `podcast-guest-preparation` drill, step 3)

**Human action required:** Design or commission podcast cover art. The cover art must be 3000x3000px square JPEG/PNG. Use your brand colors and make the podcast name readable at thumbnail size (200x200px).

### 3. Record 3 episodes

Run the the podcast episode production workflow (see instructions below) drill for each episode:

**Episode 1 (solo or interview):** Choose your strongest topic -- the one where you have the most contrarian or data-backed perspective. This is your proof-of-concept episode. Target 20-30 minutes.

**Episode 2:** If interview format, book your easiest-to-land guest (a friend, advisor, customer, or co-worker). Run `podcast-guest-preparation` to prepare talking points and tracking links. If solo, pick a different topic.

**Episode 3:** Vary the format or topic based on what felt natural in episodes 1-2. If episode 1 was solo and felt stiff, try an interview. If interviews flowed well, book another guest.

**Human action required:** The founder must record each episode. The agent prepares talking points, guest logistics, and show notes, but the founder speaks on camera/mic.

### 4. Publish and distribute manually

For each episode:
1. Edit using Descript (see the podcast episode production workflow (see instructions below) drill, step 4)
2. Upload to your hosting platform
3. After episode 1 publishes, submit the RSS feed to Apple Podcasts, Spotify, YouTube Music, and Amazon Music (one-time setup; subsequent episodes auto-distribute)
4. Write show notes with timestamps, key takeaways, and your tracking link

### 5. Promote each episode by hand

No automation at Smoke level. For each episode, do:

**On publish day:**
- Post on LinkedIn: write a hook about the episode's key insight, include 2-3 takeaways as bullets, link to the episode
- Post on Twitter/X: shorter version of the LinkedIn post, tag any guest
- Email your network: BCC relevant contacts (10-20 people) who would find the topic valuable

**Day 2-3:**
- Share in 1-2 relevant Slack or Discord communities
- Ask the guest (if any) to share with their audience
- Engage with any comments or replies on your social posts

**Human action required:** The founder posts and engages personally. This is not delegated to a tool at Smoke level.

### 6. Track results

Log performance per episode in a spreadsheet or Attio:
- Downloads at 7 days (from hosting platform dashboard)
- UTM clicks from tracking links (from PostHog)
- Social engagement (likes, comments, shares on LinkedIn/Twitter posts about the episode)
- Inbound leads: anyone who reached out, signed up, or booked a call attributable to the podcast

### 7. Evaluate against threshold

Run the `threshold-engine` drill to measure results against the pass threshold: >=100 total downloads across 3 episodes AND >=2 inbound leads.

If PASS: Move to Baseline. The podcast format works for your audience.
If FAIL: Diagnose. Check: Were the topics relevant to your ICP? Was the audio quality acceptable? Did you actually promote each episode? If promotion was weak, re-run with better distribution. If topics missed, survey 5 target listeners about what they would listen to.

---

## Time Estimate
- Infrastructure setup: 1 hour
- Episode preparation and recording (x3): 3 hours
- Editing and publishing (x3): 1.5 hours
- Manual promotion (x3): 0.5 hours

---

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Remote recording with local-quality tracks | Free: 2h/mo. Creator: $15/mo |
| Descript | Text-based audio/video editing | Free: 1h/mo transcription. Hobbyist: $24/mo |
| Buzzsprout | Podcast hosting and RSS feed | Free: 2h/mo. $12/mo: 3h |
| Spotify for Podcasters | Free podcast hosting + Spotify analytics | Free |
| PostHog | Track UTM clicks and website attribution | Free: 1M events/mo |
| Attio | Log episodes and leads in CRM | Free tier available |

---

## Drills Referenced
- `icp-definition` -- define the target listener profile and podcast positioning
- the podcast episode production workflow (see instructions below) -- record, edit, and publish each episode
- `podcast-guest-preparation` -- prepare talking points, tracking links, and guest logistics
- `threshold-engine` -- evaluate downloads and leads against pass/fail threshold
