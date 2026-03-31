---
name: pr-campaign-launch-smoke
description: >
  PR Campaign Launch — Smoke Test. Research 10-15 media targets, craft personalized pitches
  around a specific product launch or milestone, send manually, and validate that earned media
  outreach produces at least 3 placements and 5 qualified leads.
stage: "Marketing > ProblemAware"
motion: "PREarnedMentions"
channels: "Other, Social"
level: "Smoke Test"
time: "10 hours over 2 weeks"
outcome: ">=10 pitches sent, >=3 media placements (press mentions, podcast appearances, or newsletter features), and >=5 qualified leads from referral traffic within 2 weeks"
kpis: ["Pitches sent", "Pitch-to-reply rate", "Placements secured", "Referral clicks from placements", "Leads from earned media"]
slug: "pr-campaign-launch"
install: "npx gtm-skills add marketing/problem-aware/pr-campaign-launch"
drills:
  - media-target-research
  - media-pitch-outreach
  - threshold-engine
---

# PR Campaign Launch — Smoke Test

> **Stage:** Marketing > ProblemAware | **Motion:** PREarnedMentions | **Channels:** Other, Social

## Outcomes

Prove that earned media outreach produces coverage and referral traffic for your product. At this level, the agent researches media targets and helps craft pitches, and the founder sends them personally from their email. No tools beyond CRM and a spreadsheet. The goal is signal: do journalists, newsletter editors, and podcast hosts respond to your story?

**Pass threshold:** >=10 pitches sent, >=3 media placements (press mentions, podcast appearances, or newsletter features), and >=5 qualified leads from referral traffic within 2 weeks.

## Leading Indicators

- Pitch-to-reply rate exceeds 20% (at least 2 positive replies from 10 pitches)
- At least 1 journalist or editor asks for more information within 48 hours of pitch
- At least 1 placement goes live within 2 weeks
- Referral traffic from the first placement exceeds 50 clicks
- Founder receives at least 1 inbound inquiry mentioning the coverage

## Instructions

### 1. Define the Launch Angle

Before contacting any media, define what makes this newsworthy:

1. Identify the launch or milestone: product release, funding round, major customer win, data release, or market expansion
2. Craft 2-3 distinct pitch angles, each targeting a different audience:
   - **Data angle:** A specific metric or finding that is surprising or contrarian (e.g., "We analyzed 10,000 customer onboarding flows and found X")
   - **Trend angle:** How your launch connects to a broader industry trend the journalist is already covering
   - **Human angle:** The founder's personal story or motivation behind this milestone
3. For each angle, prepare: one headline sentence, one supporting data point, and one available asset (exclusive data, customer quote, founder interview)
4. Log all angles in Attio as notes on the PR campaign record

### 2. Research Media Targets

Run the `media-target-research` drill at Smoke scale (10-15 targets):

1. Map the media landscape: identify 5 trade publications your ICP reads, 5 micro-newsletters in your vertical, and 3-5 podcasts
2. Use free tools for search: Google (`"{your topic}" site:substack.com`), ListenNotes for podcasts, Twitter/X for active journalist identification
3. For each target, record: contact name, outlet, outlet type (journalist/newsletter/podcast), beat topics, contact email or DM channel, one recent relevant article or episode
4. Score each target on: relevance to your launch (1-5), estimated audience reach (1-5), and accessibility (verified email = 5, DM = 3, contact form = 1)
5. Rank by composite score. Select top 10-15 for outreach.

At Smoke level, skip Clay enrichment. Manual research and a spreadsheet are sufficient.

### 3. Craft Personalized Pitches

Run the `media-pitch-outreach` drill at Smoke scale (10-15 hand-written pitches):

1. For each target, select the pitch angle most relevant to their beat
2. Write a personalized pitch that includes:
   - **Opening line:** Reference their specific recent work (article, episode, or newsletter issue)
   - **The hook:** Your news in one sentence, tied to why their audience cares
   - **The proof:** One specific data point or customer result
   - **The offer:** What you can provide exclusively (data, interview, customer introduction)
   - **The ask:** Clear next step (15-minute call, or send more info)
3. Keep each pitch under 150 words. Journalists delete long emails.
4. **Human action required:** Founder sends each pitch from their personal email. Do not use a sending tool at Smoke level — personal emails have higher deliverability and trust.

### 4. Prepare Press Assets

Before sending pitches, assemble:

1. A one-page press kit (hosted as a Google Doc or Notion page): company logo, founder headshot, product screenshots, company boilerplate, and key stats
2. A data sheet for the data angle: the specific metrics or findings, presented in a shareable format
3. A founder bio (50 words and 150 words)
4. A link to the product or announcement page with UTM tracking: `?utm_source={outlet_slug}&utm_medium=earned&utm_campaign=pr-launch`

### 5. Send Pitches and Track Responses

1. Send all pitches over 2-3 days (not all at once — stagger to manage replies)
2. For each pitch, log in Attio: target name, outlet, pitch angle, date sent, status (sent / opened / replied / interested / covering / published / declined / no response)
3. Handle replies:
   - "Send more info" -> Reply within 2 hours with press kit link and the relevant asset. Offer a 15-minute call.
   - "I'll cover this" -> Provide everything they need immediately. Ask about their timeline.
   - "Not a fit" -> Thank them. Note their preferred topics for future pitches.
   - No reply after 5 days -> Send ONE follow-up with a different angle or new data point.

### 6. Amplify Placements

When coverage goes live:
1. Share on LinkedIn and Twitter within 24 hours — thank the journalist publicly
2. Add to your website press page or homepage
3. Log the placement URL in Attio with referral traffic tracking
4. Check PostHog for referral clicks from the placement over the first 7 days

### 7. Evaluate Against Threshold

Run the `threshold-engine` drill:

1. After 2 weeks, compile:
   - Pitches sent (threshold: >=10)
   - Placements secured: press mentions, podcast bookings, newsletter features (threshold: >=3)
   - Qualified leads from referral traffic: leads who arrived via placement URLs or mentioned coverage (threshold: >=5)
2. Calculate: pitch-to-reply rate, reply-to-placement rate, and leads per placement
3. Pass threshold: >=10 pitches AND >=3 placements AND >=5 qualified leads

**If PASS:** Your story has media-market fit. Proceed to Baseline with systematic outreach and tracking tools.

**If FAIL:** Diagnose:
- Low reply rate: pitch angle is weak or targets are wrong. Test a different angle. Research targets who covered competitors.
- Replies but no placements: the story lacks urgency or exclusivity. Add a time-sensitive hook or offer exclusive data.
- Placements but no leads: the coverage is reaching the wrong audience or your landing page is not converting. Check referral traffic in PostHog.

## Time Estimate

- 3 hours: Media target research (landscape mapping, contact finding, scoring)
- 3 hours: Pitch writing (10-15 personalized pitches at ~15 min each)
- 1 hour: Press asset preparation
- 2 hours: Sending, follow-ups, reply handling, and placement amplification
- 1 hour: Threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Gmail or personal email | Pitch sending | Free |
| LinkedIn | Journalist research and social amplification | Free |
| Attio | CRM — track pitch pipeline and placements | Free plan or $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Analytics — track referral traffic from placements | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |
| ListenNotes | Podcast discovery | Free tier — [listennotes.com](https://www.listennotes.com) |

**Estimated play-specific cost this level:** Free. All tools have free tiers sufficient for Smoke.

## Drills Referenced

- `media-target-research` — find, qualify, and rank journalists, newsletter editors, and podcast hosts for earned media pitching
- `media-pitch-outreach` — craft and send personalized media pitches, handle replies, and track the placement pipeline
- `threshold-engine` — evaluate Smoke test results against the pass threshold and recommend next action
