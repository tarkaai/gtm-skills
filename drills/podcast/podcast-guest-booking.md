---
name: podcast-guest-booking
description: Build a pipeline for sourcing, qualifying, and booking guests for your branded podcast
category: Podcast
tools:
  - Clay
  - Attio
  - Instantly
  - Cal.com
  - ListenNotes
fundamentals:
  - clay-people-search
  - clay-enrichment-waterfall
  - clay-email-verification
  - attio-lists
  - attio-contacts
  - instantly-campaign
  - calcom-booking-links
  - podcast-directory-search
---

# Podcast Guest Booking

This drill builds a repeatable system for finding, qualifying, and booking guests for your branded podcast. Unlike `podcast-pitch-outreach` (which is for getting the founder ON other podcasts), this drill is for getting interesting guests ON YOUR podcast.

## Input

- Clear podcast positioning: who is the audience, what topics matter
- ICP definition: what kinds of guests would attract your target listeners
- Episode cadence: how many guests per month you need to book
- Cal.com booking link configured for podcast recording slots

## Steps

### 1. Define your ideal guest profile

Document the criteria for a good podcast guest:

**Tier 1 guests** (big names that attract new listeners):
- Recognized founders/executives in your space (10K+ LinkedIn followers or significant company)
- Published authors on relevant topics
- Prior podcast appearances on shows with listen_score > 40

**Tier 2 guests** (strong content, moderate reach):
- Domain experts with unique insights or data
- Practitioners who can share specific tactics (not just theory)
- Rising voices in your niche (2K-10K LinkedIn followers, growing fast)

**Tier 3 guests** (easiest to book, good content filler):
- Customers with compelling use cases
- Adjacent space experts who bring a fresh perspective
- Early-career practitioners with specific case studies

Target a mix: 1 Tier 1, 2 Tier 2, and 1 Tier 3 per month (for a weekly podcast).

### 2. Build the guest prospect list

Use `clay-people-search` to find potential guests:
- Search by job title + industry + follower count
- Search by company (target companies whose founders/executives would be good guests)
- Search LinkedIn posts for people writing about your podcast's topics

Use `podcast-directory-search` to find people who have already appeared on similar podcasts (they are proven podcast guests who understand the format and will say yes more often).

Create a Clay table with columns:
- Name
- Title / Company
- LinkedIn URL
- Email (to be enriched)
- Guest tier (1/2/3)
- Topic fit (what they would talk about on your show)
- Prior podcast appearances (list of shows)
- Audience reach (LinkedIn followers, Twitter followers, newsletter subscribers)
- Outreach status (not contacted / pitched / replied / booked / declined)

### 3. Enrich guest contacts

Run `clay-enrichment-waterfall` on the prospect list:
1. Find email from LinkedIn URL
2. Find email from name + company domain
3. Verify all emails with `clay-email-verification`
4. Enrich with LinkedIn data: headline, recent posts, follower count

### 4. Craft the guest invitation

Guest invitations are different from pitching yourself as a guest. You are offering them a platform. The tone is "I'd love to feature you" not "Can I come on your show."

**Email template:**

```
Subject: Invite: {{podcast_name}} — {{topic_angle}}

Hi {{first_name}},

I host {{podcast_name}}, a podcast about {{podcast_topic}} for {{target_audience}}.

I've been following your work on {{specific_thing_they_did}} and think our audience would love to hear your take on {{specific_topic}}.

The format is a {{duration}}-minute conversation — relaxed, no prep required beyond showing up. We handle all production, promotion, and distribution.

{{social_proof — e.g., "Recent guests include X, Y, Z" or "We average X downloads per episode"}}

Would you be open to recording an episode? Here's my calendar if a time works: {{calcom_link}}

{{host_name}}
Host, {{podcast_name}}
```

Key differences from guesting pitches:
- You are offering value (a platform) not asking for it
- Higher response rates (20-40% vs 10-20% for guesting pitches)
- Less follow-up needed (2 emails max, not 3)

### 5. Send invitations

**Low volume (< 10/week):** Send from the host's personal email. Personal touch matters for Tier 1 guests.

**High volume (10+/week):** Use `instantly-campaign` with the invitation template. Segment by tier: Tier 1 gets fully personalized sends from personal email, Tier 2-3 can use Instantly with merge fields.

Set up a 2-email sequence:
- Email 1: The invitation (Day 0)
- Email 2: Light follow-up with a different angle or recent episode link as social proof (Day 5)

### 6. Handle responses and book recordings

When a guest accepts:
1. Send them the Cal.com booking link (`calcom-booking-links`) for available recording slots
2. After they book, send a confirmation email with:
   - Recording logistics (Riverside link, audio setup tips)
   - 3-5 questions or topics you plan to cover (so they can think in advance)
   - Your podcast's episode format and typical length
   - Any asks: bio, headshot, social handles for show notes
3. Update Attio (`attio-contacts`): tag as "Podcast Guest — Booked", add recording date
4. Add them to the `podcast-guest-preparation` drill pipeline 5 days before recording

### 7. Build a guest pipeline dashboard

Use `attio-lists` to create a "Podcast Guest Pipeline" list with stages:
- **Sourced**: Identified as potential guest, not yet contacted
- **Invited**: Invitation email sent
- **Interested**: Replied positively, scheduling in progress
- **Booked**: Recording date confirmed
- **Recorded**: Episode recorded, in post-production
- **Published**: Episode live
- **Declined**: Not interested (do not re-invite for 12 months)

Track pipeline velocity: how many guests do you need to invite to book one? Target: 3-5 invitations per booking for Tier 2-3, 5-10 for Tier 1.

## Output

- A continuously refreshed guest prospect list in Clay
- An outreach campaign running on a regular cadence
- A booking pipeline in Attio with clear stage visibility
- Guests booked and confirmed on the recording calendar

## Triggers

- Run the prospect sourcing step monthly to refresh the pipeline
- Run the outreach step weekly to maintain booking cadence
- Run the booking/prep step per guest as responses come in
