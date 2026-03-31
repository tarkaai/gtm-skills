---
name: media-pitch-outreach
description: Craft and send personalized media pitches to journalists, newsletter editors, and podcast hosts for earned placements
category: Media
tools:
  - Instantly
  - Attio
  - Clay
  - Gmail
fundamentals:
  - media-pitch-email
  - podcast-pitch-email
  - instantly-campaign
  - attio-contacts
  - attio-notes
  - clay-enrichment-waterfall
---

# Media Pitch Outreach

This drill takes a qualified media target list and executes personalized pitch campaigns to earn press coverage, newsletter mentions, and podcast appearances. It handles pitch copy creation, personalization at scale, sending, and reply management across three outlet types: journalists, newsletter editors, and podcast hosts.

## Input

- Enriched media target list from `media-target-research` drill (in Attio or Clay)
- 3-5 pitch angles with supporting data, quotes, and assets
- Founder bio, headshot, and company one-sheet
- Company press kit URL (or page with logos, screenshots, data assets)
- Calendar link for booking calls with interested journalists

## Steps

### 1. Prepare pitch assets

Before sending any pitches, assemble these assets:

**Press kit page** (hosted on your website):
- Company logo (PNG, SVG formats)
- Founder headshot (high-res)
- Product screenshots (2-3 key screens)
- Key stats and data points (growth metrics, user numbers, market data)
- Founder bio (50-word and 150-word versions)
- Company boilerplate (2-3 sentences: what you do, who you serve, differentiator)

**Pitch angle one-sheets** (one per angle):
- Headline: the story angle in one sentence
- The hook: why this matters right now (tie to a trend or news event)
- Key data point: one specific number that makes the story credible
- Available assets: what you can provide (exclusive data, customer quotes, expert commentary)
- Talking points: 3-5 bullet points the journalist can use

### 2. Segment the target list

Pull the media target list from Attio. Segment by outlet type and pitch approach:

**Journalists (beat reporters):**
- Pitch approach: Lead with data and the news angle. Offer exclusive access.
- Use `media-pitch-email` framework.
- Follow-up: 1 follow-up maximum, tied to new news.

**Newsletter editors:**
- Pitch approach: Lead with content they can use directly. Offer a pre-written draft or data package.
- Use the newsletter variant from `media-pitch-email` framework.
- Follow-up: 1 follow-up offering a different content format.

**Podcast hosts:**
- Pitch approach: Lead with episode topics and social proof.
- Use `podcast-pitch-email` framework.
- Follow-up: Up to 2 follow-ups with alternative angles.

### 3. Personalize each pitch

For every target, populate personalization fields from Clay:

**Required merge fields (all outlet types):**
- `contact_first_name`
- `outlet_name`
- `recent_article_topic` (or `recent_episode_topic` for podcasts)
- `specific_observation` (a genuine, specific comment about their recent work)
- `best_pitch_angle` (the angle most relevant to their coverage area)

**Additional for journalists:**
- `beat_topic`
- `compelling_data_point` (matched to their beat)

**Additional for podcast hosts:**
- `recent_guest_name`
- `talking_point_1`, `talking_point_2`, `talking_point_3`

At Smoke level: write each personalization by hand after reading their recent work.
At Baseline+: Use Clay columns to store personalization variables, with human review of Tier 1 targets.

### 4. Send pitches

**Smoke (5-10 pitches):**
Send manually from the founder's personal email. Hand-personalize every pitch. Track in a spreadsheet or Attio.

**Baseline (15-30 pitches):**
Use Instantly with the `instantly-campaign` fundamental:
1. Create three campaigns by outlet type: `pr-journalists-{date}`, `pr-newsletters-{date}`, `pr-podcasts-{date}`
2. Upload contacts from Clay with merge fields mapped
3. Sending schedule: Tue-Thu, 7am-9am journalist timezone (journalists check email early)
4. Daily send limit: 15 per account
5. Set 1 follow-up for journalists/newsletters, 2 for podcasts
6. Enable reply detection

**Scalable (50+ pitches):**
Use Instantly with inbox rotation across 2-3 sending accounts. Tier-based personalization: Tier 1 gets full hand-personalization, Tier 2 gets template + 3 merge fields, Tier 3 gets template + 2 merge fields.

### 5. Handle replies

Monitor Instantly and inbox. Classify and act:

**Journalist replies:**
- "Send more info" -> Reply with press kit link and the relevant pitch angle one-sheet. Offer a 15-minute call. Update Attio: status = "interested"
- "I'll include this" -> Provide everything they need immediately: specific data, quotes, images, customer contacts. Ask about their timeline. Update Attio: status = "covering"
- "Try [colleague]" -> Thank them, pitch the referred person. Update Attio: status = "referred", create new contact for referral
- "Not a fit" -> Thank them. Update Attio: status = "declined". Re-pitch in 3 months with a different angle
- No reply -> Mark "no response". Re-pitch in 3 months with a new angle tied to news

**Newsletter editor replies:**
- "Send a draft" -> Write a 500-800 word draft tailored to their newsletter format. Include 2-3 links back to your site. Update Attio: status = "draft requested"
- "We'll mention you" -> Provide the exact quote, stat, and link you want included. Update Attio: status = "covering"
- "We accept sponsored content" -> Evaluate if the cost is worth the audience. Log the opportunity. Update Attio: status = "sponsored option"

**Podcast host replies:**
- Follow the reply handling from the `podcast-pitch-outreach` drill: book, send one-sheet, nurture, or mark declined

### 6. Track placement pipeline

Log every outreach attempt and outcome in Attio:
- **Sent**: Pitch was sent
- **Opened**: Email was opened (from Instantly tracking)
- **Interested**: Positive reply requesting more info
- **Covering**: Journalist confirmed they will cover/mention
- **Published**: Coverage went live (add the URL)
- **Declined**: Explicit no
- **No response**: Full sequence completed, no reply

Track conversion metrics:
- Pitch-to-reply rate (target: 15-25%)
- Reply-to-placement rate (target: 30-50% of positive replies)
- Overall pitch-to-placement rate (target: 5-15%)
- Average days from pitch to publication

### 7. Maximize each placement

When coverage goes live:
1. Share on all social channels within 24 hours
2. Thank the journalist/editor publicly on social media (builds the relationship)
3. Add to your press page on your website
4. Include in your next email newsletter
5. Log the placement URL, referral traffic, and any leads attributed in PostHog

## Output

- Personalized pitches sent to all targets on the media list
- Attio pipeline updated with pitch status for every contact
- Placements secured and tracked with referral traffic attribution
- Conversion metrics for optimizing future outreach batches

## Triggers

- Run once per batch of new media targets
- Re-run with new angles when you have new news (product launch, funding, data release)
- Re-run quarterly for "no response" contacts with a fresh angle
