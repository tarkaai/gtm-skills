---
name: twitter-dm-outreach
description: Run a structured Twitter/X engagement-to-DM sequence to book meetings with target prospects
category: Outreach
tools:
  - Twitter/X
  - Clay
  - Attio
  - PhantomBuster
fundamentals:
  - twitter-x-engagement
  - twitter-x-dms
  - clay-people-search
  - attio-contacts
  - attio-deals
---

# Twitter/X DM Outreach

This drill sets up a repeatable X outreach workflow: find prospects, warm them with engagement, DM, and convert. Works best as a parallel channel alongside `linkedin-outreach` for prospects active on both platforms.

## Input

- Scored prospect list from Clay with X/Twitter handles
- ICP definition with pain points and messaging angles
- Attio workspace for tracking conversations
- X account with DMs open and a content history (prospects check your profile before replying)

## Prerequisites

- X profile optimized: bio states who you help and what problem you solve, not your job title.
- At least 10 posts in the last 30 days so your profile looks active and credible.
- Clay table with X handles for target prospects (use `clay-people-search` to find X handles from LinkedIn URLs or email addresses).
- Attio configured with a "Twitter DM" lead source tag.

## Steps

### 1. Segment your prospect list by X activity

Pull your scored prospect list from Clay. Filter to prospects with valid X handles. Check each prospect's recent post activity using the X API search endpoint (see `twitter-x-engagement` fundamental):

```
GET https://api.x.com/2/tweets/search/recent?query=from:{username}&max_results=5
```

Segment into:
- **Active** (posted in last 14 days): Prioritize these. They check X regularly and will see your engagement.
- **Semi-active** (posted in last 60 days): Include but expect slower responses.
- **Dormant** (no posts in 60+ days): Skip for X outreach. Route to LinkedIn or email instead.

### 2. Pre-DM engagement warm-up (3-5 days)

Using the `twitter-x-engagement` fundamental, run the engagement-before-DM sequence for each active prospect:

- **Day 1**: Like 2-3 of their recent posts.
- **Day 2**: Reply to one post with a substantive comment. Add value: share a data point, a related insight, or a genuine question. Keep under 280 characters. Never mention your product.
- **Day 3-4**: Like 1-2 more posts. Retweet one if genuinely relevant to your audience.
- **Day 5**: Send the DM.

Process 10-15 prospects per day through this sequence. Stagger so you have prospects at each stage simultaneously.

### 3. Craft and send the DM

Using the `twitter-x-dms` fundamental, send a personalized DM. Structure:

**Opening** (reference their content): "Your thread on [specific topic] was sharp -- especially the point about [specific detail]."

**Bridge** (connect to the problem): "We've been working on [related problem area] and seeing [specific observation or data point]."

**Ask** (low-friction CTA): "Curious if you're seeing the same thing. Worth a 15-min chat?"

Rules:
- Under 280 characters total. Shorter DMs get higher read rates on X.
- No links in the first DM. Links trigger spam detection.
- Reference something specific from their recent posts. Generic DMs get ignored.
- Send between 8am-12pm in the prospect's timezone.

### 4. Handle responses

Using the `attio-deals` fundamental for CRM updates:

- **Positive reply** (interested, asks questions): Continue the conversation in DMs. After 2-3 message exchanges, offer a cal link: "Here's my calendar if 15 min works: [cal.com link]". Create a deal in Attio at "Meeting Booked" stage.
- **Neutral reply** (acknowledges but non-committal): Send one follow-up 3 days later with a specific value add (article, data point, case study). If no response, move to nurture list.
- **Negative reply** (not interested): Thank them, tag in Attio as "not-interested-x", do not re-contact on X.
- **No reply after 5 days**: Send one follow-up DM with a different angle. If still no reply after 5 more days, tag as "x-no-response" and route to LinkedIn or email channel.

### 5. Track and optimize

Log all activity in Attio using `attio-contacts`:
- `lead_source`: "twitter-dm"
- `x_engagement_started`: date of first like/reply
- `x_dm_sent`: date DM was sent
- `x_dm_response`: date of response (if any)
- `x_meeting_booked`: date meeting was booked (if applicable)

Benchmark targets:
- DM open rate: 60%+ (X DMs have high open rates compared to email)
- Reply rate: 15-25%
- Meeting conversion from replies: 20-30%

If below benchmarks, diagnose: low open rate = prospect is not active on X (filter better). Low reply rate = DM copy is generic or too long. Low meeting conversion = ask is unclear or timing is wrong.

## Output

- Prospects engaged and DM'd on a rolling daily basis
- All interactions logged in Attio with attribution
- Meeting bookings tracked with "twitter-dm" source
- Weekly metrics: DMs sent, reply rate, meetings booked

## Triggers

Run daily. Process 10-15 new prospects through the engagement sequence each day. This means 10-15 DMs go out daily (to prospects who completed the 5-day warm-up). Total daily time: 30-45 minutes.
