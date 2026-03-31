---
name: pr-campaign-launch-baseline
description: >
  PR Campaign Launch — Baseline Run. Scale to 25-40 media targets using Clay enrichment and
  Instantly for sequenced outreach, add source request monitoring, and validate repeatable
  earned media generation over a coordinated 6-week launch campaign.
stage: "Marketing > ProblemAware"
motion: "PREarnedMentions"
channels: "Other, Social"
level: "Baseline Run"
time: "30 hours over 6 weeks"
outcome: ">=30 pitches sent, >=10 placements, and >=20 qualified leads from earned media within 6 weeks"
kpis: ["Pitch-to-reply rate", "Reply-to-placement rate", "Placements by outlet type", "Referral traffic per placement", "Leads from earned media", "Source request response rate"]
slug: "pr-campaign-launch"
install: "npx gtm-skills add marketing/problem-aware/pr-campaign-launch"
drills:
  - media-target-research
  - media-pitch-outreach
  - threshold-engine
---

# PR Campaign Launch — Baseline Run

> **Stage:** Marketing > ProblemAware | **Motion:** PREarnedMentions | **Channels:** Other, Social

## Outcomes

The first repeatable PR campaign. Outreach scales to 25-40 targets using Clay for enrichment and Instantly for sequenced sending. Source request monitoring (Qwoted, Featured.com) adds a reactive PR channel. The goal is proving that a coordinated launch campaign reliably produces placements and pipeline.

**Pass threshold:** >=30 pitches sent, >=10 placements, and >=20 qualified leads from earned media within 6 weeks.

## Leading Indicators

- Pitch-to-reply rate holds at 15-25% across all outlet types
- At least 2 placements per week by week 3
- Source request response rate >= 50% (responding to at least half of relevant journalist queries)
- Referral traffic from placements trends upward week over week
- At least 1 placement produces a backlink with domain authority > 30

## Instructions

### 1. Build the Enriched Media List

Run the `media-target-research` drill at Baseline scale (25-40 targets):

1. Expand the Smoke-level list: add Tier 2 (micro-newsletters) and Tier 3 (general tech media) targets
2. Use `clay-table-setup` to create the media target table with full columns (contact, outlet, beat, recent article, audience size, scores)
3. Run `clay-enrichment-waterfall` to fill email addresses: Clay email finder > Hunter.io > Apollo > manual LinkedIn lookup
4. Run `podcast-host-enrichment` for podcast targets: RSS feed email > Clay > Apollo
5. Verify all emails using Clay's built-in verification or NeverBounce
6. Score and rank all targets using the composite scoring method: relevance (40%), audience (25%), accessibility (20%), competitor coverage (15%)
7. Push scored list to Attio using `attio-lists`: create "PR Launch Campaign - {date}" list

### 2. Prepare Multi-Angle Pitch Assets

Build a complete pitch kit for the launch:

1. **Press page** (hosted on company website):
   - Company logo (PNG, SVG), founder headshot, product screenshots
   - Key stats formatted as pullable quotes
   - Company boilerplate (50-word and 150-word versions)
   - Founder bio with relevant credentials
2. **Pitch angle one-sheets** (one per angle):
   - 3-4 angles targeting different outlet types (data for journalists, ready-made draft for newsletter editors, episode topics for podcast hosts)
   - Each includes: headline, hook, key data point, available assets, talking points
3. **Embargo schedule** (if offering exclusives):
   - Tier 1 targets get exclusive access 48-72 hours before launch
   - Tier 2 targets get day-of access
   - Tier 3 targets get post-launch pitches

### 3. Execute Sequenced Outreach

Run the `media-pitch-outreach` drill at Baseline scale (25-40 pitches):

1. Segment targets by outlet type: journalists, newsletter editors, podcast hosts
2. Personalize each pitch using Clay merge fields: `contact_first_name`, `outlet_name`, `recent_article_topic`, `specific_observation`, `best_pitch_angle`
3. Set up Instantly campaigns:
   - `pr-launch-journalists-{date}`: journalist pitches, 1 follow-up
   - `pr-launch-newsletters-{date}`: newsletter pitches, 1 follow-up
   - `pr-launch-podcasts-{date}`: podcast pitches, 2 follow-ups
4. Sending schedule: Tuesday-Thursday, 7am-9am journalist timezone
5. Daily send limit: 15 per sending account
6. Hand-personalize all Tier 1 pitches. Tier 2 uses template + 3 merge fields.
7. Enable reply detection in Instantly

### 4. Set Up Source Request Monitoring

Add reactive PR to the outreach strategy:

1. Create accounts on Qwoted (free tier) and Featured.com (free tier)
2. Configure topic alerts matching your expertise areas
3. Set up an email filter or Slack integration to surface relevant requests
4. For each relevant request: evaluate fit, draft a response using Claude API, and submit
5. Track in Attio: request source, topic, journalist, deadline, response submitted, outcome (selected / not selected)

Target: respond to 5+ source requests per week. Selection rate benchmark: 20-30%.

### 5. Track the Full Pipeline

Build tracking in Attio and PostHog:

1. **Attio pipeline stages:** Sent -> Opened -> Replied -> Interested -> Covering -> Published -> Declined -> No Response
2. **PostHog events:** `pr_pitch_sent`, `pr_pitch_replied`, `pr_placement_published`, `pr_referral_click`, `pr_lead_from_media`
3. **UTM tracking:** All placement links use `?utm_source={outlet_slug}&utm_medium=earned&utm_campaign=pr-launch`
4. **Weekly metrics:** pitch-to-reply rate, reply-to-placement rate, placements this week, referral clicks, leads from PR

### 6. Amplify Every Placement

When coverage goes live:
1. Share on all social channels within 24 hours
2. Thank the journalist publicly on social
3. Add to website press page
4. Include in next newsletter
5. Log the placement URL, domain authority, and initial referral traffic in Attio and PostHog

### 7. Evaluate Against Threshold

Run the `threshold-engine` drill after 6 weeks:

1. Compile:
   - Pitches sent (threshold: >=30)
   - Placements secured (threshold: >=10)
   - Qualified leads from earned media (threshold: >=20)
2. Analyze by outlet type: which type (journalist, newsletter, podcast) produced the most placements and leads per pitch?
3. Analyze by pitch angle: which angle had the highest placement rate?
4. Calculate cost per placement and cost per PR-attributed lead

**If PASS:** Earned media is a repeatable channel. Proceed to Scalable with automation, ongoing media relationships, and continuous opportunity detection.

**If FAIL:** Diagnose:
- Low placements: pitch quality or targeting is off. Have a journalist contact review your pitches. Test different angles.
- Placements but low leads: outlets are reaching the wrong audience or landing pages are weak. Analyze which outlets drive ICP traffic vs. general traffic.
- Low source request wins: responses are too generic. Personalize responses with specific data and expert credentials.

## Time Estimate

- 6 hours: Media target research and enrichment
- 4 hours: Pitch asset preparation (press page, angle one-sheets)
- 6 hours: Pitch personalization and Instantly campaign setup
- 8 hours: Reply handling, source request responses, and placement amplification (over 6 weeks)
- 4 hours: Tracking setup and threshold evaluation
- 2 hours: Weekly pipeline review (6 weeks at ~20 min each)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Sequenced media outreach with reply detection | $30/mo (Growth) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Clay | Enrichment — media contact data and scoring | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| Qwoted | Source request monitoring (journalist queries) | Free tier or $99/mo (Pro) — [qwoted.com](https://www.qwoted.com) |
| Featured.com | Expert quote placement platform | Free tier — [featured.com](https://featured.com) |
| Attio | CRM — pitch pipeline and placement tracking | $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Analytics — referral traffic attribution | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost this level:** Qwoted free tier + Featured.com free tier + Instantly ~$30/mo = ~$30/mo play-specific. Clay, Attio, PostHog are standard stack.

## Drills Referenced

- `media-target-research` — build enriched, scored media target list using Clay with email verification and ranking
- `media-pitch-outreach` — execute sequenced outreach via Instantly, handle replies, and track the placement pipeline in Attio
- `threshold-engine` — evaluate Baseline results against the pass threshold and recommend next action
