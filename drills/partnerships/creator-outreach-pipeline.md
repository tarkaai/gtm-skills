---
name: creator-outreach-pipeline
description: Outreach to B2B creators, negotiate sponsorship terms, and close deals
category: Influencer
tools:
  - Instantly
  - Loops
  - Passionfroot
  - Attio
  - Cal.com
fundamentals:
  - creator-outreach-message
  - instantly-campaign
  - instantly-reply-detection
  - attio-contacts
  - attio-notes
  - calcom-booking-links
---

# Creator Outreach Pipeline

This drill manages the outreach sequence from first contact to signed deal. It covers initial outreach, follow-up, negotiation, and deal closure for B2B creator sponsorships.

## Input

- Attio list of scored creator prospects (from `creator-prospect-research` drill)
- Budget per post (or total campaign budget with per-creator allocation)
- Campaign brief outline (what you want the creator to cover)
- Cal.com booking link for scheduling calls with interested creators

## Steps

### 1. Segment creators by outreach channel

From your Attio list, segment creators into outreach buckets:

- **Passionfroot creators:** book directly through the platform. No cold outreach needed.
- **Email-available creators:** use Instantly for cold outreach sequence
- **LinkedIn-only creators:** use LinkedIn DMs (manual or via automation)

Prioritize Passionfroot creators first (lowest friction). Then email. Then LinkedIn DMs.

### 2. Book Passionfroot creators

For creators with Passionfroot storefronts:
1. Select the sponsorship slot that matches your campaign format (e.g., "LinkedIn Post" or "Newsletter Mention")
2. Enter your brief summary in the booking form
3. Submit payment
4. Update Attio status to "booked"

This is the fastest path. No negotiation, no waiting. Move to step 5 (brief).

### 3. Send cold outreach via Instantly

For creators without Passionfroot, use `creator-outreach-message` to craft personalized messages. Set up an Instantly campaign using `instantly-campaign`:

**Sequence:**
- **Email 1 (Day 0):** Personalized sponsorship inquiry. Reference a specific post. State budget range. Include Cal.com link.
- **Email 2 (Day 3):** Short follow-up if no reply. "Just bumping this — would love to chat about a sponsored post. Here is a quick 15-min slot: {{calcom_link}}"
- **Email 3 (Day 7):** Final follow-up. "Last note on this — if the timing is not right, no worries at all. I will keep following your content either way."

Use `instantly-reply-detection` to pause the sequence when a creator replies.

**Campaign settings:**
- Daily send limit: 15-20 emails (creator outreach is low-volume, high-touch)
- Sending hours: 8am-6pm in the creator's timezone
- Track opens and clicks

### 4. Handle replies and negotiate

When a creator replies:
1. Update Attio status to "negotiating"
2. Log the conversation in Attio using `attio-notes`
3. If they share a rate card, log it on their contact record

**Negotiation framework:**
- If their rate is within your budget: accept and move to booking
- If their rate is 10-30% above budget: counter with your max and offer added value (e.g., "We will reshare your post to our audience of X followers")
- If their rate is 2x+ your budget: thank them, mark as "too expensive — revisit at Scalable", move to next creator
- If they counter with a package (e.g., "I will do LinkedIn + newsletter for $X"): evaluate the bundle CPL vs. individual posts

### 5. Close the deal

Once terms are agreed:
1. Confirm in writing: creator name, format, posting date, price, tracking link, payment terms
2. Update Attio status to "booked"
3. Use `calcom-booking-links` to schedule a 15-min brief call if the creator prefers verbal communication
4. Proceed to `creator-campaign-execution` drill for brief delivery and post management

### 6. Track pipeline metrics

In Attio, monitor:
- **Outreach sent:** total creators contacted
- **Reply rate:** replies / outreach sent
- **Booking rate:** deals closed / replies received
- **Average CPP (cost per post):** total spend / posts booked
- **Time to close:** days from first outreach to deal closed

## Output

- Booked creator deals with confirmed terms (format, date, price)
- Attio records updated with status, rate cards, and conversation history
- Pipeline metrics for optimizing future outreach batches

## Triggers

Run in batches of 5-10 creators at a time. At Smoke level, outreach to 3-5 creators to book 1. At Baseline, outreach to 10-15 to book 3-5. At Scalable, maintain a rolling pipeline of 20+ creators.
