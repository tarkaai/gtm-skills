---
name: cold-dm-linkedin-twitter-smoke
description: >
  Cold DMs on LinkedIn/Twitter — Smoke Test. Manually send 40 targeted DMs (20 LinkedIn, 20 X)
  after 3-5 days of light engagement to test whether DM-only outreach can drive replies and meetings
  without layering in email.
stage: "Marketing > ProblemAware"
motion: "OutboundFounderLed"
channels: "Social"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=2 reply-positive DMs AND >=1 meeting booked from 40 DMs"
kpis: ["Reply rate", "Positive reply rate", "Meeting book rate", "Time to first reply"]
slug: "cold-dm-linkedin-twitter"
install: "npx gtm-skills add marketing/problem-aware/cold-dm-linkedin-twitter"
drills:
  - icp-definition
  - build-prospect-list
  - threshold-engine
---

# Cold DMs on LinkedIn/Twitter — Smoke Test

> **Stage:** Marketing > ProblemAware | **Motion:** OutboundFounderLed | **Channels:** Social

## Outcomes

Send 40 cold DMs (20 on LinkedIn, 20 on X) to ICP-matching prospects after a 3-5 day engagement warm-up. Prove that DM-only outreach produces replies and meetings. No automation, no budget. Founder executes manually to learn what resonates.

**Pass threshold:** >=2 positive replies AND >=1 meeting booked from 40 DMs sent.

## Leading Indicators

- Connection/follow acceptance rate (LinkedIn): >=30% within 48 hours
- Engagement visibility (X): prospects liking back or replying to your comments within the warm-up period
- DM open rate (X shows read receipts in some cases): >=50%
- Time to first reply: <24 hours for the fastest responder

## Instructions

### 1. Define ICP and select 40 targets

Run the `icp-definition` drill to document your Ideal Customer Profile. Define: company size, industry vertical, job titles, pain points, and triggering events.

Run the `build-prospect-list` drill to source 40 contacts matching this ICP from Clay. Requirements for each contact:
- LinkedIn profile URL (mandatory for all 40)
- X/Twitter handle (mandatory for the 20 assigned to X channel)
- Company name and job title (for personalization)
- One recent post or activity to reference in your DM

Split the 40 into two groups: 20 for LinkedIn, 20 for X. Assign prospects to the channel where they are more active (check last post date on each platform).

Export the list to Attio. Tag each contact with `campaign: cold-dm-smoke` and `channel: linkedin` or `channel: x`.

### 2. Prepare message variants

Write 3 DM variants for each channel (6 total). Each variant follows this structure:

**LinkedIn DM (under 300 characters):**
- Line 1: Reference their specific post or activity. ("Your comment on [topic] caught my eye.")
- Line 2: Connect to a pain point. ("We've been digging into [related problem] and found [specific observation].")
- Line 3: Low-friction ask. ("Worth a 15-min chat? Happy to share what we're seeing.")

**X DM (under 280 characters):**
- Line 1: Reference their specific post. ("Your thread on [topic] -- especially [specific point].")
- Line 2: One-sentence bridge to the problem.
- Line 3: Question, not a pitch. ("Curious if you're seeing the same thing?")

Rules:
- No links in the first DM on either platform.
- No product pitch. The DM opens a conversation; it does not sell.
- Each variant targets a different pain point from your ICP definition.

Assign each variant to ~7 prospects per channel so you can compare response rates.

### 3. Execute engagement warm-up (Days 1-5)

**Human action required:** Execute all engagement manually.

**LinkedIn (Days 1-5):**
- Day 1-2: View the profile of each of your 20 LinkedIn targets. Like 2-3 of their recent posts.
- Day 3-4: Leave a substantive comment on one post per prospect. The comment must add value: share a data point, a related experience, or ask a genuine follow-up question. Not "Great post!"
- Day 5: Send connection request with a short note (under 200 characters). Reference the comment you left.

**X (Days 1-5):**
- Day 1: Like 2-3 recent posts from each of your 20 X targets.
- Day 2: Reply to one post per prospect with a substantive comment (under 280 characters).
- Day 3-4: Like 1-2 more posts. Retweet one post per prospect if genuinely relevant.
- Day 5: Send the DM.

Log every engagement action in Attio with the date, type (like/comment/connection request), and the prospect's response (if any).

### 4. Send DMs (Days 5-7)

**Human action required:** Send all 40 DMs manually.

**LinkedIn:** Send DMs to connected prospects. For prospects who did not accept your connection request, send an InMail if you have Sales Navigator, or skip and log as "not connected."

**X:** Send DMs to all 20 X targets. If a prospect has DMs closed, log as "dm-closed" in Attio and skip.

For each DM sent, log in Attio:
- Date and time sent
- Message variant used (A, B, or C)
- Channel (linkedin or x)

### 5. Track responses (Days 5-12)

Monitor both platforms daily for 7 days after DMs are sent. For each response:
- Classify as: positive (interested, asks question), neutral (acknowledges, non-committal), negative (not interested, asks to stop).
- Log in Attio with the classification and response text.
- For positive replies: continue the conversation. After 1-2 exchanges, offer a meeting link.
- For meetings booked: create a deal in Attio at "Meeting Booked" stage with source "cold-dm-smoke".

### 6. Evaluate against threshold

Run the `threshold-engine` drill. Pull data from Attio:
- Total DMs sent (target: 40)
- Total replies by classification (positive, neutral, negative)
- Meetings booked

**Pass:** >=2 positive replies AND >=1 meeting booked.
**Fail:** <2 positive replies OR 0 meetings.

If PASS: document which message variants, channels, and ICP segments performed best. These feed into Baseline.

If FAIL: diagnose. Low reply rate on both channels = ICP mismatch or message is too generic. Low on one channel = wrong platform for your audience. Positive replies but no meetings = ask is unclear. Revise and re-run.

## Time Estimate

- ICP definition and list building: 1.5 hours
- Message variant writing: 0.5 hours
- Engagement warm-up (20 min/day x 5 days): 1.5 hours
- DM sending and response monitoring: 1.5 hours
- **Total: ~5 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn (free account) | DMs and engagement | Free |
| X (free account) | DMs and engagement | Free |
| Clay | Prospect sourcing and enrichment | Free tier: 100 credits/mo |
| Attio | CRM tracking | Free tier: up to 3 users |

**Total play-specific cost: $0**

## Drills Referenced

- `icp-definition` -- define ideal customer profile and pain points
- `build-prospect-list` -- source and enrich 40 target prospects from Clay
- `threshold-engine` -- evaluate pass/fail against the 2-reply, 1-meeting threshold
