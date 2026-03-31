---
name: founder-guest-podcasts-smoke
description: >
  Founder Guest Podcast — Smoke Test. Research 10 relevant podcasts, pitch 5 hosts manually,
  and book at least 1 guest appearance to test whether podcast exposure generates inbound interest.
stage: "Marketing > Unaware"
motion: "PR & Earned Mentions"
channels: "Content"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 1 podcast guest appearance booked"
kpis: ["Pitches sent", "Reply rate", "Bookings"]
slug: "founder-guest-podcasts"
install: "npx gtm-skills add marketing/unaware/founder-guest-podcasts"
drills:
  - podcast-prospect-research
  - podcast-pitch-outreach
  - threshold-engine
---

# Founder Guest Podcast — Smoke Test

> **Stage:** Marketing → Unaware | **Motion:** PR & Earned Mentions | **Channels:** Content

## Outcomes

Book at least 1 podcast guest appearance from a cold pitch. This validates that (a) the founder has a pitchable angle, (b) relevant podcasts exist and accept guests, and (c) the pitch-to-booking pipeline works before investing in automation.

## Leading Indicators

- Podcast hosts open pitch emails (open rate > 40%)
- At least 2 hosts reply (positive or negative — proves deliverability and relevance)
- At least 1 host requests more info or a one-sheet

## Instructions

### 1. Build a short podcast prospect list

Run the `podcast-prospect-research` drill at Smoke scale:
- Search ListenNotes for 3-5 keyword combinations related to the founder's expertise
- Cross-reference by searching for 2-3 competitor or peer founder names as podcast guests
- Qualify 10 podcasts: active (episode in last 30 days), accepts guests, listen_score >= 20
- Manually find host contact info (check podcast website, RSS feed `<itunes:email>`, Twitter bio, LinkedIn)
- Store in a spreadsheet or Attio list with: podcast name, host name, contact method, topic fit (1-5)

### 2. Prepare 3 pitch angles

Define 3 distinct topics the founder can speak on. Each must be:
- Specific enough to be a standalone episode title
- Tied to a data point, contrarian take, or founder story
- Relevant to the podcast's audience (not a product pitch)

Write a 50-word bio and a 150-word bio for the founder. List 2-3 social proof points (prior talks, published work, company milestones).

### 3. Pitch 5 podcast hosts

Run the `podcast-pitch-outreach` drill at Smoke scale:
- Send 5 personalized pitch emails from the founder's personal email (not a sales tool)
- For each pitch: reference a specific recent episode, match one pitch angle to the show's topics, keep under 150 words
- Follow up once after 5 days if no reply. Follow up a second time after 12 days. Maximum 3 emails total per host.

**Human action required:** The founder sends these emails personally. Agent prepares the drafts and personalizes each one.

### 4. Handle replies

- Positive ("let's book"): Send the founder's calendar link and bio. Log booking date in Attio.
- Soft positive ("send more info"): Send the bio and 2-3 tailored topic ideas. Follow up in 3 days.
- Form redirect ("fill out our form"): Submit the guest application form. Log in Attio.
- Negative or no reply: Log and move on. Do not re-pitch for 6 months.

### 5. Evaluate against threshold

Run the `threshold-engine` drill: did you book at least 1 guest appearance? If PASS, proceed to Baseline. If FAIL, revisit pitch angles (too generic? too niche?), target podcast selection (wrong audience?), or the founder's positioning (is there a clear reason to have them on?).

## Time Estimate

- 1 hour: Podcast research and list building
- 1 hour: Pitch writing and personalization
- 1 hour: Sending, monitoring replies, follow-ups

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| ListenNotes | Podcast search and discovery | Free tier: 5 req/min ([pricing](https://www.listennotes.com/api/pricing/)) |
| Gmail/Workspace | Send pitch emails from founder's address | Included in existing email |
| Attio | Track podcast pitch status | Part of default stack |

**Estimated play-specific cost:** Free

## Drills Referenced

- `podcast-prospect-research` — find and qualify 10 target podcasts
- `podcast-pitch-outreach` — craft and send 5 personalized pitches
- `threshold-engine` — evaluate pass/fail against booking threshold
